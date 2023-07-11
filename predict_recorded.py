#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 12:38:06 2023

@author: igortb
"""

import os
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write, read
from keras.models import load_model
from python_speech_features import mfcc
import pickle
import pandas as pd
import time

def record_audio(duration, sample_rate):
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()  # Wait for recording to complete
    return audio.flatten()

def save_audio(filename, audio, sample_rate):
    write(filename, sample_rate, audio)

def predict_class(model, audio_path, config, classes):
    rate, wav = read(audio_path)
    y_prob = []
    for i in range(0, wav.shape[0] - config.step, config.step):
        sample = wav[i:i+config.step]
        x = mfcc(sample, rate, numcep=config.nfeat, nfilt=config.nfilt, nfft=config.nfft)
        x = (x - config.min) / (config.max - config.min)
        if config.mode == "conv":
            x = x.reshape(1, x.shape[0], x.shape[1], 1)
        elif config.mode == "time":
            x = np.expand_dims(x, axis=0)
        y_hat = model.predict(x, verbose=0)
        y_prob.append(y_hat)
    y_prob_avg = np.mean(y_prob, axis=0).flatten()
    predicted_class_index = np.argmax(y_prob_avg)
    predicted_class = classes[predicted_class_index]
    confidence_percentage = y_prob_avg[predicted_class_index] * 100
    return predicted_class, confidence_percentage

# Load the model and configuration
df = pd.read_csv("training.csv")
classes = list(np.unique(df.label))
p_path = os.path.join("pickles", "conv.p")
with open(p_path, "rb") as handle:
    config = pickle.load(handle)
model = load_model(config.model_path)
# ... Load config and classes

# Recording live audio
duration = 5  # Duration in seconds
sample_rate = 16000  # Sample rate
audio_filename = "recorded_audio.wav"

confidence_percentage = 0
print("Ouvindo...")
while(confidence_percentage < 75):
    recorded_audio = record_audio(duration, sample_rate)
    save_audio(audio_filename, recorded_audio, sample_rate)
    predicted_class, confidence_percentage = predict_class(model, audio_filename, config, classes)
    print(predicted_class, confidence_percentage)


print("Música: ", predicted_class)
print("Confiança:", confidence_percentage)
