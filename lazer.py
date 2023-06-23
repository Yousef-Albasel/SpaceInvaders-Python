import pygame

class Lazer(pygame.sprite.Sprite):
    def __init__(self, pos , speed,bullet_num):
        super().__init__()
        self.image = pygame.image.load('assets/Bullet-0'+bullet_num+'.png').convert_alpha()
        self.image=pygame.transform.scale_by(self.image,4)
        self.rect = self.image.get_rect(center = pos)
        self.pos = pos
        self.speed = speed
    def destroy(self):
        if self.rect.y <= -50 or self.rect.y>=600 + 50:
            self.kill()
    def update(self):
        self.rect.y -= self.speed
        self.destroy()
