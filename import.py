import sys
import pygame
import random
from pygame.locals import *


pygame.init()



''' IMAGES '''
player_ship = 'Assets/plyship.png'
enemy_ship = 'Assets/enemyship.png'
ufo_ship = 'Assets/ufo.png'
player_bullet = 'Assets/pbullet.png'
enemy_bullet = 'Assets/enemybullet.png'
ufo_bullet = 'Assets/enemybullet.png'
live_player = 'Assets/plyship.png'
pointer_mouse_blue = 'Assets/pointer.png'
pointer_mouse_red = 'Assets/pointer_merah.png'
start_background = 'Assets/background.jpg'



''' SOUND '''
laser_sound= pygame.mixer.Sound('Assets/laser.wav')
explosion_sound = pygame.mixer.Sound('Assets/low_expl.wav')
go_sound = pygame.mixer.Sound('Assets/go.wav')
gameOver_sound = pygame.mixer.Sound('Assets/game_over.wav')
epicSong_sound = pygame.mixer.music.load('Assets/epicsong.mp3')
cyberFunk_sound = pygame.mixer.Sound('Assets/cyberfunk.mp3')
illusoryrealm_sound = pygame.mixer.Sound('Assets/illusoryrealm.mp3')
pygame.mixer.init()


screen = pygame.display.set_mode((0,0),FULLSCREEN)
s_width, s_height = screen.get_size()

clock = pygame.time.Clock()
FPS = 60

background_group = pygame.sprite.Group()
Player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
ufo_group = pygame.sprite.Group()
pbullet_group = pygame.sprite.Group()
enemyBullet_group = pygame.sprite.Group()
ufoBullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
partical_group = pygame.sprite.Group()


sprite_group = pygame.sprite.Group()

pygame.display.set_caption("Game Danar")

class Background(pygame.sprite.Sprite):
    def __init__(self, x,y):
        super().__init__()

        self.image = pygame.Surface([x,y])
        self.image.fill ('white ')
        self.image.set_colorkey('green')
        self.rect = self.image.get_rect()

    def update (self):
        self.rect.y += 1
        self.rect.x += 1
        if self.rect.y > s_height:
            self.rect.y = random.randrange(-10,0)
            self.rect.x = random.randrange(-400, s_width)

class Partical(Background):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.rect.x = random.randrange(0,s_width)
        self.rect.y = random.randrange(0,s_height)
        self.image.fill('grey')
        self.vel = random.randint(3,8)

    def update(self):
        self.rect.y += self.vel
        if self.rect.y > s_height:
            self.rect.x = random.randrange(0,s_width)
            self.rect.y = random.randrange(0,s_height)

class Image(Partical):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.rect.x = random.randrange(0,s_width)
        self.rect.y = random.randrange(0,s_height)
        self.vel = random.randint(3,8)
    def update(self):
        self.rect.y += self.vel
        if self.rect.y > self.s_height:
            self.rect.x = random.randrange(0,s_width)
            self.rect.y = random.randrange(0,s_height)

        
class Player(pygame.sprite.Sprite):
    def __init__(self,img ):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.image.set_colorkey('black')
        self.alive = True
        self.count_to_live = 0
        self.activate_bullet = True
        self.alpha_duration = 0
    def update(self):
        if self.alive:
            self.image.set_alpha(80)
            self.alpha_duration += 1
            if self.alpha_duration > 170:
                self.image.set_alpha (265)

            mouse = pygame.mouse.get_pos()
            self.rect.x = mouse[0]
            self.rect.y = mouse[1]
        else:
            self.alpha_duration = 0
            expl_x = self.rect.x +20
            expl_y = self.rect.y +40
            explosion = Explosion(expl_x,expl_y)
            explosion_group.add(explosion)
            sprite_group.add(explosion)
            pygame.time.delay(22)
            self.rect.y = s_height + 200
            self.count_to_live += 1
            if self.count_to_live >100:
                self.alive  = True
                self.count_to_live = 0
                self.activate_bullet= True

    
    def shoot(self):
        if self.activate_bullet:
            pygame.mixer.Sound.play(laser_sound)
            bullet = playerBullet(player_bullet)
            mouse = pygame.mouse.get_pos()
            bullet.rect.x = mouse[0]
            bullet.rect.x = self.rect.x +21
            bullet.rect.y = mouse[1]
            bullet.rect.y = self.rect.y -20
            pbullet_group.add(bullet)
            sprite_group.add(bullet)
            
    
    def dead(self):
        self.alive = False
        self.activate_bullet = False
        

