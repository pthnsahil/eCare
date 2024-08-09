from customtkinter import *
from tkinter import *
from PIL import Image
import subprocess
import os
from CTkMessagebox import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mysql.connector as mysql
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
import datetime
import sys
import io
import socket
import requests
import base64
import numpy as np
def is_connected():
    try:
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        pass
    return False
def DelRepo(frameRep):
    frameRep.place_forget()
    frameRep.destroy()
    PastRepoFrame(1)
def openRepo(index):
    global dataLines
    conn = mysql.connect(host = 'localhost',database = 'eCare', user = 'root', password = "")
    cur = conn.cursor()
    cur.execute("SELECT USERNAME FROM USER WHERE ID = '%s';" % (dataLines[index,2]))
    Username = cur.fetchone()[0]
    if dataLines[index,5] == 0:
        cur.execute("UPDATE monthly_rep_record SET VALIDATION_STATUS = 1 WHERE VIGILANTE_ID = '%s' AND USER_ID = '%s' AND REPORT_FROM = %s  AND REPORT_TO = %s;",(dataLines[index,1],dataLines[index,2],dataLines[index,3],dataLines[index,4]))
    cur.execute("SELECT COALESCE(SUM(TIME_TO_SEC(TIMEDIFF(CONVERT(END_TIME,TIME),CONVERT(START_TIME,TIME)))),0) FROM system_metrics WHERE CONVERT(START_TIME,DATE) = %s AND CONVERT(END_TIME,DATE) = %s AND USER_ID = '%s';",(datetime.datetime.now().date(), datetime.datetime.now().date(), dataLines[index,2]))
    TodayValue = int(cur.fetchone()[0]/3600)
    cur.execute("SELECT COALESCE(SUM(TIME_TO_SEC(TIMEDIFF(CONVERT(END_TIME,TIME),CONVERT(START_TIME,TIME)))),0) FROM system_metrics WHERE DATEDIFF(%s,START_TIME) BETWEEN 1 AND 7 AND DATEDIFF(%s,START_TIME) BETWEEN 1 AND 7 AND USER_ID = '%s';",(datetime.datetime.now().date(), datetime.datetime.now().date(), dataLines[index,2]))
    WeekValue = int(cur.fetchone()[0]/3600)
    cur.execute("SELECT COALESCE(SUM(TIME_TO_SEC(TIMEDIFF(CONVERT(END_TIME,TIME),CONVERT(START_TIME,TIME)))),0) FROM system_metrics WHERE DATEDIFF(%s,START_TIME) BETWEEN 1 AND 30 AND DATEDIFF(%s,START_TIME) BETWEEN 1 AND 30 AND USER_ID = '%s'",(datetime.datetime.now().date(), datetime.datetime.now().date(), dataLines[index,2]))
    MonthValue = int(cur.fetchone()[0]/3600)
    conn.commit()
    cur.close()
    conn.close()
    PastRepoFrame(0)
    PastRepoContentFrame = CTkScrollableFrame(master = Content, fg_color = "#CAD4E2")
    PastRepoContentFrame.place(relx = 0.5, rely = 0.5, relwidth = 0.98, relheight = 0.98, anchor = CENTER)
    ProfileLabel = CTkLabel(master = PastRepoContentFrame, image = ProfileImage, text = " "+Username, text_color = "#484545", font = ("Helvetica",30), compound = "left")
    ProfileLabel.grid(row = 0, column = 0, columnspan = 2, sticky = "nw", padx = (20,0))
    BackButton = CTkButton(master = PastRepoContentFrame, image = ArrowImage, fg_color = "#CAD4E2", text = "", hover_color = "#ADBACF", height = 50, width = 0, corner_radius = 6, command = lambda: DelRepo(PastRepoContentFrame))
    BackButton.grid(row = 0, column = 2, sticky = "")
    InfoLabel = CTkLabel(master = PastRepoContentFrame, text = str(dataLines[index,2])+" | "+str(dataLines[index,3].date())+" - "+str(dataLines[index,4].date()), text_color = "#5B5B5B", font = ("Helvetica",15))
    InfoLabel.grid(row = 1, column = 0, columnspan = 3, sticky = "nw", padx = (20,0), pady = (10,0))
    TodayFrame = CTkFrame(master = PastRepoContentFrame, fg_color = "#E8E8E8", height = 120, width = 180, corner_radius = 0)
    TodayFrameBottom = CTkFrame(master = TodayFrame, fg_color = "#237CCB", height = 120, corner_radius = 0)
    WeekFrame = CTkFrame(master = PastRepoContentFrame, fg_color = "#E8E8E8", height = 120, width = 180, corner_radius = 0)
    WeekFrameBottom = CTkFrame(master = WeekFrame, fg_color = "#D20103", height = 120, corner_radius = 0)
    MonthFrame = CTkFrame(master = PastRepoContentFrame, fg_color = "#E8E8E8", height = 120, width = 180, corner_radius = 0)
    MonthFrameBottom = CTkFrame(master = MonthFrame, fg_color = "#33B001", height = 120, corner_radius = 0)
    TodayFrameBottom.place(rely = 0.98,relwidth = 1,relheight = 0.02)
    MonthFrameBottom.place(rely = 0.98,relwidth = 1,relheight = 0.02)
    WeekFrameBottom.place(rely = 0.98,relwidth = 1,relheight = 0.02)
    TodayFrame.grid(row = 2, column = 0, padx = (20,10), pady = 10)
    WeekFrame.grid(row = 2, column = 1, padx = (0,10), pady = 10)
    MonthFrame.grid(row = 2, column = 2, padx = (0,20), pady = 10)
    TodayUsageLabel = CTkLabel(master = TodayFrame, text = "Today's Usage", text_color = "#6A6A6A", font = ("Helvetica",13))
    WeekUsageLabel = CTkLabel(master = WeekFrame, text = "Last Week's Usage", text_color = "#6A6A6A", font = ("Helvetica",13))
    MonthUsageLabel = CTkLabel(master = MonthFrame, text = "Last Month's Usage", text_color = "#6A6A6A", font = ("Helvetica",13))
    TodayUsageLabel.place(relx = 0.05, rely = 0.01, anchor = "nw")
    WeekUsageLabel.place(relx = 0.05, rely = 0.01, anchor = "nw")
    MonthUsageLabel.place(relx = 0.05, rely = 0.01, anchor = "nw")
    TodayDataLabel =  CTkLabel(master = TodayFrame,text = TodayValue, text_color = "#237CCB", font = ("Helvetica",50))
    WeekDataLabel =  CTkLabel(master = WeekFrame,text = WeekValue, text_color = "#D20103", font = ("Helvetica",50))
    MonthDataLabel =  CTkLabel(master = MonthFrame,text = MonthValue, text_color = "#33B001", font = ("Helvetica",50))
    TodayUnitLabel = CTkLabel(master = TodayFrame,text = "hr", text_color = "#484545", font = ("Helvetica",50))
    WeekUnitLabel = CTkLabel(master = WeekFrame,text = "hr", text_color = "#484545", font = ("Helvetica",50))
    MonthUnitLabel = CTkLabel(master = MonthFrame,text = "hr", text_color = "#484545", font = ("Helvetica",50))
    TodayDataLabel.place(relx = 0.3, rely = 0.6, anchor = CENTER)
    TodayUnitLabel.place(relx = 0.7, rely = 0.6, anchor = CENTER)
    WeekDataLabel.place(relx = 0.3, rely = 0.6, anchor = CENTER)
    WeekUnitLabel.place(relx = 0.7, rely = 0.6, anchor = CENTER)
    MonthDataLabel.place(relx = 0.3, rely = 0.6, anchor = CENTER)
    MonthUnitLabel.place(relx = 0.7, rely = 0.6, anchor = CENTER)
    PieFrame = CTkFrame(master = PastRepoContentFrame, fg_color = "#E8E8E8", corner_radius = 0)
    ChartFrame = CTkFrame(master = PastRepoContentFrame, fg_color = "#E8E8E8", corner_radius = 0, height = 220)
    PieFrame.grid(row = 3, column = 0, columnspan = 3,sticky = "nsew", padx = (20,20), pady = 10)
    ChartFrame.grid(row = 4,column = 0, columnspan = 3, sticky = "nsew", padx = (20,20), pady = 10)
    PieLabel = CTkLabel(master = PieFrame,text = "Top 5 Apps Used", text_color = "#6A6A6A", font = ("Helvetica",13))
    ChartLabel = CTkLabel(master = ChartFrame,text = "Usage Per Day", text_color = "#6A6A6A", font = ("Helvetica",13))
    PieLabel.place(relx = 0.02, rely = 0.01, anchor = "nw")
    ChartLabel.place(relx = 0.02, rely = 0.01, anchor = "nw")
    PastRepoContentFrame.grid_rowconfigure(4,weight = 1)
    #From ReportAnalysis File
    conn = mysql.connect(host = 'localhost',database = 'eCare', user = 'root', password = "")
    cur = conn.cursor()
    cur.execute("SELECT APP_NAME,COALESCE(SUM(TIME_TO_SEC(TIMEDIFF(CONVERT(END_TIME,TIME),CONVERT(START_TIME,TIME)))),0) AS DUR FROM activity_metrics WHERE USER_ID = '%s' AND DATEDIFF(%s,START_TIME) BETWEEN 1 AND 30 AND DATEDIFF(%s,END_TIME) BETWEEN 1 AND 30 GROUP BY APP_NAME ORDER BY DUR DESC LIMIT 5;",(dataLines[index,2],dataLines[index,4],dataLines[index,4]))
    apps = np.array(cur.fetchall())
    cur.execute("SELECT (31-DATEDIFF(%s,START_TIME)) AS DAY,COALESCE(SUM(TIME_TO_SEC(TIMEDIFF(CONVERT(END_TIME,TIME),CONVERT(START_TIME,TIME)))),0) FROM system_metrics WHERE USER_ID = '%s' AND DATEDIFF(%s,START_TIME) BETWEEN 1 AND 30 AND DATEDIFF(%s,START_TIME) BETWEEN 1 AND 30 GROUP BY CONVERT(START_TIME,DATE) ORDER BY DAY;",(dataLines[index,4], dataLines[index,2], dataLines[index,4], dataLines[index,4]))
    dayData = np.array(cur.fetchall())
    dayData[:,1] = dayData[:,1]/3600
    conn.commit()
    cur.close()
    conn.close()
    default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    figPie = plt.figure(facecolor = "#E8E8E8")
    figPie.add_subplot(111)
    plt.pie(apps[:,1])
    plt.gcf().gca().add_artist(plt.Circle((0,0),0.7,color = "#E8E8E8"))
    canvasPie = FigureCanvasTkAgg(figPie,master = PieFrame)
    canvasPie.draw()
    canvasPie.get_tk_widget().place(relx = 0,rely = 0.15, relwidth = 0.3, relheight = 0.85)
    App = []
    for i in range(5):
        App = App + [CTkButton(master = PieFrame, text = apps[i,0], fg_color = default_colors[i], hover_color = default_colors[i], text_color = "white", font = ("Helvetica",12))]
    App[0].place(relx = 0.6,rely = 0.2, relheight = 0.2, anchor = "e")
    App[1].place(relx = 0.87,rely = 0.2, relheight = 0.2, anchor = "e")
    App[2].place(relx = 0.6,rely = 0.5, relheight = 0.2, anchor = "e")
    App[3].place(relx = 0.87,rely = 0.5, relheight = 0.2, anchor = "e")
    App[4].place(relx = 0.76,rely = 0.8, relheight = 0.2, anchor = "e")

    #LineChart
    figLine = plt.figure(facecolor = "#E8E8E8", figsize = (5,1.8))
    ax = figLine.add_subplot(111)
    ax.tick_params(labelsize = 7)
    plt.plot(dayData[:,0],dayData[:,1],marker = "o")
    for i,(xi,yi) in enumerate(zip(dayData[:,0],dayData[:,1])):
        plt.annotate(f'({xi},{yi})',(xi,yi),textcoords = "offset points",xytext = (0,7),ha = "center", fontsize = 7)
    plt.xlabel("Days")
    plt.ylabel("Usage [in hrs]")
    plt.xlim(1,30)
    plt.grid(True)
    canvasLine = FigureCanvasTkAgg(figLine,master = ChartFrame)
    canvasLine.draw()
    canvasLine.get_tk_widget().place(relx = 0.05,rely = 0.11)
