'''



'''

from turtle_stuff import *


class Text:

    instance_list = []

    def __init__(self,  x , y , color , line1, frames=50, line2=''):
        '''Makes a text box at a set location that lasts for a set amount of time.'''

       

        self.x = x
        self.y = y
        self.color = color

        self.drawer = make_turtle('classic', color, 1 , 1, x, y)
        self.drawer.up()
        self.drawer.hideturtle()
        self.frames = frames
        self.line1 = line1
        self.line2 = line2
        
        Text.instance_list.append(self)
        #print(len(Text.instance_list))

    def print_text(self):

        self.drawer.clear()
        self.drawer.up()
        self.drawer.color(self.color)

        if self.frames > 0:

            self.drawer.goto(self.x,self.y)
            self.drawer.write(self.line1, font=('Arial', 16, 'normal'))

            self.drawer.goto(self.x,(self.y-25))
            self.drawer.write(self.line2, font=('Arial', 16, 'normal'))

            
            self.frames -= 1

        # else:

        #     index = Text.instance_list.index(self)
        #     Text.instance_list.pop(index)
        
        self.drawer.goto(1000,1000)

    def resume_text(self, frames, line1='nope', line2='nope'):
        '''Returns a text object once it runs out of frames, hopefully less laggy than making more'''

        self.frames = frames
        
        if line1 != 'nope':
            self.line1 = line1

        if line2 != 'nope':
            self.line2 = line2

    
            
