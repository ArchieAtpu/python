import pygame

# load all of the images in the animation using a counted loop
backgroundImgs = [ pygame.image.load(f"./assets/testStartBackground/{i}.png") for i in range(46) ]

def testStartScene(events, screen, state, globals):

    for event in events:
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            print(mousePos)

            if mousePos[0] > 604 and mousePos[0] < 916 and mousePos[1] > 590 and mousePos[1] < 700:
                globals["userAnswers"] = None
                globals["showTestAnswers"] = False
                globals["userMatchingAnswers"] = [ None, None, None, None ]
                return "testMultChoice"
            elif mousePos[0] > 125 and mousePos[0] < 440 and mousePos[1] > 590 and mousePos[1] < 700:
                return "menu"

    if not state: # initializes the state if it is empty
        state["backgroundFrame"] = 0
        state["framesToNewBackground"] = 1

    updateBackground(screen, state)

def updateBackground(screen, state):
    if state["backgroundFrame"] < 45:
        state["framesToNewBackground"] -= 1
        if state["framesToNewBackground"] == 0:
            state["framesToNewBackground"] = 3

            state["backgroundFrame"] += 1
    
    screen.blit(backgroundImgs[state["backgroundFrame"]], (0,0))