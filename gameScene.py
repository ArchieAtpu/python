# import modules
import pygame
import math
import random

# load assets
spaceshipImg = pygame.transform.scale(pygame.image.load("./assets/spaceship.png"),(68,149))
asteroidImg = pygame.transform.scale(pygame.image.load("./assets/asteroids.png"),(190,150))
backgroundImg = pygame.image.load("./assets/gameBackground.png")

explosionImgs = [ pygame.transform.scale(pygame.image.load(f"./assets/explosion/{i}.png"),(190,150)) for i in range(7) ]

# define constants
ACCELERATION = 1
MAX_SPEED = 3.3
FRICTION = 0.99

ROTATION_ACCEL = 0.32
ROTATION_FRICTION = 0.965
MAX_ROTATION_SPEED = 3.5

ASTEROID_SPAWN_SLOWEST = 3 * 60
ASTEROID_SPAWN_FASTEST = 1 * 60
ASTEROID_MAX_SPEED = 4
ASTEROID_MIN_SPEED = 0.5

PLANETS = [ "mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune"]
planetImgs = {
    "mercury": pygame.image.load("./assets/planets/mercury.png"), 
    "venus": pygame.image.load("./assets/planets/venus.png"), 
    "earth": pygame.image.load("./assets/planets/earth.png"), 
    "mars": pygame.image.load("./assets/planets/mars.png"), 
    "jupiter": pygame.image.load("./assets/planets/jupiter.png"), 
    "saturn": pygame.image.load("./assets/planets/saturn.png"), 
    "uranus": pygame.image.load("./assets/planets/uranus.png"), 
    "neptune": pygame.image.load("./assets/planets/neptune.png")
}

planetCardImgs = {
    "mercury": pygame.image.load("./assets/planetCards/mercury.png"), 
    "venus": pygame.image.load("./assets/planetCards/venus.png"), 
    "earth": pygame.image.load("./assets/planetCards/earth.png"), 
    "mars": pygame.image.load("./assets/planetCards/mars.png"), 
    "jupiter": pygame.image.load("./assets/planetCards/jupiter.png"), 
    "saturn": pygame.image.load("./assets/planetCards/saturn.png"), 
    "uranus": pygame.image.load("./assets/planetCards/uranus.png"), 
    "neptune": pygame.image.load("./assets/planetCards/neptune.png")
}

pauseMenuImg = pygame.transform.scale(pygame.image.load("./assets/pauseMenu.png"), (1024, 768))

SPACESHIP_HITBOXES = ( ((0, -15), 20), ((0, -40), 5), ((0, -55), 5), ((0, 15), 25), ((25, 25), 8), ((-25, 25), 8) )

BLASTER_BOLT_SPEED = 15
SHOOT_COOLDOWN = 0.7 * 60

ASTEROID_HITBOX = ((94, 76), 56)
PLANET_SIZES = { "mercury": 63, "venus": 77, "earth": 89, "mars": 75, "jupiter": 130, "saturn": 112, "uranus": 95, "neptune": 97 }

# main scene subprogram
def gameScene(events, screen, state, globals):
    if not state: # initialize the state if it is empty
        initializeState(state)

    if handleEvents(events, state) == False:
        return False # exits the program

    if not state["paused"]:
        updateSpaceship(screen, state)
        handleAsteroidSpawning(state)
        
        for asteroidState in state["asteroids"]: # update all asteroids
            updateAsteroid(screen, asteroidState, state)

        for boltState in state["blasterBolts"]: # update all blaster bolts
            updateBlasterBolt(screen, boltState, state)

    draw(screen, state)

# subprograms used in the scene
def initializeState(state):
    state["controls"] = { "up": False, "left": False, "down": False, "right": False }
    state["spaceship"] = { "pos": [500,400], "vel": [0,0], "angle": 0, "rotationVel": 0, "exploding": None, "framesUntilNext": 3 }
    state["timeUntilAsteroid"] = 1 * 60
    state["asteroids"] = []
    state["missingPlanets"] = PLANETS.copy()
    state["blasterBolts"] = []
    state["shootCooldown"] = 0
    state["paused"] = False
    state["planetCard"] = None

