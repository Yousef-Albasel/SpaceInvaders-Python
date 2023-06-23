import pygame

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.status = []  # List to store the animation frames
        self.frame_index = 0  # Index of the current frame
        for i in range(1, 4):
            # Load each frame and add it to the status list
            self.status.append(pygame.image.load(f'assets/flame/flame010{i}.png').convert_alpha())
        self.image = self.status[int(self.frame_index)]  # Set the initial image
        self.pos = pos
        self.rect = self.image.get_rect(midbottom=self.pos)


    def update(self):
        self.frame_index += 0.25  # Increment the frame index
        if self.frame_index >= len(self.status):
            self.frame_index = 0  # Reset the frame index if it exceeds the number of frames
        self.image = self.status[int(self.frame_index)]  # Update the image based on the frame index
        self.image = pygame.transform.scale_by(self.image,4)
        self.rect = self.image.get_rect(center=self.pos)