def changeStatus(to):
    if to == 0:
        ActiveMonitorLabel.place_forget()
        ActiveMonitorButton.place_forget()
        data = open("Status.txt","r").readlines()
        cmd = 'taskkill /F /PID '+data[0]
        subprocess.Popen(cmd, shell= True)
        open("Status.txt","w").close()
        InactiveMonitorLabel.place(relx = 0.5, rely = 0.5, anchor = CENTER)
        InactiveMonitorButton.place(relx = 0.5, rely = 0.8, anchor = CENTER)
    else:
        InactiveMonitorLabel.place_forget()
        InactiveMonitorButton.place_forget()
        conn = mysql.connect(host = 'localhost',database = 'eCare', user = 'root', password = "")
        cur = conn.cursor()
        cur.execute("SELECT SYSTEM_ALERT_DURATION,FORCE_OFFLINE FROM SETTINGS_AND_PRIVILEGES WHERE USER_ID IN (SELECT ID FROM USER WHERE USERNAME = '%s');" % (SuperUser))
        info = cur.fetchone()
        cmd = 'python "Reminder-Copy.pyw" '+SuperUser+' '+str(info[0].seconds/60)+' '+str(info[1])
        subprocess.Popen(cmd, shell= True)
        ActiveMonitorLabel.place(relx = 0.5, rely = 0.5, anchor = CENTER)
        ActiveMonitorButton.place(relx = 0.5, rely = 0.8, anchor = CENTER)
