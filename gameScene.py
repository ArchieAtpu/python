# import modules
import pygame
import math
import random

# load assets
spaceshipImg = pygame.transform.scale(pygame.image.load("./assets/spaceship.png"),(68,149))
asteroidImg = pygame.transform.scale(pygame.image.load("./assets/asteroids.png"),(190,150))

# define constants
ACCELERATION = 1
MAX_SPEED = 3
FRICTION = 0.99

ROTATION_ACCEL = 0.3
ROTATION_FRICTION = 0.965
MAX_ROTATION_SPEED = 3.5

ASTEROID_SPAWN_SLOWEST = 3 * 60
ASTEROID_SPAWN_FASTEST = 1 * 60
ASTEROID_MAX_SPEED = 4
ASTEROID_MIN_SPEED = 0.5

PLANETS = [ "mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune"]
planetImgs = {
    "mercury": pygame.image.load("./assets/spaceship.png"), 
    "venus": pygame.image.load("./assets/spaceship.png"), 
    "earth": pygame.image.load("./assets/spaceship.png"), 
    "mars": pygame.image.load("./assets/spaceship.png"), 
    "jupiter": pygame.image.load("./assets/spaceship.png"), 
    "saturn": pygame.image.load("./assets/spaceship.png"), 
    "uranus": pygame.image.load("./assets/spaceship.png"), 
    "neptune": pygame.image.load("./assets/spaceship.png")
}

SPACESHIP_HITBOXES = ( ((0, -15), 20), ((0, -40), 5), ((0, -55), 5), ((0, 15), 25), ((25, 25), 8), ((-25, 25), 8) )

BLASTER_BOLT_SPEED = 15
SHOOT_COOLDOWN = 0.7 * 60

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

    for boltState in state["blasterBolts"]: # update all blaster bolts
        updateBlasterBolt(screen, boltState, state)

# subprograms used in the scene
def initializeState(state):
    state["controls"] = { "up": False, "left": False, "down": False, "right": False }
    state["spaceship"] = { "pos": [500,400], "vel": [0,0], "angle": 0, "rotationVel": 0 }
    state["timeUntilAsteroid"] = 1 * 60
    state["asteroids"] = []
    state["missingPlanets"] = PLANETS
    state["blasterBolts"] = []
    state["shootCooldown"] = 0

def handleEvents(events, state):
    state["shootCooldown"] -= 1

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
            elif event.key == pygame.K_SPACE and state["shootCooldown"] < 1:
                angleInRadians = math.radians(state["spaceship"]["angle"] + 90)
                cosAngle = math.cos(angleInRadians)
                sinAngle = math.sin(angleInRadians)

                state["blasterBolts"].append({ "pos": [
                    state["spaceship"]["pos"][0] + cosAngle*54,
                    state["spaceship"]["pos"][1] - sinAngle*54,
                ], "vel": (
                    cosAngle * BLASTER_BOLT_SPEED, 
                    -sinAngle * BLASTER_BOLT_SPEED
                ) })

                state["shootCooldown"] = SHOOT_COOLDOWN

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
        state["spaceship"]["vel"][0] += ACCELERATION * math.cos(math.radians(state["spaceship"]["angle"] + 90))
        state["spaceship"]["vel"][1] -= ACCELERATION * math.sin(math.radians(state["spaceship"]["angle"] + 90))
    if state["controls"]["down"]:
        state["spaceship"]["vel"][0] -= ACCELERATION * math.cos(math.radians(state["spaceship"]["angle"] + 90)) * 0.1
        state["spaceship"]["vel"][1] += ACCELERATION * math.sin(math.radians(state["spaceship"]["angle"] + 90)) * 0.1
    if state["controls"]["left"]:
        state["spaceship"]["rotationVel"] += ROTATION_ACCEL
    if state["controls"]["right"]:
        state["spaceship"]["rotationVel"] -= ROTATION_ACCEL

    # decrease velocity gradually
    state["spaceship"]["vel"][0] *= FRICTION
    state["spaceship"]["vel"][1] *= FRICTION
    state["spaceship"]["rotationVel"] *= ROTATION_FRICTION 

    # limit the velocity and lower it if it is above the max
    if state["spaceship"]["vel"][0] > MAX_SPEED:
        state["spaceship"]["vel"][0] = MAX_SPEED
    elif state["spaceship"]["vel"][0] < -MAX_SPEED:
        state["spaceship"]["vel"][0] = -MAX_SPEED
    if state["spaceship"]["vel"][1] > MAX_SPEED:
        state["spaceship"]["vel"][1] = MAX_SPEED
    elif state["spaceship"]["vel"][1] < -MAX_SPEED:
        state["spaceship"]["vel"][1] = -MAX_SPEED
    if state["spaceship"]["rotationVel"] > MAX_ROTATION_SPEED:
        state["spaceship"]["rotationVel"] = MAX_ROTATION_SPEED
    elif state["spaceship"]["rotationVel"] < -MAX_ROTATION_SPEED:
        state["spaceship"]["rotationVel"] = -MAX_ROTATION_SPEED

    # move the spaceship according to the velocity
    state["spaceship"]["pos"][0] += state["spaceship"]["vel"][0]
    state["spaceship"]["pos"][1] += state["spaceship"]["vel"][1]
    state["spaceship"]["angle"] += state["spaceship"]["rotationVel"]
   
    shipCenter = spaceshipImg.get_rect(topleft=state["spaceship"]["pos"]).center
    rotatedImg = pygame.transform.rotate(spaceshipImg,state["spaceship"]["angle"])
    
    newPos = (state["spaceship"]["pos"][0] - rotatedImg.get_width()/2, state["spaceship"]["pos"][1] - rotatedImg.get_height()/2)
    #pygame.draw.circle(screen,(255,255,255),shipCenter,300)
    # draw the spaceship
    screen.blit(rotatedImg, newPos)

    for offset, size in SPACESHIP_HITBOXES:
        translatedPos = (state["spaceship"]["pos"][0] + offset[0], state["spaceship"]["pos"][1] + offset[1])
        rotatedPos = rotatePointAroundPivot(translatedPos, state["spaceship"]["pos"], -state["spaceship"]["angle"])
        #pygame.draw.circle(screen, (255,0,0), rotatedPos, size)

        for asteroid in state["asteroids"]:
            center = (asteroid["pos"][0] + 94, asteroid["pos"][1] + 76)

            if circleCircleCollision(rotatedPos, size, center, 56):
                print("hit")

