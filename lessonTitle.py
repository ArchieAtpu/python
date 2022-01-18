import pygame

mousePos = pygame.mouse.get_pos()


def lessonScene (events, screen, state, globals):  
  if mousePos[0] > 742 and mousePos[0] < 330 and mousePos[1] < 330 and mousePos[1] > 308:
    return "Sun"
  if mousePos[0] > 742 and mousePos[0] < 327 and mousePos[1] < 330 and mousePos[1] > 358:
    return "Inner/Outer Planets"
  if mousePos[0] > 742 and mousePos[0] < 373 and mousePos[1] < 330 and mousePos[1] > 405:
    return "Mercury/Venus"
  if mousePos[0] > 742 and mousePos[0] < 421 and mousePos[1] < 330 and mousePos[1] > 453:
    return "Earth/Mars"
  if mousePos[0] > 742 and mousePos[0] < 471 and mousePos[1] < 330 and mousePos[1] > 500:
    return "Jupiter/Saturn"
  if mousePos[0] > 742 and mousePos[0] < 523 and mousePos[1] < 330 and mousePos[1] > 552:
    return "Uranus/Neptune"
  if mousePos[0] > 742 and mousePos[0] < 575 and mousePos[1] < 330 and mousePos[1] > 601:
    return "Dwarf Planets"
  if mousePos[0] > 742 and mousePos[0] < 619 and mousePos[1] < 330 and mousePos[1] > 649:
    return "Stars"
