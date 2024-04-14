import pygame
from csv import reader
from pygame import mixer

mixer.init()  # initialize mixer for the audio

SCREEN_SCALE = 0.85
W, H = 1280*SCREEN_SCALE, 720*SCREEN_SCALE
FPS = 60
MENU_BUTTONS = ['START', 'OPTIONS', 'EXIT']
SETTINGS = ['EASY', 'MEDIUM', 'HARD', 'MUTE/UNMUTE', 'BACK']
SIZE = 32
BUTTON_SCALE = 0.12

vol = 0.25  #game volume
#images
ammo_box_img = pygame.image.load('graphics/Level/ammo box.png')
ammo_box_img = pygame.transform.scale(ammo_box_img, (60,32))
health_box_img = pygame.transform.scale(pygame.image.load('graphics/Level/health box.png'), (32,32))
door_img = pygame.image.load('graphics/Level/door.png')
door_img = pygame.transform.scale(door_img, (door_img.get_width()/2.5,door_img.get_height()/2.5))
bg_img = pygame.image.load('graphics/Level/background1.png')
bg_img_2 = pygame.image.load('graphics/Level/background2.png')
bg_img = pygame.transform.scale(bg_img, (W,H))
bg_img_2 = pygame.transform.scale(bg_img_2, (W,H))
bullet_img = pygame.image.load('graphics/bullet_icon.png')
bullet_img = pygame.transform.scale(bullet_img, (bullet_img.get_width()*0.02,bullet_img.get_height()*0.02))
char_1_img = pygame.image.load('graphics/Char 1/idle/0.png')
char_2_img = pygame.image.load('graphics/Char 2/idle/0.png')

# music
pygame.mixer.music.load('audio/music.wav')
pygame.mixer.music.set_volume(vol)
pygame.mixer.music.play(-1, 0, 2000)

#audio
machine_gun = pygame.mixer.Sound('audio/machine gun.wav')
hit = pygame.mixer.Sound('audio/hit.wav')
jump = pygame.mixer.Sound('audio/jump.wav')
nav = pygame.mixer.Sound('audio/menu_nav.wav')
pick_up = pygame.mixer.Sound('audio/pick up.wav')
pick_up_2 = pygame.mixer.Sound('audio/pick up 2.wav')
next_lvl = pygame.mixer.Sound('audio/win.wav')
shoot_fx = pygame.mixer.Sound('audio/shoot.wav')

machine_gun.set_volume(vol)
hit.set_volume(vol)
jump.set_volume(vol)
nav.set_volume(vol)
pick_up.set_volume(vol)
pick_up_2.set_volume(vol)
shoot_fx.set_volume(vol)
next_lvl.set_volume(vol)
pygame.mixer.music.set_volume(vol)

# controlls which level gets loaded
def select_level(lvl_num):
    lvl = {
        'ammo': f'graphics/Level/level {lvl_num}/level{lvl_num}_ammo.csv',
        'enemies' : f'graphics/Level/level {lvl_num}/level{lvl_num}_enemies.csv',
        'boss': f'graphics/Level/level {lvl_num}/level{lvl_num}_boss.csv',
        'constraints': f'graphics/Level/level {lvl_num}/level{lvl_num}_constraints.csv',
        'decor': f'graphics/Level/level {lvl_num}/level{lvl_num}_decor.csv',
        'end': f'graphics/Level/level {lvl_num}/level{lvl_num}_end.csv',
        'start': f'graphics/Level/level {lvl_num}/level{lvl_num}_start.csv',
        'ground': f'graphics/Level/level {lvl_num}/level{lvl_num}_ground.csv',
        'health': f'graphics/Level/level {lvl_num}/level{lvl_num}_health.csv'
    }
    return lvl

#draws text on screen
def draw_text(x, y, col, text, surface, font):
    img = font.render(text, True, col)
    surface.blit(img, (x, y))

# import csv for the level and return the terrain_map of the csv
def import_csv_layout(path):
    terrain_map = []

    with open(path) as level_map:
        level = reader(level_map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))

    return terrain_map

# takes the tileset and cuts the tiles into usable images
def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    surface = pygame.transform.scale(
        surface, (int(surface.get_width()*2), int(surface.get_height()*2)))
    x = int(surface.get_size()[0]/32)
    y = int(surface.get_size()[1]/32)
    cut_tiles = []
    for row in range(y):
        for col in range(x):
            xpos = col * 32
            ypos = row * 32
            new_surface = pygame.Surface(
                (32, 32), pygame.SRCALPHA)
            new_surface.fill(pygame.Color(0, 0, 0, 0))
            new_surface.blit(surface, (0, 0), pygame.Rect(
                xpos, ypos, 32, 32))
            cut_tiles.append(new_surface)

    return cut_tiles

# pause game function
# runs a second instance of pygame stopping the first one
def pause(clock, surface, resume_btn, exit_btn, font):
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    paused = False  # resume

        surface.fill('black')
        draw_text(W*0.44, 50, 'white', "PAUSED", surface, font)
        draw_text(W*0.31, 330, 'white', "Press M to resume...", surface, font)
        # surface.blit(paused_img, (W/3, H/5))
        if resume_btn.draw(surface):
            paused = False
        if exit_btn.draw(surface):
            paused = False
            pygame.quit()
            quit()

        clock.tick(60)
        pygame.display.update()


# change volume funtions
def change_audio_volume(volume):
    machine_gun.set_volume(volume)
    hit.set_volume(volume)
    jump.set_volume(volume)
    nav.set_volume(volume)
    pick_up.set_volume(volume)
    pick_up_2.set_volume(volume)
    shoot_fx.set_volume(volume)
    next_lvl.set_volume(volume)
    
def change_music_volume(volume):
    pygame.mixer.music.set_volume(volume)