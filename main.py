# import subprograms from project files
from startGame import startGame

from titleScene import titleScene
from menuScene import menuScene
from gameScene import gameScene
from testStartScene import testStartScene
from testMultChoiceScene import testMultChoiceScene

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
    "testMultChoice": testMultChoiceScene
}, "testMultChoice", (1024, 768))
