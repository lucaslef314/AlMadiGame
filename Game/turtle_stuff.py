
'''
Library of the functions associated with turtle



'''

from turtle import Screen, Turtle



def make_screen(width, height, title, color='black'):
    '''Makes a `Screen` object: the window in each turtles can draw shapes

    Parameters:
    -----------
    width: int.
        The width of the window/screen in pixels.
    height: int.
        The height of the window/screen in pixels.
    title: str.
        The name that you'd like to call the pop-up window. Appears at the center of top of the window.
    color: str.
        Color string name (e.g. 'black', 'white', etc). This is the background color of the screen.

    Returns:
    -----------
    The `Screen` object that you create.
    '''
    screen = Screen()
    screen.setup(width,height)
    screen.bgcolor(color)
    screen.title(title)
    #turtle.tracer(False)
    # turtle.hideturtle()
    

    return screen


def make_turtle(shape, color, stretch_width, stretch_length, x_pos, y_pos):
    """Returns a turtle of given parameters

    Args:
        shape (string):'arrow', 'turtle', 'circle', 'square', 'triangle', 'classic'
        color (string): name of color
        stretch_width (float): default 20, increases the strech of width
        stretch_length (float): default 20, increases the strech of height
        x_pos (float): sets x position 
        y_pos (float): sets y position

    Returns:
        new_turtle: Created turtle of these atributes
    """

    #Creates the turtle
    new_turtle = Turtle()
    new_turtle.shape(shape)
    new_turtle.shapesize(stretch_width,stretch_length)
    new_turtle.color(color)
    new_turtle.penup()
    new_turtle.setpos(x_pos,y_pos)
    new_turtle.hideturtle()
    

    return new_turtle