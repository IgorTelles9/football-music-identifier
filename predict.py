#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 28 20:01:17 2023

@author: igortb
"""

import os
from scipy.io import wavfile
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from keras.models import load_model
from tqdm import tqdm
from python_speech_features import mfcc
import pickle
from sklearn.metrics import accuracy_score


def build_predictions(audios_dir):
    y_true = []
    y_pred = []
    fn_prob = {}
    print("Extracting features from audio")
    dsstore = os.path.join(audios_dir, '.DS_Store')
    if(os.path.exists(dsstore)):
        os.remove(dsstore)
    for fn in tqdm(os.listdir(audios_dir)):
        print(str(fn))
        rate, wav = wavfile.read(os.path.join(audios_dir, fn))
        label = fn2class[fn]
        c = classes.index(label)
        y_prob = []
        
        for i in range(0, wav.shape[0]-config.step, config.step):
            sample = wav[i:i+config.step]
            x = mfcc(sample, rate, numcep=config.nfeat,
                     nfilt=config.nfilt, nfft=config.nfft)
            x = (x-config.min) / (config.max - config.min)
            
            if config.mode == "conv": 
                x = x.reshape(1, x.shape[0], x.shape[1], 1)
            elif config.mode == "time":
                x = np.expand_dims(x, axis=0)
                
            y_hat = model.predict(x)
            y_prob.append(y_hat)
            y_pred.append(np.argmax(y_hat))
            y_true.append(c)
            
        fn_prob[fn] = np.mean(y_prob, axis=0).flatten()
        
    return y_true, y_pred, fn_prob 

df = pd.read_csv("testing.csv")
classes = list(np.unique(df.label))
fn2class = dict(zip(df.fname, df.label))
p_path = os.path.join("pickles", "conv.p")

with open(p_path, "rb") as handle:
    config = pickle.load(handle)

model = load_model(config.model_path)

y_true, y_pred, fn_prob = build_predictions("testing_files")
acc_score = accuracy_score(y_true=y_true, y_pred=y_pred)
print("====")
print(acc_score)
print("====")

y_probs = []
for i, row in df.iterrows():
    y_prob = fn_prob[row.fname]
    y_probs.append(y_prob)
    for c, p in zip(classes, y_prob):
        df.at[i,c] = p
        
y_pred = [classes[np.argmax(y)] for y in y_probs]
df["y_pred"] = y_pred 
df.to_csv("predictions.csv", index=False)