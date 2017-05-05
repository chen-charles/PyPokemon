import inspect, os, wapisp

import sys
input(str(sys.version_info))
if sys.version_info[:2] == (3, 6):
    import pip
    pip.main("install pygame".split())
elif sys.version_info[:2] == (3, 2):
    try: import pygame
    except:
        wapisp.MessageBox(0, "Pygame not installed. ", "Unable to Proceed.  ", 0x10)
        exit(sys.version_info)
else:
    wapisp.MessageBox(0, "Python Version Invalid: 3.2/3.6 is REQUIRED.  ", "Unable to Proceed.  ", 0x10)
    exit(sys.version_info)
    
print(wapisp.ShellExecute(0, "open", "main.py", wapisp.NULL, os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))+os.sep+"PokemonFinalProjectV1", wapisp.SW_HIDE))
