'''
name: mario.py
author: Lucas Lefebvre
course: CS151 section B
date (last edit): 5/3/2023

Plays a version of the classic game super mario bros.


Important Numbers
Tile size 50

Screen width: 16 Tiles
Screen height: 14 tiles
Width: 800
Height: 700

'''


from turtle import Screen, Turtle
import time



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
        self.level = level
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

        #Score Variables
        self.score = 0

    
    def game_update(self):
        '''This runs in a while loop. Updates the game and checks collisions'''

        #updates accel based on ground - also need to check if no ground

        object_out = (self.mario.check_object(self.background))

        ground_out = self.mario.check_ground(self.background)
        
        en_out = self.mario.check_enemies(self.background)


        #Checks if mario dies
        if en_out == 'death' or ground_out == 'death':
            return 'death'
        
        if object_out == 'win':
            return 'win'
        
        
        elif type(object_out) == int:
            
            self.score += object_out

            self.background.display_text(0, self.mario.y_cor,
                                         'red', object_out)
        
        if type(en_out) == int:
            
            self.score += en_out
            self.background.display_text(0, self.mario.y_cor,
                                         'red', en_out)
        
        
        self.background.display_text(0, self.background.window_height//2.2, 'black',
                                     'Score:',self.score )

       

        #Applies gravity (updates y-velocity and y-position)
        self.mario.gravity()
        
        #Moves Goomba's
        for enemy in self.background.enemies:

            enemy.move_forward()
            enemy.check_objects(self.background)
        
        #Draws mario
        shape = self.mario.shape()
        offset = self.mario.x_cor
        self.background.draw_map(self.mario.y_cor,int(offset//50),offset%50, shape)


    def life_update(self, lives):

        self.background.window.bgcolor('black')

        self.background.display_text(0,0, 'white',lives, 'Lives Remaining')

        time.sleep(1)
        self.background.window.bgcolor('sky blue')
        #self.background = BackGround(800,700, self.level)

    def won(self):
        
        self.background.window.bgcolor('black')
        line1 = "Congratulations you have completed the level!"
        line2 = "You got a score of " + str(self.score) + " !"

        self.background.drawer.clear()
        self.background.display_text(-200,0, 'white',line1, line2)
        time.sleep(3)

        



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
        
        self.animation = 10

        self.falling_to_death = False
        

    def shape(self):
        """Returns the shape that is in the correction direction and frame of the
        al-madi running animation

        Returns:
            string: name of the gif: al_madix.gif where x is determined by function
        """

        #If al-madi isn't moving reset animation
        if self.x_vel == 0:
            return "al_madi1.gif"

        #increase animation frame and then check if needs to be reset
        self.animation += 1

        if self.animation >= 40:
            self.animation -= 40
        
        #If the frame is greater than 20 use the second texture, else use the first
        if self.animation > 20:
            shape_num = 2
        else:
            shape_num = 1

        
        #Finally if Mario is moving to the left use the left moving sprites
        if self.x_vel < 0:
            shape_num += 2

    
        #Returns the name of the shape based on my naming scheme
        shape = 'al_madi' + str(shape_num) + '.gif'

        return shape
    

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
        '''Goes through the list of enemies and checks if there is a collision
        Takes in a background so that it can access size information and the 
        enemy list

        Returns death if mario collides with an enemy without velocity
        '''
        #Sets variables
        en_list = background.enemies
        hit_radius = background.tile_size - 2

        #For each enemy checks collisions
        for enemy in en_list:

            if (abs(enemy.x_cor) < hit_radius
            and abs(enemy.y_cor - self.y_cor) < hit_radius):
                
                #If mario has velocity it means that he will smush the goomba
                #Runs the appropriate function in the enemy for this condition
                if self.y_vel != 0:

                    self.y_vel = 12
                    out = enemy.on_top_hit()
                    return out
                    
                #if not then he is dead
                else:

                    return 'death'




    def check_object(self, background):
        '''Checks if Mario is collided with an object
        Takes in a background so that it can access size information and the 
        enemy list
        Returns what type of collision it was, which is only used for debugging
        currently
        '''

        ob_list = background.obstacles
        hit_radius = background.tile_size

        #Goes through each obstacle to check collisions
        for obstacle in ob_list:

            #Checks if there is a collision
           
            #Within range is used to see if mario is still standing on a block
            # If he is not but an obstacle thinks it is holding mario, then the 
            # obstacle will no longer be 'holding' mario
            within_range = (abs(obstacle.x_cor) < hit_radius
                            and abs(obstacle.y_cor - self.y_cor) < hit_radius*1.2)
            
            #Checks a radius slightly smaller than the block collision
            if (abs(obstacle.x_cor) < hit_radius
            and abs(obstacle.y_cor - self.y_cor) < hit_radius*.9):
                


                #If the Top of mario hits block set velocity to -2, run the 
                # approitate function in the obstacle. Stops checking for 
                # any more collisons by returning
                if self.y_vel > 0:

                    self.y_vel = -2
                    self.y_cor -= 10

                    out = obstacle.on_top_hit()
                    return out
                    
                #Bottom of Mario hits block - Mario stands on the block
                elif self.y_vel < 0:


                    self.y_accel = 0

                    #Resets position to top
                    self.y_cor = obstacle.y_cor + hit_radius*.9 
                    
                    obstacle.holding_mario = True
                    
                    return 'bottom'
            
                #Mario runs into the right of the block and isn't on top of a block
                #Mario's vel is set to 0 and is pushed slightly in the reverse dir
                elif  (obstacle.x_cor < 0 and not obstacle.holding_mario): 
                    
                    out = obstacle.on_side_col()
                    self.x_vel = 0
                    self.x_cor += 10

                    return out


                #Mario runs into the left of the block and isn't on top of a block
                #Mario's vel is set to 0 and is pushed slightly in the reverse dir
                elif  (obstacle.x_cor > 0 and not obstacle.holding_mario):
                    
                    out = obstacle.on_side_col()
                    self.x_vel = 0
                    self.x_cor -= 10

                    return out

            #Finally if the obstacle thinks it is holding mario but there was no collisions
            #checks on a larger area.

            elif obstacle.holding_mario and not within_range:
                self.y_accel = -1
                obstacle.holding_mario = False




class Enemy:

    def __init__(self, row, col, en_type):
        """Intializes an enemy

        Args:
            row (int): the starting row of the enemy
            col (int): the starting col of the enemy
            en_type (string): the type of the enemy
        """
        
        #Saves positional information
        self.start_row = row
        self.start_col = col
        self.x_cor = 999
        self.y_cor = 999
 
        
        #Saves movement and type info
        self.x_offset = 0
        self.y_offset = 0
        self.direction = -1
        self.active = True
        self.en_type = en_type
        self.speed = 2



    def draw_enemy(self, turt, x_cor, y_cor):
        """Draws the enemy

        Args:
            turt (turtle): turtle that does the drawing
            x_cor (float): the x pos of the drawing
            y_cor (float): the y pos of the drawing
        """

        #If the goomba isn't active (dead) stop the drawing
        if not self.active:
            return
        
        #Stores the updated positional info
        self.x_cor = x_cor
        self.y_cor = y_cor


        turt.shape('minion.gif')


        #Draws the enemy at the point
        turt.up()
        turt.goto(x_cor, y_cor)
        turt.stamp()

        
        


    def on_top_hit(self):
        '''Runs when the enemy is hit on the top (smushed)
        Has different effects depending on the type of the enemy'''
        
        
        if self.en_type == 'empty':
            return
        
        elif self.en_type == 'goomba':
            '''destroy item'''
            self.x_cor = -999
            self.y_cor = -999
            self.active = False
            return 100


    def move_forward(self):
        '''Move the goomba forwards, runs after every'''
        self.x_offset += self.direction*self.speed

        #Rounds offset and columns to keep accurate positional info
        if self.x_offset >= 50:
            self.x_offset -= 50
            self.start_col += 1

        if self.x_offset <= -50:
            self.x_offset += 50
            self.start_col -= 1
        



    def check_objects(self, background):
        '''Check if goomba has hit a obstacle and should turn around
        or if it is about to fall into the ground
        
        Takes in the background
        '''

        ob_list = background.obstacles

        
        #checks if it needs to turn around due to hole in ground
        if background.grid[13][self.start_col] == '0':
            
            if self.direction > 0:
                self.start_col -= 1

            else:
                self.start_col += 1
                
            self.direction *= -1


        for obstacle in ob_list:

            #Checks if it needs to turn around based on the columns of it
            # and the obstacles
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
        '''Intializes an obstacle class'''
        
        #Stores positional information
        self.row = row
        self.col = col
        self.x_cor = 999
        self.y_cor = 999
        
        #Stores info about the type of obstacle
        self.item = item
        self.type = ob_type
        
        self.active = True
        self.holding_mario = False


    def draw_obstacle(self, turt, x_cor, y_cor):
        """Draws the obstacle

        Args:
            turt (turtle): turtle used for drawing
            x_cor (float): x-cor of drawing, stores this info
            y_cor (float): y-cor of drawing, stores this info
        """

        self.x_cor = x_cor
        self.y_cor = y_cor


        #Uses a different shape depending on the type of block 
        if self.type == 'invis':
            return


        if self.type == 'b':
            turt.shape('solid_block.gif')


        if self.type == 'x':
            turt.shape('breakable_block.gif')


        if self.type == 'flag':
            turt.color('blue')
            turt.shape('square')
            
        
        #Draws
        turt.up()
        turt.goto(x_cor, y_cor)
        turt.stamp()
        turt.goto(-1000,1000)


    def on_top_hit(self):
        '''Runs when mario hits the top of an object'''
        
        #Runs different things depending on the 'item'
        if self.item == 'empty':
            return
        
        elif self.item == 'destruct':
            '''destroy item'''
            self.x_cor = -9999
            self.y_cor = -9999
            self.active = False
            return 100
        
        elif self.item == 'win':
            return 'win'

    
    def on_side_col(self):
        '''Runs when mario hits the side of a block - mainly used for flagpole'''
        if self.item == 'win':
            return 'win'



def main():
    '''Main funcion - runs and sets up the program'''
    
    #Sets lives to base amount
    lives = 5
   
    #Game setup, in loop for lives
    while True:
        
        game = Game()
        game.life_update(lives)

        restart = True


        #Main game loop
        while restart:

            time.sleep(1./100)
            #Updates game, output may end game
            out = game.game_update()
            
        
            #If mario dies restart with one life less
            if out == 'death':
                time.sleep(1)
                restart = False
            
            #If game won, end game
            if out == 'win':
                time.sleep(1)
                game.won()
                return

        #As long as mario has lives reset the game
        if lives > 0:

            game.background.window.clearscreen()
            lives -= 1
        
        else:
            break


        


if __name__ == '__main__':
    
    main()
