import pygame
class Explosion(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.status = []  # List to store the animation frames
        self.frame_index = 0  # Index of the current frame
        for i in range(1, 4):
            # Load each frame and add it to the status list
            self.status.append(pygame.image.load(f'assets/explosion/explosion-0{i}.png').convert_alpha())
        self.image = self.status[int(self.frame_index)]  # Set the initial image
        self.pos = pos
        self.rect = self.image.get_rect(center = pos)

    def update(self):
        self.frame_index += 0.25  # Increment the frame index
        if self.frame_index >= len(self.status):
            self.frame_index= 0
            self.kill()
        self.image = self.status[int(self.frame_index)]  
        self.image = pygame.transform.scale_by(self.image,4)

class PowerUps(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.image.load('assets/ExtraHeart-0001.png')
        self.image = pygame.transform.scale_by(self.image,5)
        self.rect = self.image.get_rect(center =(pos))
    def update(self):
        self.rect.y +=4
        if (self.rect.y >650):
            self.kill()
        