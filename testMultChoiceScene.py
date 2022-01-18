import pygame
import pygame.freetype
import math

pygame.freetype.init()
bangersFont = pygame.freetype.Font("./assets/Bangers-Regular.ttf")
background = pygame.image.load("./assets/testBackground.png")
checkMark = pygame.transform.scale(pygame.image.load("./assets/checkmark.png"),(50,40))
xMark = pygame.transform.scale(pygame.image.load("./assets/xMark.png"),(43,50))

WHITE = (255,255,255)
PURPLE = (116,67,189)
CYAN = (80, 165, 187)

questions = [
    { "question": "Where is Ceres located?", "answers": [
        "The Kuiper Belt",
        "Between Earth and Mars",
        "The Asteroid Belt",
        "The Oort Cloud"
    ], "correctAnswer": 2, "image": pygame.image.load("./assets/titleBackground.png") },
    { "question": "The Jovian planets are:", "answers": [
        "Uranus, Saturn, Neptune, and Jupiter",
        "Neptune and Uranus",
        "Jupiter and Saturn",
        "Mercury, Venus, Earth, and Mars"
    ], "correctAnswer": 0, "image": pygame.image.load("./assets/demoAsteroid.jpg") },
    { "question": "Which is the hottest planet in the \nSolar System?", "answers": [
        "Ceres",
        "Mercury",
        "Mars",
        "Venus"
    ], "correctAnswer": 3, "image": pygame.image.load("./assets/demoAsteroid.jpg") },
    { "question": "Which planet is unusual because of its \nelongated shape?", "answers": [
        "Earth",
        "Makemake",
        "Uranus",
        "Haumea"
    ], "correctAnswer": 3, "image": pygame.image.load("./assets/demoAsteroid.jpg") },
    { "question": "Which planet has soil containing \niron oxide (rust)?", "answers": [
        "Venus",
        "Mercury",
        "Makemake",
        "Mars"
    ], "correctAnswer": 3, "image": pygame.image.load("./assets/demoAsteroid.jpg") },
    { "question": "Jupiter's 4 largest moons are:", "answers": [
        "Haumea, Makemake, Eris, and Ceres",
        "Io, Europa, Ganymede, and Callisto",
        "The Ganymede moons",
        "Jupiter only has 3 moons."
    ], "correctAnswer": 1, "image": pygame.image.load("./assets/demoAsteroid.jpg") },
    { "question": "Which planet is known for rotating \non its side?", "answers": [
        "Neptune",
        "Uranus",
        "Makemake",
        "Saturn"
    ], "correctAnswer": 1, "image": pygame.image.load("./assets/demoAsteroid.jpg") },
    { "question": "Which is the least densest planet in the \nsolar system?", "answers": [
        "Saturn",
        "Jupiter",
        "Neptune",
        "Uranus"
    ], "correctAnswer": 0, "image": pygame.image.load("./assets/demoAsteroid.jpg") },
    { "question": "Which planet is mostly covered by \nliquid water?", "answers": [
        "Neptune",
        "Ganymede",
        "Earth",
        "Europa"
    ], "correctAnswer": 2, "image": pygame.image.load("./assets/demoAsteroid.jpg") },
    { "question": "Which is the farthest full-fledged planet \nfrom the sun?", "answers": [
        "Uranus",
        "Pluto",
        "Neptune",
        "Mercury"
    ], "correctAnswer": 2, "image": pygame.image.load("./assets/demoAsteroid.jpg") },
]

# Scale images so that their height is 260 while preserving aspect ratio
for question in questions:
    newWidth = round(260/question["image"].get_height()*question["image"].get_width())
    question["image"] = pygame.transform.scale(question["image"], (newWidth, 260))

radioButtonSize = 20
radioButtonXCoord = 115
radioButtonYCoords = [ 410, 470, 530, 590 ]

