import pygame , sys
from player import *
from lazer import *
import obstacles
from alien import *
from random import choice,randint
from lazer import Lazer
from particles import *
class Game:
    def __init__(self):
        self.game_state = 'level-one'
    # usual method for class , sprites groups
        player_sprite = Player((screen_width/2,screen_heigt-30),600,4)
        self.player =  pygame.sprite.GroupSingle(player_sprite)
		# Health and score 
        self.lives = 3
        self.live_surface = pygame.image.load('assets/health.png').convert_alpha()
        self.live_surface = pygame.transform.scale_by(self.live_surface,4)
        self.live_x_startpos = screen_width - (self.live_surface.get_size()[0] * 2 + 0)

		# Creating Obstacles
        self.shape = obstacles.shape
        self.block_size = 4
        self.obstacle_amount = 4
        self.blocks=pygame.sprite.Group()
        self.obstacle_x_positions =[ num * (screen_width/self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions,stx=screen_width/13,sty=480)
        # Creating Aliens 
        self.aliens = pygame.sprite.Group()
        self.alien_setup(rows=6,cols=8,x_distance=70,y_distance=40,x_offset = 30, y_offset = 30)
        self.alien_direction =1
        self.alien_lazers= pygame.sprite.Group()

        # creating special Aliens
        self.aliens_special = pygame.sprite.Group()
        self.special_aliens_spawn_time = randint(400,800)
        # particles
        self.explosions = pygame.sprite.Group()
        self.extra_hearts = pygame.sprite.Group()
        # Score
        self.score = 0
        self.game_font = pygame.font.Font('fonts/munro.ttf',26)
        self.score_surface = self.game_font.render(f'  {self.score}  ',False,'White') 
        self.score_rect = self.score_surface.get_rect(center =(25,22))
        # H-Aliens 
        self.h_alien_spawn_time = randint(50,150)
        self.h_aliens=pygame.sprite.Group()      
        self.h_aliens_counter=0;  
        # Meteorite
        self.meteorite_spawn_time = randint(600,1000)
        self.meteorite=pygame.sprite.Group()
    def create_obstacles(self,stx,sty,offset_x):
        for row_idx ,row in enumerate(self.shape):
            for col_idx,col in enumerate(row):
                if col == 'x':
                    x = stx + col_idx * self.block_size + offset_x
                    y = sty + row_idx * self.block_size
                    block = obstacles.Block(self.block_size,(241,97,80),x,y)
                    self.blocks.add(block)
    def create_multiple_obstacles(self,*offset,stx,sty):
        for offset_x in offset:
            self.create_obstacles(stx,sty,offset_x)

    # Alien Functions
    def alien_setup(self,rows,cols,x_distance,y_distance,x_offset,y_offset):
        for row_idx,row in enumerate(range(rows)):
            for col_idx,col in enumerate(range(cols)):
                x = col_idx * x_distance + x_offset
                y = row_idx * y_distance + y_offset
                if row_idx == 0:
                    alien_sprite = Alien('white',x,y)
                elif row_idx >= 1 and row_idx < 3:
                    alien_sprite = Alien('yellow',x,y)
                else:
                    alien_sprite = Alien('green',x,y)


                self.aliens.add(alien_sprite)
    def alien_pos_checkout(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens :
            if alien.rect.right >= 600:
                self.alien_direction = -1
                self.alien_movement_down(1)
            if alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_movement_down(1)

    def alien_movement_down(self,distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y+=distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            lazer_sprite = Lazer(random_alien.rect.center,-3,'2')
            self.alien_lazers.add(lazer_sprite)
        if self.h_aliens.sprites():
            random_h_alien = choice(self.h_aliens.sprites())
            lazer_sprite = Lazer(random_h_alien.rect.center,-3,'2')
            self.alien_lazers.add(lazer_sprite)

    def special_alien_timer(self):
        self.special_aliens_spawn_time-=1
        if self.special_aliens_spawn_time <=0:
            self.aliens_special.add(Extra(choice(['right','left']),choice(['green','blue'])))
            self.special_aliens_spawn_time = randint(400,800)

    # Misc. FUNCTIONS
    def extra_hearts_showup(self):
        self.Extra_hearts_place = randint(0,600)
        self.extra_hearts.add(PowerUps((self.Extra_hearts_place,0)))

    def collision_checks(self):
        # Player Collisions
        if self.player:
            for player in self.player:
                if pygame.sprite.spritecollide(player,self.blocks,True):
                    pass
            for alien in self.aliens:
                if pygame.sprite.spritecollide(player,self.aliens,True):
                    pygame.quit()
                    sys.exit()
            for h_alien in self.h_aliens:
                if pygame.sprite.spritecollide(player,self.h_aliens,True):
                    pygame.quit()
                    sys.exit()
            for meteor in self.meteorite:
                if pygame.sprite.spritecollide(player,self.meteorite,True):
                    pygame.quit()
                    sys.exit()
        # Hearts Collisions
        if self.extra_hearts:
            for heart in self.extra_hearts:
                if pygame.sprite.spritecollide(heart,self.player,False):
                    if self.lives>=5:
                        pass
                    else:
                        self.lives+=1
                    print(self.lives)
                    heart.kill()
        # Player Lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                for alien in self.aliens:
                    if pygame.sprite.spritecollide(laser, self.blocks, True):
                        laser.kill()                

                    if pygame.sprite.spritecollide(laser, self.aliens, True):
                        laser.kill()
                        self.call_explosion((laser.rect.x+10,laser.rect.y-20))

                    if pygame.sprite.spritecollide(laser, self.aliens_special, True):
                        self.call_explosion((laser.rect.x+10,laser.rect.y-20))
                        self.score+=100
                        laser.kill()
                    
                for h_alien in self.h_aliens:
                    if pygame.sprite.spritecollide(laser, self.h_aliens, True):
                        self.call_explosion((laser.rect.x+10,laser.rect.y-20))
                        laser.kill()
                        self.h_aliens_counter+=1
                for meteor in self.meteorite:
                    if pygame.sprite.spritecollide(laser, self.meteorite, False):
                        laser.kill()
                        
        if self.alien_lazers:
            for laser in self.alien_lazers:
                if pygame.sprite.spritecollide(laser, self.player, False):
                    self.lives-=1
                    laser.kill()
                    if self.lives<=0:
                        pygame.quit()
                        sys.exit() 
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()      

        # Aliens
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien,self.blocks,True)
            if pygame.sprite.spritecollide(alien,self.player,True):
                pygame.quit()
                sys.exit()
    def display_lives(self):
        for live in range(self.lives-1):
            x = self.live_x_startpos - (live*(self.live_surface.get_size()[0]+10))
            screen.blit(self.live_surface,(x,10))
    def call_explosion(self,pos):
        self.explosions.add(Explosion(pos))
    def update_score(self):
        self.score+=1
        self.score_surface = self.game_font.render(f'  {self.score}  ',False,'White') 
    
    # Higher Aliens Fucntions


    def h_alien_timer(self):
        self.h_alien_spawn_time -=1
        if self.h_alien_spawn_time <=0:
            self.h_aliens.add(H_Alien(str(randint(0,9)),(randint(30,570),0),4))
            self.h_alien_spawn_time = randint(100,200)    
    
    def meteorite_timer(self):
        self.meteorite_spawn_time -=1
        if self.meteorite_spawn_time <=0:
            self.meteorite.add(Meteor(str(randint(1,2)),(randint(30,570),0),4))
            self.meteorite_spawn_time = randint(100,200)
    def h_aliens_destroy(self):
        for alien in self.h_aliens:
            if (alien.rect.y >= 650):
                self.lives -=1
                alien.kill()


    def run_l1(self):

        # update all sprite groups and draw all sprite groups
        self.player.update()
        self.player.sprite.flame_group.draw(screen)
        self.player.draw(screen)
        self.player.sprite.lasers.draw(screen)
        self.display_lives()
        self.extra_hearts.draw(screen)
        self.extra_hearts.update()
        self.explosions.draw(screen)
        self.collision_checks()
        self.blocks.draw(screen)
        self.explosions.update()
        self.aliens.update(self.alien_direction)
        self.alien_pos_checkout()
        self.alien_lazers.update()
        self.special_alien_timer()
        self.aliens_special.update()
        self.aliens.draw(screen)
        self.alien_lazers.draw(screen)
        self.aliens_special.draw(screen)
        screen.blit(self.score_surface,self.score_rect)
        if(not self.aliens):
            self.player.sprite.rect.y -=3
        if(self.player.sprite.rect.y <= -50):
            self.game_state='level-two'
    def run_l2(self):
        # update all sprite groups and draw all sprite groups
        self.player.update()
        self.player.sprite.flame_group.draw(screen)
        self.player.draw(screen)
        self.player.sprite.lasers.draw(screen)
        if self.h_aliens_counter < 20:
            self.player.sprite.rect.y=500
        self.display_lives()
        self.extra_hearts.draw(screen)
        self.extra_hearts.update()
        self.explosions.draw(screen)
        self.collision_checks()
        self.explosions.update()
        screen.blit(self.score_surface,self.score_rect)
        self.h_alien_timer()
        self.h_aliens.draw(screen)
        self.h_aliens.update()        
        self.meteorite_timer()
        self.meteorite.draw(screen)
        self.meteorite.update()
        self.h_aliens_destroy()
        if self.lives<=0:
            pygame.quit()
            sys.exit()  
        if (self.h_aliens_counter >= 20):
            self.player.sprite.rect.y -=3
            if(self.player.sprite.rect.y <= -50):
                self.game_state='level-three'
                
        print(self.h_aliens_counter)
        print(self.game_state)
    def run_l3(self):
            # update all sprite groups and draw all sprite groups
            self.player.update()
            self.player.sprite.flame_group.draw(screen)
            self.player.draw(screen)
            self.player.sprite.lasers.draw(screen)
            self.player.sprite.rect.y=500
            self.display_lives()
            self.extra_hearts.draw(screen)
            self.extra_hearts.update()
            self.explosions.draw(screen)
            self.collision_checks()
            self.explosions.update()
            screen.blit(self.score_surface,self.score_rect)

if __name__=='__main__':
    pygame.init()
    screen_width = 600
    screen_heigt = 600
    bg = pygame.image.load('assets/bg.jpeg')
    y = -600
    screen = pygame.display.set_mode((screen_width,screen_heigt))
    clock = pygame.time.Clock()
    game = Game()
    ALIIENLAZER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIIENLAZER ,800)
    
    EXTRAHEARTS = pygame.USEREVENT + 2
    pygame.time.set_timer(EXTRAHEARTS ,15000)    

    SCORECOUNTER = pygame.USEREVENT + 3
    pygame.time.set_timer(SCORECOUNTER ,1000)

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIIENLAZER:
                game.alien_shoot()            
            if event.type == SCORECOUNTER:
                game.update_score()
            if event.type == EXTRAHEARTS:
                game.extra_hearts_showup()



        if game.game_state=='level-one':
            screen.blit(bg,(0,y))
            y += 4
            if ( y == 0 ):
                y = -600
            game.run_l1()
        elif game.game_state =='level-two':
            screen.blit(bg,(0,y))
            y += 4
            if ( y == 0 ):
                y = -600
            game.run_l2()
        elif game.game_state == 'level-three':
            screen.blit(bg,(0,y))
            y += 4
            if ( y == 0 ):
                y = -600
            game.run_l3()

        pygame.display.update()
        clock.tick(60)