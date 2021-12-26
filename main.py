import os

from startGame import startGame
from menuScene import menuScene
from gameScene import gameScene

# This code is necessary for python to work on tdsb computers
import platform
if platform.system() == "Windows":
    os.environ['SDL_VIDEODRIVER'] = 'windib'

startGame({ "menu": menuScene, "game": gameScene }, "game")