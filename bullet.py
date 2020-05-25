import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):

    def __init__(self, al_game):
        super().__init__()
        self.screen = al_game.screen
        self.settings = al_game.settings
        self.color = self.settings.bullet_color
    
        #create bullet rect at (0,0) and then set correct position
        self.rect = pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
        self.rect.midtop = al_game.ship.rect.midright

        self.x = float(self.rect.x)
        #sound effect!
        #pygame.mixer.Sound("‪C:/Users/leona/Desktop/pew.wav").play()

    def update(self):
        #move bullet up the screen
        self.x += self.settings.bullet_speed
        #update rect position
        self.rect.x = self.x

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
