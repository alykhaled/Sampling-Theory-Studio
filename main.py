import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
from src.SampledSignal import SampledSignal
from src.ReconstructedSignal import ReconstructedSignal
from src.Composer import SignalComponent

def updateSignal():
    st.session_state.signal['frequency'] = st.session_state.frequency


def sidebar():
    if 'signal' not in st.session_state:
        st.session_state.signal = {
            'Time': np.array([]),
            'Amplitude': np.array([]),
            'frequency': 1,
        }

    if 'components' not in st.session_state:
        st.session_state.components = []
 
    st.sidebar.write('Upload Signal')
    uploaded_file = st.sidebar.file_uploader("Choose a file", type="csv")
    if uploaded_file is not None:
        st.session_state['signal'] = pd.read_csv(uploaded_file)

    # Composer Settings Controls
    st.sidebar.header('Composer Settings')
    magnitude = st.sidebar.number_input('Magnitude', min_value=0, max_value=None, value=12, key='componentMagnitude')
    frequency = st.sidebar.number_input('Frequency', min_value=0, max_value=None, value=25, key='componentFrequency')
    name = st.sidebar.text_input('Name', key='componentName')
    if st.sidebar.button('Add Component', key='addComponent'):
        st.session_state.components.append(SignalComponent(magnitude, frequency, name))
        if st.session_state.signal['Time'].size == 0:
            st.session_state.signal['Time'] = np.arange(0, 1, 0.01)
        for component in st.session_state.components:
            if st.session_state.signal['Amplitude'].size == 0:
                componentSignal = component.getSignal(st.session_state.signal['Time'])
                st.session_state.signal['Amplitude'] = componentSignal
            else:
                componentSignal = component.getSignal(st.session_state.signal['Time'])
                st.session_state.signal['Amplitude'] += component.getSignal(st.session_state.signal['Time'])
        st.experimental_rerun()

    labels = [component.name for component in st.session_state.components]
    selectedComponent = st.sidebar.selectbox('Components', labels, key='signalComponents')
    if st.sidebar.button('Remove Component', key='removeComponent', disabled=selectedComponent is None):
        component = st.session_state.components[labels.index(selectedComponent)]
        st.session_state.components.remove(component)
        st.session_state.signal['Amplitude'] -= component.getSignal(st.session_state.signal['Time'])
        st.experimental_rerun()

    # Frequency Settings Controls
    st.sidebar.header('Frequency Settings')
    maxFrequency = st.sidebar.number_input('Max Frequency', 0, 100, 1, key='maxFrequency')
    frequency = st.sidebar.slider('Frequency', 1, 4*maxFrequency,1, key='frequency', on_change=updateSignal)

    # Noise Settings Controls
    st.sidebar.header('Noise Settings')
    noise = st.sidebar.slider('Noise SNR', 0, 100, 0, key='noise')

    # Graph Settings Controls
    st.sidebar.header('Graph Settings')
    scroll = st.sidebar.slider('Scroll', 0, 100, 0, key='scroll')
    zoom = st.sidebar.slider('Zoom', 1, 10, 1, key='zoom')



def plotSignal():
    reconstructed = ReconstructedSignal(st.session_state.signal['Amplitude'], st.session_state.signal['Time'], st.session_state.frequency)
    plot = reconstructed.plotSampled()
    st.plotly_chart(plot, use_container_width=True)
    plot = reconstructed.plot()
    st.plotly_chart(plot, use_container_width=True)


def main():
    st.title('Signal Viewer :heart:')
    sidebar()
    plotSignal()

if __name__ == '__main__':
    main()
