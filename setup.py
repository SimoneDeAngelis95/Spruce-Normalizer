"""
Usage:
    python setup.py py2app
"""

from setuptools import setup
import globalVariables as GV

APP = ['main.py']
DATA_FILES = [GV.REMOVE_BTN_IMG_PATH, GV.ICON_PATH, GV.INFO_BTN_IMG_PATH, GV.FFMPEG_PATH]
OPTIONS = {
    'iconfile': GV.ICON_PATH,
    'plist':{
        'CFBundleName': 'Spruce Normalizer',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleExecutable': 'Spruce Normalizer'
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    author="Simone De Angelis",
    copyright="Simone De Angelis",
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)