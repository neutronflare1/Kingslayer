# © 2023. neutronflare1 all rights reserved.

from abc import *                       # 추상클래스

# 플레이어 추상클래스
class Player(metaclass=ABCMeta):
    HP = 100
    HP_regen = 0.5

    @abstractmethod
    def A(self):
        pass
    
    @abstractmethod
    def B(self):
        pass

    @abstractmethod
    def C(self):
        pass

    @abstractmethod
    def D(self):
        pass


# 검을 쓰는 직업 정의
class Player_character_use_sword(Player):
    def __init__(self, weapon, armor):
        super().__init__()
        HP = Player.HP
        HP_regen = Player.HP_regen

    def A():
        pass

    def B():
        pass

    def C():
        pass

    def D():
        pass