def setActive(frame):
    global currentFrame
    if currentFrame == 1:
        HomeFrame(0)
    elif currentFrame == 2:
        SettingsFrame(0)
    elif currentFrame == 3:
        PastRepoFrame(0)
    elif currentFrame == 5:
        LogFrame(0)
    elif currentFrame == 6:
        SignFrame(0)
    if frame == 1:
        Home.configure(fg_color = "#CAD4E2", hover_color = "#CAD4E2")
        Settings.configure(fg_color = "#4C7AE4", hover_color = "#B6913D")
        PastRepo.configure(fg_color = "#4C7AE4", hover_color = "#B6913D")
        LogOut.configure(fg_color = "#4C7AE4", hover_color = "#B6913D")
        Exit.configure(fg_color = "#4C7AE4", hover_color = "#B6913D")
        HomeFrame(1)
        currentFrame = 1
    elif frame == 2:
        Settings.configure(fg_color = "#CAD4E2", hover_color = "#CAD4E2")
        Home.configure(fg_color = "#4C7AE4", hover_color = "#B6913D")
        PastRepo.configure(fg_color = "#4C7AE4", hover_color = "#B6913D")
        Exit.configure(fg_color = "#4C7AE4", hover_color = "#B6913D")
        LogOut.configure(fg_color = "#4C7AE4", hover_color = "#B6913D")
        SettingsFrame(1)
        currentFrame = 2
    elif frame == 3:
        PastRepo.configure(fg_color = "#CAD4E2", hover_color = "#CAD4E2")
        Settings.configure(fg_color = "#4C7AE4", hover_color = "#B6913D")
        Home.configure(fg_color = "#4C7AE4", hover_color = "#B6913D")
        Exit.configure(fg_color = "#4C7AE4", hover_color = "#B6913D")
        LogOut.configure(fg_color = "#4C7AE4", hover_color = "#B6913D")
        PastRepoFrame(1)
        currentFrame = 3
    elif frame == 4: 
        Exit.configure(fg_color = "#CAD4E2", hover_color = "#CAD4E2")
        Settings.configure(fg_color = "#4C7AE4", hover_color = "#B6913D")
        PastRepo.configure(fg_color = "#4C7AE4", hover_color = "#B6913D")
        Home.configure(fg_color = "#4C7AE4", hover_color = "#B6913D")
        LogOut.configure(fg_color = "#4C7AE4", hover_color = "#B6913D")
        ExitFrame()
        newFrame = currentFrame
        currentFrame = 4
        setActive(newFrame)
    elif frame == 5:
        LogFrame(1)
        currentFrame = 5
    elif frame == 6:
        SignFrame(1)
        currentFrame = 6
    else:
        LogOut.configure(fg_color = "#CAD4E2", hover_color = "#CAD4E2")
        Settings.configure(fg_color = "#4C7AE4", hover_color = "#B6913D")
        Home.configure(fg_color = "#4C7AE4", hover_color = "#B6913D")
        Exit.configure(fg_color = "#4C7AE4", hover_color = "#B6913D")
        PastRepo.configure(fg_color = "#4C7AE4", hover_color = "#B6913D")
        if LogOutFrame() != "Yes":
            newFrame = currentFrame
            currentFrame = 7
            setActive(newFrame)
        else:
            setActive(5)
 
def updateTimer(value):
    global timerValue
    timerValue=int(value)
    timerTracker.configure(text=str(int(value))+"  Minutes" )

def convert_to_z_o(value):
    return 1 if value =="on" else 0

def saveData():
    global NewVigil, RemVigil
    conn = mysql.connect(host = 'localhost',database = 'eCare', user = 'root', password = "")
    cur = conn.cursor()
    cur.execute("SELECT ID FROM USER WHERE USERNAME = '%s';" % (SuperUser))
    UID=cur.fetchone()[0]
    v1=timerValue*60
    Sys_alert= datetime.timedelta(seconds=v1)
    m_r_g=convert_to_z_o(switch_var1.get())
    f_o=convert_to_z_o(switch_var2.get())
    r_v=convert_to_z_o(switch_var3.get())
    cur.execute("UPDATE settings_and_privileges SET FORCE_OFFLINE='%s', GENERATE_MONTHLY_REPORT='%s', REP_TO_VIGILANTE='%s' ,SYSTEM_ALERT_DURATION='%s' WHERE USER_ID='%s';"% (f_o, m_r_g, r_v, Sys_alert, UID))
    for Vigil in RemVigil:
        cur.execute("DELETE FROM VIGILANTE WHERE USER_ID = '%s' AND VIGILANTE_ID = '%s';",(UID,int(Vigil[0])))
    RemVigil = np.array([])
    for Vigil in NewVigil:
        cur.execute("INSERT INTO VIGILANTE (USER_ID,VIGILANTE_ID) VALUES ('%s','%s');", (UID,int(Vigil)))
    NewVigil = []
    conn.commit()
    setActive(2)
    
def convert_to_on_off(value):
    return "on" if value !=0 else "off"

def AdditionVigil(AddVigil,AddVigilErr):
    global NewVigil, SuperUser
    if len(AddVigil.get()) == 0:
        AddVigilErr.configure(text = "*No Username specified!")
    elif AddVigil.get() == SuperUser:
        AddVigilErr.configure(text = "*Incorrect Username!")
    else:
        conn = mysql.connect(host = 'localhost',database = 'eCare', user = 'root', password = "")
        cur = conn.cursor()
        cur.execute("SELECT ID FROM USER WHERE USERNAME = '%s';" % (AddVigil.get()))
        ID = cur.fetchall()
        if len(ID) != 0:
            NewVigil = np.insert(NewVigil,0,np.array(ID)[:,0])
            AddVigil.delete(0,'end')
            AddVigilErr.configure(text = "")
        else:
            AddVigilErr.configure(text = "*Username does not exist!")
def RemoveVigil(dataLines, DelVigil):
    global RemVigil
    if DelVigil.get() != "None":
        if len(RemVigil) != 0: 
            RemVigil = np.insert(RemVigil,0,dataLines[np.where(dataLines[:,1] == DelVigil.get())][0], axis = 0)
        else:
            RemVigil = dataLines[np.where(dataLines[:,1] == DelVigil.get())]
        DelVigil.configure(values = np.delete(dataLines,np.where(dataLines[:,1] == DelVigil.get())[0], axis = 0)[:,1])
        DelVigil.set("None")