def handleEvents(events, state):
    state["shootCooldown"] -= 1

    for event in events:
        if event.type == pygame.QUIT:
            return False # exits the program

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                state["controls"]["up"] = True
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                state["controls"]["left"] = True
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                state["controls"]["down"] = True
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                state["controls"]["right"] = True
            elif event.key == pygame.K_SPACE and state["shootCooldown"] < 1 and not state["paused"]:
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
            elif event.key == pygame.K_ESCAPE:
                if state["paused"]:
                    state["paused"] = False
                    state["planetCard"] = None
                else:
                    state["paused"] = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                state["controls"]["up"] = False
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                state["controls"]["left"] = False
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                state["controls"]["down"] = False
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                state["controls"]["right"] = False
    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            print(mousePos)

            if state["paused"]:
                if state["planetCard"]:
                    if mousePos[0] > 615 and mousePos[0] < 635 and mousePos[1] > 235 and mousePos[1] < 260:
                        state["planetCard"] = None
                        state["paused"] = False
                else:
                    if mousePos[0] > 354 and mousePos[0] < 670 and mousePos[1] > 430 and mousePos[1] < 540:
                        state["paused"] = False
                    
def updateSpaceship(screen, state):
    if state["spaceship"]["exploding"] != None:
        if state["spaceship"]["exploding"] > 20:
            state["spaceship"] = { "pos": [500,400], "vel": [0,0], "angle": 0, "rotationVel": 0, "exploding": None, "framesUntilNext": 3 }
            state["asteroids"] = []
            state["blasterBolts"] = []
            return

        state["spaceship"]["framesUntilNext"] -= 1

        if state["spaceship"]["framesUntilNext"] < 1:
            state["spaceship"]["framesUntilNext"] = 3
            state["spaceship"]["exploding"] += 1

        return

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

    if state["spaceship"]["pos"][0] < -70:
        state["spaceship"]["pos"][0] = 1094
    elif state["spaceship"]["pos"][0] > 1094:
        state["spaceship"]["pos"][0] = -70

    if state["spaceship"]["pos"][1] < -70:
        state["spaceship"]["pos"][1] = 838
    elif state["spaceship"]["pos"][1] > 838:
        state["spaceship"]["pos"][1] = -70

    for offset, size in SPACESHIP_HITBOXES:
        translatedPos = (state["spaceship"]["pos"][0] + offset[0], state["spaceship"]["pos"][1] + offset[1])
        rotatedPos = rotatePointAroundPivot(translatedPos, state["spaceship"]["pos"], -state["spaceship"]["angle"])
        #pygame.draw.circle(screen, (255,0,0), rotatedPos, size)

        for asteroid in state["asteroids"]:
            if asteroid["exploding"]:
                continue

            center, asteroidSize = getAsteroidHitbox(asteroid)

            if circleCircleCollision(rotatedPos, size, center, asteroidSize):
                print("hit")
                state["spaceship"]["exploding"] = 0

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
            for i in range(2):
                planetChoice = random.choice(PLANETS)

                if planetChoice in state["missingPlanets"]:
                    planet = planetChoice
                    print(planet)
                    break

        state["asteroids"].append({ "pos": spawnPos, "vel": asteroidVel, "planet": planet, 
            "exploding": None, "framesUntilNext": 3 }) # adds a new asteroid

def generateAsteroidSpawn():
    """Asteroids are spawned on one of the four edges of the screen."""

    spawnLen = random.randint(68,700) # the distance along the edge that the asteroid will be spawned    
    asteroidVel = [random.uniform(ASTEROID_MIN_SPEED,ASTEROID_MAX_SPEED),random.uniform(ASTEROID_MIN_SPEED,ASTEROID_MAX_SPEED)]

    if random.random() > 0.5: # spawns asteroid on the top or bottom edge
        if random.random() > 0.5: # spawns asteroid on the bottom edge
            spawnPos = [spawnLen, 868]
            asteroidVel[1] *= -1
        else: # spawns asteroid on the top edge
            spawnPos = [spawnLen, -150]

        if random.random() > 0.5: # makes the asteroid drift to the left instead of to the right
            asteroidVel[0] *= -1
    else: # spawns asteroid on the left or right edge
        if random.random() > 0.5: # spawns asteroid on the right edge
            spawnPos = [1124, spawnLen]
            asteroidVel[0] *= -1
        else: # spawns asteroid on the left edge
            spawnPos = [-150, spawnLen]

        if random.random() > 0.5: # makes the asteroid drift to up instead of down
            asteroidVel[1] *= -1

    return spawnPos, asteroidVel

