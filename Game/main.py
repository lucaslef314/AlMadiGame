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


from game import Game
import time


def main():
    '''Main funcion - runs and sets up the program'''
    
    #Sets lives to base amount
    lives = 5
   
    #Game setup, in loop for lives
    while True:
        
        game = Game(lives)
        game.life_update()

        restart = True


        #Main game loop
        while restart:


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