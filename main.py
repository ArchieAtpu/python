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
from creditScene import creditScene

from lessonScene import lessonScene
from lessonSun import lessonSun
from lessonInnerOuterPlanets import lessonInnerOuterPlanets
from lessonMercuryVenus import lessonMercuryVenus
from lessonEarthMars import lessonEarthMars
from lessonJupiterSaturn import lessonJupiterSaturn
from lessonUranusNeptune import lessonUranusNeptune
from lessonDwarf import lessonDwarf
from lessonDwarf2 import lessonDwarf2

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
    "testUncompleted": testUncompletedScene,

    "lesson": lessonScene,
    "credits": creditScene, 
    "Sun": lessonSun, 
    "Inner/Outer Planets": lessonInnerOuterPlanets,
    "Mercury/Venus": lessonMercuryVenus, 
    "Earth/Mars": lessonEarthMars, 
    "Jupiter/Saturn": lessonJupiterSaturn, 
    "Uranus/Neptune": lessonUranusNeptune, 
    "Dwarf Planets": lessonDwarf, 
    "Dwarf Planets2": lessonDwarf2
}, "title", (1024, 768))
