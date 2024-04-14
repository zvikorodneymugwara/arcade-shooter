import pygame
from settings import *
from button import Button
from world import *

pygame.init()

pygame.display.set_caption('Shooter')
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
#fonts
menu_font = pygame.font.Font('gomarice_no_continue.ttf', 50)
death_font = pygame.font.Font('joystix monospace.otf', 72)
#menu images
menu_img = pygame.transform.scale(pygame.image.load('graphics/menu.jpg'), (W,H)).convert_alpha()
menu_img_2 = pygame.transform.scale(pygame.image.load('graphics/menu2.jpg'), (W,H)).convert_alpha()
#menu buttons
resume_button = Button(W*0.4-31, H*0.7-31, pygame.image.load('graphics/play-button.png').convert_alpha(), BUTTON_SCALE)
restart_button = Button(W*0.4-31, H*0.7-31, pygame.image.load('graphics/refresh.png').convert_alpha(), BUTTON_SCALE)
exit_button = Button(W*0.6-31, H*0.7-31, pygame.image.load('graphics/exit.png').convert_alpha(), BUTTON_SCALE)
home_button = Button(W*0.5-31, H*0.7-31, pygame.image.load('graphics/home.png').convert_alpha(), BUTTON_SCALE)
Buttons = [Button(W*0.3, H*0.5, char_1_img, 4), Button(W*0.7, H*0.5, char_2_img, 4)]

#game settings
diff = 0
char_type = 0
lvl_num = 2

#game conditions
run = True
display_menu = True
display_options = False
character_select = False
start_game = False
loaded = False
game_over = False

while run:
    clock.tick(FPS)

    #exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #for the main menu
    if display_menu:
        screen.blit(menu_img, (0,0))
        buttons = []
        #draw buttons
        for count, btn in enumerate(MENU_BUTTONS):
            buttons.append(Button(W*0.2, H*0.2*(count+1),
                           menu_font.render(MENU_BUTTONS[count], True, 'white'), 1))
            buttons[count].rect.x = W*0.2-buttons[count].image.get_width()/2
            # if the mouse hovers over the text, change the colour
            pos = pygame.mouse.get_pos()    #position of mouse
            if buttons[count].rect.collidepoint(pos):
                buttons[count].image = menu_font.render(
                    MENU_BUTTONS[count], True, 'red') #change colour when mouse hovers
            if buttons[count].draw(screen):
                if count == 0:  #starts game
                    display_menu = False
                    character_select = True
                if count == 1:  #shows options
                    display_options = True
                if count == 2:  #exit
                    run = False
                nav.play()
    
    if start_game:
        #load level
        if not loaded:
            world = Level(select_level(lvl_num), lvl_num, char_type, diff)
            loaded = True
        else:
            #draw background and level
            screen.blit(bg_img.convert_alpha(), (0,0))
            screen.blit(bg_img_2.convert_alpha(), (0,0))
            world.run(screen)
            #pause button
            pause_button = Button(W*0.95-31, H*0.08-31, pygame.image.load('graphics/pause-button.png').convert_alpha(), BUTTON_SCALE)
            if pause_button.draw(screen):
                pause(clock,screen,resume_button,exit_button,menu_font)
            for player in world.player:
                if player.next_level and lvl_num < 2:   #level progression
                    lvl_num += 1
                    loaded = False
                    player.next_level = False
                if player.alive is False:   #if the player is dead
                    game_over = True
        
    #character menu
    if character_select:
        pos = pygame.mouse.get_pos()
        screen.fill((232,235,218))
        draw_text(W*0.28, H*0.25, 'blue', 'SELECT A CHARACTER...',screen, menu_font)
        for count, btn in enumerate(Buttons):
            Buttons[count].rect.x = W*(0.3+(0.4*count))-Buttons[count].image.get_width()/2
            if Buttons[count].draw(screen):
                if count == 0:
                    char_type = 1
                if count == 1:
                    char_type = 2
                character_select = False
                start_game = True
                nav.play()
            if Buttons[count].rect.collidepoint(pos):
                pygame.draw.rect(screen, 'red', Buttons[count].rect, 6)

    #options menu
    if display_options:
        pos = pygame.mouse.get_pos()
        btns = []
        display_menu = False
        screen.blit(menu_img_2, (0,0))  #background image
        #draw buttons
        for count, choice in enumerate(SETTINGS):
            btns.append(Button(W*0.65, H*0.15*(count+1), menu_font.render(SETTINGS[count], True, 'black'), 1))
            if btns[count].rect.collidepoint(pos):
                btns[count].image = menu_font.render(
                    SETTINGS[count], True, 'blue')
            if btns[count].draw(screen):
                if count == 0:
                    diff = count    #easy
                    display_options = False
                    display_menu = True
                elif count == 3:
                    if vol != 0:
                        vol = 0 #mute
                    else:
                        vol = 0.25  #unmute
                    change_audio_volume(vol)
                    change_music_volume(vol)
                elif count == 4:
                    #back button
                    display_options = False
                    display_menu = True
                else:
                    diff = count * 2    #medium and hard
                display_options = False
                display_menu = True
                nav.play()

    #game over screen
    if game_over:
        start_game = False
        loaded = False
        screen.fill('black')
        draw_text(W*0.28, H*0.4, "red", "YOU DIED!", screen, death_font)
        if exit_button.draw(screen):
            run = False #exit
            nav.play()
        if home_button.draw(screen):
            game_over = False   #main menu
            display_menu = True
            nav.play()
        if restart_button.draw(screen):
            game_over = False   #restart level
            start_game = True
            nav.play()

    pygame.display.update()