def SettingsFrame(Status):
    global SettingsContent,timerTracker,data,switch_var1,switch_var2,switch_var3,timerValue
    conn = mysql.connect(host = 'localhost',database = 'eCare', user = 'root', password = "")
    cur = conn.cursor()
    cur.execute("SELECT ID FROM USER WHERE USERNAME = '%s';" % (SuperUser))
    UID=cur.fetchone()[0]
    cur.execute("SELECT * FROM settings_and_privileges WHERE USER_ID='%s';" % (UID))
    data=np.array(cur.fetchall())

    if Status==1:
    
     SettingsContent.place(relx = 0.5, rely = 0.5, relwidth = 0.9, relheight = 0.9, anchor = CENTER)
     timerLab = CTkLabel(master = SettingsContent, text = "Timer Duration",font = ("Helvetica",15,"bold"), text_color = "#6A6A6A")
     timerLab.place(relx = 0.1, rely = 0.09)
     sp = CTkSlider(SettingsContent, from_=1, to=100 , button_color ="medium blue",height=20,command=updateTimer,button_hover_color = "#4C7AE4",width=350,progress_color="#4C7AE4",)
     sp.set(int(data[0][4].seconds/60))
     timerValue=sp.get()
     sp.place(relx = 0.5, rely = 0.19,anchor=CENTER)
     timerTracker = CTkLabel(master = SettingsContent,text = str(int(data[0][4].seconds/60))+"  Minutes",font = ("Helvetica",15,"bold"), text_color = "#6A6A6A")
     timerTracker.place(relx = 0.75, rely = 0.09)
     
     val1=convert_to_on_off(data[0][2])
     switch_var1 =StringVar(value=val1)
     mrLab = CTkLabel(master = SettingsContent, text = "Monthly Report Drafting",font = ("Helvetica",15,"bold"), text_color = "#6A6A6A")
     mrLab.place(relx = 0.1, rely = 0.25)
     se = CTkSwitch(SettingsContent,variable=switch_var1, onvalue="on", offvalue="off",text="",height=20,progress_color="#4C7AE4",button_color ="medium blue",button_hover_color = "#4C7AE4")
     se.place(relx = 0.75, rely = 0.25)
    
     val2=convert_to_on_off(data[0][1])
     switch_var2 =StringVar(value=val2)
     fsLab = CTkLabel(master = SettingsContent, text = "Force Offline",font = ("Helvetica",15,"bold"), text_color = "#6A6A6A")
     fsLab.place(relx = 0.1, rely = 0.35)
     se1 = CTkSwitch(SettingsContent,variable=switch_var2, onvalue="on", offvalue="off",text="",height=20,progress_color="#4C7AE4",button_color ="medium blue",button_hover_color = "#4C7AE4")
     se1.place(relx = 0.75, rely = 0.35)

     val3=convert_to_on_off(data[0][3])
     switch_var3 =StringVar(value=val3)
     fsLab = CTkLabel(master = SettingsContent, text = "Inform Vigilante",font = ("Helvetica",15,"bold"), text_color = "#6A6A6A")
     fsLab.place(relx = 0.1, rely = 0.45)
     se1 = CTkSwitch(SettingsContent,variable=switch_var3, onvalue="on", offvalue="off",text="",height=20,progress_color="#4C7AE4",button_color ="medium blue",button_hover_color = "#4C7AE4")
     se1.place(relx = 0.75, rely = 0.45)
     DelVigilLab = CTkLabel(master = SettingsContent, text = "Remove Vigilante",font = ("Helvetica",15,"bold"), text_color = "#6A6A6A")
     DelVigilLab.place(relx = 0.1, rely = 0.55)
     conn = mysql.connect(host = 'localhost',database = 'eCare', user = 'root', password = "")
     cur = conn.cursor()
     cur.execute("SELECT ID,USERNAME FROM USER WHERE ID IN (SELECT VIGILANTE_ID FROM VIGILANTE WHERE USER_ID IN (SELECT ID FROM USER WHERE USERNAME = '%s') AND USER_ID <> VIGILANTE_ID);" % (SuperUser))
     dataLines = np.array(cur.fetchall())
     if len(dataLines) != 0:
        dataLines = np.insert(dataLines,0,['0','None'], axis = 0)
     else:
        dataLines = np.array([['0','None']])
     DelVigil = CTkOptionMenu(SettingsContent, values = (dataLines[:,1]))
     DelVigilButton = CTkButton(SettingsContent, fg_color = "#C30809", hover_color = "#960405", text = "Remove", command = lambda: RemoveVigil(dataLines,DelVigil))
     DelVigil.place(relx = 0.4, rely = 0.55)
     DelVigilButton.place(relx = 0.7, rely = 0.55)

     AddVigilLab = CTkLabel(master = SettingsContent, text = "Add Vigilante",font = ("Helvetica",15,"bold"), text_color = "#6A6A6A")
     AddVigilLab.place(relx = 0.1, rely = 0.65)
     AddVigil = CTkEntry(master = SettingsContent, placeholder_text = "Vigil Username", fg_color = "#FFFFFF", border_width = 0, placeholder_text_color = "#606060", text_color = "#606060", corner_radius = 20)
     AddVigilButton = CTkButton(SettingsContent, fg_color = "#0E5A91", hover_color = "#14496F", text = "Add", command = lambda: AdditionVigil(AddVigil,AddVigilErr))
     AddVigil.place(relx = 0.4, rely = 0.65)
     AddVigilButton.place(relx = 0.7, rely = 0.65)
     AddVigilErr = CTkLabel(master = SettingsContent, text = "", text_color = "#D20103", font = ("Helvetica",13))
     AddVigilErr.place(relx = 0.4, rely = 0.70)
     SaveButton = CTkButton(master = SettingsContent, text = "Save", fg_color = "#4DAD27", hover_color = "#4AA227",font = ("Helvetica",15),command=saveData,width=100,height=30)
     SaveButton.place(relx = 0.5, rely = 0.85,anchor=CENTER)
     
    else:
      RemVigil = np.array([])
      NewVigil = []
      SettingsContent.place_forget()
      for widget in SettingsContent.winfo_children():
            widget.destroy()

