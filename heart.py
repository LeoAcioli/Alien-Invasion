import pygame
from settings import Settings
from pygame.sprite import Sprite

class Heart(Sprite):
    def __init__(self,al_game):
        super().__init__()
        self.screen = al_game.screen
        self.settings = al_game.settings
        self.screen_rect = al_game.screen.get_rect()

        
        self.image = pygame.image.load('heart_2.gif')
        self.rect = self.image.get_rect()
        
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)