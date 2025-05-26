from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QTableWidget
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtWidgets import QHeaderView
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QTimeEdit
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtWidgets import QDoubleSpinBox
from PyQt6.QtWidgets import QProgressBar
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtGui import QDragEnterEvent
from PyQt6.QtGui import QDropEvent
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtCore import QTime
from audioDuration import *
from pathlib import Path
from normalizationThread import normalizationThread
import globalVariables as GV
import labels as LBL
import os

_MIN_HEIGHT_ = 500
_MIN_WIDTH_ = 800

_N_OF_COLUMNS_ = 5

_REMOVE_COLUMN_ = 0
_FILE_PATH_COLUMN_ = 1
_START_CUT_COLUMN_ = 2
_END_CUT_COLUMN_ = 3
_LOADING_COLUMN_ = 4

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.indexMastering = 0                                                  # variable to keep track of the current row being processed in the mastering queue

        self.setWindowTitle(GV.APP_NAME + " " + GV.APP_VERSION)
        self.setMinimumHeight(_MIN_HEIGHT_)
        self.setMinimumWidth(_MIN_WIDTH_)

        # ======= CHOOSE FILE BUTTON =======
        self.btn_chooseFile = QPushButton()
        self.btn_chooseFile.setText(LBL.BTN_CHOOSE_FILE)
        self.btn_chooseFile.clicked.connect(self.addFileToTblFileTodo)

        # ====== QUALITY SETTINGS ======
        self.lbl_loudness = QLabel()
        self.lbl_loudness.setText(LBL.LBL_LOUDNESS)
        self.spn_loudness = QDoubleSpinBox()
        self.spn_loudness.setRange(-24, -9)
        self.spn_loudness.setSingleStep(1)
        self.spn_loudness.setDecimals(0)
        self.spn_loudness.setValue(-16)

        self.lbl_lra = QLabel()
        self.lbl_lra.setText(LBL.LBL_LRA)
        self.spn_lra = QDoubleSpinBox()
        self.spn_lra.setRange(5, 20)
        self.spn_lra.setSingleStep(1)
        self.spn_lra.setDecimals(0)
        self.spn_lra.setValue(18)

        self.lbl_truePeak = QLabel()
        self.lbl_truePeak.setText(LBL.LBL_TRUE_PEAK)
        self.spn_truePeak = QDoubleSpinBox()
        self.spn_truePeak.setRange(-24, -0.1)
        self.spn_truePeak.setSingleStep(0.1)
        self.spn_truePeak.setDecimals(1)
        self.spn_truePeak.setValue(-0.5)

        self.btn_explanation = QPushButton()
        self.btn_explanation.setIcon(QIcon(GV.INFO_BTN_IMG_PATH))
        self.btn_explanation.clicked.connect(self.showExplanation)

        # ======= FILE TODO_TABLE =======
        self.tbl_fileTodo = QTableWidget()
        self.tbl_fileTodo.setColumnCount(_N_OF_COLUMNS_)
        self.tbl_fileTodo.setHorizontalHeaderItem(_REMOVE_COLUMN_, QTableWidgetItem(LBL.HEADER_REMOVE_COLUMN))
        self.tbl_fileTodo.setHorizontalHeaderItem(_FILE_PATH_COLUMN_, QTableWidgetItem(LBL.HEADER_FILE_PATH_COLUMN))
        self.tbl_fileTodo.setHorizontalHeaderItem(_START_CUT_COLUMN_, QTableWidgetItem(LBL.HEADER_START_CUT_COLUMN))
        self.tbl_fileTodo.setHorizontalHeaderItem(_END_CUT_COLUMN_, QTableWidgetItem(LBL.HEADER_END_CUT_COLUMN))
        self.tbl_fileTodo.setHorizontalHeaderItem(_LOADING_COLUMN_, QTableWidgetItem(LBL.HEADER_LOADING_COLUMN))
        self.tbl_fileTodo.hideColumn(_LOADING_COLUMN_)
        self.tbl_fileTodo.resizeColumnsToContents()
        self.tbl_fileTodo.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.tbl_fileTodo.model().rowsRemoved.connect(self.setButtons)
        self.tbl_fileTodo.model().rowsInserted.connect(self.setButtons)

        # ====== BUTTON MASTERING ======
        self.btn_mastering = QPushButton()
        self.btn_mastering.setText(LBL.BTN_MASTERING)
        self.btn_mastering.setEnabled(False)
        self.btn_mastering.clicked.connect(self.startMastering)

        # ====== POSTFIX ======
        self.lbl_postfix = QLabel()
        self.lbl_postfix.setText(LBL.LBL_POSTFIX)
        self.txt_postfix = QLineEdit()
        self.txt_postfix.setText(LBL.TXT_POSTFIX)
        
        pattern = r'^[^\\/:*?"<>|]*$'                   # regex to allow any character except: \ / : * ? " < > | (special characters that cannot be used in file names)
        regex = QRegularExpression(pattern)
        validator = QRegularExpressionValidator(regex)
        self.txt_postfix.setValidator(validator)

        # ====== EXPORT QUALITY ======
        self.lbl_extension = QLabel()
        self.lbl_extension.setText(LBL.LBL_EXTENSION)
        self.cmb_extension = QComboBox()
        self.cmb_extension.addItems(GV.ALLOWED_EXTENSIONS)
        self.cmb_extension.currentIndexChanged.connect(self.changeBitMeaning)

        self.lbl_fc = QLabel()
        self.lbl_fc.setText(LBL.LBL_FC)
        self.cmb_fc = QComboBox()
        self.cmb_fc.addItems(GV.ALLOWED_FC)

        self.lbl_bit = QLabel()
        self.cmb_bit = QComboBox()
        self.changeBitMeaning()

        # ====== EXPORT PATH ======
        self.lbl_exportPath = QLabel()
        self.lbl_exportPath.setText(LBL.LBL_EXPORT_PATH)
        self.txt_exportPath = QLineEdit()
        self.txt_exportPath.setText(GV.DEFAULT_DIRECTORY)
        self.txt_exportPath.setDisabled(True)
        self.txt_exportPath.setStyleSheet("color: black;")
        self.btn_exportPath = QPushButton()
        self.btn_exportPath.setText(LBL.BTN_EXPORT_PATH)
        self.btn_exportPath.clicked.connect(self.chooseOutputDirectory)

        # ====== DONE BUTTON ======
        self.btn_done = QPushButton()
        self.btn_done.setText(LBL.BTN_DONE)
        self.btn_done.hide()
        self.btn_done.clicked.connect(self.finishMastering)

        # ====== CANCEL BUTTON ======
        self.btn_cancel = QPushButton()
        self.btn_cancel.setText(LBL.BTN_CANCEL)
        self.btn_cancel.hide()
        self.btn_cancel.clicked.connect(self.cancelQueue)

        # ====== LAYOUT ======
        self.lyt_main = QVBoxLayout(self)
        self.lyt_main.addWidget(self.btn_chooseFile)

        self.lyt_loudness = QHBoxLayout()
        self.lyt_loudness.addWidget(self.lbl_loudness)
        self.lyt_loudness.addWidget(self.spn_loudness)
        self.lyt_loudness.addWidget(self.lbl_lra)
        self.lyt_loudness.addWidget(self.spn_lra)
        self.lyt_loudness.addWidget(self.lbl_truePeak)
        self.lyt_loudness.addWidget(self.spn_truePeak)
        self.lyt_loudness.addWidget(self.btn_explanation)
        self.lyt_main.addLayout(self.lyt_loudness)

        self.lyt_main.addWidget(self.tbl_fileTodo)

        self.lyt_main.addWidget(self.btn_done)
        self.lyt_main.addWidget(self.btn_cancel)

        self.lyt_postfix = QHBoxLayout()
        self.lyt_postfix.addWidget(self.lbl_postfix)
        self.lyt_postfix.addWidget(self.txt_postfix)
        self.lyt_main.addLayout(self.lyt_postfix)

        self.lyt_export = QHBoxLayout()
        self.lyt_export.addWidget(self.lbl_extension)
        self.lyt_export.addWidget(self.cmb_extension)
        self.lyt_export.addWidget(self.lbl_fc)
        self.lyt_export.addWidget(self.cmb_fc)
        self.lyt_export.addWidget(self.lbl_bit)
        self.lyt_export.addWidget(self.cmb_bit)
        self.lyt_main.addLayout(self.lyt_export)

        self.lyt_exportPath = QHBoxLayout()
        self.lyt_exportPath.addWidget(self.lbl_exportPath)
        self.lyt_exportPath.addWidget(self.txt_exportPath)
        self.lyt_exportPath.addWidget(self.btn_exportPath)
        self.lyt_main.addLayout(self.lyt_exportPath)

        self.lyt_main.addWidget(self.btn_mastering)
        
        self.setAcceptDrops(True)


    def addFileToTblFileTodo(self, dragNDrop=""):
        if self.sender() == self.btn_chooseFile:
            files, _ = QFileDialog.getOpenFileNames(self, LBL.CHOOSE_FILE_WIN_NAME, GV.DEFAULT_DIRECTORY, GV.ALLOWED_EXTENSIONS_FILTER)
        else:
            files = []
            files.append(str(dragNDrop))

        for file in files:
            row = self.tbl_fileTodo.rowCount()
            self.tbl_fileTodo.insertRow(row)

            # REMOVE BUTTON
            self.tbl_fileTodo.setCellWidget(row, _REMOVE_COLUMN_, QPushButton())
            self.tbl_fileTodo.cellWidget(row, _REMOVE_COLUMN_).setIcon(QIcon(GV.REMOVE_BTN_IMG_PATH))
            self.tbl_fileTodo.cellWidget(row, _REMOVE_COLUMN_).clicked.connect(self.removeFileTodo)
            
            # FILE PATH
            self.tbl_fileTodo.setCellWidget(row, _FILE_PATH_COLUMN_, QLabel())
            self.tbl_fileTodo.cellWidget(row, _FILE_PATH_COLUMN_).setText(file)

            hours, minutes, seconds, milliseconds = get_audio_duration(file)

            # START CUT
            self.tbl_fileTodo.setCellWidget(row, _START_CUT_COLUMN_, QTimeEdit())
            self.tbl_fileTodo.cellWidget(row, _START_CUT_COLUMN_).setDisplayFormat("hh:mm:ss.zzz")
            self.tbl_fileTodo.cellWidget(row, _START_CUT_COLUMN_).setTime(QTime(0, 0, 0, 0))
            self.tbl_fileTodo.cellWidget(row, _START_CUT_COLUMN_).setMinimumTime(QTime(0, 0, 0, 0))
            self.tbl_fileTodo.cellWidget(row, _START_CUT_COLUMN_).setMaximumTime(QTime(hours, minutes, seconds - 1, milliseconds))

            # END CUT
            self.tbl_fileTodo.setCellWidget(row, _END_CUT_COLUMN_, QTimeEdit())
            self.tbl_fileTodo.cellWidget(row, _END_CUT_COLUMN_).setDisplayFormat("hh:mm:ss.zzz")
            self.tbl_fileTodo.cellWidget(row, _END_CUT_COLUMN_).setTime(QTime(hours, minutes, seconds, milliseconds))
            self.tbl_fileTodo.cellWidget(row, _END_CUT_COLUMN_).setMinimumTime(QTime(0, 0, 1, 0))
            self.tbl_fileTodo.cellWidget(row, _END_CUT_COLUMN_).setMaximumTime(QTime(hours, minutes, seconds, milliseconds))

            # LOADING
            self.tbl_fileTodo.setCellWidget(row, _LOADING_COLUMN_, QProgressBar())
            self.tbl_fileTodo.cellWidget(row, _LOADING_COLUMN_).setMaximum(0)
            self.tbl_fileTodo.cellWidget(row, _LOADING_COLUMN_).setMinimum(0)
            self.tbl_fileTodo.cellWidget(row, _LOADING_COLUMN_).setValue(0)
        
        self.tbl_fileTodo.resizeColumnsToContents()
        self.tbl_fileTodo.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

    def removeFileTodo(self):
        buttonSender = self.sender()
        index = 0
        for index in range(self.tbl_fileTodo.rowCount()):                                                 # scroll all the table to find my check box sender and so spot the row
            if(self.tbl_fileTodo.cellWidget(index, _REMOVE_COLUMN_) == buttonSender):
                break
        self.tbl_fileTodo.removeRow(index)
        self.tbl_fileTodo.resizeColumnsToContents()
        self.tbl_fileTodo.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)


    # ====== DRAG & DROP ======
    def dragEnterEvent(self, event: QDragEnterEvent):                                                     # event that is called when a file (or folder) is dragged over the window without releasing it
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):                                                               # the file (or folder) is dropped on the window
        paths = event.mimeData().urls()

        for path in paths:
            file_path = path.toLocalFile()
            file_extension = os.path.splitext(file_path)[1].lower()
            if not file_extension in GV.ALLOWED_EXTENSIONS:
                pass
            else:
                self.addFileToTblFileTodo(file_path)
    # ======

    def chooseOutputDirectory(self):
        outPath = QFileDialog.getExistingDirectory(self, LBL.CHOOSE_OUT_DIR_WIN_NAME, GV.DEFAULT_DIRECTORY)
        self.txt_exportPath.setText(outPath)

    def setButtons(self):
        if self.tbl_fileTodo.rowCount() > 0:
            self.btn_mastering.setEnabled(True)
        else:
            self.btn_mastering.setEnabled(False)

    # When change export extension this method adapt the "bit" variable meaning
    def changeBitMeaning(self):
        if self.cmb_extension.currentText() == ".wav":
            self.lbl_bit.setText(LBL.LBL_BIT_DEPTH)
            self.cmb_bit.clear()
            self.cmb_bit.addItems(GV.ALLOWED_BIT_DEPTH)
        elif self.cmb_extension.currentText() == ".mp3":
            self.lbl_bit.setText(LBL.LBL_BIT_RATE)
            self.cmb_bit.clear()
            self.cmb_bit.addItems(GV.ALLOWED_BIT_RATE)
            self.cmb_bit.setCurrentIndex(2)
    
    def showExplanation(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(LBL.LOUDNESS_EXPLANATION_WIN_NAME)
        #msgBox.setText(LBL.LOUDNESS_EXPLANATION_TITLE)
        msgBox.setInformativeText(LBL.LOUDNESS_EXPLANATION)
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.exec()

    def closeEvent(self, event):
        if not self.btn_chooseFile.isEnabled():
            self.cancelQueue()

    # =================================
    # ====== MASTERING FUNCTIONS ======
    # =================================
    def startMastering(self):
        # if I could click on the "mastering" button, means that the table isn't empty
        self.btn_chooseFile.setEnabled(False)
        self.spn_loudness.setEnabled(False)
        self.spn_lra.setEnabled(False)
        self.spn_truePeak.setEnabled(False)
        self.cmb_extension.setEnabled(False)
        self.cmb_bit.setEnabled(False)
        self.cmb_fc.setEnabled(False)
        self.btn_exportPath.setEnabled(False)
        self.btn_mastering.setEnabled(False)
        self.txt_postfix.setEnabled(False)
        self.tbl_fileTodo.hideColumn(_REMOVE_COLUMN_)
        self.tbl_fileTodo.hideColumn(_START_CUT_COLUMN_)
        self.tbl_fileTodo.hideColumn(_END_CUT_COLUMN_)
        self.tbl_fileTodo.showColumn(_LOADING_COLUMN_)
        self.btn_cancel.show()

        self.sendNextFileToMastering(self.indexMastering)

    def sendNextFileToMastering(self, row):
        path = self.tbl_fileTodo.cellWidget(row, _FILE_PATH_COLUMN_).text()
        title = Path(self.tbl_fileTodo.cellWidget(row, _FILE_PATH_COLUMN_).text()).stem + self.txt_postfix.text() # extract the file name without extension and add the postfix
        outPath = self.txt_exportPath.text()
        loudness = self.spn_loudness.value()
        lra = self.spn_lra.value()
        truePeak = self.spn_truePeak.value()
        extension = self.cmb_extension.currentText()[1:] # remove the dot from the extension
        fc = self.cmb_fc.currentText()[:-3]              # remove the " Hz" from the end of the string
        if extension == "wav":
            bit = self.cmb_bit.currentText()[:-4]
        elif extension == "mp3":
            bit = self.cmb_bit.currentText()[:-5]
        star_cut = self.tbl_fileTodo.cellWidget(row, _START_CUT_COLUMN_).text()
        end_cut = self.tbl_fileTodo.cellWidget(row, _END_CUT_COLUMN_).text()

        """
        print(path)
        print(title)
        print(outPath)
        print(loudness)
        print(lra)
        print(truePeak)
        print(extension)
        print(fc)
        print(bit)
        print(star_cut)
        print(end_cut)
        """

        masteringThread = normalizationThread(self, path, title, outPath, loudness, lra, truePeak, extension, fc, bit, star_cut, end_cut)
        masteringThread.finished.connect(self.currentMasteringFinished)
        masteringThread.start()

    def currentMasteringFinished(self, result):
        self.tbl_fileTodo.setCellWidget(self.indexMastering, _LOADING_COLUMN_, QLabel())
        if result == True:
            self.tbl_fileTodo.cellWidget(self.indexMastering, _LOADING_COLUMN_).setText(LBL.NORMALIZATION_DONE)
        else:
            self.tbl_fileTodo.cellWidget(self.indexMastering, _LOADING_COLUMN_).setText(LBL.NORMALIZATION_ERROR)
        self.indexMastering += 1
        
        if self.indexMastering < self.tbl_fileTodo.rowCount():
            self.sendNextFileToMastering(self.indexMastering)
        else:
            self.btn_done.show()
            self.btn_cancel.hide()

    def finishMastering(self):
        self.indexMastering = 0
        self.btn_done.hide()
        self.btn_chooseFile.setEnabled(True)
        self.spn_loudness.setEnabled(True)
        self.spn_lra.setEnabled(True)
        self.spn_truePeak.setEnabled(True)
        self.cmb_extension.setEnabled(True)
        self.cmb_bit.setEnabled(True)
        self.cmb_fc.setEnabled(True)
        self.btn_exportPath.setEnabled(True)
        self.txt_postfix.setEnabled(True)
        self.tbl_fileTodo.showColumn(_REMOVE_COLUMN_)
        self.tbl_fileTodo.showColumn(_START_CUT_COLUMN_)
        self.tbl_fileTodo.showColumn(_END_CUT_COLUMN_)
        self.tbl_fileTodo.hideColumn(_LOADING_COLUMN_)
        self.btn_cancel.hide()
        
        while self.tbl_fileTodo.rowCount() != 0:
            self.tbl_fileTodo.removeRow(0)

    def cancelQueue(self):                                       # remove all the rows in the table, so the queue is empty except the first one that is processing
        while self.tbl_fileTodo.rowCount() != 1:
            self.tbl_fileTodo.removeRow(1)