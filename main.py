import pandas as pd
import streamlit as st
import librosa

st.set_page_config(layout="wide")
import re
import matplotlib.pyplot as plt
df2 = pd.read_csv('./raw_output_matrics_audit.csv')

background_style = """
    <style>
        .custom-green-background {
            background-color: #aaf683;
            padding: 10px;
            border-radius: 5px;
        }
        .custom-red-background {
            background-color: #ff85a1;
            padding: 10px;
            border-radius: 5px;
        }
    </style>
"""

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

    filtered_df2=df2[df2['Link'] == selected_url]
    #st.write(filtered_df2)

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
    # st.write("John")
    st.write(filtered_df2.columns)
    st.write()
    # st.write(filtered_df2['Total Talk Duration'].iloc[0])
    # st.write(filtered_df2['Total Effective Talk Percent'].iloc[0])
    st.write()
    st.write()
    # st.write(filtered_df2['Talk Percent (Mono Right)'].iloc[0])
    # st.write(filtered_df2['Overlaps Count (Total)'].iloc[0])
    # st.write(filtered_df2['Overlaps Count (Mono Right)'].iloc[0])
    
    # st.write(filtered_df2['Overlaps Count (Mono Left))'].iloc[0])
  
    # st.write(filtered_df2["Overlaps Duration (Total)"].iloc[0])
    # st.write(filtered_df2["Overlaps Duration (Mono Right)"].iloc[0])
    # st.write(filtered_df2["Overlaps Percent (Total)"].iloc[0])

    # st.write(filtered_df2["Overlaps Duration (Mono Left)"].iloc[0])
    # st.write(filtered_df2["Overlaps Percent (Mono Right)"].iloc[0])
    # st.write(filtered_df2["Overlaps Percent (Mono Left)"].iloc[0])
    for column, values in filtered_df2.iterrows():
        st.write(f"{column} : {values.values[0]}")
    labels = ["Total","Right","Left"]
    st.set_option('deprecation.showPyplotGlobalUse', False)

    total_duration = filtered_df2['Total Audio Duration'].iloc[0] + filtered_df2['Overlaps Duration - Total'].iloc[0]
    left_duration = filtered_df2['Talk Duration - Mono Left'].iloc[0]
    right_duration = filtered_df2['Talk Duration - Mono Right'].iloc[0]

    percentage_left = (left_duration / total_duration) * 100
    percentage_right = (right_duration / total_duration) * 100
    percentage_blank = 100 - percentage_left - percentage_right

    # Create the donut chart
    fig, ax = plt.subplots(figsize=(3, 3))  # Adjust the figsize values to achieve a size of 300 pixels
    wedges, texts, autotexts = ax.pie([percentage_left, percentage_right, percentage_blank], labels=['Left Duration', 'Right Duration', 'Blank Duration'], autopct="%1.1f%%", startangle=100, pctdistance=0.55, wedgeprops=dict(width=0.1))

    ax.set_title('Talk Percent')
    ax.axis('equal')  # Equal aspect ratio ensures a circular donut

    # Display the chart in Streamlit
    st.pyplot(fig)






    # for column in columns_to_display:
    #     if column in filtered_df2.columns:
    #         st.write(f"{column}:")
    #     else:
    #         st.write(f"Column '{column}' not found in the DataFrame.")






    call_url=filtered_df['url'].iloc[0]
    dataframes=filtered_df
    st.write(dataframes)
    mono_left_df = dataframes[dataframes['channel'] == 'Mono_Left']
    first_start_timestamp_mono_left = mono_left_df['start'].iloc[0]
    call_duration = pd.to_numeric(mono_left_df['call_duration'].iloc[0])
    # print(call_duration)
    # print(first_start_timestamp_mono_left)
    pattern = re.compile(r'https://s3-ap-southeast-1\.amazonaws\.com/exotelrecordings/futwork1/|\.mp3$')
    cleaned_url = re.sub(pattern, '',call_url)
    st.markdown(f"<div style='background-color:#ff85a1; padding-top: 10px;'>", unsafe_allow_html=True)
    st.write("Orignal Audio")
    audio =(f'./output_files/{cleaned_url}.mp3')
    y,sr=librosa.load(audio)
    st.audio(y, sample_rate=sr)
    st.markdown(f"<div style='background-color: #ff85a1; padding-bottom: 10px;padding-top: 0px;'>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:#ff85a1; padding-top: 10px;'>", unsafe_allow_html=True)

    st.write("Agent Audio")

    audio =(f'./output_files/{cleaned_url}_left.mp3')
    y,sr=librosa.load(audio)

    st.audio(y, sample_rate=sr)
    st.markdown(f"<div style='background-color: #ff85a1; padding-bottom: 10px;padding-top: 0px;'>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:#ff85a1; padding-top: 10px;'>", unsafe_allow_html=True)

    st.write("Customer Audio")
    audio =(f'./output_files/{cleaned_url}_right.mp3')
    y,sr=librosa.load(audio)

    st.audio(y, sample_rate=sr)
    st.markdown(f"<div style='background-color: #ff85a1; padding-bottom: 10px;padding-top: 0px;'>", unsafe_allow_html=True)


    
    fig, ax = plt.subplots(3, 1, figsize=(8, 6))

    # Plot the audio signal
    ax[1].plot(y)
    ax[1].set_title('Audio Signal')
    ax[1].set_xlabel('Time')
    ax[1].set_ylabel('Amplitude')

