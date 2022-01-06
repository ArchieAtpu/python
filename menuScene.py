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

            if mousePos[0] > 565 and mousePos[0] < 885 and mousePos[1] > 385 and mousePos[1] < 495:
                return False
            if mousePos[0] > 135 and mousePos[0] < 455 and mousePos[1] > 385 and mousePos[1] < 495:
                return "game"

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
            state["framesToNewBackground"] = 4

            state["backgroundFrame"] += 1
    
    screen.blit(menuBackgroundImgs[state["backgroundFrame"]], (0,0))
