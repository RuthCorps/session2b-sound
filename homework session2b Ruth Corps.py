import csv
import os
from pydub import AudioSegment, silence
from pydub.playback import play
from matplotlib.pyplot import plot, show

path_to_repository = "/Users/rcorps/Documents/IMPRS Python/session_2 /session2b-sound"

# This piece of code is here to help you.
# It reads a text file with information about the stimuli you are going to split (names & condition),
# and returns a dictionary named 'stimuli' with condition as key, and the word itself as value.
# Use this dictionary to name the files you have to save.
stimuli_info = open(os.path.join(path_to_repository, "lexdec_stimuli.txt"))
stimuli_reader = csv.reader(stimuli_info, delimiter=',')
headers = next(stimuli_reader, None)

# Create the dictionary
stimuli = {}
for stimulus in stimuli_reader:
    if stimulus[2] not in stimuli.keys():
        stimuli[stimulus[2]] = list()
    stimuli[stimulus[2]].append(stimulus[3])

# Put them in alphabetical order
for condition, words in stimuli.items():
    sort = sorted(words)
    stimuli[condition] = sort

# change the non-word condition name
stimuli["NW"] = stimuli.pop("none")

# where are the sound files? 
sound_folder = "/Users/rcorps/Documents/IMPRS Python/session_2 /session2b-sound/raw"

# make new folders
new_folder_HF = "/Users/rcorps/Documents/IMPRS Python/session_2 /session2b-sound/HF"
if not os.path.isdir(new_folder_HF):
    os.mkdir(new_folder_HF)
new_folder_LF = "/Users/rcorps/Documents/IMPRS Python/session_2 /session2b-sound/LF"
if not os.path.isdir(new_folder_LF):
    os.mkdir(new_folder_LF)
new_folder_NW = "/Users/rcorps/Documents/IMPRS Python/session_2 /session2b-sound/NW"
if not os.path.isdir(new_folder_NW):
    os.mkdir(new_folder_NW)

# where are the sound files?
sound_folder = "/Users/rcorps/Documents/IMPRS Python/session_2 /session2b-sound/raw"

# Open the high frequency audio 
High_path = os.path.join(sound_folder, "HF_recording.wav")
High_sound = AudioSegment.from_wav(High_path)
Low_path = os.path.join(sound_folder, "LF_recording.wav")
Low_sound = AudioSegment.from_wav(Low_path)
None_path = os.path.join(sound_folder, "NW_recording.wav")
None_sound = AudioSegment.from_wav(None_path)

# split the words
High_words = silence.split_on_silence(High_sound, min_silence_len=200, silence_thresh=-50)
Low_words = silence.split_on_silence(Low_sound, min_silence_len=200, silence_thresh=-50)
None_words = silence.split_on_silence(None_sound, min_silence_len=200, silence_thresh=-50)

norm_HF = []
norm_LF = []
norm_NW = []

# normalise the volume
for word in High_words:
    target_volume = -10
    current_volume = word.dBFS
    change = target_volume - current_volume
    normalized_HF = word.apply_gain(change)
    norm_HF.append(normalized_HF)

for word in Low_words:
    target_volume = -10
    current_volume = word.dBFS
    change = target_volume - current_volume
    normalized_LF = word.apply_gain(change)
    norm_LF.append(normalized_LF)

for word in None_words: 
    target_volume = -10
    current_volume = word.dBFS
    change = target_volume - current_volume
    normalized_NW = word.apply_gain(change)
    norm_NW.append(normalized_NW)

# export to the folders
for i in range(len(norm_HF)):
    sound = norm_HF[i]
    filename = stimuli['HF'][i] + ".wav"
    sound.export(os.path.join(new_folder_HF, filename))

for i in range(len(norm_LF)):
    sound = norm_LF[i]
    filename = stimuli['LF'][i] + ".wav"
    sound.export(os.path.join(new_folder_LF, filename))

for i in range(len(norm_NW)):
    sound = norm_NW[i]
    filename = stimuli['NW'][i] + ".wav"
    sound.export(os.path.join(new_folder_NW, filename))
