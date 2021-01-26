#!/usr/bin/python3

import PySimpleGUI as sg
import os.path
from datetime import datetime
import csv

csvName = ''
currentTime = datetime.now()
fileStartTime = datetime.now()
workingVideoFile = ''
recordingFlag = False
videoLength = 3600

def mainLoop():
    global recordingFlag
    global csvName
    global currentTime
    global fileStartTime
    global workingVideoFile
    global videoLengthf

    while True:
        event, values = window.read(timeout=500)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        
        if event == "-FOLDER-":
            folder = values["-FOLDER-"]
            try:
                csvSetup(str(folder))
                window.FindElement("Start Recording").Update(disabled=False)
                window.FindElement("Submit Log with Time Stamp").Update(disabled=False)
            except:
                print ('Trying to set destination folder')
                print (Exception)
        
        if event == "Start Recording":
            try:
                window.FindElement("Start Recording").Update(disabled=True)
                window.FindElement("Stop Recording").Update(disabled=False)
                fileStartTime = datetime.now()
                currentVideoName = datetime.now().strftime("%m%d%Y%H%M%S")
                # Sent Bash command or whatever
                recordingFlag = True
            except:
                print ('Trying to start recording')
                print (Exception)

        if event == "Stop Recording":
            try:
                window.FindElement("Start Recording").Update(disabled=False)
                window.FindElement("Stop Recording").Update(disabled=True)
                # Send bash command or whatever
                recordingFlag = False
            except:
                print ('Trying to stop recording')
                print (Exception)
        
        if event == "Submit Log with Time Stamp":

            log = values["logText"].replace('\n', ' ')
            now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            currentVideoName = "video 50:relative time" # get this
            logEntry = [now,currentVideoName, log]

            try:
                ################################################################## new lines register as new cells -------fix it
                with open(csvName, "a") as logFile:
                    logWriter = csv.writer(logFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    logWriter.writerow(logEntry)

                window.FindElement("logText").Update('')
            except:
                print ('Trying to write CSV')
                print (Exception)

        if recordingFlag and (datetime.now() - fileStartTime).total_seconds() >= videoLength:
            fileStartTime = datetime.now()
            currentVideoName = datetime.now().strftime("%m%d%Y%H%M%S")
            

    window.close()

def windowSetup():

    global window
    global layout

    sg.theme('DarkBlue')

    firstColumn = [
        [
            sg.Text("Select Location to Save Video File:"),
            sg.In(size=(40, 1), enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse(),
        ],
        [
            sg.Text("                         ")
        ],
        [
            sg.Multiline(size=(200, 50), key='logText')
        ],
        [
            sg.Text ("                                                                                      "),
            sg.Button("Submit Log with Time Stamp", disabled=True),
        ],
    ]

    secondColumn = [
        [
            sg.Button("Start Recording", disabled=True),
        ],
        [
            sg.Text("               ")
        ],
        [
            sg.Text("               ")
        ],
        [
            sg.Button("Stop Recording", disabled=True),
        ],
    ]

    layout = [
        [
            sg.Column(firstColumn),
            sg.Column(secondColumn)
        
        ]
    ]

def csvSetup(dirr):
    global csvName

    now = datetime.now().strftime("%m-%d-%Y")
    csvName = dirr + "/" + now + ".csv"
    
    if  not os.path.exists(csvName):
        try:
            with open(csvName, "w") as logFile:
                logWriter = csv.writer(logFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                logWriter.writerow(['TIMESTAMP', 'VIDEO TIMESTAMP', 'LOG'])
        except:
            print('In csvSetup Function')
            print(Exception)
    
windowSetup()
window = sg.Window("Video Recorder", layout)
mainLoop()