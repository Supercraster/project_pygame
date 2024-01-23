from pygame import *


class Platform(sprite.Sprite):
    def __init__(self, x, y, tip):
        sprite.Sprite.__init__(self)
        if tip == "grass":
            self.image = transform.scale(image.load("data/GrassCliffMid.png"), (50, 50))
        elif tip == "dirt":
            self.image = transform.scale(image.load("data/Dirt.png"), (50, 50))
        elif tip == "coin":
            self.image = transform.scale(image.load("data/coin.png"), (50, 50))
        elif tip == "spike":
            self.image = transform.scale(image.load("data/Spike_Up.png"), (50, 50))
        elif tip == "portal":
            self.image = transform.scale(image.load("data/portal.png"), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y