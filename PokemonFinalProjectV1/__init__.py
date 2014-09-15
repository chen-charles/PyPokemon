import os
import sys
import inspect
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(path)+os.sep+"PokemonFinalProjectV1")
input(sys.path)
import main

##__version__ = buildinfo.get(path+"/__init__")
__author__ = 'Charles-Jianye Chen'
sys.path.pop(0)
