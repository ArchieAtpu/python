import pygame 

background = pygame.image.load('./assets/creditBackground.png')

def creditScene(events, screen, state, globals):
    for event in events:
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            if mousePos[0] > 388 and mousePos[0] < 640 and mousePos[1] > 657 and mousePos[1] < 743:
                return "credits" 
            elif mousePos[0] > 827 and mousePos[0] < 1004 and mousePos[1] > 693 and mousePos[1] < 753:
                return "menu"

    screen.blit(background, (0,0))
    print(pygame.mouse.get_pos())
