import inspect, os, wapisp
wapisp.ShellExecute(0, "open", "main.py", wapisp.NULL, os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))+os.sep+"PokemonFinalProjectV1", wapisp.SW_HIDE)
