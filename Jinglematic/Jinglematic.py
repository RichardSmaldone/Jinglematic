"""

Credits:

freewavesamples.com

https://stackoverflow.com/questions/59544098/rhythm-detection-with-python    
Rhythm detection with python

https://github.com/csteinmetz1/pyloudnorm
audio levelling

https://github.com/vivjay30/pychorus
pychorus

https://stackoverflow.com/questions/57082826/how-can-a-chromagram-file-produced-by-librosa-be-interpreted-as-a-set-of-musical
key detection


required modules:
    
pip install librosa
pip install soundfile  (dont need)   
pip install pydub
pip install pyloudnorm
pip install git+https://github.com/RichardSmaldone/pychorus@master
"""

# Clear variables
from IPython import get_ipython
get_ipython().magic('reset -sf')

import librosa,librosa.display
import numpy as np
import soundfile as sf
from os.path import isfile, join
from os import listdir, path, remove
from tkinter import filedialog
from tkinter import *
import os


from pydub import AudioSegment
import pychorus as pyc
import matplotlib.pyplot as plt
import pyloudnorm as pyln
import random as rnd


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


# 0-5

NumJingle = 5
include_upbeats = False
tightness = 200
bellvol_adj = 1  # higher values reduce volume of bells.  (1 - 4)
rnd.seed()


# Bring up the file dialog to load the audio file
root = Tk()
root.update()
root.file =  filedialog.askopenfilename(initialdir = "/",title = "Select music to be jingled",filetypes = (("Audio files",".mp3 .wav .flac .m4a .aac"),("all files","*.*")))
root.destroy()

xy, sr = librosa.load(root.file, sr=44100)

# print (root.filename)
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

song_file_path = root.file
#output_file = root.file + "_jingled.mp3"
song_file = os.path.basename(root.file)
song_name = os.path.splitext(song_file)[0]
output_file = os.path.dirname(root.file) + "/" + os.path.splitext(song_file)[0] + "_jingled.mp3"
os.path.dirname(root.file)



# be nice to remember the directory, so just wipe out chorus_start_1 & 2

"""v
# To use a source directory rather than file dialog
songs_path = dname + '/source files/'
# Get the song files from given dir
song_files = [f for f in listdir(songs_path) if isfile(join(songs_path, f))]

count = len(song_files)

# Process each song file
for i, song_file in enumerate(song_files):
    print(str(i+1) + "/" + str(count) + " Processing song: ", song_file)
    song_file_path = songs_path + "/" + song_file
    output_file = ps_files_path + "/" + song_file
 """
hype =  rnd.randint(1,5)
 
if hype == 1:
    print("\n" + song_name + "!  One of the elves' favorites, you've got great taste.")
elif hype == 2:
    print("\nI just talked to Santa and he said that " + song_name + " totally slaps.")   
elif hype == 3:
    print("\nFun fact, " + song_name + " was basically my college anthem.")    
elif hype == 4:
    print("\nThe reindeer can't stop dancing every time " + song_name + " comes on the radio.  Fact.")    
elif hype == 5:
    print("\nNow jingling some Christmas cheer into " + song_name)    
    
    

ps_files_path = dname + '/output files/'
jingle_path = dname + '/SFX/jingle/'

# fetch the bells
jingle = [j for j in sorted(listdir(jingle_path)) if isfile(join(jingle_path,j))]
      
# fetch the horses
clipclop1, sr = librosa.load(dname +"/SFX/woodblock1.wav", sr=44100)
clipclop2, sr = librosa.load(dname +"/SFX/woodblock2.wav", sr=44100)
harp, sr = librosa.load(dname +"/SFX/harp.wav", sr=44100)
whip, sr = librosa.load(dname +"/SFX/whip.wav", sr=44100)
handbell, sr = librosa.load(dname +"/SFX/bell_c.wav", sr=44100)
hoho1, sr = librosa.load(dname +"/SFX/ho_01.wav", sr=44100)
hoho2, sr = librosa.load(dname +"/SFX/ho_02.wav", sr=44100)
hoho3, sr = librosa.load(dname +"/SFX/ho_03.wav", sr=44100)