def RepoInfoFrame(Name,From,To,index):
    global GreenTickImage
    Repoframe = CTkFrame(master = RepoContent, fg_color = "#E8E8E8", height = 120, corner_radius = 0)
    NewFrameBottom = CTkFrame(master = Repoframe, fg_color = "#37AD07", height = 120, corner_radius = 0)
    OldFrameBottom = CTkFrame(master = Repoframe, fg_color = "#8F8E8E", height = 120, corner_radius = 0)
    UserLabel = CTkLabel(master = Repoframe, text = "User: "+Name, text_color = "#6A6A6A")
    DateLabel = CTkLabel(master = Repoframe, text = "Duration: "+str(From)+" to "+str(To), text_color = "#6A6A6A")
    ViewButton = CTkButton(master = Repoframe, text = "View Report", fg_color = "#0E5A91", hover_color = "#14496F", command = lambda: openRepo(index))
    DateLabel.place(relx = 0.95,rely = 0.15, anchor = "e")
    UserLabel.place(relx = 0.05,rely = 0.02)
    if dataLines[index,5] == 1:
        OldFrameBottom.place(relx = 0.993, rely = 0,relwidth = 0.007,relheight = 1)
    else:
        NewFrameBottom.place(relx = 0.993, rely = 0,relwidth = 0.007,relheight = 1)
    ViewButton.place(relx = 0.95, rely = 0.9, relwidth = 0.2, relheight = .3, anchor = "se")
    return(Repoframe)
def PastRepoFrame(Status):
    global RepoContent
    global frame
    global dataLines
    if Status == 1:
    
        conn = mysql.connect(host = 'localhost',database = 'eCare', user = 'root', password = "")
        cur = conn.cursor()
        cur.execute("SELECT ID FROM USER WHERE USERNAME = '%s';" % (SuperUser))
        UID = cur.fetchone()[0]
        cur.execute("SELECT * FROM monthly_rep_record WHERE VIGILANTE_ID = '%s';" % (UID))
        dataLines = np.array(cur.fetchall())
        conn.commit()
        cur.close()
        conn.close()
        RepoContent.place(relx = 0.5, rely = 0.5, relwidth = 0.98, relheight = 0.98, anchor = CENTER)
        for i in range(len(dataLines)):
            conn = mysql.connect(host = 'localhost',database = 'eCare', user = 'root', password = "")
            cur = conn.cursor()
            cur.execute("SELECT USERNAME FROM USER WHERE ID = '%s';" % (dataLines[i,2]))
            repName = UID = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
            frame = frame + [RepoInfoFrame(repName,dataLines[i,3].date(),dataLines[i,4].date(),i)]
            frame[i].grid(row = i, column = 0, sticky = "nsew", pady = 7)
    else:
        RepoContent.place_forget()

        for widget in RepoContent.winfo_children():
            widget.destroy()
        frame = []
        frame.clear()
def HomeFrame(Status):
    global UserImage, UserName
    if Status == 1:
        if is_connected():
            conn = mysql.connect(host = 'localhost',database = 'eCare', user = 'root', password = "")
            cur = conn.cursor()
            cur.execute("SELECT PROFILE_PHOTO FROM USER WHERE USERNAME = '%s';" % (SuperUser))
            img = CTkImage(Image.open(io.BytesIO(base64.b64decode(cur.fetchone()[0]))),size = (165,100))
            UserName.configure(image = img)
        UserName.configure(text = SuperUser)
        data = open("Status.txt","r").readlines()
        if len(data) == 0:
            InactiveMonitorLabel.place(relx = 0.5, rely = 0.5, anchor = CENTER)
            InactiveMonitorButton.place(relx = 0.5, rely = 0.8, anchor = CENTER)
        else:
            ActiveMonitorLabel.place(relx = 0.5, rely = 0.5, anchor = CENTER)
            ActiveMonitorButton.place(relx = 0.5, rely = 0.8, anchor = CENTER)
    else:
        data = open("Status.txt","r").readlines()
        if len(data) == 0:
            InactiveMonitorLabel.place_forget()
            InactiveMonitorButton.place_forget()
        else:
            ActiveMonitorLabel.place_forget()
            ActiveMonitorButton.place_forget()
def ExitFrame():
    msg = CTkMessagebox(title="Exit?", message="Are you sure you wish to quit the application?", icon="warning", option_1="Cancel", option_2="Yes")
    if msg.get() == "Yes":
        root.destroy()
        exit()
def LogOutFrame():
    msg = CTkMessagebox(title="Logging Out?", message="Unsaved changes may no longer persist.  Are you sure?", icon="warning", option_1="Cancel", option_2="Yes")
    if msg.get() == "Yes":
        open("UserCred.txt","w").close()
    return(msg.get())
def Resize(self):
    global root
    LogInImage.configure(size = (root.winfo_width()*0.5,root.winfo_height()))
def LogInCred(LogInPageUser, LogInPagePass, LogInPageErr):
    global SuperUser
    if LogInPageUser.get() == "":
        LogInPageErr.configure(text = "*Username is required!")
    elif LogInPagePass.get() == "":
        LogInPageErr.configure(text = "*Password is required!")
    else:
        conn = mysql.connect(host = 'localhost',database = 'eCare', user = 'root', password = "")
        cur = conn.cursor()
        cur.execute("SELECT * FROM USER WHERE USERNAME = '%s';" % (LogInPageUser.get()))
        dataLines = cur.fetchall()
        if len(dataLines) == 0:
            LogInPageErr.configure(text = "*Username is incorrect!")
        elif dataLines[0][3] != LogInPagePass.get():
            LogInPageErr.configure(text = "*Password is incorrect!")
        else:
            LogInPageErr.configure(text = "")
            SuperUser = LogInPageUser.get()
            f = open("UserCred.txt","w")
            f.write(SuperUser+"\n")
            f.close()
            setActive(1)
