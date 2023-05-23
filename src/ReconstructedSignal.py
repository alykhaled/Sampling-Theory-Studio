import streamlit as st
import numpy as np
import plotly.graph_objects as go
from .Signal import Signal
from .SampledSignal import SampledSignal
import scipy.interpolate as interpolate
import scipy.signal as signal
from scipy.special import sinc

class ReconstructedSignal(SampledSignal):
    def __init__(self, data, time, frequency, addNoise, noise, scroll=0, zoom=1):
        super().__init__(data, time, frequency, addNoise, noise, scroll, zoom)
        self.reconstructedTime = []
        self.reconstructedSignal = []

    
    def reconstruct(self):
        super().sample()  # Sample the signal
        if len(self.time) == 0:
            return
        
        # TODO: Reconstruct the signal
        new_len = len(self.data)
        resampled_data = signal.resample(self.samplingPointsSignal, new_len)
        reconstructed_time = np.linspace(0, new_len - 1, new_len)
        
        # Apply sinc interpolation
        reconstructed_signal = np.zeros_like(reconstructed_time)
        for i, t in enumerate(reconstructed_time):
            reconstructed_signal[i] = np.sum(resampled_data * np.sinc(t - np.arange(len(resampled_data))))
        
        self.reconstructedSignal = reconstructed_signal
        self.reconstructedTime = self.time
        
        return self.reconstructedTime, self.reconstructedSignal

    def plotSampled(self):
        # Draw Graph
        return super().plot()

    def plot(self):
        # Draw Graph
        self.reconstruct()
        plot = go.Figure()
        plot.add_trace(go.Scatter(x=self.reconstructedTime, y=self.reconstructedSignal, mode='lines', name="Reconstructed Signal"))
        plot.update_layout(title="Reconstructed Signal", xaxis_title='Time', yaxis_title='Signal',showlegend=False, xaxis_range=[self.scroll, self.scroll + self.zoom],)
        return plot

    def plotDifference(self):
        self.reconstruct()
        tempReconstructedSignal = np.round(self.reconstructedSignal, 2)
        tempSignal = np.round(self.data, 2)
        differenceSignal = tempReconstructedSignal - tempSignal
        differenceTime = self.reconstructedTime
        plot = go.Figure()
        plot.add_trace(go.Scatter(x=differenceTime, y=differenceSignal, mode='lines', name="Difference"))
        plot.update_layout(title="Difference", xaxis_title='Time', yaxis_title='Signal',showlegend=False, xaxis_range=[self.scroll, self.scroll + self.zoom],)
        return plot