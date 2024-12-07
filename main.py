#Copyright (c) 2024 Blazeboss
import pygame
from pygame import *
import time as tm
from random import *

pygame.init()
mixer.init()




window = display.set_mode((800, 600))
background = transform.scale(image.load("galaxy.jpg"), (800, 600))
mixer.music.load('space.ogg')
mixer.music.set_volume(0.1)
mixer.music.play()

font.init()
font1 = font.Font(None, 50)
lose = font1.render("You Lose!", True, (255, 0, 0))




clock = pygame.time.Clock()
FPS = 60
game = True
score = 0
missed = 0

show_message = False
message_start_time = 0
game_active = True  
monsters = sprite.Group()
bullets = sprite.Group()

class GameSprite(sprite.Sprite):
    def __init__(self, image_path, x, y, width, height, speed=10, speed2=2):
        super().__init__()
        self.image = transform.scale(image.load(image_path), (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.speed2 = speed2
        self.direction = 1

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def fire(self):

        bullet = Bullet('bullet.png', self.rect.x, self.rect.y, 50, 50)
        bullets.add(bullet)

class Player(GameSprite):
    def update(self, keys):
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 700 - self.rect.width:
            self.rect.x += self.speed


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed2 

        global missed


        if self.rect.y >= 490 :
            missed += 1
            self.rect.y = 0
            self.rect.x = randint(0, 635)
            self.speed2 = randint(1, 5)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()





player = Player("rocket.png", 300, 450, 35, 35)




for i in range(5):
    enemy = Enemy("ufo.png", randint(0, 700), 0, 35, 35)
    monsters.add(enemy)

false = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()


    keys_pressed = key.get_pressed()

    collides = sprite.groupcollide(monsters, bullets, True, True)
    for _ in collides:
            score += 1 
            enemy = Enemy("ufo.png", randint(0, 600),0, 35, 35)
            monsters.add(enemy)

    score_text = font1.render('Score:' + str(score), True, (255, 255, 255))
    missed_text = font1.render('Missed:' + str(missed), True, (255, 255, 255))



    if missed >= 10:
        window.blit(lose, (200, 200))
        false = True

    window.blit(background, (0, 0))
    window.blit(score_text, (10, 10))
    window.blit(missed_text, (0, 50))

    if false == False:

        player.update(keys_pressed)
        monsters.update()
        
        

        player.draw(window)
        monsters.draw(window)
    
        bullets.update()
        bullets.draw(window)

    display.update()
    clock.tick(FPS)

pygame.quit()
