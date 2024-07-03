import subprocess
import os
cmd = 'python "Reminder - Copy.pyw" Kiyan 1'
data = open("Status.txt","r").readlines()
if len(data) == 0:
    print("The script is not running! Do you wish to run it?")
    choice = int(input())
    if choice == 1:
        subprocess.Popen(cmd, shell= True)
    else:
        exit()
print("The script is up & running!")
choice = int(input("Do you wish to terminate it?"))
if choice == 1:
    data = open("Status.txt","r").readlines()
    cmd = 'taskkill /F /PID '+data[0]
    subprocess.Popen(cmd, shell= True)
    open("Status.txt","w").close()


