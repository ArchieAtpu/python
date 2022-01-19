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
    ], "correctAnswer": 2 },
    { "question": "The Jovian planets are:", "answers": [
        "Uranus, Saturn, Neptune, and Jupiter",
        "Neptune and Uranus",
        "Jupiter and Saturn",
        "Mercury, Venus, Earth, and Mars"
    ], "correctAnswer": 0 },
    { "question": "Which is the hottest planet \nin the Solar System?", "answers": [
        "Ceres",
        "Mercury",
        "Mars",
        "Venus"
    ], "correctAnswer": 3 },
    { "question": "Which planet is unusual because \nof its elongated shape?", "answers": [
        "Earth",
        "Makemake",
        "Uranus",
        "Haumea"
    ], "correctAnswer": 3 },
    { "question": "Which planet has soil \ncontaining iron oxide (rust)?", "answers": [
        "Venus",
        "Mercury",
        "Makemake",
        "Mars"
    ], "correctAnswer": 3 },
    { "question": "Jupiter's 4 largest \nmoons are:", "answers": [
        "Haumea, Makemake, Eris, and Ceres",
        "Io, Europa, Ganymede, and Callisto",
        "The Ganymede moons",
        "Jupiter only has 3 moons."
    ], "correctAnswer": 1 },
    { "question": "What is the sun \nmostly made of?", "answers": [
        "Hydrogen and helium",
        "Oxygen",
        "Helium",
        "Hydrogen, helium, and oxygen"
    ], "correctAnswer": 0 },
    { "question": "Which planet is known for \nrotating on its side?", "answers": [
        "Neptune",
        "Uranus",
        "Makemake",
        "Saturn"
    ], "correctAnswer": 1 },
    { "question": "Which is the least densest \nplanet in the solar system?", "answers": [
        "Saturn",
        "Jupiter",
        "Neptune",
        "Uranus"
    ], "correctAnswer": 0 },
    { "question": "Which planet is mostly covered \nby liquid water?", "answers": [
        "Neptune",
        "Ganymede",
        "Earth",
        "Europa"
    ], "correctAnswer": 2 },
    { "question": "Which is the farthest \nfull-fledged planet from the sun?", "answers": [
        "Uranus",
        "Pluto",
        "Neptune",
        "Mercury"
    ], "correctAnswer": 2 },
    { "question": "Where does the Sun \nproduce its energy?", "answers": [
        "The Photosphere",
        "The Core",
        "The Sun doesn't produce energy.",
        "The Chromosphere"
    ], "correctAnswer": 1 },
]

radioButtonSize = 20
radioButtonXCoord = 70
radioButtonYCoords = [ 310, 380, 450, 520 ]

def testMultChoiceScene(events, screen, state, globals):
    # initialize variables if they don't exist
    if not ("userAnswers" in globals and globals["userAnswers"]):
        globals["userAnswers"] = [ None for i in range(len(questions)) ]
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
    
    if globals["showTestAnswers"]:
        showAnswers(screen, state, globals)

def renderText(screen, state):
    currentQuestion = questions[state["currentQuestion"]]["question"]

    if "\n" in currentQuestion:
        splitQuestion = currentQuestion.splitlines()
        bangersFont.render_to(screen, (50, 136), splitQuestion[0], WHITE, size=58)
        bangersFont.render_to(screen, (50, 184), splitQuestion[1], WHITE, size=58)
    else:
        bangersFont.render_to(screen, (50, 136), questions[state["currentQuestion"]]["question"], WHITE, size=66)

    bangersFont.render_to(screen, (105, 290), questions[state["currentQuestion"]]["answers"][0], PURPLE, size=52)
    bangersFont.render_to(screen, (105, 360), questions[state["currentQuestion"]]["answers"][1], CYAN, size=52)
    bangersFont.render_to(screen, (105, 430), questions[state["currentQuestion"]]["answers"][2], PURPLE, size=52)
    bangersFont.render_to(screen, (105, 500), questions[state["currentQuestion"]]["answers"][3], CYAN, size=52)

def radioButton(screen, radius, pos, selected, unselectedColor, selectedColor):
    pygame.draw.circle(screen, selectedColor if selected else unselectedColor, pos, radius, radius//7)

    if selected:
        pygame.draw.circle(screen, selectedColor, pos, radius//2)

def drawButtons(screen, state, globals):
    for i in range(4):
        radioButton(screen, radioButtonSize, (radioButtonXCoord, radioButtonYCoords[i]), 
            globals["userAnswers"][state["currentQuestion"]] == i, (190,190,190), (255,255,255))

def showAnswers(screen, state, globals):
    screen.blit(checkMark, (radioButtonXCoord - 70, radioButtonYCoords[questions[state["currentQuestion"]]["correctAnswer"]] - 25))
    if globals["userAnswers"][state["currentQuestion"]] != questions[state["currentQuestion"]]["correctAnswer"] \
        and globals["userAnswers"][state["currentQuestion"]] != None:
        screen.blit(xMark, (radioButtonXCoord - 62, radioButtonYCoords[globals["userAnswers"][state["currentQuestion"]]] - 27))