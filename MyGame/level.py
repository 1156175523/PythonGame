#地图

import pygame
import time

import scene
import tanks

#地图基类
class Map(object):
    def __init__(self, width=630, height=630):
        #基础元素
        self.brickGroup = pygame.sprite.Group()         #普通砖块
        self.ironGroup = pygame.sprite.Group()          #金属砖块
        self.iceGroup = pygame.sprite.Group()           #冰块
        self.treeGroup = pygame.sprite.Group()          #树
        self.riverGroup = pygame.sprite.Group()         #河
        self.m_bgImg = './images/others/background.png'
        self.m_bgImg_surf = pygame.image.load(self.m_bgImg)
        self.m_font = './font/STLITI.TTF'
        self.m_fontColor = (100,100,100)
        self.m_width = width
        self.m_height = height
        self.m_oldHome = scene.MyHome()
        self.m_oldHome.rect.topleft = [3+12*24, 24*24+3]
        #老家被击中事件
        self.m_isHitTime = None
        self.m_isOver = False

    #大本营
    def protect_home(self):
        for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24), (11, 25), (14, 25)]:
            self.iron = scene.Iron()
            self.iron.rect.left, self.iron.rect.top = 3 + x * 24, 3 + y * 24
            self.iron.being = True
            self.ironGroup.add(self.iron)

    #关卡开始显示界面
    def show_switch_stage(self, screen:pygame.Surface, width:int, heigth:int, stage:int):
        font = pygame.font.Font(self.m_font, width//10)
        content_str = f"第 {stage} 关"
        content_surf = font.render(content_str, True, self.m_fontColor)
        rect = content_surf.get_rect()
        rect.midtop(width/2, heigth/2)
        screen.blit(self.m_bgImg_surf, (0,0))
        screen.blit(content_surf, rect)
        pygame.display.update()
        time.sleep(1)

    #初始化布景位置
    def initBackgroundMap(self):
        pass

    #显示地图
    def show_map(self, screen):
        #显示地图元素
        screen.blit(self.m_bgImg_surf, (0,0))
        for var_surf in self.brickGroup:
            screen.blit(var_surf.m_brick, var_surf.rect)
        for var_surf in self.ironGroup:
            screen.blit(var_surf.m_iron, var_surf.rect)
        for var_surf in self.iceGroup:
            screen.blit(var_surf.m_iron, var_surf.rect)
        for var_surf in self.treeGroup:
            screen.blit(var_surf.m_iron, var_surf.rect)
        for var_surf in self.riverGroup:
            screen.blit(var_surf.m_iron, var_surf.rect)
        if not self.m_isOver:
            screen.blit(self.m_oldHome.m_home, self.m_oldHome.rect)
        else:
            #被击中动态显示
            timeNow = pygame.time.get_ticks()
            if self.m_isHitTime == None:
                boomSurf = pygame.image.load("./images/others/boom_static.png")
                screen.blit(boomSurf, self.m_oldHome.rect)
                self.m_isHitTime = timeNow
            elif timeNow-self.m_isHitTime < 100:
                boomSurf = pygame.image.load("./images/others/boom_static.png")
                screen.blit(boomSurf, self.m_oldHome.rect)
            else:
                screen.blit(self.m_oldHome.m_destroy, self.m_oldHome.rect)

#第一关
class Level1(Map):
    #关卡1
    def __init__(self):
        Map.__init__(self)
        self.m_stage = 1

    #初始化布景位置
    def initBackgroundMap(self):
        for x in [2, 3, 6, 7, 18, 19, 22, 23]:
            for y in [2, 3, 4, 5, 6, 7, 8, 9, 10, 17, 18, 19, 20, 21, 22, 23]:
                brick = scene.Brick()
                brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
                brick.being = True
                self.brickGroup.add(brick)
        for x in [10, 11, 14, 15]:
            for y in [2, 3, 4, 5, 6, 7, 8, 11, 12, 15, 16, 17, 18, 19, 20]:
                brick = scene.Brick()
                brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
                brick.being = True
                self.brickGroup.add(brick)
        for x in [4, 5, 6, 7, 18, 19, 20, 21]:
            for y in [13, 14]:
                brick = scene.Brick()
                brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
                brick.being = True
                self.brickGroup.add(brick)
        for x in [12, 13]:
            for y in [16, 17]:
                brick = scene.Brick()
                brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
                brick.being = True
                self.brickGroup.add(brick)
        for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24), (11, 25), (14, 25)]:
            brick = scene.Brick()
            brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
            brick.being = True
            self.brickGroup.add(brick)
        for x, y in [(0, 14), (1, 14), (12, 6), (13, 6), (12, 7), (13, 7), (24, 14), (25, 14)]:
            iron = scene.Iron()
            iron.rect.left, iron.rect.top = 3 + x * 24, 3 + y * 24
            iron.being = True
            self.ironGroup.add(iron)


