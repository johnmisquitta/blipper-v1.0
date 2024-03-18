import pandas as pd
import streamlit as st
import librosa
st.set_page_config(layout="wide")

import matplotlib.pyplot as plt
# Function to process the uploaded CSV file
df2 = pd.read_csv('./output_matrics (4).csv')

def process_csv(file):
    if file is not None:
        # Read the CSV file
        df = pd.read_csv(file)

        # Extract unique URLs
        unique_urls = df['url'].unique()
        return df, unique_urls
    else:
        return None, None

# Function to navigate to a new page with selected URL
def navigate_to_url_page(selected_url, df):
    # Filter DataFrame based on selected URL
    filtered_df = df[df['url'] == selected_url]
    
    # Display filtered DataFrame
    st.write(filtered_df)

    filtered_df2=df2[df2['Link'] == selected_url]
    st.write(filtered_df2)


    st.title('Call Analysis')
    
    # Print other details
    columns_to_display = [
    "Total Call Duration",
    "Total Effective Talk Duration",
    "Total Effective Talk Percent",
    "Talk Duration (Mono Right)",
    "Talk Duration (Mono Left)",
    "Talk Percent (Mono Right)",
    "Talk Percent (Mono Left)",
    "Overlaps Count (Total)",
    "Overlaps Count (Mono Right)",
    "Overlaps Count (Mono Left)",
    "Overlaps Duration (Total)",
    "Overlaps Duration (Mono Right)",
    "Overlaps Duration (Mono Left)",
    "Overlaps Percent (Total)",
    "Overlaps Percent (Mono Right)",
    "Overlaps Percent (Mono Left)"
]

    for column in columns_to_display:
        st.write(column + ":", filtered_df2[column].iloc[0])

st.title("Upload Processed CSV")

# Define variables
df = None
unique_urls = None

# File uploader for selecting CSV file
csv_file = st.file_uploader("CSV file", type=["csv"])

# Display buttons for each unique URL when CSV file is uploaded
if csv_file is not None:
    df, unique_urls = process_csv(csv_file)
    # Display buttons for each unique URL
    for url in unique_urls:
        if st.button(url):
            navigate_to_url_page(url, df)

# Check if query parameter contains selected URL
if "url" in st.experimental_get_query_params():
    selected_url = st.experimental_get_query_params()["url"]
    st.write(f"Selected URL: {selected_url}")
