import pygame
from tile import Tile

class Bullet(Tile):
    def __init__(self, x: int, y: int, type: int):
        super().__init__(x,y)
        self.image = pygame.image.load(
            f'graphics/bullet{type}.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 6
        self.direction = 0
        self.flip = False
        self.mask = pygame.mask.from_surface(self.image)
        self.health_taken = False
    
    def draw(self, surface):
        surface.blit(pygame.transform.flip(self.image,self.flip,False), self.rect)

    #if the bullet collides with something, take health if it can and kill the bullet
    def collision(self, dmg, target, take_health):
        for t in target:
            if t.rect.colliderect(self.rect):
                if take_health and not self.health_taken and t.alive:
                    t.health -= dmg
                    self.health_taken = True
                    self.kill()
                elif not take_health:
                    self.kill()
            
    def update(self, player):
        self.scroll(player) #scroll the bullet wrt the player
        self.rect.x += self.speed*self.direction
        if self.rect.x > 1280*0.85 or self.rect.x < 0:
            self.kill()
