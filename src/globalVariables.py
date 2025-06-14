import os
import platform

APP_NAME = "Spruce Normalizer"
APP_VERSION = "1.2.2"
ICON_PATH = "./logo.ico"

REMOVE_BTN_IMG_PATH = "./remove.png"
INFO_BTN_IMG_PATH = "./info.png"

ALLOWED_EXTENSIONS = [".wav", ".mp3"]
ALLOWED_EXTENSIONS_FILTER = "WAV Files (*.wav);;MP3 Files (*.mp3)"

ALLOWED_FC = ["44100 Hz", "48000 Hz"]

ALLOWED_BIT_DEPTH = ["16 bit", "24 bit"]
ALLOWED_BIT_RATE = ["320 kbps", "256 kbps", "192 kbps", "128 kbps", "96 kbps", "64 kbps"]


if platform.system() == 'Darwin' or platform.system() == 'Linux':
    DEFAULT_DIRECTORY = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')   # DEFAULT_DIRECTORY
    FFMPEG_PATH = "./ffmpeg" # FFMPEG
elif platform.system() == 'Windows':
    DEFAULT_DIRECTORY = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') # DEFAULT_DIRECTORY
    FFMPEG_PATH = "./ffmpeg.exe" # FFMPEG