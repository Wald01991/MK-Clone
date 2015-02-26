import pygame
import time
import random

import constants
import platforms
import enemies

class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    # Lists of sprites used in all levels. Add or remove
    # lists as needed for your game. """
    platform_list = None
    enemy_list = None

    # Background image
    background = None

    def __init__(self, player_one, player_two):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()        
        self.player_one = player_one
        self.player_two = player_two
        
        # Time to reference since last enemy spawn
        self.enemy_timer = time.time()
        # Time in seconds until next enemy spawn
        self.enemy_spawnspace = 0
        # Enemy spawn timer
        self.enemy_spawn_time = time.time()
        
        self.spawn_increase = 5
        self.spawn_decrease = 3
        
        
    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        
        self.spawn()
        
        self.platform_list.update()
        self.bullet_list.update()
        self.enemy_list.update()
        
        for enemy in self.enemy_list:
            if enemy.rect.y > constants.SCREEN_HEIGHT:
                self.enemy_list.remove(enemy)

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        # We don't shift the background as much as the sprites are shifted
        # to give a feeling of depth.
        screen.fill(constants.BLUE)
        screen.blit(self.background, (0,0))

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.bullet_list.draw(screen)

# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player_one, player_two):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player_one, player_two)

        self.background = pygame.image.load("forest.PNG").convert()
        self.background.set_colorkey(constants.WHITE)


        # Array with type of platform, and x, y location of the platform.
        level = [ 
                  [platforms.GRASS_MIDDLE, 0, 220],
                  [platforms.GRASS_MIDDLE, 70, 220],
                  [platforms.GRASS_RIGHT, 140, 220],
                  [platforms.GRASS_LEFT, 425, 220],
                  [platforms.GRASS_MIDDLE, 495, 220],
                  [platforms.GRASS_MIDDLE, 565, 220],
                  [platforms.GRASS_MIDDLE, 635, 220],
                  [platforms.GRASS_RIGHT, 705, 220],
                  [platforms.GRASS_LEFT, 990, 220],
                  [platforms.GRASS_MIDDLE, 1060, 220],
                  [platforms.GRASS_MIDDLE, 1130, 220],
                  [platforms.GRASS_MIDDLE, 0, 435],
                  [platforms.GRASS_MIDDLE, 70, 435],
                  [platforms.GRASS_MIDDLE, 140, 435],
                  [platforms.GRASS_MIDDLE, 210, 435],
                  [platforms.GRASS_MIDDLE, 280, 435],
                  [platforms.GRASS_MIDDLE, 350, 435],
                  [platforms.GRASS_RIGHT, 420, 435],
                  [platforms.GRASS_LEFT, 710, 435],
                  [platforms.GRASS_MIDDLE, 780, 435],
                  [platforms.GRASS_MIDDLE, 850, 435],
                  [platforms.GRASS_MIDDLE, 920, 435],
                  [platforms.GRASS_MIDDLE, 990, 435],
                  [platforms.GRASS_MIDDLE, 1060, 435],
                  [platforms.GRASS_MIDDLE, 1130, 435],
                  [platforms.GRASS_LEFT, 215, 650],
                  [platforms.GRASS_MIDDLE, 285, 650],
                  [platforms.GRASS_MIDDLE, 355, 650],
                  [platforms.GRASS_MIDDLE, 425, 650],
                  [platforms.GRASS_MIDDLE, 495, 650],
                  [platforms.GRASS_MIDDLE, 565, 650],
                  [platforms.GRASS_MIDDLE, 635, 650],
                  [platforms.GRASS_MIDDLE, 705, 650],
                  [platforms.GRASS_MIDDLE, 775, 650],
                  [platforms.GRASS_MIDDLE, 845, 650],
                  [platforms.GRASS_RIGHT, 915, 650],
                  [platforms.GRASS_MIDDLE, 0, 865],
                  [platforms.GRASS_MIDDLE, 70, 865],
                  [platforms.GRASS_MIDDLE, 140, 865],
                  [platforms.GRASS_MIDDLE, 210, 865],
                  [platforms.GRASS_MIDDLE, 280, 865],
                  [platforms.GRASS_MIDDLE, 350, 865],
                  [platforms.GRASS_RIGHT, 420, 865],
                  [platforms.GRASS_LEFT, 710, 865],
                  [platforms.GRASS_MIDDLE, 780, 865],
                  [platforms.GRASS_MIDDLE, 850, 865],
                  [platforms.GRASS_MIDDLE, 920, 865],
                  [platforms.GRASS_MIDDLE, 990, 865],
                  [platforms.GRASS_MIDDLE, 1060, 865],
                  [platforms.GRASS_MIDDLE, 1130, 865]
                  ]

        outer_wall = 0
        # Create top outer limit wall
        for block in range(18):
            level.append([platforms.GRASS_MIDDLE, outer_wall, -70])
            outer_wall += 70
        outer_wall = 0
        # Create left outer limit wall
        for block in range(13):
            level.append([platforms.GRASS_MIDDLE, -70, outer_wall])
            outer_wall += 70
        outer_wall = 0
        # Create left outer limit wall
        for block in range(13):
            level.append([platforms.GRASS_MIDDLE, 1200, outer_wall])
            outer_wall += 70
        
        # Go through the array above and add platforms
        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player_one = self.player_one
            block.player_two = self.player_two
            self.platform_list.add(block)
            
    def spawn(self):
        
        # Enemy spawn timer compare
        second_spawn_timer = time.time()
        # Compare this timer to the first
        temp_enemy_timer = time.time()
        # Save the difference to this variable
        enemy_spawn = temp_enemy_timer - self.enemy_timer
        # Create an enemy if the time passed is longer than required
        if enemy_spawn >= self.enemy_spawnspace:
            # Give the old timer the new timer value
            self.enemy_timer = temp_enemy_timer
            # Create the enemy
            walker = enemies.Walker(constants.WALKER_AT, self.platform_list)
            # Set the enemy's spawn side depending on face direction
            if walker.direction == "R":
                walker.rect.x = 0
                walker.rect.y = 220 - walker.rect.height
            else:
                walker.rect.x = 1200 - walker.rect.width
                walker.rect.y = 220 - walker.rect.height
            # Add to the level's list of enemies
            self.enemy_list.add(walker)
            # Pick random time until next enemy spawn
            if second_spawn_timer - self.enemy_spawn_time >= self.spawn_increase:
                self.spawn_increase += 10
                if self.spawn_decrease >= .3:
                    self.spawn_decrease -= .7
                else:
                    self.spawn_decrease = .3
            self.enemy_spawnspace = random.uniform(1, self.spawn_decrease)
            
