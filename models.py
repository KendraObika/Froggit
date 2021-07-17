"""
Models module for Froggit

This module contains the model classes for the Frogger game. Anything that you
interact with on the screen is model: the frog, the cars, the logs, and so on.

Just because something is a model does not mean there has to be a special class for
it. Unless you need something special for your extra gameplay features, cars and logs
could just be an instance of GImage that you move across the screen. You only need a new
class when you add extra features to an object.

That is why this module contains the Frog class.  There is A LOT going on with the
frog, particularly once you start creating the animation coroutines.

If you are just working on the main assignment, you should not need any other classes
in this module. However, you might find yourself adding extra classes to add new
features.  For example, turtles that can submerge underneath the frog would probably
need a custom model for the same reason that the frog does.

If you are unsure about  whether to make a new class or not, please ask on Piazza. We
will answer.

Kendra Obika kao78
December 20 2020
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py.  If you need extra information from a lane or level object, then it
# should be a parameter in your method.


class Frog(GSprite):         # You will need to change this by Task 3
    """
    A class representing the frog

    The frog is represented as an image (or sprite if you are doing timed animation).
    However, unlike the obstacles, we cannot use a simple GImage class for the frog.
    The frog has to have additional attributes (which you will add).  That is why we
    make it a subclass of GImage.

    When you reach Task 3, you will discover that Frog needs to be a composite object,
    tracking both the frog animation and the death animation.  That will likely cause
    major modifications to this class.
    """

    # LIST ALL HIDDEN ATTRIBUTES HERE

    # Attribute _jumpSound: The ribbit sound for when the frog jumps
    # Invariant: _jumpSound is a Sound object

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO SET FROG POSITION

    def __init__(self, x, y, hitdic):
        """
        Initializer to set the frog's position and sound

        Parameter x: The frog's starting horizontal grid position
        Precondition: x is a float or int

        Parameter y: The frog's starting vertical grid position
        Precondition: y is a float or int

        Parameter hitdic: hitdic is the JSON file for objects
        Precondition: hitdic is a dictionary
        """

        hitboxes = hitdic["sprites"]["frog"]["hitboxes"]
        format = hitdic["sprites"]["frog"]["format"]
        image = hitdic["sprites"]["frog"]["file"]

        super().__init__(x = (x+0.5) * GRID_SIZE, y = (y+0.5) * GRID_SIZE, \
            source = image, format = format, hitboxes = hitboxes)

        self.angle = FROG_NORTH
        self.frame = 0
        self._jumpSound = Sound(CROAK_SOUND)

    # ADDITIONAL METHODS (DRAWING, COLLISIONS, MOVEMENT, ETC)

    def v_slide(self, direction):
        """
        Coroutine to animate frog sliding vertically

        Parameter direction: The direction the frog is hopping, up or down
        Precondition: direction is a string
        """
        self._jumpSound.play()

        start = self.y

        if direction == 'up':
            final = start + GRID_SIZE
        else:
            final = start - GRID_SIZE

        steps = (final-start)/FROG_SPEED
        animating = True
        while animating:
            dt = (yield)
            amount = steps*dt
            self.y = self.y+amount

            if abs(self.y-start) >= GRID_SIZE:
                self.y = final
                animating = False

            self._animation(self.y, start, final, direction)

    def h_slide(self, direction):
        """
        Coroutine to animate frog sliding horizontally

        Parameter direction: The direction the frog is hopping, left or right
        Precondition: direction is a string
        """
        self._jumpSound.play()

        start = self.x

        if direction == 'right':
            final = start + GRID_SIZE
        else:
            final = start - GRID_SIZE

        steps = (final-start)/FROG_SPEED
        animating = True
        while animating:
            dt = (yield)
            amount = steps*dt
            self.x = self.x+amount

            if abs(self.x-start) >= GRID_SIZE:
                self.x = final
                animating = False

            self._animation(self.x, start, final, direction)

    def _animation(self, xy, start, final, direction):
        """
        Controls the sprite animations for the frog in the horizontal direction

        Parameter xy: The x or y value of the frog
        Precondition: xy is a float stored in the attribute

        Parameter start: The starting value of the frog attribute
        Precondition: start is a float

        Parameter final: The final value of the frog attribute
        Precondition: final is a float

        Parameter direction: The direction the frog is hopping
        Precondition: direction is a string
        """
        #Copied and adapted from sample code's coroutine2.py file.

        frac = 2*(xy-start)/(final-start)

        if frac < 1:
            if direction == 'right' or direction == "up":
                frame = POSITION_NEUTRAL+frac*(POSITION_FIRST-POSITION_NEUTRAL)
                self.frame = round(frame)
            elif direction == 'left' or direction == "down":
                frame = POSITION_NEUTRAL+frac*(POSITION_LAST-POSITION_NEUTRAL)
                self.frame = round(frame)

        else:
            frac = frac-1
            if direction == 'right' or direction == "up":
                frame = POSITION_FIRST+frac*(POSITION_NEUTRAL-POSITION_FIRST)
                self.frame = round(frame)
            elif direction == 'left' or direction == "down":
                frame = POSITION_LAST+frac*(POSITION_NEUTRAL-POSITION_LAST)
                self.frame = round(frame)


# IF YOU NEED ADDITIONAL CLASSES, THEY GO HERE

class Death(GSprite):
    """
    A class representing the death sprite
    """

    # INITIALIZER TO SET FROG POSITION

    def __init__(self, x, y, hitdic):
        """
        Initializer to set the death sprite's position

        Parameter x: The death sprite's horizontal grid position
        Precondition: x is a float or int

        Parameter y: The death sprite's starting vertical grid position
        Precondition: y is a float or int

        Parameter hitdic: hitdic is the JSON file for objects
        Precondition: hitdic is a dictionary
        """

        format = hitdic["sprites"]["skulls"]["format"]
        image = hitdic["sprites"]["skulls"]["file"]

        super().__init__(x = x, y = y, source = image, format = format)
        self.frame = 0

    def animate(self):
        """
        Coroutine to animate the skulls

        Changes the frame of the skull from 0 to 7 over the time DEATH_SPEED

        I know this is incorrect, but alas :(
        """

        start = DEATH_FIRST
        final = DEATH_LAST

        s_frame = self.frame
        f_frame = s_frame + 7

        #steps = (final-start)/DEATH_SPEED
        animating = True
        current = 0

        while animating:

            dt = (yield)
            print (dt)
            #amount = steps*dt
            current = dt*3+current

            frac = 7*(current-0)/(DEATH_SPEED-0)
            frame = frac*(DEATH_LAST-DEATH_FIRST)

            self.frame = round(frame)

            if self.frame == 7:
                animating = False
