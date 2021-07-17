"""
Lanes module for Froggit

This module contains the lane classes for the Frogger game. The lanes are the vertical
slice that the frog goes through: grass, roads, water, and the exit hedge.

Each lane is like its own level. It has hazards (e.g. cars) that the frog has to make
it past.  Therefore, it is a lot easier to program frogger by breaking each level into
a bunch of lane objects (and this is exactly how the level files are organized).

You should think of each lane as a secondary subcontroller.  The level is a subcontroller
to app, but then that subcontroller is broken up into several other subcontrollers, one
for each lane.  That means that lanes need to have a traditional subcontroller set-up.
They need their own initializer, update, and draw methods.

There are potentially a lot of classes here -- one for each type of lane.  But this is
another place where using subclasses is going to help us A LOT.  Most of your code will
go into the Lane class.  All of the other classes will inherit from this class, and
you will only need to add a few additional methods.

If you are working on extra credit, you might want to add additional lanes (a beach lane?
a snow lane?). Any of those classes should go in this file.  However, if you need additional
obstacles for an existing lane, those go in models.py instead.  If you are going to write
extra classes and are not sure where they would go, ask on Piazza and we will answer.

Kendra Obika kao78
December 20 2020
"""
from game2d import *
from consts import *
from models import *

# PRIMARY RULE: Lanes are not allowed to access anything in any level.py or app.py.
# They can only access models.py and const.py. If you need extra information from the
# level object (or the app), then it should be a parameter in your method.

class Lane(object):         # You are permitted to change the parent class if you wish
    """
    Parent class for an arbitrary lane.

    Lanes include grass, road, water, and the exit hedge.  We could write a class for
    each one of these four (and we will have classes for THREE of them).  But when you
    write the classes, you will discover a lot of repeated code.  That is the point of
    a subclass.  So this class will contain all of the code that lanes have in common,
    while the other classes will contain specialized code.

    Lanes should use the GTile class and to draw their background.  Each lane should be
    GRID_SIZE high and the length of the window wide.  You COULD make this class a
    subclass of GTile if you want.  This will make collisions easier.  However, it can
    make drawing really confusing because the Lane not only includes the tile but also
    all of the objects in the lane (cars, logs, etc.)
    """

    # LIST ALL HIDDEN ATTRIBUTES HERE

    # Attribute _tile: The GTile attribute that the lane instance is associated with
    # Invariant: _tile is a GTile

    # Attribute _objs: List of objects in the lane instance
    # Invariant: _objs is a list or None

    # Attribute _lanespeed: Speed the lane moves in number of pixels/second, if it moves.
    # Invariant: _lanespeed is a number or None


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getTile(self):
        """
        Returns the GTile object associated with the Lane instance
        """
        return self._tile

    def getObjs(self):
        """
        Returns a list of objects for a lane instance if any
        """
        return self._objs

    def getLaneSpeed(self):
        """
        Returns the speed of the lane, if there is one.
        Would not be called otherwise
        """
        return self._lanespeed

    # INITIALIZER TO SET LANE POSITION, BACKGROUND,AND OBJECTS
    def __init__(self, dic, pos, back, hitdic):
        """
        Initializes the lane position, background, and objects

        Parameter dic: dic is the main loaded JSON file
        Precondition: dic is a dictionary

        Parameter pos: pos is the order the lane goes in
        Precondition: pos is an int >= 0

        Parameter back: back is the image file of the lane
        Precondition: back is a string

        Parameter hitdic: hitdic is the JSON file for objects
        Precondition: hitdic is a dictionary
        """
        w = dic['size'][0] * GRID_SIZE
        lanes_list = dic['lanes']
        self._tile = GTile(width=w, height=GRID_SIZE, x = w/2, \
            y = GRID_SIZE*(pos+0.5), source = back)

        if "speed" in lanes_list[pos]:
            self._lanespeed = lanes_list[pos]["speed"]

        self._objs = []

        if "objects" in lanes_list[pos]:
            objects_list = lanes_list[pos]["objects"]

            for obj in objects_list:
                position = obj["position"]
                pic = obj["type"] + '.png'
                file = obj["type"]
                hitbox = hitdic["images"][file]["hitbox"]

                if "speed" in lanes_list[pos] and lanes_list[pos]["speed"] < 0:
                    self._objs.append(GImage(x = GRID_SIZE*(position+0.5), \
                    y = self._tile.y, source=pic, angle = 180, hitbox = hitbox))

                else:
                    self._objs.append(GImage(x = GRID_SIZE*(position+0.5), \
                    y = self._tile.y, source=pic, hitbox = hitbox))

    # ADDITIONAL METHODS (DRAWING, COLLISIONS, MOVEMENT, ETC)

    def update(self, dt, w, buffer):
        """
        Updates all of the obstacles in the lane

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter w: The width of a lane in pixels
        Precondition: w is a number (int or float)

        Parameter buffer: The offscreen buffer for obstacles in a lane
        Precondition: buffer is a number (int or float)
        """

        if self._tile.source == "road.png" or self._tile.source == "water.png":

            for object in self._objs:

                if self._lanespeed >= 0:
                    object.x = object.x + self._lanespeed * dt
                    if object.x > w + buffer*GRID_SIZE:
                        d = object.x - (w + buffer*GRID_SIZE)
                        object.x = -buffer*GRID_SIZE + d

                else:
                    object.x = object.x + self._lanespeed * dt
                    if object.x < -buffer*GRID_SIZE:
                        d = object.x - (-buffer*GRID_SIZE)
                        object.x = w+buffer*GRID_SIZE - d

    def draw(self, view):
        """
        To draw the background tiles and objects for the lane

        Parameter view: The game view, used in drawing
        Precondition: view is an instance of GView
        """
        self._tile.draw(view)

        for object in self._objs:
            object.draw(view)


