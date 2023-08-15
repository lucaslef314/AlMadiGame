'''
character class


'''




class Character:

    def __init__(self, ground_y):
        '''Intializes the character class. Needs to know what the ground y is'''
        
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

        
        #Finally if Character is moving to the left use the left moving sprites
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
        '''Checks if character is on the ground or falling to death'''

        #If y_cor is really low, then kills character
        if self.y_cor <= (self.ground_y - background.tile_size * 4):
            return 'death'

        #If character is currently falling to death stop ground check
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
        '''Updates velocity based on gravity. Also moves character based on velocity'''
       
        #Updates y velocity if there is acceleration.
        if  self.y_accel != 0:

            self.y_cor += self.y_vel
            self.y_vel += self.y_accel
        
        #If there isn't acceleration then set velocity to zero
        else:
            self.y_vel = 0

        #Updates x velocity
        if self.x_vel != 0:

            #Moves character by x velocity
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

        Returns death if character collides with an enemy without velocity
        '''
        #Sets variables
        en_list = background.enemies
        hit_radius = background.tile_size - 2

        #For each enemy checks collisions
        for enemy in en_list:

            if (abs(enemy.x_cor) < hit_radius
            and abs(enemy.y_cor - self.y_cor) < hit_radius):
                
                #If character has velocity it means that he will smush the goomba
                #Runs the appropriate function in the enemy for this condition
                if self.y_vel != 0:

                    self.y_vel = 12
                    out = enemy.on_top_hit()
                    return out
                    
                #if not then he is dead
                else:

                    return 'death'




    def check_object(self, background):
        '''Checks if Character is collided with an object
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
           
            #Within range is used to see if character is still standing on a block
            # If he is not but an obstacle thinks it is holding character, then the 
            # obstacle will no longer be 'holding' character
            within_range = (abs(obstacle.x_cor) < hit_radius
                            and abs(obstacle.y_cor - self.y_cor) < hit_radius*1.2)
            
            #Checks a radius slightly smaller than the block collision
            if (abs(obstacle.x_cor) < hit_radius
            and abs(obstacle.y_cor - self.y_cor) < hit_radius*.9):
                


                #If the Top of character hits block set velocity to -2, run the 
                # approitate function in the obstacle. Stops checking for 
                # any more collisons by returning
                if self.y_vel > 0:

                    self.y_vel = -2
                    self.y_cor -= 10

                    out = obstacle.on_top_hit()
                    return out
                    
                #Bottom of Character hits block - Character stands on the block
                elif self.y_vel < 0:


                    self.y_accel = 0

                    #Resets position to top
                    self.y_cor = obstacle.y_cor + hit_radius*.9 
                    
                    obstacle.holding_character = True
                    
                    return 'bottom'
            
                #Character runs into the right of the block and isn't on top of a block
                #Character's vel is set to 0 and is pushed slightly in the reverse dir
                elif  (obstacle.x_cor < 0 and not obstacle.holding_character): 
                    
                    out = obstacle.on_side_col()
                    self.x_vel = 0
                    self.x_cor += 10

                    return out


                #Character runs into the left of the block and isn't on top of a block
                #Character's vel is set to 0 and is pushed slightly in the reverse dir
                elif  (obstacle.x_cor > 0 and not obstacle.holding_character):
                    
                    out = obstacle.on_side_col()
                    self.x_vel = 0
                    self.x_cor -= 10

                    return out

            #Finally if the obstacle thinks it is holding character but there was no collisions
            #checks on a larger area.

            elif obstacle.holding_character and not within_range:
                self.y_accel = -1
                obstacle.holding_character = False
