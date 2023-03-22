import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('dark_background')

st.title("Sampling Studio")

with st.sidebar:
    amplitude, frequency = st.columns([1,3])
    frequency = st.number_input("Frequency") # Getting the sine wave frequency
    amplitude = st.number_input("Amplitude") # Getting the sine wave amplitude
    
t = np.linspace(0,10,100) # X-axis (time)
wave = amplitude * np.sin(2 * np.pi * frequency * t)
fig, ax = plt.subplots()
ax.plot(wave)
ax.set_xlabel('time', fontsize=15)
ax.set_ylabel('amplitude', fontsize=15)
ax.set_facecolor((0.64,0.13,0.22)) # Changing the plot background color
st.pyplot(fig)

def unit_step(a,n):
    units = []
    for unit in n:
        if unit < a:
            units.append(0)
        else:
            units.append(1)
    return (units)

a = 0
n = np.arange(0, 10,1)
unit = unit_step(a, n)
fig1, ax1 = plt.subplots()
ax1.stem(n,unit)
ax1.set_xlabel('time', fontsize=15)
ax1.set_ylabel('amplitude', fontsize=15)
st.pyplot(fig1)


f_sampling = 2 * frequency