def rotatePointAroundPivot(point, pivot, angle):
    """Takes an angle in degrees. I figured out the maths for this myself!!!!"""

    distance = math.hypot(point[0] - pivot[0], point[1] - pivot[1])
    angleToPoint = math.atan2(point[1] - pivot[1], point[0] - pivot[0])

    newAngle = math.radians(angle) + angleToPoint
    newPoint = list(point)
    newPoint[0] = pivot[0] + math.cos(newAngle) * distance
    newPoint[1] = pivot[1] + math.sin(newAngle) * distance

    return newPoint

def circleCircleCollision(pos1, radius1, pos2, radius2):
    return math.hypot(pos1[0] - pos2[0], pos1[1] - pos2[1]) < radius1 + radius2

def handleAsteroidSpawning(state):
    state["timeUntilAsteroid"] -= 1

    if state["timeUntilAsteroid"] == 0:
        state["timeUntilAsteroid"] = random.randint(ASTEROID_SPAWN_FASTEST, ASTEROID_SPAWN_SLOWEST)

        while True:
            spawnPos, asteroidVel = generateAsteroidSpawn()

            # if the spawn position is too close to the player, try again; otherwise, break from the loop
            if pygame.math.Vector2(spawnPos[0], -spawnPos[1]).distance_to((state["spaceship"]["pos"][0], -state["spaceship"]["pos"][1])) > 300:
                break

        planet = None

        if state["missingPlanets"] and random.random() < 0.2:
            for i in range(3):
                planetChoice = random.choice(PLANETS)

                if planetChoice in state["missingPlanets"]:
                    planet = planetChoice
                    print(planet)
                    break

        state["asteroids"].append({ "pos": spawnPos, "vel": asteroidVel, "planet": planet }) # adds a new asteroid

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

    if asteroidState["pos"][0] > 2000 or asteroidState["pos"][0] < -1000 or \
        asteroidState["pos"][1] > 2000 or asteroidState["pos"][1] < -1000:
        state["asteroids"].remove(asteroidState) # deletes the asteroid
    else:
        #pygame.draw.circle(screen, (255,0,0), (asteroidState["pos"][0] + 94, asteroidState["pos"][1] + 76), 56)
        # draws the asteroid
        if asteroidState["planet"]:
            screen.blit(planetImgs[asteroidState["planet"]], asteroidState["pos"])
        else:
            screen.blit(asteroidImg, asteroidState["pos"])

def updateBlasterBolt(screen, boltState, state):
    boltState["pos"][0] += boltState["vel"][0]
    boltState["pos"][1] += boltState["vel"][1]

    if boltState["pos"][0] > 2000 or boltState["pos"][0] < -1000 or \
        boltState["pos"][1] > 2000 or boltState["pos"][1] < -1000:
        state["blasterBolts"].remove(boltState) # deletes the asteroid
    else:
        pygame.draw.circle(screen, (255,0,0), boltState["pos"], 5)
        # draws the blaster bolt
        #screen.blit(asteroidImg, asteroidState["pos"])
