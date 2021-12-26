import os
import pygame

def startGame(scenes, startingScene):
    assert startingScene in scenes, f"The scene '{startingScene}' was not found."
    gameGlobals = {}
    currentScene = scenes[startingScene]
    currentSceneState = {}

    pygame.init()   
    screen = pygame.display.set_mode((800,800))
    clock = pygame.time.Clock()

    running = True
    
    while running:
        screen.fill((0,0,0))

        events = pygame.event.get()
        updateResult = currentScene(events, screen, currentSceneState, gameGlobals)

        if updateResult is not None:
            if not updateResult: # If False is returned, stop the program.
                running = False
            else: # Switches to the scene that was returned.
                assert updateResult in scenes, f"The scene '{updateResult}' was not found." # Ensures that the scene exists.
                currentScene = scenes[updateResult]
                currentSceneState = {}
                    
        pygame.display.flip()
        clock.tick(60)
