import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import webbrowser

# Dimensions for app size
_xDim = 720
_yDim = 720

# Class for chess board image
class BoardImage(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 500, 300)

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap("pythonImage.png")
        painter.drawPixmap(self.rect(), pixmap)

# Main class for chess gui
class Window(QMainWindow):

    # Creates a the menu for the main gui
    def _createMenuBar(self):
        menuBar = self.menuBar()
        # Creates all submenus
        gameMenu = QMenu('Game', self)
        viewMenu = QMenu('View', self)
        engineMenu = QMenu('Engine', self)
        windowMenu = QMenu('Window', self)
        helpMenu = QMenu('Help', self)
        # Populate game menu
        for _ in range(3):
            gameMenu.addAction(QAction('**SAMPLE**', self))
        # Populate view menu
        for _ in range(3):
            viewMenu.addAction(QAction('**SAMPLE**', self))
        # Populate engine menu
        for _ in range(3):
            engineMenu.addAction(QAction('**SAMPLE**', self))
        # Populate window menu
        for _ in range(3):
            windowMenu.addAction(QAction('**SAMPLE**', self))
        # Populate help menu
        helpOptions = [QAction('Suicide Hotline', self), QAction('Rules of Chess', self), QAction('Bot Commands', self)]
        helpOptions[1].triggered.connect(lambda : webbrowser.open('uschess.org/index.php/Learn-About-Chess/Learn-to-Play-Chess.html'))
        for option in helpOptions:
            helpMenu.addAction(option)
        # Adds all submenus to main menu
        menuBar.addMenu(gameMenu)
        menuBar.addMenu(viewMenu)
        menuBar.addMenu(engineMenu)
        menuBar.addMenu(windowMenu)
        menuBar.addMenu(helpMenu)

    # Initializes the main window
    def __init__(self, parent=None):
        super().__init__(parent)
        self._createMenuBar()
        self.setCentralWidget(BoardImage())
        self.setWindowTitle('Hamuy-Zimmerman Bot')
        self.setGeometry(0, 0, _xDim, _yDim)

# Creates an application with a window inside of it
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Windows')
    win = Window()
    win.show()
    sys.exit(app.exec_())