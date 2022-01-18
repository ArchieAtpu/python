import pygame 

background = pygame.image.load('./assets/titleBackground.png')

def titleScene(events, screen, state, globals):
    for event in events:
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            print(mousePos)

            if mousePos[0] > 231 and mousePos[0] < 425 and mousePos[1] > 676 and mousePos[1] < 741:
                return False
            elif mousePos[0] > 650 and mousePos[0] < 850 and mousePos[1] > 675 and mousePos[1] < 745:
                return "menu"

    screen.blit(background, (0,0))