class Grass(Lane):                           # We recommend AGAINST changing this one
    """
    A class representing a 'safe' grass area.

    You will NOT need to actually do anything in this class.  You will only do anything
    with this class if you are adding additional features like a snake in the grass
    (which the original Frogger does on higher difficulties).
    """
    pass

    # ONLY ADD CODE IF YOU ARE WORKING ON EXTRA CREDIT EXTENSIONS.


class Road(Lane):                           # We recommend AGAINST changing this one
    """
    A class representing a roadway with cars.

    If you implement Lane correctly, you do really need many methods here (not even an
    initializer) as this class will inherit everything.  However, roads are different
    than other lanes as they have cars that can kill the frog. Therefore, this class
    does need a method to tell whether or not the frog is safe.
    """
    # DEFINE ANY NEW METHODS HERE

    def car_hits_frog(self, frog):
        """
        Returns True if any car has collided and commited manslaughter on a frog.

        Parameter frog: An instance of a Frog GSprite
        Precondition: frog is a Frog (GSprite) object (or None)
        """

        if not frog is None:
            return any (car.collides(frog) for car in self.getObjs())


class Water(Lane):
    """
    A class representing a waterway with logs.

    If you implement Lane correctly, you do really need many methods here (not even an
    initializer) as this class will inherit everything.  However, water is very different
    because it is quite hazardous. The frog will die in water unless the (x,y) position
    of the frog (its center) is contained inside of a log. Therefore, this class needs a
    method to tell whether or not the frog is safe.

    In addition, the logs move the frog. If the frog is currently in this lane, then the
    frog moves at the same rate as all of the logs.
    """

    def frog_on_log(self, frog):
        """
        Returns True if any of the water's logs contains the frog's center

        Parameter frog: An instance of a Frog GSprite
        Precondition: frog is a Frog (GSprite) object (or None)
        """
        point = (frog.x, frog.y)

        return any (log.contains(point) for log in self.getObjs())

    def frogDrown(self, frog):
        """
        Returns True if the frog is on a water tile and not on a log.

        Parameter frog: An instance of a Frog GSprite
        Precondition: frog is a Frog (GSprite) object (or None)
        """
        if not frog is None:
            return (self.getTile().collides(frog) and not self.frog_on_log(frog))


