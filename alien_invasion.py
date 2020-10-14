import sys      #Used to exit the game when the player quits.
from time import sleep      #allows the pause function
import pygame       #Used to build the game
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien 

class AlienInvasion:
    """Overall class to manage game assets and behavor."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))       #Creates a display window
        pygame.display.set_caption("Alien Invasion")        #

        #Create an instance to store game stats & scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #Make play button
        self.play_button = Button(self, "Play")
        
        #Set the background color
        self.bg_color = (230,230,230)       #RGB

    def run_game(self):
        """Start the main loop for the game"""
        while True:         #runs continuously waiting for an event (user input)
            self._check_events()
            
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                
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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()      #must click button
                    self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #Reset the game settings
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            #Hide the mouse curser
            pygame.mouse.set_visible(False)

            #Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleet
            self._create_fleet()
            self.ship.center_ship()

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

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collision"""
        #Remove and bullets and aliens that have collided.
        #Check for any bullets that have hit aliens. IF so, get rid of the bullet and alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)      #true -> delete the bullets and aliens (false,true) = super bullets
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)      #Get points every time an alien is shot
            self.sb.prep_score()
            self.sb.check_high_score()


        if not self.aliens:     #is aliens group empty?
            #Destroy exisiting bullets ad create a new fleet
            self.bullets.empty()    #deletes existing bullets
            self._create_fleet()    #creates new fleet
            self.settings.increase_speed()

            #increase level
            self.stats.level +=1
            self.sb.prep_level()

    def _update_aliens(self):
        """Check if alien is at the edge --> Update the position of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        #look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        #Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        #Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)     #.fill fills the background w the desired color
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        #Draw the score info
        self.sb.show_score()

        #Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

            #Make the most recently drawn screen visibile.
        pygame.display.flip()

    def _create_fleet(self):
        """Create the fleet of aliens"""
        #Create an alien and find the number of aliens in a row.
        #Spacing between each alien is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size       #storing the width to call later
        avaliable_space_x = self.settings.screen_width - (2 * alien_width)      #avaliable horizontal space and # of aliens that can fit
        number_aliens_x = avaliable_space_x // (2 * alien_width)

        #Determine the number of rows of aliens tht fit on the screen
        ship_height = self.ship.rect.height
        avaliable_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = avaliable_space_y // (2 * alien_height)

        #Create a full fleet of aliens
        for row_number in range (number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
            #Create an alien and place it in the row.
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
            self.aliens.add(alien)

    def _check_fleet_edges(self):   
        """Respond appropriatly if any aliens have reached an edge"""
        for alien in self.aliens.sprites():         #is alien at the edge?
            if alien.check_edges():
                self._change_fleet_direction()
                break       #break the loop
    
    def _change_fleet_direction(self):
        """Drop the fleet and change the direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed      #Drop the fleet
        self.settings.fleet_direction *= -1     #change the dirrection

    def _ship_hit(self):
        """Respond to the ship being hit"""
        if self.stats.ships_left > 0:
            #Decrement ships_left
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #Get rid of any reamining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            #Creae a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #Pause
            sleep(0.5)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #Treat this the same as if the ship got hit
                self._ship_hit()
                break

if __name__ == '__main__':
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()