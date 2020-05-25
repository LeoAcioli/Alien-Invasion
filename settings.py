class Settings:
    def __init__(self):
        #screen things
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (230,230,230)
        #ship things
        self.ship_limit = 5
        self.superalien_hit =5
        #bullet things
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (250,0,100)
        self.bullets_allowed = 5
        #alien
        #How quickly it speeds up
        self.speedup_scale = 1.08

        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 1
        self.bullet_speed = 3.0
        self.alien_speed = 0.3
        #1 represents right, -1 left
        self.fleet_direction = -1
        self.alien_points = 50
    
    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale  
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)