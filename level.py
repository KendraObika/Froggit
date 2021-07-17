"""
Subcontroller module for Froggit

This module contains the subcontroller to manage a single level in the Froggit game.
Instances of Level represent a single game, read from a JSON.  Whenever you load a new
level, you are expected to make a new instance of this class.

The subcontroller Level manages the frog and all of the obstacles. However, those are
all defined in models.py.  The only thing in this class is the level class and all of
the individual lanes.

This module should not contain any more classes than Levels. If you need a new class,
it should either go in the lanes.py module or the models.py module.

Kendra Obika kao78
December 20 2020
"""
from game2d import *
from consts import *
from lanes  import *
from models import *

# PRIMARY RULE: Level can only access attributes in models.py or lanes.py using getters
# and setters. Level is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Level(object):
    """
    This class controls a single level of Froggit.

    This subcontroller has a reference to the frog and the individual lanes.  However,
    it does not directly store any information about the contents of a lane (e.g. the
    cars, logs, or other items in each lane). That information is stored inside of the
    individual lane objects.

    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lesson 27 for an example.  This class will be similar to that
    one in many ways.

    All attributes of this class are to be hidden.  No attribute should be accessed
    without going through a getter/setter first.  However, just because you have an
    attribute does not mean that you have to have a getter for it.  For example, the
    Froggit app probably never needs to access the attribute for the Frog object, so
    there is no need for a getter.

    The one thing you DO need a getter for is the width and height.  The width and height
    of a level is different than the default width and height and the window needs to
    resize to match.  That resizing is done in the Froggit app, and so it needs to access
    these values in the level.  The height value should include one extra grid square
    to suppose the number of lives meter.
    """

    # LIST ALL HIDDEN ATTRIBUTES HERE

    # Attribute _hitdic: JSON file for objects
    # Invariant: _hitdic is a dictionary

    # Attribute _width: The width of a level in pixels
    # Invariant: _width is a number

    # Attribute _height: The height of a level in pixels
    # Invariant: _height is a number

    # Attribute _start: The starting position coordinates of the frog
    # Invariant: _start is a number

    # Attribute _buffer: The offscreen buffer for obstacles in a lane
    # Invariant: _buffer is a number

    # Attribute _switch: A "switch" to discern between pausing and winning the game
    # Invariant: _switch is an int

    # Attribute _animator: A coroutine for performing the frog jump animation
    # Invariant: _animator is a generator-based coroutine (or None)

    # Attribute _animatorD: A coroutine for performing the death animation
    # Invariant: _animatorD is a generator-based coroutine (or None)

    # Attribute _death: An attribute for the instance of a death sprite
    # Invariant: _death is a Death (GSprite) object (or None)

    # Attribute _deathSound: The splat sound for when the frog dies
    # Invariant: _deathSound is a Sound object

    # Attribute _exitSound: The trill sound for when the frog enters an exit
    # Invariant: _exitSound is a Sound object

    # Attribute _lanes: A list of all the lanes in a json
    # Invariant: _lanes is a list consisting of Grass, Road, Water, Hedge objects

    # Attribute _frog: An attribute for the instance of a Frog GSprite
    # Invariant: _frog is a Frog (GSprite) object (or None)

    # Attribute _lives: List of frog head GImages representing the frog's lives
    # Invariant: _lives is a list consisting of GImages or empty

    # Attribute _lifelabel: The label "LIVES:" next to the frog heads
    # Invariant: _lifelabel An instance of a GLabel

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getWidth(self):
        """
        Returns the width in pixels of the level
        """
        return self._width

    def getHeight(self):
        """
        Returns the height in pixels of the level
        Includes the white life bar at the top
        """
        return self._height

    def getCenter(self):
        """
        Returns the tile of the lane that is in the center of the game
        """
        x = len(self._lanes) // 2

        return (self._lanes[x]).getTile()

    # INITIALIZER (standard form) TO CREATE THE FROG AND LANES
    def __init__(self, dic, hitdic):
        """
        Initializes the frog, lanes, sounds, and other things here and there.

        Parameter dic: dic is the main loaded JSON file
        Precondition: dic is a dictionary

        Parameter hitdic: hitdic is the JSON file for objects
        Precondition: hitdic is a dictionary
        """
        self._hitdic = hitdic
        lanes_list = dic['lanes']
        self._width = (dic['size'][0]) * GRID_SIZE
        self._height = ((dic['size'][1]) * GRID_SIZE) + GRID_SIZE
        self._start = dic["start"]
        self._buffer = dic["offscreen"]
        self._switch = 3
        self._animator = None
        self._animatorD = None
        self._death = None
        self._deathSound = Sound(SPLAT_SOUND)
        self._exitSound = Sound(TRILL_SOUND)
        self._lanes = []

        for pos in range(len(lanes_list)):
            type = lanes_list[pos]["type"]
            pic = type + '.png'

            if type == "grass":
                self._lanes.append(Grass(dic=dic,pos=pos,back=pic,hitdic=hitdic))
            if type == "road":
                self._lanes.append(Road(dic=dic,pos=pos,back=pic,hitdic=hitdic))
            if type == "water":
                self._lanes.append(Water(dic=dic,pos=pos,back=pic,hitdic=hitdic))
            if type == "hedge":
                self._lanes.append(Hedge(dic=dic,pos=pos,back=pic,hitdic=hitdic))

        self._frog = Frog(x=self._start[0],y=self._start[1],hitdic=self._hitdic)
        self._lifebar(dic['size'][1], dic['size'][0])

    # UPDATE METHOD TO MOVE THE FROG AND UPDATE ALL OF THE LANES
    def update(self, dt, input):
        """
        Moves the frog, monitors its vitals /s, and updates all the lanes

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter input: The user input, used to control the frog
        Precondition: input is an instance of GInput
        """
        self._movefrog(dt, input)

        self._killfroggy(dt)

        for lane in self._lanes:
            lane.update(dt, self._width, self._buffer)

        self._landing()

    # DRAW METHOD TO DRAW THE FROG AND THE INDIVIDUAL LANES
    def draw(self, view):
        """
        Draws the frog, lanes, death sprite, and the lifebar.

        Parameter view: The game view, used in drawing
        Precondition: view is an instance of GView
        """
        for lane in self._lanes:
            lane.draw(view)

        if not self._frog is None:
            self._frog.draw(view)

        if not self._death is None:
            self._death.draw(view)

        for life in self._lives:
            life.draw(view)

        self._lifelabel.draw(view)

    # NECESSARY (UN-HIDDEN) HELPERS

    def resetFrog(self):
        """
        Resets the frog after it's death (only if it hasn't run out of lives)
        Flips the switch back to neutral, and gets rid of the death sprite.
        """
        self._switch = 3
        self._frog = Frog(x=self._start[0],y=self._start[1],hitdic=self._hitdic)
        self._death = None

    def endGame(self):
        """
        Returns True if we should end the game.
        If safefrogs have filled each exit, switch is "flipped" and game ends.
        """
        return (self._switch == 5)

    def pauseGame(self):
        """
        Returns True if we should pause the game.
        If the frog enters an exit (not last one) or dies (with lives left),
        switch is "flipped" and we pause the game.
        """
        return (self._switch == 4)

    def noLives(self):
        """
        Returns True if the frog has run out of lives.
        If so, game is paused and ends.
        """
        return (len(self._lives) == 0)

    # NECESSARY (HIDDEN) HELPERS

    def _lifebar(self, h, w):
        """
        Initializes the life bar for the froggie :D

        Parameter h: total grids in the height (not including lives bar)
        Precondition: h is an int >= 8

        Parameter w: total grids in width
        Precondition: w is an int >= 10
        """
        self._lives = []
        for pos in range(FROG_LIVES):
            self._lives.append(GImage(x=GRID_SIZE*(w-2.5+pos),top=self._height,\
            width = GRID_SIZE, height = GRID_SIZE, source = FROG_HEAD))

        self._lifelabel = GLabel(text="LIVES:", font_name = ALLOY_FONT, \
        font_size=ALLOY_SMALL, y = GRID_SIZE*(h+0.5),right=self._lives[0].left,\
        linecolor="dark green")

    def _movefrog(self, dt, input):
        """
        Moves the frog whichever direction the user inputs with UDLR keys

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter input: The user input, used to control the frog
        Precondition: input is an instance of GInput
        """
        if not self._frog is None:
            if not self._animator is None:
                try:
                    self._animator.send(dt)
                except:
                    self._animator = None

            elif input.is_key_down("up"):
                self._frog.angle = FROG_NORTH
                if self._frog.y <= (self._height-(2*GRID_SIZE)):
                    self._hedgecontrol()

            elif input.is_key_down("down"):
                self._frog.angle = FROG_SOUTH
                if self._frog.y - GRID_SIZE > 0:
                    self._animator = self._frog.v_slide("down")
                    next(self._animator)

            elif input.is_key_down("left"):
                self._frog.angle = FROG_WEST
                if self._frog.x - GRID_SIZE > 0:
                    self._animator = self._frog.h_slide("left")
                    next(self._animator)

            elif input.is_key_down("right"):
                self._frog.angle = FROG_EAST
                if self._frog.x < (self._width-GRID_SIZE):
                    self._animator = self._frog.h_slide("right")
                    next(self._animator)
            self._waterdamage(dt)

    def _waterdamage(self, dt):
        """
        Allows the frog to take a log for a ride!
        Kills the frog if it rides offscreen

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        for lane in self._lanes:
            if isinstance(lane, Water):

                if lane.frog_on_log(self._frog) and self._animator is None:
                    self._frog.x = self._frog.x + lane.getLaneSpeed()*dt

        if self._frog.x <= 0 or self._frog.x >= self._width:
            x = self._frog.x
            y = self._frog.y
            self._frog = None
            self._animator = None
            self._morgue(x, y)

    def _hedgecontrol(self):
        """
        Stops the frog from going into the hedges but allows it to enter opens
        and/or an unoccupied exit
        """
        is_hedge = []
        lane = int(((self._frog.y-GRID_SIZE//2) + GRID_SIZE)//GRID_SIZE)

        for x in range(len(self._lanes)):
            is_hedge.append(isinstance(self._lanes[x], Hedge))

        if is_hedge[lane]:
            if self._frog.collides(self._lanes[lane-1].getTile()):
                if self._lanes[lane].frog_in_exit(self._frog):

                    self._animator = self._frog.v_slide("up")
                    next(self._animator)

        else:
            self._animator = self._frog.v_slide("up")
            next(self._animator)

    def _landing(self):
        """
        Controls the landing of the frog into an exit
        If there are exits left to enter, we pause, otherwise, we end the game.
        """
        if not self._frog is None:

            lane = int(((self._frog.y-GRID_SIZE//2) + GRID_SIZE)//GRID_SIZE)
            is_hedge = []
            onlyhedges = []

            for x in range(len(self._lanes)):
                is_hedge.append(isinstance(self._lanes[x], Hedge))
                if isinstance(self._lanes[x], Hedge):
                    onlyhedges.append(self._lanes[x])

            if is_hedge[lane]:

                if self._lanes[lane].frog_lands(self._frog):

                    self._exitSound.play()
                    self._animator = None

                    if all (hedge.noExitsLeft() for hedge in onlyhedges):
                        self._switch = 5
                        self._frog = None
                        self.endGame()
                    else:
                        self._switch = 4
                        self._frog = None
                        self.pauseGame()

    def _killfroggy(self, dt):
        """
        Kills the frog if it gets hit by a car or drowns. Calls the morgue

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if not self._animatorD is None:
            try:
                self._animatorD.send(dt)
            except:
                self._animatorD = None

        for lane in self._lanes:

            if isinstance(lane, Road):
                if lane.car_hits_frog(self._frog):
                    x = self._frog.x
                    y = self._frog.y
                    self._frog = None
                    self._animator = None
                    self._morgue(x, y)

            if isinstance(lane, Water):
                if lane.frogDrown(self._frog) and self._animator is None:
                    x = self._frog.x
                    y = self._frog.y
                    self._frog = None
                    self._animator = None
                    self._morgue(x, y)

    def _morgue(self, x, y):
        """
        Executes a few tasks after the frog dies

        Parameter x: The stored x position of the frog's final resting place
        Precondition: x is a float

        Parameter y: The stored y position of the frog's final resting place
        Precondition: y is a float
        """
        self._death = Death(x, y, self._hitdic)
        self._deathSound.play()

        self._animatorD = self._death.animate()
        next(self._animatorD)

        del self._lives[-1]
        self._switch = 4
        self.pauseGame()