"""
        # Add a custom moving platform
        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1350
        block.rect.y = 280
        block.boundary_left = 1350
        block.boundary_right = 1600
        block.change_x = 1
        block.players = self.players
        block.level = self
        self.platform_list.add(block)


# Create platforms for the level
class Level_02(Level):
     Definition for level 2. 

    def __init__(self, players):
        Create level 1. 

        # Call the parent constructor
        Level.__init__(self, players)

        self.background = pygame.image.load("background_02.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = -1000

        # Array with type of platform, and x, y location of the platform.
        level = [ [platforms.STONE_PLATFORM_LEFT, 500, 550],
                  [platforms.STONE_PLATFORM_MIDDLE, 570, 550],
                  [platforms.STONE_PLATFORM_RIGHT, 640, 550],
                  [platforms.GRASS_LEFT, 800, 400],
                  [platforms.GRASS_MIDDLE, 870, 400],
                  [platforms.GRASS_RIGHT, 940, 400],
                  [platforms.GRASS_LEFT, 1000, 500],
                  [platforms.GRASS_MIDDLE, 1070, 500],
                  [platforms.GRASS_RIGHT, 1140, 500],
                  [platforms.STONE_PLATFORM_LEFT, 1120, 280],
                  [platforms.STONE_PLATFORM_MIDDLE, 1190, 280],
                  [platforms.STONE_PLATFORM_RIGHT, 1260, 280],
                  ]


        # Go through the array above and add platforms
        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.players = self.players
            self.platform_list.add(block)

        # Add a custom moving platform
        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.players = self.players
        block.level = self
        self.platform_list.add(block)
"""