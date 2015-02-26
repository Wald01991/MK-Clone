"""
Main module for multiplayer Mario clone.
"""

import pygame
from sys import exit
import time

import constants
import levels
from players import Player
import weapons
import score

def main():
    """ Main Program """
    pygame.init()

# -------------- Screen Settings ----------------

    # Set the height and width of the screen
    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    # Top of window caption
    pygame.display.set_caption("Muffin Knight Clone")
 
# ----------------- Scores + Players ------------------- 

    # Create the player
    player_one = Player(constants.PLAYER_ONE_AT)
    player_two = Player(constants.PLAYER_TWO_AT)
  
    # Scores
    player_one_score = 0
    player_two_score = 0
    p1_old_score = -1
    p2_old_score = -1

# ---------------- Level Assignment ---------------

    # Create all the levels
    level_list = []
    level_list.append(levels.Level_01(player_one, player_two))

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

# ----------------- Create Sprite Groups -------------------
    
    # Create list of players sprites
    active_sprite_list = pygame.sprite.Group()
    
    # Create list of scores sprites
    scores_list = pygame.sprite.Group()
    
    # Group that only contains scoreboard
    scoreboard_list = pygame.sprite.GroupSingle()
    
# --------------- Assign Player Attributes -------------- 


    # Set the players levels
    player_one.level = current_level
    player_two.level = current_level
    
    # Set the player locations
    player_one.rect.x = 100
    player_two.rect.x = 1100
    player_one.rect.y = 865 - player_one.rect.height
    player_two.rect.y = 865 - player_two.rect.height
    
    # Add players to their sprite list
    active_sprite_list.add(player_one)
    active_sprite_list.add(player_two)

# ----------------- Scoreboard -----------------

    # Create the scoreboard frame and add to it's sprite list
    scoreboard = score.Scoreboard()
    
    scoreboard_list.add(scoreboard)

# ------------------- Timing --------------------

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    
    # Player 1 time between bullets
    p1_bullet_time = time.time()
    # Payer 2 time between bullets
    p2_bullet_time = time.time()

# ---------------- Sounds --------------------
    
    # Load backround music
    music = pygame.mixer.music.load('music.mid')
    # Backround music loop    
    pygame.mixer.music.play(-1)
    
# -------- MAIN PROGRAM LOOP -----------

    done = False
    #Loop until the user hits backspace
    while not done:

# ---------- Player Controls ------------

        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop

            if event.type == pygame.KEYDOWN:
            # Player One controls
                if event.key == pygame.K_a:
                    player_one.go_left()
                if event.key == pygame.K_d:
                    player_one.go_right()
                if event.key == pygame.K_w:
                    player_one.jump()
                if event.key == pygame.K_SPACE:
                    p1_temp_btime = time.time()
                    if (p1_temp_btime - p1_bullet_time) >= .5:
                        bullet = weapons.Bullet(player_one)
                        current_level.bullet_list.add(bullet)
                        p1_bullet_time = p1_temp_btime
                # Player Two controls
                if event.key == pygame.K_LEFT:
                    player_two.go_left()
                if event.key == pygame.K_RIGHT:
                    player_two.go_right()
                if event.key == pygame.K_UP:
                    player_two.jump()
                if event.key == pygame.K_KP0:
                    p2_temp_btime = time.time()
                    if (p2_temp_btime - p2_bullet_time) >= .5:
                        bullet = weapons.Bullet(player_two)
                        current_level.bullet_list.add(bullet)
                        p2_bullet_time = p2_temp_btime
                # Quit game
                if event.key == pygame.K_ESCAPE:
                    done = True

            if event.type == pygame.KEYUP:
                # Player One controls
                if event.key == pygame.K_a and player_one.change_x < 0:
                    player_one.stop()
                if event.key == pygame.K_d and player_one.change_x > 0:
                    player_one.stop()
                # Player Two controls
                if event.key == pygame.K_LEFT and player_two.change_x < 0:
                    player_two.stop()
                if event.key == pygame.K_RIGHT and player_two.change_x > 0:
                    player_two.stop()

