import sys
import csv
import enums
import pickle
from enums import Alarms


alarms = {}


with open('AlarmList.csv', 'r', encoding='utf-8') as f:
            rdr = csv.reader(f)
            
            alarmList = [] 
            
            for row in rdr:
                 alarmList.append(row)
                #  print(connList)
                #  connectListBox.addItem(row[0])
# alarms = dict(alarmList)


for i in Alarms:
    alarms[i.name] = alarmList[i.value]
    # print(alarms[i.name][1])

# print(alarms)

with open('AlarmList.bin', 'wb') as f:
     pickle.dump(alarms, f)