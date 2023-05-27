import streamlit as st
import numpy as np
import plotly.graph_objects as go
from .Signal import Signal

class SampledSignal(Signal):
    def __init__(self, data, time, frequency,addNoise, noise, scroll=0, zoom=1):
        super().__init__(data, time, frequency,scroll,addNoise, noise,  zoom)
        self.samplingPointsTime = np.array([])
        self.samplingPointsSignal = np.array([])

    def sample(self):
        """
        Sample the signal using frequency variable
        return: samplingPointsTime, samplingPointsSignal
        """
        if len(self.time) == 0:
            return
        if self.frequency == 0:
            self.frequency = 1

        data = self.data
        if self.addNoise:
            data = self.data + self.addSignalNoise()
        maxSamplingFrequency = len(self.time) / (max(self.time))
        # st.write(maxSamplingFrequency)
        length = len(self.time)
        step = round(maxSamplingFrequency / self.frequency)

        for i in range(0, length, step):
            # st.write(i)
            self.samplingPointsTime = np.append(self.samplingPointsTime, self.time[i])
            self.samplingPointsSignal = np.append(self.samplingPointsSignal, data[i])
        # st.write(self.samplingPointsTime)
        return self.samplingPointsTime, self.samplingPointsSignal

    def plot(self):
        # Draw Graph
        self.sample()
        plot = go.Figure()
        # print(self.time)
        # print(self.data)
        data = self.data
        if self.addNoise:
            data = self.data + self.addSignalNoise()

        plot.add_trace(go.Scatter(x=self.time, y=data, mode='lines', name="Original Signal"))
        plot.add_trace(go.Scatter(x=self.samplingPointsTime, y=self.samplingPointsSignal, mode='markers', name='Sampled Signal', marker=dict(color='red')))
        plot.update_layout(title="Sampled Signal", xaxis_title='Time', yaxis_title='Signal',showlegend=False, )
        return plot
    
    # def signal_csv(self):
    #      with open('sampledSignal.txt', 'w') as f: 
    #          f.write('Time,Amplitude')
    #          for i in range(len(self.samplingPointsTime)):
    #              f.write(str(self.samplingPointsTime[i]))
    #              f.write(',')
    #              f.write(str(self.samplingPointsSignal[i]))
    #              f.write('\n')
    #      f.close()
    #      return f
              
    


        



                    

        