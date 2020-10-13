import sys      #Used to exit the game when the player quits.
import pygame       #Used to build the game
from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
    """Overall class to manage game assets and behavor."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))       #Creates a display window
        pygame.display.set_caption("Alien Invasion")        #

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        #Set the background color
        self.bg_color = (230,230,230)       #RGB

    def run_game(self):
        """Start the main loop for the game"""
        while True:         #runs continuously waiting for an event (user input)
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()
            # watch for keyboard and mouse events

    def _check_events(self):
        """Respond to keypress and mouse events"""
        for event in pygame.event.get():        #the event loop
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
        #Move the ship to the right.
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to Key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        #Update bullet positions.
        self.bullets.update()       #updates each bullet
            
             #Get rid of bullets that disappear
        for bullet in self.bullets.copy():      #Use copy b/c for py expects lists to stay the same length
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        #Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)     #.fill fills the background w the desired color
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

            #Make the most recently drawn screen visibile.
        pygame.display.flip()



if __name__ == '__main__':
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()