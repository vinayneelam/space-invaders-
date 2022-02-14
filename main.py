import pygame
import random
import math

#initze
pygame.init()
#screen
screen=pygame.display.set_mode((800,600))#w,h
#title and icon
pygame.display.set_caption("space invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)
#background
background=pygame.image.load("background.jpg")
#player
plyimg=pygame.image.load("ship.png")
playerX=360
px_change=0
playerY=480
py_change=0
#enemy
#we create a list to get multiple enemies
eneimg=[]
eneX=[]
eneY=[]
ex_change=[]
ey_change=[]
num=6
for i in range(num):
    eneimg.append(pygame.image.load("alien.png"))
    eneX.append(random.randint(0,735))
    ex_change.append(0.5)
    eneY.append(random.randint(50,150))
    ey_change.append(40)
#bullet
#ready bullet cant be seen
#fire bullet is fired
bulimg=pygame.image.load("bullet.png")
bulX=0
bulY=480
by_change=6
b_state="ready"

#score
score=0
font = pygame.font.Font("freesansbold.ttf",32)
tX=10
tY=10
#game over txt
over_font = pygame.font.Font("freesansbold.ttf",64)

def show_score(x,y):
    sc = font.render("score :"+str(score),True,(255,255,255))#first render then blit
    screen.blit(sc,(x,y))
def g_o():
    go = over_font.render("GAME OVER" ,True, (255, 255, 255))  # first render then blit
    screen.blit(go, (200,250))

#display the player
def player(x,y):
    screen.blit(plyimg,(x,y))
#display the enemy
def enemy(x,y,i):
    screen.blit(eneimg[i],(x,y))
#display of bullet
def fire_b(x,y):
    global b_state
    b_state="fire"
    screen.blit(bulimg,(x+16,y+10))#to place the bullet at the center top of spaceship

#collision of bullet and enemy
def iscosn(eneX,eneY,bulX,bulY):
    dist = math.sqrt(math.pow(eneX-bulX,2)+math.pow(eneY-bulY,2))
    if dist<27:
        return True
    else:
        return False

#game loop
running = True
while running:
    # colour on screen RGB
    screen.fill((55, 56, 67))
    #background image
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        #keystroke pressed or not, left or right creating movements
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                px_change = -2
            if event.key == pygame.K_RIGHT:
                px_change = 2
            if event.key == pygame.K_SPACE:
                if b_state == "ready":
                    bulX=playerX
                    fire_b(bulX,bulY)#to fire only one bullet at a time
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                px_change=0
    #apply the movement change
    playerX+=px_change
    #creating the boundaries player
    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736
    #enemy movement
    for i in range(num):
        #game over
        if eneY[i] > 330:
            for j in range(num):
                eneY[j] = 2000
            g_o()
            break
        eneX[i] += ex_change[i]
    #enemy boundaries
        if eneX[i]<=0:
            ex_change[i]=1
            eneY[i]+=ey_change[i]
        elif eneX[i]>=736:
            ex_change[i]=-1
            eneY[i]+=ey_change[i]
        #collision
        colision = iscosn(eneX[i], eneY[i], bulX, bulY)
        if colision:
            bulY = 480
            b_state = "ready"
            score += 1
            eneX[i] = random.randint(0, 735)
            eneY[i] = random.randint(50, 150)
        enemy(eneX[i], eneY[i], i)


    #bullet movement
    if bulY<=0:
        bulY=480
        b_state="ready"#resets bullet movement to start position
    if b_state == "fire":
        fire_b(playerX,bulY)
        bulY-=by_change

    player(playerX,playerY)
    show_score(tX,tY)
    pygame.display.update()#update every time new feature is given.
