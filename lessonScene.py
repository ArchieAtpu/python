import pygame 

background = pygame.image.load('./assets/lessonBackground.png')

def lessonScene(events, screen, state, globals):
  for event in events:
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
          mousePos = pygame.mouse.get_pos()
          
          if event.type == pygame.MOUSEBUTTONUP:
            if mousePos[0] > 231 and mousePos[0] < 676 and mousePos[1] < 741 and mousePos[1] > 676:
              return 'lesson'
  screen.blit(background, (0,0))
  print(pygame.mouse.get_pos())
