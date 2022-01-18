import pygame 

background = pygame.image.load('./assets/testSubmissionBackground.png')

def testSubmissionScene(events, screen, state, globals):
    for event in events:
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            print(mousePos)

            if mousePos[0] > 125 and mousePos[0] < 440 and mousePos[1] > 590 and mousePos[1] < 700:
                return "testMatching"
            elif mousePos[0] > 600 and mousePos[0] < 915 and mousePos[1] > 590 and mousePos[1] < 700:
                return "results"

    screen.blit(background, (0,0))

