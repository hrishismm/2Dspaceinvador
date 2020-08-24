#Importing pygame module
import pygame
import random
import math
#Music
from pygame import mixer

#Initialize the pygame
pygame.init()

#Creating our screen
screen=pygame.display.set_mode((800,600))

#Background
backgroundimage=pygame.image.load("spacebackground.png")

#Title and Icon
pygame.display.set_caption("Space Invader")
icon=pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

#player Image
playerimage=pygame.image.load("space-invaders.png")
playerX=370
playerY=480
playerX_change=0

#bg music
mixer.music.load('background.wav')
mixer.music.play(-1)

#Enemy Images
enemyImg =[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=6

for i in range(num_of_enemies):
   
    enemyImg.append(pygame.image.load("ufo.png")) 
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(20)

#Bullet Image
bulletImg =pygame.image.load("bullet.png")
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=10
bullet_state="ready"

#Score
score_value=0

#Creating fonts
font=pygame.font.Font('freesansbold.ttf',32)
over_font=pygame.font.Font('freesansbold.ttf',64)

textX=10
textY=10

def show_score(x,y):
    score=font.render("Score:"+str(score_value),True, (255,255,255))
    screen.blit(score,(x,y))

def player(x,y):
    screen.blit(playerimage,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg,(x+16,y+16))

def collision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance<27:
        return True
    else:
        return False

def game_over_text():
    over_text=font.render("Game Over",True, (255,255,255))
    screen.blit(over_text,(325,300))

#Game loop
running=True

"""
Here we create a game loop 
which is true when we run the game
then we iterate the events that happen during the game
and if a quit event occurs then the while condition turns false and
we quit the game
"""

while running:
    #RGB-Red Green Blue
    screen.fill((0,0,0))
    
    #Background Image
    screen.blit(backgroundimage,(0,0))

    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
            pygame.quit()
            #Check keystrokes
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change=-5
                #print("Left arrow is pressed")
            if event.key==pygame.K_RIGHT:
                playerX_change=5
                #print("Right arrow is pressed")
            if event.key==pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound=mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX=playerX
                    fire_bullet(bulletX, bulletY)
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerX_change=0
                #print("Keystroke has been released")
        
    playerX+=playerX_change
    
    #Does not go out of the screen
    if(playerX<=0):
        playerX=0
    elif playerX>=736:
        playerX=736
    
    #Enemy movement
    for i in range(num_of_enemies):
         #Game Over
        if enemyY[i]>440 :
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break
       
        enemyX[i]+=enemyX_change[i]
        
        if(enemyX[i]<=0):
            enemyX_change[i]=4
            enemyY[i]+=enemyY_change[i]
        
        elif enemyX[i]>=736:
            enemyX_change[i]=-4
            enemyY[i]+=enemyY_change[i]
    
         #Collision
        collisionvalue=collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collisionvalue:
            explosion_sound=mixer.Sound('explosion.wav')
            explosion_sound.play()
                    
            bulletY=480
            bullet_state="ready"
            score_value+=1
            enemyX[i]=random.randint(0, 800)
            enemyY[i]=random.randint(50, 150)
        
        enemy(enemyX[i], enemyY[i],i)
    
    #bullet movement
    if bulletY<=0:
        bulletY=480
        bullet_state="ready"
    
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY-=bulletY_change
        
    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()
            
