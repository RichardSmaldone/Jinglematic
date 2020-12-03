"""
todo:
   
parameterize the bell sfx  (DONE)
    
jingle_05 - double
jingle_06 - long (use when tempo is low)
---------

Jingle bells aren't precisely on the beat.  trim a few ms off. (DONE)
---------

detect upbeats and add option to place sfx there (DONE)

--------

upbeat bells when tempo is slow (Won't Do)

-------

Volume levelling

mp3 track levels vary considerably.

detected average loudness

base the bellvolume as a number inverse to the loudness.


-------

find notable events via volume spikes and insert fx


mir_eval has a few functions:
    
    segment, pattern, 

-------

isolate bass track and insert ho's 

-------

triplets?  Just do what you did for upbeats but divide by three?

-------

random intro and outro sfx

-------

use pychorus to add a little pizazz to the chorus (clipclops?)

-------

create UI - IN PROGRESS

----
compile into executable
    

Credits:

freewavesamples.com

https://stackoverflow.com/questions/59544098/rhythm-detection-with-python    
"Rhythm detection with python"

https://github.com/csteinmetz1/pyloudnorm
audio levelling



"""

import librosa,librosa.display
import numpy as np
import soundfile as sf
from os.path import isfile, join
from os import listdir, path, remove
import os
from pydub import AudioSegment
import pychorus
import pandas as pd
import matplotlib.pyplot as plt
import pyloudnorm as pyln


# 0-5

NumJingle = 5
include_upbeats = True
tightness = 200
bellvolume = 1  # higher values reduce volume of bells.


'''
print("Jingle 1: Default")
print("Jingle 2: Brief")
print("Jingle 3: Retro")
print("Jingle 4: Brief")
print("Jingle 5: The Double Jingle")
print("Jingle 6: High Fidelity")
print("Default: 6")
JingleInput = input("Select your jingle (1-6): ")

print()
print("Do you want to include jingles on the upbeats too?")
print("It works best on songs withr very slow tempos.")
print("Default: no")
UpbeatInput = input("(y)es  or (n)o: ")


if UpbeatInput.lower()=='y': include_upbeats = True

if JingleInput in str([1,2,3,4,5,6]): NumJingle = int(JingleInput) - 1
else: NumJingle = 5

'''


SONGS_PATH = "./Kringle/source files"
PS_FILES_PATH = "./Kringle/output files"
jingle_path = "./Kringle/SFX/jingle/"
detection_mode = "bells"

# Get the song files from given dir
song_files = [f for f in listdir(SONGS_PATH) if isfile(join(SONGS_PATH, f))]

# fetch the bells
jingle = [j for j in sorted(listdir(jingle_path)) if isfile(join(jingle_path,j))]
                
finetune = [3,3,7,3,5,3]

