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


import turtle
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
    screen = turtle.getscreen()
    screen.setup(width,height)
    screen.bgcolor(color)
    screen.title(title)
    turtle.tracer(False)
    turtle.hideturtle()
    

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
    new_turtle = turtle.Turtle()
    new_turtle.shape(shape)
    new_turtle.shapesize(stretch_width,stretch_length)
    new_turtle.color(color)
    new_turtle.penup()
    new_turtle.setpos(x_pos,y_pos)

    return new_turtle


class Game:

    def __init__(self):
        ''''''
        
        #self.screen_height = 700
        self.background = BackGround(800,700)
        ground_y = self.background.window_height//-2 + 3*self.background.tile_size
        self.mario = Mario(ground_y)
        self.right_held = False
        self.jump_held = False
        self.left_held = False
        self.top_col = False
        self.bottom_col = False
        self.side_col = False
        
        self.background.window.listen()
        self.background.window.onkeypress(self.mario.jump,'w')
        self.background.window.onkeypress(self.left,'a')
        #background.window.onkeypress(mario,'Up')
        self.background.window.onkeypress(self.right,'d')
        self.background.window.onkeyrelease(self.right_stop, 'd')
        #self.background.window.onkeyrelease(self.jump_stop, 'w')
        self.background.window.onkeyrelease(self.left_stop, 'a')

        self.background.draw_map(0,0,0)



    def right(self):
        self.right_held = True

        while self.right_held and self.mario.x_vel < self.mario.max_x_vel:
            self.mario.x_vel += .5


    def right_stop(self):
        self.right_held = False


    
        

    # def jump_stop(self):
    #     ''''''
    #     #self.jump_held = False
        

    def left(self):
        ''''''
        self.left_held = True

        while self.left_held and self.mario.x_vel > -self.mario.max_x_vel:
            self.mario.x_vel -= .5


    def left_stop(self):
        self.left_held = False
                

    def game_update(self):
        '''oop'''

        #Updates position based on velocity and decreases velocity based on acceleration

        sc_bottom = -(self.background.window_height//2)

        #Converts mario's relative y-pos into the absolute y-position


        #updates accel based on ground - also need to check if no ground

        output = (self.mario.check_object(self.background))
        if output != None:
            print(output)
        
        self.mario.check_ground()

        #Updates y velocity
        if  self.mario.y_accel != 0:
            self.jump_held = False
            self.mario.y_cor += self.mario.y_vel
            self.mario.y_vel += self.mario.y_accel

        else:
            #self.jump_held = False
            #self.mario.y_cor = 0
            self.mario.y_vel = 0
            self.top_col = False
            #self.bottom_col = False


        #Updates x velocity
        if self.mario.x_vel != 0:


            self.mario.x_cor += self.mario.x_vel

            if self.mario.x_vel > 0 and not self.right_held:
                self.mario.x_vel -= 1
            elif self.mario.x_vel < 0 and not self.left_held:
                self.mario.x_vel += 1
  
        
        #Moves Goomba's
        for enemy in self.background.enemies:

            enemy.move_forward()
        
        #Draws mario
        offset = self.mario.x_cor
        self.background.draw_map(self.mario.y_cor,int(offset//50),offset%50)




        #Check cols
        #self.check_col(self.background.obstacles)
        #self.check_col(self.background.enemies)


    def check_col(self, ob_list):
        '''Checks if mario has hit any obstacles or enemies'''

        #The hit radius is the tile size
        hit_radius = self.background.tile_size
        no_col = False

        #For each obstacle, checks if they are colliding with mario
        for obstacle in ob_list:

            # print('m ' + str(self.mario.y_cor))
            # print('o ' + str(obstacle.y_cor))
            # time.sleep(.1)
            sc_bottom = -(self.background.window_height//2)

            #Converts mario's relative y-pos into the absolute y-position
            mario_y_cor =  sc_bottom + self.background.tile_size * 3 + self.mario.y_cor
            is_inside = abs(obstacle.y_cor - mario_y_cor) < (hit_radius/1.8)

            if (abs(obstacle.x_cor) < hit_radius
                    and abs(obstacle.y_cor - mario_y_cor) < hit_radius):
                
                if self.mario.y_vel > 0 and not self.jump_held:
                    #print('up hit')
                    self.mario.y_vel = -.01
                    self.top_col = True
                    obstacle.on_top_hit()
                    

                elif self.mario.y_vel < 0 and not self.top_col:
                    #print('bottom hit')
                    #self.mario.y_vel = 0
                    self.bottom_col = True
                    #return 2
                
                elif (self.mario.y_vel and self.top_col and obstacle.y_cor - mario_y_cor < 0):
                    self.bottom_col = True
                    #return 2
            
                
                elif  (obstacle.x_cor < 0 and not self.jump_held) and (is_inside or not self.bottom_col): #and not self.top_col:
                    self.mario.x_vel = 0
                   # self.side_col = True
                    self.mario.x_cor += 10
                    #return 4

                elif  (obstacle.x_cor > 0 and not self.jump_held) and (is_inside or not self.bottom_col): # and not self.top_col:
                    self.mario.x_vel = 0
                    #self.side_col = True
                    self.mario.x_cor -= 10
                    #return 5


                elif self.bottom_col:
                    #return 3
                    ''''''

                else:
                    no_col = True

                if not no_col:
                    return
#abs(self.mario.max_x_vel) > 0 and   abs(self.mario.max_x_vel) > 0 and

        self.bottom_col = False
        return 0
                
                



class BackGround:


    def __init__(self, width, height):
        
        self.window_width = width
        self.window_height = height
        self.tile_size = 50
        self.obstacles = []
        self.enemies = []

        self.window = make_screen(self.window_width, self.window_height, 'Super Al Madi', 'white' )
        self.window.tracer(False)
        turtle.hideturtle()
        self.drawer = make_turtle('square','red',1,1,0,0)
        self.read_map('1_1')
        



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

        self.window.reset()

        # move turtle to initial drawing position

        x_pos = self.window_width//-2
        y_pos = self.window_height//2
        if mario_y == 'def':
            mario_y = self.window_height//-2 + 2 * self.tile_size

        turt = self.drawer

        
        mario_y = mario_y #-y_pos + self.tile_size * 3 + mario_y

        turt.shape('square')
        turt.color('blue')
        turt.shapesize(self.tile_size/20, self.tile_size/20)

        turt.up()
        turt.goto(0,mario_y)
        turt.stamp()
        turt.down()

        turt.up()
        turt.goto(x_pos, y_pos)
        turt.down()


        # go over every cell in the grid
        for row in range(len(self.grid)):

            for col in range(s_col, 16 + s_col + 2): #len(self.grid[row])):
                
                # move turtle to the position of the cell in the grid
                turt.up()
                turt.goto(x_pos - offset + (col - s_col) * self.tile_size, 
                          y_pos  - (row) * self.tile_size)
                turt.down()


                # if the cell is an obstacle (X) draw a black dot
                if self.grid[row][col] == 'g':
                    #turt.stamp(tile_size-5, "Black")
                    turt.color('brown')
                    turt.stamp()
                
                # if the cell is the start drawing position (S) draw a yellow dot
                elif self.grid[row][col] == 'm':
                    turt.dot(self.tile_size-5, "yellow")

                
                # if the cell is the End position (E) draw a Red dot
                elif self.grid[row][col] == 'b':
                    #turt.dot(self.tile_size-5, "red")
                    self.grid[row][col] = '0'
                    self.obstacles.append(Obstacle(row,col,'b'))

                elif self.grid[row][col] == 'i':
                    #turt.dot(self.tile_size-5, "red")
                    self.grid[row][col] = '0'
                    self.obstacles.append(Obstacle(row,col,'invis'))


                elif self.grid[row][col] == 'x':
                    #turt.dot(self.tile_size-5, "red")
                    self.grid[row][col] = '0'
                    self.obstacles.append(Obstacle(row,col,'x','destruct'))

                elif self.grid[row][col] == 'e':
                    #turt.dot(self.tile_size-5, "red")
                    self.grid[row][col] = '0'
                    self.enemies.append(Enemy(row,col,'g'))


        #Draws the obstacles seperatly 
        for obstacles in self.obstacles:
            turt.up()

            column_pos = obstacles.col - s_col
            x_cor = x_pos - offset + (column_pos) * self.tile_size
            y_cor = y_pos  - (obstacles.row) * self.tile_size

            #Makes sure the obstacles are within the screen view
            if (column_pos >= 0 and obstacles.active and column_pos <= 18):

                obstacles.draw_obstacle(self.drawer, x_cor, y_cor)

        #Draws the obstacles seperatly 
        for enemy in self.enemies:
            turt.up()

            column_pos = enemy.start_col - s_col
            x_cor = x_pos - offset + (column_pos) * self.tile_size + enemy.x_offset
            y_cor = y_pos  - (enemy.start_row) * self.tile_size + enemy.y_offset

            #Makes sure the obstacles are within the screen view
            if (column_pos >= 0 and obstacles.active and column_pos <= 18):

                enemy.draw_enemy(self.drawer, x_cor, y_cor)


        #game.check
        self.window.update()
        

class Mario:

    def __init__(self, ground_y):
        ''''''
        self.ground_y = ground_y
        self.x_cor = 0
        self.y_cor = ground_y
        self.right_held = False
        self.y_vel = 0
        self.start_y_vel = 20
        self.x_vel = 0
        self.max_x_vel = 8
        self.y_accel = 0
        self.x_accel = 0
        self.jumping = False

    def jump(self):
        ''''''
        #print('oop', self.mario.y_vel, self.bottom_col)
        
        if abs(self.y_vel) == 1:
            self.y_vel = 0

        if self.y_accel == 0: # or self.bottom_col:
            #
            # print('e')
            self.y_vel = self.start_y_vel
            self.y_accel = -1
            #self.jumping = True


    def check_ground(self):
        
        if self.y_cor < self.ground_y:
            self.y_cor = self.ground_y
            self.y_accel = 0


    def check_object(self,background):
        '''Checks if Mario is collided with an object'''

        ob_list = background.obstacles
        sc_bottom = -(background.window_height//2)
        #mario_y_cor =  sc_bottom + background.tile_size * 3 + self.y_cor
        hit_radius = background.tile_size

        for obstacle in ob_list:
            ''''''
            #Checks if there is a collision

            
            
            if (abs(obstacle.x_cor) < hit_radius
            and abs(obstacle.y_cor - self.y_cor) < hit_radius):
                
                # print(self.y_cor)
                # print(obstacle.y_cor)

                #Bottom of Mario Hit
                if self.y_vel < 0:

                    self.y_vel = 0
                    self.y_accel = 0
                    self.y_cor = obstacle.y_cor + background.tile_size + 1
                    self.jumping = True
                    return 'top'
                

                #Top of Mario hit
                if self.y_vel > 0 and self.y_accel != 0: #and self.jumping:
                    self.y_vel = 0
                    self.y_cor = obstacle.y_cor - background.tile_size
                    #print('bottom')
                    return 'bottom'
                
            if not (abs(obstacle.x_cor) < hit_radius) and self.jumping :
                return

        self.y_accel = -1
        self.jumping = False
        print('e')
            



        





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


    def draw_enemy(self, turt, x_cor, y_cor):
        ''''''
        self.x_cor = x_cor
        self.y_cor = y_cor


        turt.color('orange')

        turt.up()
        turt.goto(x_cor, y_cor)
        turt.stamp()


    def on_top_hit(self):

        if self.item == 'empty':
            return
        
        elif self.item == 'destruct':
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


    def draw_obstacle(self, turt, x_cor, y_cor):
        ''''''
        self.x_cor = x_cor
        self.y_cor = y_cor

        if self.type == 'invis':
            return
        

        if self.type == 'b':
            turt.color('brown')

        
        if self.type == 'x':
            turt.color('yellow')
            
        

        turt.up()
        turt.goto(x_cor, y_cor)
        turt.stamp()


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
    while True:
        game = Game()
        restart = True
        #game.read_map('1_1')


        while restart:
            death = game.game_update()
            game.background.window.update()

            if death:
                restart = False

        #Reduce lives and check if no lives left

        


if __name__ == '__main__':
    main()

    # if self.turt.distance(alien.turt) < 20:
    #     return True