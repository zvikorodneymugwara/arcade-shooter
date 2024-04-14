import pygame
from settings import *
from tile import *
from player import *
from healthbar import *
from enemies import *

class Level:
    def __init__(self, level_data, level_num, player_num, difficulty):
        self.p_num = player_num
        self.difficulty = difficulty
        self.level_num = level_num
        # all the sprites
        #bombs
        ammo_sprites = import_csv_layout(level_data['ammo'])
        self.ammo_sprites = self.create_tile_group(ammo_sprites, 'ammo')

        #cannons
        enemies_sprites = import_csv_layout(level_data['enemies'])
        self.enemies_sprites = self.create_tile_group(
            enemies_sprites, 'enemies')

        #coins
        boss_sprites = import_csv_layout(level_data['boss'])
        self.boss_sprites = self.create_tile_group(boss_sprites, 'boss')

        #decor
        decor_sprites = import_csv_layout(level_data['decor'])
        self.decor_sprites = self.create_tile_group(decor_sprites, 'decor')

        #exits
        end_sprites = import_csv_layout(level_data['end'])
        self.end_sprites = self.create_tile_group(end_sprites, 'end')

        #hearts
        health_sprites = import_csv_layout(level_data['health'])
        self.health_sprites = self.create_tile_group(health_sprites, 'health')

        #platforms
        ground = import_csv_layout(level_data['ground'])
        self.ground_sprites = self.create_tile_group(ground, 'ground')
        
        #platforms
        constraints = import_csv_layout(level_data['constraints'])
        self.constraints_sprites = self.create_tile_group(constraints, 'constraints')
        
        # start position and player
        start_pos = import_csv_layout(level_data['start'])
        self.player = self.create_tile_group(start_pos, 'start')
        self.p = pygame.sprite.GroupSingle()

        for p in self.player:
            self.p.add(p)
    #this iterates throught the csv file and places a tile image in the respective positions
    #it then returns the group of tiles that were requested e.g 'platforms' or 'bombs'
    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, value in enumerate(row):
                if value != '-1':   #if not empty space, add an object at that position
                    x = col_index * 32
                    y = row_index * 32

                    if type == 'ground':
                        terrain_list = import_cut_graphics(
                            'graphics/Level/prop pack.png')
                        tile_surface = terrain_list[int(value)]
                        sprite_group.add(WorldTile(x, y+4, tile_surface))

                    if type == 'ammo':
                        sprite_group.add(WorldTile(x, y+4, ammo_box_img.convert_alpha()))

                    if type == 'health':
                        sprite_group.add(WorldTile(x, y+4, health_box_img.convert_alpha()))

                    if type == 'enemies':
                        sprite_group.add(Robot(x, y-55, self.difficulty))

                    if type == 'boss':
                        sprite_group.add(Boss(x, y-118, self.difficulty))

                    if type == 'decor':
                        terrain_list = import_cut_graphics(
                            'graphics/Level/prop pack.png')
                        tile_surface = terrain_list[int(value)]
                        sprite_group.add(WorldTile(x, y+4, tile_surface))

                    if type == 'end':
                        sprite_group.add(WorldTile(x, y-80, door_img.convert_alpha()))

                    if type == "constraints":
                        sprite_group.add(Tile(x, y))

                    if type == "start":
                        sprite_group.add(Player(x, y+(4 + (self.p_num - 1)*4), f'Char {self.p_num}', 2, 1))

        return sprite_group
    
    #all the logic of the game
    def game_logic(self):
        #progress to next level when at door
        for sprite in self.end_sprites:
            for p in self.player:
                if sprite.rect.colliderect(p.rect) and self.level_num < 2:
                    p.next_level = True
                    next_lvl.play()
                elif sprite.rect.colliderect(p.rect) and self.level_num >= 2:
                    pygame.quit()
        
        #health box pick up
        for sprite in self.health_sprites:
            for p in self.player:
                if sprite.rect.colliderect(p.rect):
                    p.health += 30
                    sprite.kill()
                    pick_up.play()
                    
        #ammo box pick up
        for sprite in self.ammo_sprites:
            for p in self.player:
                if sprite.rect.colliderect(p.rect):
                    p.ammo += 5
                    sprite.kill()
                    pick_up_2.play()
        
        #increase player score if enemy is felled
        for sprite in self.enemies_sprites:
            for p in self.player:
                if sprite.alive is False and sprite.player_score_increased is False:
                    p.score += 20
                    sprite.player_score_increased = True

        for sprite in self.boss_sprites:
            for p in self.player:
                if sprite.alive is False and sprite.player_score_increased is False:
                    p.score += 100
                    sprite.player_score_increased = True
    
    def run(self, surface):
        f2 = pygame.font.Font('gomarice_no_continue.ttf', 36)   #font used

        #draw all the sprites from the group
        self.ground_sprites.draw(surface)
        self.decor_sprites.draw(surface)
        self.health_sprites.draw(surface)
        self.ammo_sprites.draw(surface)
        self.end_sprites.draw(surface)
        self.game_logic()
        
        #draw and update enemy bullets
        for b in self.boss_sprites:
            b.draw_enemy(surface)
            for bullet in b.bullets:
                bullet.collision(7*(1+b.difficulty/8),self.player, True)
                bullet.collision(7*(1+b.difficulty/8),self.ground_sprites, False)
                for p in self.player:
                    if bullet.rect.colliderect(p):
                        hit.play()
                
        for e in self.enemies_sprites:
            e.draw_enemy(surface)
            for bullet in e.bullets:
                bullet.collision(5*(1+e.difficulty/8),self.player, True)
                bullet.collision(5*(1+e.difficulty/8),self.ground_sprites, False)
                for p in self.player:
                    if bullet.rect.colliderect(p):
                        hit.play()
                
        for p in self.player:
            p.draw(surface) #draw player
            p.update(self.ground_sprites)   #update player
            p_health = HealthBar(50,50,p.health,100)    #player healthbar
            p_health.draw(p.health, surface)    #draw player healthbar
            
            for x in range(0, p.ammo+1):
                surface.blit(bullet_img, (50+bullet_img.get_width()*x, 110)) #place a coin on the ui
            draw_text(50, 70, 'gold', f'Score: {str(p.score)}', surface, f2)    #draw the player score
            for b in p.bullets:
                #update bullets shot from the players gun
                b.collision(25,self.ground_sprites, False)
                b.collision(25,self.boss_sprites, True)
                b.collision(25,self.enemies_sprites, True)
                            
            self.enemies_sprites.update(p, self.constraints_sprites)
            self.health_sprites.update(p)
            self.ammo_sprites.update(p)
            self.ground_sprites.update(p)
            self.decor_sprites.update(p)
            self.boss_sprites.update(p, self.constraints_sprites)
            self.end_sprites.update(p)
            self.constraints_sprites.update(p)