def LogFrame(Status):
    if Status == 1:
        LogInImage = CTkImage(Image.open("Images/134.jpg"),size = (500,600))
        LogInImageLabel =  CTkLabel(master = LogInImageFrame, image = LogInImage, text = "", text_color = "white", pady = 10, font = ("Helvetica",20))
        LogInPageLabel = CTkLabel(master = LogInPageFrame, text = "Login", text_color = "black", font = ("NoirPro-Regular",30))
        LogInPageUser = CTkEntry(master = LogInPageFrame, placeholder_text = "Enter your username", fg_color = "#FFFFFF", border_width = 0, placeholder_text_color = "#606060", text_color = "#606060", corner_radius = 20)
        LogInPagePass = CTkEntry(master = LogInPageFrame, placeholder_text = "Enter your password", fg_color = "#FFFFFF", border_width = 0, show = "*", placeholder_text_color = "#606060", text_color = "#606060", corner_radius = 20)
        LogInPageSub = CTkButton(master = LogInPageFrame, text = "Log In", fg_color = "#A755A9", hover_color = "#8B278D", corner_radius = 20, font = ("Helvetica",15), command = lambda: LogInCred(LogInPageUser, LogInPagePass, LogInPageErr))
        LogInPageSignUpLabel = CTkLabel(master = LogInPageFrame, text = "Not a member?", text_color = "#606060", font = ("Helvetica",15))
        LogInPageSignUp = CTkButton(master = LogInPageFrame, text = "Sign up", anchor = "w", fg_color = "#CAD4E2", hover_color = "#CAD4E2", border_width = 0, font = ("Helvetica",15), text_color = "blue", command = lambda: setActive(6))
        LogInPageLabel.place(relx = 0.1, rely = 0.05, anchor = "nw")
        LogInUserImageLabel =  CTkLabel(master = LogInPageFrame, image = LogInUserImage, anchor = "e", text = "", fg_color = "#FFFFFF", pady = 10, font = ("Helvetica",20))
        LogInPassImageLabel =  CTkLabel(master = LogInPageFrame, image = LogInPassImage, anchor = "e", text = "", fg_color = "#FFFFFF", pady = 10, font = ("Helvetica",20))
        LogInPageErr = CTkLabel(master = LogInPageFrame, text = "", text_color = "#D20103", font = ("Helvetica",13))
        LogInImageLabel.place(relx = 0.5, rely = 0.5, relwidth = 1, relheight = 1, anchor = CENTER)
        LogInImageFrame.place(relx = 0, rely = 0, relwidth = 0.5, relheight = 1, anchor = "nw")
        LogInPageFrame.place(relx = 1, rely = 0, relwidth = 0.5, relheight = 1, anchor = "ne")
        LogInPageUser.place(relx = 0.1, rely = 0.2, relwidth = 0.8, relheight = 0.1)
        LogInUserImageLabel.place(relx = 0.76, rely = 0.2, relwidth = 0.1, relheight = 0.1)
        LogInPagePass.place(relx = 0.1, rely = 0.4, relwidth = 0.8, relheight = 0.1)
        LogInPassImageLabel.place(relx = 0.76, rely = 0.4, relwidth = 0.1, relheight = 0.1)
        LogInPageSub.place(relx = 0.5, rely = 0.6, relwidth = 0.4, relheight = 0.08, anchor = CENTER)
        LogInPageSignUpLabel.place(relx = 0.44, rely = 0.68, relwidth = 0.4, relheight = 0.08, anchor = CENTER)
        LogInPageSignUp.place(relx = 0.74, rely = 0.68, anchor = CENTER)
        LogInPageErr.place(relx = 0.5, rely = 0.75, anchor = CENTER)
        root.bind("<Configure>",Resize)
    else:
        LogInImageFrame.place_forget()
        LogInPageFrame.place_forget()
        root.unbind("<Configure>")
        for widget in LogInImageFrame.winfo_children():
            widget.destroy()
        for widget in LogInPageFrame.winfo_children():
            widget.destroy()
def getFile(Profile):
    global file
    filename = filedialog.askopenfilename()
    if filename != "":
        file = open(filename,'rb').read()
        file = base64.b64encode(file)
        Profile.configure(state = "normal")
        Profile.insert(0,filename)
        Profile.configure(state = "disabled")
def SignUpCred(SignUpProg,FullName,UserName,Password,ConPassword,DOB,SignUpErr):
    global file, SuperUser
    if SignUpProg.get() < 0.9:
        SignUpErr.configure(text = "*All fields are mandatory!")
    elif Password.get() != ConPassword.get():
        SignUpErr.configure(text = "*The Password should be same as Confirm Password!")
    else:
        conn = mysql.connect(host = 'localhost',database = 'eCare', user = 'root', password = "")
        cur = conn.cursor()
        cur.execute("SELECT * FROM USER WHERE USERNAME = '%s';" % (UserName.get()))
        dataLines = cur.fetchall()
        if len(dataLines) != 0:
            SignUpErr.configure(text = "*The Username already exists!")
        else:
            cur.execute("INSERT INTO USER (FULL_NAME,USERNAME,PASSWORD,DATE_OF_BIRTH,AGE,PROFILE_PHOTO) VALUES (%s,%s,%s,%s,%s,%s);",(FullName.get(),UserName.get(),Password.get(),DOB.get_date(),datetime.datetime.now().year - DOB.get_date().year,file))
            conn.commit()
            cur.close()
            conn.close()
            SuperUser = UserName.get()
            f = open("UserCred.txt","w")
            f.write(SuperUser+"\n")
            f.close()
            setActive(1)
def CheckProg(event,SignUpProg,FullName,UserName,Password,ConPassword,DOB):
    global file
    SignUpProg.set(0)
    Step = 0
    if FullName.get() != "":
        Step += 1/6
    if UserName.get() != "":
        Step += 1/6
    if Password.get() != "":
        Step += 1/6
    if ConPassword.get() != "":
        Step += 1/6
    if file != 0:
        Step += 1/6
    if DOB.get_date() != datetime.datetime.now().date():
        Step += 1/6
    SignUpProg.set(Step)
