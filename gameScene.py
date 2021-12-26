import pygame
import math

spaceshipImg = pygame.transform.scale(pygame.image.load("./assets/demoship.png"),(50,80))
ACCELERATION = 0.3
MAX_SPEED = 5
FRICTION = 0.99

def gameScene(events, screen, state, globals):
    if not state:
        state["controls"] = { "up": False, "left": False, "down": False, "right": False }
        state["spaceship"] = { "pos": [0,0], "vel": [0,0] }

    for event in events:
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                state["controls"]["up"] = True
            elif event.key == pygame.K_a:
                state["controls"]["left"] = True
            elif event.key == pygame.K_s:
                state["controls"]["down"] = True
            elif event.key == pygame.K_d:
                state["controls"]["right"] = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                state["controls"]["up"] = False
            elif event.key == pygame.K_a:
                state["controls"]["left"] = False
            elif event.key == pygame.K_s:
                state["controls"]["down"] = False
            elif event.key == pygame.K_d:
                state["controls"]["right"] = False

    if state["controls"]["up"]:
        state["spaceship"]["vel"][1] -= ACCELERATION
    if state["controls"]["left"]:
        state["spaceship"]["vel"][0] -= ACCELERATION
    if state["controls"]["down"]:
        state["spaceship"]["vel"][1] += ACCELERATION
    if state["controls"]["right"]:
        state["spaceship"]["vel"][0] += ACCELERATION

    state["spaceship"]["vel"][0] *= FRICTION
    state["spaceship"]["vel"][1] *= FRICTION

    if state["spaceship"]["vel"][0] > MAX_SPEED:
        state["spaceship"]["vel"][0] = MAX_SPEED
    elif state["spaceship"]["vel"][0] < -MAX_SPEED:
        state["spaceship"]["vel"][0] = -MAX_SPEED
    if state["spaceship"]["vel"][1] > MAX_SPEED:
        state["spaceship"]["vel"][1] = MAX_SPEED
    elif state["spaceship"]["vel"][1] < -MAX_SPEED:
        state["spaceship"]["vel"][1] = -MAX_SPEED

    state["spaceship"]["pos"][0] += state["spaceship"]["vel"][0]
    state["spaceship"]["pos"][1] += state["spaceship"]["vel"][1]

    drawSpaceship(screen, state["spaceship"]["pos"], pygame.mouse.get_pos())

def drawSpaceship(screen, pos, mousePos):
    shipCenter = spaceshipImg.get_rect(topleft=pos).center
    angle = 270 - math.atan2(mousePos[1] - shipCenter[1], mousePos[0] - shipCenter[0])*180/math.pi
    rotatedImg = pygame.transform.rotate(spaceshipImg,angle)
    newRect = rotatedImg.get_rect(center=shipCenter)
    screen.blit(rotatedImg, newRect)