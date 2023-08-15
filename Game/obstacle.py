'''

obstacle class
'''


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
        self.holding_character = False


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
        '''Runs when character hits the top of an object'''
        
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
        '''Runs when character hits the side of a block - mainly used for flagpole'''
        if self.item == 'win':
            return 'win'