#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 11:58:27 2023

@author: igortb
"""

import os
import pandas as pd

csv_path = "training.csv"
directory_path = "training_files"

# Read the CSV file
df = pd.read_csv(csv_path)

# Get the list of files in the directory
files_in_directory = os.listdir(directory_path)

# Get the list of filenames from the CSV
files_in_csv = df["fname"].tolist()

# Find inconsistencies between CSV and directory
missing_files = set(files_in_csv) - set(files_in_directory)
extra_files = set(files_in_directory) - set(files_in_csv)

# Print the inconsistencies
print("Missing files in directory:")
for file in missing_files:
    print(file)

print("\nExtra files in directory:")
for file in extra_files:
    print(file)