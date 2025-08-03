import sys
import pygame
from settings import Settings
from ship import Ship
from arsenal import Arsenal
from alien_fleet import AlienFleet
from game_stats import GameStats
from time import sleep
from button import Button

class AlienInvasion:

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.settings.initialize_dynamic_settings()
        self.game_stats = GameStats(self.settings.starting_ship_count)
        self.screen = pygame.display.set_mode((self.settings.screen_w, self.settings.screen_h))
        pygame.display.set_caption(self.settings.name)
    
        self.running = True
        self.clock = pygame.time.Clock()

        
        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg, (self.settings.screen_w, self.settings.screen_h))

        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.7)

        self.impact_sound = pygame.mixer.Sound(self.settings.impact_sound)
        self.impact_sound.set_volume(0.7)

        self.ship = Ship(self, Arsenal(self))
        self.alien_fleet = AlienFleet(self)
        self.alien_fleet.create_fleet()
        self.game_active = False
        self.play_button = Button(self, 'Play')
    def run_game(self):
        # Game Loop
        while self.running:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self.alien_fleet.update_fleet()
                self._check_collisions()
            self._update_screen()
            self.clock.tick(self.settings.FPS)
    
    def _check_collisions(self):
    
        if self.ship.check_collisions(self.alien_fleet.fleet):#check collisions for ship
            self._check_game_status()#Alien fleet to reset
            
            

        #check collisions for aliens and bottom of screen
        if self.alien_fleet.check_fleet_bottom():
            self._check_game_status()
        #check collisions of projectiles and aliens
        collisions = self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)
        if collisions:
             self.impact_sound.play()
        
        if self.alien_fleet.check_destroyed_status():
            self._reset_level()
    def _check_game_status(self):
        if self.game_stats.ships_left > 0:
            self.game_stats.ships_left -= 1 #Subtract 1 life
            self._reset_level()
            sleep(0.5)
        else:
            self.game_active = False

    def _reset_level(self):
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet()
    def restart_game(self):
        self.game_active = True
        self._reset_level()
        self.ship._center_ship()
        pygame.mouse.set_visible(False)
    def _update_screen(self):
        self.screen.blit(self.bg, (0,0))
        self.ship.draw()
        self.alien_fleet.draw()
        if not self.game_active:
            self.play_button.draw()
            pygame.mouse.set_visible(True)
        pygame.display.flip()
        
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and self.game_active == True:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_button_clicked()

    def _check_button_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.play_button.check_clicked(mouse_pos):
            self.restart_game()

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            if self.ship.fire():
                self.laser_sound.play()
        elif event.key == pygame.K_q:
            pygame.quit()
            sys.exit()
    
    def _check_keyup_events(self, event):
         if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
         elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
