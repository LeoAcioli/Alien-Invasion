import pygame
from pygame.sprite import Sprite
from alien import Alien

class SuperAlien(Alien):
    def __init__(self, ai_game):
        super().__init__(ai_game)
        self.image = pygame.image.load('advancedAlien.png')
