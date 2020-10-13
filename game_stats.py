class GameStats:
    "Track the stats for Alien Invasion"

    def __init__(self, ai_game):
        """Initialize stats"""
        self.settings = ai_game.settings
        self.reset_stats()
        #Start alieninvasion in an active state
        self.game_active = True
    def reset_stats(self):
        """Initialize stats that can change during the game"""
        self.ships_left = self.settings.ship_limit
