# -*- coding:utf-8 -*-
#调用函数库
import math,random
import pygame
from pygame.locals import*

def game():
#变量赋予初值
    directionKey = [False,False,False,False] # 分别控制w，s，a，d
    playerPosition = [100,70]
    pi = math.pi
    bulletTrajectory = []
    bulletSpeed = 10
    monsterHealth = 4
    monsterAttack = 1
    monsterSpeed = 5
    playerHealth = 100
    playerAttack = 1
    playerSpeed = 8
    time = 0
    #monster AI设置
    allMonsters = []
    def monsterCreation(allMonsters,time,monsterAttack,monsterHealth):
        if time >= 500 or len(allMonsters) == 0:
            #（allMonster（health，attack，角度，x，y）
            allMonsters.append([monsterHealth,monsterAttack,0,random.randint(60,570), random.randint(60,400)])
            time = 0
        return allMonsters,time
    def monsterControl(allMonsters,time,playerHealth):
        monsterPointer = 0
        for monster in allMonsters:
            if (monster[3] <= playerPosition[0]  + 20 and monster[3] >= playerPosition[0]  - 20) and (monster[4] <= playerPosition[1]+20 and monster[4] >= playerPosition[1]-20):
                playerHealth -= monster[1]
                allMonsters.pop(monsterPointer)
            else:
                if monster[3] <= 610 and monster[3] >= 30 and monster[4] <= 450 and monster[4] >= 30:
                    if time%29 == 0:
                        monster[2] = math.atan2(random.uniform(-5,5),random.uniform(-5,5))
                        allMonsters[monsterPointer][2] = monster[2]
                        monsterRotate = pygame.transform.rotate(monsterPicture, (360-monster[2]*180//pi))
                        monster[3] += monsterSpeed*math.cos(monster[2])
                        monster[4] += monsterSpeed*math.sin(monster[2])
                        allMonsters[monsterPointer][3] = monster[3]
                        allMonsters[monsterPointer][4] = monster[4]
                        screen.blit(monsterRotate, (monster[3], monster[4]))
                    else:
                        monsterRotate = pygame.transform.rotate(monsterPicture, (360-monster[2]*180//pi))
                        x =monster[3] + monsterSpeed*math.cos(monster[2])
                        y =monster[4] + monsterSpeed*math.sin(monster[2])
                        allMonsters[monsterPointer][3] = x
                        allMonsters[monsterPointer][4] = y
                        screen.blit(monsterRotate, (x, y))
                elif monster[3] > 610:
                    monsterRotate = pygame.transform.rotate(monsterPicture, (360-monster[2]*180//pi))
                    x =monster[3] - abs(monsterSpeed*math.cos(monster[2]))
                    allMonsters[monsterPointer][3] = x
                    screen.blit(monsterRotate, (x, monster[4]))
                elif monster[4] > 450:
                    monsterRotate = pygame.transform.rotate(monsterPicture, (360-monster[2]*180//pi))
                    y =monster[4] - abs(monsterSpeed*math.sin(monster[2]))
                    allMonsters[monsterPointer][4] = y
                    screen.blit(monsterRotate, (monster[3], y))
                elif monster[3] < 30:
                    monsterRotate = pygame.transform.rotate(monsterPicture, (360-monster[2]*180//pi))
                    x =monster[3] + abs(monsterSpeed*math.cos(monster[2]))
                    allMonsters[monsterPointer][3] = x
                    screen.blit(monsterRotate, (x, monster[4]))
                elif monster[4] < 30:
                    monsterRotate = pygame.transform.rotate(monsterPicture, (360-monster[2]*180//pi))
                    y =monster[4] + abs(monsterSpeed*math.sin(monster[2]))
                    allMonsters[monsterPointer][4] = y
                    screen.blit(monsterRotate, (monster[3], y))

                monsterPointer += 1
        time += random.randint(5,20)
        return allMonsters,time,playerHealth

    #创建窗口
    pygame.init()
    screenWidth, screenHeight = 640, 480
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption('Welcome to play this boring game!')
    #加载图片素材
    playerPicture = pygame.image.load('Resources/Images/kuangsan.png')
    backgroundPickture = pygame.image.load('Resources/Images/background.jpg')
    bulletPicture = pygame.image.load('Resources/Images/bullet.png')
    monsterPicture = pygame.image.load('Resources/Images/monster_shidao.png')

    #窗口更新循环
    while 1:
    
        screen.fill(0)
        screen.blit(backgroundPickture, (0, 0))
        #player的旋转功能
        mousePosition = pygame.mouse.get_pos()
        playerAngle = math.atan2(mousePosition[1]-playerPosition[1],mousePosition[0]-playerPosition[0])
        playerRotate = pygame.transform.rotate(playerPicture,270-(playerAngle*180//pi))
        #找回player左上角
        playerPosition_real = (playerPosition[0]-playerRotate.get_rect().width//2,playerPosition[1]-playerRotate.get_rect().height//2)
        screen.blit(playerRotate, playerPosition_real)
        #monster制造

        a = list(monsterCreation(allMonsters,time,monsterAttack,monsterHealth))
        allMonsters = a[0]
        time = a[1]
        b = list(monsterControl(allMonsters,time,playerHealth))
        allMonsters = b[0]
        time = b[1]
        playerHealth = b[2]

        pygame.display.flip()
        #键位&鼠标操作
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == K_w:
                    directionKey[0] = True
                elif event.key == K_s:
                    directionKey[1] = True
                if event.key == K_a:
                    directionKey[2] = True
                elif event.key == K_d:
                    directionKey[3] = True
            if event.type == pygame.KEYUP:
                if event.key == K_w:
                    directionKey[0] = False
                if event.key == K_s:
                    directionKey[1] = False
                if event.key == K_a:
                    directionKey[2] = False
                if event.key == K_d:
                    directionKey[3] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePosition = pygame.mouse.get_pos()
                #bulletTrajectory的参数为（射击角度，初位置x，初位置y）
                bulletTrajectory.append([math.atan2(mousePosition[1]-playerPosition[1],mousePosition[0]-playerPosition[0]),playerPosition_real[0]+20,playerPosition_real[1]+30])
        #bullet控制
        bulletPointer = 0
        for bullet in bulletTrajectory:
            monsterPointer = 0
            if bullet[1] >= 620 or bullet[1] <= 0 or bullet[2] >= 460 or bullet[2] <= 0:
                bulletTrajectory.pop(bulletPointer)
            else:
                bullet_x = math.cos(bullet[0])*bulletSpeed
                bullet_y = math.sin(bullet[0])*bulletSpeed
                bullet[1] += bullet_x
                bullet[2] += bullet_y
                bulletTrajectory[bulletPointer][1] = bullet[1]
                bulletTrajectory[bulletPointer][2] = bullet[2]
                bulletPointer += 1
                bulletRotate = pygame.transform.rotate(bulletPicture, 360-(bullet[0]*180//pi))
                screen.blit(bulletRotate, (bullet[1], bullet[2]))
                for monster in allMonsters:
                    if (monster[3]+20 >= bullet[1] and monster[3]-20 <= bullet[1]) and (monster[4] <= bullet[2]+20 and monster[4] >= bullet[2]-20):
                        monster[0] -= playerAttack
                        if monster[0] <= 0:
                            allMonsters.pop(monsterPointer)
                            monsterPointer += 1

        pygame.display.flip()
        if directionKey[0] and playerPosition[1] >= 40:#防止player跑出屏幕
            playerPosition[1] -= playerSpeed
        if directionKey[1] and playerPosition[1] <= 440:
            playerPosition[1] += playerSpeed
        if directionKey[2] and playerPosition[0] >= 40:
            playerPosition[0] -= playerSpeed
        if directionKey[3] and playerPosition[0] <= 600:
            playerPosition[0] += playerSpeed

