# Speech-Dual-Task-AX-CPT
The code is using speech recognition libraries to get reaction times and errors from audio files, getting the cognitive performance using the audio version of the AX-CPT cognitive task. 
AX Continuous Performance Test (AX-CPT) is a task where people see two letters in a row (or listen in our case), first a cue and then a target (or also known as "probe"). The task was originally designed by Rosvold and his colleagues at Yale University. In this task, people must press a target button only when they see A followed by X. All other pairs (e.g., A–Y, B–X, B–Y) require a different or no response. It tests how well people use context (the first letter) to decide how to respond to the second.
In our case, we use the pair A-I, and the response was verbal, saying YES only after listening to A-I.

The libraries used are,

pyaudio == #!pip install pyaudio
pydub == 0.25.1 #!pip install pydub
ffmpeg #!conda install -c conda-forge ffmpeg, DOWNLOAD FFMPGE FOR YOUR OS https://www.ffmpeg.org/download.html
simpleaudio ==  #!pip install simpleaudio
noisereduce == 3.0.3 #!pip install noisereduce
SpeechRecognition == 3.14.2 #!pip install SpeechRecognition,  google and azure
glob == 
pandas == 2.2.2
numpy == 
scipy == 
