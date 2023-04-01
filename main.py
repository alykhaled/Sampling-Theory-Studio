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
        }

    if 'components' not in st.session_state:
        st.session_state.components = []

    if 'maxFrequency' not in st.session_state:
        st.session_state.maxFrequency = 1
 
    st.sidebar.write('Upload Signal')
    uploaded_file = st.sidebar.file_uploader("Choose a file", type="csv")
    if uploaded_file is not None:
        st.session_state['signal'] = pd.read_csv(uploaded_file)

    # Composer Settings Controls
    st.sidebar.header('Composer Settings')
    magnitude = st.sidebar.number_input('Magnitude', min_value=1, max_value=None, value=1, key='componentMagnitude')
    frequency = st.sidebar.number_input('Frequency', min_value=1, max_value=None, value=1, key='componentFrequency')
    name = st.sidebar.text_input('Name', key='componentName')
    if st.sidebar.button('Add Component', key='addComponent'):
        st.session_state.components.append(SignalComponent(magnitude, frequency, name))
        if st.session_state.signal['Time'].size == 0:
            st.session_state.signal['Time'] = np.arange(0, 1, 0.001)
        new_component = st.session_state.components[-1] 
        new_component_signal = new_component.getSignal(st.session_state.signal['Time'])
        if st.session_state.signal['Amplitude'].size == 0:
            st.session_state.signal['Amplitude'] = new_component_signal
        else:
            st.session_state.signal['Amplitude'] += new_component_signal
        st.experimental_rerun()

    labels = ["{} - {} HZ".format(component.name,component.frequency) for component in st.session_state.components]
    selectedComponent = st.sidebar.selectbox('Components', labels, key='signalComponents')
    if st.sidebar.button('Remove Component', key='removeComponent', disabled=selectedComponent is None):
        component = st.session_state.components[labels.index(selectedComponent)]
        st.session_state.components.remove(component)
        st.session_state.signal['Amplitude'] -= component.getSignal(st.session_state.signal['Time'])
        st.session_state.signal['Amplitude'] = np.round(st.session_state.signal['Amplitude'],5)
        st.experimental_rerun()

    # Frequency Settings Controls
    st.sidebar.header('Frequency Settings')
    maxFrequency = st.session_state['maxFrequency']
    # st.write(maxFrequency)
    # st.sidebar.write('Max Frequency: {}'.format(st.session_state.maxFrequency))
    frequency = st.sidebar.slider('Frequency', 1, int(4*maxFrequency),1, key='frequency', on_change=updateSignal)

    # Noise Settings Controls
    st.sidebar.header('Noise Settings')
    addNoise = st.sidebar.checkbox('Add Noise', key='addNoise')
    noise = st.sidebar.slider('Noise SNR', 1, 30, 30, key='noise', disabled=not addNoise)

    # Graph Settings Controls
    st.sidebar.header('Graph Settings')
    maxScroll = np.array(st.session_state.signal['Time'])[-1] if st.session_state.signal['Time'].size > 0 else 1.0
    scroll = st.sidebar.slider('Scroll', 0.0, maxScroll, 0.0, key='scroll', disabled=True if st.session_state.components else False)



def plotSignal():
    
    reconstructed = ReconstructedSignal(st.session_state.signal['Amplitude'], np.array(st.session_state.signal['Time']), st.session_state.frequency, st.session_state.noise, st.session_state.addNoise, st.session_state.scroll)
    reconstructed.addSignalNoise()
    st.session_state.maxFrequency = reconstructed.getMaxFrequency()
    
    st.write('Max Frequency: {}'.format(st.session_state.maxFrequency))
    plot = reconstructed.plotSampled()
    st.plotly_chart(plot, use_container_width=True)
    plot = reconstructed.plot()
    st.plotly_chart(plot, use_container_width=True)
    plot = reconstructed.plotDifference()
    st.plotly_chart(plot, use_container_width=True)


def main():
    st.set_page_config(page_title='Signal Sampling Studio', page_icon=':heart:', layout='wide', initial_sidebar_state='auto')
    st.title('Signal Sampling Studio :heart:')
    sidebar()
    plotSignal()

if __name__ == '__main__':
    main()
