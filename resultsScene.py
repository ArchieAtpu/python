import pygame

PURPLE = (116,67,189)
CYAN = (80, 165, 187)

backgroundImg = pygame.image.load("./assets/resultsBackground.png")
bangersFont = pygame.freetype.Font("./assets/Bangers-Regular.ttf")

correctAnswers = [ 2, 0, 3, 3, 3, 1, 0, 1, 0, 2, 2, 1 ]
correctMatches = [ 1, 3, 2, 0 ]

def resultsScene(events, screen, state, globals):

    if not state:
        state["testScore"] = 0

        for userAnswer, correctAnswer in zip(globals["userAnswers"] + globals["userMatchingAnswers"], correctAnswers + correctMatches):
            if userAnswer == correctAnswer:
                state["testScore"] += 1

        state["testScorePercentage"] = round(state["testScore"] / (len(correctAnswers)+len(correctMatches)) * 100)

    for event in events:
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            print(mousePos)

            if mousePos[0] > 130 and mousePos[0] < 440 and mousePos[1] > 590 and mousePos[1] < 700:
                return "menu"
            elif mousePos[0] > 600 and mousePos[0] < 920 and mousePos[1] > 590 and mousePos[1] < 700:
                globals["showTestAnswers"] = True
                return "testMultChoice"    

    screen.blit(backgroundImg, (0,0))

    # True equals 1 and False equals 0 when used in arithmetic.
    bangersFont.render_to(screen, (365 + 35*(state["testScore"] < 10), 312), str(state["testScore"]), CYAN, size=150)
    bangersFont.render_to(screen, (466 - 25*(len(str(state['testScorePercentage']))), 445),
        f"({state['testScorePercentage']}%)", PURPLE, size=100)