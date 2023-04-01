import random
import pygame
import kolejka



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


SCALE = 1.3

class Wizard(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.immunity = 0
        self.hp = 100
        idle = pygame.image.load("Wizard Pack/Idle.png")
        run = pygame.image.load("Wizard Pack/Run.png")
        jump = pygame.image.load("Wizard Pack/Jump.png")
        fall = pygame.image.load("Wizard Pack/Fall.png")
        attack1 = pygame.image.load("Wizard Pack/Attack1.png")
        attack2 = pygame.image.load("Wizard Pack/Attack2.png")
        attack3 = pygame.image.load("Wizard Pack/Attack1.png")
        hit = pygame.image.load("Wizard Pack/Hit.png")
        die = pygame.image.load("Wizard Pack/Death.png")
        self.actions = kolejka.Queue()
        self.lastaction = None
        self.actual_frame = 0
        self.idleframe = 0
        self.dying_frame = 0
        self.animations = [(idle, 6), (run, 8), (jump, 2), (fall, 2), (attack1, 8), (attack2, 8), (attack3, 8), (hit, 4), (die, 7)]
        self.orientation = RIGHT
        self.dying_orientation = RIGHT
        rect = pygame.Rect(0, 0, 231, 190)
        subsurface = self.animations[IDLE][0].subsurface(rect)
        subsurface = pygame.transform.scale(pygame.transform.flip(subsurface, self.orientation, False), (231*SCALE, 190*SCALE))
        self.fullrect = subsurface.get_rect()
        self.rect = pygame.Rect(0, 0, 50, 100)
        self.rect.x = 0
        self.rect.y = 0
        self.fullrect.x = -130
        self.fullrect.y = -80
        self.drop = 0
        self.jumping = 0
        
        
    def attack_check(self,projectiles):
        if self.lastaction in [self.animations[ATT1], self.animations[ATT2], self.animations[ATT3]] and self.actual_frame==5:
            projectiles.add(Fireball((self.rect.centerx, self.rect.centery-30), self.orientation))
        return projectiles
        
    def __getframe__(self):
        
        
        if self.hp <= 0:
            if self.dying_frame==7:
                self.kill()
                rect = pygame.Rect(6*231, 0, 231, 190)
                subsurface = self.animations[DIE][0].subsurface(rect)
                subsurface = pygame.transform.scale(pygame.transform.flip(subsurface, self.dying_orientation, False), (231*SCALE, 190*SCALE))
                return subsurface 
            rect = pygame.Rect(self.dying_frame*231, 0, 231, 190)
            subsurface = self.animations[DIE][0].subsurface(rect)
            subsurface = pygame.transform.scale(pygame.transform.flip(subsurface, self.dying_orientation, False), (231*SCALE, 190*SCALE))
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
                if self.idleframe==6:
                    self.idleframe=0
                rect = pygame.Rect(self.idleframe*231, 0, 231, 190)
                subsurface = self.animations[IDLE][0].subsurface(rect)
                subsurface = pygame.transform.scale(pygame.transform.flip(subsurface, self.orientation, False), (231*SCALE, 190*SCALE))
                # self.rect = subsurface.get_rect()
                self.idleframe+=1
                return subsurface
            self.lastaction = self.actions.dequeue()
        rect = pygame.Rect(self.actual_frame*231, 0, 231, 190)
        subsurface = self.lastaction[0].subsurface(rect)
        subsurface = pygame.transform.scale(pygame.transform.flip(subsurface, self.orientation, False), (231*SCALE, 190*SCALE))
        self.actual_frame+=1
        if self.actual_frame==self.lastaction[1]:
            self.actual_frame=0
            self.lastaction = None
            
        # self.rect = subsurface.get_rect()
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
            
            
    # def attack_spawn(self, list_of_enemies:pygame.sprite.Group):
    #     list
    def attack(self):
        if (self.lastaction==self.animations[ATT1] or self.actions.peek==self.animations[ATT1]) and self.actions.peek()!=self.animations[ATT2]:
            self.actions.enqueue(self.animations[ATT2])
        elif (self.lastaction==self.animations[ATT2] or self.actions.peek==self.animations[ATT2]) and self.actions.peek()!=self.animations[ATT3]:
            self.actions.enqueue(self.animations[ATT3])
        elif self.lastaction not in [self.animations[ATT1], self.animations[ATT2]] and self.actions.peek() not in [self.animations[ATT1], self.animations[ATT2]]:
            self.actions.enqueue(self.animations[ATT1])
            
            
    def get_hit(self):
                self.actions = kolejka.Queue()
                self.lastaction = None
                self.actual_frame = 0
                self.hp -= random.randint(20,40)
                self.actions.enqueue(self.animations[HIT])
                if self.hp < 0 and self.lastaction!=self.animations[DIE]:
                    self.death()
                    return 1
                return 0
        
    def death(self):
        self.dying_orientation=self.orientation
            
        
        
        
class Fireball(pygame.sprite.Sprite):
    def __init__(self, spawn:tuple, orient:bool) -> None:
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("Wizard Pack/fire-ball.png"), (3*3*19, 3*16))
        self.rect = pygame.Rect(0,0,3*19, 3*16)
        self.rect.x = spawn[0]
        self.rect.y = spawn[1]
        self.actual_frame = 0
        self.orientation = orient
        
        
    def __getframe__(self):
        if self.actual_frame ==3:
            self.actual_frame=0
        subspace = pygame.transform.flip(self.image.subsurface(pygame.Rect(self.actual_frame*3*19, 0, 3*19, 3*16)), not self.orientation, False)
        return subspace
        
    def move(self):
        if not self.orientation:
            self.rect.move_ip(10, 0)
        else:
            self.rect.move_ip(-10,0)
        if self.rect.x>800 or self.rect.x<-50:
            self.kill()
    
    def hit(self, enemie):
        if self.rect.colliderect(enemie.rect):
            enemie.get_hit()
            self.kill()


    
        
        
        