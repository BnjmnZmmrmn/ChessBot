import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QMouseEvent
import webbrowser
import datetime

# Dimensions for app size
_xDim = 720
_yDim = 720

"""       TEMP CODES:
           wr | br
          wkn | bkn
           wb | bb
      wk, wq  |  bk, bq
           wp | bp
"""

# Initialize board storage
_pieceDict = {}
for i in range(1, 9):
    _pieceDict[chr(i + 96) + "2"] = "wp"
    _pieceDict[chr(i + 96) + "7"] = "bp"
    if i == 1 or i == 8:
        _pieceDict[chr(i + 96) + "1"] = "wr"
        _pieceDict[chr(i + 96) + "8"] = "br"
    if i == 2 or i == 7:
        _pieceDict[chr(i + 96) + "1"] = "wkn"
        _pieceDict[chr(i + 96) + "8"] = "bkn"
    if i == 3 or i == 6:
        _pieceDict[chr(i + 96) + "1"] = "wb"
        _pieceDict[chr(i + 96) + "8"] = "bb"
    if i == 4:
        _pieceDict[chr(i + 96) + "1"] = "wk"
        _pieceDict[chr(i + 96) + "8"] = "bq"
    if i == 5:
        _pieceDict[chr(i + 96) + "1"] = "wq"
        _pieceDict[chr(i + 96) + "8"] = "bk"
    _pieceDict[chr(i + 96) + "3"] = ""
    _pieceDict[chr(i + 96) + "4"] = ""
    _pieceDict[chr(i + 96) + "5"] = ""
    _pieceDict[chr(i + 96) + "6"] = ""


# Colors for board
_brdClrOne = QColor(207, 138, 70)
_brdClrTwo = QColor(253, 204, 157)
_brdClrClck = QColor(253, 0, 0)

# Class for engine debug console
class EngineDebug(QFrame):
    def __init__(self, engine, diff):
        super().__init__()
        self.engineName = engine
        self.diff = diff
        self.setFixedSize(int(_xDim), int(_yDim / 2))
        layout = QVBoxLayout()
        self.setLayout(layout)
        title = self.createTitle()
        layout.addWidget(title)
        self.textBox = QLabel()
        self.textBox.setIndent(5)
        self.textBox.setStyleSheet("background-color: white;" "border: 2px solid grey;")
        self.textBox.setAlignment(Qt.AlignTop)
        layout.addWidget(self.textBox)
        self.updateText("Sample")
        self.setLayout(layout)
        self.setObjectName("frame");
        self.setStyleSheet("#frame { border: 1px solid grey; }");

    def updateText(self, debug):
        currText = self.textBox.text()
        self.textBox.setText(currText + datetime.datetime.now().strftime("%H:%M:%S") + " <" + self.engineName + self.diff + ": " + debug + "\n")
    
    def createTitle(self):
        header = QLabel()
        font = header.font()
        font.setPointSize(10)
        header.setFont(font)
        header.setText("Engine Debug")
        header.setFixedHeight(20)
        return header

# Class for move table
class MoveList(QTableWidget):
    white = True

    def __init__(self):
        super().__init__()
        self.setFixedSize(int(_xDim / 2), int(_yDim / 2))
        self.setRowCount(0)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(['White', 'Black'])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    # Adds a move to the table
    def addMoveToTable(self, move):
        if self.white:
            self.setRowCount(self.rowCount() + 1)
            rowNum = self.rowCount() - 1
            itemOne = QTableWidgetItem(move)
            itemOne.setFlags(itemOne.flags() & ~(Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled))
            itemTwo = QTableWidgetItem()
            itemTwo.setFlags(itemTwo.flags() & ~(Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled))
            self.setItem(rowNum, 0, itemOne)
            self.setItem(rowNum, 1, itemTwo)
        else:
            rowNum = self.rowCount() - 1
            itemTwo = QTableWidgetItem(move)
            itemTwo.setFlags(itemTwo.flags() & ~(Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled))
            self.setItem(rowNum, 1, itemTwo)
        self.white = not self.white 


