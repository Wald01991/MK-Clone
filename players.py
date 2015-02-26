"""
This module is used to hold the Player class. The Player represents the user-
controlled sprite on the screen.
"""
import pygame
import time

import constants
from spritesheet_functions import SpriteSheet
#from platforms import MovingPlatform

class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
    controls. """
    # List of sprites we can bump against
    level = None

    # -- Methods
    def __init__(self, player):
        """ 
        walk_images is a list of sprite locations found in constants
        and sprite_sheet is the walking PNG file
        """

        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
        
        self.pname = player['name']

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        self.sprite_sheet = SpriteSheet(player['spritesheet'])
        self.frozen_sprite_sheet = SpriteSheet(player['frozen_spritesheet'])
        
        # This holds all the images for the animated walk left/right
        # of our player
        self.walking_frames_l = []
        self.walking_frames_r = []
        self.frozen_frames_l = []
        self.frozen_frames_r = []
    
        self.direction = player['direction']
        
        self.stunned = False
        self.stunned_direction = None
        self.stun_start = time.time()
        
        self.lives = 3
        
        # Load all the right facing images into a list
        for frame in player['walk_images']:
        
            image = self.sprite_sheet.get_image(frame[0], frame[1], frame[2], 
                                                frame[3]).convert()
            self.walking_frames_r.append(image)
            
            # Flip them and load into left facing list
            image = pygame.transform.flip(image, True, False)
            self.walking_frames_l.append(image)
            
            # Creates the frozen sprites
            image = self.frozen_sprite_sheet.get_image(frame[0], frame[1], 
            frame[2], frame[3]).convert()
            self.frozen_frames_r.append(image)
            
            # Flip them and load into left facing list
            image = pygame.transform.flip(image, True, False)
            self.frozen_frames_l.append(image)
            
        # Set the image the player starts with
        self.image = self.walking_frames_r[0]

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()
        
        # Check to see if player has been stunned
        if self.stunned == True:
            
            self.stun_check = time.time()
            
            # How long the player has been stunned for
            if self.stun_check - self.stun_start < 2:
                
                # Stop horizontal movement
                self.change_x = 0
                
                # Keep player facing same direction
                self.direction = self.stunned_direction
                
                # If player is jumping stop vertical movement 
                if self.change_y < 0:
                    self.change_y = 0
            else:
                self.stunned = False

        # Move left/right
        self.rect.x += self.change_x
        pos = self.rect.x
        
        # Pick a frame (switch to frozen if needed)
        if self.stunned == True:
            if self.direction == "R":
                frame = (pos // 30) % len(self.frozen_frames_r)
                self.image = self.frozen_frames_r[frame]
            else:
                frame = (pos // 30) % len(self.frozen_frames_l)
                self.image = self.frozen_frames_l[frame]
        else:    
            if self.direction == "R":
                frame = (pos // 30) % len(self.walking_frames_r)
                self.image = self.walking_frames_r[frame]
            else:
                frame = (pos // 30) % len(self.walking_frames_l)
                self.image = self.walking_frames_l[frame]

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0
            
#For moving player if hit by moving platform
#            if isinstance(block, MovingPlatform):
#                self.rect.x += block.change_x

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .45
            
        if self.rect.y > constants.SCREEN_HEIGHT:
            
            # Move to the top middle platform
            self.rect.x = 585
            self.rect.y = 100
            
            # Minus a life
            self.lives -= 1

    def jump(self):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
            self.change_y = -15

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6
        self.direction = "L"

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
        self.direction = "R"

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
