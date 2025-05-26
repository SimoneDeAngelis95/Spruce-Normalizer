from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QGuiApplication
from MainWindow import MainWindow
import globalVariables as GV
import sys

app = QApplication(sys.argv)
app.setApplicationName(GV.APP_NAME)

myWindow = MainWindow()

# center the window on the screen
screenGeometry = QGuiApplication.primaryScreen().availableGeometry()
windowGeometry = myWindow.frameGeometry()
windowGeometry.moveCenter(screenGeometry.center())
myWindow.move(windowGeometry.topLeft())

myWindow.show()

if __name__ == "__main__":
    app.exec()