def SignFrame(Status):
    if Status == 1:
        SignUpFrame.place(relx = 0,rely = 0.01, relwidth = 1, relheight = 0.99)
        SignUpFrameBot.place(relx = 0,rely = 0, relwidth = 1, relheight = 0.01)
        SignUpProg = CTkProgressBar(master = SignUpFrameBot, orientation = "horizontal", progress_color = "#FE9900")
        SignUpProg.set(0)
        SignUpProg.place(relx = 0.5, rely = 0.5, relwidth = 1, relheight = 1, anchor = CENTER)
        for i in range(2):
            SignUpFrame.grid_columnconfigure(i,weight = 1)
        AccLabel = CTkLabel(master = SignUpFrame, text = "Create your account", text_color = "black", font = ("NoirPro-Regular",30))
        AccLabel.grid(row = 0, column = 0, sticky = "w", ipadx = 10, pady = (10,0))
        FullNameLabel = CTkLabel(master = SignUpFrame, text = "Full Name", text_color = "black", font = ("NoirPro-Regular",20))
        FullNameLabel.grid(row = 1, column = 0, sticky = "w", padx = (30,0), pady = (30,0), columnspan = 1)
        FullName =  CTkEntry(master = SignUpFrame, placeholder_text = "Enter your Full Name", fg_color = "#FFFFFF", border_width = 0, placeholder_text_color = "#606060", text_color = "#606060", corner_radius = 20, font = ("NoirPro-Regular",20), height = 50)
        FullName.bind("<FocusOut>", lambda event: CheckProg(event,SignUpProg,FullName,UserName,Password,ConPassword,DOB))
        FullName.grid(row = 2, column = 0, sticky = "ew", padx = (20,0), pady = (10,0), columnspan = 1)
        SignUpUserImageLabel =  CTkLabel(master = SignUpFrame, image = LogInUserImage, anchor = "e", text = "", fg_color = "#FFFFFF", pady = 10, font = ("NoirPro-Regular",20))
        SignUpUserImageLabel.grid(row = 2, column = 0, sticky = "e", padx = (30,10), pady = (10,0))
        #
        UserNameLabel = CTkLabel(master = SignUpFrame, text = "User Name", text_color = "black", font = ("NoirPro-Regular",20))
        UserNameLabel.grid(row = 1, column = 1, sticky = "w", padx = (30,0), pady = (40,0), columnspan = 1)
        UserName =  CTkEntry(master = SignUpFrame, placeholder_text = "Enter your Username", fg_color = "#FFFFFF", border_width = 0, placeholder_text_color = "#606060", text_color = "#606060", corner_radius = 20, font = ("NoirPro-Regular",20), height = 50)
        UserName.bind("<FocusOut>", lambda event: CheckProg(event,SignUpProg,FullName,UserName,Password,ConPassword,DOB))
        UserName.grid(row = 2, column = 1, sticky = "ew", padx = (20,20), pady = (10,0), columnspan = 1)
        SignUpUserImageLabel =  CTkLabel(master = SignUpFrame, image = LogInUserImage, anchor = "e", text = "", fg_color = "#FFFFFF", pady = 10, font = ("NoirPro-Regular",20))
        SignUpUserImageLabel.grid(row = 2, column = 1, sticky = "e", padx = (30,30), pady = (10,0))
        ##
        PasswordLabel = CTkLabel(master = SignUpFrame, text = "Password", text_color = "black", font = ("NoirPro-Regular",20))
        PasswordLabel.grid(row = 3, column = 0, sticky = "w", padx = (30,0), pady = (40,0), columnspan = 1)
        Password =  CTkEntry(master = SignUpFrame, show = "*", placeholder_text = "Enter your Password", fg_color = "#FFFFFF", border_width = 0, placeholder_text_color = "#606060", text_color = "#606060", corner_radius = 20, font = ("NoirPro-Regular",20), height = 50)
        Password.bind("<FocusOut>", lambda event: CheckProg(event,SignUpProg,FullName,UserName,Password,ConPassword,DOB))
        Password.grid(row = 4, column = 0, sticky = "ew", padx = (20,0), pady = (10,0), columnspan = 1)
        SignUpPassImageLabel =  CTkLabel(master = SignUpFrame, image = LogInPassImage, anchor = "e", text = "", fg_color = "#FFFFFF", pady = 10, font = ("NoirPro-Regular",20))
        SignUpPassImageLabel.grid(row = 4, column = 0, sticky = "e", padx = (30,10), pady = (10,0))
        #
        ConPasswordLabel = CTkLabel(master = SignUpFrame, text = "Confirm Password", text_color = "black", font = ("NoirPro-Regular",20))
        ConPasswordLabel.grid(row = 3, column = 1, sticky = "w", padx = (30,0), pady = (40,0), columnspan = 1)
        ConPassword =  CTkEntry(master = SignUpFrame, show = "*", placeholder_text = "Confirm your Password", fg_color = "#FFFFFF", border_width = 0, placeholder_text_color = "#606060", text_color = "#606060", corner_radius = 20, font = ("NoirPro-Regular",20), height = 50)
        ConPassword.bind("<FocusOut>", lambda event: CheckProg(event,SignUpProg,FullName,UserName,Password,ConPassword,DOB))
        ConPassword.grid(row = 4, column = 1, sticky = "ew", padx = (20,20), pady = (10,0), columnspan = 1)
        SignUpCPassImageLabel =  CTkLabel(master = SignUpFrame, image = LogInPassImage, anchor = "e", text = "", fg_color = "#FFFFFF", pady = 10, font = ("NoirPro-Regular",20))
        SignUpCPassImageLabel.grid(row = 4, column = 1, sticky = "e", padx = (30,30), pady = (10,0))
        ##
        ProfileLabel = CTkLabel(master = SignUpFrame, text = "Profile Picture", text_color = "black", font = ("NoirPro-Regular",20))
        ProfileLabel.grid(row = 5, column = 0, sticky = "w", padx = (30,0), pady = (40,0), columnspan = 1)
        Profile =  CTkEntry(master = SignUpFrame, fg_color = "#FFFFFF", border_width = 0, text_color = "#606060", corner_radius = 20, font = ("NoirPro-Regular",20), height = 50)
        Profile.insert(0,"No File Selected")
        Profile.configure(state = "disabled")
        Profile.grid(row = 6, column = 0, sticky = "ew", padx = (20,0), pady = (10,0), columnspan = 1)
        ProfileButton = CTkButton(master = SignUpFrame, text = "Choose a File", height = 50, corner_radius = 0, bg_color = "#FFFFFF", fg_color = "#5F5656", hover_color = "#443D3D", font = ("NoirPro-Regular",15), command = lambda: getFile(Profile))
        ProfileButton.bind("<Button-1>", lambda event: CheckProg(event,SignUpProg,FullName,UserName,Password,ConPassword,DOB))
        ProfileButton.grid(row = 6, column = 0, sticky = "e", padx = (30,0), pady = (10,0))
        #
        DOBLabel = CTkLabel(master = SignUpFrame, text = "Date OF Birth", text_color = "black", font = ("NoirPro-Regular",20))
        DOBLabel.grid(row = 5, column = 1, sticky = "w", padx = (30,0), pady = (40,0), columnspan = 1)
        DOB =  DateEntry(master = SignUpFrame, selectmode='day', font = ("Helvetica",15))
        DOB.bind("<FocusOut>", lambda event: CheckProg(event,SignUpProg,FullName,UserName,Password,ConPassword,DOB))
        DOB.grid(row = 6, column = 1, sticky = "ew", padx = (20,20), pady = (10,0), columnspan = 1)
        #
        ProfileSub = CTkButton(master = SignUpFrame, text = "Submit", height = 50, corner_radius = 10, bg_color = "#CAD4E2", fg_color = "#D88403", hover_color = "#975C03", font = ("NoirPro-Regular",15), command = lambda: SignUpCred(SignUpProg,FullName,UserName,Password,ConPassword,DOB,SignUpErr))
        ProfileSub.bind("<Enter>", lambda event: CheckProg(event,SignUpProg,FullName,UserName,Password,ConPassword,DOB))
        ProfileSub.grid(row = 7, column = 0, padx = (30,0), pady = (50,0), columnspan = 2)
        #
        SignUpErr = CTkLabel(master = SignUpFrame, text = "", text_color = "#D20103", font = ("NoirPro-Regular",15))
        SignUpErr.grid(row = 8, column = 0, padx = (30,0), pady = (20,0), columnspan = 2)
    else:
        SignUpFrame.place_forget()
        SignUpFrameBot.place_forget()
        for widget in SignUpFrame.winfo_children():
            widget.destroy()
        for widget in SignUpFrameBot.winfo_children():
            widget.destroy()
