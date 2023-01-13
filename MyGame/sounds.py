import pygame

class GameSound(object):
    def __init__(self):
        # 加载音效
        pygame.mixer.init()
        self.m_addSound = pygame.mixer.Sound("./audios/add.wav")
        self.m_addSound.set_volume(1)
        self.m_bangSound = pygame.mixer.Sound("./audios/bang.wav")
        self.m_bangSound.set_volume(1)
        self.m_blastSound = pygame.mixer.Sound("./audios/blast.wav")
        self.m_blastSound.set_volume(1)
        self.m_fireSound = pygame.mixer.Sound("./audios/fire.wav")
        self.m_fireSound.set_volume(1)
        self.m_GunfireSound = pygame.mixer.Sound("./audios/Gunfire.wav")
        self.m_GunfireSound.set_volume(1)
        self.m_hitSound = pygame.mixer.Sound("./audios/hit.wav")
        self.m_hitSound.set_volume(1)
        self.m_startSound = pygame.mixer.Sound("./audios/start.wav")
        self.m_startSound.set_volume(1)


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    sound = GameSound()
    sound.m_startSound.play()
    while True:
        pygame.time.delay(1000)
        ret = sound.m_startSound.get_length()
        print(f"ret:{ret}")