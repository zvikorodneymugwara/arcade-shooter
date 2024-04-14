import pygame

#healthbar will change in length based on ratio of hp and max_hp
class HealthBar:
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp, surface):
        # draw green health bar over red. green health bar varies with the ratio of max_health and current health
        self.hp = hp
        ratio = self.hp/self.max_hp
        # draw black border first
        pygame.draw.rect(surface, 'black', (self.x - 2, self.y - 2, 154, 19))
        pygame.draw.rect(surface, 'red', (self.x, self.y, 150, 15))
        pygame.draw.rect(surface, 'green', (self.x, self.y, 150 * ratio, 15))


class EnemyHealth(HealthBar):
    def __init__(self, x, y, hp, max_hp):
        super().__init__(x, y, hp, max_hp)

    def draw(self, hp, len, surface):
        self.hp = hp
        ratio = self.hp/self.max_hp
        pygame.draw.rect(surface, 'red', (self.x, self.y, len, 5))
        pygame.draw.rect(surface, 'green', (self.x, self.y, len * ratio, 5))
