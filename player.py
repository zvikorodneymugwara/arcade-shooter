import pygame
from os import listdir
from bullet import Bullet
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, type, size, bullet_type):
        super().__init__()
        #image and animation
        self.animation_speed = 0.16
        self.flip = False
        self.animation_index = 0
        self.size = size
        self.type = type
        self.states = {'idle': [], 'run': [], 'jump': [], 'fall':[]}
        self.animation = 'idle'
        for anim in self.states:
            self.states[anim] = self.load_images(
                f'graphics/{type}/{anim}')
        self.image = self.states[self.animation][self.animation_index]
        self.rect = self.image.get_rect(topleft=(x,y))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.mask = pygame.mask.from_surface(self.image)
        #movement
        self.gravity = 0.7
        self.jump_height = -16
        self.moving_left = False
        self.moving_right = False
        self.on_ground = True
        self.in_air = False
        self.speed = 5
        self.direction = pygame.math.Vector2()
        #mechanics
        self.score = 0
        self.health = 100
        self.ammo = 8
        self.bullet_type = bullet_type
        self.bullets = pygame.sprite.Group()
        self.shot_timer = 1
        self.next_level = False
        self.alive = True
        
    def controls(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.shot_timer -= 1
            if self.shot_timer == 0:
                self.shoot()
                shoot_fx.play()
        if keys[pygame.K_w] and self.in_air is False:
            self.direction.y = self.jump_height
            if self.direction.y < 0:
                self.in_air = True
                self.on_ground = False
                jump.play()
        # if moving left and the player isnt off screen
        elif keys[pygame.K_a] and self.rect.x > 0:
            self.direction.x = -1
            self.animation = 'run'
            self.flip = True
        # if the player is moving right and is behind the scroll threshhold
        elif keys[pygame.K_d] and self.rect.right < 1280*0.84:
            self.direction.x = 1
            self.animation = 'run'
            self.flip = False
        else:
            self.animation = 'idle'
            self.direction.x = 0  # idle

    def shoot(self):
        self.ammo -= 1
        if self.shot_timer <= 0:
            self.shot_timer = 30
        #place bullet according to player diretion
        if self.ammo > 0:
            if self.flip:
                bullet = Bullet(self.rect.left,\
                    self.rect.centery-15, self.bullet_type)
                bullet.direction = -1
            else:
                bullet = Bullet(self.rect.right,\
                    self.rect.centery-15, self.bullet_type)
                bullet.direction = 1
            bullet.flip = self.flip
            self.bullets.add(bullet)

    def vertical_collision(self, world):
        self.apply_gravity()
        for tile in world:
            if tile.rect.colliderect(self.rect):
                # stop the player from going up if under a tile
                if self.direction.y < 0:
                    self.rect.top = tile.rect.bottom
                    self.direction.y = 0
                # stop the player from falling down if on a tile
                if self.direction.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.direction.y = 0
                    self.on_ground = True
        #if player is falling
        if self.on_ground and self.direction.y < 0 or self.direction.y > 1:
            self.on_ground = False
            self.in_air = True

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        if self.on_ground:
            self.in_air = False

    def horizontal_collision(self, world):
        self.rect.x += self.direction.x * self.speed
        for tile in world:
            # stop the player from moving left or right when they hit a wall
            if tile.rect.colliderect(self.rect.x + (self.direction.x*5), self.rect.y, self.width, self.height):
                if self.direction.x < 0:
                    self.rect.left = tile.rect.right
                    self.moving_left = False
                if self.direction.x > 0:
                    self.rect.right = tile.rect.left
                    self.moving_right = False
                self.direction.x = 0
            # controlls which animation is being shown
    def update_animation(self):
        if self.in_air:
            if self.direction.y < 0:
                self.animation = 'jump'
            elif self.direction.y > 0:
                self.animation = 'fall'
            
        if self.health > 100:
            self.health = 100
    # loads the images in the path for the animation and scales them
    def load_images(self, path):
        img_list = []
        frame_num = len(listdir(path))
        for i in range(frame_num):
            img = pygame.image.load(f'{path}/{i}.png').convert_alpha()
            img = pygame.transform.scale(img,(img.get_width()*self.size, img.get_height()*self.size))
            img_list.append(img)
        return img_list
    
    def animate(self):
        animation = self.states[self.animation]
        # if the index is greater than the number of frames, reset the index
        self.animation_index += self.animation_speed
        if self.animation_index >= len(animation):
            self.animation_index = 0

        self.image = animation[int(self.animation_index)]

    def draw(self, surface):
        surface.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        for b in self.bullets:
            b.draw(surface)
        # pygame.draw.rect(surface,'red',self.rect, 1)
    
    def update(self, tiles):
        self.update_animation()
        self.animate()
        self.controls()
        self.vertical_collision(tiles)
        self.horizontal_collision(tiles)
        for b in self.bullets:
            b.update(self)
        if self.health <= 0 or self.rect.bottom >= 720*0.85:
            self.health = 0
            self.alive = False
    