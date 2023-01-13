#坦克类

import pygame
import random

import bullet

#日志模块 - 方便排查问题
import logging
logging.basicConfig(format = '[%(asctime)s]-[%(funcName)s:%(lineno)d]- %(levelname)s - %(message)s', level=logging.INFO, )

g_up, g_down, g_left, g_right = 0, 1, 2, 3 #方向
g_tankLevel = [0, 1, 2] #坦克等级
g_tankSpeed = [6, 12, 24] #坦克速度

class Tank(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.m_shootInterval = 500
        self.m_lastShootTime = pygame.time.get_ticks()  #最后射击的事件戳
        self.m_bulletGroup = pygame.sprite.Group()    #子弹
        self.m_pos = [0, 0]     #位置
        self.m_deriction = g_up #坦克方向
        self.m_speedLevel = 0;
        self.m_speed = g_tankSpeed[self.m_speedLevel]
        self.m_tankLevel = 0

        #初始化图片渐变
        self.m_initImg = './images/others/appear.png'
        self.m_initSurf = pygame.image.load(self.m_initImg)
        self.m_initSurfs = []
        self.m_initSurfs.append(self.m_initSurf.subsurface((0,0), (48,48)))
        self.m_initSurfs.append(self.m_initSurf.subsurface((48,0), (48,48)))
        self.m_initSurfs.append(self.m_initSurf.subsurface((96,0), (48,48)))
        self.m_state = 0 #记录当前初始化状态-实现渐变使用 0,1,2,初始化阶段 3正常 , 4爆炸
        self.m_initShowLastTime = pygame.time.get_ticks()

        #坦克爆炸
        self.m_boomImg = './images/others/boom_static.png'
        self.m_boomSurf = pygame.image.load(self.m_boomImg)
        self.m_dieTime = None
        self.m_isLive = True

    #加载坦克模型
    def loadTankMod(self, tankImg:str, pos:list):
        self.m_pos = pos.copy()
        #坦克模型
        self.m_tankImg = tankImg
        tankSurfTotal = pygame.image.load(self.m_tankImg)
        #显示前进动作
        tankUpMods = [tankSurfTotal.subsurface((0, 0), (48, 48)), tankSurfTotal.subsurface((48, 0), (48, 48))] #向上模型
        tankDownMods = [tankSurfTotal.subsurface((0, 48), (48, 48)), tankSurfTotal.subsurface((48, 48), (48, 48))] #向下模型
        tankLeftMods = [tankSurfTotal.subsurface((0, 96), (48, 48)), tankSurfTotal.subsurface((48, 96), (48, 48))] #向左模型
        tankRightMods = [tankSurfTotal.subsurface((0, 144), (48, 48)), tankSurfTotal.subsurface((48, 144), (48, 48))] #向右模型
        self.m_tankMods = []
        self.m_tankMods.append(tankUpMods)
        self.m_tankMods.append(tankDownMods)
        self.m_tankMods.append(tankLeftMods)
        self.m_tankMods.append(tankRightMods)
        #坦克矩形区域
        self.m_tank = self.m_tankMods[self.m_deriction][0]
        self.rect = self.m_tank.get_rect()
        self.rect = self.rect.move(self.m_pos)

    #初始化
    def show_init(self, screen:pygame.Surface, stage:int):
        screen.blit(self.m_initSurfs[stage], self.rect)
        for bullet in self.m_bulletGroup:
            screen.blit(bullet.m_bullet, bullet.rect)
        self.m_state = stage

    def boom(self):
        self.m_state = 4

    #显示坦克相关信息
    def show_tank(self, screen:pygame.Surface):
        #根据坦克状态显示坦克模型对应的模型
        #-初始化状态
        if self.m_state < 3:
            self.show_init(screen, self.m_state)
            timeNow = pygame.time.get_ticks()
            if timeNow - self.m_initShowLastTime > 200:
                #logging.warning(f"state:{self.m_state} initSurf.size:{len(self.m_initSurfs)}")
                self.m_state += 1
                self.m_initShowLastTime = timeNow
            return
        #坦克爆炸
        if self.m_state == 4:
            timeNow = pygame.time.get_ticks()
            if self.m_dieTime == None or timeNow - self.m_dieTime < 100:
                screen.blit(self.m_boomSurf, self.rect)
                if self.m_dieTime == None:
                    self.m_dieTime = pygame.time.get_ticks()
        #正常显示
        if self.m_state != 4:
            screen.blit(self.m_tank, self.rect)
        #判断是否还显示坦克相关模型
        if self.m_state == 4 and len(self.m_bulletGroup) < 1:
            self.m_isLive = False
        #坦克子弹显示
        for bullet in self.m_bulletGroup:
            screen.blit(bullet.m_bullet, bullet.rect)

    #坦克子弹移动
    def bulletMove(self):
        for bullet in self.m_bulletGroup:
            if not bullet.move(): #无效子弹移出-射出区域之外的子弹
                self.m_bulletGroup.remove(bullet)

    #坦克移动
    def move(self, brickGroup, ironGroup, tanksGroup):
        if self.m_state != 3:
            return
        if (self.m_deriction == g_up):
            self.moveUp(brickGroup, ironGroup, tanksGroup)
        elif (self.m_deriction == g_down):
            self.moveDown(brickGroup, ironGroup, tanksGroup)
        elif (self.m_deriction == g_left):
            self.moveLeft(brickGroup, ironGroup, tanksGroup)
        elif (self.m_deriction == g_right):
            self.moveRight(brickGroup, ironGroup, tanksGroup)

    #向上移动
    def moveUp(self, brickGroup, ironGroup, tanksGroup):
        if self.m_state != 3:
            return
        #方向不一致先调整方向
        if self.m_deriction != g_up:
            self.m_tank = self.m_tankMods[g_up][0]
            self.rect = self.m_tank.get_rect()
            self.rect.topleft = self.m_pos
            self.m_deriction = g_up
            return True
        #方向一致移动
        oldPos = self.m_pos.copy()
        #logging.info(f"oldPos[{oldPos}] pos[{self.m_pos}] rect[{self.rect}]")
        #边界判断
        self.m_pos[1] += self.m_speed*(-1)
        self.rect = self.rect.move(0, self.m_speed*(-1))
        #self.rect.topleft = self.m_pos
        #边界判断
        if self.m_pos[1] < 3:
            self.m_pos = oldPos
            self.rect = self.rect.move(0, self.m_speed*1)
            return False
        #检查碰撞
        if (isinstance(brickGroup, pygame.sprite.Group) and pygame.sprite.spritecollide(self, brickGroup, False, None))\
            or (isinstance(ironGroup, pygame.sprite.Group) and pygame.sprite.spritecollide(self, ironGroup, False, None))\
            or (isinstance(tanksGroup, pygame.sprite.Group) and pygame.sprite.spritecollide(self, tanksGroup, False, None)):
            #print('发生碰撞----')
            self.m_pos = oldPos
            self.rect = self.rect.move(0, self.m_speed*1)
            return False

        #交替替换图片
        if self.m_tank == self.m_tankMods[g_up][0]:
            self.m_tank = self.m_tankMods[g_up][1]
        elif self.m_tank == self.m_tankMods[g_up][1]:
            self.m_tank = self.m_tankMods[g_up][0]

        return True

    #向下移动
    def moveDown(self, brickGroup, ironGroup, tanksGroup):
        if self.m_state != 3:
            return
        #方向不一致先调整方向
        if self.m_deriction != g_down:
            self.m_tank = self.m_tankMods[g_down][0]
            self.rect = self.m_tank.get_rect()
            self.rect.topleft = self.m_pos
            self.m_deriction = g_down
            return True
        #方向一致移动
        oldPos = self.m_pos.copy()
        #边界判断
        self.m_pos[1] += self.m_speed*(1)
        self.rect = self.rect.move(0, self.m_speed*1)
        #边界判断
        if self.m_pos[1] > 630-3-48:
            self.m_pos = oldPos
            self.rect = self.rect.move(0, self.m_speed*(-1))
            return False
        #检查碰撞
        if (isinstance(brickGroup, pygame.sprite.Group) and pygame.sprite.spritecollide(self, brickGroup, False, None))\
            or (isinstance(ironGroup, pygame.sprite.Group) and pygame.sprite.spritecollide(self, ironGroup, False, None))\
            or (isinstance(tanksGroup, pygame.sprite.Group) and pygame.sprite.spritecollide(self, tanksGroup, False, None)):
            #print('发生碰撞----')
            self.m_pos = oldPos
            self.rect = self.rect.move(0, self.m_speed*(-1))
            return False

        #交替替换图片
        if self.m_tank == self.m_tankMods[g_down][0]:
            self.m_tank = self.m_tankMods[g_down][1]
        elif self.m_tank == self.m_tankMods[g_down][1]:
            self.m_tank = self.m_tankMods[g_down][0]
        
        return True

    #向左移动
    def moveLeft(self, brickGroup, ironGroup, tanksGroup):
        if self.m_state != 3:
            return
        #方向不一致先调整方向
        if self.m_deriction != g_left:
            self.m_tank = self.m_tankMods[g_left][0]
            self.rect = self.m_tank.get_rect()
            self.rect.topleft = self.m_pos
            self.m_deriction = g_left
            return True
        #方向一致移动
        oldPos = self.m_pos.copy()
        #logging.info(f"oldPos:[{oldPos}] pos:[{self.m_pos}] rect[{self.rect}]")
        #边界判断
        self.m_pos[0] += self.m_speed*(-1)
        self.rect = self.rect.move(self.m_speed*(-1), 0)
        #logging.info(f"oldPos:[{oldPos}] pos:[{self.m_pos}] rect[{self.rect}]")
        #边界判断
        if self.m_pos[0] < 3:
            self.m_pos = oldPos
            self.rect = self.rect.move(self.m_speed*(1), 0)
            return False

        #检查碰撞
        if (isinstance(brickGroup, pygame.sprite.Group) and pygame.sprite.spritecollide(self, brickGroup, False, None))\
            or (isinstance(ironGroup, pygame.sprite.Group) and pygame.sprite.spritecollide(self, ironGroup, False, None))\
            or (isinstance(tanksGroup, pygame.sprite.Group) and pygame.sprite.spritecollide(self, tanksGroup, False, None)):
            #print('发生碰撞----')
            self.m_pos = oldPos
            self.rect = self.rect.move(self.m_speed*(1), 0)
            return False

        #交替替换图片
        if self.m_tank == self.m_tankMods[g_left][0]:
            self.m_tank = self.m_tankMods[g_left][1]
        elif self.m_tank == self.m_tankMods[g_left][1]:
            self.m_tank = self.m_tankMods[g_left][0]

        return True
    
    #向右移动
    def moveRight(self, brickGroup, ironGroup, tanksGroup):
        if self.m_state != 3:
            return
        #方向不一致先调整方向
        if self.m_deriction != g_right:
            self.m_tank = self.m_tankMods[g_right][0]
            self.rect = self.m_tank.get_rect()
            self.rect.topleft = self.m_pos
            self.m_deriction = g_right
            return True
        #方向一致移动
        oldPos = self.m_pos.copy()
        #logging.info(f"oldPos:[{oldPos}] pos:[{self.m_pos}] rect[{self.rect}]")
        #边界判断
        self.m_pos[0] += self.m_speed*(1)
        self.rect = self.rect.move(self.m_speed*(1), 0)
        #logging.info(f"oldPos:[{oldPos}] pos:[{self.m_pos}] rect[{self.rect}]")
        #边界判断
        if self.m_pos[0] > 630-3-48:
            self.m_pos = oldPos
            self.rect = self.rect.move(self.m_speed*(-1), 0)
            return False

        #检查碰撞
        if (isinstance(brickGroup, pygame.sprite.Group) and pygame.sprite.spritecollide(self, brickGroup, False, None))\
            or (isinstance(ironGroup, pygame.sprite.Group) and pygame.sprite.spritecollide(self, ironGroup, False, None))\
            or (isinstance(tanksGroup, pygame.sprite.Group) and pygame.sprite.spritecollide(self, tanksGroup, False, None)):
            #logging.info(f"oldPos:[{oldPos}] pos:[{self.m_pos}] rect[{self.rect}]")
            self.m_pos = oldPos
            self.rect = self.rect.move(self.m_speed*(-1), 0)
            return False

        #交替替换图片
        if self.m_tank == self.m_tankMods[g_right][0]:
            self.m_tank = self.m_tankMods[g_right][1]
        elif self.m_tank == self.m_tankMods[g_right][1]:
            self.m_tank = self.m_tankMods[g_right][0]

        #logging.info(f"Final oldPos:[{oldPos}] pos:[{self.m_pos}] rect[{self.rect}]")

        return True
    
    #射击
    def shoot(self):
        if self.m_state != 3:
            return
        shootTime = pygame.time.get_ticks()
        #logging.info(f"now bullets:[{len(self.m_bulletGroup)}]")
        if shootTime - self.m_lastShootTime < self.m_shootInterval and len(self.m_bulletGroup)>0:
            return

        new_bullet = bullet.Bullet()
        new_bullet.turn(self.m_deriction)
        if self.m_deriction == g_up:
            new_bullet.initPos([self.rect.left + self.rect.width/2 - new_bullet.rect.width/2 , self.rect.top - new_bullet.rect.width])
        elif self.m_deriction == g_down:
            new_bullet.initPos([self.rect.left + self.rect.width/2 - new_bullet.rect.width/2, self.rect.bottom + new_bullet.rect.width])
        elif self.m_deriction == g_left:
            new_bullet.initPos([self.rect.left - new_bullet.rect.width, self.rect.top + self.rect.width/2 - new_bullet.rect.width/2])
        elif self.m_deriction == g_right:
            new_bullet.initPos([self.rect.right + new_bullet.rect.width, self.rect.top + self.rect.width/2 - new_bullet.rect.width/2])

        self.m_bulletGroup.add(new_bullet)
        self.m_lastShootTime = shootTime