import sys
import pygame
import os
from Player import Player
from Platforms import Platform


SIZE = (900, 700)
Gamee = False
collected_coins = 0

window = pygame.display.set_mode(SIZE)
screen = pygame.Surface(SIZE)
clock = pygame.time.Clock()

pygame.mixer.init()
music_file = "m.mp3"
pygame.mixer.music.load(music_file)
pygame.mixer.music.set_volume(0.04)

pygame.init()

portal_entries = 0


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


with open('results.txt', 'w') as res:
    res.write(str(int(collected_coins)))


def start_screen():
    intro_text = ["гма", "",
                  "Проект от: Артемия Шульгина и Адизова Дени"]

    fon = pygame.transform.scale(pygame.image.load('fon.jpg'), SIZE)
    window.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        window.blit(string_rendered, intro_rect)

    while True:
        global Gamee
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                Gamee = True
                return

        pygame.display.flip()
        clock.tick(50)


def final_screen(result):
    intro_text = ["Конец нашей великой игры", f"{result} монет собрано", ""
                  "Проект от: Артемия Шульгина и Адизова Дени"]

    fon = pygame.transform.scale(pygame.image.load('fon2.jpeg'), SIZE)
    window.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('purple'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        window.blit(string_rendered, intro_rect)

    while True:
        global Gamee
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
                Gamee = False
                return

        pygame.display.flip()
        clock.tick(50)


class BackGround(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("data/Background.png"), SIZE)
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y


class Camera:
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_func(camera, target_rect):
    l = -target_rect.x + SIZE[0] / 2
    t = -target_rect.y + SIZE[1] / 2
    w, h = camera.width, camera.height

    l = min(0, l)
    l = max(-(camera.width - SIZE[0]), l)
    t = max(-(camera.height - SIZE[1]), t)
    t = min(0, t)

    return pygame.Rect(l, t, w, h)


hero = Player(55, 850)
Back = BackGround(0, 0)
left = right = up = False

level1 = [
       "#                                 #",
       "#                                 #",
       "#                                 #",
       "#    0                            #",
       "#    --    - --                   #",
       "#               -                 #",
       "#                   -    -        #",
       "#                           -     #",
       "#                                 #",
       "#                         -       #",
       "#                     -           #",
       "#                 -               #",
       "#             -                   #",
       "#        -                        #",
       "#                                 #",
       "#    -                            #",
       "#  $$                             #",
       "#  --          ^              --- #",
       "#--##-------------^^-^^-^^----###-#"]

level2 = [
       "#                                 #",
       "#                                 #",
       "#                                 #",
       "#                                 #",
       "#                                 #",
       "#                                 #",
       "#                                 #",
       "#                                 #",
       "#                                 #",
       "#                                 #",
       "#       0                         #",
       "#       --     --                 #",
       "#                   -             #",
       "#                      -          #",
       "#                  -              #",
       "#            -   -               -#",
       "#       $   -#                    #",
       "#       --                    --- #",
       "#--##^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#"]


def load_level(level):
    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Platform(x, y, "grass")
                sprite_group.add(pf)
                platforms.append(pf)
            elif col == "#":
                pf = Platform(x, y, "dirt")
                sprite_group.add(pf)
                platforms.append(pf)
            elif col == "^":
                pf = Platform(x, y, "spike")
                sprite_group.add(pf)
                spikes.append(pf)
            elif col == "$":
                pf = Platform(x, y, "coin")
                sprite_group.add(pf)
                coins.append(pf)
            elif col == "0":
                pf = Platform(x, y, "portal")
                sprite_group.add(pf)
                portals.append(pf)
            x += 50
        y += 50
        x = 0


sprite_group = pygame.sprite.Group()
BackGround_group = pygame.sprite.Group()
levels = [level1, level2]

sprite_group.add(hero)
BackGround_group.add(Back)
coins = []
platforms = []
spikes = []
portals = []

game = True
timer = pygame.time.Clock()
pygame.display.set_caption('RedSquare2')
n = 0
load_level(levels[n])

level_width = len(levels[n][0]) * 50
level_height = len(levels[n]) * 50

start_screen()
if pygame.mixer.music.get_busy():
    pygame.mixer.music.stop()
else:
    pygame.mixer.music.play(-1)

camera = Camera(camera_func, level_width, level_height)
while game:
    for e in pygame.event.get():
        if e .type == pygame.QUIT:
            game = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_a:
            left = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_d:
            right = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            up = True

        if e.type == pygame.KEYUP and e.key == pygame.K_d:
            right = False
        if e.type == pygame.KEYUP and e.key == pygame.K_a:
            left = False
        if e.type == pygame.KEYUP and e.key == pygame.K_SPACE:
            up = False

    screen.fill((10, 120, 10))
    BackGround_group.draw(screen)
    hero.update(left, right, up, platforms, spikes, portals, coins)
    for p in coins:
        if hero.is_collided_with(p):
            collected_coins += 1
            coins.remove(p)
            p.kill()
    if hero.collide_portal(portals):
        sprite_group.empty()
        platforms = []
        spikes = []
        portals = []
        coins = []
        n = (n + 1) % 2
        portal_entries += 1
        load_level(levels[n])
        hero.teleport()
        sprite_group.add(hero)
        sprite_group.draw(screen)
        if portal_entries % 2 == 0:
            final_screen(collected_coins)
    camera.update(hero)
    for c in sprite_group:
        screen.blit(c.image, camera.apply(c))
    window.blit(screen, (0, 0))
    timer.tick(60)

    pygame.display.flip()
