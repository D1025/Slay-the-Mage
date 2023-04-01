import pygame

class background():
    def __init__(self) -> None:
        self.moon = pygame.transform.scale(pygame.image.load("Final/Background_0.png"), (768, 416))
        self.church = pygame.transform.scale(pygame.image.load("Final/Background_1.png"), (768, 416))
        bushes = pygame.image.load("Final/brush.png")
        rect = pygame.Rect(0,0,224,96)
        self.bush1 = bushes.subsurface(rect)
        rect = pygame.Rect(0,96, 224, 96)
        self.bush2 = bushes.subsurface(rect)
        self.grass_background1 = pygame.image.load("Final/Grass_background_1.png")
        self.grass_background2 = pygame.image.load("Final/Grass_background_2.png")
    
        
        
        
    def __printbackground__(self, screen):
        screen.blit(self.moon, (0,0))
        screen.blit(self.church, (0,0))
        
    def __printfront__(self, screen):
        screen.blit(self.grass_background1, (0,130))
        screen.blit(self.grass_background2, (352, 130))
        screen.blit(self.grass_background1, (704, 130))
        
    
    
    
    
class tile(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.tiles = pygame.image.load("Final/Tiles.png")
        rect = pygame.Rect(128, 0, 96, 63)
        self.image = self.tiles.subsurface(rect)
        self.realrect = self.image.get_rect()
        self.realrect.x = x
        self.realrect.y = y
        self.rect = pygame.Rect(x, y+20, 96, 43)
        