# Class for chess board image
class BoardImage(QWidget):
    prevClick = None

    def __init__(self):
        super().__init__()
        self.setFixedSize(int(_xDim / 2), int(_yDim / 2))

    def paintEvent(self, event):
        squareSize = int(_xDim / 16)
        selfPainter = QPainter(self)
        alt = False
        for x in [squareSize * i for i in range(8)]:
            alt = not alt
            for y in [squareSize * i for i in range(8)]:
                square = chr(int(x / squareSize) + 97) + str(8 - int(y / squareSize))
                if self.prevClick == square:
                    selfPainter.fillRect(x, y, squareSize, squareSize, _brdClrClck)
                elif not alt:
                    selfPainter.fillRect(x, y, squareSize, squareSize, _brdClrOne)
                else:
                    selfPainter.fillRect(x, y, squareSize, squareSize, _brdClrTwo)
                alt = not alt
                piece = _pieceDict[square]
                if piece == "wr":
                    selfPainter.drawImage(x, y, QImage('./assets/wr.png'))
                elif piece == "br":
                    selfPainter.drawImage(x, y, QImage('./assets/br.png'))
                elif piece == "wkn":
                    selfPainter.drawImage(x, y, QImage('./assets/wkn.png'))
                elif piece == "bkn":
                    selfPainter.drawImage(x, y, QImage('./assets/bkn.png'))
                elif piece == "wb":
                    selfPainter.drawImage(x, y, QImage('./assets/wb.png'))
                elif piece == "bb":
                    selfPainter.drawImage(x, y, QImage('./assets/bb.png'))
                elif piece == "wk":
                    selfPainter.drawImage(x, y, QImage('./assets/wk.png'))
                elif piece == "bk":
                    selfPainter.drawImage(x, y, QImage('./assets/bk.png'))
                elif piece == "wq":
                    selfPainter.drawImage(x, y, QImage('./assets/wq.png'))
                elif piece == "bq":
                    selfPainter.drawImage(x, y, QImage('./assets/bq.png'))
                elif piece == "wp":
                    selfPainter.drawImage(x, y, QImage('./assets/wp.png'))
                elif piece == "bp":
                    selfPainter.drawImage(x, y, QImage('./assets/bp.png'))
        selfPainter.drawRect(0, 0, squareSize * 8, squareSize * 8)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = chr(97 + (event.x() // int(_xDim / 16)))
            y = 8 - (event.y() // int(_yDim / 16))
            newClick = x + str(y)
            if self.prevClick != None and _pieceDict[self.prevClick] != "":
                piece = _pieceDict[self.prevClick]
                # validateMove(self.prevClick, x + str(y))
                _pieceDict[self.prevClick] = ""
                _pieceDict[newClick] = piece
                self.prevClick = None
                self.parent().parent().on_board_image_clicked(newClick, True)
            else:
                self.prevClick = newClick
                self.parent().parent().on_board_image_clicked(newClick, False)


# Houses all compenents of the chess gui for the main window
class WindowLayout(QWidget):
    brdImg = None
    mvLst = None
    ngnDbg = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.brdImg = BoardImage()
        self.mvLst = MoveList()
        self.ngnDbg = EngineDebug("DylanBot", "5")
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        topLayout = QHBoxLayout()
        topLayout.setSpacing(0)
        topLayout.setContentsMargins(0, 0, 0, 0)
        topLayout.addWidget(self.brdImg)
        topLayout.addWidget(self.mvLst) 
        housing = QWidget()
        housing.setLayout(topLayout)
        layout.addWidget(housing)
        layout.addWidget(self.ngnDbg)
        self.setLayout(layout)
    
    def on_board_image_clicked(self, loc, addMove):
        if addMove:
            piece = _pieceDict[loc]
            self.mvLst.addMoveToTable(piece + " to " + loc)
            self.ngnDbg.updateText("Good move!")
        self.brdImg.update()

# Menu for the main gui
class WindowMenu(QMenuBar):
    prevClick = None

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