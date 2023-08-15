'''
name: character.py
author: Lucas Lefebvre
course: CS151 section B
date (last edit): 5/3/2023

Plays a version of the classic game super character bros.


Important Numbers
Tile size 50

Screen width: 16 Tiles
Screen height: 14 tiles
Width: 800
Height: 700

'''


from turtle import Screen, Turtle
from background import BackGround
from turtle_stuff import *
from character import Character
import time


class Game:

    def __init__(self, level='1_1'):
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
        
        
        elif type(object_out) == int:
            
            self.score += object_out

            self.background.display_text(0, self.character.y_cor,
                                         'red', object_out)
        
        if type(en_out) == int:
            
            self.score += en_out
            self.background.display_text(0, self.character.y_cor,
                                         'red', en_out)
        
        
        self.background.display_text(0, self.background.window_height//2.2, 'black',
                                     'Score:',self.score )

       

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

        









