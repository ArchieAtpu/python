# import subprograms from project files
from startGame import startGame

from titleScene import titleScene
from menuScene import menuScene
from gameScene import gameScene
from testStartScene import testStartScene
from testMultChoiceScene import testMultChoiceScene
from testMatchingScene import testMatchingScene
from testSubmissionScene import testSubmissionScene
from resultsScene import resultsScene
from testUncompletedScene import testUncompletedScene

# This code is necessary for python to work on tdsb computers
import platform
import os
if platform.system() == "Windows":
    os.environ['SDL_VIDEODRIVER'] = 'windib'

# run the main subprogram
startGame({
    "title": titleScene,
    "menu": menuScene,
    "game": gameScene,
    "testStart": testStartScene,
    "testMultChoice": testMultChoiceScene,
    "testMatching": testMatchingScene,
    "testSubmission": testSubmissionScene,
    "results": resultsScene,
    "testUncompleted": testUncompletedScene
}, "title", (1024, 768))
