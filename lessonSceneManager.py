# import subprograms from project files
from lessonScene import lessonScene
from lessonSun import lessonSun
from lessonInnerOuterPlanets import lessonInnerOuterPlanets
from lessonMercuryVenus import lessonMercuryVenus
from lessonEarthMars import lessonEarthMars
from lessonJupiterSaturn import lessonJupiterSaturn
from lessonUranusNeptune import lessonUranusNeptune
from lessonDwarf import lessonDwarf
from lessonStars import lessonStars


# This code is necessary for python to work on tdsb computers
import platform
import os
if platform.system() == "Windows":
    os.environ['SDL_VIDEODRIVER'] = 'windib'

# run the main subprogram
lessonScene({"Sun": lessonSun, "Inner/Outer Planets": lessonInnerOuterPlanets, "Mercury/Venus": lessonMercuryVenus, "Earth/Mars": lessonEarthMars, "Jupiter/Saturn": lessonJupiterSaturn, "Uranus/Neptune": lessonUranusNeptune, "Dwarf Planets": lessonDwarf, "Stars": lessonStars }, "title", (1024,768))