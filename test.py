import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import scipy.interpolate as interpolate
import scipy.signal as signal


plt.style.use('dark_background')

st.title("Sampling Studio")

with st.sidebar:
    uploaded_file = st.file_uploader("Choose a wav file", type=['wav']) 
    # An error will be thrown but goes away when a file is chosen
    amplitude, frequency = st.columns([1,3])
    frequency = st.number_input("Frequency") # Getting the sine wave frequency
    amplitude = st.number_input("Amplitude") # Getting the sine wave amplitude
    

rate, data = wav.read(uploaded_file)
sampling_freq= rate
nyquist_freq = sampling_freq / 2
sampling_rate = nyquist_freq
samples = np.arange(0, len(data), sampling_rate)
sampled_data = data[np.round(samples).astype(int)]

fig1, ax1 = plt.subplots()
ax1.stem(sampled_data)
ax1.set_xlabel('Time', fontsize=15)
ax1.set_ylabel('Amplitude', fontsize=15)
ax1.set_title('Sampled Signal', fontsize=20)
st.pyplot(fig1)

new_len = len(data)
resampled_data = signal.resample(sampled_data, new_len)

interpolator = interpolate.interp1d(np.arange(0, new_len), resampled_data, kind='linear')
reconstructed_data = interpolator(np.linspace(0, new_len -1, new_len))

fig2, ax2 = plt.subplots()
ax2.plot(reconstructed_data)
ax2.set_xlabel('Time', fontsize=15)
ax2.set_ylabel('Amplitude', fontsize=15)
ax2.set_title('Reconstructed Siganl', fontsize=20)
st.pyplot(fig2)

