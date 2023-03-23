import streamlit as st
import numpy as np
import plotly.graph_objects as go

class Signal():
    def __init__(self, data, time, frequency, scroll, zoom):
        self.data = data
        self.time = time
        self.frequency = frequency
        self.scroll = scroll
        self.zoom = zoom

    def plot(self):
        # Draw Graph
        st.header(self.name)
        plot = go.Figure()
        plot.add_trace(go.Scatter(x=self.time, y=self.data, mode='lines'))
        plot.update_layout(title=self.name, xaxis_title='Time', yaxis_title='Signal',showlegend=False, xaxis_range=[0, self.zoom])
        return plot