import os
import csv
import random
import re

def extract_label(filename):
    match = re.match(r'^([a-zA-Z]+)', filename)
    if match:
        return match.group(1)
    else:
        return ''

def split_file_list(file_list, split_ratio):
    total_files = len(file_list)
    split_index = int(total_files * split_ratio)
    random.shuffle(file_list)
    return file_list[:split_index], file_list[split_index:]

def create_file_lists(directory, csv_95_filename, csv_5_filename):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            label = extract_label(file)
            file_list.append([file, label])

    # Split file list into 95% and 5% parts
    file_list_95, file_list_5 = split_file_list(file_list, 0.95)

    # Write 95% file list to CSV
    with open(csv_95_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['fname', 'label'])
        writer.writerows(file_list_95)

    # Write 5% file list to CSV
    with open(csv_5_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['fname', 'label'])
        writer.writerows(file_list_5)

# Example usage:
directory_path = './samples'  # Replace with your directory path
csv_95_file_path = './training.csv'  # Replace with the desired output CSV file path for 95%
csv_5_file_path = './testing.csv'  # Replace with the desired output CSV file path for 5%

create_file_lists(directory_path, csv_95_file_path, csv_5_file_path)
