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
    for x in range(n):
        rows.append(QWidget)
    return rows
    
def initRowsLayout(n):
    rowsLayout=[]
    for x in range(n):
        rowsLayout.append(QHBoxLayout)
    return rowsLayout   

def assignLayoutRows(rows, rowsLayout):
    n=min(len(rows), len(rowsLayout))  
    for x in range(n):
        rows[n].setLayout(rowsLayout[n])
    return




app=QApplication(sys.argv)
app.setFont(QFont("Fira Code", 30))

window = QMainWindow()
window.setWindowTitle("Orari Certosa")

rowsLayout=initRowsLayout(6)
rows=initRows(6)

