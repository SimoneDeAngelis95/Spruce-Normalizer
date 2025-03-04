from PyQt6.QtCore import QThread
from PyQt6.QtCore import pyqtSignal
import globalVariables as GV
import subprocess
import os
import platform

class normalizationThread(QThread):
    finished = pyqtSignal(bool)

    def __init__(self, parent, filePath, title, outputPath, loudness, loudnessRange, truePeak, extension, fc, bit, startTime, finishTime):
        super().__init__(parent=parent)
        self.filePath = filePath
        self.title = title
        self.outputPath = outputPath
        self.loudness = loudness
        self.loudnessRange = loudnessRange
        self.truePeak = truePeak
        self.extension = extension
        self.fc = fc
        self.bit = bit
        self.startTime = startTime
        self.finishTime = finishTime

    def run(self):
        
        # GESTIRE CONFLITTI NOME
        outPath = self.outputPath + "/" + self.title
        if os.path.exists(outPath + "." + self.extension):
            index = 0
            postFix = ""
            while os.path.exists(outPath + postFix + "." + self.extension):
                index += 1
                postFix = " (" + str(index) + ")"
            outPath = self.outputPath + "/" + self.title + postFix
        outPath = outPath + "." + self.extension
        
        filters = "loudnorm=I=" + str(self.loudness) + ":LRA=" + str(self.loudnessRange) + ":TP=" + str(self.truePeak)
        
        if self.extension == "wav":
            if self.bit == "16":
                bitRateOrBitDepth = "-sample_fmt"
                self.bit = "s16"
            elif self.bit == "24":
                bitRateOrBitDepth = "-c:a"
                self.bit = "pcm_s24le"
        
        elif self.extension == "mp3":
            bitRateOrBitDepth = "-b:a"
            self.bit += "k"
        try:
            cmd = [
                GV.FFMPEG_PATH,
                "-i", self.filePath,
                "-ss",
                self.startTime,
                "-to",
                self.finishTime,
                "-filter:a",
                filters,
                "-ar",
                self.fc,
                bitRateOrBitDepth,
                self.bit,
                outPath
            ]
            #cmd_str = ' '.join(cmd)  # Converti la lista cmd in una stringa
            #print(cmd_str)
            
            if platform.system() == 'Darwin' or platform.system() == 'Linux':
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            elif platform.system() == 'Windows':
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW) # creationflags=subprocess.CREATE_NO_WINDOW indispensabile per non far apparire la finestra di terminale su windows. Su macOS non è obbligatorio
            
            while process.poll() is None:
                pass
                #print("Waiting...")
                #os.system('clear')
            
            #stdout = process.communicate() # devo catturare comunque l'output altrimenti si blocca, ma a quanto pare no
            #print(stdout)

            if process.returncode == 0:
                self.finished.emit(True)
            else:
                self.finished.emit(False)
        except:
            self.finished.emit(False)