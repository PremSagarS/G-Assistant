from time import sleep
import win11toast
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

reminderFile = open('D:\\reminders.txt')

reminders = []

DATEONLY = 123
DATETIME = 321
DATETIMEFORMAT = '%d-%m-%y-%H-%M-%S'
DATEONLYFORMAT = '%d-%m-%y'

for line in reminderFile.readlines():
    remname,remstring =  line.strip().split()
    try:
        reminder = datetime.strptime(remstring, DATETIMEFORMAT)
        remType = DATETIME
    except ValueError:
        reminder = datetime.strptime(remstring, DATEONLYFORMAT)
        remType = DATEONLY
    
    reminders.append((remname, reminder, remType))

reminderFile.close()

newReminders = []

for remname, reminder, remType in reminders:
    time_now = datetime.now()
    if remType == DATEONLY:
        if abs((time_now - reminder).days) == 0:
            retval = win11toast.toast("Time for an event!!!", remname, icon = "D:/Projects/GenAIHackathon/mail.avif", buttons=['Dismiss', 'Snooze'])
            if retval == {'arguments': 'http:Snooze', 'user_input': {}}:
                newReminders.append((remname, datetime.now() + timedelta(minutes=10), DATETIME))
        else:
            newReminders.append((remname, reminder, remType))
    elif remType == DATETIME:
        diffa = (time_now - reminder)
        if diffa.days == -1 or diffa.seconds < 120:
            retval = win11toast.toast("Time for an event!!!", remname, icon = "D:/Projects/GenAIHackathon/mail.avif", buttons=['Dismiss', 'Snooze'])
            if retval == {'arguments': 'http:Snooze', 'user_input': {}}:
                newReminders.append((remname, datetime.now() + timedelta(minutes=10), DATETIME))
            else:
                newReminders.append((remname, reminder, remType))

reminderFile = open('D:\\reminders.txt', 'w')

for remname, reminder, remType in newReminders:
    if remType == DATETIME:
        reminderFile.write(f"{remname} {reminder.strftime(DATETIMEFORMAT)}\n")
    else:
        reminderFile.write(f"{remname} {reminder.strftime(DATEONLYFORMAT)}\n")