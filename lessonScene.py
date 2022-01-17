import pygame 

background = pygame.image.load('./assets/lessonsBackground/lessonBackground.png')

def lessonScene(events, screen, state, globals):
  for event in events:
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
          mousePos = pygame.mouse.get_pos()
          
          if mousePos[0] > 330 and mousePos[0] < 742 and mousePos[1] > 269 and mousePos[1] < 308:
            return 'Sun'
          elif mousePos[0] > 330 and mousePos[0] < 742 and mousePos[1] > 327 and mousePos[1] < 358:
            return 'Inner/Outer Planets'  
          elif mousePos[0] > 330 and mousePos[0] < 742 and mousePos[1] > 373 and mousePos[1] < 405:
            return 'Mercury/Venus'   
          elif mousePos[0] > 330 and mousePos[0] < 742 and mousePos[1] > 421 and mousePos[1] < 453:
            return 'Earth/Mars'     
          elif mousePos[0] > 330 and mousePos[0] < 742 and mousePos[1] > 471 and mousePos[1] < 500:
            return 'Jupiter/Saturn'    
          elif mousePos[0] > 330 and mousePos[0] < 742 and mousePos[1] > 523 and mousePos[1] < 552:
            return 'Uranus/Neptune'
          elif mousePos[0] > 330 and mousePos[0] < 742 and mousePos[1] > 575 and mousePos[1] < 601:
            return 'Dwarf Planets'
          elif mousePos[0] > 330 and mousePos[0] < 742 and mousePos[1] > 619 and mousePos[1] < 649:
            return 'Dwarf Planets2'
    
            
  screen.blit(background, (0,0))



