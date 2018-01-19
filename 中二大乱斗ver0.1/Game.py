__author__ = 'wesley'
# -*- coding:utf-8 -*-
#调用函数库
import math,random
import pygame
import sys
from pygame.locals import*

class MainGame:
    def __init__(self,saveFile):
        pygame.init()#初始化pygame中各个类和函数
        self.saveFile = saveFile
        self.time = 0 #控制怪物转向与生成
        self.monsterUpdateTime = 0
        self.skill_time = 0
        self.pauseFlag = False
        self.playerLevelUpFlag = False
        self.skill_1_flag = False
        self.skill_2_flag = False
        self.gameOverFlag = False

    #创建初始窗口
    def screenCreating(self):
        self.screenWidth, self.screenHeight = 640, 560
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption('Welcome to play this interesting game!')

    #玩家、monster以及子弹的初始设置
    def AttributeSetting_player(self):
        self.directionKey = [False,False,False,False]
        self.playerPosition = [100,70]
        self.playerMaxHealth = 100
        self.playerHealth = 100
        self.playerMaxMagic = 1000
        self.playerMagic = 0
        self.playerAttack = 1
        self.playerSpeed = 8
        self.playerMaxExp = 10
        self.playerExp = 0
        self.playerLevel = 0
        self.playerDistance = 15#判定大小，越小,人物越不容易被碰到

    def AttributeSetting_bullet(self):
        self.bulletTrajectory = []
        self.bulletSpeed = 20

    def AttributeSetting_monster(self):
        self.monsterLevel = 0
        self.monsterHealth = 5
        self.monsterAttack = 10
        self.monsterSpeed = 5
        self.monsterEXP = 1
        self.monsterDistance = 20
        self.allMonsters = []

    def load(self):
        if self.saveFile:
            f = open(self.saveFile,'r')
            list_playerAttribute = []
            list_f = f.readlines()
            f.close()
            for i in list_f:
                list_playerAttribute.append(eval(i.split('=')[1]))
            self.playerMaxHealth = list_playerAttribute[0]
            self.playerHealth = list_playerAttribute[1]
            self.playerMaxMagic = list_playerAttribute[2]
            self.playerMagic = list_playerAttribute[3]
            self.playerAttack = list_playerAttribute[4]
            self.playerSpeed = list_playerAttribute[5]
            self.playerMaxExp = list_playerAttribute[6]
            self.playerExp = list_playerAttribute[7]
            self.playerLevel = list_playerAttribute[8]
            self.playerDistance = list_playerAttribute[9]
            self.monsterLevel = list_playerAttribute[10]
            self.monsterHealth= list_playerAttribute[11]
            self.monsterAttack = list_playerAttribute[12]
            self.monsterSpeed = list_playerAttribute[13]
            self.monsterEXP = list_playerAttribute[14]
            self.monsterDistance = list_playerAttribute[15]

    def pictureLoading(self):
        #加载图片素材
        self.playerPicture = pygame.image.load('Resources/Images/kuangsan.png')
        self.backgroundPicture = pygame.image.load('Resources/Images/background.jpg')
        self.bulletPicture = pygame.image.load('Resources/Images/bullet.png')
        self.monsterPicture = pygame.image.load('Resources/Images/monster_shidao.png')
        self.levelupPicture = pygame.image.load('Resources/Images/levelup.jpg')
        self.skill_1_Picture = pygame.image.load('Resources/Images/Aleph.png')
        self.skill_2_Picture = pygame.image.load('Resources/Images/Dalet.png')
        self.playerAttributePicture = pygame.image.load('Resources/Images/Attributes.png')
        self.playerSkillPicture_1 = pygame.image.load('Resources/Images/skill.png')
        self.playerSkillPicture_2 = pygame.image.load('Resources/Images/skill2.png')

    def audioLoading(self):
        #加载声音素材
        self.bulletAudio = pygame.mixer.Sound("Resources/Audios/bullet.wav") #以片段形式加载音效
        self.hitMonsterAudio1 = pygame.mixer.Sound("Resources/Audios/monster_death/monster_death1.wav")
        self.hitMonsterAudio2 = pygame.mixer.Sound("Resources/Audios/monster_death/monster_death2.wav")
        self.hitMonsterAudio3 = pygame.mixer.Sound("Resources/Audios/monster_death/monster_death3.wav")
        self.hitMonsterAudio4 = pygame.mixer.Sound("Resources/Audios/monster_death/monster_death4.wav")
        self.hitMonsterAudio5 = pygame.mixer.Sound("Resources/Audios/monster_death/monster_death5.wav")
        self.hitMonsterAudio = [self.hitMonsterAudio1,self.hitMonsterAudio2,self.hitMonsterAudio3,self.hitMonsterAudio4,self.hitMonsterAudio5]
        self.playerBeHit1 = pygame.mixer.Sound("Resources/Audios/playerBeHit/playerBeHit1.wav")
        self.playerBeHit2 = pygame.mixer.Sound("Resources/Audios/playerBeHit/playerBeHit2.wav")
        self.playerBeHit3 = pygame.mixer.Sound("Resources/Audios/playerBeHit/playerBeHit3.wav")
        self.playerBeHit4 = pygame.mixer.Sound("Resources/Audios/playerBeHit/playerBeHit4.wav")
        self.playerBeHit5 = pygame.mixer.Sound("Resources/Audios/playerBeHit/playerBeHit5.wav")
        self.playerBeHit = [self.playerBeHit1,self.playerBeHit2,self.playerBeHit3,self.playerBeHit4,self.playerBeHit5]
        self.levelupAudio = pygame.mixer.Sound("Resources/Audios/levelup.wav")
        self.skill_1_Audio = pygame.mixer.Sound("Resources/Audios/skill_1.wav")
        self.skill_2_Audio = pygame.mixer.Sound("Resources/Audios/skill_2.wav")

    def playerControl(self):
        #player的旋转功能，通过鼠标位置和人物当前位置的三角函数计算，使人物子弹发射口转向鼠标
        self.mousePosition = pygame.mouse.get_pos()#pygame获取鼠标当前位置的方法，返回一个元祖(x,y)
        self.playerAngle = math.atan2(self.mousePosition[1]-self.playerPosition[1],self.mousePosition[0]-self.playerPosition[0])
        self.playerRotate = pygame.transform.rotate(self.playerPicture,270-(self.playerAngle*180//math.pi))
        #找回player左上角 (pygame的blit()方法即类似tkinter中pack()等方法，其锚点为对象左上角)
        self.playerPosition_real = (self.playerPosition[0]-self.playerRotate.get_rect().width//2,self.playerPosition[1]-self.playerRotate.get_rect().height//2)
        self.screen.blit(self.playerRotate, self.playerPosition_real)
        #防止player跑出屏幕
        if self.directionKey[0] and self.playerPosition[1] >= 40:
            self.playerPosition[1] -= self.playerSpeed
        if self.directionKey[1] and self.playerPosition[1] <= 440:
            self.playerPosition[1] += self.playerSpeed
        if self.directionKey[2] and self.playerPosition[0] >= 40:
            self.playerPosition[0] -= self.playerSpeed
        if self.directionKey[3] and self.playerPosition[0] <= 600:
            self.playerPosition[0] += self.playerSpeed

    #玩家升级
    def playerLevelUp(self):
        self.directionKey = [False,False,False,False]
        self.screen.blit(self.levelupPicture, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:#返回主界面
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == K_SPACE:
                    self.levelupAudio.play()
                    self.playerLevelUpFlag = False
                    self.playerLevel += 1
                    self.playerExp -= self.playerMaxExp
                    self.playerMaxExp = (10 + self.playerMaxExp) * 1.5
                    self.playerMaxHealth += (self.playerLevel * 20 + 10)
                    self.playerHealth = self.playerMaxHealth
                    self.playerMaxMagic += self.playerLevel * 20
                    self.playerAttack += self.playerLevel ** 2
                    self.playerSpeed += 1

    #玩家技能1
    def playerSkill_1(self):
        if self.skill_1_AudioFlag:
            self.skill_1_Audio.play()
            self.skill_1_AudioFlag = False
        self.screen.blit(self.skill_1_Picture, (0, 0))
        self.playerDistance = 0
        self.monsterSpeed = 0
        self.skill_time += 1
        during = 100 + self.playerLevel * 20
        if during >= 1000:
            during = 1000
        if self.skill_time >= during:
            self.skill_time = 0
            self.monsterSpeed = self.monsterSpeed_temp
            self.playerDistance = self.playerDistance_temp
            self.skill_1_flag = False

    #玩家技能2
    def playerSkill_2(self):
        if self.skill_2_AudioFlag:
            self.skill_2_Audio.play()
            self.skill_2_AudioFlag = False
        self.screen.blit(self.backgroundPicture, (0, 0))
        self.screen.blit(self.skill_2_Picture, (0, 0))
        self.skill_time += 1
        during = 20
        if self.skill_time >= during:
            self.skill_time = 0
            self.playerHealth += (50 + self.playerLevel * 25)
            if self.playerHealth >= self.playerMaxHealth:
                self.playerHealth = self.playerMaxHealth
            self.skill_2_flag = False

    #用来储存技能等情况造成的临时属性变化
    def tempUpdate(self):
        self.monsterSpeed_temp = self.monsterSpeed
        self.playerDistance_temp = self.playerDistance

    #控制怪物生成，生成条件为场上没有怪物了或者每隔一段时间;并且场上怪物剩余越少，人物等级越高，生成速度越快
    def monsterCreating(self):
        if self.time >= 500-self.playerLevel*10 or len(self.allMonsters) == 0:
            #allMonster（[health，attack，角度，x，y,怪物判定大小]）
            self.allMonsters.append([self.monsterHealth,self.monsterAttack,0,random.randint(60,570), random.randint(60,400),self.monsterDistance])
            self.time = 0
        #怪物过一段时间则升级一次
        if self.monsterUpdateTime >= 1000:
            self.monsterUpdateTime = 0
            self.monsterLevelUp()

    #从列表中去除血量为0的怪物
    def monsterKill(self):
        monsterPointer = 0
        for monster in self.allMonsters:
            if monster[0] <= 0:
                self.allMonsters.pop(monsterPointer)
                #播放怪物被消灭声效
                i = random.randint(0,4)
                self.hitMonsterAudio[i].play()
                self.playerExp += self.monsterEXP
            else:
                monsterPointer += 1

    def monsterLevelUp(self):
        self.monsterLevel += 1
        self.monsterHealth += self.monsterLevel * 10
        self.monsterAttack += self.monsterLevel * 2
        self.monsterSpeed += 1
        self.monsterEXP += self.monsterLevel

    def monsterControl(self):
        #怪物绘制，让怪物随机生成并随机移动和变向,考虑到减小游戏难度，怪物和人的碰撞体积小于实际图片显示
        monsterPointer = 0
        for monster in self.allMonsters:
            #判定人物是否和怪物相撞，若相撞则怪物消失，玩家血量减少
            if (monster[3] <= (self.playerPosition[0]  +self.playerDistance) and monster[3] >= (self.playerPosition[0]  - self.playerDistance)) and \
                    (monster[4] <= (self.playerPosition[1]+self.playerDistance) and monster[4] >= (self.playerPosition[1]-self.playerDistance)):
                self.playerHealth -= monster[1]
                self.allMonsters.pop(monsterPointer)
                #播放人物受伤音效
                i = random.randint(0,4)
                self.playerBeHit[i].play()

            else:
                #控制怪物转向，29为测试后得到的一个质数，转向频率较合理
                if monster[3] <= 610 and monster[3] >= 30 and monster[4] <= 450 and monster[4] >= 30:
                    if (self.time%29 == 0) and (self.time != 0):
                        monster[2] = math.atan2(random.uniform(-5,5),random.uniform(-5,5))
                        self.allMonsters[monsterPointer][2] = monster[2]
                        monsterRotate = pygame.transform.rotate(self.monsterPicture, (360-monster[2]*180//math.pi))
                        monster[3] += self.monsterSpeed*math.cos(monster[2])
                        monster[4] += self.monsterSpeed*math.sin(monster[2])
                        self.allMonsters[monsterPointer][3] = monster[3]
                        self.allMonsters[monsterPointer][4] = monster[4]
                        self.screen.blit(monsterRotate, (monster[3], monster[4]))
                    else:
                        monsterRotate = pygame.transform.rotate(self.monsterPicture, (360-monster[2]*180//math.pi))
                        x =monster[3] + self.monsterSpeed*math.cos(monster[2])
                        y =monster[4] + self.monsterSpeed*math.sin(monster[2])
                        self.allMonsters[monsterPointer][3] = x
                        self.allMonsters[monsterPointer][4] = y
                        self.screen.blit(monsterRotate, (x, y))
                        #monster血量显示
                        font = pygame.font.SysFont(None, 40)
                        str_monsterHP = str(monster[0]) + '/' + str(self.monsterHealth)
                        text_monsterHP = font.render(str_monsterHP,1, (255, 0, 0))
                        self.screen.blit(text_monsterHP,(x+40, y+40))

                #确保怪物不会走出画布，在画布边界处自行返回
                elif monster[3] > 600:
                    monsterRotate = pygame.transform.rotate(self.monsterPicture, (360-monster[2]*180//math.pi))
                    x = monster[3] - 3*abs(self.monsterSpeed*math.cos(monster[2]))
                    self.allMonsters[monsterPointer][3] = x
                    self.screen.blit(monsterRotate, (x, monster[4]))
                elif monster[4] > 430:
                    monsterRotate = pygame.transform.rotate(self.monsterPicture, (360-monster[2]*180//math.pi))
                    y = monster[4] - 3*abs(self.monsterSpeed*math.sin(monster[2]))
                    self.allMonsters[monsterPointer][4] = y
                    self.screen.blit(monsterRotate, (monster[3], y))
                elif monster[3] < 40:
                    monsterRotate = pygame.transform.rotate(self.monsterPicture, (360-monster[2]*180//math.pi))
                    x = monster[3] + 3*abs(self.monsterSpeed*math.cos(monster[2]))
                    self.allMonsters[monsterPointer][3] = x
                    self.screen.blit(monsterRotate, (x, monster[4]))
                elif monster[4] < 40:
                    monsterRotate = pygame.transform.rotate(self.monsterPicture, (360-monster[2]*180//math.pi))
                    y = monster[4] + 3*abs(self.monsterSpeed*math.sin(monster[2]))
                    self.allMonsters[monsterPointer][4] = y
                    self.screen.blit(monsterRotate, (monster[3], y))
                monsterPointer += 1
        self.time += random.randint(5,20)
        self.monsterUpdateTime += 1

    #bullet控制
    def bulletControl(self):
        bulletPointer = 0
        for bullet in self.bulletTrajectory:
            #判断子弹是否飞出屏幕，飞出则从列表中剔除，否则和monster进行接触判定
            if (bullet[1] >= 650) or (bullet[1] <= -20) or (bullet[2] >= 490) or (bullet[2] <= -20):
                self.bulletTrajectory.pop(bulletPointer)
            else:
                bullet_x = math.cos(bullet[0])*self.bulletSpeed
                bullet_y = math.sin(bullet[0])*self.bulletSpeed
                bullet[1] += bullet_x
                bullet[2] += bullet_y
                self.bulletTrajectory[bulletPointer][1] = bullet[1]
                self.bulletTrajectory[bulletPointer][2] = bullet[2]
                bulletPointer += 1
                bulletRotate = pygame.transform.rotate(self.bulletPicture, 360-(bullet[0]*180//math.pi))
                self.screen.blit(bulletRotate, (bullet[1], bullet[2]))
                #子弹是否击中怪物的判定
                for monster in self.allMonsters:
                    if ((monster[3]+monster[5]) >= bullet[1] and (monster[3]-monster[5]) <= bullet[1]) and (monster[4] <= (bullet[2]+monster[5])
                        and monster[4] >= (bullet[2]-monster[5])) and bullet[3] == False:
                        monster[0] -= self.playerAttack
                        #标记该子弹失效
                        bullet[3] = True

    #玩家属性绘制
    def playerAttributeShow(self):
        black = (0, 0, 0)
        green = (0, 255, 0)
        red = (255, 0, 0)
        white = (255,255,255)
        blue = (0,0,255)
        #pygame设置字体
        font = pygame.font.SysFont(None, 25)
        font_skill = pygame.font.SysFont(None, 30)

        text_blood = font.render("HP:",1, black)
        str_bloodNumber = str(self.playerHealth) + '/' + str(self.playerMaxHealth)
        text_bloodNumber = font.render(str_bloodNumber,1, white)
        self.screen.blit(text_blood,(10,10))
        #建立玩家血槽，底色黑色，如果血量大于百分之二十则为绿色，否则为红色
        #pygame.line的参数分别为（所在画面，颜色，左上角，右上角，宽度）
        pygame.draw.line(self.screen, black,(40,15),(220,15),20)
        playerHealth_remain = float(self.playerHealth)/(self.playerMaxHealth)
        if playerHealth_remain > 0.2:
            bloodColour = green
        else:
            bloodColour = red
        if playerHealth_remain >= 0:
            pygame.draw.line(self.screen,bloodColour,(40,15),(40+playerHealth_remain*180,15),20)
        self.screen.blit(self.playerAttributePicture,(20,480))
        str_attackNumber = "ATK:" + str(self.playerAttack)
        text_attackNumber = font.render(str_attackNumber,1, black)
        self.screen.blit( text_attackNumber,(50,490))

        str_speedNumber = "SPD:" + str(self.playerSpeed)
        text_speedNumber = font.render(str_speedNumber,1, black)
        self.screen.blit(text_speedNumber,(150,490))

        str_skill = "Skill"
        text_skill = font_skill.render(str_skill,1, black)
        self.screen.blit(text_skill,(300,490))

        str_EXPNumber = "EXP:" + str(int(self.playerExp)) + '/' + str(int(self.playerMaxExp))
        text_EXPNumber = font.render(str_EXPNumber,1, black)
        self.screen.blit(text_EXPNumber,(300,10))

        str_levelNumber = "LV:" + str(self.playerLevel)
        text_levelNumber = font.render(str_levelNumber,1, black)
        self.screen.blit(text_levelNumber,(250,10))

        self.screen.blit(text_blood,(10,10))

        #技能槽
        pygame.draw.line(self.screen,white,(40,30),(220,30),15)
        playerMagic_remain = float(self.playerMagic)/self.playerMaxMagic
        if playerMagic_remain > 0.2:
            magicColour = blue
        else:
            magicColour = red
        pygame.draw.line(self.screen,magicColour,(40,30),(40+playerMagic_remain*180,30),15)
        str_magic = "Mp:"
        text_magic = font.render(str_magic,1,black)
        str_magicNumber = str(self.playerMagic) + '/' + str(self.playerMaxMagic)
        text_magicNumber = font.render(str_magicNumber,1, black)

        self.screen.blit(text_magic,(10,25))
        self.screen.blit(text_bloodNumber,(80,10))
        self.screen.blit(text_magicNumber,(80,25))

    def playerSkillShow(self):
        if self.playerLevel >= 0:
            self.screen.blit(self.playerSkillPicture_1,(360,480))
        if self.playerLevel >= 6:
            self.screen.blit(self.playerSkillPicture_2,(420,480))

    def settingShow(self):
        black = (0, 0, 0)
        font = pygame.font.SysFont(None, 20)
        #save
        text_save = font.render('[SAVE] Automatically When QUIT',2,black)
        self.screen.blit(text_save,(25,525))
        #pause
        text_pause = font.render('"SPACE" to [Pause]',2,black)
        self.screen.blit(text_pause,(425,525))

    #功能函数
    def save(self):
        list_playerAttribute = ['playerMaxHealth='+str(self.playerMaxHealth)+'\n',
            'playerHealth='+str(self.playerHealth)+'\n',
            'playerMaxMagic='+str(self.playerMaxMagic)+'\n',
            'playerMagic='+str(self.playerMagic)+'\n',
            'playerAttack='+str(self.playerAttack)+'\n',
            'playerSpeed='+str(self.playerSpeed)+'\n',
            'playerMaxExp='+str(self.playerMaxExp)+'\n',
            'playerExp='+str(self.playerExp)+'\n',
            'playerLevel='+str(self.playerLevel)+'\n',
            'playerDistance='+str(self.playerDistance_temp)+'\n',
            'monsterLevel='+str(self.monsterLevel)+'\n',
            'monsterHealth='+str(self.monsterHealth)+'\n',
            'monsterAttack='+str(self.monsterAttack)+'\n',
            'monsterSpeed='+str(self.monsterSpeed_temp)+'\n',
            'monsterEXP='+str(self.monsterEXP)+'\n',
            'monsterDistance='+str(self.monsterDistance)]
        f = open('saveData.txt','w')
        for atr in list_playerAttribute:
            f.write(atr)
        f.close()

    def gameOver(self):
        self.screen.blit(self.backgroundPicture, (0, 0))
        font = pygame.font.SysFont(None, 60)
        red = (255,0,0)
        str_gameOver = 'Sorry,Game Over!'
        text_gameOver = font.render(str_gameOver,3, red)
        self.screen.blit(text_gameOver,(130,180))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:#返回主界面
                pygame.quit()

    def pause(self):
        self.screen.blit(self.backgroundPicture, (0, 0))
        font = pygame.font.SysFont(None, 40)
        str_pause = 'Please press "SPACE" to resume the game!'
        black = (0,0,0)
        text_pause = font.render(str_pause,2, black)
        self.screen.blit(text_pause,(20,220))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:#保存并退出
                self.save()
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == K_SPACE:
                    self.pauseFlag = False

    #窗口更新循环
    def update(self):
        self.screen.blit(self.backgroundPicture, (0, 0))
        #如果有技能被触发，则优先处理技能效果
        if self.skill_1_flag:
            self.playerSkill_1()
        elif self.skill_2_flag:
            self.playerSkill_2()
        else:
            self.tempUpdate()
            self.monsterCreating()

        self.playerControl()
        #monster制造、运动和判定
        self.monsterControl()
        #画制人物属性、技能
        self.playerAttributeShow()
        self.playerSkillShow()
        #绘制设置
        self.settingShow()
        #pygame刷新画布的方法
        pygame.display.flip()
        #键位&鼠标操作
        # pygame的event放在自身event类中，存放在一个列表里，
        # 提供各种类的方法对列表里元素进行操作，此处用到了退出事件、鼠标事件和键盘事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:#保存并退出
                self.save()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_w:
                    self.directionKey[0] = True
                elif event.key == K_s:
                    self.directionKey[1] = True
                if event.key == K_a:
                    self.directionKey[2] = True
                elif event.key == K_d:
                    self.directionKey[3] = True
                if event.key == K_j and self.playerMagic >= 1000:
                    if self.skill_1_flag == False and self.skill_2_flag == False:
                        self.skill_1_flag = True
                        self.skill_1_AudioFlag = True
                        self.playerMagic -= 1000
                elif event.key == K_k and self.playerMagic >= 700 and self.playerLevel >= 6:
                    if self.skill_1_flag == False and self.skill_2_flag == False:
                        self.skill_2_flag = True
                        self.skill_2_AudioFlag = True
                        self.playerMagic -= 700

            if event.type == pygame.KEYUP:
                if event.key == K_SPACE:
                    self.pauseFlag = True
                else:
                    if event.key == K_w:
                        self.directionKey[0] = False
                    if event.key == K_s:
                        self.directionKey[1] = False
                    if event.key == K_a:
                        self.directionKey[2] = False
                    if event.key == K_d:
                        self.directionKey[3] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mousePosition = pygame.mouse.get_pos()
                #bulletTrajectory的参数为（[射击角度，初位置x，初位置y,hitFlag]）
                self.bulletTrajectory.append([math.atan2(self.mousePosition[1]-self.playerPosition[1],
                    self.mousePosition[0]-self.playerPosition[0]),self.playerPosition_real[0]+20,self.playerPosition_real[1]+30,False])
                self.bulletAudio.play()#子弹发射音效
        #mp回复
        if self.playerMagic <= self.playerMaxMagic:
            self.playerMagic += 1
        self.bulletControl()
        self.monsterKill()
        pygame.display.flip()
        #Flag判定
        if self.playerExp >= self.playerMaxExp and self.skill_1_flag == False and self.skill_2_flag == False:
            self.playerLevelUpFlag = True
        if self.playerHealth <= 0:
            self.gameOverFlag = True

    def run(self):
        self.AttributeSetting_player()
        self.AttributeSetting_monster()
        self.AttributeSetting_bullet()
        self.load()
        self.screenCreating()
        self.pictureLoading()
        self.audioLoading()
        while 1:
            if self.playerLevelUpFlag == True:
                self.playerLevelUp()
            elif self.pauseFlag == True:
                self.pause()
            elif self.gameOverFlag == True:
                self.gameOver()
            else:
                self.update()
