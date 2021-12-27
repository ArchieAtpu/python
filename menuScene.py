import pygame

def menuScene(events, screen, state, globals):
        pygame.init()
    screen = pygame.display.set_mode((1000, 500))

    running = True
    while running:

        for event in pygame.event.get():
            ...
    
        screen.blit(screen, (0, 0))

        pygame.display.update()

    for event in events:
        if event.type == pygame.QUIT:
            return False
