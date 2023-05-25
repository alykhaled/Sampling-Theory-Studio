import streamlit as st
import numpy as np
import plotly.graph_objects as go

class Signal():
    def __init__(self, data, time, frequency, scroll ,noise ,addNoise ,zoom):
        self.data = data
        self.time = time
        self.frequency = frequency
        self.scroll = scroll
        self.zoom = zoom
        self.SNR = noise
        self.addNoise = addNoise

    def plot(self):
        # Draw Graph
        st.header(self.name)
        plot = go.Figure()
        plot.add_trace(go.Scatter(x=self.time, y=self.data, mode='lines'))
        plot.update_layout(title=self.name, xaxis_title='Time', yaxis_title='Signal',showlegend=False, xaxis_range=[0, self.zoom])
        return plot

    def getMaxFrequency(self):
        """
        Get the maximum frequency of the signal using FFT
        return: maxFrequency
        """
        if len(self.time) == 0:
            return 1
        # Perform Fourier transform on signal
        fft_data = np.fft.fft(self.data)
        
        # Calculate the total duration of the signal
        T = self.time[-1] - self.time[0]
        
        # Calculate the corresponding frequency values using total duration
        freq = np.fft.fftfreq(len(self.data), d=T/len(self.data))
        # freq = np.sort(freq)
        fft_data = np.abs(fft_data)
        # Round the frequency values to 2 decimal places
        fft_data = np.round(fft_data, 2)
        # Find the index of the all maximum values in the FFT array
        max_index = np.where(np.abs(fft_data) == np.max(np.abs(fft_data)))
        # st.write(np.max(np.abs(fft_data)))
        # st.write(freq)
        # st.write(max_index)
        # st.write(fft_data)

        # Return the corresponding frequency value as the maximum frequency
        max_frequency = 0
        for i in max_index[0]:
            max_frequency = max(max_frequency, np.abs(freq[i]))
        
        return max_frequency

    def addSignalNoise(self):
        """
        Add noise to the signal
        SNR: Signal to Noise Ratio
        """
        if not self.addNoise:
            return
        np.random.seed(seed=0)
        powerSignal = np.mean(self.data**2)
        powerNoise = powerSignal / (10**(self.SNR/10))
        noise = np.random.normal(scale=np.sqrt(powerNoise), size=self.data.shape)
        self.data = self.data + noise
        return noise