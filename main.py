# importuju co potrebuji
import pygame
import button
from sys import exit
from map import World
from tetris import Tetris

pygame.init()
pygame.mixer.init()

# obrazovka, hodinky, keys
screen_w = 1280
screen_h = 800
screen = pygame.display.set_mode((screen_w,screen_h))
clock = pygame.time.Clock()
key = pygame.key.get_pressed()
pygame.mixer.music.load("assets/Music/musik.mp3")
pygame.mixer.music.play(-1)

# tetris
tetris = Tetris(screen)

# Fonty
font = pygame.font.Font(None, 60)
font2 = pygame.font.Font(None, 40)

# Mapy
Start = World("assets/Start/start.tmx", screen)
Game = World("assets/PLay/mapa.tmx", screen)
Tutorial = World("assets/Tutorial/tutorial.tmx", screen)
Level = World("assets/Choose/choosing.tmx", screen)

# Tlacitka
start_img = pygame.image.load("assets/Start/start.png")
play_img = pygame.image.load("assets/Tutorial/play.png")
pause_img = pygame.image.load("assets/PLay/pause.png")

start_button = button.Button(450, 620, start_img, 10)
play_button = button.Button(870, 650, play_img, 8)
pause_button = button.Button(70, 185, pause_img, 6)

# Menu
menu_img = pygame.image.load("assets/Play/Menu/menu.png")
resume_img = pygame.image.load("assets/Play/Menu/resume.png")
quit_img = pygame.image.load("assets/Play/Menu/quit.png")
safety = pygame.image.load("assets/Play/safety.png")

resume_button = button.Button(490, 300, resume_img, 8)
quit_button = button.Button(490, 500, quit_img, 8)

# Texty
drop_img = pygame.image.load("assets/Tutorial/Texts/drop.png")
rotate_img = pygame.image.load("assets/Tutorial/Texts/rotate.png")
move_left_img = pygame.image.load("assets/Tutorial/Texts/left.png")
move_right_img = pygame.image.load("assets/Tutorial/Texts/right.png")
score_img = pygame.image.load("assets/Play/score.png")
top_score_img = pygame.image.load("assets/Play/top_score.png")

# Šipky
up_img = pygame.image.load("assets/Tutorial/Keys/up.png")
down_img = pygame.image.load("assets/Tutorial/Keys/down.png")
left_img = pygame.image.load("assets/Tutorial/Keys/left.png")
right_img = pygame.image.load("assets/Tutorial/Keys/right.png")

# Levlely
lvl_0 = pygame.image.load("assets/Choose/level_0.png")
lvl_1 = pygame.image.load("assets/Choose/level_1.png")
lvl_2 = pygame.image.load("assets/Choose/level_2.png")
lvl_3 = pygame.image.load("assets/Choose/level_3.png")
lvl_4 = pygame.image.load("assets/Choose/level_4.png")
lvl_5 = pygame.image.load("assets/Choose/level_5.png")
lvl_6 = pygame.image.load("assets/Choose/level_6.png")
lvl_7 = pygame.image.load("assets/Choose/level_7.png")
lvl_8 = pygame.image.load("assets/Choose/level_8.png")
lvl_9 = pygame.image.load("assets/Choose/level_9.png")

level_0 = button.Button(365, 270, lvl_0, 7)
level_1 = button.Button(475, 270, lvl_1, 7)
level_2 = button.Button(585, 270, lvl_2, 7)
level_3 = button.Button(695, 270, lvl_3, 7)
level_4 = button.Button(805, 270, lvl_4, 7)
level_5 = button.Button(365, 470, lvl_5, 7)
level_6 = button.Button(475, 470, lvl_6, 7)
level_7 = button.Button(585, 470, lvl_7, 7)
level_8 = button.Button(695, 470, lvl_8, 7)
level_9 = button.Button(805, 470, lvl_9, 7)

# Bloky
L_img = pygame.image.load("assets/Block_images/L.png")
J_img = pygame.image.load("assets/Block_images/J.png")
O_img = pygame.image.load("assets/Block_images/O.png")
Z_img = pygame.image.load("assets/Block_images/Z.png")
S_img = pygame.image.load("assets/Block_images/S.png")
T_img = pygame.image.load("assets/Block_images/T.png")
I_img = pygame.image.load("assets/Block_images/I.png")

# Skore
top_points = 0

# Stavy
game_started = True
game_choose = False
game_pause = False
game_playing = False
game_tutorial = False