def updateAsteroid(screen, asteroidState, state):

    if asteroidState["exploding"] != None:
        if asteroidState["exploding"] > 10:
            if asteroidState["planet"]:
                try:
                    state["missingPlanets"].remove(asteroidState["planet"])

                    print("found " + asteroidState["planet"])
                    state["paused"] = True
                    state["planetCard"] = asteroidState["planet"]
                except ValueError:
                    pass

            state["asteroids"].remove(asteroidState) # deletes the asteroid
            return

        asteroidState["framesUntilNext"] -= 1

        if asteroidState["framesUntilNext"] < 1:
            asteroidState["framesUntilNext"] = 3
            asteroidState["exploding"] += 1

        return

    # moves the asteroid according to its velocity
    asteroidState["pos"][0] += asteroidState["vel"][0]
    asteroidState["pos"][1] += asteroidState["vel"][1]

    if asteroidState["pos"][0] > 2000 or asteroidState["pos"][0] < -1000 or \
        asteroidState["pos"][1] > 2000 or asteroidState["pos"][1] < -1000:
        state["asteroids"].remove(asteroidState) # deletes the asteroid
        return


    #pygame.draw.circle(screen, (255,0,0), (asteroidState["pos"][0] + 94, asteroidState["pos"][1] + 76), 56)
    center, size = getAsteroidHitbox(asteroidState)

    #pygame.draw.circle(screen, (0,255,0), center, size)
    for bolt in state["blasterBolts"]:

        if circleCircleCollision(bolt["pos"], 5, center, size):
            print("boom")
            asteroidState["exploding"] = 0
            state["blasterBolts"].remove(bolt) # deletes the blaster bolt

def getAsteroidHitbox(asteroidState):
    if asteroidState["planet"]:
        center = (asteroidState["pos"][0] + planetImgs[asteroidState["planet"]].get_width() / 2, 
            asteroidState["pos"][1] + planetImgs[asteroidState["planet"]].get_height() / 2)
        size = PLANET_SIZES[asteroidState["planet"]]
    else:
        center = (asteroidState["pos"][0] + ASTEROID_HITBOX[0][0], asteroidState["pos"][1] + ASTEROID_HITBOX[0][1])
        size = ASTEROID_HITBOX[1]
    
    return center, size

def updateBlasterBolt(screen, boltState, state):
    boltState["pos"][0] += boltState["vel"][0]
    boltState["pos"][1] += boltState["vel"][1]

    if boltState["pos"][0] > 2000 or boltState["pos"][0] < -1000 or \
        boltState["pos"][1] > 2000 or boltState["pos"][1] < -1000:
        state["blasterBolts"].remove(boltState) # deletes the blaster bolt
        return

def draw(screen, state):
    screen.blit(backgroundImg, (0,0))

    # draw the spaceship
    if state["spaceship"]["exploding"] != None:
        if state["spaceship"]["exploding"] > 5:
            frame = explosionImgs[6]
        else:
            frame = explosionImgs[state["spaceship"]["exploding"]]

        screen.blit(frame, state["spaceship"]["pos"])
    else:
        rotatedImg = pygame.transform.rotate(spaceshipImg,state["spaceship"]["angle"])
        newPos = (state["spaceship"]["pos"][0] - rotatedImg.get_width()/2, state["spaceship"]["pos"][1] - rotatedImg.get_height()/2)
        #pygame.draw.circle(screen,(255,255,255),shipCenter,300)
        screen.blit(rotatedImg, newPos)

    # draw the asteroids
    for asteroidState in state["asteroids"]:
        if asteroidState["exploding"] != None:
            if asteroidState["exploding"] > 5:
                frame = explosionImgs[6]
            else:
                frame = explosionImgs[asteroidState["exploding"]]

            if asteroidState["planet"]:
                planetImg = planetImgs[asteroidState["planet"]]
                frame = pygame.transform.scale(frame, (planetImg.get_width(), planetImg.get_height()))

            screen.blit(frame, asteroidState["pos"])
        else:
            if asteroidState["planet"]:
                screen.blit(planetImgs[asteroidState["planet"]], asteroidState["pos"])
            else:
                screen.blit(asteroidImg, asteroidState["pos"])

    for boltState in state["blasterBolts"]:
        pygame.draw.circle(screen, (255, 0, 0), boltState["pos"], 5) # draws the blaster bolt

    if state["paused"]:
        if state["planetCard"]:
            screen.blit(planetCardImgs[state["planetCard"]], (230,140))
        else:
            screen.blit(pauseMenuImg, (0,0))