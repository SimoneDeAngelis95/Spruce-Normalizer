import globalVariables as GV
from cx_Freeze import setup, Executable

# Sostituisci 'tuo_script.py' con il nome del tuo script principale
script = 'main.py'
icon_path = GV.ICON_PATH

# Configurazione di cx_Freeze
options = {
    'build_exe': {
        'packages': [],  # Lista dei moduli da includere
        'include_files': [GV.REMOVE_BTN_IMG_PATH, GV.ICON_PATH, GV.INFO_BTN_IMG_PATH, GV.FFMPEG_PATH],  # Lista di file aggiuntivi da includere
    },
}

# Definizione dell'eseguibile
executables = [
    Executable(
        script,
        base="Win32GUI", # per forzare l'app a non essere aperta da terminale
        icon=icon_path
    )
]

# Chiamata a setup
setup(
    name='Spruce Normalizer',
    version='1.0.1',
    description='',
    options=options,
    executables=executables
)
