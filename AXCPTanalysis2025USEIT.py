#!/usr/bin/env python
# coding: utf-8

# In[12]:

    
# DATA HERE
# https://ohsuitg-my.sharepoint.com/:f:/r/personal/burgosp_ohsu_edu/Documents/Analysis/SpeechAutomaticity/DataSpeechAutomaticity?csf=1&web=1&e=O49vFY

#!pip install pyaudio
#!pip install pydub
#!conda install -c conda-forge ffmpeg
#!pip install simpleaudio
#!pip install noisereduce
#!pip install SpeechRecognition

#BAD EXAMPLE<  AUT_205_Visit1_0_240321_0929.xlsx
# GOD EXAMPLE 


#%% get files from server In[14]:


from glob import glob
import pandas as pd

inohsu=False

if inohsu:
    files = glob(r"\\rdsmsb.ohsu.edu\bdlab\Data\R01 Automaticity\AUT_*\Visit*\Audio\*.mp3", recursive = True)
    
    filesdf = pd.DataFrame(files)
    filesdf = filesdf[~filesdf[0].str.contains('AUT_000')]
    filesdf = filesdf[~filesdf[0].str.contains('AUT_001')]
    filesdf = filesdf[~filesdf[0].str.contains('Visit3')]
    filesdf = filesdf[~filesdf[0].str.contains('Visit4')]
    filesdf.to_excel("filesAnalysis.xlsx")
    
    files = list(filesdf[0])
    
    
    
    
    fipre = files[0]
    xfip = fipre.split("\\")
    participantpre = xfip[-4]+xfip[-3]
    
    info = []
    cond =-1
    
    
    for fi in files:
        ###
        dffi=pd.DataFrame()
        xfi = fi.split("\\")
        dffi ['participant'] = [xfi[-4]]
        dffi ['visit'] = [xfi[-3]]
        
        if xfi[-4]+xfi[-3] == participantpre:
            cond += 1
            
        else:
            cond =0
        #condition = xfi[-1].split("_")[0] # seated, walking, turning
        dffi ['condition'] = cond
        dffi ['namefile'] = [xfi[-1][0:-4]]
    
    
        dffi ['audio_file'] =  [fi]
        info.append(dffi)
        
        # if xfi[-4] != participantpre:
        #     participantpre = xfip[-4]
        #     visitpre = xfip[-3]
        #     cond = 0
    
    
        participantpre = xfi[-4]+xfi[-3]
        
    infof = pd.concat(info,ignore_index=1)   
    
    
    infof.to_excel("files_info.xlsx")
else:
    infof = pd.read_excel("files_info.xlsx")

#used = set()

#files = [x for x in files if x not in used and (used.add(x) or True)]

#files


# In[15]:


# from pydub import AudioSegment
# from pydub.playback import play

# #mp3_file = "./audiotest/AUT_000/Visit1/Audio/230808_1309.mp3"
# mp3_file = files[0]
# print(mp3_file)
# audio = AudioSegment.from_file(mp3_file, format='mp3')




#play(audio)



#pydub.AudioSegment.ffmpeg = "/absolute/path/to/ffmpeg"
#audio = AudioSegment.from_mp3("test.mp3")


#%% main loop 


from pydub import AudioSegment
if not inohsu:
    AudioSegment.converter = '/opt/homebrew/opt/ffmpeg/bin/ffmpeg'  # Replace with your actual path

import noisereduce as nr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as style

from pydub.silence import detect_nonsilent
import pydub.scipy_effects
from scipy import signal

import speech_recognition as sr
from pydub.playback import play

import pandas as pd
from supportFunctions import sound_peaks_detection
import shutil



# shutil.copyfile(src, dst)
dst = 'C:/Users/burgosp/OneDrive - Oregon Health & Science University/Analysis/SpeechAutomaticity/DataSpeechAutomaticity'




style.use('ggplot')

#%%ONEFILE




subexc = infof.participant.isin(["AUT_015","AUT_016","AUT_216","AUT_217","AUT_218","AUT_219"])
filexc = infof.namefile.isin(['240626_0905'])

infof = infof[(~subexc)&(~filexc)]

startstop = pd.read_excel('startstop3.xlsx')


# onefile = 0
# infof = infof.iloc[onefile:onefile+1,:]

infof = infof.iloc[149:168,:]
#%%
# fi = files[0]
errors1=[]
errors2=[]


    #%% first try getting onsets and voice recognition

