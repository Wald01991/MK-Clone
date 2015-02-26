import pygame

import constants
from spritesheet_functions import SpriteSheet

class Scoreboard(pygame.sprite.Sprite):
    """ This holds and displays the scores """

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        # Get scoreboard image
        self.image = pygame.image.load("scoreboard.png").convert()
        # Get rect from image
        self.rect = self.image.get_rect()
        # Set location
        self.rect.x = 530
        self.rect.y = 0
        
    def get_score(self, player_score):
        
        score_word = str(player_score)
        
        first = score_word[0]
        second = score_word[1]
        
        num_list = [int(first), int(second)]
        
        return num_list
    
    def display_score(self, score, player):
        # Create player scores
        
        if player == True:
            spot_one = 530
            spot_two = 560
        else:
            spot_one = 610
            spot_two = 640
        
        if score < 10:
            # Create number images 
            num_one = GetScoreImage(0, spot_one)
            num_two = GetScoreImage(score, spot_two)
            
            score_final = [num_one, num_two]
        else:
            # Break player one's score into two numbers
            broke_score = self.get_score(score)
            # Create number images 
            num_one = GetScoreImage(broke_score[0], spot_one)
            num_two = GetScoreImage(broke_score[1], spot_two)
            
            score_final = [num_one, num_two]
            
        return score_final
            
class GetScoreImage(pygame.sprite.Sprite):
    """ Player one score's first number """
    
    def __init__(self, number, rect_x):
    
        pygame.sprite.Sprite.__init__(self)
        
        self.sprite_sheet = SpriteSheet("numbers.png")

        # List of spritesheet co-ordinates for number
        coor_list = constants.NUMBERS[number]
        
        x = coor_list[0]
        y = coor_list[1]
        width = coor_list[2]
        height = coor_list[3]
        
        self.image = self.sprite_sheet.get_image(x,y,width,height).convert()
        self.rect = self.image.get_rect()
        
        self.rect.x = rect_x
        self.rect.y = 14
        