# Display the plot using Streamlit
    st.pyplot(fig)



    if first_start_timestamp_mono_left>10 and call_duration > 10:
        st.markdown(background_style, unsafe_allow_html=True)
        st.markdown(f"###### Call ID - {cleaned_url}")
        st.markdown(f"<div class='custom-red-background'>id_1_1_Fail<br>Reason - (call is over 10 sec and Agent Started Speaking after 10 sec)<br>Agent Started At {first_start_timestamp_mono_left}</div>", unsafe_allow_html=True)

        st.write(f"<div class='custom-red-background'>id_1_1_Fail<br>Reason - (call is over 10 sec and Agent Started Speaking after 10 sec)<br>Agent Started At {first_start_timestamp_mono_left}</div>", unsafe_allow_html=True)

        # with st.write("id_1_1_Fail"):
        #     # Display additional information
        #     st.info("Reason - (call is over 10 sec and Agent Started Speaking after 10 sec)")
            # # Display text with blue and red colors
            # st.markdown(f"Agent Started At {first_start_timestamp_mono_left} <span style='color:blue'>blue</span> and <span style='color:red'>red</span>.")
            # # Display text with a custom background
            # st.write(f"<div class='custom-background'>Agent Started At {first_start_timestamp_mono_left} .</div>")
            # # Display a warning message
            # st.warning("Playing First 15 seconds of audio")



        # st.write(f"<div class='custom-red-background'>id_1_1_Fail</div>", unsafe_allow_html=True)



    
        # st.info(f"Reason - (call is over 10 sec and Agent Started Speaking after 10 sec)")
        # st.markdown(f"Agent Started At {first_start_timestamp_mono_left} <span style='color:blue'>blue</span> and <span style='color:red'>red</span>.", unsafe_allow_html=True)
        # st.write(f"<div class='custom-background'>Agent Started At {first_start_timestamp_mono_left} .</div>", unsafe_allow_html=True)
        # st.warning("Playing First 15 seconds of audio")
        
        # st.warning("")

        # print(f"id_1_1_Fail")
        # print(f"(Reason - call is over 10 sec and Agent Started Speaking after 10 sec)")
        # print(f"Agent Started At {first_start_timestamp_mono_left}")

        # print("Playing First 15 seconds of audio")
        # print()
        play_from=0
        play_till=15

        audio =(f'./output_files/{cleaned_url}_left.mp3')
        st.write(f"<div class='custom-red-background'>Agent Clip</div>", unsafe_allow_html=True)

        y, sr=librosa.load(audio)
        start_sample = int(play_from *sr)
        end_sample = int(play_till *sr)


        # Extract the desired segment of the audio
        clip = y[start_sample:end_sample]
        #display(Audio(data=clip, rate=sr, autoplay=False))
        with st.container():
            st.markdown(f"<div style='background-color:#ff85a1; padding-top: 10px;'>", unsafe_allow_html=True)
            st.audio(clip, sample_rate=sr)
            st.markdown(f"<div style='background-color: #ff85a1; padding-bottom: 10px;padding-top: 0px;'>", unsafe_allow_html=True)




        st.write(f"<div class='custom-red-background'>Orignal Clip</div>", unsafe_allow_html=True)

        audio =(f'./output_files/{cleaned_url}.mp3')
        y, sr=librosa.load(audio)
        start_sample = int(play_from *sr)
        end_sample = int(play_till *sr)



        # Extract the desired segment of the audio
        clip = y[start_sample:end_sample]
        background_color = "red"

        with st.container():
            st.markdown(f"<div style='background-color:#ff85a1; padding-top: 10px;'>", unsafe_allow_html=True)
            st.audio(clip, sample_rate=sr)
            st.markdown(f"<div style='background-color: #ff85a1; padding-bottom: 10px;padding-top: 0px;'>", unsafe_allow_html=True)


            #display(Audio(data=clip, rate=sr, autoplay=False))
    else:
        st.markdown(background_style, unsafe_allow_html=True)

        st.markdown(f"<div class='custom-green-background'>id_1_1_Pass</div>", unsafe_allow_html=True)



    # for i in unique_urls:


    # dataframes=empty_response_time_df[empty_response_time_df['url']==i]
    # mono_left_df = dataframes[dataframes['channel'] == 'Mono_Left']
    # first_start_timestamp_mono_left = mono_left_df['start'].iloc[0]
    # call_duration = pd.to_numeric(mono_left_df['call_duration'].iloc[0])
    # # print(call_duration)
    # # print(first_start_timestamp_mono_left)

    # if first_start_timestamp_mono_left>10 and call_duration > 10:

    #     print(f"id_1_1_Fail")
    #     print(f"(Reason - call is over 10 sec and Agent Started Speaking after 10 sec)")
    #     print(f"Agent Started At {first_start_timestamp_mono_left}")

    #     print("Playing First 15 seconds of audio")
    #     print()
    #     play_from=0
    #     play_till=15


    #     pattern = re.compile(r'https://s3-ap-southeast-1\.amazonaws\.com/exotelrecordings/futwork1/|\.mp3$')
    #     cleaned_url = re.sub(pattern, '',i)
    #     audio =(f'./output_files/{cleaned_url}_left.mp3')
    #     print("Agent Clip")
    #     y, sr=librosa.load(audio)
    #     start_sample = int(play_from *sr)
    #     end_sample = int(play_till *sr)


    #     # Extract the desired segment of the audio
    #     clip = y[start_sample:end_sample]
    #     display(Audio(data=clip, rate=sr, autoplay=False))



    #     print("Orignal Clip")

    #     audio =(f'./output_files/{cleaned_url}.mp3')
    #     y, sr=librosa.load(audio)
    #     start_sample = int(play_from *sr)
    #     end_sample = int(play_till *sr)



    #     # Extract the desired segment of the audio
    #     clip = y[start_sample:end_sample]
    #     display(Audio(data=clip, rate=sr, autoplay=False))
    # else:
    #     print("id_1_1_Pass")
    #     print()

   
    # Additional visualization options (uncomment to enable)

    # # Bar chart example
    # st.bar_chart(df[selected_cols])

    # # Text data display example
    # st.write(df[["Overall Emotion (Total)", "Overall Emotion (Mono Right)", "Overall Emotion (Mono Left)"]])

# Create Streamlit web app

st.sidebar.title("Upload Processed CSV")

# Define variables
df = None
unique_urls = None

# File uploader for selecting CSV file
csv_file = st.sidebar.file_uploader("CSV file", type=["csv"])
# empty_response_time_df.to_csv(csv_file, index=False)

# # # Display buttons for each unique URL when CSV file is uploaded
if csv_file is not None:

    df, unique_urls = process_csv(csv_file)
    # Display buttons for each unique URL
    for url in unique_urls:
        if st.sidebar.button(url):
            navigate_to_url_page(url, df)

# # # Check if query parameter contains selected URL
# if "url" in st.experimental_get_query_params():
#     selected_url = st.experimental_get_query_params()["url"]
#     st.write(f"Selected URL: {selected_url}")
