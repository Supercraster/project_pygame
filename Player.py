from pygame import *
import pyganim

MOVE_SPEED = 6
SIZE = (40, 38)
GRAVITY = 0.37
JUMP_POWER = 18

ANIMATION_DELAY = 0.1
ANIMATION_STAY = [(transform.scale(image.load("data/hero/Hobbit - idle1.png"), SIZE), ANIMATION_DELAY),
                  (transform.scale(image.load("data/hero/Hobbit - idle2.png"), SIZE), ANIMATION_DELAY),
                  (transform.scale(image.load("data/hero/Hobbit - idle3.png"), SIZE), ANIMATION_DELAY),
                  (transform.scale(image.load("data/hero/Hobbit - idle4.png"), SIZE), ANIMATION_DELAY)]

ANIMATION_RIGHT = [(transform.scale(image.load("data/hero/Hobbit - run1.png"), SIZE)),
                   (transform.scale(image.load("data/hero/Hobbit - run2.png"), SIZE)),
                   (transform.scale(image.load("data/hero/Hobbit - run3.png"), SIZE)),
                   (transform.scale(image.load("data/hero/Hobbit - run4.png"), SIZE)),
                   (transform.scale(image.load("data/hero/Hobbit - run5.png"), SIZE)),
                   (transform.scale(image.load("data/hero/Hobbit - run6.png"), SIZE)),
                   (transform.scale(image.load("data/hero/Hobbit - run7.png"), SIZE)),
                   (transform.scale(image.load("data/hero/Hobbit - run8.png"), SIZE)),
                   (transform.scale(image.load("data/hero/Hobbit - run9.png"), SIZE)),
                   (transform.scale(image.load("data/hero/Hobbit - run10.png"), SIZE)),]

ANIMATION_LEFT = [(transform.flip(transform.scale(image.load("data/hero/Hobbit - run1.png"), SIZE), True, False)),
                   (transform.flip(transform.scale(image.load("data/hero/Hobbit - run2.png"), SIZE), True, False)),
                   (transform.flip(transform.scale(image.load("data/hero/Hobbit - run3.png"), SIZE), True, False)),
                   (transform.flip(transform.scale(image.load("data/hero/Hobbit - run4.png"), SIZE), True, False)),
                   (transform.flip(transform.scale(image.load("data/hero/Hobbit - run5.png"), SIZE), True, False)),
                   (transform.flip(transform.scale(image.load("data/hero/Hobbit - run6.png"), SIZE), True, False)),
                   (transform.flip(transform.scale(image.load("data/hero/Hobbit - run7.png"), SIZE), True, False)),
                   (transform.flip(transform.scale(image.load("data/hero/Hobbit - run8.png"), SIZE), True, False)),
                   (transform.flip(transform.scale(image.load("data/hero/Hobbit - run9.png"), SIZE), True, False)),
                   (transform.flip(transform.scale(image.load("data/hero/Hobbit - run10.png"), SIZE), True, False))]

class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0  # скорость перемещения
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?
        self.image = Surface(SIZE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image.set_colorkey((0, 0, 0))

        def make_boltAnim(anim_list, delay):
            boltAnim = []
            for anim in anim_list:
                boltAnim.append((anim, delay))
            Anim = pyganim.PygAnimation(boltAnim)
            return Anim

        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()

        self.boltAnimRight = make_boltAnim(ANIMATION_RIGHT, ANIMATION_DELAY)
        self.boltAnimRight.play()

        self.boltAnimLeft = make_boltAnim(ANIMATION_LEFT, ANIMATION_DELAY)
        self.boltAnimLeft.play()

    def update(self, left, right, up, platforms, spikes, portals, coins):
        if left:
            self.xvel = -MOVE_SPEED  # Лево = x- n
            self.image.fill((0, 0, 0))
            self.boltAnimLeft.blit(self.image, (0, 0))

        if right:
            self.xvel = MOVE_SPEED  # Право = x + n
            self.image.fill((0, 0, 0))
            self.boltAnimRight.blit(self.image, (0, 0))

        if up:
            if self.onGround:
                self.yvel = -JUMP_POWER

        if not (left or right):
            self.xvel = 0
            if not up:
                self.image.fill((0, 0, 0))
                self.boltAnimStay.blit(self.image, (0, 0))

        self.onGround = False
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)
        if not self.onGround:
            self.yvel += GRAVITY
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)
        self.collide_spikes(spikes)
        self.collide_portal(portals)
        self.collide_coins(coins)

    def collide_coins(self, coins):
        for p in coins:
            if sprite.collide_rect(self, p):
                print('монетка')


    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def collide_spikes(self, spikes):
        for p in spikes:
            if sprite.collide_rect(self, p):
                self.rect.x = 55
                self.rect.y = 600

    def collide_portal(self, portals):
        for p in portals:
            if sprite.collide_rect(self, p):
                return True

    def teleport(self):
        self.rect.x = 55
        self.rect.y = 600

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком
                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает
            if not sprite.collide_rect(self, p) and self.yvel > 0:
                self.onGround = False