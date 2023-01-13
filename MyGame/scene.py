#场景组件

import pygame

g_brickImg='./images/scene/brick.png'
g_ironImg='./images/scene/iron.png'
g_iceImg='./images/scene/ice.png'
g_riverImgs=['./images/scene/river1.png', './images/scene/river1.png']
g_treeImg='./images/scene/tree.png'
g_homeImg1 = './images/home/home1.png'
g_homeImg2 = './images/home/home2.png'
g_destroyImg = './images/home/home_destroyed.png'

#普通砖块类
class Brick(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.m_brick = pygame.image.load(g_brickImg)
        self.rect = self.m_brick.get_rect()
        self.being = False

#金属砖块类
class Iron(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.m_iron = pygame.image.load(g_ironImg)
        self.rect = self.m_iron.get_rect()
        self.being = False

#大本
class MyHome(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.m_home = pygame.image.load(g_homeImg1)
        self.m_destroy = pygame.image.load(g_destroyImg)
        self.rect = self.m_home.get_rect()
        self.being = False