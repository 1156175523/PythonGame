#坦克类

import pygame
import random

#日志模块 - 方便排查问题
import logging
logging.basicConfig(format = '[%(asctime)s]-[%(funcName)s:%(lineno)d]- %(levelname)s - %(message)s', level=logging.INFO, )

g_up, g_down, g_left, g_right = 0, 1, 2, 3 #方向
g_tankLevel = [0, 1, 2] #坦克等级
g_tankSpeed = [6, 12, 18] #坦克速度

class Tank(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.m_bullet = None    #子弹
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

    #加载坦克模型
    def loadTankMod(self, tankImg:str, pos:list):
        self.m_pos = pos
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

    #向上移动
    def moveUp(self, brickGroup, ironGroup, tanksGroup):
        #方向不一致先调整方向
        if self.m_deriction != g_up:
            self.m_tank = self.m_tankMods[g_up][0]
            self.rect = self.m_tank.get_rect()
            self.rect.topleft = self.m_pos
            self.m_deriction = g_up
            return True
        #方向一致移动
        oldPos = self.m_pos.copy()
        logging.info(f"oldPos[{oldPos}] pos[{self.m_pos}] rect[{self.rect}]")
        #边界判断
        self.m_pos[1] += self.m_speed*(-1)
        self.rect.move(self.m_pos)
        self.rect.topleft = self.m_pos
        #边界判断
        if self.m_pos[1] < 3:
            self.m_pos = oldPos
            self.rect.topleft = self.m_pos
            return False
        #检查碰撞
        if pygame.sprite.spritecollide(self, brickGroup, False, None)\
            or pygame.sprite.spritecollide(self, ironGroup, False, None):
            print('发生碰撞----')
            self.m_pos = oldPos
            self.rect.topleft = self.m_pos
            return False

        #交替替换图片
        if self.m_tank == self.m_tankMods[g_up][0]:
            self.m_tank = self.m_tankMods[g_up][1]
        elif self.m_tank == self.m_tankMods[g_up][1]:
            self.m_tank = self.m_tankMods[g_up][0]

        self.rect.topleft = self.m_pos

        return True

    #向下移动
    def moveDown(self, brickGroup, ironGroup, tanksGroup):
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
        self.rect.move(self.m_pos)
        self.rect.topleft = self.m_pos
        #边界判断
        if self.m_pos[1] > 630-3-48:
            self.m_pos = oldPos
            self.rect.topleft = self.m_pos
            return False
        #检查碰撞
        if pygame.sprite.spritecollide(self, brickGroup, False, None)\
            or pygame.sprite.spritecollide(self, ironGroup, False, None):
            print('发生碰撞----')
            self.m_pos = oldPos
            self.rect.topleft = self.m_pos
            return False

        #交替替换图片
        if self.m_tank == self.m_tankMods[g_down][0]:
            self.m_tank = self.m_tankMods[g_down][1]
        elif self.m_tank == self.m_tankMods[g_down][1]:
            self.m_tank = self.m_tankMods[g_down][0]
        
        self.rect.topleft = self.m_pos

        return True

    #向左移动
    def moveLeft(self, brickGroup, ironGroup, tanksGroup):
        #方向不一致先调整方向
        if self.m_deriction != g_left:
            self.m_tank = self.m_tankMods[g_left][0]
            self.rect = self.m_tank.get_rect()
            self.rect.topleft = self.m_pos
            self.m_deriction = g_left
            return True
        #方向一致移动
        oldPos = self.m_pos.copy()
        logging.info(f"oldPos:[{oldPos}] pos:[{self.m_pos}] rect[{self.rect}]")
        #边界判断
        self.m_pos[0] += self.m_speed*(-1)
        self.rect.move(self.m_pos)
        self.rect.topleft = self.m_pos
        print(f"oldPos:[{oldPos}] pos:[{self.m_pos}] rect[{self.rect}]")
        logging.info(f"oldPos:[{oldPos}] pos:[{self.m_pos}] rect[{self.rect}]")
        #边界判断
        if self.m_pos[0] < 3:
            print(f"oldPos:[{oldPos}]")
            self.m_pos = oldPos
            self.rect.topleft = self.m_pos
            return False

        #检查碰撞
        if pygame.sprite.spritecollide(self, brickGroup, False, None)\
            or pygame.sprite.spritecollide(self, ironGroup, False, None):
            print('发生碰撞----')
            self.m_pos = oldPos
            self.rect.topleft = self.m_pos
            return False


        #交替替换图片
        if self.m_tank == self.m_tankMods[g_left][0]:
            self.m_tank = self.m_tankMods[g_left][1]
        elif self.m_tank == self.m_tankMods[g_left][1]:
            self.m_tank = self.m_tankMods[g_left][0]

        self.rect.topleft = self.m_pos

        return True
    
    #向右移动
    def moveRight(self, brickGroup, ironGroup, tanksGroup):
        #方向不一致先调整方向
        if self.m_deriction != g_right:
            self.m_tank = self.m_tankMods[g_right][0]
            self.rect = self.m_tank.get_rect()
            self.rect.topleft = self.m_pos
            self.m_deriction = g_right
            return True
        #方向一致移动
        oldPos = self.m_pos.copy()
        logging.info(f"oldPos:[{oldPos}] pos:[{self.m_pos}] rect[{self.rect}]")
        #边界判断
        self.m_pos[0] += self.m_speed*(1)
        self.rect.move(self.m_pos)
        self.rect.topleft = self.m_pos
        logging.info(f"oldPos:[{oldPos}] pos:[{self.m_pos}] rect[{self.rect}]")
        #边界判断
        if self.m_pos[0] > 630-3-48:
            self.m_pos = oldPos
            self.rect.topleft = self.m_pos
            return False
        #检查碰撞
        if pygame.sprite.spritecollide(self, brickGroup, False, None)\
            or pygame.sprite.spritecollide(self, ironGroup, False, None):
            print('发生碰撞----')
            logging.info(f"oldPos:[{oldPos}] pos:[{self.m_pos}] rect[{self.rect}]")
            self.m_pos = oldPos
            self.rect.topleft = self.m_pos
            return False

        #交替替换图片
        if self.m_tank == self.m_tankMods[g_right][0]:
            self.m_tank = self.m_tankMods[g_right][1]
        elif self.m_tank == self.m_tankMods[g_right][1]:
            self.m_tank = self.m_tankMods[g_right][0]

        self.rect.topleft = self.m_pos
        logging.info(f"Final oldPos:[{oldPos}] pos:[{self.m_pos}] rect[{self.rect}]")

        return True
    
    #射击
    def shoot(self):
        pass