from mutagen.mp3 import MP3
from mutagen.wave import WAVE

def get_audio_duration(file_path):
    if file_path.endswith(".mp3"):
        audio = MP3(file_path)
    elif file_path.endswith(".wav"):
        audio = WAVE(file_path)
    else:
        return False
    
    duration = audio.info.length

    hours = int(duration // 3600)
    minutes = int((duration % 3600) // 60)
    seconds = int(duration % 60)

    return hours, minutes, seconds