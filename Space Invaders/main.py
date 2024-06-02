import pgzrun
import random

WIDTH = 1200
HEIGHT = 600

white = (255,255,255)
blue = (0,0,255)

bullets = []
enemies = []
score = 0
speed = 5
direction = 1

player = Actor("galaga")
player.pos = (WIDTH//2,HEIGHT-60)
player.dead = False
player.countdown = 90

bug_enemy = Actor("bug")
for row in range(8):
    for col in range(4):
        enemies.append(Actor("bug"))
        enemies[-1].x = 100+50*row
        enemies[-1].y = 80+50*col

def display_score():
    screen.draw.text(str(score), (50,50), color=white)

def on_key_down(key):
    if key == keys.SPACE:
        bullets.append(Actor("bullet"))
        bullets[-1].x = player.x
        bullets[-1].y = player.y - 20
    
def update():
    global score, direction, speed
    move_down = False
    if player.dead == False:
        if keyboard.left:
            player.x -= speed
            if player.x <= 0:
                player.x = 0
        elif keyboard.right:
            player.x += speed
            if player.x >= WIDTH:
                player.x = WIDTH
    
    #firing bullet - making it move
    if keyboard.space:
        bullets.append(Actor("bullet"))
        bullets[-1].x = player.x
        bullets[-1].y = player.y - 20
    for bullet in bullets:
        if bullet.y <= 0:
            bullets.remove(bullet)
        else: 
            bullet.y -= 7

    if len(enemies) > 0 and (enemies[-1].x >= WIDTH-80 or enemies[0].x <= 80):
        move_down = True
        direction = direction * -1
    
    if len(enemies) == 0:
        game_over()

    for enemy in enemies:
        enemy.x += 5*direction
        if move_down:
            enemy.y += speed

        if enemy.y > HEIGHT:
            enemies.remove(enemy)
        
        for bullet in bullets:
            if enemy.colliderect(bullet):
                score += 10
                bullets.remove(bullet)
                enemies.remove(enemy)
                if len(enemies) == 0:
                    game_over()
        
        if player.colliderect(enemy):
            player.dead = True
    
    if player.dead:
        player.countdown -= 1
    
    if player.countdown == 0:
        player.dead = False
        player.countdown = 90

def draw():
    screen.clear()
    screen.fill((24, 38, 71))
    if player.dead == False:
        player.draw()

    for enemy in enemies:
        enemy.draw()
    
    for bullet in bullets:
        bullet.draw()
    
    display_score()

    if len(enemies) == 0:
        game_over()

def game_over():
    screen.draw.text("Game Over! Try again.", (50,50), color=white, fontsize=64)

pgzrun.go()