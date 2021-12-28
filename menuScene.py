import pygame

# load all of the images in the animation using a counted loop
menuBackgroundImgs = [ pygame.transform.scale(pygame.image.load(f"./assets/menuBackgroundImgs/{i}.png"), (768,576)) for i in range(71) ]

def menuScene(events, screen, state, globals):
    # code for the menu goes here
    # store persistent variables in the state
    # store global variables in globals
    # return False to stop the program
    # return the name of another scene to switch scenes

    if not state: # initializes the state if it is empty
        state["backgroundFrame"] = 0
        state["framesToNewBackground"] = 1
    
    for event in events:
        if event.type == pygame.QUIT:
            return False

    updateBackground(screen, state)

    # do this to go to the game scene: return "game"

def updateBackground(screen, state):
    if state["backgroundFrame"] < 70:
        state["framesToNewBackground"] -= 1
        if state["framesToNewBackground"] == 0:
            state["framesToNewBackground"] = 4

            state["backgroundFrame"] += 1
    
    screen.blit(menuBackgroundImgs[state["backgroundFrame"]], (0,0))