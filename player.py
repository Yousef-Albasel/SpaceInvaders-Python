import pygame 
from lazer import *

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
        self.rect = self.image.get_rect(center = pos)
	


    def update(self,pos):
        self.frame_index += 0.25  # Increment the frame index
        if self.frame_index >= len(self.status):
            self.frame_index = 0  # Reset the frame index if it exceeds the number of frames
        self.image = self.status[int(self.frame_index)]  
        self.image = pygame.transform.scale_by(self.image,3)
        self.rect = self.image.get_rect(center=pos)
	

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,constraint,speed):
		super().__init__()
		self.status = []
		self.status.append(pygame.image.load('assets/ship-01.png').convert_alpha())
		self.status.append(pygame.image.load('assets/ship-01-right.png').convert_alpha())
		self.status.append(pygame.image.load('assets/ship-01-left.png').convert_alpha())
		# Main Attributes
		self.image = self.status[0]
		self.image = pygame.transform.scale_by(self.image,4)
		self.rect = self.image.get_rect(midbottom = pos)
		self.speed = speed
		self.max_x_constraint = constraint
		self.ready = True

		
		# Laser and flame Attr
		self.laser_time = 0
		self.laser_cooldown = 400
		self.lasers = pygame.sprite.Group()
		self.flame = Generic((self.rect.centerx,self.rect.centery+17))
		self.flame_group = pygame.sprite.GroupSingle(self.flame)
		self.direction = pygame.math.Vector2()


		

	def get_input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT]:
			self.rect.x += self.speed
			self.direction.x = 1
		elif keys[pygame.K_LEFT]:		
			self.direction.x = -1
			self.rect.x -= self.speed		
		else:	
			self.direction.x = 0


		if keys[pygame.K_SPACE] and self.ready:
			self.shoot_lazer()
			self.ready = False
			self.laser_time = pygame.time.get_ticks()
	def switch_image(self):
		if self.direction.x == 1 :
			self.get_status(1)
		elif self.direction.x == -1 :
			self.get_status(2)
		else:
			self.get_status(0)

	def recharge(self):
		if not self.ready:
			current_time = pygame.time.get_ticks()
			if current_time - self.laser_time >= self.laser_cooldown:
				self.ready = True

	def constraint(self):
		if self.rect.left <= 0:
			self.rect.left = 0
		if self.rect.right >= self.max_x_constraint:
			self.rect.right = self.max_x_constraint
	def shoot_lazer(self):
		self.lasers.add(Lazer(self.rect.center,4,'1'))
	def get_status(self,i):
		self.image = self.status[i]	
		self.image = pygame.transform.scale_by(self.image,4)
		
	def update(self):
		self.get_input()
		self.constraint()
		self.recharge()
		self.lasers.update()
		self.flame_group.update((self.rect.centerx,self.rect.centery+17))
		self.switch_image()
