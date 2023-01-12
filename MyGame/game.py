import pygame
import sys,os

import tanks
import level

class MyGame(object):
    def __init__(self):
        self.m_screen :pygame.Surface
        self.m_width = 630    #屏幕宽
        self.m_height = 630   #屏幕高
        self.m_gameName = u"坦克大战"
        self.m_opt1_str = u"1、单人游戏"
        self.m_opt2_str = u"2、双人游戏"

        self.m_isOver = False
        self.m_optBgClr = (100,100,100)
        self.m_bg_surf : pygame.Surface
        
        self.m_playMode = 1     #模式，1-单人 2-双人
        self.m_userNum1 = 3       #多少条命
        self.m_userPos1 = [3 + 24 * 8, 3 + 24 * 24]   #玩家1初始位置
        self.m_userNum2 = 3
        self.m_userPos2 = [3 + 24 * 12, 3 + 24 * 24]   #玩家2初始位置

        self.m_userTank1 = None
        self.m_userTank2 = None

        #地图-默认第一关
        self.m_map = level.Level1() #地图

        #按键标识
        self.up_state = False
        self.down_state = False
        self.left_state = False
        self.right_state = False
        self.m_timeLast1 = pygame.time.get_ticks()  #标记按键间隔 - 当键盘按键持续按压时使用-用户1按键
        self.m_timeLast2 = pygame.time.get_ticks()  #标记按键间隔 - 当键盘按键持续按压时使用-用户2按键

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
                return True

    #结束界面
    def show_over(self):
        pass

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
        #坦克出现
        pygame.time.delay(200)
        self.m_map.show_map(self.m_screen)
        self.m_userTank1.show_tank(self.m_screen)
        if self.m_playMode == 2:
            self.m_userTank2.show_init(self.m_screen, i)
        pygame.display.update()

    #键盘操作控制
    def playerOption(self, event:pygame.event.Event):
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

        timeNow = pygame.time.get_ticks()
        #上下左右按键
        if self.down_state:
            if timeNow - self.m_timeLast1 > 30:
                self.m_userTank1.moveDown(self.m_map.brickGroup, self.m_map.ironGroup, None)
                self.m_map.show_map(self.m_screen)
                self.m_screen.blit(self.m_userTank1.m_tank, self.m_userTank1.rect)
                self.m_timeLast1 = timeNow
        if self.up_state:
            if timeNow - self.m_timeLast1 > 30:
                self.m_userTank1.moveUp(self.m_map.brickGroup, self.m_map.ironGroup, None)
                self.m_map.show_map(self.m_screen)
                self.m_screen.blit(self.m_userTank1.m_tank, self.m_userTank1.rect)
                self.m_timeLast1 = timeNow
        if self.left_state:
            if timeNow - self.m_timeLast1 > 30:
                self.m_userTank1.moveLeft(self.m_map.brickGroup, self.m_map.ironGroup, None)
                self.m_map.show_map(self.m_screen)
                self.m_screen.blit(self.m_userTank1.m_tank, self.m_userTank1.rect)
                self.m_timeLast1 = timeNow
        if self.right_state:
            if timeNow - self.m_timeLast1 > 30:
                self.m_userTank1.moveRight(self.m_map.brickGroup, self.m_map.ironGroup, None)
                self.m_map.show_map(self.m_screen)
                self.m_screen.blit(self.m_userTank1.m_tank, self.m_userTank1.rect)
                self.m_timeLast1 = timeNow
        #子弹移动事件
        if event.type == self.BULLET_MOVE_EVENT:
            #未碰撞则移动子弹
            for bullet in self.m_userTank1.m_bulletGroup:
                if not bullet.move(): #无效子弹移出-射出区域之外的子弹
                    self.m_userTank1.m_bulletGroup.remove(bullet)
            #检查碰撞
            pygame.sprite.groupcollide(self.m_userTank1.m_bulletGroup, self.m_map.brickGroup, True, True, None)
            pygame.sprite.groupcollide(self.m_userTank1.m_bulletGroup, self.m_map.ironGroup, True, False, None)
            #渲染
            self.m_map.show_map(self.m_screen)
            #self.m_screen.blit(self.m_userTank1.m_tank, self.m_userTank1.rect)
            self.m_userTank1.show_tank(self.m_screen)

        #用户是否射击
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.m_userTank1.shoot()
            #检查碰撞
            pygame.sprite.groupcollide(self.m_userTank1.m_bulletGroup, self.m_map.brickGroup, True, True, None)
            pygame.sprite.groupcollide(self.m_userTank1.m_bulletGroup, self.m_map.ironGroup, True, False, None)
            for bullet in self.m_userTank1.m_bulletGroup:
                self.m_screen.blit(bullet.m_bullet, bullet.rect)
        #更新画面
        pygame.display.update()

    #开始游戏
    def start(self):
        self.init()
        self.show_begin()

        self.m_map.initBackgroundMap()

        #注册用户自定义事件
        self.CPU_MOVE_TIME_EVENT = pygame.USEREVENT + 1      #CPU移动的定时事件
        self.CPU_SHOOT_TIME_EVENT = pygame.USEREVENT + 2     #CPU发射子弹的频率
        self.CPU_ADD_EVENT = pygame.USEREVENT + 3            #CPU添加事件
        self.UPDATE_LOOP_EVENT = pygame.USEREVENT + 4        #画面更新事件
        self.BULLET_MOVE_EVENT = pygame.USEREVENT + 5        #子弹移动事件
        pygame.time.set_timer(self.CPU_MOVE_TIME_EVENT, 800) #CPU移动间隔
        pygame.time.set_timer(self.CPU_SHOOT_TIME_EVENT, 1000)#CPU射击间隔
        pygame.time.set_timer(self.UPDATE_LOOP_EVENT, 50)    #CPU射击间隔
        pygame.time.set_timer(self.BULLET_MOVE_EVENT, 20)    #CPU射击间隔

        #新关卡开始加载
        self.loadLevelTobegin()

        while not self.m_isOver:
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
            self.playerOption(event)