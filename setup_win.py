# =====================================================================
def add_src_prefix(path): # helper function to add 'src/' prefix to paths
    return f'src/{path}'
# =====================================================================

import src.globalVariables as GV
from cx_Freeze import setup, Executable

script = 'src/main.py'
icon_path = add_src_prefix(GV.ICON_PATH)

options = {
    'build_exe': {
        'packages': [],
        'include_files': [
            add_src_prefix(GV.REMOVE_BTN_IMG_PATH),
            add_src_prefix(GV.ICON_PATH),
            add_src_prefix(GV.INFO_BTN_IMG_PATH),
            add_src_prefix(GV.FFMPEG_PATH)
        ],
    },
}

# define the executables
executables = [
    Executable(
        script,
        base="Win32GUI", # Use "Win32GUI" to avoid a console window
        icon=icon_path
    )
]

setup(
    name=GV.APP_NAME,
    version=GV.APP_VERSION,
    description='Audio normalization tool',
    options=options,
    executables=executables
)
