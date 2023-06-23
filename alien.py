import pygame 
class Alien(pygame.sprite.Sprite):
    def __init__(self,color,x,y):
        super().__init__()
        file_path = 'assets/Aliens/alien-'+color+'.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.image = pygame.transform.scale_by(self.image,5)
        self.rect = self.image.get_rect(topleft = (x,y))
    def update(self,direction):
        self.rect.x+=direction

class Extra(pygame.sprite.Sprite):
    def __init__(self,side,color):
        super().__init__()
        self.image= pygame.image.load('assets/Aliens/Special-'+color+'.png').convert_alpha()
        self.image = pygame.transform.scale_by(self.image,5)

        if side=='right':
            x = 650
            self.speed = -3
        if side == 'left':
            x = -50
            self.speed = 3

        self.rect = self.image.get_rect(topleft = (x,30))
    def update(self):
        self.rect.x +=self.speed

class H_Alien(pygame.sprite.Sprite):
    def __init__(self,num,pos,speed):
        super().__init__()
        self.image = pygame.image.load('assets/Higher-Aliens/H-Alien0'+num+'.png')
        self.image = pygame.transform.scale_by(self.image,4)
        self.rect = self.image.get_rect(topleft= pos)
        self.speed = speed
    def update(self):
        self.rect.y += self.speed


class Meteor(pygame.sprite.Sprite):
    def __init__(self,num,pos,speed):
        super().__init__()
        self.image = pygame.image.load('assets/Higher-Aliens/Meteorite-0'+num+'.png')
        self.image = pygame.transform.scale_by(self.image,4)
        self.rect = self.image.get_rect(topleft= pos)
        self.speed = speed
    def update(self):
        self.rect.y += self.speed