import inspect, os, wapisp

import sys

try:
    import pygame
except ImportError:
    wapisp.MessageBox(0, "Pygame not installed. ", "Unable to Proceed.  ", 0x10)
    exit(sys.version_info)

print(wapisp.ShellExecute(0, "open", "main.py", wapisp.NULL, os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))+os.sep+"PokemonFinalProjectV1", wapisp.SW_HIDE))
