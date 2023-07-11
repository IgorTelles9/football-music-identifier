#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 11:00:04 2023

@author: igortb
"""

import os
from tqdm import tqdm
import numpy as np 
import matplotlib.pyplot as plt
from scipy.io import wavfile
from python_speech_features import mfcc, logfbank
import pandas as pd
import librosa 

def envelope(y, rate, threshold):
    mask = []
    y = pd.Series(y).apply(np.abs)
    y_mean = y.rolling(window=int(rate/10), min_periods=1, center=True).mean()
    for mean in y_mean:
        if(mean > threshold):
            mask.append(True)
        else:
            mask.append(False)
    return mask



def base_gen(filename):
    df = pd.read_csv(filename+"2.csv")
    df.set_index("fname", inplace=True)
    for f in df.index:
        if (f == ".DS_Store"):
            continue
        rate, signal = wavfile.read("wav/"+f)
        df.at[f, "length"] = signal.shape[0]/rate
    
    if len([file for file in os.listdir(filename+"_files/") if file.endswith('.wav')]) == 0:
        for f in tqdm(df.index):
            if (f == ".DS_Store"):
                continue
            signal, rate = librosa.load("wav/"+f, sr=16000)
            mask = envelope(signal, rate, 0.0005)
            wavfile.write(filename=filename+"_files/"+f, rate=rate, 
                          data=signal[mask])

base_gen("training")
#base_gen("testing")