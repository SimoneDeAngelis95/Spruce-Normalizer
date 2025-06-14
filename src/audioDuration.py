from mutagen.mp3 import MP3
from mutagen.wave import WAVE

def get_audio_duration(file_path):
    if file_path.endswith(".mp3") or file_path.endswith(".MP3"):     # TODO: soluzione tampone, sistema quando hai tempo
        audio = MP3(file_path)
    elif file_path.endswith(".wav") or file_path.endswith(".WAV"):
        audio = WAVE(file_path)
    else:
        return False
    
    duration = audio.info.length

    hours = int(duration // 3600)
    minutes = int((duration % 3600) // 60)
    seconds = int(duration % 60)
    milliseconds = int((duration % 1) * 1000)

    return hours, minutes, seconds, milliseconds