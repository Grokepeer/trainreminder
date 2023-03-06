#Developer: Federico De Rocco
#Written using PyQt6 Lib

from __future__ import print_function
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QToolBar, QLabel, QHBoxLayout, QToolTip
from PyQt6.QtGui import QPalette, QColor, QAction, QFont, QIcon
from PyQt6.QtCore import Qt, QSize
import sys
import main
import json

rows=[]
rowsLayout=[]

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)
        
class trainWindow(QMainWindow):
	def __init__(self):
		super(trainWindow, self).__init__()
                
		self.setWindowTitle("Orari Certosa")
		self.setWindowIcon(QIcon("icons\\train.png"))
                
		toolbar = QToolBar("My main toolbar")
		toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
		toolbar.setIconSize(QSize(24,24))
		toolbar.setFont(QFont("Fira Code", 10))
                
		buttonRefresh = QAction(QIcon("icons\\arrow.png"),"Refresh", self)
		buttonRefresh.triggered.connect(self.refreshTrains)
		toolbar.addAction(buttonRefresh)


		buttonSettings = QAction(QIcon("icons\\gear.png"), "Settings", self)
		toolbar.addAction(buttonSettings)

		buttonClose = QAction(QIcon("icons\\cross.png"),"Close", self)
		buttonClose.triggered.connect(self.close)
		toolbar.addAction(buttonClose)
                
		self.addToolBar(toolbar)
    
	def refreshTrains(self):
		main.refreshWindow(json.load(open("settings.json")))
		return
        

        
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
app.setFont(QFont("Fira Code", 28))

QToolTip.setFont(QFont("Fira Code", 8))


w=trainWindow()

rowsLayout=initRowsLayout(6)
rows=initRows(6)

w.showFullScreen()



   

# app.exec()