"""
Usage:
To create a macOS app bundle using py2app, run the following command in the terminal:
    - pip install py2app
    - python setup_macos.py py2app
    - This will generate a .app bundle in the 'dist' directory.
This script is used to package a Python application into a macOS app bundle using py2app.

This setup works with macOS silicon and intel architectures.
"""
# =====================================================================
def add_src_prefix(path): # helper function to add 'src/' prefix to paths
    return f'src/{path}'
# =====================================================================

from setuptools import setup
import src.globalVariables as GV


APP = ['src/main.py']
DATA_FILES = [
    add_src_prefix(GV.REMOVE_BTN_IMG_PATH),
    add_src_prefix(GV.ICON_PATH),
    add_src_prefix(GV.INFO_BTN_IMG_PATH),
    add_src_prefix(GV.FFMPEG_PATH)
]

OPTIONS = {
    'iconfile': add_src_prefix(GV.ICON_PATH),
    'plist':{
        'CFBundleName': GV.APP_NAME,
        'CFBundleVersion': GV.APP_VERSION,
        'CFBundleShortVersionString': GV.APP_VERSION, 
        'CFBundleExecutable': GV.APP_NAME,
        'NSHumanReadableCopyright': '© 2024-2025 Made with Love by Simone De Angelis',
        'CFBundleIdentifier': 'com.simonedeamelis.sprucenormalizer',                   # Unique identifier for the app
        'LSApplicationCategoryType': 'public.app-category.utilities',                  # Application category
        'NSHighResolutionCapable': True,                                               # Support for high-resolution displays
    },
    'excludes': ['tkinter'],                                                           # Exclude unnecessary modules to reduce app size
    'optimize': 2,                                                                     # Python bytecode optimization level
}

setup(
    app=APP,
    data_files=DATA_FILES,
    author="Simone De Angelis",
    copyright="Simone De Angelis",
    description="Audio normalization tool",
    license="GPLv3",
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)