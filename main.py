# import subprograms from project files
from title import titleScene
from startGame import startGame


# This code is necessary for python to work on tdsb computers
import platform
import os
if platform.system() == "Windows":
    os.environ['SDL_VIDEODRIVER'] = 'windib'

# run the main subprogram
startGame({"title": titleScene}, "title", (1024,768))
