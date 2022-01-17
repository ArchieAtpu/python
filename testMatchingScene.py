from gettext import find
import pygame 
import math

background = pygame.image.load('./assets/testMatchingBackground.png')

leftChoicesXCoord = 310
rightChoicesXCoord = 601
choicesYCoords = [ 194, 308, 425, 555 ]
choiceSize = 20

WHITE = (255, 255, 255)
GREEN = (67, 201, 54)
RED = (224, 49, 49)

correctAnswers = [1,3,2,0]

def testMatchingScene(events, screen, state, globals):
    globals["showTestAnswers"] = True
    globals["userMatchingAnswers"] = [2,1,3,0]

    if not "userMatchingAnswers" in globals:
        globals["userMatchingAnswers"] = [ None, None, None, None ]

    if not state:
        state["selectedChoice"] = None

    mousePos = pygame.mouse.get_pos()

    for event in events:
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(mousePos)

            # code for the radio buttons
            if not globals["showTestAnswers"]: 
                for i in range(8):
                    xCoord = leftChoicesXCoord if i < 4 else rightChoicesXCoord
                    yCoord = choicesYCoords[i % 4]

                    if math.hypot(mousePos[0] - xCoord, mousePos[1] - yCoord) <= choiceSize:
                        if state["selectedChoice"] == i:
                            state["selectedChoice"] = None
                        elif state["selectedChoice"] == None or \
                            (state["selectedChoice"] < 4 and i < 4) or (state["selectedChoice"] > 4 and i > 4):

                            if i < 4:
                                globals["userMatchingAnswers"][i] = None
                            else:
                                try:
                                    globals["userMatchingAnswers"][globals["userMatchingAnswers"].index(i % 4)] = None
                                except ValueError:
                                    pass
                        
                            state["selectedChoice"] = i
                        else:
                            if i < 4:
                                globals["userMatchingAnswers"][i] = state["selectedChoice"] % 4
                            else:
                                try:
                                    globals["userMatchingAnswers"][globals["userMatchingAnswers"].index(i % 4)] = None
                                except ValueError:
                                    pass

                                globals["userMatchingAnswers"][state["selectedChoice"]] = i % 4

                            state["selectedChoice"] = None

                        break
            
            # back button
            if mousePos[0] > 215 and mousePos[0] < 445 and mousePos[1] > 640 and mousePos[1] < 725:
                globals["fromMatching"] = True
                return "testMultChoice"

            # next button
            elif mousePos[0] > 595 and mousePos[0] < 825 and mousePos[1] > 640 and mousePos[1] < 725:
                if globals["showTestAnswers"]:
                    pass
                else:
                    return "testSubmission"

    screen.blit(background, (0,0))

    if state["selectedChoice"] != None:
        xCoord = leftChoicesXCoord if state["selectedChoice"] < 4 else rightChoicesXCoord
        yCoord = choicesYCoords[state["selectedChoice"] % 4]
        pygame.draw.circle(screen, (255,255,255), (xCoord, yCoord), 6)
        pygame.draw.line(screen, (255,255,255), (xCoord, yCoord), mousePos, 10)

    if globals["showTestAnswers"]:
        drawChoiceLines(screen, RED, globals["userMatchingAnswers"])
        drawChoiceLines(screen, GREEN, correctAnswers)
    else:
        drawChoiceLines(screen, WHITE, globals["userMatchingAnswers"])

def drawChoiceLines(screen, color, choices):
    for i, answer in enumerate(choices):
        if answer == None:
            continue

        leftChoiceCoords = (leftChoicesXCoord, choicesYCoords[i])
        rightChoiceCoords = (rightChoicesXCoord, choicesYCoords[answer])

        pygame.draw.circle(screen, color, leftChoiceCoords, 6)
        pygame.draw.circle(screen, color, rightChoiceCoords, 6)
        pygame.draw.line(screen, color, leftChoiceCoords, rightChoiceCoords, 10)