# each sleighbell sound effect is ever so slightly off the beat
# this finetunes the timing so they hit directly on downbeats
finetune = [3,3,7,3,5,3]



# Load file
#xy, sr = librosa.load(song_file_path, sr=44100)
bell, sr = librosa.load(jingle_path + jingle[NumJingle], sr=44100)
sleighbell, sr = librosa.load(jingle_path + jingle[2], sr=44100)

# find tempo and beats
tempo, beat_frames = librosa.beat.beat_track(y=xy, sr=sr, tightness=tightness, trim=True)

# calculate the average loudness of the track to help set jingle audio levels
meter = pyln.Meter(sr) # create BS.1770 meter
loudness = meter.integrated_loudness(xy) # measure loudness

# sloppy curve fitting to slightly adjust bell volume based on detected loudness
bellvol_adj = 4.02933 + (1.128807 - 4.02933)/(1 + (-loudness/15.20084)**22.80542)

print("\nAverage track loudness: " + str(round(loudness,1)) + " dB")

#print(beat_times)
print("Tempo: " + str(round(tempo)) + " bpm.")

meter = pyln.Meter(sr) # create BS.1770 meter
loudness = meter.integrated_loudness(bell) # measure loudness

print("Bell loudness: " + str(round(loudness,1)) + " dB.  Adjusted loudness: " + str(round(meter.integrated_loudness(bell/bellvol_adj),1)) + " dB.")

# Determine the key of the song and load the appropriate church bells

# get song chroma
chroma_cq = librosa.feature.chroma_cqt(xy, sr)
song_chroma = list(np.mean(chroma_cq,1))
 
# pitches in 12 tone equal temperament 
pitches = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

# print note to value relations
# for y in range(len(song_chroma)):
#    print(str(pitches[y]) + '\t' + str(song_chroma[y]))

# select the most dominant pitch
pitch_id = song_chroma.index(max(song_chroma))
pitch = pitches[pitch_id]

min_third_id = (pitch_id+3)%12
maj_third_id = (pitch_id+4)%12

#check if the musical 3rd is major or minor
if song_chroma[min_third_id] < song_chroma[maj_third_id]:
    third = 'major'
    print(str.format('\nThis song is likely in {} {}',pitch, third))
elif song_chroma[min_third_id] > song_chroma[maj_third_id]:
    third = 'minor'
    print(str.format('\nThis song is likely in {} {}',pitch, third))
else:
    print(str.format('\nThis song might be in {} something???',pitch))
    
    
# if minor key go three half steps up.
if third == 'minor': 
    adj_key = pitch_id + 3
else:
    adj_key = pitch_id

if adj_key > 11:
    adj_key = adj_key - 12

songkey = pitches[adj_key]

if third == 'minor':
    print(str.format('Adjusted to {} major',pitches[adj_key]))

if adj_key > 6:
    adj_key = adj_key-12


# shift the pitch of the woodblocks so they're in key
# default key of C    
# pitches[0] is C   

#clipclop1 = librosa.effects.pitch_shift(clipclop1, sr, n_steps=adj_key, bins_per_octave=24) 
#clipclop2 = librosa.effects.pitch_shift(clipclop2, sr, n_steps=adj_key, bins_per_octave=24) 

   
# shift the pitch of the handbells so they're in key
# default key of C    
# pitches[0] is C   

handbell1 = librosa.effects.pitch_shift(handbell, sr, n_steps=adj_key, bins_per_octave=12) 
handbell2 = librosa.effects.pitch_shift(handbell, sr, n_steps=adj_key-5, bins_per_octave=12) 


#y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=4, bins_per_octave=24)   
churchbells, sr = librosa.load(dname +'/SFX//churchbells//churchbells_' + songkey + '.wav', sr=44100)  

#pyc.create_chroma()
#pyc.find_chorus(chroma, sr, song_length_sec, clip_length)
   
## So since pychorus can only find one chorus per audio file
## I could divide the audio files into half with np.split, and find the best chorus in first and second half
## and add clipclops to both.  Or parameterize it into several splits.