for fi,participant,visit,condition,namefile in  zip(infof.audio_file,infof.participant,infof.visit,infof.condition,infof.namefile):
    
    #%%
    print(fi)
    condition = str(condition)
    if inohsu:
        shutil.copy2(fi, dst)
    
    silence_threshPB=-40
    th0 = 15
    if participant == 'AUT_002':
        th0 = 1 #15
    try:
        xfi = fi.split("\\")
        # participant = xfi[-4]
        # visit = xfi[-3]
        #condition = xfi[-1].split("_")[0] # seated, walking, turning
        # condition = xfi[-1][0:-4]
        # namefile = xfi[-1][0:-4]
        print(namefile)
        
        audio_file =  fi
        #audio = AudioSegment.from_file(audio_file) #wav{¿}
        
        if inohsu:
            audio = AudioSegment.from_file(audio_file, format='mp3')
        else:
            audio_file= './DataSpeechAutomaticity/' + namefile + '.mp3'
            audio = AudioSegment.from_file(audio_file, format='mp3')
        samples = np.array(audio.get_array_of_samples())
        times  = np.linspace(0,len(audio)/1000,len(samples))
        
        plt.figure()
        plt.plot(times,samples)
        plt.xticks(np.arange(0,times[-1],5),rotation=90)
        plt.show()
        
        block5 = np.arange(0,times[-1],5)
        ener5 =[]
        for ch in block5:
            ener5.append((np.max(samples[(times>=ch) & (times<=ch+5)])-
                         np.min(samples[(times>=ch) & (times<=ch+5)]))*-1                         
                         )
        plt.plot(ener5)
        idxener = ener5<np.percentile(ener5, 25)
        idxener2 = np.where(np.diff(idxener))
        
        # start = block5[idxener2[0][0]]
        # stop = block5[idxener2[0][1]]+5
        
        
        start = startstop.on1.values[startstop.file == fi][0]
        stop = startstop.off1.values[startstop.file == fi][0]
        print("start and stop: " + str(start) + " " + str(stop))    
        
        # start = input("choose the starting point in secs: ")
        # stop  = input("choose the end point in secs: ")
        
        no1 = (int(start)-2)*int(audio.frame_rate)
        no2 = int(start)*int(audio.frame_rate)
        no3 = int(stop)*int(audio.frame_rate)
        noisy_part = samples[no1:no2]   # audio before the first letter with the baclgroud noise, no speech
        noisy_part0 = audio[no1:no2]
        play(noisy_part0)
        # no1 = int(start)*int(audio.frame_rate)
        # no2 = (int(start)+2)*int(audio.frame_rate)
        # noisy_part = samples[no1:no2] 
        
        audio = audio[no1:no3]

        reduced_noise = nr.reduce_noise(y = samples, sr=audio.frame_rate, 
                                        y_noise = noisy_part, n_std_thresh_stationary=1.5,stationary=True)
        reduced_audio = AudioSegment(
            reduced_noise.tobytes(), 
            frame_rate=audio.frame_rate, 
            sample_width=audio.sample_width, 
            channels=audio.channels
        )
        audio_file_out =   "./audiotest/"+namefile+"_wo_noise.wav"  
        reduced_audio.export(audio_file_out,format="wav")
    
        #% Detect non-silent chunks
        audio1 = reduced_audio
        samples = np.array(audio1.get_array_of_samples())
        times  = np.linspace(0,len(audio1)/1000,len(samples))
    
        dBFS=audio1.dBFS
    
        #nonsilent_data = detect_nonsilent(audio1, min_silence_len=50, silence_thresh=dBFS-abs(dBFS/3), seek_step=1)#strict
        #nonsilent_data = detect_nonsilent(audio1, min_silence_len=50, silence_thresh=dBFS-abs(dBFS/2), seek_step=1)
        # nonsilent_data = detect_nonsilent(audio1, min_silence_len=30, silence_thresh=dBFS-abs(dBFS), seek_step=1)
        nonsilent_data = detect_nonsilent(audio1, min_silence_len=30, silence_thresh=silence_threshPB, seek_step=1)
