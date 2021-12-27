# import modules
import pygame
import math
import random

# load assets
spaceshipImg = pygame.transform.scale(pygame.image.load("./assets/demoship.png"),(70,110))
asteroidImg = pygame.transform.scale(pygame.image.load("./assets/demoAsteroid.jpg"),(150,150))

# define constants
ACCELERATION = 0.3
MAX_SPEED = 5
FRICTION = 0.99

ASTEROID_SPAWN_SLOWEST = 3 * 60
ASTEROID_SPAWN_FASTEST = 1 * 60
ASTEROID_MAX_SPEED = 4
ASTEROID_MIN_SPEED = 0.5

# main scene subprogram
def gameScene(events, screen, state, globals):
    if not state: # initialize the state if it is empty
        initializeState(state)

    if handleEvents(events, state) == False:
        return False # exits the program

    updateSpaceship(screen, state)
    handleAsteroidSpawning(state)
    
    for asteroidState in state["asteroids"]: # update all asteroids
        updateAsteroid(screen, asteroidState, state)

# subprograms used in the scene
def initializeState(state):
    state["controls"] = { "up": False, "left": False, "down": False, "right": False }
    state["spaceship"] = { "pos": [0,0], "vel": [0,0] }
    state["timeUntilAsteroid"] = 10 * 60
    state["asteroids"] = []

def handleEvents(events, state):
    for event in events:
        if event.type == pygame.QUIT:
            return False # exits the program

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

def updateSpaceship(screen, state):
    # increase velocity according to user input
    if state["controls"]["up"]:
        state["spaceship"]["vel"][1] -= ACCELERATION
    if state["controls"]["left"]:
        state["spaceship"]["vel"][0] -= ACCELERATION
    if state["controls"]["down"]:
        state["spaceship"]["vel"][1] += ACCELERATION
    if state["controls"]["right"]:
        state["spaceship"]["vel"][0] += ACCELERATION

    # decrease velocity gradually
    state["spaceship"]["vel"][0] *= FRICTION
    state["spaceship"]["vel"][1] *= FRICTION

    # limit the velocity and lower it if it is above the max
    if state["spaceship"]["vel"][0] > MAX_SPEED:
        state["spaceship"]["vel"][0] = MAX_SPEED
    elif state["spaceship"]["vel"][0] < -MAX_SPEED:
        state["spaceship"]["vel"][0] = -MAX_SPEED
    if state["spaceship"]["vel"][1] > MAX_SPEED:
        state["spaceship"]["vel"][1] = MAX_SPEED
    elif state["spaceship"]["vel"][1] < -MAX_SPEED:
        state["spaceship"]["vel"][1] = -MAX_SPEED

    # move the spaceship according to the velocity
    state["spaceship"]["pos"][0] += state["spaceship"]["vel"][0]
    state["spaceship"]["pos"][1] += state["spaceship"]["vel"][1]

    # rotate the ship and its hitbox to face the mouse
    mousePos = pygame.mouse.get_pos()
    shipCenter = spaceshipImg.get_rect(topleft=state["spaceship"]["pos"]).center
    angle = 270 - math.atan2(mousePos[1] - shipCenter[1], mousePos[0] - shipCenter[0])*180/math.pi
    rotatedImg = pygame.transform.rotate(spaceshipImg,angle)
    newRect = rotatedImg.get_rect(center=shipCenter)
    
    # draw the spaceship
    screen.blit(rotatedImg, newRect)

def handleAsteroidSpawning(state):
    state["timeUntilAsteroid"] -= 1

    if state["timeUntilAsteroid"] == 0:
        state["timeUntilAsteroid"] = random.randint(ASTEROID_SPAWN_FASTEST, ASTEROID_SPAWN_SLOWEST)

        while True:
            spawnPos, asteroidVel = generateAsteroidSpawn()

            # if the spawn position is too close to the player, try again; otherwise, break from the loop
            if pygame.math.Vector2(spawnPos[0], -spawnPos[1]).distance_to((state["spaceship"]["pos"][0], -state["spaceship"]["pos"][1])) > 200:
                break
        
        state["asteroids"].append({ "pos": spawnPos, "vel": asteroidVel }) # adds a new asteroid

def generateAsteroidSpawn():
    """Asteroids are spawned on one of the four edges of the screen."""

    spawnLen = random.randint(0,800) # the distance along the edge that the asteroid will be spawned    
    asteroidVel = [random.uniform(ASTEROID_MIN_SPEED,ASTEROID_MAX_SPEED),random.uniform(ASTEROID_MIN_SPEED,ASTEROID_MAX_SPEED)]

    if random.random() > 0.5: # spawns asteroid on the top or bottom edge
        if random.random() > 0.5: # spawns asteroid on the bottom edge
            spawnPos = [spawnLen, 830]
            asteroidVel[1] *= -1
        else: # spawns asteroid on the top edge
            spawnPos = [spawnLen, -30]

        if random.random() > 0.5: # makes the asteroid drift to the left instead of to the right
            asteroidVel[0] *= -1
    else: # spawns asteroid on the left or right edge
        if random.random() > 0.5: # spawns asteroid on the right edge
            spawnPos = [830, spawnLen]
            asteroidVel[0] *= -1
        else: # spawns asteroid on the left edge
            spawnPos = [-30, spawnLen]

        if random.random() > 0.5: # makes the asteroid drift to up instead of down
            asteroidVel[1] *= -1

    return spawnPos, asteroidVel

def updateAsteroid(screen, asteroidState, state):
    # moves the asteroid according to its velocity
    asteroidState["pos"][0] += asteroidState["vel"][0]
    asteroidState["pos"][1] += asteroidState["vel"][1]

    # draws the asteroid
    screen.blit(asteroidImg, asteroidState["pos"])