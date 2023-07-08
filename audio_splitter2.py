import os
import soundfile as sf

def split_wav_file(input_path, output_path, duration):
    audio, sample_rate = sf.read(input_path)

    total_samples = len(audio)

    num_chunks = total_samples // (duration * sample_rate)

    for i in range(num_chunks):
        start_sample = i * duration * sample_rate
        end_sample = (i + 1) * duration * sample_rate
        chunk = audio[start_sample:end_sample]

        filename = os.path.splitext(os.path.basename(input_path))[0]
        output_filename = f"{filename}_chunk{i + 1}.wav"
        output_file_path = os.path.join(output_path, output_filename)

        sf.write(output_file_path, chunk, sample_rate)
        
    print(f"split {input_path} into {num_chunks} chunks of {duration} seconds each.")

input_directory = "./wav"
output_directory = "./samples"
duration = 5  #duration
for filename in os.listdir(input_directory):
    if filename.endswith(".wav"):
        input_file_path = os.path.join(input_directory, filename)
        split_wav_file(input_file_path, output_directory, duration)