#Decibels are a logarithmic scale, so -10dB would be equivalent to 1/10th of full volume, -20dB is 1/100th of full volume, -30 is 1/1000th, and so on.
        
        # Print start and stop times of non-silent chunks
        onset=[]
        ofset=[]
        segments = []
        peaks1 = []
        #print("Start, Stop")
        for chunks in nonsilent_data:
            on2 = np.where(times==times[times>=chunks[0]/1000][0])[0][0]
            of2 = np.where(times==times[times>=chunks[1]/1000][0])[0][0]
            s = samples[on2:of2]
            onset.append(on2)
            ofset.append(of2)    
            # energy by chunk
            segments.append(np.sum(np.abs(s)))
            peaks1.append(np.max(np.abs(s)))
            #print([chunk/1000 for chunk in chunks])
    
        # th0=16
        # Plot the audio data
        plt.figure()
        plt.plot(times,samples)
        plt.plot(times[onset],samples[onset],"bo")
        plt.plot(times[ofset],samples[ofset],"yo")
        plt.show()
    
        segments = np.array(segments)
        peaks1 = np.array(peaks1)
        xt = np.arange(0,len(segments))
        plt.figure()
        plt.plot(xt,peaks1)
    
        segments1 = segments.copy()   # non mod
        x = np.arange(0,len(segments))
        
        th = min(segments1) + ((max(segments1)-min(segments1))*(th0/100)) #5%
        #th = (max(segments)-min(segments))/20 #5%
        idth = segments<th
        
        #print plot(segments)
        plt.figure()
        plt.plot(xt,segments)
        plt.plot(xt[idth],segments[idth],"bo")
        plt.show()
    
        #clean onset ofset
        onset2 = onset.copy()
        ofset2 = ofset.copy()
        onset2 = np.array(onset2)[~idth]
        ofset2 = np.array(ofset2)[~idth]
        
        #onset2 = onset2[onset2>int(start)*int(audio.frame_rate)]  #OCT2025
        # onset2 = onset2[onset2<int(stop)*int(audio.frame_rate)]
        
        #ofset2 = ofset2[ofset2>int(start)*int(audio.frame_rate)]  #OCT2025
        # ofset2 = ofset2[ofset2<int(stop)*int(audio.frame_rate)]
    
        plt.figure()
        plt.plot(times,samples)
        plt.plot(times[onset2],samples[onset2],"bo")
        plt.plot(times[ofset2],samples[ofset2],"yo")
        plt.show()
        
        #delete extra onsets  Commented OCT2025
        # if np.any(np.diff(onset2)>160000):
        #     prepost=np.argwhere(np.diff(onset2)>160000)
        #     if len(prepost)<2:
        #         if prepost[0][0] <10:
        #             onset2 = onset2[prepost[0][0]+1:]
        #             ofset2 = ofset2[prepost[0][0]+1:]
        #         else:
        #             onset2 = onset2[:prepost[-1][0]]
        #             ofset2 = ofset2[:prepost[-1][0]]                    
        #     else:
        #         onset2 = onset2[prepost[0][0]+1:prepost[-1][0]]
        #         ofset2 = ofset2[prepost[0][0]+1:prepost[-1][0]]
    
        # plt.figure()
        # plt.plot(times,samples)
        # plt.plot(times[onset2],samples[onset2],"bo")
        # plt.plot(times[ofset2],samples[ofset2],"yo")
        # plt.show()    
        
        #% #####VALERIO##### peaks detection
        audio = AudioSegment.from_file(audio_file_out)
        peaks_list = []
        properties_list = []
        for n_on in range(len(onset2)):
            print(n_on)
            selected_audio_segment = audio[int(times[onset2[n_on]]*1000)-50:int(times[ofset2[n_on]]*1000)+100]
            samples_sa = np.array(selected_audio_segment.get_array_of_samples())
            times_sa  = np.linspace(times[onset2[n_on]],times[ofset2[n_on]],len(samples_sa))
            # plt.figure()
            # plt.plot(times_sa-times_sa[0],samples_sa)
            peaks, properties = sound_peaks_detection(samples_sa,0)
            peaks_list.append(peaks)
            properties_list.append(properties)
            
        save_ind = []
        for i in range(0, len(peaks_list), 1):  
            if len(peaks_list[i]) > 1:  
                save_ind.append(i)

        #1 detect chunks with 2 peaks
        #2 separate using the pydub functiondetect_nonsilent
        # nonsilent_data = detect_nonsilent(audio1, min_silence_len=30, silence_thresh=-80, seek_step=1)
        #% 2b remove noisy values over min noisy part, and below max noisy part
        
        # samples_wn[(samples_wn>min(noisy_part))&(samples_wn<max(noisy_part))]=0
        nonsilent_corrupted_chunks = []
        for n_on in save_ind:
            print(n_on)
            selected_audio_segment = audio[int(times[onset2[n_on]]*1000)-50:int(times[ofset2[n_on]]*1000)+100]
            samples_sa = np.array(selected_audio_segment.get_array_of_samples())
            times_sa  = np.linspace(times[onset2[n_on]],times[ofset2[n_on]],len(samples_sa))
            # plt.figure()
            # plt.plot(times_sa-times_sa[0],samples_sa)
            nonsilent_corrupted_chunks.append(detect_nonsilent(selected_audio_segment, min_silence_len=3, silence_thresh=-80, seek_step=1))
       
        
        
        ######VALERIO##### peaks detection   
        
        #%% Load audio file  CLEAN GOOGLE
        audio = AudioSegment.from_file(audio_file_out)
        print(namefile)
    
        r = sr.Recognizer()
        non =0
        #non2=len(ofset2)-1
    
        base1= int(times[onset2[non]]*1000)-100
        base0= base1-3000
    
        baseline = audio[base0:base1]
        play(baseline)
    
    
        out_letters=[]
        baseline = audio[base0:base1]
        for n_on in range(len(onset2)):
            print(n_on)
            selected_audio_segment = audio[int(times[onset2[n_on]]*1000)-50:int(times[ofset2[n_on]]*1000)+100]
            #selected_audio_segment = audio[int(times[onset2[0]]*1000)-250:int(times[ofset2[0]]*1000)+2000]
            selected_audio_segment=baseline.append(selected_audio_segment.append(baseline))
    
            selected_audio_segment.export("test.wav", format='wav')
            with sr.AudioFile("test.wav") as source:
                audio3 = r.record(source)  # read the entire audio file
    
            #goo = r.recognize_google(audio3)
            #goo2 = goo.split()
            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                goo = r.recognize_google(audio3)
                goo2 = goo.split()
                out_letters.append(goo2[0])
                print("Google Speech Recognition thinks you said " + goo)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                out_letters.append(None)
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                out_letters.append(None)
    
        #%% Load audio file  RAW GOOGLE
        audio = AudioSegment.from_file(audio_file)
        print(namefile)
    
    
        out_lettersb=[]
    
        for n_on in range(len(onset2)):
            print(n_on)
            selected_audio_segment = audio[int(times[onset2[n_on]]*1000)-50:int(times[ofset2[n_on]]*1000)+100]
            #selected_audio_segment = audio[int(times[onset2[0]]*1000)-250:int(times[ofset2[0]]*1000)+2000]
            selected_audio_segment=baseline.append(selected_audio_segment.append(baseline))
    
            selected_audio_segment.export("test.wav", format='wav')
            with sr.AudioFile("test.wav") as source:
                audio3 = r.record(source)  # read the entire audio file
    
            #goo = r.recognize_google(audio3)
            #goo2 = goo.split()
            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                goo = r.recognize_google(audio3)
                goo2 = goo.split()
                out_lettersb.append(goo2[0])
                print("Google Speech Recognition thinks you said " + goo)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                out_lettersb.append(None)
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                out_lettersb.append(None)
    

        #%% Load audio file CLEAN AZURE
        AZURE_SPEECH_KEY = "cf360caff7d747a18dc11ae18d700e07"  # Microsoft Speech API keys 32-character lowercase hexadecimal strings
        AZURELOCATION = "eastus"
        
        audio = AudioSegment.from_file(audio_file_out)
        print(namefile)
    
        r = sr.Recognizer()
    
        out_letters2=[]
    
        baseline = audio[base0:base1]
        for n_on in range(len(onset2)):
            print(n_on)
            selected_audio_segment = audio[int(times[onset2[n_on]]*1000)-50:int(times[ofset2[n_on]]*1000)+100]
            #selected_audio_segment = audio[int(times[onset2[0]]*1000)-250:int(times[ofset2[0]]*1000)+2000]
            selected_audio_segment=baseline.append(selected_audio_segment.append(baseline))
    
            selected_audio_segment.export("test.wav", format='wav')
            with sr.AudioFile("test.wav") as source:
                audio3 = r.record(source)  # read the entire audio file
    
            try:
                print(r.recognize_azure(audio3, key=AZURE_SPEECH_KEY,location=AZURELOCATION))
                #print("Microsoft Azure Speech thinks you said " + r.recognize_azure(audio3, key=AZURE_SPEECH_KEY,location=AZURELOCATION))
                az = r.recognize_azure(audio3, key=AZURE_SPEECH_KEY,location=AZURELOCATION)
                out_letters2.append(az)
            except sr.UnknownValueError:
                print("Microsoft Azure Speech could not understand audio")
                out_letters2.append(None)
            except sr.RequestError as e:
                print("Could not request results from Microsoft Azure Speech service; {0}".format(e))
                out_letters2.append(None)
    
        #%% Load audio file RAW AZURE
        audio = AudioSegment.from_file(audio_file)
        print(namefile)
    
        r = sr.Recognizer()
    
        out_letters2b=[]
    
        baseline = audio[base0:base1]
        for n_on in range(len(onset2)):
            print(n_on)
            selected_audio_segment = audio[int(times[onset2[n_on]]*1000)-50:int(times[ofset2[n_on]]*1000)+100]
            #selected_audio_segment = audio[int(times[onset2[0]]*1000)-250:int(times[ofset2[0]]*1000)+2000]
            selected_audio_segment=baseline.append(selected_audio_segment.append(baseline))
    
            selected_audio_segment.export("test.wav", format='wav')
            with sr.AudioFile("test.wav") as source:
                audio3 = r.record(source)  # read the entire audio file
    
            try:
                print(r.recognize_azure(audio3, key=AZURE_SPEECH_KEY,location=AZURELOCATION))
                #print("Microsoft Azure Speech thinks you said " + r.recognize_azure(audio3, key=AZURE_SPEECH_KEY,location=AZURELOCATION))
                az = r.recognize_azure(audio3, key=AZURE_SPEECH_KEY,location=AZURELOCATION)
                out_letters2b.append(az)
            except sr.UnknownValueError:
                print("Microsoft Azure Speech could not understand audio")
                out_letters2b.append(None)
            except sr.RequestError as e:
                print("Could not request results from Microsoft Azure Speech service; {0}".format(e))
                out_letters2b.append(None)        
    
    
