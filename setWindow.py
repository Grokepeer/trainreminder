#Developer: Federico De Rocco
#Written using PyQt6 Lib

from __future__ import print_function
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QToolBar, QLabel, QHBoxLayout
from PyQt6.QtGui import QPalette, QColor, QAction, QFont
from PyQt6.QtCore import Qt
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

toolbar = QToolBar("My main toolbar")
toolbar.setFont(QFont("Fira Code", 10))
window.addToolBar(toolbar)
buttonRefresh = QAction("Refresh", window)
toolbar.addAction(buttonRefresh)
buttonClose = QAction("Close", window)
toolbar.addAction(buttonClose)

rowsLayout=initRowsLayout(6)
rows=initRows(6)

window.showFullScreen()