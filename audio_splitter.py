from pydub import AudioSegment
import os

AUDIO_DIR = r'D:\UFRJ\7º Período\ProcVoz\football-music-identifier\audio'
SONGS = ['anajulia', 'horto', 'louco']

def split_song(import_path, split_duration, export_dir, base_filename):
    ''''
    import_path: Path to the original audio file
    split_duration: Splitted audio duration in seconds
    export_dir: Directory to export the splitted audios
    base_filename: The original audio filename
    '''
     
    audio = AudioSegment.from_wav(fr'{import_path}')
    audio_duration = audio.duration_seconds * 1000
    split_duration *= 1000
    split_parts = (int) (audio_duration//split_duration)

    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    
    for i in range(0, split_parts):
        splitted_audio = audio[i*split_duration : (i+1)*split_duration]
        splitted_audio.export(fr'{export_dir}\{base_filename}_{i:02d}.wav', format='wav')
    
    final_split = audio[split_parts*split_duration:]
    final_split.export(fr'{export_dir}\{base_filename}_{split_parts:02d}.wav', format='wav')


wav_filenames = os.listdir(AUDIO_DIR)
song_filename = {}

for song in SONGS:
    song_filename[song] = []
    for filename in wav_filenames:
        if(song in filename):
            song_filename[song].append(filename)

for song in song_filename.keys():
    export_dir = fr'{AUDIO_DIR}\{song}_splitted'
    for filename in song_filename.get(song):
        base_filename = filename[:-4]
        split_song(fr'{AUDIO_DIR}\{filename}', 5, export_dir, base_filename)

