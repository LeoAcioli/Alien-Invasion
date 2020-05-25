from settings import Settings
from ship import Ship
from bullet import Bullet
import sys
import pygame
from alien import Alien 
from time import sleep 
from game_stats import GameStats
from button import Button
from scoreBoard import Scoreboard
import random
from superalien import SuperAlien

class AlienInvasion:
    #to manage general behaviors of game
    def __init__ (self): 
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion!")

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.superaliens = pygame.sprite.Group()

        self._create_fleet()

        self.play_button = Button(self,"PLAY")
       

    def run_game (self):
        #start main loop of game
        while True:
            self. _check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_all_aliens()

            self._update_screen()
           
    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_hearts()
            self.bullets.empty()
            sleep(0.1)
        else:
            self.stats.game_active = False 
            pygame.mouse.set_visible(True) 
        
            
    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
                if bullet.rect.right > self.settings.screen_width:
                    self.bullets.remove(bullet)

        collisions = pygame.sprite.groupcollide (self.bullets, self.aliens, True, True)
        #true true stands for when bullet AND alien,respectively, collide they both get destroyed
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points *len(aliens)
                self.sb.prep_score()
                self.sb.check_high_score()

        collisionssuper = pygame.sprite.groupcollide (self.bullets, self.superaliens, True, False) #deletes bullet but not superalien 
        if collisionssuper:
            self.stats.hits_left -= 1
            if self.stats.hits_left <= 0 :
                for superalien in collisionssuper.values():
                    self.superaliens.remove(superalien)
                    self.stats.score += self.settings.alien_points *len(superalien) *3 #three times the points for killing super alien!
                    self.sb.prep_score()
                    self.sb.check_high_score()
            

        if ((not self.aliens) and (not self.superaliens)) :
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level+=1
            self.sb.prep_level()
            self.stats.reset_superalienhit() #everytime a new fleet comes reset the number of hits to kill superalien


    def _update_all_aliens(self):
        #check if its on edge first
        self._check_fleet_edges()
        self.aliens.update()
        self.superaliens.update() # for superaliens
        alien = pygame.sprite.spritecollideany(self.ship,self.aliens, collided = None) #return WHICH ALIEN was hit with the method
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
            self.aliens.remove(alien) #delete which ALIEN was hit  
        superalien = pygame.sprite.spritecollideany(self.ship,self.superaliens, collided = None) #return WHICH ALIEN was hit with the method
        if pygame.sprite.spritecollideany(self.ship,self.superaliens):
            self._ship_hit()
            self.superaliens.remove(superalien) #delete which SUPERALIEN was hit  
        

    def _update_screen(self):
            #Redraw the screen during each iteration of loop
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
            #Make the most recently drawn screen visible.
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)
            self.superaliens.draw(self.screen) #draw SUPER ALIEN
            self.sb.show_score()

            if not self.stats.game_active:
                self.play_button.draw_button()

            pygame.display.flip()  #caused me A LOT of trouble!


    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._key_down_events(event)
            elif event.type == pygame.KEYUP:
                self._key_up_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    
    def _check_play_button(self, mouse_pos): #ALSO RESET GAME METHOD
        button_clicked =  self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_hearts()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            pygame.mouse.set_visible(True)
            

    def _key_down_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True  #MOVING UP AND DOWN ADDED
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

            
    def _key_up_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:  
            self.ship.moving_down = False


    def _fire_bullet(self):
        if len(self.bullets)<self.settings.bullets_allowed:  
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _create_fleet(self):
        #ALIENS######
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3* alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        available_space_x = self.settings.screen_width - (2*alien_width)#for borders
        number_aliens_x = available_space_x // (2*alien_width)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
        
        #SUPERALIENS#######
        superalien = SuperAlien(self)
        superalien_width, superalien_height = superalien.rect.size

        for x in range(2):
            for y in range(2):
                self._create_superalien(x,y)
        
        

    def _check_fleet_edges(self): #USED TO DELETE ALIENS IF OFF SCREEN
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.aliens.remove(alien) #if alien goes off the screen just delete it  
                break
        for superalien in self.superaliens.sprites():
            if superalien.check_edges():                   #FOR SUPER ALIENS
                self.superaliens.remove(superalien)
                break

    def _create_alien(self, alien_number, col_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = self.settings.screen_width #To make it appear out of screen
        alien.rect.x = alien.x
        for x in range (1):
            y = random.randint(alien_height, self.settings.screen_height-alien_height) #creates alien at random position in the y axis
        alien.rect.y = y

        it_collides = False
        for alienloop in self.aliens.sprites():
            colliding = pygame.sprite.collide_rect(alien,alienloop)
            if colliding:
                it_collides = True                                       #GETS RID OF COLLIDING ALIENS!
                break
            else:
                continue
        if not it_collides:
            self.aliens.add(alien)
    
    def _create_superalien (self,superalien_number,col_number):
        superalien = SuperAlien(self)
        superalien_width, superalien_height = superalien.rect.size
        superalien.x = self.settings.screen_width * 1.5 #To make it appear out of screen after normal aliens
        superalien.rect.x = superalien.x
        for x in range (1):
            y = random.randint(superalien_height, self.settings.screen_height- superalien_height) #creates alien at random position in the y axis
        superalien.rect.y = y

        it_collides = False
        for superalienloop in self.superaliens.sprites():
            colliding = pygame.sprite.collide_rect(superalien,superalienloop)
            if colliding:
                it_collides = True                                       #GETS RID OF COLLIDING SUPERALIENS!
                break
            else:
                continue
        if not it_collides:
            self.superaliens.add(superalien)  #CAUSE ALL THE PROBLEMS!
    


if __name__ == "__main__":
    # Make a game instance, then run the game
    ai = AlienInvasion()
    ai.run_game()

    


