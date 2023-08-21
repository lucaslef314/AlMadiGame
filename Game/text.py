'''



'''

from turtle_stuff import *


class Text:
    
    #Stores all created text boxes
    instance_list = []

    def __init__(self,  x , y , color , line1, frames=50, line2=''):
        """Makes a text box at a set location that lasts for a set amount of time.

        Args:
            x (int): x location of text - not centered
            y (int): y location of text - not centered
            color (string): color of text
            line1 (string): first line of text
            frames (int, optional): Time text lasts for. Defaults to 50.
            line2 (str, optional): Second line of text. Defaults to '', empty.
        """
        ''''''

       
        #Store info
        self.x = x
        self.y = y
        self.color = color
        self.frames = frames
        self.line1 = line1
        self.line2 = line2

        #Setup turtle
        self.drawer = make_turtle('classic', color, 1 , 1, x, y)
        self.drawer.up()
        self.drawer.hideturtle()
        
        #Add to list of all texts
        Text.instance_list.append(self)
       

    def print_text(self):
        """prints a given text box on a location in the right color
        """
        #clears previous text and sets props
        self.drawer.clear()
        self.drawer.up()
        self.drawer.color(self.color)

        #checks if text has frames left
        if self.frames > 0:

            self.drawer.goto(self.x,self.y)
            self.drawer.write(self.line1, font=('Arial', 16, 'normal'))

            self.drawer.goto(self.x,(self.y-25))
            self.drawer.write(self.line2, font=('Arial', 16, 'normal'))

            
            self.frames -= 1

        #move off-screen
        self.drawer.goto(1000,1000)


    def resume_text(self, frames, line1='nope', line2='nope'):
        """Returns a text object once it runs out of frames, hopefully less laggy than making more
        Can change some things about the field

        Args:
            frames (int): new amount of frames
            line1 (str, optional): new line1. Defaults to no change.
            line2 (str, optional): new line2. Defaults to no change.
        """


        self.frames = frames
        
        if line1 != 'nope':
            self.line1 = line1

        if line2 != 'nope':
            self.line2 = line2

    
            
