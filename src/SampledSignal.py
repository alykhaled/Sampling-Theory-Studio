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
        # TODO: Sample the signal
        pass

    def plot(self):
        # Draw Graph
        plot = go.Figure()
        plot.add_trace(go.Scatter(x=self.time, y=self.data, mode='lines', name="Sampled Signal"))
        plot.add_trace(go.Scatter(x=self.samplingPointsTime, y=self.samplingPointsSignal, mode='markers', name='Sampled Signal'))
        plot.update_layout(title="Sampled Signal", xaxis_title='Time', yaxis_title='Signal',showlegend=False, xaxis_range=[0, self.zoom])
        return plot