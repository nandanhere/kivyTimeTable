import csv,os,sys
from datetime import datetime
from time import sleep
from plyer import notification
from pathlib import Path
from jnius import autoclass

from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient

CLIENT = OSCClient('localhost', 3002)
# enable for debug prints
DEBUG = False
# monday is 0
days = {
 0 : "Monday",
1 : "Tuesday",
2: "Wednesday",
3 : "Thursday",
4 : "Friday",
5 : "Saturday",
6 : "Sunday",
}


def giveTimes(table):
    times = [(0,0)]
    rawtimes = [(0,0)]
    for x in table[0][1:]:
        ss = x.split('-')
        t1,t2 = list(map(int,ss[0].split(':'))),list(map(int,ss[1].split(':'))) #type:ignore
        tt1,tt2 = int('{:02d}{:02d}'.format(t1[0] + 12 if t1[0] < 6 else t1[0],t1[1] + 12 if t1[1] < 6 else t1[1])),int('{:02d}{:02d}'.format(t2[0] + 12 if t2[0] < 6 else t2[0],t2[1] + 12 if t2[1] < 6 else t2[1]))
        times.append((tt1,tt2)) #type:ignore
        rawtimes.append((ss[0],ss[1]))
    return (times,rawtimes)

def giveMessage(ind,sub,next):
        rets = ""
        if sub == next == 'free' or sub == next == '':
            rets = "You are Free ! go home and enjoy :)"
        elif ind + 1 < len(rawtimes):
            if next != "" or next != "free":
                rets =  "You now have {} from {} to {} \n Next You have {} at {}".format(sub,rawtimes[ind][0],rawtimes[ind][1],next,rawtimes[ind + 1][0])
        else:
            rets = "You now have {} from {} to {} \n Yay! you are free after that".format(sub,rawtimes[ind][0],rawtimes[ind][1])
        return rets
def sendNotif(ind,sub,nextsub):
    message = giveMessage(ind=ind,sub=sub,next=nextsub)
    notification.notify(title="Time Table",message=message) #type:ignore


if __name__ == '__main__':
    PythonService = autoclass('org.kivy.android.PythonService')
    # PythonService.mService.setAutoRestartService(True)
    recievedDataOnce = False
    times,rawtimes,table = [],[],[]
    from android.storage import primary_external_storage_path                   #type: ignore
     
    dir = primary_external_storage_path()
    download_dir_path = os.path.join(dir, 'Download')                           #type: ignore
    addr = download_dir_path + "/timeTable.csv"
    if Path(addr).exists():
      with open(addr,'r') as f: #type:ignore
              cs = csv.reader(f)
              table = []
              for row in cs:
                  table.append(row)
              times,rawtimes = giveTimes(table)
    else:
      with open(os.path.join(sys.path[0],'assets/tt.csv'),'r') as f: #type:ignore
              cs = csv.reader(f)
              table = []
              with open(addr,'w') as w:
                csw = csv.writer(w)
                for row in cs:
                  table.append(row)
                  csw.writerow(row)
              times,rawtimes = giveTimes(table)

    SERVER = OSCThreadServer()
    SERVER.listen('localhost', port=3000, default=True)
    def sendinfo(data=True):
        global recievedDataOnce,times, table
        ss = '0;' + str(times) + ";" + str(table)  if data else '1'
        message = bytes(ss,'utf-8')
        if DEBUG : print('was pinged! will send',times, table)
        CLIENT.send_message(b'/message',[message, ],)
        recievedDataOnce = True
    SERVER.bind(b'/ping',sendinfo)
    
    count = 0
    while True:
        cdt = datetime.now()
        day = days[cdt.today().weekday()]
        currtime = int("{:02d}{:02d}".format(cdt.hour,cdt.minute))
        flip = False
        for row in table:
                for i in range(len(row)):
                    entry = row[i]
                    if count % 600 == 0 and day == row[0]:
                        if DEBUG:print("Notification!")
                        if  times[i][0] <= currtime <=  times[i][1]:
                            if i + 1 < len(row):
                                sendNotif(ind=i,sub=entry,nextsub=row[i + 1])  #type:ignore
                            else:
                                sendNotif(ind=i,sub=entry,nextsub='free')  
                            flip = True
        if not flip and count % 600 == 0 :sendNotif(0,"free","free")
        count %= 600
        if DEBUG : print("service is sending data.")
        if recievedDataOnce:
            sleep(10)
            print("still running,",datetime.now(),count) 
            count = (count + 10)
            sendinfo(data=False)
        else:
            sleep(1)