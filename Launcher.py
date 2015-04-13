import inspect, os, wapisp

import sys

if not sys.version_info[:2] == (3, 2):
    wapisp.MessageBox(0, "Python Version Invalid: 3.2.x is REQUIRED.  ", "Unable to Proceed.  ", 0x10)
    exit(sys.version_info)
print(wapisp.ShellExecute(0, "open", "main.py", wapisp.NULL, os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))+os.sep+"PokemonFinalProjectV1", wapisp.SW_HIDE))
