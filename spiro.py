"""
Module for drawing spiros using turtle for drawing and Pillow for saving images.
"""

import math
import turtle
import random
import argparse
from time import time

from PIL import Image


# A class that draws a Spirograph.
class Spiro:
    def __init__(self, xc, yc, col, R, r, l):
        self.t = turtle.Turtle()
        self.t.shape('turtle')

        # Set the step in degrees.
        self.step = 5
        self.drawing_complete = False

        # Set initial parameters.
        self.setparams(xc, yc, col, R, r, l)

        # Initialize the drawing.
        self.restart()

    def setparams(self, xc, yc, col, R, r, l):
        # The Spirograph parameters.
        self.xc = xc
        self.yc = yc
        self.col = col
        self.R = R
        self.r = r
        self.l = l

        # Reduce r/R to its smallest form by dividing with the GCD.
        gcd_val = math.gcd(self.r, self.R)
        self.nRot = self.r / gcd_val

        # Get ratio of radii.
        self.k = r / float(R)

        # Set the color.
        self.t.color(*col)

        # Store the current angle.
        self.a = 0

    def restart(self):
        # Set the flag.
        self.drawing_complete = False

        # Show the turtle.
        self.t.showturtle()

        # Go to the first point.
        self.t.up()
        R, k, l = self.R, self.k, self.l
        a = 0.0

        x = R * ((1 - k) * math.cos(a) + l * k * math.cos((1 - k) * a / k))
        y = R * ((1 - k) * math.sin(a) - l * k * math.sin((1 - k) * a / k))

        self.t.setpos(self.xc + x, self.yc + y)
        self.t.down()

    def draw(self):
        # Draw the whole thing.
        R, k, l = self.R, self.k, self.l

        for i in range(0, 360 * self.nRot + 1, self.step):
            a = math.radians(i)
            x = R * ((1 - k) * math.cos(a) + l * k * math.cos((1 - k) * a / k))
            y = R * ((1 - k) * math.sin(a) - l * k * math.sin((1 - k) * a / k))
            self.t.setpos(self.xc + x, self.yc + y)

        # Drawing is now done so hide the turtle cursor.
        self.t.hideturtle()

    # Update by one step.
    def update(self):
        # Skip if done.
        if self.drawing_complete:
            return

        # Increment the angle.
        self.a += self.step

        # Draw a step.
        R, k, l = self.R, self.k, self.l

        # Set the angle.
        a = math.radians(self.a)
        x = self.R * ((1 - k) * math.cos(a) + l * k * math.cos((1 - k) * a / k))
        y = self.R * ((1 - k) * math.sin(a) - l * k * math.sin((1 - k) * a / k))
        self.t.setpos(self.xc + x, self.yc + y)

        # If drawing is complete, set the flag.
        if self.a >= 360 * self.nRot:
            self.drawing_complete = True

            # Drawing is now done so hide the turtle cursor.
            self.t.hideturtle()

    # clear everything
    def clear(self):
        self.t.clear()



# A class for animating Spirographs.
class SpiroAnimator:
    def __init__(self, N):
        # Set the timer value in milliseconds.
        self.deltaT = 10

        # Get the window dimensions.
        self.width = turtle.window_width()
        self.height = turtle.window_height()

        # Create the Spiro objects.
        self.spiros = []
        for i in range(N):
            # Generate random parameters.
            rparams = self.genRandomParams()
            # Set the spiro parameters.
            spiro = Spiro(*rparams)
            self.spiros.append(spiro)

        # Call timer.
        turtle.ontimer(self.update, self.deltaT)

    # Generate random parameters.
    def genRandomParams(self):
        width, height = self.width, self.height

        R = random.randint(50, min(width, height) // 2)
        r = random.randint(10, 9 * R // 10)
        l = random.uniform(0.1, 0.9)
        xc = random.randint(-width // 2, width // 2)
        yc = random.randint(-height // 2, height // 2)
        col = (random.random(), random.random(), random.random())
        return xc, yc, col, R, r, l

    # Restart spiro drawing.
    def restart(self):
        for spiro in self.spiros:
            # clear
            spiro.clear()
            # generate random parameters
            rparams = self.genRandomParams()
            # set the spiro parameters
            spiro.setparams(*rparams)
            # restart drawing
            spiro.restart()

    def update(self):
        # update all spiros
        nComplete = 0
        for spiro in self.spiros:
            # update
            spiro.update()
            # count completed spiros
            if spiro.drawing_complete:
                nComplete += 1
        # restart if all spiros are complete
        if nComplete == len(self.spiros):
            self.restart()
        # call the timer
        turtle.ontimer(self.update, self.deltaT)

    # toggle turtle cursor on and off
    def toggleTurtles(self):
        for spiro in self.spiros:
            if spiro.t.isvisible():
                spiro.t.hideturtle()
            else:
                spiro.t.showturtle()


# save drawings as PNG files
def saveDrawing():
    # hide the turtle cursor
    turtle.hideturtle()
    # generate unique filenames
    dateStr = f'{time()}'
    fileName = 'spiro-' + dateStr
    print('saving drawing to %s.eps/png' % fileName)
    # get the tkinter canvas
    canvas = turtle.getcanvas()
    # save the drawing as a postscipt image
    canvas.postscript(file=fileName + '.eps')
    # use the Pillow module to convert the postscript image file to PNG
    img = Image.open(fileName + '.eps')
    img.save(fileName + '.png', 'png')
    # show the turtle cursor
    turtle.showturtle()


# main() function
def main():
    # use sys.argv if needed
    print('generating spirograph...')
    # create parser
    descStr = """This program draws Spirographs using the Turtle module.
    When run with no arguments, this program draws random Spirographs.
    Terminology:
    R: radius of outer circle
    r: radius of inner circle
    l: ratio of hole distance to r
    """
    parser = argparse.ArgumentParser(description=descStr)
    # add expected arguments
    parser.add_argument('--sparams', nargs=3, dest='sparams', required=False,
    help="The three arguments in sparams: R, r, l.")
    # parse args
    args = parser.parse_args()
    # set the width of the drawing window to 80 percent of the screen width
    turtle.setup(width=0.8)
    # set the cursor shape to turtle
    turtle.shape('turtle')
    # set the title to Spirographs!
    turtle.title("Spirographs!")
    # add the key handler to save our drawings
    turtle.onkey(saveDrawing, "s")
    # start listening
    turtle.listen()
    # hide the main turtle cursor
    turtle.hideturtle()
    # check for any arguments sent to --sparams and draw the Spirograph
    if args.sparams:
        params = [float(x) for x in args.sparams]
        # draw the Spirograph with the given parameters
        col = (0.0, 0.0, 0.0)
        spiro = Spiro(0, 0, col, *params)
        spiro.draw()
    else:
        # create the animator object
        spiroAnim = SpiroAnimator(4)
        # add a key handler to toggle the turtle cursor
        turtle.onkey(spiroAnim.toggleTurtles, "t")
        # add a key handler to restart the animation
        turtle.onkey(spiroAnim.restart, "space")
    # start the turtle main loop
    turtle.mainloop()


if __name__ == '__main__':
    main()
