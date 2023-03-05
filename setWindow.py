#Developer: Federico De Rocco
#Written using PyQt6 Lib

from __future__ import print_function
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QToolBar, QLabel, QHBoxLayout, QToolTip
from PyQt6.QtGui import QPalette, QColor, QAction, QFont, QIcon
from PyQt6.QtCore import Qt, QSize
import sys

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)
        
def initRows(n):
    rows=[]
    rows.append(Color("#fdd701"))
    flag=0
    if n%2==0:
        flag=1
        n=n-1
    
    for x in range(1,int((n+1)/2)):
        rows.append(Color("#fee581"))
        rows.append(Color("#7c7c7a"))
    if flag==1:
        rows.append(Color("#fee581"))
    return rows
    
def initRowsLayout(n):
    rowsLayout=[]
	
    for x in range(n):
        rowsLayout.append(QHBoxLayout())
    return rowsLayout   

def assignLayoutRows(rows, rowsLayout):
    n=min(len(rows), len(rowsLayout))  
    for x in range(n):
        rows[x].setLayout(rowsLayout[x])
    return

app=QApplication(sys.argv)
app.setFont(QFont("Fira Code", 30))

window = QMainWindow()
window.setWindowTitle("Orari Certosa")
window.setWindowIcon(QIcon("icons\\train.png"))

QToolTip.setFont(QFont("Fira Code", 8))

toolbar = QToolBar("My main toolbar")
toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
toolbar.setIconSize(QSize(24,24))
toolbar.setFont(QFont("Fira Code", 10))
window.addToolBar(toolbar)
buttonRefresh = QAction(QIcon("icons\\arrow.png"),"Refresh", window)
toolbar.addAction(buttonRefresh)
buttonSettings = QAction(QIcon("icons\\gear.png"), "Settings", window)
toolbar.addAction(buttonSettings)
buttonClose = QAction(QIcon("icons\\cross.png"),"Close", window)
toolbar.addAction(buttonClose)

rowsLayout=initRowsLayout(6)
rows=initRows(6)

window.showFullScreen()