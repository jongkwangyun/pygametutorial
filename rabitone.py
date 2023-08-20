# 1. 파이게임 모듈을 불러온다.
import pygame
import math
import random

# 2. 초기화 시킨다.
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
acc = [0,0]
arrows = []
badtimer = 100
badtimer1 = 0
badguys = [[640,100]]
healthvalue = 194

# 3. 이미지를 가져온다.
player = pygame.image.load("resources/images/dude.png")
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
arrow = pygame.image.load("resources/images/bullet.png")
badguyimg = pygame.image.load("resources/images/badguy.png")
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")

keys = [False, False, False, False]
playpos = [100,100]

# 4. 계속 화면이 보이도록 한다.

running = 1
exitcode = 0

while running:
  badtimer-=1
  # 5. 화면을 깨끗하게 한다.
  screen.fill((0,0,0))  # (R,G,B)

  # 6. 모든 요소들을 다시 그린다.
  for x in range(width//grass.get_width()+1):
    for y in range(height//grass.get_height()+1):
      screen.blit(grass, (x*100,y*100))

  screen.blit(castle, (0, 30))
  screen.blit(castle, (0, 135))
  screen.blit(castle, (0, 240))
  screen.blit(castle, (0, 345))

  # 6.1 - Set player position and rotation
  position = pygame.mouse.get_pos()
  angle = math.atan2(position[1]-(playpos[1]+32), position[0]-(playpos[0]+26))
  playerrot = pygame.transform.rotate(player, 360-angle*57.29)
  playerpos1 = (playpos[0]-playerrot.get_rect().width//2, playpos[1]-playerrot.get_rect().height//2)
  screen.blit(playerrot, playerpos1)

  # 6.2 - Draw arrows
  for bullet in arrows:  # bullet <== [각도, 플레이어의 x좌표, 플레이어의 y좌표]
    index=0
    velx=math.cos(bullet[0])*10
    vely=math.sin(bullet[0])*10
    bullet[1]+=velx
    bullet[2]+=vely
    if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
      arrows.pop(index)
    index+=1

    for projectile in arrows:
      arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
      screen.blit(arrow1, (projectile[1], projectile[2]))

  # 6.3 - Draw Badguys
  if badtimer==0:
    badguys.append([640, random.randint(50,430)])
    badtimer=100-(badtimer1*2)
    if badtimer1>=35:
      badtimer1=35
    else:
      badtimer1+=5

  index=0
  for badguy in badguys:
    if badguy[0]<-64:
      badguys.pop(index)
    else:
      badguy[0]-=3

    # 6.3.1 - Attack castle
    badrect=pygame.Rect(badguyimg.get_rect())
    badrect.top=badguy[1]
    badrect.left=badguy[0]
    if badrect.left<64:
      healthvalue -= random.randint(5,20)
      badguys.pop(index)

    # 6.3.2 - Check for collisions
    index1=0
    for bullet in arrows:
      bullrect=pygame.Rect(arrow.get_rect())
      bullrect.left=bullet[1]
      bullrect.top=bullet[2]
      if badrect.colliderect(bullrect):
        acc[0]+=1
        badguys.pop(index)
        arrows.pop(index1)
      index1+=1

    # 6.3.3 - Next bad guy
      
    index+=1
  for badguy in badguys:
    screen.blit(badguyimg, badguy)
  
  # 6.4 - Draw clock
  font = pygame.font.Font(None, 24)
  survivedtext = font.render(str(int((90000-pygame.time.get_ticks())/60000))+":"\
                             +str(int((90000-pygame.time.get_ticks())/1000%60)).zfill(2), True, (0,0,0))
  textRect = survivedtext.get_rect()
  textRect.topright=[635,5]
  screen.blit(survivedtext, textRect)

  # 6.5 - Draw health bar
  screen.blit(healthbar, (5,5))
  for health1 in range(healthvalue):
    screen.blit(health, (health1+8,8))
  
  # 7. 화면을 다시 그린다.
  pygame.display.flip()

  # 8. 게임을 종료
  for event in pygame.event.get():
    # X 를 눌렀으면,
    if event.type == pygame.QUIT:
      # 게임종료한다
      pygame.quit()
      exit(0)

    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_w:
        keys[0] = True
      elif event.key == pygame.K_a:
        keys[1] = True
      elif event.key == pygame.K_s:
        keys[2] = True
      elif event.key == pygame.K_d:
        keys[3] = True

    if event.type == pygame.KEYUP:
      if event.key == pygame.K_w:
        keys[0] = False
      elif event.key == pygame.K_a:
        keys[1] = False
      elif event.key == pygame.K_s:
        keys[2] = False
      elif event.key == pygame.K_d:
        keys[3] = False

    if event.type == pygame.MOUSEBUTTONDOWN:
      position = pygame.mouse.get_pos()
      acc[1] = acc[1]+1
      arrows.append([math.atan2(position[1]-(playpos[1]+32), position[0]-(playpos[0]+26)), \
                     playerpos1[0]+32, playerpos1[1]+32])

    # 9 - Move player
    if keys[0]:
      playpos[1] = playpos[1] - 5
    elif keys[2]:
      playpos[1] = playpos[1] + 5
    elif keys[1]:
      playpos[0] = playpos[0] - 5
    elif keys[3]:
      playpos[0] = playpos[0] + 5
    
    # 10 - Win/Lose check
    if pygame.time.get_ticks()>90000:
      running=0
      exitcode=1
    if healthvalue<=0:
     running=0
     exitcode=0
    if acc[1]!=0:
      accuracy=round(acc[0]*1.0/acc[1]*100)
    else:
      accuracy=0
  
# 11 = Win/Lose display
if exitcode==0:
  pygame.font.init()
  font = pygame.font.Font(None, 24)
  text = font.render("Accuracy: "+str(accuracy)+"%", True, (255,0,0))
  textRect = text.get_rect()
  textRect.centerx = screen.get_rect().centerx
  textRect.centery = screen.get_rect().centery+24
  screen.blit(gameover, (0,0))
  screen.blit(text, textRect)
else:
  pygame.font.init()
  font = pygame.font.Font(None, 24)
  text = font.render("Accuracy: "+str(accuracy)+"%", True, (255,0,0))
  textRect = text.get_rect()
  textRect.centerx = screen.get_rect().centerx
  textRect.centery = screen.get_rect().centery+24
  screen.blit(youwin, (0,0))
  screen.blit(text, textRect)

while 1:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit(0)
  pygame.display.flip()