class Hedge(Lane):
    """
    A class representing the exit hedge.

    This class is a subclass of lane because it does want to use a lot of the features
    of that class. But there is a lot more going on with this class, and so it needs
    several more methods.  First of all, hedges are the win condition. They contain exit
    objects (which the frog is trying to reach). When a frog reaches the exit, it needs
    to be replaced by the blue frog image and that exit is now "taken", never to be used
    again.

    That means this class needs methods to determine whether or not an exit is taken.
    It also need to take the (x,y) position of the frog and use that to determine which
    exit (if any) the frog has reached. Finally, it needs a method to determine if there
    are any available exits at all; once they are taken the game is over.

    These exit methods will require several additional attributes. That means this class
    (unlike Road and Water) will need an initializer. Remember to user super() to combine
    it with the initializer for the Lane.
    """

    # LIST ALL HIDDEN ATTRIBUTES HERE


    # Attribute _exitlist: Copied list of unoccupied exit objects, after empty, you win!
    # Invariant: _exitlist is a possibly empty list

    # Attribute _both: Copied list of both exit and (if any) open objects
    # Invariant: _both is a possibly empty list

    # Attribute _safefrogs: List of safefrog GImage objects at their specific exit
    # Invariant: _safefrogs is a possibly empty list

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO SET ADDITIONAL EXIT INFORMATION
    def __init__(self, dic, pos, back, hitdic):
        """
        Initializes lists of exit objects and safefrogs.

        Parameter dic: dic is the main loaded JSON file
        Precondition: dic is a dictionary

        Parameter pos: pos is the order the hedge goes in
        Precondition: pos is an int >= 0

        Parameter back: back is the image file of the lane ("hedge.png")
        Precondition: back is a string

        Parameter hitdic: hitdic is the JSON file for objects
        Precondition: hitdic is a dictionary
        """
        super().__init__(dic = dic, pos = pos, back = back, hitdic = hitdic)
        self._safefrogs = []
        self._both = self.getObjs().copy()
        self._exitlist = self.getObjs().copy()

        for pos in range(len(self.getObjs())):
            item = self.getObjs()[pos]
            if item.source == "open.png":
                del self._exitlist[pos]

    def draw(self, view):
        """
        To draw the safefrogs of the hedge

        Parameter view: The game view, used in drawing
        Precondition: view is an instance of GView
        """
        super().draw(view)

        if self._safefrogs != []:
            for safefrog in self._safefrogs:
                safefrog.draw(view)

    # ANY ADDITIONAL METHODS
    def frog_lands(self, frog):
        """
        Returns True if the chosen exit contains the frog

        Adds a safefrog to whichever exit the frog lands in
        Once landed, it removes that exit from being a potential landing spot

        Parameter frog: An instance of a Frog GSprite
        Precondition: frog is a Frog (GSprite) object (or None)
        """
        point = (frog.x, frog.y)

        for exit in self.getObjs():
            if not exit.source == "open.png":

                if exit.contains(point):
                    self._safefrogs.append(GImage(x = exit.x, y = exit.y, \
                        source = FROG_SAFE))
                    self._exitlist.remove(exit)
                    self._both.remove(exit)
                    return True

    def frog_in_exit(self, frog):
        """
        Returns True if the frog center would be in one of the hedge's exits that
        are unoccupied if the frog hopped up one step.

        Parameter frog: An instance of a Frog GSprite
        Precondition: frog is a Frog (GSprite) object (or None)
        """
        point = (frog.x, frog.y+GRID_SIZE)
        return any (exit.contains(point) for exit in self._both)

    def noExitsLeft(self):
        """
        Returns True if all empty exits have been filled up with safefrogs
        """
        return len(self._exitlist) == 0

# IF YOU NEED ADDITIONAL LANE CLASSES, THEY GO HERE
