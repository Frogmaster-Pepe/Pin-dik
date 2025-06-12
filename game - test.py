import pygame
import sys
import math

pygame.init()
w_width, w_height = 1600, 900

class Player1(pygame.sprite.Sprite):
    def __init__(self): 
        super().__init__() 
        self.original_image = pygame.image.load("pl1.png")
        self.original_image = pygame.transform.scale(self.original_image, (50, 50))
        self.rect = self.original_image.get_rect(midbottom=(0.05 * w_width, 0.5 * w_height))
        self.image = self.original_image    
        self.angle = 0

    def player_input(self): 
        dx, dy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: dy -= 5
        if keys[pygame.K_s]: dy += 5
        if keys[pygame.K_a]: dx -= 5
        if keys[pygame.K_d]: dx += 5

        self.rect.x += dx
        self.rect.y += dy

        if dx != 0 or dy != 0:
            if dx > 0 and dy == 0: self.angle = 0
            elif dx < 0 and dy == 0: self.angle = 180
            elif dy < 0 and dx == 0: self.angle = -90
            elif dy > 0 and dx == 0: self.angle = 90
            elif dx > 0 and dy < 0: self.angle = -45
            elif dx < 0 and dy < 0: self.angle = -135
            elif dx > 0 and dy > 0: self.angle = 45
            elif dx < 0 and dy > 0: self.angle = 135

        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # screen wrapping
        if self.rect.x <= -50: self.rect.x = w_width
        elif self.rect.x >= w_width: self.rect.x = -50
        if self.rect.y <= -50: self.rect.y = w_height
        elif self.rect.y >= w_height: self.rect.y = -50

    def update(self):
        self.player_input()

class Player2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  
        self.original_image = pygame.image.load("pl2.png")
        self.original_image = pygame.transform.scale(self.original_image, (50, 50))
        self.rect = self.original_image.get_rect(midbottom=((0.95 * w_width, 0.5 * w_height)))
        self.image = self.original_image
        self.angle = 0    

    def player_input(self): 
        dx, dy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]: dy -= 5
        if keys[pygame.K_DOWN]: dy += 5
        if keys[pygame.K_LEFT]: dx -= 5
        if keys[pygame.K_RIGHT]: dx += 5

        self.rect.x += dx
        self.rect.y += dy

        if dx != 0 or dy != 0:
            if dx > 0 and dy == 0: self.angle = 180
            elif dx < 0 and dy == 0: self.angle = 0
            elif dy < 0 and dx == 0: self.angle = 90
            elif dy > 0 and dx == 0: self.angle = -90
            elif dx > 0 and dy < 0: self.angle = 135
            elif dx < 0 and dy < 0: self.angle = 45
            elif dx > 0 and dy > 0: self.angle = -135
            elif dx < 0 and dy > 0: self.angle = -45

        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # screen wrapping
        if self.rect.x <= -50: self.rect.x = w_width
        elif self.rect.x >= w_width: self.rect.x = -50
        if self.rect.y <= -50: self.rect.y = w_height
        elif self.rect.y >= w_height: self.rect.y = -50

    def update(self):
        self.player_input()

class Projectile1(pygame.sprite.Sprite):
    def __init__(self, pos, angle, vel):
        super().__init__()
        self.image = pygame.image.load("bullet.png")
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect(center=pos)

        radians = math.radians(angle)
        self.velocity = pygame.math.Vector2(math.cos(radians), math.sin(radians)) * vel

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        if (self.rect.right < 0 or self.rect.left > w_width or
            self.rect.bottom < 0 or self.rect.top > w_height):
            self.kill()

class Projectile2(pygame.sprite.Sprite):
    def __init__(self, pos, angle, vel):
        super().__init__()
        self.image = pygame.image.load("bullet.png")
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect(center=pos)

        radians = math.radians(angle)
        self.velocity = pygame.math.Vector2(-math.cos(radians), -math.sin(radians)) * vel

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        if (self.rect.right < 0 or self.rect.left > w_width or
            self.rect.bottom < 0 or self.rect.top > w_height):
            self.kill()

# Setup
screen = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption("Brambor")
clock = pygame.time.Clock()
background = pygame.Surface((w_width, w_height))
background.fill("darkgreen")

# Game objects
player1 = Player1()
player2 = Player2()
players = pygame.sprite.Group(player1, player2)
projectiles1 = pygame.sprite.Group()
projectiles2 = pygame.sprite.Group()
bullet_velocity = 15
game_active = True

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                projectile = Projectile1(player1.rect.center, player1.angle, bullet_velocity)
                projectiles1.add(projectile)
            if event.key == pygame.K_RCTRL:
                projectile = Projectile2(player2.rect.center, player2.angle, bullet_velocity)
                projectiles2.add(projectile)

    if game_active:
        screen.blit(background, (0, 0))

        # Update
        players.update()
        projectiles1.update()
        projectiles2.update()

        # Draw
        players.draw(screen)
        projectiles1.draw(screen)
        projectiles2.draw(screen)

        # Collision check
        if player1.alive() and pygame.sprite.spritecollide(player1, projectiles2, True):
            players.remove(player1)
            print("💥 Player 1 has been hit!")

        if player2.alive() and pygame.sprite.spritecollide(player2, projectiles1, True):
            players.remove(player2)
            print("💥 Player 2 has been hit!")

    else:
        screen.blit(background, (0, 0))

    pygame.display.update()
    clock.tick(60)
