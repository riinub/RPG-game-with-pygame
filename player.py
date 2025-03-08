from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collison_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(join("images", "player", "down","0.png")).convert_alpha()
        self.rect = self.image.get_frect(center = pos) 

        #movement
        self.direction = pygame.Vector2()
        self.speed = 500
        self.colliision_spritres = collison_sprites
        
        #hitbox 
        self.hitbox_rect = self.rect.inflate(-60, 0)



    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        #normalization
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt #handles the left/right side movement of player.rect
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt #handles the up/down movement of player.rect
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center #for player movement


    def collision(self, direction):
        #sprite collision logic
        for sprite in self.colliision_spritres: #for sprites in sprite group
            if sprite.rect.colliderect(self.hitbox_rect): #check for any collisions b/w sprites
                if direction == 'horizontal':
                    #check if the obj is moving in the positive x direction(moving right) 
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left 
                    '''When the player or an object collides with something while moving right,
                        this code adjusts the position so they stop exactly at the edge of what they hit, 
                        preventing overlap.'''
                    #check for moving left 
                    if self.direction.x < 0 : self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom #moving up
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top #moving down

    def update(self, dt):
        self.input()
        self.move(dt)