import pygame 

background = pygame.image.load('./assets/lessonsBackground/lessonPlanets.png')

def lessonInnerOuterPlanets(events, screen, state, globals):
    for event in events:
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            if mousePos[0] > 14 and mousePos[0] < 91 and mousePos[1] > 692 and mousePos[1] < 762:
                return "menu"
            elif mousePos[0] > 827 and mousePos[0] < 1004 and mousePos[1] > 693 and mousePos[1] < 753:
                return "Mercury/Venus"

    screen.blit(background, (0,0))