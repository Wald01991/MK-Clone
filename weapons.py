"""
This module contains all the weapon classes
"""

import pygame
import constants

class Bullet(pygame.sprite.Sprite):
    """
    This class represents in game projectiles
    """

    def __init__(self, player):
        """
        Constructor that takes the player instance as a parameter.
        """

        pygame.sprite.Sprite.__init__(self)
        
        self.player = player
        self.player_name = player.pname
        
        self.speed = 10

        # Create a bullet image and fill it with black
        self.image = pygame.Surface([4, 10])
        self.image.fill(constants.BLACK)

        # Set the rect box as the dimensions of the image
        self.rect = self.image.get_rect()
        
        # Set where bullet starts
        self.rect.x = self.player.rect.center[0]
        self.rect.y = self.player.rect.center[1]
        
        if self.player.direction == "L":
            self.speed *= -1
        
        
        
    def update(self):
        """
        Move the bullet in the direction the player is facing
        """

        self.rect.x += self.speed