# take it apart
xy1, xy2 = np.array_split(xy,2)

# put 'er back together
#xyc = np.concatenate((xy1,xy2))

# it would be nice to find two choruses
# but we'll settle for one
chorus_start_1 = pyc.find_and_output_chorus_nparray(xy1, sr, None, 10) 
chorus_start_2 = None

if chorus_start_1 is None: 
    chorus_start_1 = pyc.find_and_output_chorus_nparray(xy, sr , None, 15)
else:
    chorus_start_2 = pyc.find_and_output_chorus_nparray(xy2, sr, None, 10)
    if chorus_start_2 != None:
            chorus_start_2 = chorus_start_2 + librosa.get_duration(xy1)

# if there's no chorus found at all, let's just pretend it's at the halfway mark.
if chorus_start_1 is None:
    chorus_start_1 = librosa.get_duration(xy,sr)/2       

print("Adding festive holiday cheer...")
    

# tweaking the beatmap just a pinch so the jingles land right on the beats
beat_frames = beat_frames - finetune[NumJingle]
 
# delete any that are less than zero after shifting
beat_frames = beat_frames[beat_frames > 0]
  
if tempo <= 100: 
   include_upbeats = True
   print("BPM <= 100, adding jingles on the upbeat")
         
if include_upbeats == True:
    upbeat_frames = (beat_frames[1:] + beat_frames[:-1]) / 2
    beat_frames = np.sort(np.concatenate((beat_frames,upbeat_frames)))
       

# Get the beat times and create click track
beat_times = librosa.frames_to_time(beat_frames)

# get frame start for chorus
librosa.time_to_frames(chorus_start_1, sr, hop_length=1024, n_fft=None)
chorus1_start_frame = librosa.time_to_frames(chorus_start_1,sr)

# add clipclops
clipclop_frames = beat_frames[beat_frames > chorus1_start_frame]      

# limit it to 32 clipclops
clipclop_frames = clipclop_frames[clipclop_frames < clipclop_frames[32]]

# and upbeats for a different clop sound
clipclop_upbeat_frames = (clipclop_frames[1:] + clipclop_frames[:-1]) / 2

# adding a second upbeat to emulate a horse cadence
clipclop_quarter_frames = clipclop_upbeat_frames[:-1] + np.diff(clipclop_upbeat_frames)/4        
clipclop_quarter_frames = np.concatenate((clipclop_quarter_frames[:8],clipclop_quarter_frames[20:28]))  
clipclop_upbeat_frames = np.sort(np.concatenate((clipclop_upbeat_frames,clipclop_quarter_frames)))
   
# add some jingle to the chorus downbeats.
# numpy gets sassy with mismatched array sizes, fill the short one with 0s
clipclop1 = clipclop1 + np.concatenate((sleighbell,np.zeros(len(clipclop1)-len(sleighbell))))

# build the clipclop track (with slight frame adjustment for timing)
clip_clops = librosa.clicks(frames=clipclop_frames, sr=sr, click = clipclop1, length=len(xy))        
clip_upclops = librosa.clicks(frames=clipclop_upbeat_frames, sr=sr, click = clipclop2, length=len(xy))

# Roll all the clipclops back together into a single array
clip_clops = clip_clops + clip_upclops
   
# let's drop in some churchbells to keep the horses company on the 1st and 16th beat of the chorus
# random hoho preceding chorus
hoho = eval("hoho" + str(rnd.randint(1,3)))       
harp_indices = [0,28]
whip_indices = [6,12,20]

harp_sound = librosa.clicks(frames=np.take(clipclop_frames, harp_indices), sr=sr, click = harp, length=len(xy))
whip_sound = librosa.clicks(frames=np.take(clipclop_frames, whip_indices), sr=sr, click = whip, length=len(xy))
hoho_sound = librosa.clicks(frames=librosa.time_to_frames(chorus_start_1-1,sr), sr=sr, click = hoho, length=len(xy))
   
# pull the jingles out where clipclops exist. 
beat_frames = np.array([i for i in beat_frames if i not in clipclop_frames]) 
 
