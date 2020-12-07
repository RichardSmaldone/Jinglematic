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

https://github.com/vivjay30/pychorus
pychorus

pip install git+https://github.com/RichardSmaldone/pychorus@master


necessary modules:
    
pip install pydub
pip install pyloudnorm
pip install git+https://github.com/steinbachr/pychorus



"""

import librosa,librosa.display
import numpy as np
import soundfile as sf
from os.path import isfile, join
from os import listdir, path, remove
import os


from pydub import AudioSegment
import pychorus as pyc
#from pychorus.helpers import find_and_output_chorus_nparray
import pandas as pd
import matplotlib.pyplot as plt
import pyloudnorm as pyln


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


# 0-5

NumJingle = 5
include_upbeats = False
tightness = 200
bellvol_adj = 1  # higher values reduce volume of bells.  (1 - 4)




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
print("It works best on songs with very slow tempos.")
print("Default: no")
UpbeatInput = input("(y)es  or (n)o: ")


if UpbeatInput.lower()=='y': include_upbeats = True

if JingleInput in str([1,2,3,4,5,6]): NumJingle = int(JingleInput) - 1
else: NumJingle = 5

'''


songs_path = dname + '/source files/'
ps_files_path = dname + '/output files/'
jingle_path = dname + '/SFX/jingle/'
detection_mode = 'bells'

# Get the song files from given dir
song_files = [f for f in listdir(songs_path) if isfile(join(songs_path, f))]

# fetch the bells
jingle = [j for j in sorted(listdir(jingle_path)) if isfile(join(jingle_path,j))]
      
# fetch the horses
clipclop, sr = librosa.load(dname +"/SFX/clipclop2.wav", sr=44100)
churchbells, sr = librosa.load(dname +"/SFX/churchbells.wav", sr=44100)          

# each sleighbell sound effect is ever so slightly off the beat
# this finetunes the timing so they hit directly on downbeats
finetune = [3,3,7,3,5,3]

count = len(song_files)
# Process each song file
for i, song_file in enumerate(song_files):
    print(str(i+1) + "/" + str(count) + " Processing song: ", song_file)
    song_file_path = songs_path + "/" + song_file
    output_file = ps_files_path + "/" + song_file

    # Load file
    xy, sr = librosa.load(song_file_path, sr=44100)
    bell, sr = librosa.load(jingle_path + jingle[NumJingle], sr=None)


    # calculate the average loudness of the track to help set jingle audio levels
    meter = pyln.Meter(sr) # create BS.1770 meter
    loudness = meter.integrated_loudness(xy) # measure loudness
    
    # sloppy curve fitting to slightly adjust bell volume based on detected loudness
    bellvol_adj = 4.02933 + (1.128807 - 4.02933)/(1 + (-loudness/15.20084)**22.80542)
    
    print("Average track loudness: " + str(round(loudness,1)) + " dB")
    
    meter = pyln.Meter(sr) # create BS.1770 meter
    loudness = meter.integrated_loudness(bell) # measure loudness
    
    print("Bell loudness: " + str(round(loudness,1)) + " dB.  Adjusted loudness: " + str(round(meter.integrated_loudness(bell/bellvol_adj),1)) + " dB.")
    
    
    
    
    # Find the best chorus time
    #chorus_start_sec = pyc.find_and_output_chorus_nparray(xy, sr , output_file + "_chorus_np.wav", 15)
    
    #pyc.create_chroma()
    #pyc.find_chorus(chroma, sr, song_length_sec, clip_length)
    
    
    ## So since pychorus can only find one chorus per audio file
    ## I could divide the audio files into half with np.split, and find the best chorus in first and second half
    ## and add clipclops to both.  Or parameterize it into several splits.
    
    # take it apart
    xy1, xy2 = np.array_split(xy,2)
    
    # put 'er back together
    #xyc = np.concatenate((xy1,xy2))

    chorus_start_1 = pyc.find_and_output_chorus_nparray(xy1, sr, output_file + "_chorus_1st half.wav", 10)
    chorus_start_2 = pyc.find_and_output_chorus_nparray(xy2, sr, output_file + "_chorus_2nd half.wav", 10)
    
    
    """
    chorus 1 & 2
    35.74421735030646
    64.24673357131631
    """
    
    """    
    
    xy1, xy2, xy3 = np.array_split(xy,3)
    
    chorus_start_sec = pyc.find_and_output_chorus_nparray(xy1, sr, output_file + "_chorus_1.wav", 10)
    chorus_start_sec = pyc.find_and_output_chorus_nparray(xy2, sr, output_file + "_chorus_2.wav", 10)   
    chorus_start_sec = pyc.find_and_output_chorus_nparray(xy3, sr, output_file + "_chorus_3.wav", 10)
    
    """
        
    """
    "" and fourths
    xy1, xy2, xy3,xy4 = np.split(xy,4)
    
    chorus_start_sec = pyc.find_and_output_chorus_nparray(xy1, sr, output_file + "_chorus_1.wav", 10)
    chorus_start_sec = pyc.find_and_output_chorus_nparray(xy2, sr, output_file + "_chorus_2.wav", 10)   
    chorus_start_sec = pyc.find_and_output_chorus_nparray(xy3, sr, output_file + "_chorus_3.wav", 10)
    chorus_start_sec = pyc.find_and_output_chorus_nparray(xy4, sr, output_file + "_chorus_4.wav", 10)
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
        beat_frames = beat_frames[beat_frames > 0]
        
        # Get the beat times and create click track
        beat_times = librosa.frames_to_time(beat_frames)
        
        
        chorus1_start_frame = librosa.time_to_frames(chorus_start_1,sr)

        clipclop_frames = beat_frames[beat_frames > chorus1_start]      
        
        # limit it to 32 clipclops
        clipclop_frames = clipclop_frames[clipclop_frames < clipclop_frames[32]]
        
        # build the clipclop track (with slight frame adjustment)
        clip_clops = librosa.clicks(frames=clipclop_frames+3, sr=sr, click = clipclop, length=len(xy))

        # drop in some churchbells to keep the horses company on the 1st and 16th beat of the chorus
        
        indices = [0,15]
              
        church_bells = librosa.clicks(frames=np.take(clipclop_frames, indices), sr=sr, click = churchbells, length=len(xy))


        # pull the bells out where clipclops exist. 
        beat_frames = [i for i in beat_frames if i not in clipclop_frames]
        
        # make the jingle track
        beat_clicks = librosa.clicks(frames=beat_frames, sr=sr, click = bell, length=len(xy))

        #chorus2_start_frame = librosa.time_to_frames(chorus_start_2,sr)
        #chorus2_end_frame = 

        # we have the times of the two best choruses in the 1st & 2nd halfs
        # delete from beat_clicks where frames between start and end
        # then for the clipclop track
        # delete from clip_clop where frames NOT between start and end



 
        #if tempo <=105: 
        #   include_upbeats = True
        #   print("BPM <= 100, automatically doubling the jingles for your convenience")

        if include_upbeats == True:
            
            # half the distance between each detected beat
            upbeat_frames = (beat_frames[1:] + beat_frames[:-1]) / 2

            # Get the upbeat times and create click track
            upbeat_times = librosa.frames_to_time(upbeat_frames)
            upbeat_clicks = librosa.clicks(frames=upbeat_frames, sr=sr, click = bell, length=len(xy))
            
            mixed = xy + (beat_clicks/bellvol_adj) + (upbeat_clicks/bellvol_adj)
        
        else:        
            mixed = xy + (beat_clicks/bellvol_adj) + clip_clops +  church_bells
            
           

        
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
    plt.title(song_file + ' Tightness: ' + str(tightness))
    
    '''
    y, sr = librosa.load(librosa.ex('choice'), duration=10)
    fig, ax = plt.subplots(nrows=3, sharex=True, sharey=True)
    librosa.display.waveplot(y, sr=sr, ax=ax[0])
    ax[0].set(title='Monophonic')
    ax[0].label_outer()
    '''  
   
    print("Done.\n")