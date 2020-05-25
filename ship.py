import pygame
from settings import Settings
from pygame.sprite import Sprite
from heart import Heart

class Ship(Sprite):
    def __init__(self,al_game):
        super().__init__()
        self.screen = al_game.screen
        self.settings = al_game.settings
        self.screen_rect = al_game.screen.get_rect()

        #load the sahip image and its rect
        self.image = pygame.image.load('ship.bmp')
        self.rect = self.image.get_rect()
        #start each new ship at the left of screen
        self.rect.midleft= self.screen_rect.midleft
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        #moving flag
        self.moving_down = False
        self.moving_up= False
        self.moving_left = False
        self.moving_right = False

        self.heart = Heart(self) #avoid player to stay on top all the time

    def update(self):
        #update ships position based on movement flag
        if self.moving_right and (self.rect.right < self.screen_rect.right):
            self.x = self.x + self.settings.ship_speed
        elif self.moving_left and (self.rect.left > 0):
            self.x = self.x - self.settings.ship_speed
        elif self.moving_up and (self.rect.top > self.heart.rect.height*2): #so just ship can't be on top all the time avoiding aliens!
            self.y = self.y - self.settings.ship_speed
        elif self.moving_down and (self.rect.bottom < self.screen_rect.height ):
            self.y = self.y + self.settings.ship_speed
        #udpate rect location
        self.rect.y = self.y
        self.rect.x = self.x

    def blitme(self):
        #draw ship on its current location
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        self.rect.midleft = self.screen_rect.midleft
        self.y = float (self.rect.y)
