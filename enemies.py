import pygame
from tile import TILE_SIZE, Tile
from os import listdir
from bullet import Bullet
from random import choice, randint
from healthbar import EnemyHealth
from settings import *

class Character(Tile):
    def __init__(self, x, y, char_type, size, bullet_type):
        super().__init__(x,y)
        self.bullet_type = bullet_type
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.attack_speed = 1
        self.direction = pygame.math.Vector2()
        self.attack_cooldown = 30
        self.attack = False
        self.alive = True
        self.flip = False
        self.size = size
        self.bullets = pygame.sprite.Group()
        self.animation_index = 0
        self.animation_speed = 0.16
        self.type = char_type
    # loads the images in the path for the animation and scales them
    def load_images(self, path):
        img_list = []
        frame_num = len(listdir(path))
        for i in range(frame_num):
            img = pygame.image.load(f'{path}/{i}.png').convert_alpha()
            img = pygame.transform.scale(img,(img.get_width()*self.size, img.get_height()*self.size))
            img_list.append(img)
        return img_list
    
    #create a bullet, add it to the group then draw it in the draw function
    def shoot(self):
        bullet = Bullet(self.rect.x+(self.direction.x*self.image.get_width()/3), self.rect.centery-self.image.get_height()/4, self.bullet_type)
        bullet.direction = self.direction.x
        bullet.flip = self.flip
        self.bullets.add(bullet)
    
    #controlls rate of enemy fire
    def update_shoot(self):
        if self.attack:
            self.attack_cooldown -= self.attack_speed
            if self.attack_cooldown <= 0:
                self.shoot()
                shoot_fx.play()
                self.attack_cooldown = 30
        if self.attack is False:
            self.attack_cooldown = 30

    def animate(self):
        animation = self.states[self.animation]
        # if the index is greater than the number of frames, reset the index
        self.animation_index += self.animation_speed
        if self.animation_index >= len(animation):
            if self.alive:
                self.animation_index = 0
            else:
                self.animation_index = len(animation)-1

        self.image = animation[int(self.animation_index)]

    def draw(self, surface):
        self.bullets.draw(surface)
        surface.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class Enemy(Character):
    def __init__(self, x: int, y: int, enemy_type: str, size: int, difficulty: int, bullet_type):
        super().__init__(x, y, enemy_type, size, bullet_type)
        self.states = {'Walk': [], 'Attack': [], 'Death': []}
        self.animation = 'Walk'
        self.direction.x = choice([-1, 1])  #enemies patrol in random directions
        self.difficulty = difficulty    #enemy attributes linked to difficulty
        self.speed = randint(2,3)*(1+self.difficulty/8)
        # for each animation state, load the images for the animation
        for anim in self.states:
            self.states[anim] = self.load_images(
                f'graphics/{self.type}/{anim}')
        self.image = self.states[self.animation][self.animation_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        #attack rect for enemy to attack player if within this rect
        self.attack_rect = pygame.Rect(self.rect.x, self.rect.y, self.width*2, self.height)
        self.player_score_increased = False
        self.mask = pygame.mask.from_surface(self.image)
        
    #enemy ai
    def ai(self, player, constraints):
        #enemy is dead if health is 0
        if self.health <= 0:
            self.health = 0
            self.alive = False
        
        #change direction if the enemy runs into a constraint
        for c in constraints:
            if c.rect.colliderect(self.rect.x + (self.direction.x*20), self.rect.y,\
                                  self.image.get_width(), self.image.get_height()):
                self.direction.x *= -1

        #enemy moves if alive
        if self.alive:
            self.rect.x += self.direction.x*self.speed

        #enemy stops to attack player else it continues on patrol
        if self.attack:
            self.speed = 0
            self.animation = 'Attack'
        else:
            self.speed = randint(2,3)*(1+self.difficulty/8)
            
        #animation controll
        if self.speed != 0:
            self.animation = 'Walk'
        if self.alive is False:
            self.animation = 'Death'
        
        #if the enemy is alive and the player is within range, attack the player
        if self.alive:
            if player.rect.colliderect(self.attack_rect) and player.alive:
                self.speed = 0
                self.attack = True
            else:
                self.speed = randint(2,3)*(1+self.difficulty/8)
                self.attack = False

    def draw_enemy(self, surface):
        surface.blit(pygame.transform.flip(
            self.image, self.flip, False), self.rect)
        for b in self.bullets:
            b.draw(surface)

    def update(self, player, constraints):
        #update enemies and bullets wrt to player
        self.scroll(player)
        self.animate()
        self.ai(player, constraints)
        if self.alive:
            self.update_shoot()
        for b in self.bullets:
            b.update(player)


class Boss(Enemy):
    def __init__(self, x: int, y: int, difficulty: int):
        super().__init__(x, y, 'Boss', 2.5, difficulty, 2)
        self.health = 250*(1+self.difficulty/8)
        self.ypos = y
        self.max_health = self.health

    #boss shoots 2 bullets from its machine gun
    def shoot(self):
        machine_gun.play()
        for x in range(0,2):
            if self.flip:
                bullet = Bullet(self.rect.right+30+(x*15),\
                self.rect.centery-5+(x*25), self.bullet_type)
            else:
                bullet = Bullet(self.rect.left+(x*15),\
                self.rect.centery-5+(x*25), self.bullet_type)
            bullet.direction = self.direction.x
            bullet.flip = self.flip
            self.bullets.add(bullet)
        
    #boss image needs to be flipped differently
    def ai(self, player, constraints):
        if self.direction.x > 0:
            self.flip = True
        else:
            self.flip = False
            
        if not self.flip:
            self.attack_rect = pygame.Rect(
                self.rect.left-self.width*2, self.rect.y, self.width*2, self.height)
        else:
            self.attack_rect = pygame.Rect(
                self.rect.right, self.rect.y, self.width*2, self.height)

        return super().ai(player, constraints)
    
    def draw_enemy(self, surface):
        if self.alive:
            health = EnemyHealth(
                self.rect.x, self.rect.y-10, self.health, self.max_health)
            health.draw(self.health, self.rect.width, surface)
        return super().draw_enemy(surface)

class Robot(Enemy):
    def __init__(self, x: int, y: int, difficulty: int):
        super().__init__(x, y, 'Robot Gaurd', 1.2, difficulty, 3)
        self.health = 50*(1+self.difficulty/8)
        self.animation_speed = 0.08
        self.attack_cooldown = 80
        self.max_health = self.health

    def ai(self, player, constraints):
        if self.direction.x < 0:
            self.flip = True
        else:
            self.flip = False
        if self.flip:
            self.attack_rect = pygame.Rect(
                self.rect.left-self.width*2, self.rect.y, self.width*2, self.height)
        else:
            self.attack_rect = pygame.Rect(
                self.rect.right, self.rect.y, self.width*2, self.height)

        return super().ai(player, constraints)
    
    def draw_enemy(self, surface):
        if self.alive:
            health = EnemyHealth(
                self.rect.x, self.rect.y-10, self.health, self.max_health)
            health.draw(self.health, self.rect.width, surface)
        return super().draw_enemy(surface)