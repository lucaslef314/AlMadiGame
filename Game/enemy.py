



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