# --------------- Updates ----------------- 

        # Update the player
        current_level.update()
        active_sprite_list.update()

        # Update items in the level (for moving platforms)
        #current_level.update()
        
# ------------------- Check For Stun ------------------

        for player in active_sprite_list:

            player_stun_list = pygame.sprite.spritecollide(player, 
            current_level.bullet_list, False)
            
            # If player is hit by a bullet
            if player_stun_list:
                
                if player.pname != player_stun_list[0].player_name:
                    if player.stunned == False:
                        player.stun_wait = time.time()
                        
                        # Check if the player has cooled down since last stun
                        if player.stun_wait - player.stun_start >= 5:
                            player.stunned = True
                            player.stunned_direction = player.direction
                            player.stun_start = time.time()
                
        
# ------------ Check If Player Is Hit By Enemy ---------

        hit_players = pygame.sprite.groupcollide(active_sprite_list, 
        current_level.enemy_list, False, False)
        
        for hit_player in hit_players:
            
            # Send player to respawn point
            hit_player.rect.x = 585
            hit_player.rect.y = 100
            
            # Remove a life and point from hit player
            hit_player.lives -= 1
            if hit_player.pname == 'p1':
                player_one_score -= 1
            else:
                player_two_score -= 1
                
            # Need to add a delay and explosion class

# ----------- Check If Players Are Off Map ----------
 
        for guy in active_sprite_list:
            if guy.rect.y > constants.SCREEN_HEIGHT:
                
                # Move to the top middle platform
                guy.rect.x = 585
                guy.rect.y = 100
                
                # Minus a life
                guy.lives -= 1
                
                # Lose five points for falling death
                if guy.pname == 'p1':
                    player_one_score -= 5
                else:
                    player_two_score -= 5
                
# -------------- Bullet Impacts ------------

        # Lists of bullet impacts
        for bullet in current_level.bullet_list:
            
            bullet_hit_list = pygame.sprite.spritecollide(bullet, 
            current_level.enemy_list, False)
            
            for enemy in bullet_hit_list:
                
                enemy.health -= 1
                
                if enemy.health <= 0:
                    # Create explosion instance here
                    enemy.kill()
                    
                    if bullet.player_name == 'p1':
                        player_one_score += 1
                    else:
                        player_two_score += 1
                        
                bullet.kill()
                
        # Create an explosion in dead enemy's place
        #for enemy in enemy_explode:
        #    explosion = explosions.WalkerExplosion()
        #    explosion_list.add(explosion)

        
        bullet_wall_hit = pygame.sprite.groupcollide(level_list[0].bullet_list, 
        current_level.platform_list, True, False)
        
# ------------ Scoreboard Display ------------    
        
        # Set score to zero if it's negative
        if player_one_score < 0:
            player_one_score = 0
        elif player_two_score < 0:
            player_two_score = 0

        # Used to decide if score had changed
        if player_one_score != p1_old_score or player_two_score != p2_old_score:
        
            p1_old_score = player_one_score
            p2_old_score = player_two_score

            #Removes old scores from list
            scores_list.empty()

            # Returns images of player one's score
            new_score = scoreboard.display_score(player_one_score, 1)

            # Add player one's scores to list
            scores_list.add(new_score[0])
            scores_list.add(new_score[1])

            # Return images of player two's score
            new_score = scoreboard.display_score(player_two_score, 0)

            # Adds player two's score to list
            scores_list.add(new_score[0])
            scores_list.add(new_score[1])  


# --------------- Draw To Display ---------------
        
        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        scoreboard_list.draw(screen)
        scores_list.draw(screen)
        active_sprite_list.draw(screen)
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        
        if player_one_score >= 20:
            print 'PLAYER ONE WINS!!'
            done = True
        elif player_two_score >=20:
            print 'PLAYER TWO WINS!!'
            done = True

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()

if __name__ == "__main__":
    main()
