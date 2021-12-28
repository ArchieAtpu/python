import os
import pygame

def startGame(scenes, startingScene, screenSize):
    assert startingScene in scenes, f"The scene '{startingScene}' was not found."  # Ensures that the scene exists.

    # initialize variables
    gameGlobals = {}
    currentScene = scenes[startingScene]
    currentSceneState = {}

    # initialize pygame and pygame variables
    pygame.init()   
    screen = pygame.display.set_mode(screenSize)
    clock = pygame.time.Clock()

    running = True
    
    # Game Loop: Calls the current scene's subprogram each iteration and stores the 'state' between calls.
    while running:
        screen.fill((0,0,0)) # Clears the screen

        events = pygame.event.get()
        updateResult = currentScene(events, screen, currentSceneState, gameGlobals) # Calls the update subprogram

        if updateResult is not None:
            if not updateResult: # If False is returned, stop the program.
                running = False
            else: # Switches to the scene that was returned.
                assert updateResult in scenes, f"The scene '{updateResult}' was not found." # Ensures that the scene exists.
                currentScene = scenes[updateResult]
                currentSceneState = {}
           
        pygame.display.flip() # updates the screen
        clock.tick(60) # limits the fps to 60