currentFrame = 1
frame = []
dataLines = []
SuperUser = ""
RemVigil = np.array([])
NewVigil = np.array([], dtype = int)
root = CTk()
root.title("eCare")
root.geometry("800x600")
height = root.winfo_height()
width = root.winfo_width()
Menu = CTkFrame(master = root, fg_color = "#4C7AE4")
file = 0
FontManager.load_font("C:/Users/HP/eCare/Noir/NoirPro-Regular.ttf")
Content = CTkFrame(master = root, fg_color = "#CAD4E2")
SignUpFrame = CTkScrollableFrame(master = root, fg_color = "#CAD4E2", corner_radius = 0)
SignUpFrameBot = CTkFrame(master = root, fg_color = "#CAD4E2", corner_radius = 0)
RepoContent = CTkScrollableFrame(master=Content, fg_color="#CAD4E2")
SettingsContent=CTkFrame(master=Content,fg_color="#E8E8E8")
RepoContent.grid_columnconfigure(0,weight = 1)
User = CTkFrame(master = Menu, corner_radius = 0, fg_color = "#4C7AE4")
MenuOpt = CTkFrame(master = Menu, corner_radius = 0, fg_color = "#4C7AE4")
MenuFoot = CTkFrame(master = Menu, corner_radius = 0, fg_color = "#4C7AE4")
SettingsImage = CTkImage(Image.open("Images/settings-icon.png"),size = (30,30))
LogInImageFrame = CTkFrame(master = root)
LogInImage = CTkImage(Image.open("Images/134.jpg"),size = (500,600))
LogInUserImage = CTkImage(Image.open("Images/username-icon.jpg"),size = (30,30))
LogInPassImage = CTkImage(Image.open("Images/password-icon.jpg"),size = (30,30))
LogOutImage = CTkImage(Image.open("Images/log-out-icon.jpg"),size = (30,30))
LogInPageFrame = CTkFrame(master = root, fg_color = "#CAD4E2")
PastRepoImage = CTkImage(Image.open("Images/reports-icon.png"),size = (30,30))
HomeImage = CTkImage(Image.open("Images/home-icon.png"),size = (30,30))
ExitImage = CTkImage(Image.open("Images/exit-icon.png"),size = (30,30))
ArrowImage = CTkImage(Image.open("Images/arrow-icon.png"),size = (55,55))
ProfileImage = CTkImage(Image.open("Images/profile-icon.png"),size = (50,50))
GreenTickImage = CTkImage(Image.open("Images/greentick-icon.png"),size = (15,15))
UserImage = CTkImage(Image.open("Images/user-icon.png"),size = (165,100))
ActiveMonitorImage = CTkImage(Image.open("Images/monitor-active-icon.png"),size = (200,200))
ActiveMonitorButton = CTkButton(master = Content, text = "Terminate Session", fg_color = "#DC1E1E", hover_color = "#BB2323", command = lambda: changeStatus(0))
InactiveMonitorButton = CTkButton(master = Content, text = "Start a Session", fg_color = "#4DAD27", hover_color = "#4AA227", command = lambda: changeStatus(1))
InactiveMonitorImage = CTkImage(Image.open("Images/monitor-inactive-icon.png"),size = (200,200))
UserName = CTkLabel(master = User, image = UserImage, text = SuperUser, pady = 10, font = ("Helvetica",20))
ActiveMonitorLabel = CTkLabel(master = Content, image = ActiveMonitorImage, text = "The session is currently active", text_color = "black", pady = 10, font = ("Helvetica",20))
InactiveMonitorLabel = CTkLabel(master = Content, image = InactiveMonitorImage, text = "The system is not being monitored", text_color = "black", pady = 5, font = ("Helvetica",20))
UserName._label.config(relief="solid", compound="top")
ActiveMonitorLabel._label.config(relief="solid", compound="top")
InactiveMonitorLabel._label.config(relief="solid", compound="top")
User.place(relx = 0, rely = 0,relheight = .3, relwidth = 1)
MenuOpt.place(relx = 0, rely = 0.3,relheight = .5, relwidth = 1)
MenuFoot.place(relx = 0, rely = 0.8,relheight = .2, relwidth = 1)
Home = CTkButton(master = MenuOpt, anchor = "w", corner_radius = 15, text = "Home", text_color = "black", fg_color = "#CAD4E2", hover_color = "#CAD4E2", image = HomeImage, command = lambda: setActive(1))
Settings = CTkButton(master = MenuOpt, anchor = "w", corner_radius = 15, text = "Settings", text_color = "black", fg_color = "#4C7AE4", hover_color = "#B6913D", image = SettingsImage, command = lambda: setActive(2))
LogOut = CTkButton(master = MenuOpt, anchor = "w", corner_radius = 15, text = "Log Out", text_color = "black", fg_color = "#4C7AE4", hover_color = "#B6913D", image = LogOutImage, command = lambda: setActive(7))
PastRepo = CTkButton(master = MenuOpt, anchor = "w", corner_radius = 15, text = "Past Reports", text_color = "black", fg_color = "#4C7AE4", hover_color = "#B6913D", image = PastRepoImage, command = lambda: setActive(3))
Exit = CTkButton(master = MenuOpt, anchor = "w", corner_radius = 15, text = "Quit", text_color = "black", fg_color = "#4C7AE4", hover_color = "#B6913D", image = ExitImage, command = lambda: setActive(4))
Home.place(relx = 0.25, rely = 0.05, relheight = 0.13, relwidth = 0.8)
Settings.place(relx = 0.25, rely = 0.45, relheight = 0.13, relwidth = 0.8)
PastRepo.place(relx = 0.25, rely = 0.25, relheight = 0.13, relwidth = 0.8)
LogOut.place(relx = 0.25, rely = 0.65, relheight = 0.13, relwidth = 0.8)
Exit.place(relx = 0.25, rely = 0.85, relheight = 0.13, relwidth = 0.8)
UserName.place(relx = 0.5, rely = 0.5, anchor = CENTER)
Menu.place(relx = 0, rely = 0, relwidth = 0.25, relheight = 1)
Content.place(relx = 0.25, rely = 0, relwidth= 0.75, relheight = 1)
root.protocol("WM_DELETE_WINDOW", sys.exit)
file = open("UserCred.txt","r")
dataLog = file.readlines()
if len(dataLog) == 0:
    currentFrame = 5
    LogFrame(1)
else:
    SuperUser = (dataLog[0].split("\n",2))[0]
    HomeFrame(1)
root.mainloop()