class Enemy(Player):
    def __init__ (self, img):
        super().__init__(img)
        self.rect.x = random.randrange(80,s_width-80)
        self.rect.y = random.randrange (-500,0)
        screen.blit(self.image,(self.rect.x,self.rect.y))
    
    def update(self):
        self.rect.y += 1
        if self.rect.y > s_height:
            self.rect.x = random.randrange(80,s_width-80)
            self.rect.y = random.randrange(-2000,0)
        self.shoot()
        
    def shoot(self):
        if self.rect.y in (0, 300, 700):
            enemybullet = enemyBullet(enemy_bullet)
            enemybullet.rect.x = self.rect.x +15
            enemybullet.rect.y = self.rect.y +50
            enemyBullet_group.add(enemybullet)
            sprite_group.add(enemybullet)

class ufo(Enemy):
    def __init__ (self,img):
        super().__init__(img)
        self.rect.x = -200
        self.rect.y = 200
        self.move = 1
    
    def update(self):
        self.rect.x += self.move
        if self.rect.x > s_width + 200:
            self.move *= -1
        elif self.rect.x < -200:
            self.move *= -1
        self.shoot()

    def shoot(self):
            if self.rect.x % 50 == 0 :
                ufobullet = ufoBullet(ufo_bullet)
                ufobullet.rect.x = self.rect.x +50
                ufobullet.rect.y = self.rect.y +110
                ufoBullet_group.add(ufobullet)
                sprite_group.add(ufobullet)


