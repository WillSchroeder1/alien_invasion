import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #Create a bullet rect at (0,0) and then set correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)     #Creating the rectangle for the bullet
        self.rect.midtop = ai_game.ship.rect.midtop             #Makes the bullet appear from the midtop of the ship

        #Store the bullet's position as a decimal value
        self.y = float(self.rect.y)         #allows us to store decimals, allowing us to further tweak the bullet's speed


    def update(self):
        """Move the bullet up the screen"""
        #Update the decimal position of the bullet
        self.y -= self.settings.bullet_speed
        #Update the rect position
        self.rect.y = self.y        #use self.y to set the value of the rect


    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect) 