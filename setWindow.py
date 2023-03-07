#Developer: Federico De Rocco
#Written using PyQt6 Lib

from __future__ import print_function
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QToolBar, QLabel, QHBoxLayout, QToolTip, QLineEdit, QGroupBox, QPushButton
from PyQt6.QtGui import QPalette, QColor, QAction, QFont, QIcon, QWindow, QIntValidator
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
		buttonSettings.triggered.connect(self.showSettings)
		toolbar.addAction(buttonSettings)

		buttonClose = QAction(QIcon("icons\\cross.png"),"Close", self)
		buttonClose.triggered.connect(self.killApp)
		toolbar.addAction(buttonClose)
                
		self.addToolBar(toolbar)
    
	def refreshTrains(self):
		jsonFile=open("settings.json")
		main.refreshWindow(json.load(jsonFile))
		jsonFile.close()
		return
        
	def killApp(self):
		app.exit()
		return
        
	def showSettings(self):
		trainSettings.show()
		return

class settingsWindow(QMainWindow):
	fieldDeparturesStation=""
	fieldArrivalStation=""
	fieldDelayMargin=""
	fieldDelaySafe=""
	fieldFontPts=""

	def __init__(self):
		super(settingsWindow, self).__init__()
                
		
		jsonFile=open("settings.json")
		settings=json.load(jsonFile)
		jsonFile.close()
		mainWidget=QWidget()
        
		self.setWindowTitle("Settings")
		self.setWindowIcon(QIcon("icons\\gear.png"))
                
		mainWidget.setFont(QFont("Fira Code", 12))
                
		validDelay = QIntValidator(0, 60, self)
		validFont = QIntValidator(2, 40, self) 
       
		settingsLayout=QVBoxLayout()
        
        
		inputDeparturesStation=QLineEdit()
		inputDeparturesStation.setText(settings["departuresStationID"])
		inputDeparturesStation.textEdited.connect(self.editedDeparturesStation)
		self.fieldDeparturesStation=settings["departuresStationID"]
                
		inputArrivalStation=QLineEdit()
		inputArrivalStation.setText(settings["arrivalStationID"])
		inputArrivalStation.textEdited.connect(self.editedArrivalStation)
		self.fieldArrivalStation=settings["arrivalStationID"]
                
		inputDelayMargin=QLineEdit()
		inputDelayMargin.setValidator(validDelay)
		inputDelayMargin.setText(str(settings["delayMargin"]))
		inputDelayMargin.textEdited.connect(self.editedDelayMargin)
		self.fieldDelayMargin=str(settings["delayMargin"])
                
		inputDelaySafe=QLineEdit()
		inputDelaySafe.setValidator(validDelay)
		inputDelaySafe.setText(str(settings["delaySafe"]))
		inputDelaySafe.textEdited.connect(self.editedDelaySafe)
		self.fieldDelaySafe=str(settings["delaySafe"])
                
		inputFontPts=QLineEdit()
		inputFontPts.setValidator(validFont)
		inputFontPts.setText(str(settings["fontPts"]))
		inputFontPts.textEdited.connect(self.editedFontPts)
		self.fieldFontPts=str(settings["fontPts"])
                
		labelDepartureStation=QLabel("Departures station ID:")
		labelArrivalStation=QLabel("Arrival station ID:")
		labelDelayMargin=QLabel("Minimum delay:")
		labelDelaySafe=QLabel("Minutes removed:")
		labelFontPts=QLabel("Font points:")
                
		departureStation=QHBoxLayout()
		departureStation.addWidget(labelDepartureStation)
		departureStation.addWidget(inputDeparturesStation)
		widgetDeparturesStation = QWidget()
		widgetDeparturesStation.setLayout(departureStation)
                
		arrivalStation=QHBoxLayout()
		arrivalStation.addWidget(labelArrivalStation)
		arrivalStation.addWidget(inputArrivalStation)
		widgetArrivalStation = QWidget()
		widgetArrivalStation.setLayout(arrivalStation)
                
		delayMargin=QHBoxLayout()
		delayMargin.addWidget(labelDelayMargin)
		delayMargin.addWidget(inputDelayMargin)
		widgetDelayMargin = QWidget()
		widgetDelayMargin.setLayout(delayMargin)
                
		delaySafe=QHBoxLayout()
		delaySafe.addWidget(labelDelaySafe)
		delaySafe.addWidget(inputDelaySafe)
		widgetDelaySafe = QWidget()
		widgetDelaySafe.setLayout(delaySafe)
                
		fontPts=QHBoxLayout()
		fontPts.addWidget(labelFontPts)
		fontPts.addWidget(inputFontPts)
		widgetFontPts = QWidget()
		widgetFontPts.setLayout(fontPts)
                

		boxStationsSettings = QGroupBox()
		stationSettings=QVBoxLayout()
		boxStationsSettings.setTitle("Stations settings")
		stationSettings.addWidget(widgetDeparturesStation)
		stationSettings.addWidget(widgetArrivalStation)
		boxStationsSettings.setLayout(stationSettings)
		settingsLayout.addWidget(boxStationsSettings)
                
		boxDelaySettings=QGroupBox()
		delaySettings=QVBoxLayout()
		boxDelaySettings.setTitle("Delay settings")
		delaySettings.addWidget(widgetDelayMargin)
		delaySettings.addWidget(widgetDelaySafe)
		boxDelaySettings.setLayout(delaySettings)
		settingsLayout.addWidget(boxDelaySettings)

		boxFontSettings=QGroupBox()
		fontSettings=QVBoxLayout()
		boxFontSettings.setTitle("Font settings")
		fontSettings.addWidget(widgetFontPts)
		boxFontSettings.setLayout(fontSettings)
		settingsLayout.addWidget(boxFontSettings)
                
		buttonClose=QPushButton("Close", self)
		buttonClose.clicked.connect(self.closeWindow)
		buttonSave=QPushButton("Save", self)
		buttonSave.clicked.connect(self.saveSettings)

		buttonsLayout=QHBoxLayout()
		widgetButtons=QWidget()
		buttonsLayout.addWidget(buttonClose)
		buttonsLayout.addWidget(buttonSave)
		widgetButtons.setLayout(buttonsLayout)
		settingsLayout.addWidget(widgetButtons)


		mainWidget.setLayout(settingsLayout)
                
		self.setCentralWidget(mainWidget)
		return
    
	def closeWindow(self):
		self.close()
		main.resetSettings()
		return
	
	def saveSettings(self):
		settings=dict()

		settings["departuresStationID"]=self.fieldDeparturesStation
		settings["arrivalStationID"]=self.fieldArrivalStation
		settings["delayMargin"]=int(self.fieldDelayMargin)
		settings["delaySafe"]=int(self.fieldDelaySafe)
		settings["fontPts"]=int(self.fieldFontPts)
		
		jsonFile=open("settings.json", "w")
		json.dump(settings, jsonFile)
		jsonFile.close()

		main.refreshWindow(settings)
		self.close()
		return
        
	def editedDeparturesStation(self, s):
		self.fieldDeparturesStation=s
		return
              
	def editedArrivalStation(self, s):
		self.fieldArrivalStation=s
		return
              
	def editedDelayMargin(self, s):
		self.fieldDelayMargin=s
		return
	
	def editedDelaySafe(self, s):
		self.fieldDelaySafe=s
		return

	def editedFontPts(self, s):
		self.fieldFontPts=s
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
app.setWindowIcon(QIcon("icons\\train.png"))
QToolTip.setFont(QFont("Fira Code", 8))


trainMonitor=trainWindow()
trainSettings=settingsWindow()

rowsLayout=initRowsLayout(6)
rows=initRows(6)

trainMonitor.showFullScreen()



   

# app.exec()