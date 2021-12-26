import pygame

def menuScene(events, screen, state, globals):
    # code for the menu goes here
    # store persistent variables in the state
    # store global variables in globals
    # return False to stop the program
    # return the name of another scene to switch scenes
    
    for event in events:
        if event.type == pygame.QUIT:
            return False