# Drop in a second chorus if it exists
if chorus_start_2 != None:
    # get frame start for chorus to add clipclops 
    chorus2_start_frame = librosa.time_to_frames(chorus_start_2,sr,1024)
    clipclop_frames2 = beat_frames[beat_frames > chorus2_start_frame]  
    
    # limit it to 32 clipclops
    clipclop_frames2 = clipclop_frames2[clipclop_frames2 < clipclop_frames2[32]]

    # and upbeats for a different clop sound
    clipclop_upbeat_frames2 = (clipclop_frames2[1:] + clipclop_frames2[:-1]) / 2
    
    # adding a second upbeat to emulate a horse cadence
    clipclop_quarter_frames2 = clipclop_upbeat_frames2[:-1] + np.diff(clipclop_upbeat_frames2)/4     
    clipclop_quarter_frames2 = np.concatenate((clipclop_quarter_frames2[:8],clipclop_quarter_frames2[20:28]))   
    clipclop_upbeat_frames2 = np.sort(np.concatenate((clipclop_upbeat_frames2,clipclop_quarter_frames2)))

    # build the clipclop track (with slight frame adjustment for timing)
    clip_clops2 = librosa.clicks(frames=clipclop_frames2, sr=sr, click = clipclop1, length=len(xy))
    clip_upclops2 = librosa.clicks(frames=clipclop_upbeat_frames2, sr=sr, click = clipclop2, length=len(xy))
   
    clip_clops2 = clip_clops2 + clip_upclops2        

    # build the clipclop track (with slight frame adjustment for timing)
    clip_clops = clip_clops + clip_clops2
   
    # let's drop in some churchbells to keep the horses company on the 1st and 16th beat of the chorus
    # random hoho preceding chorus
    hoho = eval("hoho" + str(rnd.randint(1,3)))        
    harp_indices = [0,28]
    whip_indices = [6,12,20]
      
    harp_sound = harp_sound + librosa.clicks(frames=np.take(clipclop_frames2, harp_indices), sr=sr, click = harp, length=len(xy))
    whip_sound = whip_sound + librosa.clicks(frames=np.take(clipclop_frames2, whip_indices), sr=sr, click = whip, length=len(xy))
    hoho_sound = hoho_sound + librosa.clicks(frames=librosa.time_to_frames(chorus_start_2-1), sr=sr, click = hoho, length=len(xy))
   
    # pull the jingles out where clipclops exist. 
    beat_frames = np.array([i for i in beat_frames if i not in clipclop_frames2])
   
# make the jingle track
beat_clicks = librosa.clicks(frames=beat_frames, sr=sr, click = bell, length=len(xy))
   
# Add in some handbells tuned to the key of the song 
handbell_frames = beat_frames[::8]
handbell2_frames = beat_frames[4::8]

handbell1_sound = librosa.clicks(frames=handbell_frames, sr=sr, click = handbell1, length=len(xy))        
handbell2_sound = librosa.clicks(frames=handbell2_frames, sr=sr, click = handbell2, length=len(xy))      
   
handbell_sound = handbell1_sound + handbell2_sound      

# Combine all our ingredients together        
mixed = xy + (
        beat_clicks / bellvol_adj) + (
        clip_clops / (bellvol_adj * 2)) +  (
        harp_sound / (bellvol_adj * 2)) + (
        whip_sound / bellvol_adj) + (
        hoho_sound/ bellvol_adj +
        handbell_sound / (bellvol_adj * 10 )         
        ) 

sf.write(output_file + ".wav", mixed, sr)
AudioSegment.from_wav(output_file + ".wav").export(output_file, bitrate="192k", format="mp3") #   
os.remove(output_file + ".wav")
   
# ipd.display.Audio(filename=output_file + "_jingled.mp3",)
   
# check beat detection in the middle of the song 
# would be better to have it plot out the chorus but it'll do
chartstart = int(np.count_nonzero(xy)/2)

plt.figure(figsize=(14, 8))
librosa.display.waveplot(xy[chartstart:chartstart + 200000], alpha=0.6)#, ax=ax[0])
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