count = len(song_files)
# Process each song file
for i, song_file in enumerate(song_files):
    print(str(i+1) + "/" + str(count) + " Processing song: ", song_file)
    song_file_path = SONGS_PATH + "/" + song_file
    output_file = PS_FILES_PATH + "/" + song_file

    # Load file
    xy, sr = librosa.load(song_file_path, sr=44100)
    bell, sr = librosa.load(jingle_path + jingle[NumJingle], sr=None)
    clipclop, sr = librosa.load("./Kringle/SFX/clipclop.wav", sr=44100)

    # calculate the average loudness of the track to help set jingle audio levels
    meter = pyln.Meter(sr) # create BS.1770 meter
    loudness = meter.integrated_loudness(xy) # measure loudness


    print(loudness)
    
    """ 
        # Get the onset times
        onset_times = librosa.frames_to_time(onset_frames)
        onset_clicks = librosa.clicks(frames=onset_frames, sr=sr3, click = bell2, length=len(xy))
    
        # find tempo and beats
        tempo, beat_frames = librosa.beat.beat_track(y=xy, sr=sr)
        
        # Get the beat times
        beat_times = librosa.frames_to_time(beat_frames)
        beat_clicks = librosa.clicks(frames=beat_frames, sr=sr, click = bell, length=len(xy))
        
        # librosa.core.clicks(times=None, frames=None, sr=22050, hop_length=512, click_freq=1000.0, click_duration=0.1, click=None, length=None)
        # bell must be a numpy.ndarray
    """

    # Generate a txt file which is contains times, and create a audio file with click effect.
    print("Adding festive holiday cheer...")
    if detection_mode == "only-onsets":
        
        # Find onsets
        onset_frames = librosa.onset.onset_detect(xy, sr=sr, wait=1, pre_avg=1, post_avg=1, pre_max=1, post_max=1)
    
        # Get the onset times
        onset_times = librosa.frames_to_time(onset_frames)
        onset_clicks = librosa.clicks(frames=onset_frames, sr=sr3, click = bell2, length=len(xy))
        sf.write(output_file + "_onset_clicks.wav", xy + onset_clicks, sr)
            
        #librosa.output.write_wav(output_file + " - onset_clicks.wav", xy + onset_clicks, sr)
        file = open(output_file + "_onset_times.txt","ab")
        np.savetxt(file, onset_times, '%.2f') 
        
    elif detection_mode == "bells":
        
        # find tempo and beats
        tempo, beat_frames = librosa.beat.beat_track(y=xy, sr=sr, tightness=tightness, trim=True)
        
        # tweaking the beatmap just a pinch so the jingles land right on the beats
        beat_frames = beat_frames - finetune[NumJingle]
        
        # delete any that are less than zero after shifting
        mask = beat_frames > 0
        beat_frames = beat_frames[mask]
        
        # Get the beat times and create click track
        beat_times = librosa.frames_to_time(beat_frames)
        beat_clicks = librosa.clicks(frames=beat_frames, sr=sr, click = bell, length=len(xy))

 
        #if tempo <=105: 
        #   include_upbeats = True
        #   print("BPM <= 100, automatically doubling the jingles for your convenience")

        if include_upbeats == True:
            
            # half the distance between each detected beat
            upbeat_frames = (beat_frames[1:] + beat_frames[:-1]) / 2

            # Get the upbeat times and create click track
            upbeat_times = librosa.frames_to_time(upbeat_frames)
            upbeat_clicks = librosa.clicks(frames=upbeat_frames, sr=sr, click = bell, length=len(xy))
            
            mixed = xy + beat_clicks + upbeat_clicks
        
        else:        
            mixed = xy + beat_clicks/bellvolume
            #mixed = librosa.effects.remix(mixed, intervals[::-1])

        
        sf.write(output_file + ".wav", mixed, sr)
        AudioSegment.from_wav(output_file + ".wav").export(output_file + "_jingled.mp3", bitrate="192k", format="mp3") #
        #file = open(output_file + "_beat_times.txt","ab")
        #np.savetxt(file, beat_times, '%.2f')       
        os.remove(output_file + ".wav")

       # ipd.display.Audio(filename=output_file + "_jingled.mp3",)


        #print(beat_times)
        print("Tempo: " + str(round(tempo)) + " bpm.")
        # calculate the upbeats by returning exactly half the distance between each beat
        # easy enough???
        
    elif detection_mode == "sleigh":
        
        # find tempo and beats
        tempo, beat_frames = librosa.beat.beat_track(y=xy, sr=sr)
    
        # Get the beat times
        beat_times = librosa.frames_to_time(beat_frames)
        
        beat_clicks = librosa.clicks(frames=beat_frames, sr=sr, click = clipclop, length=len(xy))
        
        mixed = xy + beat_clicks # combine audio with click track
        sf.write(output_file + ".wav", mixed, sr)
        AudioSegment.from_wav(output_file + ".wav").export(output_file + "_sleigh_ride.mp3", bitrate="192k", format="mp3") #
        #file = open(output_file + "_beat_times.txt","ab")
        #np.savetxt(file, beat_times, '%.2f')       
        os.remove(output_file + ".wav")
        
    else:
        
        # Get the onset times
        onset_times = librosa.frames_to_time(onset_frames)
        onset_clicks = librosa.clicks(frames=onset_frames, sr=sr, click = bell, length=len(xy))

        # find tempo and beats
        tempo, beat_frames = librosa.beat.beat_track(y=xy, sr=sr)
    
        # Get the beat times
        beat_times = librosa.frames_to_time(beat_frames)
        beat_clicks = librosa.clicks(frames=beat_frames, sr=sr, click = clipclop, length=len(xy))
    
        mixed = xy + beat_clicks + onset_clicks # combine audio with click track
        sf.write(output_file + ".wav", mixed, sr)
        AudioSegment.from_wav(output_file + ".wav").export(output_file + "_full_clicks.mp3", bitrate="192k", format="mp3") #
        #file = open(output_file + "_beat_times.txt","ab")
        #np.savetxt(file, beat_times, '%.2f')       
        os.remove(output_file + ".wav") 
   
    
    # check beat detection for beginning of song    
    plt.figure(figsize=(14, 8))
    librosa.display.waveplot(xy[:500000], alpha=0.6)#, ax=ax[0])
    plt.vlines(beat_times, -1, 1, color='r')
    plt.ylim(-1, 1)
    plt.title('Tightness: ' + str(tightness))
    
    '''
    y, sr = librosa.load(librosa.ex('choice'), duration=10)
    fig, ax = plt.subplots(nrows=3, sharex=True, sharey=True)
    librosa.display.waveplot(y, sr=sr, ax=ax[0])
    ax[0].set(title='Monophonic')
    ax[0].label_outer()
    '''  
   
    print("Done.\n")