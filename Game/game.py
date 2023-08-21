


from background import BackGround
from turtle_stuff import *
from character import Character
import time
from text import Text


class Game:

    def __init__(self, lives, level='1_1'):
        '''Intializes the game.
        Takes in a level to load. Currently the only levels are 1_1 and 1_0
        '''
        
        #Creates the background
        self.level = level
        self.background = BackGround(800,700, level)
        
        #Using the window height and tile size figures out what the ground 
        #Then creates the character object with this info
        self.character = Character(self.background.ground_y)

        #Sets all of the keybindings
        self.background.window.listen()
        self.background.window.onkeypress(self.character.jump,'w')
        self.background.window.onkeypress(self.character.left,'a')
        self.background.window.onkeypress(self.character.right,'d')

        #These keybindindings are needed so that one can hold a key down
        self.background.window.onkeyrelease(self.character.right_stop, 'd')
        self.background.window.onkeyrelease(self.character.left_stop, 'a')

        #Score Variables
        self.score = 0
        self.lives = lives

        #Creates text fields used
        self.score_display = Text(0, self.background.window_height//2.2, 'black',
                                     'Score:', 10, 0 )
        
        self.life_counter = Text(0,0, 'white',lives, 10, 'Lives Remaining')
        
        self.won_text = Text(-100,0, 'white', '', 0, '')

    
    def game_update(self):
        '''This runs in a while loop. Updates the game and checks collisions'''

        #updates accel based on ground - also need to check if no ground

        object_out = (self.character.check_object(self.background))

        ground_out = self.character.check_ground(self.background)
        
        en_out = self.character.check_enemies(self.background)


        #Checks if character dies
        if en_out == 'death' or ground_out == 'death':
            return 'death'
        
        if object_out == 'win':
            return 'win'
        
        #Displays text according to points earned and location
        elif type(object_out) == int:
            
            self.score += object_out
            
            object_points = Text(0, self.character.y_cor + 50,
                                         'dark red', object_out, 25)
        
        if type(en_out) == int:
            
            self.score += en_out
            
            enemy_points = Text(0, self.character.y_cor + 50,
                                         'dark red', en_out, 25)
        

        
        self.score_display.resume_text(10, 'nope', self.score)

       

        #Applies gravity (updates y-velocity and y-position)
        self.character.gravity()
        
        #Moves Goomba's
        for enemy in self.background.enemies:

            enemy.move_forward()
            enemy.check_objects(self.background)
        
        #Draws character
        shape = self.character.shape()
        offset = self.character.x_cor
        self.background.draw_map(self.character.y_cor,int(offset//50),offset%50, shape)


    def life_update(self):
        #tells the player lives remaining

        self.background.window.bgcolor('black')

        self.life_counter.print_text()
        self.background.window.update()
        
        time.sleep(1)
        self.background.window.bgcolor('sky blue')



    def won(self):
        #tells the player they have won
        
        self.background.window.bgcolor('black')
        line1 = "Congratulations you have completed the level!"
        line2 = "You got a score of " + str(self.score) + " !"

        self.background.drawer.clear()

        self.won_text.resume_text(1, line1, line2)
        self.won_text.print_text()
        self.background.window.update()
        
        time.sleep(3)

        









