import streamlit as st
import numpy as np
import plotly.graph_objects as go
from .Signal import Signal

class SampledSignal(Signal):
    def __init__(self, data, time, frequency,addNoise, noise, scroll=0, zoom=1):
        super().__init__(data, time, frequency,scroll,addNoise, noise,  zoom)
        self.samplingPointsTime = []
        self.samplingPointsSignal = []

    def sample(self):
        """
        Sample the signal using frequency variable
        return: samplingPointsTime, samplingPointsSignal
        """
        if len(self.time) == 0:
            return
        self.samplingPointsTime = np.arange(0, self.time[-1], 1/self.frequency)
        self.samplingPointsSignal = np.interp(self.samplingPointsTime, self.time, self.data)
        


    def plot(self):
        # Draw Graph
        self.sample()
        plot = go.Figure()
        # print(self.time)
        # print(self.data)
        plot.add_trace(go.Scatter(x=self.time, y=self.data, mode='lines', name="Original Signal"))
        plot.add_trace(go.Scatter(x=self.samplingPointsTime, y=self.samplingPointsSignal, mode='markers', name='Sampled Signal', marker=dict(color='red')))
        plot.update_layout(title="Sampled Signal", xaxis_title='Time', yaxis_title='Signal',showlegend=False, xaxis_range=[self.scroll, self.scroll + self.zoom], )
        return plot