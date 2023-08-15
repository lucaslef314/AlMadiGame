'''

background class


'''

from turtle_stuff import *
from obstacle import Obstacle
from enemy import Enemy

class BackGround:


    def __init__(self, width, height,level='1_1'):
        """Intializes the background

        Args:
            width (int): screen width
            height (int): screen height
            level (str, optional): level that is being played. Defaults to '1_1'.
        """

        #Stores width and height
        self.window_width = width
        self.window_height = height

        #Sets tile size to default
        self.tile_size = 50

        #Creates two lists, one for obstacles and one for enemies.
        self.obstacles = []
        self.enemies = []

        #Stores the ground y, the position that the blocks will be at
        self.ground_y = self.window_height//-2 + 3*self.tile_size
        self.window = make_screen(self.window_width, self.window_height, 'Super Al Madi', 'sky blue' )
        self.window.tracer(False)
        #turtle.hideturtle()
       # turtle.goto(-1000,1000)
        
        self.drawer = make_turtle('square','red',1,1,0,0)
        #self.drawer.hideturtle()
        self.read_map(level)


        #Adds new shapes to window
        self.window.addshape("breakable_block.gif")
        self.window.addshape("grass.gif")
        self.window.addshape("ground.gif")
        self.window.addshape("solid_block.gif")
        self.window.addshape("minion.gif")
        self.window.addshape("al_madi1.gif")
        self.window.addshape("al_madi2.gif")
        self.window.addshape("al_madi3.gif")
        self.window.addshape("al_madi4.gif")




    def display_text(self, x , y , color , line1, line2=''):
        """Writes text at some point

        Args:
            x (float): x position of text being written
            y (float): y position of text being written
            color (string): color of text
            line1 (string): _description_
            line2 (string, optional): Second line, defaults to None
        """

        self.drawer.goto(x,y)
        self.drawer.color(color)
        self.drawer.write(line1, font=('Arial', 16, 'normal'))

        self.drawer.goto(x,(y-25))
        self.drawer.write(line2, font=('Arial', 16, 'normal'))


    def read_map(self, level):
        '''Read the map'''
        # create an empty grid (an empty list called grid)
        self.grid = []

        level += '.txt'

        # open the text file
        file = open(level)

        # read a line from the file
        line = file.readline()

        # replace \n with nothing
        line = line.replace('\n','')

        while line:
            # split the line into tokens
            line = line.split(',')

            # add the tokens to the grid as a single row (use append)
            self.grid.append(line)

            # read a new line from the file

            line = file.readline()
            
            # replace \n with nothing in the line
            line = line.replace('\n','')
        
       


    def draw_map(self, mario_y, s_col=0, offset=0, mario_shape='al_madi1.gif'):
        ''' draws a grid at x_pos, y_pos with a specific tile_size 
        Takes the starting row of drawing and a x offset
        
        '''

        #Resets window
        self.window.reset()


        #Stores positional info for top left of the screen
        x_pos = self.window_width//-2
        y_pos = self.window_height//2
        
        
        self.drawer.shapesize(self.tile_size/20, self.tile_size/20)

        #Draws mario
        self.drawer.up()
        self.drawer.goto(0,mario_y)

        self.drawer.shape(mario_shape)
        self.drawer.stamp()

        # go over every cell in the grid and draw the positonal info
        for row in range(len(self.grid)):

            for col in range(s_col, 16 + s_col + 2):
                
                # move turtle to the position of the cell in the grid

                self.drawer.goto(x_pos - offset + (col - s_col) * self.tile_size, 
                          y_pos  - (row) * self.tile_size)
                


                # if the cell is a ground cell stamp the ground texture
                if self.grid[row][col] == 'g':

                    self.drawer.shape('ground.gif')
                    self.drawer.stamp()


                # if the cell is a grass cell stamp the grass texture
                if self.grid[row][col] == 'r':

                    self.drawer.shape('grass.gif')
                    self.drawer.stamp()   

                
                # if the cell is a block cell replace the entry with an object
                elif self.grid[row][col] == 'b':

                    self.grid[row][col] = 'rb'
                    self.obstacles.append(Obstacle(row,col,'b'))


                # if the cell is a invis-wall cell replace the entry with an object
                elif self.grid[row][col] == 'i':
 
                    self.grid[row][col] = 'ri'
                    self.obstacles.append(Obstacle(row,col,'invis'))


                # if the cell is a breakable block cell replace the entry with an object
                elif self.grid[row][col] == 'x':
  
                    self.grid[row][col] = 'rx'
                    self.obstacles.append(Obstacle(row,col,'x','destruct'))


                # if the cell is a enemy cell replace the entry with an object
                elif self.grid[row][col] == 'e':
       
                    self.grid[row][col] = 're'
                    self.enemies.append(Enemy(row,col, 'goomba'))

                # if the cell is the flagpole replace it with an object
                elif self.grid[row][col] == 'w':
       
                    self.grid[row][col] = 'we'
                    self.obstacles.append(Obstacle(row,col, 'flag', 'win'))

                
        #Draws the obstacles seperatly after they have been popped
        for obstacles in self.obstacles:
            
            self.drawer.up()

            #Figures out where to draw the obstacle
            column_pos = obstacles.col - s_col
            x_cor = x_pos - offset + (column_pos) * self.tile_size
            y_cor = y_pos  - (obstacles.row) * self.tile_size

            #Makes sure the obstacles are within the screen view and then draws it
            if (column_pos >= 0 and obstacles.active and column_pos <= 18):

                obstacles.draw_obstacle(self.drawer, x_cor, y_cor)


        #Draws the enemies seperatly 
        

        for enemy in self.enemies:
            self.drawer.up()


            #Move drawer to position of enemy
            column_pos = enemy.start_col - s_col
            x_cor = x_pos - offset + (column_pos) * self.tile_size + enemy.x_offset
            y_cor = y_pos  - (enemy.start_row) * self.tile_size + enemy.y_offset

            #Makes sure the enemies are within the screen view
            if (column_pos >= 0 and obstacles.active and column_pos <= 18):

                enemy.draw_enemy(self.drawer, x_cor, y_cor)


        #move drawer out of the way and update screen
        self.drawer.goto(-1000,1000)
        self.drawer.hideturtle()
        self.window.update()