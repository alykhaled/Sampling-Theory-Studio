import numpy as np

class SignalComponent():
    def __init__(self,magnitude,frequency,name="Sine Wave"):
        self.magnitude = magnitude
        self.frequency = frequency
        self.name = name if name != "" else "Sine Wave"

    def getSignal(self,time):
        signal = self.magnitude * np.sin(2 * np.pi * self.frequency * time)
        print("Signal: ", signal)
        return self.magnitude * np.sin(2 * np.pi * self.frequency * time)