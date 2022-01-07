import pygame

# load all of the images in the animation using a counted loop
backgroundImgs = [ pygame.image.load(f"./assets/testStartBackground/{i}.png") for i in range(40) ]

def testStartScene(events, screen, state, globals):

    for event in events:
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            print(mousePos)

            if mousePos[0] > 350 and mousePos[0] < 675 and mousePos[1] > 580 and mousePos[1] < 695:
                return "testMultChoice"

    if not state: # initializes the state if it is empty
        state["backgroundFrame"] = 0
        state["framesToNewBackground"] = 1

    updateBackground(screen, state)

def updateBackground(screen, state):
    if state["backgroundFrame"] < 39:
        state["framesToNewBackground"] -= 1
        if state["framesToNewBackground"] == 0:
            state["framesToNewBackground"] = 4

            state["backgroundFrame"] += 1
    
    screen.blit(backgroundImgs[state["backgroundFrame"]], (0,0))