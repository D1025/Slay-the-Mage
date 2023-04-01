import random
import pygame
from wizard import Wizard

class Attack(pygame.sprite.Sprite):
    def __init__(self, rect:pygame.Rect, orientation) -> None:
        super().__init__()
        center = list(rect.center)
        center[1] -=100
        if orientation:
            center[0]-=200
        self.rect = pygame.Rect(center[0], center[1], 200, 200)
        

def spawn(enemies:pygame.sprite.Group, width:int) -> Wizard:
    if enemies.__len__()>7:
        return enemies
    if random.randint(1,30)==1:
        wiz = Wizard()
        x = random.randint(1,width)
        wiz.fullrect.move_ip(x, -200)
        wiz.rect.move_ip(x, -200)
        enemies.add(wiz)
    return enemies


def do_something(enemies:pygame.sprite.Group):
    for enemie in enemies:
        if random.randint(1,40)==1:
            enemie.attack()
        else:
            if enemie.lastaction == enemie.animations[1]:
                if random.randint(1,5)!=1:
                    if random.randint(1,20)==1:
                        if enemie.orientation:
                            enemie.move_right()
                        else:
                            enemie.move_left()
                    else:
                        if enemie.orientation:
                            enemie.move_left()
                        else:
                            enemie.move_right()
            else:
                if random.randint(1,5)==1:
                    if random.randint(1,20)==1:
                        if enemie.orientation:
                            enemie.move_right()
                        else:
                            enemie.move_left()
                    else:
                        if enemie.orientation:
                            enemie.move_left()
                        else:
                            enemie.move_right()


                    