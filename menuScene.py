import pygame

# load all of the images in the animation using a counted loop
menuBackgroundImgs = [ pygame.image.load(f"./assets/menuBackground/{i}.png") for i in range(71) ]

def menuScene(events, screen, state, globals):
    # code for the menu goes here
    # store persistent variables in the state
    # store global variables in globals
    # return False to stop the program
    # return the name of another scene to switch scenes

    for event in events:
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            print(mousePos)

            if mousePos[0] > 565 and mousePos[0] < 885 and mousePos[1] > 385 and mousePos[1] < 495:
                return False
            elif mousePos[0] > 135 and mousePos[0] < 455 and mousePos[1] > 385 and mousePos[1] < 495:
                return "game"
            elif mousePos[0] > 385 and mousePos[0] < 645 and mousePos[1] > 525 and mousePos[1] < 615:
                return "testStart"
            elif mousePos[0] > 720 and mousePos[0] < 975 and mousePos[1] > 575 and mousePos[1] < 665:
                if "userAnswers" in globals:
                    return "results"
                else:
                    return "testUncompleted"
            elif mousePos[0] > 60 and mousePos[0] < 302 and mousePos[1] > 557 and mousePos[1] < 657:
              return 'lesson'
            elif mousePos[0] > 388 and mousePos[0] < 640 and mousePos[1] > 657 and mousePos[1] < 743:
                return "credits"

            # the other buttons do not work yet

    if not state: # initializes the state if it is empty
        state["backgroundFrame"] = 0
        state["framesToNewBackground"] = 1


    updateBackground(screen, state)

    # do this to go to the game scene: return "game"

def updateBackground(screen, state):
    if state["backgroundFrame"] < 70:
        state["framesToNewBackground"] -= 1
        if state["framesToNewBackground"] == 0:
            state["framesToNewBackground"] = 3

            state["backgroundFrame"] += 1
    
    screen.blit(menuBackgroundImgs[state["backgroundFrame"]], (0,0))