def testMultChoiceScene(events, screen, state, globals):
    # initialize variables if they don't exist
    if not ("userAnswers" in globals and globals["userAnswers"]):
        globals["userAnswers"] = [ 0 for i in range(len(questions)) ]
    if not state:
        state["currentQuestion"] = 0

    # if back button on matching screen was pressed
    if globals.get("fromMatching", False):
        globals["fromMatching"] = False
        state["currentQuestion"] = len(questions) - 1

    for event in events:
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            print(mousePos)

            # code for the radio buttons
            if not globals["showTestAnswers"]: 
                for i in range(4):
                    if math.hypot(mousePos[0] - radioButtonXCoord, mousePos[1] - radioButtonYCoords[i]) <= radioButtonSize:
                        globals["userAnswers"][state["currentQuestion"]] = i
                        break
            
            # back button
            if mousePos[0] > 215 and mousePos[0] < 445 and mousePos[1] > 640 and mousePos[1] < 725:
                if state["currentQuestion"] != 0: 
                    state["currentQuestion"] -= 1
                elif globals["showTestAnswers"]:
                    return "results"

            # next button
            elif mousePos[0] > 595 and mousePos[0] < 825 and mousePos[1] > 640 and mousePos[1] < 725:
                if state["currentQuestion"] == len(questions) - 1:
                    return "testMatching"
                state["currentQuestion"] += 1
    
    screen.blit(background, (0,0))

    # covers the back button
    if state["currentQuestion"] == 0 and not globals["showTestAnswers"]:
        screen.fill((0,0,0), pygame.Rect(215,640,235,85))

    renderText(screen, state)
    drawButtons(screen, state, globals)
    drawImg(screen, state)
    
    if globals["showTestAnswers"]:
        showAnswers(screen, state, globals)

def renderText(screen, state):
    currentQuestion = questions[state["currentQuestion"]]["question"]

    if "\n" in currentQuestion:
        splitQuestion = currentQuestion.splitlines()
        bangersFont.render_to(screen, (60, 17), splitQuestion[0], WHITE, size=58)
        bangersFont.render_to(screen, (60, 65), splitQuestion[1], WHITE, size=58)
    else:
        bangersFont.render_to(screen, (60, 20), questions[state["currentQuestion"]]["question"], WHITE, size=66)

    bangersFont.render_to(screen, (150, 390), questions[state["currentQuestion"]]["answers"][0], PURPLE, size=52)
    bangersFont.render_to(screen, (150, 450), questions[state["currentQuestion"]]["answers"][1], CYAN, size=52)
    bangersFont.render_to(screen, (150, 510), questions[state["currentQuestion"]]["answers"][2], PURPLE, size=52)
    bangersFont.render_to(screen, (150, 570), questions[state["currentQuestion"]]["answers"][3], CYAN, size=52)

def radioButton(screen, radius, pos, selected, unselectedColor, selectedColor):
    pygame.draw.circle(screen, selectedColor if selected else unselectedColor, pos, radius, radius//7)

    if selected:
        pygame.draw.circle(screen, selectedColor, pos, radius//2)

def drawButtons(screen, state, globals):
    for i in range(4):
        radioButton(screen, radioButtonSize, (radioButtonXCoord, radioButtonYCoords[i]), 
            globals["userAnswers"][state["currentQuestion"]] == i, (190,190,190), (255,255,255))

def drawImg(screen, state):
    questionImg = questions[state["currentQuestion"]]["image"]
    position = (512 - questionImg.get_width()/2, 240 - 125) # center image around (512,240)
    screen.blit(questionImg, position)

def showAnswers(screen, state, globals):
    screen.blit(checkMark, (radioButtonXCoord - 70, radioButtonYCoords[questions[state["currentQuestion"]]["correctAnswer"]] - 25))
    if globals["userAnswers"][state["currentQuestion"]] != questions[state["currentQuestion"]]["correctAnswer"]:
        screen.blit(xMark, (radioButtonXCoord - 62, radioButtonYCoords[globals["userAnswers"][state["currentQuestion"]]] - 27))