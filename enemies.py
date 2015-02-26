"""
This module is used to hold the Enemy classes.
"""

import pygame
import time
import random
import constants
from spritesheet_functions import SpriteSheet
#from platforms import MovingPlatform # Needed for moving platforms

class Enemy(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
    controls. """

    def __init__(self, enemy, platform_list):
        """ 
        walk_images is a list of sprite locations found in constants
        and sprite_sheet is the walking PNG file
        """

        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        self.platform_list = platform_list
        
        self.sprite_sheet = SpriteSheet(enemy['spritesheet'])
        
        self.walking_frames_l = []
        self.walking_frames_r = []
        
        self.change_x = enemy['change_x']
        self.change_y = enemy['change_y']
        self.direction = None
        
        self.health = enemy['health']
        
        # Pick random start direction for enemy
        face = random.randint(0,1)
        if face == 0:
            self.direction = "R"
        else:
            self.direction = "L"
            
        # Change walking direction
        if self.direction == "L":
            self.change_x *= -1
            
        # Load all the right facing images into a list
        for frame in enemy['walk_images']:
        
            image = self.sprite_sheet.get_image(frame[0], frame[1], frame[2], 
                                                frame[3])
            self.walking_frames_r.append(image)
            
            # Flip them and load into left facing list
            image = pygame.transform.flip(image, True, False)
            self.walking_frames_l.append(image)
            
        # Set the image the player starts with
        self.image = self.walking_frames_r[0]

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
        
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .45
            
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.platform_list, False)
        self.rect.y -= 2
        
        # Stop enemy from moving sideways if falling
        if not platform_hit_list:
            self.change_x = 0
        else:
            self.change_x = 4
            if self.direction == "L":
                self.change_x *= -1

class Walker(Enemy):
    """ This class represents the basic walking enemy with two health and speed
        of four. It has no special abilities. """
    def update(self):
        """ Calculate enemy position """
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x
        pos = self.rect.x
        if self.direction == "R":
            frame = (pos // 30) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = (pos // 30) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
        # Check if enemy hit a wall and change direction if so.
        if self.direction == "R":
            if self.rect.right >= constants.SCREEN_WIDTH:
                self.direction = "L"
        else:
            if self.rect.left <= 0:
                self.direction = "R"
                
        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0
            
#For moving the enemy if hit by moving platform
#            if isinstance(block, MovingPlatform):
#                self.rect.x += block.change_x

class Flyer(Enemy):
    """ This is the basic flying class. It isn't effected by platforms.
        it has two health and four speed
    """
    
    def __init__(self, enemy, platform_list):
        """ 
        walk_images is a list of sprite locations found in constants
        and sprite_sheet is the walking PNG file
        """

        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        self.platform_list = platform_list
        
        self.sprite_sheet = SpriteSheet(enemy['spritesheet'])
        
        self.walking_frames_l = []
        self.walking_frames_r = []
        
        self.change_x = enemy['change_x']
        self.change_y = enemy['change_y']
        self.direction = None
        
        # For deciding frame
        self.creation_time = time.time()
        
        # Time in seconds until next direction change
        self.time_direct = randint(2,3)
        # Compared against to decide on movement
        self.timer = time.time()
        
        self.health = enemy['health']
        
        # Pick random start direction for enemy
        face = random.randint(0,1)
        if face == 0:
            self.direction = "R"
        else:
            self.direction = "L"
            
        # Change walking direction
        if self.direction == "L":
            self.change_x *= -1
            
        # Load all the right facing images into a list
        for frame in enemy['walk_images']:
        
            image = self.sprite_sheet.get_image(frame[0], frame[1], frame[2], 
                                                frame[3])
            self.walking_frames_r.append(image)
            
            # Flip them and load into left facing list
            image = pygame.transform.flip(image, True, False)
            self.walking_frames_l.append(image)
            
        # Set the image the player starts with
        self.image = self.walking_frames_r[0]

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
        
    def update(self):
        """ Calculate enemy position """

        self.timer_two = time.time()
        
        # If the flyer hits the edge of the screen or the timer is uo
        # change the enemy's direction
        if self.timer_two - self.timer > self.time_direct or self.rect.x <= 0 or self.rect.x >= SCREEN_WIDTH - self.rect.width or self.rect.y <= 0 or self.rect.y >= SCREEN_HEIGHT - self.rect.height:
            
            self.x_rand = randint(1,2)
            
            if self.x_rand == 1:
                self.change_x *= -1
            
            self.x_rand = randint(1,2)
            
            if self.x_rand == 1:
                self.change_y *= -1
        # Move left/right
        self.rect.x += self.change_x
        # Move up/down
        self.rect.y += self.change_y
