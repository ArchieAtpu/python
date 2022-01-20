import pygame 

background = pygame.image.load('./assets/winBackground.png')

def winScene(events, screen, state, globals):
    for event in events:
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            print(mousePos)

            if mousePos[0] > 330 and mousePos[0] < 715 and mousePos[1] > 585 and mousePos[1] < 716:
                globals["gameCompleted"] = True
                if "missingPlanets" in globals:
                    del globals["missingPlanets"]
                return "menu"

    screen.blit(background, (0,0))