class playerBullet(pygame.sprite.Sprite):
    def __init__ (self,img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.image.set_colorkey('black')
    
    def update(self):
        self.rect.y -=  10
        if self.rect.y < 0:
            self.kill()

class enemyBullet(playerBullet):
    def __init__ (self,img):
        super().__init__(img)
        self.image.set_colorkey('white')

    def update(self):
        self.rect.y += 3
        if self.rect.y > s_height:
            self.kill()

class ufoBullet(enemyBullet):
    def __init__ (self,img):
        super().__init__(img)
        self.image.set_colorkey('white')

    def update(self):
        self.rect.y += 2
        if self.rect.y > s_height:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.img_list = []
        for i in range(1,6):
            img = pygame.image.load(f'Assets/exp{i}.png').convert()
            img.set_colorkey('black')
            img = pygame.transform.scale(img, (120,120))
            self.img_list.append(img)
        self.index = 0
        self.image = self.img_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.count_delay = 0
    
    def update(self):
        self.count_delay += 1
        if self.count_delay >= 12:
            if self.index < len(self.img_list)-1:
                self.count_delay = 0
                self.index += 1
                self.image = self.img_list[self.index]
        if self.index >= len(self.img_list)-1:
            if self.count_delay >= 12:
                self.kill()

class Game():
    def __init__(self):
        self.count_hit = 0
        self.count_hit2 = 0
        self.count_hit3 = 0
        self.lives = 3
        self.score = 0
        self.init_create = True
        self.illusoryrealm_sound_delay = 0
        self.start_screen()
        

    def create_background(self):
        for i in range(20):
            x = random.randint(1,6)
            background_image = Background(x,x)
            background_image.rect.x = random.randrange(0, s_width)
            background_image.rect.y = random.randrange(0, s_height)
            background_group.add(background_image)
            sprite_group.add(background_image)
    def start_background(self):
            bg_screen = pygame.image.load(start_background)
            width = 1350
            height = 730
            image_width=pygame.transform.scale(bg_screen,(width, height))
            image_rect = image_width.get_rect()
            image_rect.center = (s_width//2, s_height//2)
            screen.blit(image_width, image_rect)
    
    def create_partical(self):
        for i in range(100):
            x = 1
            y = random.randint(1,7)
            partical = Partical(x,y)
            partical_group.add(partical)
            sprite_group.add(partical)
    


    def create_player(self):
        self.player = Player(player_ship)
        Player_group.add(self.player)
        sprite_group.add(self.player)

    def create_enemy(self):
        for i in range(10):
            self.enemy = Enemy(enemy_ship)
            enemy_group.add(self.enemy)
            sprite_group.add(self.enemy)
    
    def create_ufo(self):
        for i in range(1):
            self.ufo = ufo(ufo_ship)
            ufo_group.add(self.ufo)
            sprite_group.add(self.ufo)

    def playerBullet_hits_enemy(self):
        hits = pygame.sprite.groupcollide(enemy_group, pbullet_group, False, True)
        for i in hits:
            self.count_hit += 1
            if self.count_hit == 3:
                pygame.mixer.Sound.play(explosion_sound)
                self.score +=10
                expl_x = i.rect.x +20
                expl_y = i.rect.y +40
                explosion = Explosion(expl_x, expl_y)
                explosion_group.add(explosion)
                sprite_group.add(explosion)
                i.rect.x = random.randrange(0, s_width)
                i.rect.y = random.randrange(-3000 , 100)
                self.count_hit = 0

    
    def playerBullet_hits_ufo(self):
        hits = pygame.sprite.groupcollide(ufo_group, pbullet_group, False, True)
        for i in hits:
            self.count_hit2 += 1
            if self.count_hit2 == 20:
                pygame.mixer.Sound.play(explosion_sound)
                self.score += 20
                expl_x = i.rect.x +50
                expl_y = i.rect.y +60
                explosion = Explosion(expl_x, expl_y)
                explosion_group.add(explosion)
                sprite_group.add(explosion)
                i.rect.x = -199
                self.count_hit2 = 0
    
    def enemyBullet_hits_player(self):
        if self.player.image.get_alpha() ==255:
            hits = pygame.sprite.spritecollide(self.player,enemyBullet_group,True)
            if hits:
                self.lives -= 1
                pygame.mixer.Sound.play(explosion_sound)
                self.player.dead()
                if self.lives < 0 :
                    self.gameOver_screen ()
    
    def ufoBullet_hits_player(self):
        if self.player.image.get_alpha() == 255:
            hits = pygame.sprite.spritecollide(self.player,ufoBullet_group,True)
            if hits:
                self.lives -= 1
                pygame.mixer.Sound.play(explosion_sound)
                self.player.dead()
                if self.lives < 0:
                    self.gameOver_screen()

    def player_enemy_crash(self):
        if self.player.image.get_alpha() == 255:
            hits = pygame.sprite.spritecollide(self.player, enemy_group, False)
            if hits:
                for i in hits:
                    i.rect.x = random.randrange(0, s_width)
                    i.rect.y =random.randrange(-3000,100)
                    self.lives -= 1
                    pygame.mixer.Sound.play(explosion_sound)
                    self.player.dead()
                    if self.lives < 0 :
                       self.gameOver_screen()

    def player_ufo_crash(self):
        if self.player.image.get_alpha() == 255:
            hits = pygame.sprite.spritecollide(self.player, ufo_group, False)
            if hits:
                for i in hits:
                        self.lives -=2
                        self.player.dead()
                        i.rect.x = -199
                        pygame.mixer.Sound.play(explosion_sound)
                        if self.lives < 0:
                            self.gameOver_screen()

    def create_lives(self):
        self.lives_img = pygame.image.load( live_player)
        self.lives_img = pygame.transform.scale(self.lives_img, (20,23))
        n = 0
        for i in range(self.lives):
            screen.blit(self.lives_img, (0+n,s_height -720))
            n += 60
    
    def create_score(self):
        score = self.score
        font = pygame.font.SysFont('Times New Roman',30)
        text = font.render("Score: "+ str(score),True,'Green')
        text_rect = text.get_rect(center= (s_width-150, s_height-710))
        screen.blit(text,text_rect)
    
    def start_text(self):
        font = pygame.font.SysFont('times new roman bold',200)
        text = font.render('SPACE WAR',True,'blue')
        text_rect = text.get_rect(center=(s_width/2,s_height/2-140))
        screen.blit(text,text_rect)

        font2 = pygame.font.SysFont('times new roman bold',20)
        text2 = font2.render('@DAMAS_Game 2024',True,'white')
        text2_rect = text.get_rect(center=(s_width/2-200,s_height/2+411))
        screen.blit(text2,text2_rect)
        

    def start_screen(self):
        pygame.mixer.Sound.stop(gameOver_sound)
        pygame.mixer.music.stop()
        pygame.mixer.Sound.stop(illusoryrealm_sound)
        pygame.mixer.Sound.play(cyberFunk_sound)
        self.lives = 3
        sprite_group.empty()
        font1 = pygame.font.SysFont('times new roman bold',75)
        surf1 = font1.render('START GAME',True,'White')
        surf_text1 = surf1.get_rect(center=(s_width/2-5,s_height/2+50))
        color1 = (0,0,128,255)
        Button1 = pygame.draw.rect(screen,color1,[460,376,350,60],border_radius = 2,
                         border_top_left_radius=-1,
                         border_top_right_radius=-1,
                         border_bottom_left_radius=-1,
                         border_bottom_right_radius=-1)
        font2 = pygame.font.SysFont('times new roman bold',75)
        surf2 = font2.render('QUIT GAME',True,'White')
        surf_text = surf2.get_rect(center=(s_width/2-10,s_height/2+130))
        color2 = [0,0,128,255]
        Button2 = pygame.draw.rect(screen,color2,[460,460,350,60],border_radius = 2,
                         border_top_left_radius=-1,
                         border_top_right_radius=-1,
                         border_bottom_left_radius=-1,
                         border_bottom_right_radius=-1)
        
        while True:
            self.startScreen_Cursor()
            self.start_background()
            self.start_text()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN: ## PERHATIKAN POSISI DARI BLOK ATAU KOTAKNYA DAN TEKSNYA DIMANA LOKASINYA AGAR NANTI BISA MEMILIH CLICK YANG AKAN  DIPILIH
                    if Button1.collidepoint(event.pos):
                        self.run_game()
                    if Button2.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
            a,b= pygame.mouse.get_pos()
            if Button1.x<= a <= Button1.x +350 and Button1.y <= b <= Button1.y +60:
                pygame.draw.rect(screen,(180,180,180),Button1)
            else:
                pygame.draw.rect(screen,(110,110,110),Button1)
            screen.blit(surf1,surf_text1)
            if Button2.x<= a <= Button2.x +350 and Button2.y<= b <= Button2.y +60:
                pygame.draw.rect(screen,(180,180,180),Button2)
            else:
                pygame.draw.rect(screen,(110,110,110),Button2)
            screen.blit(surf2,surf_text)


                                   
            pygame.display.update()

    def pause_text(self):
        font = pygame.font.SysFont('times new roman bold',100)
        text = font.render('PAUSED',True,'white')
        text_rect = text.get_rect(center=(s_width/2,s_height/2))
        screen.blit(text,text_rect)

        font2 = pygame.font.SysFont('times new roman ',50)
        text2 = font2.render('Click Space To Continue',True,'grey')
        text2_rect = text.get_rect(center=(s_width/2-100,s_height/2+200))
        screen.blit(text2,text2_rect)

    def pause_screen(self):
        self.init_create = False
        while True:
            pygame.mouse.set_visible(False)
            self.pause_text()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_SPACE:
                        self.run_game()
            
            pygame.display.update()

    def gameOver_text(self):
        font = pygame.font.SysFont('times new roman bold',200)
        text = font.render('GAME OVER',True,'red')
        text_rect = text.get_rect(center=(s_width/2,s_height/2))
        screen.blit(text,text_rect)
    
    def gameOver_screen(self):
        pygame.mixer.Sound.play(gameOver_sound)
        pygame.mixer.music.stop()
        pygame.mixer.Sound.stop(illusoryrealm_sound)
        pygame.mixer.Sound.stop(cyberFunk_sound)

        while True:
            screen.fill('black')
            self.gameoverScreen_Cursor()
            self.gameOver_text()
            font = pygame.font.SysFont('times new roman bold',75)
            text = font.render("CLICK BACK TO MENU",True,'blue')
            text_rect = text.get_rect(center=[s_width/2,s_height/2+185])
            self.illusoryrealm_sound_delay += 1
            if self.illusoryrealm_sound_delay >  500:
                pygame.mixer.Sound.play(illusoryrealm_sound)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN :
                    if text_rect.collidepoint(event.pos):
                        self.start_screen()
                        pygame.mixer.Sound.play(cyberFunk_sound)
                    
            a,b = pygame.mouse.get_pos()
            if text_rect.x <= a <= text_rect.x and text_rect.y <= b <= text_rect:
                pygame.draw.rect(screen,[180,180,180],text_rect)
            if text_rect.x >=a >=text_rect.x and text_rect.y >=b >=text_rect.y:
                pygame.draw.rect(screen,[110,110,110],text_rect)
            screen.blit(text,text_rect)

            pygame.display.update()

    def startScreen_Cursor(self):
        pygame.mouse.set_visible(True)
        convert_image = pygame.image.load(pointer_mouse_blue).convert_alpha()
        scale_cursor= pygame.transform.scale(convert_image, (35,35))
        cursor_image = pygame.cursors.Cursor((0,0),scale_cursor)
        pygame.mouse.set_cursor(cursor_image)



    
    def gameoverScreen_Cursor(self):
        pygame.mouse.set_visible(True)
        convert_image2 = pygame.image.load(pointer_mouse_red).convert_alpha()
        scale_cursor2= pygame.transform.scale(convert_image2, (35,35))
        cursor_image2 = pygame.cursors.Cursor((0,0),scale_cursor2)
        pygame.mouse.set_cursor(cursor_image2)

    # def astro(self):
    #         image = pygame.image.load(astro_startscreen)
    #         image.fill('white')
    #         image.set_colorkey('black')
    #         screen.blit(image,(500,500))


        
    def run_update(self):
        sprite_group.draw(screen)
        sprite_group.update()

    def run_game(self):
        pygame.mouse.set_visible(False)
        pygame.mixer.Sound.stop(gameOver_sound)
        pygame.mixer.Sound.play(go_sound)
        pygame.mixer.Sound.stop(cyberFunk_sound)
        pygame.mixer.music.play(-1)
        pygame.mixer.Sound.stop(illusoryrealm_sound)
        if self.init_create:
            self.create_background()
            self.create_partical()
            self.create_player()
            self.create_enemy()
            self.create_ufo()
        while True:
            screen.fill('black')
            self.playerBullet_hits_enemy()
            self.playerBullet_hits_ufo()
            self.enemyBullet_hits_player()
            self.ufoBullet_hits_player()
            self.player_enemy_crash()
            self.player_ufo_crash()
            self.run_update()
            pygame.draw.rect(screen, 'black',(0,0,s_width,30))
            self.create_score()
            self.create_lives()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit() 
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.player.shoot()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                    if event.key == K_SPACE:
                        self.pause_screen()
                
                
            pygame.display.update()
            clock.tick(FPS)
    
def main():
    game = Game()

if __name__ == '__main__':
    main()


 

