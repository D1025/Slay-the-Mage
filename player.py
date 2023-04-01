import random
import pygame
import kolejka
import attack


IDLE = 0
RUN = 1
JUMP = 2
FALL = 3
ATT1 = 4
ATT2 = 5
ATT3 = 6
HIT = 7
DIE = 8


RIGHT = False
LEFT = True


SCALE = 2

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.immunity = 0
        self.hp = 100
        idle = pygame.image.load("Medieval King Pack 2/Sprites/Idle.png")
        run = pygame.image.load("Medieval King Pack 2/Sprites/Run.png")
        jump = pygame.image.load("Medieval King Pack 2/Sprites/Jump.png")
        fall = pygame.image.load("Medieval King Pack 2/Sprites/Fall.png")
        attack1 = pygame.image.load("Medieval King Pack 2/Sprites/Attack1.png")
        attack2 = pygame.image.load("Medieval King Pack 2/Sprites/Attack2.png")
        attack3 = pygame.image.load("Medieval King Pack 2/Sprites/Attack3.png")
        hit = pygame.image.load("Medieval King Pack 2/Sprites/Take Hit - white silhouette.png")
        die = pygame.image.load("Medieval King Pack 2/Sprites/Death.png")
        self.actions = kolejka.Queue()
        self.lastaction = None
        self.actual_frame = 0
        self.idleframe = 0
        self.dying_frame = 0
        self.animations = [(idle, 8), (run, 8), (jump, 2), (fall, 2), (attack1, 4), (attack2, 4), (attack3, 4), (hit, 4), (die, 6)]
        self.orientation = RIGHT
        self.dying_orientation = RIGHT
        rect = pygame.Rect(0, 0, 160, 111)
        subsurface = self.animations[IDLE][0].subsurface(rect)
        subsurface = pygame.transform.scale(pygame.transform.flip(subsurface, self.orientation, False), (160*SCALE, 111*SCALE))
        self.fullrect = subsurface.get_rect()
        self.rect = pygame.Rect(0, 0, 50, 100)
        self.rect.x = 0
        self.rect.y = 0
        self.fullrect.x = -135
        self.fullrect.y = -110
        self.drop = 0
        self.jumping = 0
        self.score = 0
        
        
    def __getframe__(self, enemies:pygame.sprite.Group):
        
        
        if self.hp <= 0:
            if self.dying_frame==6:
                self.dying_frame=4
            rect = pygame.Rect(self.dying_frame*160, 0, 160, 111)
            subsurface = self.animations[DIE][0].subsurface(rect)
            subsurface = pygame.transform.scale(pygame.transform.flip(subsurface, self.dying_orientation, False), (160*SCALE, 111*SCALE))
            self.dying_frame+=1
            return subsurface
        
        if self.jumping != 0:
            if self.jumping%10==0:
                self.actions.enqueue(self.animations[JUMP])
            self.rect.move_ip(0,-self.jumping)
            self.fullrect.move_ip(0,-self.jumping)
            self.jumping-=5
            
        
        
        if self.drop !=0:
            if self.drop%10==0:
                self.actions.enqueue(self.animations[FALL])
        

        if self.lastaction!= None and self.lastaction ==self.animations[RUN]:
                if self.actions.peek() == self.animations[RUN]:
                    self.lastaction=self.actions.dequeue()
                else:
                    self.actual_frame=0
                    self.lastaction=None
    
            # elif self.lastaction==self.actions.peek():
            #     self.actions.dequeue()
            # if self.actions.is_empty():
            #     self.actual_frame=0
        
        if self.actual_frame == 0:
            if self.actions.is_empty():
                if self.idleframe==8:
                    self.idleframe=0
                rect = pygame.Rect(self.idleframe*160, 0, 160, 111)
                subsurface = self.animations[IDLE][0].subsurface(rect)
                subsurface = pygame.transform.scale(pygame.transform.flip(subsurface, self.orientation, False), (160*SCALE, 111*SCALE))
                # self.rect = subsurface.get_rect()
                self.idleframe+=1
                return subsurface
            self.lastaction = self.actions.dequeue()
        
        if self.lastaction in [self.animations[ATT1], self.animations[ATT2], self.animations[ATT3]] and self.actual_frame==2:
            self.attack_check(enemies)
        rect = pygame.Rect(self.actual_frame*160, 0, 160,111)
        subsurface = self.lastaction[0].subsurface(rect)
        subsurface = pygame.transform.scale(pygame.transform.flip(subsurface, self.orientation, False), (160*SCALE, 111*SCALE))
        self.actual_frame+=1
        if self.actual_frame==self.lastaction[1]:
            self.actual_frame=0
            self.lastaction = None
            
        # self.rect = subsurface.get_rect()
        self.immunity-=1
        return subsurface
    
    
        
    def move_right(self):
        if self.actions.peek() not in [self.animations[RUN],self.animations[JUMP],self.animations[FALL]] and self.lastaction not in [self.animations[JUMP],self.animations[FALL]]:
            self.actions.enqueue(self.animations[RUN])
        self.orientation = RIGHT
        if self.rect.right>=760:
            return
        self.rect.move_ip(10, 0)
        self.fullrect.move_ip(10, 0)
        
        
    def move_left(self):
        if self.actions.peek() not in [self.animations[RUN],self.animations[JUMP],self.animations[FALL]] and self.lastaction not in [self.animations[JUMP],self.animations[FALL]]:
            self.actions.enqueue(self.animations[RUN])
        self.orientation = LEFT
        if self.rect.left<=10:
            return
        self.rect.move_ip(-10, 0)
        self.fullrect.move_ip(-10, 0)
        
        
        
    def dropping(self, tiles):
        if self.drop:
            self.rect.move_ip(0, +self.drop)
            self.fullrect.move_ip(0, +self.drop)
            #self.actions.enqueue(self.animations[3])
        colided = pygame.sprite.spritecollide(self, tiles, False)
        
        if colided or self.jumping!=0:
            if colided and self.drop!=0:
                self.lastaction = None
                self.actual_frame = 0
                self.actions = kolejka.Queue()
            self.drop=0
        else:
            self.drop +=5
            if self.drop>30:
                self.drop=30
        # if self.rect.colliderect(colided[0].rect) or self.jumping!=0:
        #     self.drop = 0
        # else:
        #     self.drop +=5
        #     if self.drop>30:
        #         self.drop=30

            
    def jump(self):
        if self.jumping==0 and self.drop==False:
            self.jumping = 30
            
    def attack_check(self, enemies:pygame.sprite.Group):
        
        colided = pygame.sprite.spritecollide(attack.Attack(self.rect, self.orientation), enemies, False)
        for enemie in colided:
            self.score+=enemie.get_hit()

    def attack(self):
        if self.actions.size()>3:
            return
        if (self.lastaction==self.animations[ATT1] or self.actions.peek==self.animations[ATT1]) and self.actions.peek()!=self.animations[ATT2]:
            self.actions.enqueue(self.animations[ATT2])
        elif (self.lastaction==self.animations[ATT2] or self.actions.peek==self.animations[ATT2]) and self.actions.peek()!=self.animations[ATT3]:
            self.actions.enqueue(self.animations[ATT3])
        elif self.lastaction not in [self.animations[ATT1], self.animations[ATT2]] and self.actions.peek() not in [self.animations[ATT1], self.animations[ATT2]]:
            self.actions.enqueue(self.animations[ATT1])
            
            
    def get_hit(self):
        if self.immunity<=0:
            self.immunity = 12
            self.actions = kolejka.Queue()
            self.lastaction = None
            self.actual_frame = 0
            self.actions.enqueue(self.animations[HIT])
            self.hp -= random.randint(20,40)
            if self.hp < 0:
                self.death()
        
    def death(self):
        self.dying_orientation=self.orientation
            
            
    def showhp(self)->float:
        return self.hp/100
    
    
    def isntAlive(self):
        return self.hp <= 0 and self.dying_frame==6
        
        
        
        

        
        


    
        
        
        