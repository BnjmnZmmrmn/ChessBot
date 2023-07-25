import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import webbrowser

# Dimensions for app size
_xDim = 720
_yDim = _xDim

# Colors for board
_brdClrOne = QColor(207, 138, 70)
_brdClrTwo = QColor(253, 204, 157)
_pcClrOne = QColor(255, 255, 255)
_pcClrTwo = QColor(0, 0, 0)


# Class for chess board image
class BoardImage(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        squareSize = int(_xDim / 16)
        selfPainter = QPainter(self)
        alt = False
        for x in [squareSize * i for i in range(8)]:
            alt = not alt
            for y in [squareSize * i for i in range(8)]:
                if not alt:
                    selfPainter.fillRect(x, y, squareSize, squareSize, _brdClrOne)
                else:
                    selfPainter.fillRect(x, y, squareSize, squareSize, _brdClrTwo)
                alt = not alt

# Houses all compenents of the chess gui for the main window
class WindowLayout(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        topLayout = QHBoxLayout()
        topLayout.setSpacing(0)
        topLayout.setContentsMargins(0, 0, 0, 0)
        topLayout.addWidget(BoardImage())
        topLayout.addWidget(QWidget())
        housing = QWidget()
        housing.setLayout(topLayout)
        layout.addWidget(housing)
        layout.addWidget(QWidget())
        self.setLayout(layout)

# Menu for the main gui
class WindowMenu(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
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
        self.addMenu(gameMenu)
        self.addMenu(viewMenu)
        self.addMenu(engineMenu)
        self.addMenu(windowMenu)
        self.addMenu(helpMenu)
    
# Main class for chess gui
class Window(QMainWindow):

    # Initializes the main window
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMenuBar(WindowMenu())
        self.setCentralWidget(WindowLayout())
        self.setWindowTitle('Hamuy-Zimmerman Bot')

# Creates an application with a window inside of it
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Windows')
    res = app.desktop().screenGeometry()
    w, h = res.width(), res.height()
    win = Window()
    win.setGeometry(int((w - _xDim)/2), int((h - _yDim)/2), _xDim, _yDim)
    win.show()
    sys.exit(app.exec_())