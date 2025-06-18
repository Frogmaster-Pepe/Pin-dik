import pygame
import sys
import math
import random
import time

pygame.init()
w_width, w_height = 1300, 700

class Diamond(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("diamond.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=(w_width//2, w_height//2))

class Player1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img_idle = pygame.transform.scale(pygame.image.load("pl1.png"), (50, 50))
        self.image = self.img_idle
        self.rect = self.image.get_rect(midbottom=(0.48*w_width, 0.5*w_height))
        self.angle = 0
        self.last_shot = 0

    def player_input(self):
        dx = dy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: dy -= 5
        if keys[pygame.K_s]: dy += 5
        if keys[pygame.K_a]: dx -= 5
        if keys[pygame.K_d]: dx += 5
        moving = dx != 0 or dy != 0
        if moving:
            self.angle = math.degrees(math.atan2(-dy, -dx))
        else:
            self.image = self.img_idle
        self.rect.move_ip(dx, dy)
        # Wrap edges
        self.rect.x %= w_width
        self.rect.y %= w_height

    def update(self):
        self.player_input()

    def can_shoot(self):
        now = time.time()
        if now - self.last_shot >= 0.75:
            self.last_shot = now
            return True
        return False

class Player2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img_idle = pygame.transform.scale(pygame.image.load("pl2.png"), (50, 50))
        self.image = self.img_idle
        self.rect = self.image.get_rect(midbottom=(0.52*w_width, 0.5*w_height))
        self.angle = 0
        self.last_shot = 0

    def player_input(self):
        dx = dy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]: dy -= 5
        if keys[pygame.K_DOWN]: dy += 5
        if keys[pygame.K_LEFT]: dx -= 5
        if keys[pygame.K_RIGHT]: dx += 5
        moving = dx != 0 or dy != 0
        if moving:
            self.angle = math.degrees(math.atan2(-dy, -dx))
        else:
            self.image = self.img_idle
        self.rect.move_ip(dx, dy)
        self.rect.x %= w_width
        self.rect.y %= w_height

    def update(self):
        self.player_input()

    def can_shoot(self):
        now = time.time()
        if now - self.last_shot >= 0.75:
            self.last_shot = now
            return True
        return False

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, angle, vel, img, size):
        super().__init__()
        base = pygame.transform.scale(pygame.image.load(img), size)
        self.image = pygame.transform.rotate(base, -angle)
        self.rect = self.image.get_rect(center=pos)
        rad = math.radians(angle)
        self.vel = pygame.math.Vector2(-math.cos(rad), -math.sin(rad)) * vel

    def update(self):
        self.rect.move_ip(self.vel)
        if not screen.get_rect().colliderect(self.rect):
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, dir, speed):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("enemy.png"), (50, 50))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.spawn = dir
        self.reset_position()

    def reset_position(self):
        if self.spawn == "top":
            self.rect.center = (random.randint(50, w_width - 50), 50)
        elif self.spawn == "bottom":
            self.rect.center = (random.randint(50, w_width - 50), w_height - 50)
        elif self.spawn == "left":
            self.rect.center = (50, random.randint(50, (w_height - 50)))
        elif self.spawn == "right":
            self.rect.center = (w_width - 50 , random.randint(50, w_height - 50))

    def update(self):
        target = pygame.math.Vector2(w_width//2, w_height//2)
        pos = pygame.math.Vector2(self.rect.center)
        dir = (target - pos).normalize()
        self.rect.move_ip(dir * self.speed)

class Boss(pygame.sprite.Sprite):
    def __init__(self, direc, speeed):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("boss.png"), (100, 100))
        self.rect = self.image.get_rect()
        self.speeed = speeed
        self.spaawn = direc
        self.reset_position()

    def reset_position(self):
        if self.spaawn == "left":
            self.rect.center = (100, random.randint(100, (w_height - 100)))
        elif self.spaawn == "right":
            self.rect.center = (w_width - 100 , random.randint(100, w_height - 100))

    def update(self):
        target = pygame.math.Vector2(w_width//2, w_height//2)
        pos = pygame.math.Vector2(self.rect.center)
        direc = (target - pos).normalize()
        self.rect.move_ip(direc * self.speeed)

screen = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption("Defend the crystal")
clock = pygame.time.Clock()
bg = pygame.transform.scale(pygame.image.load("background.png"), (w_width, w_height))
sg = pygame.transform.scale(pygame.image.load("startground.png"), (w_width, w_height))
eg = pygame.transform.scale(pygame.image.load("endground.png"), (w_width, w_height))
diamond_over = pygame.image.load("diamond_over.png")
over = pygame.transform.scale(pygame.image.load("diamond_over.png"),(100,100))

font = pygame.font.SysFont(None, 40)
font_small = pygame.font.SysFont(None, 30)

player1 = Player1()
player2 = Player2()
players = pygame.sprite.Group(player1, player2)
p1shots = pygame.sprite.Group()
p2shots = pygame.sprite.Group()
enemies = pygame.sprite.Group()
diamond = Diamond()
diamond_group = pygame.sprite.Group(diamond)
boss = pygame.sprite.Group()
projectile = pygame.sprite.Group()

wave = 0
wave_pending = False
wave_timer = 0
respawn = {}
game_active = False
show_intro = True
score = 0
enemy_baseSpeed = 3.0
boss_baseSpeed = 2.0
colision_conter = 0

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.KEYDOWN:
            if show_intro:
                show_intro = False
                game_active = True
            elif not game_active and e.key == pygame.K_SPACE:
                boss.empty()
                enemies.empty()
                p1shots.empty()
                p2shots.empty()
                players.empty()
                player1.rect.midbottom = (0.48*w_width, 0.5*w_height)
                player2.rect.midbottom = (0.52*w_width, 0.5*w_height)
                players.add(player1, player2)
                wave = 0
                score = 0
                colision_conter = 0
                respawn.clear()
                wave_pending = False
                game_active = True
            elif game_active:
                if e.key == pygame.K_f and player1 in players and player1.can_shoot():
                    p1shots.add(Projectile(player1.rect.center, player1.angle, 25, "bluesword.png", (50,15)))
                if e.key == pygame.K_RCTRL and player2 in players and player2.can_shoot():
                    p2shots.add(Projectile(player2.rect.center, player2.angle, 25, "redsword.png", (50,15)))

    if show_intro:
        screen.blit(sg, (0,0))
        text = ["Welcome to Defend the crystal",
                "P1: Move=WASD, Shoot=F",
                "P2: Move=Arrows, Shoot=Right Ctrl",
                "Protect the diamond in the center.",
                "If you die you respawn in five seconds",
                "Stop waves of enemies.",
                "Protect the crystal at all cost",
                "",
                "Press any key to start."]
        for i,t in enumerate(text):
            txt = font_small.render(t, True, (255,255,255))
            screen.blit(txt, (w_width//2 - txt.get_width()//2, 180 + i*40))

    elif game_active:
        screen.blit(bg, (0,0))

        if not wave_pending and not enemies:
            wave += 1
            colision_conter = 0 
            wave_pending = True
            wave_timer = time.time()
            for _ in range(5 + wave*2):
                dir = random.choice(["top","bottom","left","right"])
                enemies.add(Enemy(dir, enemy_baseSpeed + wave*0.1))
            if ((wave)//5):
                for i in range(1):
                    direc = random.choice(["left","right"])
                    boss.add(Boss(direc, boss_baseSpeed + wave*0.5))
            elif ((wave)//10):
                for i in range(1):
                    direc = random.choice(["left","right"])
                    boss.add(Boss(direc, boss_baseSpeed + wave*0.5))        
        if wave_pending and time.time()-wave_timer > 2:
            wave_pending = False

        players.update()
        p1shots.update()
        p2shots.update()
        enemies.update()
        boss.update()

        screen.blit(bg, (0,0))
        diamond_group.draw(screen)
        players.draw(screen)
        p1shots.draw(screen)
        p2shots.draw(screen)
        enemies.draw(screen)
        boss.draw(screen)

        if wave_pending:
            wmsg = font.render(f"Wave {wave} incoming!", True, (255,255,0))
            screen.blit(wmsg, (w_width//2 - wmsg.get_width()//2, 50))

        now = time.time()
        for i,p in enumerate([player1,player2], start=1):
            if p in players and pygame.sprite.spritecollideany(p, enemies):
                players.remove(p)
                respawn[f"p{i}"] = now
            if f"p{i}" in respawn and now-respawn[f"p{i}"] > 5:
                players.add(p)
                del respawn[f"p{i}"]

        for shot in p1shots:
            if pygame.sprite.spritecollide(shot, enemies, True):
                shot.kill()
                score += 1
        for shot in p2shots:
            if pygame.sprite.spritecollide(shot, enemies, True):
                shot.kill()
                score += 1         

        for shot  in p1shots:
            if  pygame.sprite.spritecollide(shot, boss, False) :
                colision_conter = colision_conter + 1
                shot.kill()
                if colision_conter >= 5:
                    score += 10
                    colision_couter = 0
                    for b in boss:
                        b.kill()  
        for shot  in p2shots:
            if  pygame.sprite.spritecollide(shot, boss, False) :
                colision_conter = colision_conter + 1
                shot.kill()
                if colision_conter >= 5:
                    score += 10
                    colision_conter = 0 
                    for b in boss:
                        b.kill()  
                                  

        if pygame.sprite.groupcollide(enemies, diamond_group, False, False):
            game_active = False

        scr = font.render(f"Score: {score}", True, (255,255,255))
        screen.blit(scr, (0,0))

    else:
        screen.blit(eg, (0,0))
        go = font.render("Game Over!", True, (255,0,0))
        ri = font.render("Press SPACE to Restart", True, (255,255,255))
        screen.blit(scr, (w_width//2 - scr.get_width()//2, w_height//2 - 150))
        screen.blit(go, (w_width//2 - go.get_width()//2, w_height//2 - 200))
        screen.blit(ri, (w_width//2 - ri.get_width()//2, w_height//2 - 100))
        screen.blit(over, over.get_rect(center =(w_width // 2, w_height // 2 )))

    pygame.display.update()
    clock.tick(60)
