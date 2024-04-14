import pygame
TILE_SIZE = 32

# basic grey tile class
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.image.fill('grey')

    #draw tile screen
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def scroll(self, player):
        # update the x position of tile based on player position on screen
        if player.rect.right >= 700 and player.direction.x > 0:
            player.speed = 0
            self.rect.x -= 5
        elif player.rect.left <= 400 and player.direction.x < 0:
            player.speed = 0
            self.rect.x += 5
        else:
            player.speed = 5

    def update(self, player):
        self.scroll(player)

# world tile is the basic tile, but the tile image (surface) must be loaded
class WorldTile(Tile):
    def __init__(self, x, y, surface):
        super().__init__(x, y)
        self.image = surface
        self.mask = pygame.mask.from_surface(self.image)


# a handful of the world object we see
# they all just have different paths to their images

class Exit(WorldTile):
    def __init__(self, x, y):
        super().__init__(x, y, surface=pygame.image.load(
            'graphics/Level/door.png').convert_alpha())
        self.image = pygame.transform.scale(
            self.image, (self.image.get_width()*0.3, self.image.get_height()*0.3))

class Ammo(WorldTile):
    def __init__(self, x, y):
        super().__init__(x, y, surface=pygame.image.load(
            'graphics/Level/ammo box.png').convert_alpha())
        self.image = pygame.transform.scale(
            self.image, (self.image.get_width()*0.3, self.image.get_height()*0.3))

class HealthBox(WorldTile):
    def __init__(self, x, y):
        super().__init__(x, y, surface=pygame.image.load(
            'graphics/Level/health box.png').convert_alpha())
        self.image = pygame.transform.scale(
            self.image, (self.image.get_width(), self.image.get_height()))
