import streamlit as st
import numpy as np
import plotly.graph_objects as go
from .Signal import Signal
from .SampledSignal import SampledSignal

class ReconstructedSignal(SampledSignal):
    def __init__(self, data, time, frequency, scroll=0, zoom=1):
        super().__init__(data, time, frequency, scroll, zoom)
        self.reconstructedTime = []
        self.reconstructedSignal = []

    def reconstruct(self):
        """
        Reconstruct the signal from the sampled signal using Nyquist-Shannon Sampling Theorem
        This function should be called after sample()
        Then update the reconstructedTime and reconstructedSignal variables
        return: reconstructedTime, reconstructedSignal
        """
        super().sample() # Sample the signal
        # TODO: Reconstruct the signal
        

    def plotSampled(self):
        # Draw Graph
        return super().plot()


    def plot(self):
        # Draw Graph
        plot = go.Figure()
        plot.add_trace(go.Scatter(x=self.reconstructedTime, y=self.reconstructedSignal, mode='lines', name="Reconstructed Signal"))
        plot.update_layout(title="Reconstructed Signal", xaxis_title='Time', yaxis_title='Signal',showlegend=False, xaxis_range=[0, self.zoom])
        return plot