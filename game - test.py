import pygame
import sys
import math
import random
import time

pygame.init()
w_width, w_height = 1300, 700

class Player1(pygame.sprite.Sprite):
    def __init__(self): 
        super().__init__() 
        self.original_image = pygame.image.load("pl1.png")
        self.original_image = pygame.transform.scale(self.original_image, (50, 50))
        self.rect = self.original_image.get_rect(midbottom=(0.48 * w_width, 0.5 * w_height))
        self.image = self.original_image    
        self.angle = 0
        self.last_shot_time = 0  

    def player_input(self): 
        dx, dy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: dy -= 5 
        if keys[pygame.K_s]: dy += 5
        if keys[pygame.K_a]: dx -= 5
        if keys[pygame.K_d]: dx += 5
        #if keys == pygame.key.get_pressed():
        
        self.rect.x += dx
        self.rect.y += dy

        
        if dx > 0: 
            self.angle = 0 
            self.image = pygame.transform.flip(self.original_image, False, False) 
        elif dx < 0:
            self.angle = 180  
            self.image = pygame.transform.flip(self.original_image, True, False)  

        
        self.rect = self.image.get_rect(center=self.rect.center)

        
        if self.rect.x <= -50: self.rect.x = w_width
        elif self.rect.x >= w_width: self.rect.x = -50
        if self.rect.y <= -50: self.rect.y = w_height
        elif self.rect.y >= w_height: self.rect.y = -50

    def update(self):
        self.player_input()

    def can_shoot(self):
        """Check if enough time has passed to shoot"""
        current_time = time.time()
        if current_time - self.last_shot_time >= 0.5:  # 0.5 second cooldown
            self.last_shot_time = current_time
            return True
        return False

class Player2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  
        self.original_image = pygame.image.load("pl2.png")
        self.original_image = pygame.transform.scale(self.original_image, (50, 50))
        self.rect = self.original_image.get_rect(midbottom=(0.52 * w_width, 0.5 * w_height))
        self.image = self.original_image
        self.angle = 0
        self.last_shot_time = 0  # Track the last time the player shot

    def player_input(self): 
        dx, dy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]: dy -= 5
        if keys[pygame.K_DOWN]: dy += 5
        if keys[pygame.K_LEFT]: dx -= 5
        if keys[pygame.K_RIGHT]: dx += 5

        # Update player position
        self.rect.x += dx
        self.rect.y += dy

        # Flip the image based on movement
        if dx > 0: 
            self.angle = 0  # Facing left
            self.image = pygame.transform.flip(self.original_image, False, False)  # No flip needed
        elif dx < 0:
            self.angle = 180  # Facing right
            self.image = pygame.transform.flip(self.original_image, True, False)  # Flip horizontally

        # Rotate image based on angle
        self.rect = self.image.get_rect(center=self.rect.center)

        # Screen wrapping
        if self.rect.x <= -50: self.rect.x = w_width
        elif self.rect.x >= w_width: self.rect.x = -50
        if self.rect.y <= -50: self.rect.y = w_height
        elif self.rect.y >= w_height: self.rect.y = -50

    def update(self):
        self.player_input()

    def can_shoot(self):
        current_time = time.time()
        if current_time - self.last_shot_time >= 0.5:  # 0.5 second cooldown
            self.last_shot_time = current_time
            return True
        return False

class Projectile1(pygame.sprite.Sprite):
    def __init__(self, pos, angle, vel):
        super().__init__()
        self.image = pygame.image.load("bluesword.png")
        self.image = pygame.transform.scale(self.image, (20, 20))
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
        self.image = pygame.image.load("redsword.png")
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect(center=pos)

        radians = math.radians(angle)
        self.velocity = pygame.math.Vector2(math.cos(radians), math.sin(radians)) * vel

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        if (self.rect.right < 0 or self.rect.left > w_width or
            self.rect.bottom < 0 or self.rect.top > w_height):
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, spawn_direction):
        super().__init__()
        self.image = pygame.image.load("enemy.png")  
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.speed = 3
        self.spawn_direction = spawn_direction
        self.reset_position()

    def reset_position(self):
        if self.spawn_direction == "top":
            self.rect.center = (random.randint(0, w_width), -50)
        elif self.spawn_direction == "bottom":
            self.rect.center = (random.randint(0, w_width), w_height + 50)
        elif self.spawn_direction == "left":
            self.rect.center = (-50, random.randint(0, w_height))
        elif self.spawn_direction == "right":
            self.rect.center = (w_width + 50, random.randint(0, w_height))

    def update(self):
        if self.spawn_direction == "top" or self.spawn_direction == "bottom":
            self.rect.y += self.speed if self.spawn_direction == "bottom" else -self.speed
        elif self.spawn_direction == "left" or self.spawn_direction == "right":
            self.rect.x += self.speed if self.spawn_direction == "right" else -self.speed

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
enemy_group = pygame.sprite.Group()
bullet_velocity = 15
game_active = True



# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f and player1.can_shoot():
                projectile = Projectile1(player1.rect.center, player1.angle, bullet_velocity)
                projectiles1.add(projectile)
            if event.key == pygame.K_RCTRL and player2.can_shoot():
                projectile = Projectile2(player2.rect.center, player2.angle, bullet_velocity)
                projectiles2.add(projectile)

    if game_active:
        screen.blit(background, (0, 0))

        # Update
        players.update()
        projectiles1.update()
        projectiles2.update()
        spawn_enemies()
        enemy_group.update()

        # Draw
        players.draw(screen)
        projectiles1.draw(screen)
        projectiles2.draw(screen)
        enemy_group.draw(screen)

        # Collision check
        if pygame.sprite.spritecollideany(player1, enemy_group):
            players.remove(player1)
            print("💥 Player 1 has been hit by an enemy!")

        if pygame.sprite.spritecollideany(player2, enemy_group):
            players.remove(player2)
            print("💥 Player 2 has been hit by an enemy!")

        # Projectiles kill enemies
        for projectile in projectiles1:
            pygame.sprite.spritecollide(projectile, enemy_group, True)
        for projectile in projectiles2:
            pygame.sprite.spritecollide(projectile, enemy_group, True)

    else:
        screen.blit(background, (0, 0))

    pygame.display.update()
    clock.tick(60)
