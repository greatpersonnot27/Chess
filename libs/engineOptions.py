# Handles the options available in the engine
class EngineOptions:
    def __init__(self, uci, debug):
        self.id = "AIEngline"
        self.name = "Ika$Shota Engine"

        self.uci = uci
        self.debugMode = debug