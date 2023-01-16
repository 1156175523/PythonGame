import pygame
import sys,os
import random

import tanks
import level
import sounds

class MyGame(object):
    def __init__(self):
        self.m_screen :pygame.Surface
        self.m_width = 630    #屏幕宽
        self.m_height = 630   #屏幕高
        self.m_gameName = u"坦克大战"
        self.m_opt1_str = u"1、单人游戏"
        self.m_opt2_str = u"2、双人游戏"

        self.m_optBgClr = (100,100,100)
        self.m_bg_surf : pygame.Surface
        
        self.m_playMode = 1     #模式，1-单人 2-双人
        self.m_userNum1 = 3       #多少条命
        self.m_userPos1 = [3 + 24 * 8, 3 + 24 * 24]   #玩家1初始位置
        self.m_userNum2 = 3
        self.m_userPos2 = [3 + 24 * 12, 3 + 24 * 24]   #玩家2初始位置

        self.m_enemyPosList = ([3, 3], [630/2-24-3, 3], [630-48-3, 3])

        self.m_userTank1 = None
        self.m_userTank2 = None

        #地图-默认第一关
        self.m_map = level.Level1() #地图

        #CPU坦克集合
        self.m_cpuTanksGroup = pygame.sprite.Group()        #精灵族
        self.m_cpuTankNums = 5 * self.m_map.m_stage         #敌人总数
        self.m_maxShowEnemy = 5                             #最多同时显示多少敌人
        self.m_enemyImgLists = ['./images/enemyTank/enemy_1_0.png', './images/enemyTank/enemy_1_3.png', 
                                './images/enemyTank/enemy_2_0.png', './images/enemyTank/enemy_2_1.png', './images/enemyTank/enemy_2_2.png', './images/enemyTank/enemy_2_3.png',
                                './images/enemyTank/enemy_3_0.png', './images/enemyTank/enemy_3_3.png',
                                './images/enemyTank/enemy_4_0.png', './images/enemyTank/enemy_4_3.png']

        #按键标识
        self.up_state = False
        self.down_state = False
        self.left_state = False
        self.right_state = False
        self.m_timeLast1 = pygame.time.get_ticks()  #标记按键间隔 - 当键盘按键持续按压时使用-用户1按键
        self.m_timeLast2 = pygame.time.get_ticks()  #标记按键间隔 - 当键盘按键持续按压时使用-用户2按键

        #声音
        self.m_sound = sounds.GameSound()

    #初始化
    def init(self):
        pygame.init()
        self.m_screen = pygame.display.set_mode((self.m_width, self.m_height))
        pygame.display.set_caption(self.m_gameName)
        self.m_bg_surf = pygame.image.load("./images/others/background.png")
        self.m_logo_surf = pygame.image.load("./images/others/logo.png")
        self.m_logo_surf = pygame.transform.scale(self.m_logo_surf, (200,100))
        self.m_logo_rect = self.m_logo_surf.get_rect()
        self.m_logo_rect.midtop = (self.m_width//2, self.m_height//3)

    #取消初始化
    def uninit(self):
        pygame.quit()

    #开始界面
    def show_begin(self):
        font = pygame.font.Font("./font/STLITI.TTF", self.m_width//6)
        name_surf = font.render(self.m_gameName, True, (100,200,200))
        fontOpt = pygame.font.Font("./font/simfang.ttf", self.m_width//20)
        opt1_surf = fontOpt.render(self.m_opt1_str, True, (200,200,200), self.m_optBgClr)
        opt2_surf = fontOpt.render(self.m_opt2_str, True, (200,200,200))
        #布局
        name_rect = name_surf.get_rect();
        name_rect.midtop = (self.m_width//2, self.m_height//8)
        opt1_rect = opt1_surf.get_rect();
        opt1_rect.midtop= (self.m_width//2, self.m_height//1.8)
        opt2_rect = opt2_surf.get_rect();
        opt2_rect.midtop= (self.m_width//2, self.m_height//1.6)
        #绘制
        self.m_screen.blit(self.m_bg_surf, (0,0))
        self.m_screen.blit(self.m_logo_surf, self.m_logo_rect)
        self.m_screen.blit(name_surf, name_rect)
        self.m_screen.blit(opt1_surf, opt1_rect)
        self.m_screen.blit(opt2_surf, opt2_rect)
        pygame.display.update()
        self.start_option()

    #开始界面控制
    def start_option(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.uninit()
                    sys.exit()
                ret = self.selectOption(event)
                if ret:
                    return

    #开始界面选择操作
    def selectOption(self, event:pygame.event.Event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                font = pygame.font.Font("./font/STLITI.TTF", self.m_width//6)
                name_surf = font.render(self.m_gameName, True, (100,200,200))
                fontOpt = pygame.font.Font("./font/simfang.ttf", self.m_width//20)
                opt1_surf = fontOpt.render(self.m_opt1_str, True, (200,200,200), self.m_optBgClr)
                opt2_surf = fontOpt.render(self.m_opt2_str, True, (200,200,200))
                #布局
                name_rect = name_surf.get_rect();
                name_rect.midtop = (self.m_width//2, self.m_height//8)
                opt1_rect = opt1_surf.get_rect();
                opt1_rect.midtop= (self.m_width//2, self.m_height//1.8)
                opt2_rect = opt2_surf.get_rect();
                opt2_rect.midtop= (self.m_width//2, self.m_height//1.6)
                #绘制
                self.m_screen.blit(self.m_bg_surf, (0,0))
                self.m_screen.blit(self.m_logo_surf, self.m_logo_rect)
                self.m_screen.blit(name_surf, name_rect)
                self.m_screen.blit(opt1_surf, opt1_rect)
                self.m_screen.blit(opt2_surf, opt2_rect)
                pygame.display.update()
                self.m_playMode = 1
                return False
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                font = pygame.font.Font("./font/STLITI.TTF", self.m_width//6)
                name_surf = font.render(self.m_gameName, True, (100,200,200))
                fontOpt = pygame.font.Font("./font/simfang.ttf", self.m_width//20)
                opt1_surf = fontOpt.render(self.m_opt1_str, True, (200,200,200))
                opt2_surf = fontOpt.render(self.m_opt2_str, True, (200,200,200), self.m_optBgClr)
                #布局
                name_rect = name_surf.get_rect();
                name_rect.midtop = (self.m_width//2, self.m_height//8)
                opt1_rect = opt1_surf.get_rect();
                opt1_rect.midtop= (self.m_width//2, self.m_height//1.8)
                opt2_rect = opt2_surf.get_rect();
                opt2_rect.midtop= (self.m_width//2, self.m_height//1.6)
                #绘制
                self.m_screen.blit(self.m_bg_surf, (0,0))
                self.m_screen.blit(self.m_logo_surf, self.m_logo_rect)
                self.m_screen.blit(name_surf, name_rect)
                self.m_screen.blit(opt1_surf, opt1_rect)
                self.m_screen.blit(opt2_surf, opt2_rect)
                pygame.display.update()
                self.m_playMode = 2
                return False
            elif event.key == pygame.K_RETURN:
                print(f"开始游戏。。。")
                if self.m_playMode ==1:
                    self.m_userTank1 = tanks.Tank()
                    self.m_userTank1.loadTankMod("./images/myTank/tank_T1_0.png", self.m_userPos1)
                if self.m_playMode == 2:
                    self.m_userTank1 = tanks.Tank()
                    self.m_userTank1.loadTankMod("./images/myTank/tank_T1_0.png", self.m_userPos1)
                    self.m_userTank2 = tanks.Tank()
                    self.m_userTank2.loadTankMod("./images/myTank/tank_T2_0.png", self.m_userPos2)
                self.m_sound.m_startSound.play()
                return True

    #结束界面
    def show_over(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.m_map.m_isOver = False
                self.m_map.initBackgroundMap()
                #用户坦克重新初始化
                if self.m_playMode ==1:
                    self.m_userTank1 = tanks.Tank()
                    self.m_userTank1.loadTankMod("./images/myTank/tank_T1_0.png", self.m_userPos1)
                if self.m_playMode == 2:
                    self.m_userTank1 = tanks.Tank()
                    self.m_userTank1.loadTankMod("./images/myTank/tank_T1_0.png", self.m_userPos1)
                    self.m_userTank2 = tanks.Tank()
                    self.m_userTank2.loadTankMod("./images/myTank/tank_T2_0.png", self.m_userPos2)
                #机器人删除掉
                for enemyTank in self.m_cpuTanksGroup:
                    self.m_cpuTanksGroup.remove(enemyTank)
                self.m_cpuTankNums = 5 * self.m_map.m_stage
                #重新加载
                self.loadLevelTobegin()
                #清空事件
                pygame.event.get()
                return
        overImg = './images/others/gameover.png'
        overSurf = pygame.image.load(overImg)
        rect = overSurf.get_rect()
        self.m_screen.blit(overSurf, (self.m_width/2 - rect.width/2, self.m_height/2 - rect.height/2))
        pygame.display.update()

    #显示机器人坦克
    def show_enemyTanks(self):
        for enemyTank in self.m_cpuTanksGroup:
            if enemyTank.m_isLive:
                enemyTank.show_tank(self.m_screen)
            else:
                self.m_cpuTanksGroup.remove(enemyTank)

    #关卡加载模块-显示用户
    def loadLevelTobegin(self):
        #坦克出场动画
        for i in range(0, len(self.m_userTank1.m_initSurfs)):
            pygame.time.delay(200)
            self.m_map.show_map(self.m_screen)
            self.m_userTank1.show_init(self.m_screen, i)
            if self.m_playMode == 2:
                self.m_userTank2.show_init(self.m_screen, i)
            pygame.display.update()

        self.m_sound.m_addSound.play()
        #坦克出现
        pygame.time.delay(200)
        self.m_map.show_map(self.m_screen)
        self.m_userTank1.show_tank(self.m_screen)
        if self.m_playMode == 2:
            self.m_userTank2.show_init(self.m_screen, i)
        pygame.display.update()

    #键盘操作控制
    def playerOption(self, event:pygame.event.Event):
        #--按键标识模块
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.up_state = True
            elif event.key == pygame.K_DOWN:
                self.down_state = True
            elif event.key == pygame.K_LEFT:
                self.left_state = True
            elif event.key == pygame.K_RIGHT:
                self.right_state = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.up_state = False
            if event.key == pygame.K_DOWN:
                self.down_state = False
            if event.key == pygame.K_LEFT:
                self.left_state = False
            if event.key == pygame.K_RIGHT:
                self.right_state = False
        #--按键标识模块

        timeNow = pygame.time.get_ticks()
        #上下左右按键
        if self.down_state:
            if timeNow - self.m_timeLast1 > 30:
                self.m_userTank1.moveDown(self.m_map.brickGroup, self.m_map.ironGroup, self.m_cpuTanksGroup)
                self.m_map.show_map(self.m_screen)
                self.m_screen.blit(self.m_userTank1.m_tank, self.m_userTank1.rect)
                self.m_timeLast1 = timeNow
        if self.up_state:
            if timeNow - self.m_timeLast1 > 30:
                self.m_userTank1.moveUp(self.m_map.brickGroup, self.m_map.ironGroup, self.m_cpuTanksGroup)
                self.m_map.show_map(self.m_screen)
                self.m_screen.blit(self.m_userTank1.m_tank, self.m_userTank1.rect)
                self.m_timeLast1 = timeNow
        if self.left_state:
            if timeNow - self.m_timeLast1 > 30:
                self.m_userTank1.moveLeft(self.m_map.brickGroup, self.m_map.ironGroup, self.m_cpuTanksGroup)
                self.m_map.show_map(self.m_screen)
                self.m_screen.blit(self.m_userTank1.m_tank, self.m_userTank1.rect)
                self.m_timeLast1 = timeNow
        if self.right_state:
            if timeNow - self.m_timeLast1 > 30:
                self.m_userTank1.moveRight(self.m_map.brickGroup, self.m_map.ironGroup, self.m_cpuTanksGroup)
                self.m_map.show_map(self.m_screen)
                self.m_screen.blit(self.m_userTank1.m_tank, self.m_userTank1.rect)
                self.m_timeLast1 = timeNow
        #子弹移动事件
        if event.type == self.BULLET_MOVE_EVENT:
            '''
            for bullet in self.m_userTank1.m_bulletGroup:
                if not bullet.move(): #无效子弹移出-射出区域之外的子弹
                    self.m_userTank1.m_bulletGroup.remove(bullet)
            '''
            self.m_userTank1.bulletMove()
            #检查与场景的碰撞
            pygame.sprite.groupcollide(self.m_userTank1.m_bulletGroup, self.m_map.brickGroup, True, True, None)
            pygame.sprite.groupcollide(self.m_userTank1.m_bulletGroup, self.m_map.ironGroup, True, False, None)
            #检查命中敌人
            retEnemyTanks = pygame.sprite.groupcollide(self.m_userTank1.m_bulletGroup, self.m_cpuTanksGroup, True, False, None)
            if retEnemyTanks != None:
                for bullet,enemyTankList in retEnemyTanks.items():
                    #print(f"bullet type:{type(bullet)} enemy typ:{type(enemyTank)}") 
                    '''
                    for enemyTank in enemyTankList:
                        enemyTank.boom()
                        break   #杀掉一个敌人
                    '''
                    #图层渲染问题删除最后一个-最顶上的那个模型
                    enemyTankList[-1].boom()
            #检查是否击中老家
            ret1 = pygame.sprite.spritecollide(self.m_map.m_oldHome, self.m_userTank1.m_bulletGroup, True, None)
            if isinstance(ret1, list) and len(ret1) > 0:
                self.m_map.m_isOver = True
                self.m_sound.m_bangSound.play()
            #敌人子弹
            for enemyTank in self.m_cpuTanksGroup:
                #场景的碰撞
                enemyTank.bulletMove()
                pygame.sprite.groupcollide(enemyTank.m_bulletGroup, self.m_map.brickGroup, True, True, None)
                pygame.sprite.groupcollide(enemyTank.m_bulletGroup, self.m_map.ironGroup, True, False, None)
                #用户坦克的碰撞
                userTankGroupTmp = pygame.sprite.Group()
                userTankGroupTmp.add(self.m_userTank1)
                retEnemyTanks = pygame.sprite.groupcollide(enemyTank.m_bulletGroup, userTankGroupTmp, True, False, None)
                for bullet,userTankList in retEnemyTanks.items():
                        userTankList[-1].boom()
                #检查是否击中老家
                ret2 = pygame.sprite.spritecollide(self.m_map.m_oldHome, enemyTank.m_bulletGroup, True, None)
                if isinstance(ret2, list) and len(ret2) > 0:
                    self.m_map.m_isOver = True
                    self.m_sound.m_bangSound.play()

        #用户是否射击
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.m_userTank1.shoot()
            #检查碰撞
            pygame.sprite.groupcollide(self.m_userTank1.m_bulletGroup, self.m_map.brickGroup, True, True, None)
            pygame.sprite.groupcollide(self.m_userTank1.m_bulletGroup, self.m_map.ironGroup, True, False, None)
            for bullet in self.m_userTank1.m_bulletGroup:
                self.m_screen.blit(bullet.m_bullet, bullet.rect)

        #通过定时事件检查添加机器人
        if event.type == self.CPU_ADD_EVENT:
            if len(self.m_cpuTanksGroup) < self.m_maxShowEnemy and self.m_cpuTankNums > 0:
                newEnemyTank = tanks.Tank();
                pos = random.choice(self.m_enemyPosList)
                tankImg = random.choice(self.m_enemyImgLists)
                newEnemyTank.loadTankMod(tankImg, pos)
                newEnemyTank.moveDown(self.m_map.brickGroup, self.m_map.ironGroup, self.m_cpuTankNums)
                self.m_cpuTanksGroup.add(newEnemyTank)
                self.m_cpuTankNums -= 1

        #定时事件-机器人转向事件
        if event.type == self.CPU_TURN_TIME_EVENT:
            for enemyTank in self.m_cpuTanksGroup:
                moveDirection = random.choice([tanks.g_up, tanks.g_down, tanks.g_left, tanks.g_right])
                if moveDirection == tanks.g_up:
                    enemyTank.moveUp(self.m_map.brickGroup, self.m_map.ironGroup, None)
                elif moveDirection == tanks.g_down:
                    enemyTank.moveDown(self.m_map.brickGroup, self.m_map.ironGroup, None)
                if moveDirection == tanks.g_left:
                    enemyTank.moveLeft(self.m_map.brickGroup, self.m_map.ironGroup, None)
                if moveDirection == tanks.g_right:
                    enemyTank.moveRight(self.m_map.brickGroup, self.m_map.ironGroup, None)

        #定时事件-机器人移动数据事件
        if event.type == self.CPU_MOVE_TIME_EVENT:
            for enemyTank in self.m_cpuTanksGroup:
                userTankGroupTmp = pygame.sprite.Group()
                userTankGroupTmp.add(self.m_userTank1)
                enemyTank.move(self.m_map.brickGroup, self.m_map.ironGroup, userTankGroupTmp)
        #定时事件-机器人射击速度
        if event.type == self.CPU_SHOOT_TIME_EVENT:
            for enemyTank in self.m_cpuTanksGroup:
                enemyTank.shoot()

        #用户坦克初始化检查
        if not self.m_userTank1.m_isLive:
            self.m_userNum1 -= 1
            self.m_userTank1.rect.topleft = self.m_userPos1
            self.m_userTank1.m_state = 0
            self.m_userTank1.m_isLive = True
            self.m_userTank1.m_pos = self.m_userPos1.copy()

        #更新画面
        self.m_map.show_map(self.m_screen)
        self.m_userTank1.show_tank(self.m_screen)
        self.show_enemyTanks()
        pygame.display.update()

    #开始游戏
    def start(self):
        self.init()
        self.show_begin()

        self.m_map.initBackgroundMap()

        #注册用户自定义事件
        self.CPU_MOVE_TIME_EVENT = pygame.USEREVENT + 1      #CPU移动的定时事件
        self.CPU_TURN_TIME_EVENT = pygame.USEREVENT + 2      #CPU转向的定时事件
        self.CPU_SHOOT_TIME_EVENT = pygame.USEREVENT + 3     #CPU发射子弹的频率
        self.CPU_ADD_EVENT = pygame.USEREVENT + 4            #CPU添加事件
        self.UPDATE_LOOP_EVENT = pygame.USEREVENT + 5        #画面更新事件
        self.BULLET_MOVE_EVENT = pygame.USEREVENT + 6        #子弹移动事件
        pygame.time.set_timer(self.CPU_MOVE_TIME_EVENT, 50) 
        pygame.time.set_timer(self.CPU_TURN_TIME_EVENT, 1000)
        pygame.time.set_timer(self.CPU_SHOOT_TIME_EVENT, 500)
        pygame.time.set_timer(self.CPU_ADD_EVENT, 1000)
        pygame.time.set_timer(self.UPDATE_LOOP_EVENT, 50)
        pygame.time.set_timer(self.BULLET_MOVE_EVENT, 20)

        self.m_map.show_switch_stage(self.m_screen, self.m_width, self.m_height, self.m_map.m_stage)

        #新关卡开始加载
        self.loadLevelTobegin()

        while True:
            """
            #避免CPU占用过高
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.uninit()
                    sys.exit()
                #用户操作处理
                self.playerOption(event)
            """
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                self.uninit()
                sys.exit()

            #判断是否击中老家
            if self.m_map.m_isOver:
                self.show_over(event)
                continue

            self.playerOption(event)