USER_TIME_LOOP_EVENT = pygame.USEREVENT + 1

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((630,630))
    leve1 = Level1()
    leve1.initBackgroundMap()

    leve1.show_map(screen)
    
    pygame.display.update()

    pos = [3 + 24 * 8, 3 + 24 * 24]
    #pos = [3 + 24 * 24, 3 + 24 * 8]
    tank = tanks.Tank()
    tank.loadTankMod("./images/myTank/tank_T1_0.png", pos)
    for i in range(0, len(tank.m_initSurfs)):
        print("load.....")
        pygame.time.delay(200)
        leve1.show_map(screen)
        screen.blit(tank.m_initSurfs[i], tank.rect)
        pygame.display.update()

    leve1.show_map(screen)
    screen.blit(tank.m_tank, tank.m_pos)
    pygame.display.update()

    timeLast = pygame.time.get_ticks()
    up_state = False
    down_state = False
    left_state = False
    right_state = False

    #注册定时事件
    pygame.time.set_timer(USER_TIME_LOOP_EVENT, 30)
    while True:
        #for event in pygame.event.get():
        event = pygame.event.wait(20)
        if event.type == pygame.QUIT:
            exit()

        ##判断键盘按键，移动图片
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                up_state = True
            elif event.key == pygame.K_DOWN:
                down_state = True
            elif event.key == pygame.K_LEFT:
                left_state = True
            elif event.key == pygame.K_RIGHT:
                right_state = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                up_state = False
            if event.key == pygame.K_DOWN:
                down_state = False
            if event.key == pygame.K_LEFT:
                left_state = False
            if event.key == pygame.K_RIGHT:
                right_state = False

        if down_state:
            timeNow = pygame.time.get_ticks()
            #if timeNow - timeLast > 100:
            if timeNow - timeLast > 30:
                tank.moveDown(leve1.brickGroup, leve1.ironGroup, None)
                leve1.show_map(screen)
                screen.blit(tank.m_tank, tank.rect)
                timeLast = timeNow
        if up_state:
            timeNow = pygame.time.get_ticks()
            #if timeNow - timeLast > 100:
            if timeNow - timeLast > 30:
                tank.moveUp(leve1.brickGroup, leve1.ironGroup, None)
                leve1.show_map(screen)
                screen.blit(tank.m_tank, tank.rect)
                timeLast = timeNow
        if left_state:
            timeNow = pygame.time.get_ticks()
            #if timeNow - timeLast > 100:
            if timeNow - timeLast > 30:
                tank.moveLeft(leve1.brickGroup, leve1.ironGroup, None)
                leve1.show_map(screen)
                screen.blit(tank.m_tank, tank.rect)
                timeLast = timeNow
        if right_state:
            timeNow = pygame.time.get_ticks()
            #if timeNow - timeLast > 100:
            if timeNow - timeLast > 30:
                tank.moveRight(leve1.brickGroup, leve1.ironGroup, None)
                leve1.show_map(screen)
                screen.blit(tank.m_tank, tank.rect)
                timeLast = timeNow

        #子弹移动
        if event.type == USER_TIME_LOOP_EVENT:
            #print(f"----》》》》》》bullet.size:{len(tank.m_bulletGroup)}")
            for bullet in tank.m_bulletGroup:
                if bullet.being:
                    bullet.move()  
                    #普通砖块处理
                    delBrickList = pygame.sprite.spritecollide(bullet, leve1.brickGroup, False, None)
                    if delBrickList != None and len(delBrickList) > 0:
                        tank.m_bulletGroup.remove(bullet)
                        for brick in delBrickList:
                            leve1.brickGroup.remove(brick)
                    #铁砖处理
                    ironList = pygame.sprite.spritecollide(bullet, leve1.ironGroup, False, None)
                    #print(f"ironList:{ironList}")
                    if ironList != None and len(ironList) > 0:
                        tank.m_bulletGroup.remove(bullet)
                else:
                    tank.m_bulletGroup.remove(bullet)

                leve1.show_map(screen)
                screen.blit(tank.m_tank, tank.rect)

        #是否射击
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            tank.shoot()

        for bullet in tank.m_bulletGroup:
            screen.blit(bullet.m_bullet, bullet.rect)

        pygame.display.update()