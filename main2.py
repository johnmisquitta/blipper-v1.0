
        #creates temp file
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as mono_temp_file:
            mono_temp_file_path = mono_temp_file.name
            stereo_audio.export(mono_temp_file_path, format="mp3")
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as mono_left_tempfile:
            left_tempfile_path = mono_left_tempfile.name
            mono_left.export(left_tempfile_path, format="mp3")
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as mono_right_tempfile:
            right_tempfile_path = mono_right_tempfile.name
            mono_right.export(right_tempfile_path, format="mp3")


        thread_left = threading.Thread(target=lambda:segmentation_mono_left(left_tempfile_path))
        thread_right = threading.Thread(target=lambda:segmentation_mono_right(right_tempfile_path))
        thread_left.start()
        thread_right.start()

        # Wait for both threads to finish
        thread_left.join()
        thread_right.join()
        completed_tasks += 1
        print(f"Completed tasks: {completed_tasks}/{num_tasks}")




        #audio, sr = librosa.load(mono_temp_file, sr=None)
        #audio_duration = librosa.get_duration(y=audio, sr=sr)

            # Split audio into mono channels
        stereo_audio.export(os.path.join(files_directory, mono_file))

        mono_audios = stereo_audio.split_to_mono()


        mono_left, mono_right = mono_audios[0].export(os.path.join(files_directory, mono_left_file) ), mono_audios[1].export(os.path.join(files_directory, mono_right_file))
        
        audio_left, sr_left = librosa.load(mono_left, sr=None)

    
        audio_right, sr_right = librosa.load(mono_right, sr=None)
        total_audio_duration = AudioSegment.from_file(os.path.join(files_directory, mono_file)).duration_seconds




        #AudioSegment.from_file(mono_audios)




        speech_data_left = [segment for segment, _ in monoleft_timestamp.itertracks()]
        speech_data_right = [segment for segment, _ in monoright_timestamp.itertracks()]
        # Create a dictionary with start and end times
        segments_dict_left = {'start': [segment.start for segment in speech_data_left],
                                'end': [segment.end for segment in speech_data_left]}
        segments_dict_right = {'start': [segment.start for segment in speech_data_right],
                            'end': [segment.end for segment in speech_data_right]}

        df_left = pd.DataFrame(segments_dict_left)

        df_left=pd.DataFrame(segments_dict_left)
        df_right=pd.DataFrame(segments_dict_right)



        # Create a dictionary with start and end times

        # Convert the dictionary to a pandas DataFrame

        # print(df_left)
        # print(df_right)


        # mono all dataframe
        combined_df = pd.concat([df_left, df_right], ignore_index=True)

        #sorted df
        mono_df = combined_df.sort_values(by='start')




        







        right_result = []
        right_result_lock = threading.Lock()

        left_result = []
        left_result_lock = threading.Lock()

        def process_audio(segments, audio, sr, channel, result_list, result_lock):
            for _, segment in segments.iterrows():
                segment_start, segment_end = segment['start'], segment['end']
                
                segment_start_sample = int(segment_start * sr)
                segment_end_sample = int(segment_end * sr)
                segment_audio = audio[segment_start_sample:segment_end_sample]


                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
                    temp = temp_audio_file.name
                    soundfile.write(temp, segment_audio, samplerate=sr)
                print(f"Channel : {channel}")

                print(f"Timestamps : start - {segment_start} end - {segment_end}")

                emotion = get_emotion(temp)
                print(f"Emotion : {emotion}")



                transcribe_left_file = Transcribe()
                transcript_left =transcribe_left_file.deepgram(temp)
                transcription =transcript_left[0]#  "sample_transcript"#transcript_left[0] # get_transcript(temp)
                print(f"Transcript :{transcription}")

                #sentiment
                sentiment=get_sentiment([transcription])
                sentiment_max_score = max(sentiment, key=lambda k: sentiment[k])

                print(f"Sentiments : {sentiment_max_score}")

                wpm=get_wpm(segment_start,segment_end,transcription)
                print(f"Talk Speed (WPM) : {wpm}")

                rms=calculate_rms_energy(temp)
                print(f"Energy Level (WPM) : {rms}")


                #features = calculate_audio_features(temp)

              

                with result_lock:
                    result_list.append({
                        'url': audio_file,
                        'channel': channel,
                        'start': segment_start.round(1),
                        'end': segment_end.round(1),
                        'emotion': emotion,
                        'transcript': transcription,
                        'sentiment':sentiment_max_score,
                        'words-per-min':wpm[0],
                        'pace':wpm[1],
                        'energy':rms
                        # 'total_audio_duration':total_audio_duration,
                        # 'signals':features[13],
                        # 'mfcc': features[0],
                        # 'l2_norm': features[1],
                        # 'rms': features[2],
                        # 'intensity': features[3],
                        # 'loudness_db': features[4],

                        # 'harmonic_energy': features[5],

                        # 'residual_energy': features[6],

                        # 'non_harmonic_energy': features[7],
                        # 'snr': features[8],
                        # 'jitter': features[9],
                        # 'shimmer': features[10],
                        # 'mfb': features[11],
                        # 'lpc': features[12]
                    })

        # Using ThreadPoolExecutor for parallel processing
                    
        segment_start=time.time()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submitting tasks for each segment in the left channel
            futures_left = [executor.submit(process_audio, df_left, audio_left, sr_left, 'Mono_Left', left_result, left_result_lock)]

            # Submitting tasks for each segment in the right channel
            futures_right = [executor.submit(process_audio, df_right, audio_right, sr_right, 'Mono_Right', right_result, right_result_lock)]

            # Wait for all tasks to complete in both channel
            concurrent.futures.wait(futures_left + futures_right)
        segment_end=time.time()

        print(f"Emotion Time = {segment_end-segment_start}")
        

        # Optionally, you can process the aggregated results in right_result
                

            # Optionally, you can process the aggregated results in right_result
            #print(right_result)

            # Optionally, you can process the aggregated results in left_result
            #print(left_result)




    # Optionally, you can process the aggregated results in right_result
        # print(left_result)
        # print(right_result)
        left_result_df=pd.DataFrame(left_result)
        right_result_df=pd.DataFrame(right_result)
        common_column = 'start'

    # Merge the DataFrames
    # merged_df = pd.merge(left_result_df, right_result_df, on=common_column, how='inner')

        global emotion_append_to_csv_df

        # emotion_append_to_csv_df.append(left_result_df)
        # emotion_append_to_csv_df.append(right_result_df)
        emotion_append_to_csv_df = emotion_append_to_csv_df.append(left_result_df, ignore_index=True)
        emotion_append_to_csv_df = emotion_append_to_csv_df.append(right_result_df, ignore_index=True)


        # Merge the resulting DataFrame with the left result DataFrame
        # merged_df = merged_df.append(left_result_df, ignore_index=True)

        # # Sort the merged DataFrame based on the 'start' column
        # emotion_sorted_df_to_csv = merged_df.sort_values(by='start')

        # # If you want to reset the index after sorting
        # emotion_sorted_df_to_csv.reset_index(drop=True, inplace=True)

        # emotion_append_to_csv_df=emotion_append_to_csv_df.append(emotion_sorted_df_to_csv)

        # Display the sorted DataFrame


        # temp_emotion_append_to_csv_df_right = emotion_append_to_csv_df.append(right_result_df, ignore_index=True)

        # temp_emotion_append_to_csv_df_left = emotion_append_to_csv_df.append(left_result_df, ignore_index=True)
        # combined_emotion__df_to_csv = pd.merge(temp_emotion_append_to_csv_df_left, temp_emotion_append_to_csv_df_right, on='key', how='inner')  # You can choose the type of join (inner, outer, left, right)


        




        # try:
        #     existing_df = pd.read_csv(raw_csv)
            
        #     # Append the new DataFrame to the existing one
        #     combined_df = existing_df.append(left_result_df, ignore_index=True)
            
        #     # Write the combined DataFrame back to the CSV file
        #     combined_df.to_csv(raw_csv, index=False)
        
        # # If the file doesn't exist, create it and write the DataFrame to it
        # except FileNotFoundError:
        #     left_result_df.to_csv(raw_csv, index=False)

            # Try to read the existing CSV file





        file_paths = [mono_right_file]
        

        #csv_file_path = 'emotion_matrics.csv'
        #emotion_append_to_csv_df = emotion_append_to_csv_df.sort_values(by='start')

        #emotion_append_to_csv_df = emotion_append_to_csv_df.sort_values(by='start')
        #emotion_append_to_csv_df.to_csv(csv_file_path, index=False)


        # Sort by 'start' column


    # Save the sorted DataFrame to a CSV file



        start=time.time()



        overall_emotion="nutral"#get_emotion(f"{files_directory}/{mono_file}")
        overall_emotion_left="nutral"#get_emotion(f"{files_directory}/{mono_left_file}")
        overall_emotion_right="nutral"#get_emotion(f"{files_directory}/{mono_right_file}")
        # overall_emotion = threading.Thread(target=lambda:get_emotion(f"{files_directory}/{mono_file}"))
        # overall_emotion_left = threading.Thread(target=lambda:get_emotion(f"{files_directory}/{mono_left_file}"))
        # overall_emotion_right = threading.Thread(target=lambda:get_emotion(f"{files_directory}/{mono_right_file}"))

        # overall_emotion.start()
        # overall_emotion_left.start()
        # overall_emotion_right.start()

        # # Wait for both threads to finish
        # overall_emotion.join()
        # overall_emotion_left.join()
        # overall_emotion_right.join()


        end_time=time.time()
        print(f"Overall emotion time {end_time-start}")


        overlaps_df = pd.DataFrame(columns=['start', 'end', 'duration'])

        

        segment_start=time.time()
        for index1, row1 in df_left.iterrows():
            for index2, row2 in df_right.iterrows():
                # Find the overlapping duration
                #overlap_duration=overlap_duration(row1['start'],row1['end'],row2['start'],row2['end'],)
                overlap_start = max(row1['start'], row2['start'])
                overlap_end = min(row1['end'], row2['end'])

                # Check if there is an overlap and it meets the threshold
                overlap_duration = overlap_end - overlap_start
                if overlap_start < overlap_end and overlap_duration >= 1:
                    overlaps_df = overlaps_df.append({'start': overlap_start, 'end': overlap_end, 'duration': overlap_duration}, ignore_index=True)

        segment_end=time.time()

        print(f"Overlap Time = {segment_end-segment_start}")


        #Print the dataframe with overlapping durations


        # set the threshold for overlap duration
        overlaps_df = pd.DataFrame(columns=['start', 'end', 'duration', 'overlapping_df'])

        segment_start=time.time()

        for index_left, row_left in df_left.iterrows():
            for index_right, row_right in df_right.iterrows():
                # find the overlapping duration
                overlap_start = max(row_left['start'], row_right['start'])
                overlap_end = min(row_left['end'], row_right['end'])

                # check overlap threshold
                overlap_duration = overlap_end - overlap_start
                if overlap_start < overlap_end and overlap_duration >= 1:

                    # which data frame overlapped with the other
                    if row_left['start'] <= row_right['start']:
                        overlapping_df = 'Mono_Right'
                    else:
                        overlapping_df = 'Mono_Left'

                    overlaps_df = overlaps_df.append({
                        'start': overlap_start,
                        'end': overlap_end,
                        'duration': overlap_duration,
                        'overlapping_df': overlapping_df
                    },ignore_index=True)#, ignore_index=True
        segment_end=time.time()

        print(f"Who overlapped Whoom Time = {segment_end-segment_start} seconds")





        mono_left_df = overlaps_df[overlaps_df['overlapping_df'] == 'Mono_Left']
        mono_right_df = overlaps_df[overlaps_df['overlapping_df'] == 'Mono_Right']



        df_left['duration'] = df_left['end'] - df_left['start']

        print(audio_file)

        total_time_left = df_left['duration'].sum()
        df_right['duration'] = df_right['end'] - df_right['start']
        total_time_right = df_right['duration'].sum()
        total_time=total_time_left+total_time_right
        print(f"Total Call Duration : {round(total_time/60,2)} Minutes")
        count_items_mono_overlaps_df=len(overlaps_df)
        sum_duration_mono = overlaps_df['duration'].sum()
        print("Total Overlaps :", count_items_mono_overlaps_df,"Times")
        print("Total Overlaps Duration :", round(sum_duration_mono/60,2),"Minutes")
        print(f"Mono Right :\nTalk Duration : {round(total_time_right/60,2)} Minutes | Talk Percent {round(total_time_right/total_time*100,2)} %")
        count_items_mono_right = len(mono_right_df)
        # Sum the duration
        sum_duration_mono_right = mono_right_df['duration'].sum()
        # Print the results
        print("Total Overlaps by Mono_Right :", count_items_mono_right,"Times")
        print("Total Overlaps Duration by Mono_Right", round(sum_duration_mono_right/60,2),"Minutes")
        print(f"Total Overlaps Duration by Mono_Right Duration : {round(sum_duration_mono_right/60,2)} Minutes | Percent {round((sum_duration_mono_right/60)/(total_time_right/60)*100,2)} %")
        count_items_mono_left = len(mono_left_df)
        # Sum the duration
        sum_duration_mono_left = mono_left_df['duration'].sum()
        print(f"Mono Left :\nTalk Duration : {round(total_time_left/60,2)} Minutes | Talk Percent {round(total_time_left/total_time*100,2)} %")
        # Print the results
        print("Total Overlaps by Mono_Left :", count_items_mono_left,"Times")
        print("Total Overlaps Duration by Mono_Right", round(sum_duration_mono_left/60,2),"Minutes")
        print(f"Total Overlaps Duration by Mono_Left Duration : {round(sum_duration_mono_left/60,2)} Minutes | Percent {round((sum_duration_mono_left/60)/(total_time_left/60)*100,2)} %")

        print("_______________________________________________________________________________________________________")
            #max_emotions_all = max(set(emotions_all), key=emotions_all.count)
            #max_emotions_left = max(set(emotions_left), key=emotions_left.count)
            #max_emotions_right = max(set(emotions_right), key=emotions_right.count)
        #print("raw_martrics_df")
        

        segment_start=time.time()
        
        # total_talk_duration = f"{round(total_time/60,2)} Minutes"
        # total_talk_percent = f"{round(total_time/60,2)/(total_audio_duration/60)*100} %"
        # total_overlaps = f"{count_items_mono_overlaps_df} Times"
        # total_overlaps_duration = f"{round(sum_duration_mono/60,2)} Minutes"
        # total_overlaps_percent = f"{round((sum_duration_mono_right/60)/(total_time_right/60)*100,2)} %"

        # mono_right_talk_duration = f"{round(total_time_right/60,2)} Minutes"
        # mono_right_talk_percent = f"{round(total_time_right/total_time*100,2)} %"
        # mono_right_total_overlaps = f"{count_items_mono_right} Times"
        # mono_right_overlaps_duration = f"{round(sum_duration_mono_right/60,2)} Minutes"
        # mono_right_overlaps_percent = f"{round((sum_duration_mono_right/60)/(total_time_right/60)*100,2)} %"

        # mono_left_talk_duration = f"{round(total_time_left/60,2)} Minutes"
        # mono_left_talk_percent = f"{round(total_time_left/total_time*100,2)} %"
        # mono_left_total_overlaps = f"{count_items_mono_left} Times"
        # mono_left_overlaps_duration = f"{round(sum_duration_mono_left/60,2)} Minutes"
        # mono_left_overlaps_percent = f"{round((sum_duration_mono_left/60)/(total_time_left/60)*100,2)} %"
        segment_end=time.time()

        print(f"Matrics calculation Time = {segment_end-segment_start} seconds")


        
        # Specify the CSV file path

        print("raw"*20)


        # matrics = []
        # matrics.append({
        #     'Link': audio_file,
        #     'Total Call Duration':f"{round(total_audio_duration/60,2)} Minutes",
        #     'Total Talk Duration': total_talk_duration-sum_duration_mono,
        #     'Talk Duration - Mono Right': mono_right_talk_duration,
        #     'Talk Duration - Mono Left': mono_left_talk_duration,
        #     'Talk Percent - Total': total_talk_percent,
        #     'Talk Percent - Mono Right': mono_right_talk_percent,
        #     'Talk Percent - Mono Left': mono_left_talk_percent,
        #     'Total Overlaps - Total': total_overlaps,
        #     'Total Overlaps - Mono Right': mono_right_total_overlaps,
        #     'Total Overlaps - Mono Left': mono_left_total_overlaps,
        #     'Overlaps Duration - Total': total_overlaps_duration,
        #     'Overlaps Duration - Mono Right': mono_right_overlaps_duration,
        #     'Overlaps Duration - Mono Left': mono_left_overlaps_duration,
        #     'Overlaps Percent - Total': total_overlaps_percent,
        #     'Overlaps Percent - Mono Right': mono_right_overlaps_percent,
        #     'Overlaps Percent - Mono Left': mono_left_overlaps_percent,
        #     'Overall Emotion - Total': overall_emotion,
        #     'Overall Emotion - Mono Right': overall_emotion_left,
        #     'Overall Emotion - Mono Left': overall_emotion_right
        # })
        # print("raw"*20)

        # martrics_df=pd.DataFrame(matrics)

        #     # Append the second dataframe to the first one
        # global output_metric_append_to_csv_df
        # output_metric_append_to_csv_df = output_metric_append_to_csv_df.append(martrics_df, ignore_index=True)

        # print("raw"*20)



        # ##################

        segment_start=time.time()

        total_talk_duration = total_time
        total_talk_percent = (total_time)/(total_audio_duration)
        total_overlaps = count_items_mono_overlaps_df
        total_overlaps_duration = sum_duration_mono
        total_overlaps_percent = sum_duration_mono/(total_time_right+total_time_right)

        mono_right_talk_duration = total_time_right
        mono_right_talk_percent = total_time_right/total_time
        mono_right_total_overlaps = count_items_mono_right
        mono_right_overlaps_duration = sum_duration_mono_right
        mono_right_overlaps_percent = (sum_duration_mono_right)/(total_time_right)

        mono_left_talk_duration = total_time_left
        mono_left_talk_percent = total_time_left/total_time
        mono_left_total_overlaps = count_items_mono_left
        mono_left_overlaps_duration = sum_duration_mono_left
        mono_left_overlaps_percent = (sum_duration_mono_left)/(total_time_left)
        segment_end=time.time()

        print(f"Raw matrics Time = {segment_end-segment_start} seconds")

        print("raw"*20)

        raw_matrics = []
        raw_matrics.append({
            'Link': audio_file,
            'Total Audio Duration':total_audio_duration,
            'Total Talk Duration': total_talk_duration-sum_duration_mono,###checkpoint
            'Talk Duration - Mono Right': mono_right_talk_duration,
            'Talk Duration - Mono Left': mono_left_talk_duration,
            'Talk Percent - Total': total_talk_percent,
            'Talk Percent - Mono Right': mono_right_talk_percent,
            'Talk Percent - Mono Left': mono_left_talk_percent,
            'Total Overlaps - Total': total_overlaps,
            'Total Overlaps - Mono Right': mono_right_total_overlaps,
            'Total Overlaps - Mono Left': mono_left_total_overlaps,
            'Overlaps Duration - Total': total_overlaps_duration,
            'Overlaps Duration - Mono Right': mono_right_overlaps_duration,
            'Overlaps Duration - Mono Left': mono_left_overlaps_duration,
            'Overlaps Percent - Total': total_overlaps_percent,
            'Overlaps Percent - Mono Right': mono_right_overlaps_percent,
            'Overlaps Percent - Mono Left': mono_left_overlaps_percent,
            'Overall Emotion - Total': overall_emotion,
            'Overall Emotion - Mono Right': overall_emotion_right,
            'Overall Emotion - Mono Left': overall_emotion_left
        })
        raw_martrics_df=pd.DataFrame(raw_matrics)
        global raw_output_metric_append_to_csv_df
        raw_output_metric_append_to_csv_df = raw_output_metric_append_to_csv_df.append(raw_martrics_df, ignore_index=True)





