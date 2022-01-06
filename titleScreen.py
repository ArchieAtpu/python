import pygame 

pygame.init()

width = 1024
height = 768
screen = pygame.display.set_mode((width, height))

background = pygame.image.load('background_title.png')


def titleScene(events, screen, state, globals):
  for event in events:
    if event.type == pygame.QUIT:
      return False
    if event.type == pygame.MOUSEBUTTONUP:
      pos = pygame.mouse.get_pos()
      if pos[0] > 231 and pos[0] < 676 and pos[1] < 741 and pos[1] > 676:
        return 'menu'

  screen.blit(background, (0,0))
  print(pygame.mouse.get_pos())