# Cyklus
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            tetris.control(key=event.key)

# Start
    if game_started == True:
        pygame.display.update()
        Start.draw_background()

        if start_button.draw(screen):
            game_started = False
            game_choose = True

# Vyber levelu
    if game_choose == True:
        pygame.display.update()
        Level.draw_background()

        if level_0.draw(screen):
            tetris.lines_destroyed = 0
            game_choose = False
            game_tutorial = True
        if level_1.draw(screen):
            tetris.lines_destroyed = 10
            game_choose = False
            game_tutorial = True
        if level_2.draw(screen):
            tetris.lines_destroyed = 20
            game_choose = False
            game_tutorial = True
        if level_3.draw(screen):
            tetris.lines_destroyed = 30
            game_choose = False
            game_tutorial = True
        if level_4.draw(screen):
            tetris.lines_destroyed = 40
            game_choose = False
            game_tutorial = True
        if level_5.draw(screen):
            tetris.lines_destroyed = 50
            game_choose = False
            game_tutorial = True
        if level_6.draw(screen):
            tetris.lines_destroyed = 60
            game_choose = False
            game_tutorial = True
        if level_7.draw(screen):
            tetris.lines_destroyed = 70
            game_choose = False
            game_tutorial = True
        if level_8.draw(screen):
            tetris.lines_destroyed = 80
            game_choose = False
            game_tutorial = True
        if level_9.draw(screen):
            tetris.lines_destroyed = 90
            game_choose = False
            game_tutorial = True



# Menu
    if game_pause == True:
        pygame.display.update()
        screen.blit(menu_img, [200, 150])

        if resume_button.draw(screen):
            game_pause = False
            game_playing = True
        if quit_button.draw(screen):
            pygame.quit()

# Tutorial 
    if game_tutorial == True:
        pygame.display.update()
        Tutorial.draw_background()

        screen.blit(rotate_img, [350, 340])
        screen.blit(drop_img, [350, 240])
        screen.blit(move_left_img, [350, 440])
        screen.blit(move_right_img, [350, 540])

        screen.blit(down_img, [830, 230])
        screen.blit(up_img, [830, 330])
        screen.blit(left_img, [830, 430])
        screen.blit(right_img, [830, 530])

        if play_button.draw(screen):
            game_tutorial = False
            game_playing = True

# Hra
    if game_playing == True:

        pygame.display.update()
        Game.draw_background()

        tetris.update()
        tetris.draw()
        tetris.control(key)

        screen.blit(score_img, [1015, 320])
        screen.blit(top_score_img, [980, 500])
        screen.blit(safety,[464,1])
        
        if tetris.points > top_points:
            top_points = tetris.points

        score = font.render(f"{tetris.points : 04d}", False, "#FFFFFF")
        top_score = font.render(f"{top_points : 04d}", False, "#FFFFFF")

        screen.blit(score, (1035 , 400))
        screen.blit(top_score, (1035 , 570))

        screen.blit(L_img, [80, 340])
        screen.blit(J_img, [80, 380])
        screen.blit(Z_img, [80, 420])
        screen.blit(S_img, [80, 460])
        screen.blit(O_img, [80, 500])
        screen.blit(T_img, [80, 540])
        screen.blit(I_img, [80, 580])

        L_score = font2.render(f"{tetris.L_points : 04d}", False, "#FFFFFF")
        J_score = font2.render(f"{tetris.J_points : 04d}", False, "#FFFFFF")
        Z_score = font2.render(f"{tetris.Z_points : 04d}", False, "#FFFFFF")
        S_score = font2.render(f"{tetris.S_points : 04d}", False, "#FFFFFF")
        O_score = font2.render(f"{tetris.O_points : 04d}", False, "#FFFFFF")
        T_score = font2.render(f"{tetris.T_points : 04d}", False, "#FFFFFF")
        I_score = font2.render(f"{tetris.I_points : 04d}", False, "#FFFFFF")

        screen.blit(L_score, (200 , 335))
        screen.blit(J_score, (200 , 375))
        screen.blit(Z_score, (200 , 415))
        screen.blit(S_score, (200 , 455))
        screen.blit(O_score, (200 , 495))
        screen.blit(T_score, (200 , 535))
        screen.blit(I_score, (200 , 575))

        if pause_button.draw(screen):
            game_pause = True
            game_playing = False

    clock.tick(60)
    