import pandas as pd
import streamlit as st
import librosa
st.set_page_config(layout="wide")

import matplotlib.pyplot as plt
# Function to process the uploaded CSV file
df2 = pd.read_csv('./output_matrics (4).csv')
