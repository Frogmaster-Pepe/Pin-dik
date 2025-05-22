import pygame
import sys

pygame.init()

class Player1(pygame.sprite.Sprite):
    def __init__(self): 
        super().__init__() 
        self.original_image = pygame.image.load("pl1.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (50,50))
        self.rect = self.original_image.get_rect(midbottom = (100, 0.5*w_height))
        self.image = self.original_image
        
        
    
    def player_input(self): 
        dx = 0
        dy = 0
        angle = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            dy -= 5
        if keys[pygame.K_s]:
            dy += 5
        if keys[pygame.K_a]:
            dx -= 5
        if keys[pygame.K_d]:
            dx += 5
        self.rect.x += dx
        self.rect.y += dy

        if dx != 0 or dy != 0:
            if dx > 0 and dy == 0: angle = 0
            elif dx < 0 and dy == 0: angle = 180
            elif dy < 0 and dx == 0: angle = -90
            elif dy > 0 and dx == 0: angle = 90
            elif dx > 0 and dy < 0: angle = -45
            elif dx < 0 and dy < 0: angle = -135
            elif dx > 0 and dy > 0: angle = 45
            elif dx < 0 and dy > 0: angle = 135
            

        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.rect.x = max(0, min(w_width - 50, self.rect.x))
        self.rect.y = max(0, min(w_height - 50, self.rect.y))

    def update(self):
        self.player_input()

class Player2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  
        self.original_image = pygame.image.load("pl2.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (50,50))
        self.rect = self.original_image.get_rect(midbottom = (1200, 0.5*w_height))
        self.image = self.original_image
        
        
    
    def player_input(self): 
        dx = 0
        dy = 0
        angle = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            dy -= 5
        if keys[pygame.K_DOWN]:
            dy += 5
        if keys[pygame.K_LEFT]:
            dx -= 5
        if keys[pygame.K_RIGHT]:
            dx += 5
        self.rect.x += dx
        self.rect.y += dy

        if dx != 0 or dy != 0:
            if dx > 0 and dy == 0: angle = 180
            elif dx < 0 and dy == 0: angle = 0
            elif dy < 0 and dx == 0: angle = 90
            elif dy > 0 and dx == 0: angle = -90
            elif dx > 0 and dy < 0: angle = 135
            elif dx < 0 and dy < 0: angle = 45
            elif dx > 0 and dy > 0: angle = -135
            elif dx < 0 and dy > 0: angle = -45
            

        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.rect.x = max(0, min(w_width - 50, self.rect.x))
        self.rect.y = max(0, min(w_height - 50, self.rect.y))

    def update(self):
        self.player_input()

w_width, w_height = 1300, 700
screen = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption("Brambor")
clock = pygame.time.Clock()

background = pygame.Surface((w_width,w_height))
background.fill("darkgreen")

player = pygame.sprite.Group() 
player.add(Player1(),Player2())

game_active = True
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            exit() 

    if game_active:
        screen.blit(background, (0,0))

        player.draw(screen)
        player.update()

    else:  
        screen.blit(background,(0,0))

    pygame.display.update()
    clock.tick(60)