#%%mixing google and azure  
  
        df = pd.DataFrame(out_letters)
        df.columns = ["google"]
        df["google2"] = out_lettersb
    
        out_letters3 = []
        for ou in out_letters2:
            try:
                out_letters3.append(ou[0])
            except:
                out_letters3.append("None")
    
        out_letters4 = []
        for ou in out_letters2b:
            try:
                out_letters4.append(ou[0])
            except:
                out_letters4.append("None")
    
        df["azure"] = out_letters3
        df["azure2"] = out_letters4
        df["time"]= times[onset2]
    
        df.to_excel("./reports/output1_letters_"+ participant +"_"+ visit +"_"+ condition +"_"+namefile+".xlsx")
    except:
        errors1.append(participant +"_"+ visit +"_"+ condition +"_"+namefile)
        continue
#%% second try getting RT and correct yes answers
    try:
        yes= ((df.google=="yes") | (df.google2=="yes") 
        |    (df.google=="yes yes") | (df.google2=="yes yes") 
        |    (df.google=="cast") | (df.google2=="cast")
        |    (df.azure=="Yeah.") | (df.azure2=="Yeah.")
        |    (df.azure=="Yes.") | (df.azure2=="Yes."))
    
        hey= ((df.google=="hey") | (df.google2=="hey")
        |   (df.google=="a") | (df.google2=="a") 
        |   (df.azure=="Hey.") | (df.azure2=="Hey.")
        |   (df.azure=="A.") | (df.azure2=="A."))
    
        #fakehey0
        #fakehey1
    
        iii= ((df.google=="I") | (df.google2=="hi")
        | (df.google=="hi") | (df.google2=="I") 
        | (df.azure=="I.") | (df.azure2=="I.")
        | (df.azure=="Eye.") | (df.azure2=="Eye.")
        | (df.azure=="Ay.") | (df.azure2=="Ay.")
        | (df.azure=="Aye.") | (df.azure2=="Aye."))  
    
        yesi = np.where(yes)[0]
    
    
        heyi = np.where(hey)[0]
    
    
        #iiii = np.where(iii)[0]
    
    
        right=0
        rt = []
        for yi in yesi:
            if yi<len(out_letters3)-2:
                if hey[yi-2] and iii[yi-1]:
                    right+=1
                    rt.append(df.time.iloc[yi]-df.time.iloc[yi-1])
    
        print("right answers")        
        print(right)
        print("total yes number")
        print(len(yesi))
    
        error1 = len(yesi)-right
    
        error = 0 # omision
    
        for he in heyi:
            if he<len(out_letters3)-2 :
                if ((iii[he+1]) and not(yes[he+2])):
                    print(he)
                    error+=1
        print("error extra yes")        
        print(error1)
        print("error missing yes")
        print(error)
        print("mean RT")
        print(np.mean(rt))
        print("std RT")
        print(np.std(rt))
    
        d = {"Sub_ID":[participant],"visit":[visit],"condition":[condition],"file":[namefile],"right answers":[right],"total yes number":[len(yesi)], 
            "error extra yes":[error1],"error missing yes":[error],
             "mean RT":[np.mean(rt)],"std RT":[np.std(rt)]}
        dfd = pd.DataFrame.from_dict(d, orient='columns')
        dfd.to_excel("./reports/output2_rt_"+ participant +"_"+ visit +"_"+ condition +"_"+namefile+".xlsx")
    except:
        errors2.append(participant +"_"+ visit +"_"+ condition +"_"+namefile)
        continue
    ###


# In[19]:




