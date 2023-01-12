#子弹类

import pygame

#from tanks import g_up,g_down,g_left,g_right
import tanks

import logging
logging.basicConfig(format = '[%(asctime)s]-[%(funcName)s:%(lineno)d]- %(levelname)s - %(message)s', level=logging.INFO, )

class Bullet(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        #子弹图片
        self.m_bulletImgs = ['./images/bullet/bullet_up.png', './images/bullet/bullet_down.png', './images/bullet/bullet_left.png', './images/bullet/bullet_right.png']
        self.m_bullet = pygame.image.load(self.m_bulletImgs[0])
        self.rect = self.m_bullet.get_rect()
        #子弹速度
        self.m_speed = 6
        #子弹强度
        self.m_stronger = False
        #子弹是否存在
        self.being = True
        #子弹方向
        #上(0,-1) 下(0,1) 左(-1,0) 右(1,0)
        self.m_direction_x, self.m_direction_y = 0, -1 #默认方向上
        return None
    
    #设置子弹初始位置
    def initPos(self, pos:list) -> None:
        self.rect.topleft = pos
        return None

    #改变方向
    def turn(self, dirction:int) -> None:
        if dirction == tanks.g_up:
            self.m_direction_x, self.m_direction_y = 0, -1
            self.m_bullet = pygame.image.load(self.m_bulletImgs[0])
        elif dirction == tanks.g_down:
            self.m_direction_x, self.m_direction_y = 0, 1
            self.m_bullet = pygame.image.load(self.m_bulletImgs[1])
        elif dirction == tanks.g_left:
            self.m_direction_x, self.m_direction_y = -1, 0
            self.m_bullet = pygame.image.load(self.m_bulletImgs[2])
        elif dirction == tanks.g_right:
            self.m_direction_x, self.m_direction_y = 1, 0
            self.m_bullet = pygame.image.load(self.m_bulletImgs[3])
        return None

    #移动
    def move(self):
        self.rect = self.rect.move(self.m_speed*self.m_direction_x, self.m_speed*self.m_direction_y)
        #logging.info(f"bullet move-----rect[{self.rect}]")
        #到地图边缘后消失
        if (self.rect.top < 3) or (self.rect.bottom > 630-3) or (self.rect.left < 3) or (self.rect.right > 630-3):
            self.being = False
            return False
        else:
            return True

if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((630,630))
    backgrand = pygame.image.load("./images/others/background.png")
    bullet1 = Bullet()
    bullet1.turn(tanks.g_right)
    logging.info(f"bullet1.rect[{bullet1.rect}]")
    screen.blit(backgrand, (0,0))
    screen.blit(bullet1.m_bullet, bullet1.rect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.time.delay(1000)
        bullet1.move()
        screen.blit(backgrand, (0,0))
        screen.blit(bullet1.m_bullet, bullet1.rect)
        pygame.display.update()