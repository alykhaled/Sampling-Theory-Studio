import streamlit as st
import numpy as np
import plotly.graph_objects as go
from .Signal import Signal

class SampledSignal(Signal):
    def __init__(self, data, time, frequency, scroll=0, zoom=1):
        super().__init__(data, time, frequency, scroll, zoom)
        self.samplingPointsTime = []
        self.samplingPointsSignal = []

    def sample(self):
        """
        Sample the signal using frequency variable
        return: samplingPointsTime, samplingPointsSignal
        """
        for i in range(0, len(self.time), self.frequency):
            self.samplingPointsTime.append(self.time[i])
            self.samplingPointsSignal.append(self.data[i])
        


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