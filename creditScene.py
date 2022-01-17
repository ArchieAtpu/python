import pygame 

background = pygame.image.load('./assets/creditsBackground.png')

def creditsScene(events, screen, state, globals):
    for event in events:
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            if mousePos[0] > 388 and mousePos[0] < 640 and mousePos[1] > 657 and mousePos[1] < 743:
                return "credits"

    screen.blit(background, (0,0))
    print(pygame.mouse.get_pos())