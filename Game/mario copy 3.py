'''
name: name.py
author: Lucas Lefebvre
course: CS151 section B
date (last edit): 4/3/2023

Description


'''

'''
Important Numbers
Tile size 50

Screen width: 16 Tiles
Screen height: 14 tiles
Width: 800
Height: 700

'''


from turtle import Screen, Turtle
import time
#import playsound


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
    # turtle.tracer(False)
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


class Game:

    def __init__(self, level='1_1'):
        '''Intializes the game.
        Takes in a level to load. Currently the only levels are 1_1 and 1_0
        '''
        
        #Creates the background
        self.background = BackGround(800,700, level)
        
        #Using the window height and tile size figures out what the ground 
        #Then creates the mario object with this info
        self.mario = Mario(self.background.ground_y)

        #Sets all of the keybindings
        self.background.window.listen()
        self.background.window.onkeypress(self.mario.jump,'w')
        self.background.window.onkeypress(self.mario.left,'a')
        self.background.window.onkeypress(self.mario.right,'d')

        #These keybindindings are needed so that one can hold a key down
        self.background.window.onkeyrelease(self.mario.right_stop, 'd')
        self.background.window.onkeyrelease(self.mario.left_stop, 'a')

        #Draws the intial map
        self.background.draw_map(0,0,0)

    
    def game_update(self):
        '''This runs in a while loop. Updates the game and checks collisions'''

        #updates accel based on ground - also need to check if no ground

        object_out = (self.mario.check_object(self.background))

        ground_out = self.mario.check_ground(self.background)
        
        en_out = self.mario.check_enemies(self.background)

        #Checks if mario dies
        if en_out == 'death' or ground_out == 'death':
            return True


        #Applies gravity (updates y-velocity and y-position)
        self.mario.gravity()
        
        #Moves Goomba's
        for enemy in self.background.enemies:

            enemy.move_forward()
            enemy.check_objects(self.background)
        
        #Draws mario
        offset = self.mario.x_cor
        self.background.draw_map(self.mario.y_cor,int(offset//50),offset%50)


    
                
                



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
        self.window.addshape("al_madi1.gif")

        #self.window.bgcolor('sky blue')


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
        
        #print(self.grid)


    def draw_map(self, mario_y = 'def', s_col=0, offset=0):
        ''' draws a grid at x_pos, y_pos with a specific tile_size 
        Takes the starting row of drawing and a x offset
        
        '''

        #Resets window
        self.window.reset()

        # move turtle to initial drawing position

        x_pos = self.window_width//-2
        y_pos = self.window_height//2
        if mario_y == 'def':
            mario_y = self.window_height//-2 + 2 * self.tile_size

        #self.drawer = self.drawer

        
        mario_y = mario_y #-y_pos + self.tile_size * 3 + mario_y

        self.drawer.shape('square')
        self.drawer.color('blue')
        self.drawer.shapesize(self.tile_size/20, self.tile_size/20)

        self.drawer.up()
        self.drawer.goto(0,mario_y)
        self.drawer.shape("al_madi1.gif")
        self.drawer.stamp()
        self.drawer.down()

        self.drawer.up()
        self.drawer.goto(x_pos, y_pos)
        self.drawer.down()


        # go over every cell in the grid
        for row in range(len(self.grid)):

            for col in range(s_col, 16 + s_col + 2): #len(self.grid[row])):
                
                # move turtle to the position of the cell in the grid
                self.drawer.up()
                self.drawer.goto(x_pos - offset + (col - s_col) * self.tile_size, 
                          y_pos  - (row) * self.tile_size)
                self.drawer.down()


                # if the cell is a ground cell stamp the ground texture
                if self.grid[row][col] == 'g':

                    self.drawer.shape('ground.gif')
                    self.drawer.stamp()


                # if the cell is a grass cell stamp the grass texture
                if self.grid[row][col] == 'gr':

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
        

class Mario:

    def __init__(self, ground_y):
        '''Intializes the mario class. Needs to know what the ground y is'''
        
        #Position information
        self.ground_y = ground_y
        
        self.x_cor = 0
        self.y_cor = ground_y
        

        #physics info
        self.y_vel = 0
        self.start_y_vel = 20
        self.x_vel = 0
        self.max_x_vel = 8
        self.y_accel = 0
        self.x_accel = 0
        
        #Bools needed for movement
        self.right_held = False
        self.left_held = False

        self.falling_to_death = False
        

    def right(self):
        '''Increases x-vel as long as key is held and not max velocity'''
        
        self.right_held = True

        while self.right_held and (self.x_vel < self.max_x_vel):
            self.x_vel += .5


    def right_stop(self):
        '''Stop increasing x-vel when d is let go'''
        self.right_held = False


    def left(self):
        '''Increases negative x-vel as long as key is held and not max velocity'''
        self.left_held = True

        while self.left_held and self.x_vel > -self.max_x_vel:
            self.x_vel -= .5


    def left_stop(self):
        '''Stop increasing negative x-vel when d is let go'''
        self.left_held = False


    


    def jump(self):
        '''Jumps by setting velocity if acceleration is zero (on ground)'''

        if self.y_accel == 0: 

            self.y_cor += 1
            self.y_vel = self.start_y_vel
            self.y_accel = -1



    def check_ground(self, background):
        '''Checks if mario is on the ground or falling to death'''

        #If y_cor is really low, then kills mario
        if self.y_cor <= (self.ground_y - background.tile_size * 4):
            return 'death'

        #If mario is currently falling to death stop ground check
        # (there is no escape)
        if self.falling_to_death:
            return True

        #Checks ground level to see if it is a ground. If not fall to death
        col = int(self.x_cor/50) + 8
        if background.grid[13][col] == '0' and self.y_cor <= self.ground_y:
            self.y_accel = -1
            self.falling_to_death = True
            return True

        #If on the ground stop accel
        if self.y_cor < self.ground_y:
            self.y_cor = self.ground_y
            self.y_accel = 0
            return True

        #Once they equal don't reset acceleration (So they can jump)
        elif self.y_cor == self.ground_y:
            return True
           

    def gravity(self):
        '''Updates velocity based on gravity. Also moves mario based on velocity'''
       
        #Updates y velocity if there is acceleration.
        if  self.y_accel != 0:

            self.y_cor += self.y_vel
            self.y_vel += self.y_accel
        
        #If there isn't acceleration then set velocity to zero
        else:
            self.y_vel = 0

        #Updates x velocity
        if self.x_vel != 0:

            #Moves mario by x velocity
            self.x_cor += self.x_vel

            #If not currently moving, decrease velocity to move towards stop
            if self.x_vel > 0 and not self.right_held:
                self.x_vel -= 1
            elif self.x_vel < 0 and not self.left_held:
                self.x_vel += 1



    def check_enemies(self, background):
        ''''''
        en_list = background.enemies
        hit_radius = background.tile_size - 2

        for enemy in en_list:

            if (abs(enemy.x_cor) < hit_radius
            and abs(enemy.y_cor - self.y_cor) < hit_radius):
                

                if self.y_vel != 0:

                    self.y_vel = 12
                    enemy.on_top_hit()
                    

                else:

                    return 'death'




    def check_object(self, background):
        '''Checks if Mario is collided with an object'''

        ob_list = background.obstacles
        sc_bottom = -(background.window_height//2)
        #mario_y_cor =  sc_bottom + background.tile_size * 3 + self.y_cor
        hit_radius = background.tile_size

        for obstacle in ob_list:
            ''''''
            #Checks if there is a collision
            no_col = False

            is_inside = abs(obstacle.y_cor - self.y_cor) < (hit_radius/1.8)
            within_range = (abs(obstacle.x_cor) < hit_radius 
                            and abs(obstacle.y_cor - self.y_cor) < hit_radius*1.2)
            
            if (abs(obstacle.x_cor) < hit_radius*.8
            and abs(obstacle.y_cor - self.y_cor) < hit_radius*.8):
                
                # print(self.y_cor)
                # print(obstacle.y_cor)

                #Top of mario hits block
                if self.y_vel > 0:
                    #print('up hit')
                    self.y_vel = -2
                    self.y_cor -= 10
                    #self.top_col = True
                    obstacle.on_top_hit()
                    return 'top'
                    
                #Bottom of Mario hits block
                elif self.y_vel < 0:
                    #print('bottom hit')
                    #self.mario.y_vel = 0
                    self.y_accel = 0
                    self.y_cor = obstacle.y_cor + background.tile_size 
                    obstacle.holding_mario = True
                    #self.bottom_col = True
                    return 'bottom'
            
                
                elif  (obstacle.x_cor < 0 and not obstacle.holding_mario): #and not self.top_col:
                    self.x_vel = 0
                   # self.side_col = True
                    self.x_cor += 10
                    #return 4
                    return 'right'

                elif  (obstacle.x_cor > 0 and not obstacle.holding_mario): # and not self.top_col:
                    self.x_vel = 0
                    #self.side_col = True
                    self.x_cor -= 10
                    #return 5
                    return 'left'


            elif obstacle.holding_mario and not within_range:
                self.y_accel = -1
                obstacle.holding_mario = False

        #return 'air'



class Enemy:

    def __init__(self, row, col, en_type):
        self.start_row = row
        self.start_col = col
        self.x_cor = 999
        self.y_cor = 999
        self.speed = 2
        self.en_type = en_type
        self.x_offset = 0
        self.y_offset = 0
        self.direction = -1
        self.active = True



    def draw_enemy(self, turt, x_cor, y_cor):
        ''''''

        if not self.active:
            return
        

        self.x_cor = x_cor
        self.y_cor = y_cor


        turt.color('orange')

        turt.up()
        turt.goto(x_cor, y_cor)
        turt.stamp()
        


    def on_top_hit(self):

        if self.en_type == 'empty':
            return
        
        elif self.en_type == 'goomba':
            '''destroy item'''
            self.x_cor = -999
            self.y_cor = -999
            self.active = False


    def move_forward(self):
        self.x_offset += self.direction*self.speed

        if self.x_offset >= 50:
            self.x_offset -= 50
            self.start_col += 1

        if self.x_offset <= -50:
            self.x_offset += 50
            self.start_col -= 1
        



    def check_objects(self, background):

        ob_list = background.obstacles

        hit_radius = background.tile_size
        left_goomba = self.x_cor - hit_radius/2
        right_goomba = self.x_cor + hit_radius/2
        
        #checks if it needs to turn around
        if background.grid[13][self.start_col] == '0':
            
            if self.direction > 0:
                self.start_col -= 1

            else:
                self.start_col += 1
                
            self.direction *= -1

        for obstacle in ob_list:

            #Checks again if it needs to turn around
            if (abs(obstacle.col - self.start_col) <= 1 
                and obstacle.row == self.start_row):
                
                if self.direction > 0:
                    self.start_col -= 1

                else:
                    self.start_col += 1
                
                self.direction *= -1

            if (self.start_row != 11):
                
                if (background.grid[self.start_row + 1][self.start_col] == '0'):
                    self.start_row += 1

                
        

                




class Obstacle:

    def __init__(self, row, col, ob_type, item='empty'):
        ''''''
        self.row = row
        self.col = col
        self.x_cor = 999
        self.y_cor = 999
        self.item = item
        self.type = ob_type
        self.active = True
        self.holding_mario = False


    def draw_obstacle(self, turt, x_cor, y_cor):
        ''''''
        self.x_cor = x_cor
        self.y_cor = y_cor



        if self.type == 'invis':
            return
        

        if self.type == 'b':
            #turt.color('brown')
            turt.shape('solid_block.gif')

        
        if self.type == 'x':
            turt.shape('breakable_block.gif')
            
        

        turt.up()
        turt.goto(x_cor, y_cor)
        turt.stamp()
        turt.goto(-1000,1000)

        #turt.color('white')


    def on_top_hit(self):

        if self.item == 'empty':
            return
        
        elif self.item == 'destruct':
            '''destroy item'''
            self.x_cor = -9999
            self.y_cor = -9999
            self.active = False




def main():
    '''Main funcion'''
    lives = 5
    #turtle.hideturtle()
    #test = make_turtle('square', 'sky blue', 50/20, 50/20, 0,0)
    
    while True:
        print(lives)
        
        game = Game()
        restart = True
        #game.read_map('1_1')


        while restart:
            death = game.game_update()
            #game.background.window.update()
            
            #Could add death animation

            if death:
                time.sleep(1)
                restart = False

        if lives > 0:
            del game.background
            lives -= 1
            del game
        
        else:
            break
        #Reduce lives and check if no lives left

        


if __name__ == '__main__':
    main()

    # if self.turt.distance(alien.turt) < 20:
    #     return True