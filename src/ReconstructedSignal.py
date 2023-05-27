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
        self.reconstructedTime = np.array([])
        self.reconstructedSignal = np.array([])
    

    
    def reconstruct(self):
        super().sample()  # Sample the signal
        if len(self.time) == 0:
            return
        
        # Interpolate the signal
        T = self.samplingPointsTime[1] - self.samplingPointsTime[0]

        temp = self.samplingPointsTime[:, np.newaxis]
        sincM = np.tile(self.time, (len(self.samplingPointsTime), 1)) - np.tile(temp, (1, len(self.time)))
        sincM = sincM / T
        sincM = np.sinc(sincM)
        output = np.dot(self.samplingPointsSignal, sincM)
        self.reconstructedTime = self.time
        self.reconstructedSignal = output

        return self.reconstructedTime, self.reconstructedSignal


        

    def plotSampled(self):
        # Draw Graph
        return super().plot()

    def plot(self):
        # Draw Graph
        self.reconstruct()
        plot = go.Figure()
        # divide self.reconstructedTime by 2
        self.reconstructedSignal = self.reconstructedSignal / 2
        plot.add_trace(go.Scatter(x=self.reconstructedTime, y=self.reconstructedSignal, mode='lines', name="Reconstructed Signal"))
        plot.update_layout(title="Reconstructed Signal", xaxis_title='Time', yaxis_title='Signal',showlegend=False, xaxis_range=[self.scroll, self.scroll + self.zoom],)
        return plot

    def plotDifference(self):
        self.reconstruct()
        
        # index at time = 0.037
        ind = np.where(self.reconstructedTime == 0.037)[0]
        # st.write(self.reconstructedSignal[ind])
        # st.write(self.data[ind])

        tempReconstructedSignal = self.reconstructedSignal / 2
        tempSignal = self.data
        differenceSignal = tempSignal - tempReconstructedSignal
        differenceTime = self.time
        plot = go.Figure()
        plot.add_trace(go.Scatter(x=differenceTime, y=differenceSignal, mode='lines', name="Difference"))
        plot.update_layout(title="Difference", xaxis_title='Time', yaxis_title='Signal',showlegend=False, xaxis_range=[self.scroll, self.scroll + self.zoom],)
        return plot