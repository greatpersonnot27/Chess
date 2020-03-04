# Handles the options available in the engine
class EngineOptions:
    def __init__(self):
        self.id = "AIEngline"
        self.name = "Ika$Shota Engine"
        self.allOptions = {"Hash": {"type": "spin", "min": "1", "max": "4096", "default": "32", "value": "32"},
                           "Max CPUs": {"type": "spin", "min": "1", "max": "2048", "default": "2048", "value": "2048"},
                           "Display PV Tips": {"type": "check", "default": "false", "value": "false"},
                           "CPU Usage": {"type": "spin", "min": "1", "max": "100", "default": "100", "value": "100"},
                           "Win Percentage to Hash Usage": {"type": "check", "default": "false", "value": "false"},
                           "Display Current Move": {"type": "check", "default": "true", "value": "true"},
                           "NalimovPath": {"type": "string", "default": "<empty>", "value": "<empty>"},
                           "NalimovCache": {"type": "spin", "min": "1", "max": "256", "default": "1", "value": "1"},
                           "Ponder": {"type": "check", "default": "true", "value": "true"},
                           "UCI_AnalyseMode": {"type": "check", "default": "false", "value": "false"}}

    def send_available_options(self):
        for name, options in self.allOptions.items():
            ops = ""
            for key, value in options.items():
                ops += " " + key + " " + value
            print("option name " + name + ops)

    def set_option(self, option):
        optionName = " ".join(option.split()[2:-2])
        self.allOptions[optionName]["value"] = option.split()[-1]
