#Developer: Federico De Rocco
#Written using PyQt6 Lib

from __future__ import print_function
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QToolBar, QLabel, QHBoxLayout, QToolTip, QLineEdit, QGroupBox, QPushButton, QStatusBar, QCheckBox
from PyQt6.QtGui import QPalette, QColor, QAction, QFont, QIcon, QWindow, QIntValidator
from PyQt6.QtCore import Qt, QSize, QTimer
from time import sleep
import sys
import main
import json

rows=[]
rowsLayout=[]

jsonStations=open("vt_data\\stationIDs.json")
stationIDs=json.load(jsonStations)
jsonStations.close()

jsonFile=open("settings.json")
settings=json.load(jsonFile)
jsonFile.close()

app=QApplication(sys.argv)
app.setFont(QFont("Fira Code", 28))
app.setWindowIcon(QIcon("icons\\train.png"))
QToolTip.setFont(QFont("Fira Code", 8))



class RefreshTimer(QTimer):
	def __init__(self):
		super(RefreshTimer, self).__init__()

		self.timeout.connect(self.refreshWindow)
		return

	def refreshWindowSettings(self, trains):
		rows=initRows(6)
		rowsLayout=initRowsLayout(6)

		main.setRowsWindow(trains, rows, rowsLayout)
		layoutWindow=QVBoxLayout()
    

		for x in rows:
			layoutWindow.addWidget(x)

		trainMonitor.setNewLayout(layoutWindow)
		return

	def refreshWindow(self):
		trainMonitor.refreshing()
		app.processEvents()
		trains=main.getFilteredList(settings["departuresStationID"], settings["arrivalStationID"], 6)
		self.refreshWindowSettings(trains)
		trainMonitor.setTrains(trains)
		main.trains=trains
		trainMonitor.white()
		return

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)
        
class trainWindow(QMainWindow):
	trains=[]
	statusBarRef=QStatusBar()
	stationDeparturesName=""
	stationArrivalName=""
	def __init__(self):
		super(trainWindow, self).__init__()

		self.statusBar=QStatusBar()    
		self.setWindowTitle("Orari Certosa")
		self.setWindowIcon(QIcon("icons\\train.png"))

		self.stationDeparturesName=stationIDs["S0"+settings["departuresStationID"]]
		self.stationArrivalName=stationIDs["S0"+settings["arrivalStationID"]]	
                
		toolbar = QToolBar("mainToolbar")
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
                
		self.statusBarRef.setFont(QFont("Fira Code", 10))
		self.statusBar.showMessage("Milano Certosa")
			
		self.addToolBar(toolbar)
		self.setStatusBar(self.statusBarRef)
    
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
	
	def setTrains(self, trainsList):
		self.trains=trainsList
		return
	
	def setNewLayout(self, newLayout):
		widget=QWidget()
		widget.setLayout(newLayout)
		self.setCentralWidget(widget)
		return
	
	def refreshing(self):
		self.findChild(QStatusBar).showMessage("Refreshing train list | Please Wait...")
		return
	
	def white(self):
		self.findChild(QStatusBar).showMessage(self.stationDeparturesName + " -> "+self.stationArrivalName)
		return

class settingsWindow(QMainWindow):
	fieldDeparturesStation=""
	fieldArrivalStation=""
	fieldDelayMargin=""
	fieldDelaySafe=""
	fieldFontPts=""
	fieldRefresh=0

	flagNeedsTrainsRefresh=0

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
		validFont = QIntValidator(2, 80, self) 
		validRefreshTime = QIntValidator(1000, 300000)
       
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

		inputRefresh=QCheckBox()
		if settings["refresh"]!=1:
			inputRefresh.setCheckState(Qt.CheckState.Checked)
		else:
			inputRefresh.setCheckState(Qt.CheckState.Unchecked)
		inputRefresh.stateChanged.connect(self.editedRefresh)
		self.fieldRefresh=settings["refresh"]

		inputRefreshTime=QLineEdit()
		inputRefreshTime.setText(str(settings["refreshTime"]))
		inputRefreshTime.setValidator(validRefreshTime)
		inputRefreshTime.textEdited.connect(self.editedRefreshTime)
		self.fieldRefreshTime=settings["refreshTime"]

                
		labelDepartureStation=QLabel("Departures station ID:")
		labelArrivalStation=QLabel("Arrival station ID:")
		labelDelayMargin=QLabel("Minimum delay:")
		labelDelaySafe=QLabel("Minutes removed:")
		labelFontPts=QLabel("Font points:")
		labelRefresh=QLabel("Automatic refresh:")
		labelRefreshTime=QLabel("Seconds between refreshes:")
                
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

		refresh=QHBoxLayout()
		refresh.addWidget(labelRefresh)
		refresh.addWidget(inputRefresh)
		widgetRefresh=QWidget()
		widgetRefresh.setLayout(refresh)

		refreshTime=QHBoxLayout()
		refreshTime.addWidget(labelRefreshTime)
		refreshTime.addWidget(inputRefreshTime)
		widgetRefreshTime=QWidget()
		widgetRefreshTime.setLayout(refreshTime)
                

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

		boxRefreshSettings=QGroupBox()
		refreshSettings=QVBoxLayout()
		boxRefreshSettings.setTitle("Refresh settings")
		refreshSettings.addWidget(widgetRefresh)
		refreshSettings.addWidget(widgetRefreshTime)
		boxRefreshSettings.setLayout(refreshSettings)
		settingsLayout.addWidget(boxRefreshSettings)
                
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
		settings["refresh"]=int(self.fieldRefresh)
		settings["refreshTime"]=int(self.fieldRefreshTime)

		trainMonitor.stationDeparturesName=stationIDs["S0"+settings["departuresStationID"]]
		trainMonitor.stationArrivalName=stationIDs["S0"+settings["arrivalStationID"]]
		
		jsonFile=open("settings.json", "w")
		json.dump(settings, jsonFile)
		jsonFile.close()
		if self.flagNeedsTrainsRefresh==1:
			main.refreshWindow(settings)
			self.flagNeedsTrainsRefresh=0
		else:
			main.refreshWindowSettings(settings, trainMonitor.trains)
		self.close()
		return
        
	def editedDeparturesStation(self, s):
		self.flagNeedsTrainsRefresh=1
		self.fieldDeparturesStation=s
		return
              
	def editedArrivalStation(self, s):
		self.flagNeedsTrainsRefresh=1
		self.fieldArrivalStation=s
		return
              
	def editedDelayMargin(self, s):
		self.flagNeedsTrainsRefresh=1
		self.fieldDelayMargin=s
		return
	
	def editedDelaySafe(self, s):
		self.flagNeedsTrainsRefresh=1
		self.fieldDelaySafe=s
		return

	def editedFontPts(self, s):
		self.fieldFontPts=s
		return

	def editedRefresh(self, n):
		self.fieldRefresh=n
		return

	def editedRefreshTime(self, s):
		self.fieldRefreshTime=s
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


trainMonitor=trainWindow()
trainSettings=settingsWindow()

trainMonitor.white()

if(settings["refresh"]!=0):
	refreshTimer=RefreshTimer()
	refreshTimer.start(settings["refreshTime"]*1000)

rowsLayout=initRowsLayout(6)
rows=initRows(6)

trainMonitor.showFullScreen()
