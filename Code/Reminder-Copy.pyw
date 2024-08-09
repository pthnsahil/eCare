import winotify
import time as tm
import schedule
import subprocess
import sys
import os
import numpy as np
import mysql.connector as mysql
import datetime
import random
import socket
lines = ["Take a break and look outside.","Here's your virtual KitKat. Have a break, have a KitKat.","Taking a break can sometimes lead to breakthroughs.","Sometimes doing nothing makes way for everything. You certainly haven't tried it yet.","Learn to meditate because...In the silence of heart, one learns the journey of the wise.","Reminder...it's okay to stop and take a rest when you need one.","Taking time to do nothing often brings everything into perspective.","All that is important comes in quietness and waiting.","Today, i choose to take a <br/>. Would you?","Warning: prolonged work without breaks may result in spontaneous dance breaks. Proceed with caution.","Don't make me use my 'take a break' spell on you! (It's very persuasive.)","Break time is the best time. Trust me, I'm a breakologist!","Remember, breaks are not exceptions, they're part of the loop. Take one now!"]
PID = os.getpid()
file = open("Status.txt","w")
file.write(str(PID))
file.close()
Username = sys.argv[1]
NotDuration = sys.argv[2]
ForceOFF = int(sys.argv[3])
exceptionList = ["COM Surrogate"]
def is_connected():
    try:
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        pass
    return False
if is_connected() and ForceOFF != 1:
    conn = mysql.connect(host = 'localhost',database = 'eCare', user = 'root', password = "")
    cur = conn.cursor()
    cur.execute("SELECT ID FROM USER WHERE USERNAME = '%s';" % (Username))
    UID = cur.fetchone()[0]
    file = open("Data.txt","r")
    dataLines = file.readlines()
    Ind = 0
    while Ind < len(dataLines):
         startTime = (dataLines[Ind].split("\n",1))[0]
         startTime = datetime.datetime.strptime(startTime,"%Y-%m-%d %H:%M:%S.%f")
         endTime = startTime
         Ind = Ind + 2
         while dataLines[Ind] != "----------\n":
             data = dataLines[Ind].split("\t",2)
             curTime = datetime.datetime.strptime((data[2].split("\n",1))[0],"%Y-%m-%d %H:%M:%S.%f")
             if endTime < curTime:
                 endTime = curTime
             cur.execute("INSERT INTO ACTIVITY_METRICS (USER_ID, APP_NAME, START_TIME, END_TIME) VALUES ( %s, %s, %s, %s);",(UID, data[0], data[1], (data[2].split("\n",1))[0]))
             Ind += 1
         cur.execute("INSERT INTO SYSTEM_METRICS (USER_ID, START_TIME, END_TIME) VALUES ( %s, %s, %s);",(UID,startTime,endTime))
         Ind += 1
    file.close()
    file = open("Data.txt","w")
    file.close()
    conn.commit()
    cur.close()
    conn.close()
def checkProcess():
    cmd = ' powershell "gps | where { $_.MainWindowTitle } | select Description'
    proc = subprocess.Popen(cmd, shell= True, stdout = subprocess.PIPE)
    processes = []
    for line in proc.stdout:
        if not line.decode()[0].isspace():
            processes += [line.decode().rstrip()]
    return(processes[2:])
runProcesses = checkProcess()
startTime = datetime.datetime.now()
file = open("Data.txt","a")
file.write(str(startTime)+"\n")
file.write("----------\n")
for process in runProcesses:
    if process in exceptionList:
        continue
    file.write(process+"\t")
    file.write(str(datetime.datetime.now())+"\t")
    tm.sleep(1)
    file.write(str(datetime.datetime.now())+"\n")
file.write("----------\n")
file.close()
def updateTime():
    global runProcesses
    curProcesses = checkProcess()
    file = open("Data.txt","r")
    dataLines = file.readlines()
    file.close()
    startInd = dataLines.index(str(startTime)+"\n")
    Ind = startInd+2
    while Ind < len(dataLines):
        if (dataLines[Ind].split("\t",2))[0] in curProcesses:
            dataLines[Ind] = dataLines[Ind].replace((dataLines[Ind].split("\t",2))[2],str(datetime.datetime.now())+"\n")
        elif dataLines[Ind] == "----------\n":
                break
        Ind = Ind + 1
    for process in curProcesses:
        if process not in runProcesses and (dataLines[Ind].split("\t",2))[0] not in exceptionList:
            line = process+"\t"+str(datetime.datetime.now())+"\t"
            tm.sleep(1)
            dataLines.insert(startInd+2,line+str(datetime.datetime.now())+"\n")
    runProcesses = curProcesses
    file = open("Data.txt","w")
    file.writelines(dataLines)
    file.close()
def callNot():
    random.seed(datetime.datetime.now().second)
    choose = random.randrange(len(lines) - 1)
    toast = winotify.Notification(app_id = "eCare",title = "It's been "+NotDuration+" minutes!", msg = lines[choose],duration = "short", icon = "D:/eCare_COPY/Code/Images/bell-icon.png")
    toast.set_audio(winotify.audio.Mail,loop = False)
    toast.show()
NotifyTask = schedule.every(float(NotDuration)).minutes.do(callNot)
UpdateTask = schedule.every(1).seconds.do(updateTime)
while True:
    schedule.run_pending()
    tm.sleep(1)