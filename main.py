from settings import *
from player import Player
from sprite import *
from groups import AllSprites
from pytmx.util_pygame import load_pygame
from random import randint
class Game:
    def __init__ (self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("survivor")
        self.clock = pygame.time.Clock()
        self.running = True

        #Groups
        self.all_sprites = AllSprites()
        self.collision_sprite = pygame.sprite.Group()
        self.setup()
        

        self.player = Player((400, 300), self.all_sprites, self.collision_sprite)
        

    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))
        #tiled layer
        for x,y,image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites))

        #object layer
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprite))

        #collison layer
        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprite)

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000

            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            #update
            self.all_sprites.update(dt)


            #draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

    pygame.quit()    


if __name__ == '__main__':
    game = Game()
    game.run()