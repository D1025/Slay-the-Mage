
import sys
import pygame

from player import Player
from background import background, tile
from wizard import Wizard
from attack import spawn, do_something
from button import Button




pygame.init()



width = 768
height = 416
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

def get_font(size):
    # return pygame.font.SysFont("arial", size)
    return pygame.font.Font("assets/font.ttf", size)



def start():
    tlo = background()

    character = Player()
    wizard = Wizard()
    wizard.rect.x+=400
    wizard.fullrect.x+=400
    wizard.orientation=True
    enemies = pygame.sprite.Group()
    enemies.add(wizard)

    projectiles = pygame.sprite.Group()


    tiles = pygame.sprite.Group()
    for i in range(8):
        tiles.add(tile(i*96, 300)) 







    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                character.jump()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                character.attack()
                
            # if event.type == pygame.KEYDOWN and event.key==pygame.K_d:
            
            
            
        
            
        keys = pygame.key.get_pressed()

        # Sprawdź, czy klawisz "D" jest przytrzymany
        if keys[pygame.K_d]:
            character.move_right()
        elif keys[pygame.K_a]:
            character.move_left()
            
        # if keys[pygame.K_RIGHT]:
        #     archer.move_right()
        # elif keys[pygame.K_LEFT]:
        #     archer.move_left()
            
        colided = pygame.sprite.spritecollide(character, tiles, False)
        if keys[pygame.K_SPACE] and colided:
            character.jump()
        
        do_something(enemies)
        enemies = spawn(enemies, width)
            
            
        tlo.__printbackground__(screen)
        screen.fill((0,0,0), [0,330, width,height])
        for til in tiles:
            screen.blit(til.image,til.realrect)
            #screen.fill((0,255,0), til.rect)
        #scaled_image = pygame.transform.scale(szkielet.get_frame(), (4*24, 4*32))
        character.dropping(tiles)
        
        for proj in projectiles:
            proj.move()
            proj.hit(character)
            screen.blit(proj.__getframe__(), proj.rect)
        # screen.blit(szkielet.__getframe__(), szkielet.get_possition())
        for enemie in enemies:
            enemie.dropping(tiles)
            projectiles = enemie.attack_check(projectiles)
            screen.blit(enemie.__getframe__(), enemie.fullrect)
        #screen.fill((0, 255,0), archer.fullrect)
        #screen.fill((255,0,0), archer.rect)
        
        # screen.fill((255,0,0), character.rect)
        
        screen.blit(character.__getframe__(enemies), character.fullrect)

        tlo.__printfront__(screen)
        
        screen.fill((255,0,0), pygame.Rect(10,10,10+740*character.showhp(), 20))
        screen.blit(get_font(30).render(f"SCORE: {character.score}", True, (255, 255, 255)),(10, 30))
    
        pygame.display.flip()
        running = character.isAlive()
        clock.tick(12)
        
        
def menu():
    tlo = pygame.transform.scale(pygame.image.load("assets/bg.png"), (768, 416))
    while True:
        
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(40).render("SLAY THE MAGE", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(384, 50))

        PLAY_BUTTON = Button(image=pygame.transform.scale_by(pygame.image.load("assets/Play Rect.png"), 0.5) , pos=(384, 130), 
                            text_input="PLAY", font=get_font(20), base_color="#d7fcd4", hovering_color="#b68f40")
        OPTIONS_BUTTON = Button(image=pygame.transform.scale_by(pygame.image.load("assets/Play Rect.png"), 0.5), pos=(384, 210), 
                            text_input="OPTIONS", font=get_font(20), base_color="#d7fcd4", hovering_color="#b68f40")
        QUIT_BUTTON = Button(image=pygame.transform.scale_by(pygame.image.load("assets/Play Rect.png"), 0.5), pos=(384, 290), 
                            text_input="QUIT", font=get_font(20), base_color="#d7fcd4", hovering_color="#b68f40")
        
        # tlo.__printbackground__(screen)
        screen.blit(tlo, (0,0))

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    start()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pass
                    #options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(12)
        
menu()
        
pygame.quit()