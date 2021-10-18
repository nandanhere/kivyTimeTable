import ast,time
from datetime import datetime
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from jnius import autoclass
import platform
# from kivymd.uix.button import MDFlatButton
from oscpy.client import OSCClient
from oscpy.server import OSCThreadServer
from kivy.utils import platform
DEBUG = False

 
class WindowManager(ScreenManager):
        pass
class HomeScreen(Screen):
    pass
class LabelWithBorder(Label):
    pass
Builder.load_string("""
#:import ScrollView kivy.uix.scrollview

WindowManager: 
    HomeScreen

<HomeScreen>:
    ScrollView:
        do_scroll_x:True
        do_scroll_y:True
        id:sv
        GridLayout:
            size_hint_y: None
            size_hint_x: None
            height:self.minimum_height
            width:self.minimum_width
            id:gv
            rows:11
            cols:9
            row_default_height:100
            col_default_width: 300
            col_force_default:True
            row_force_default:True 
            spacing:"20dp"
            padding:"20dp"
            

""")
 
class HomeScreen(Screen):
    def __init__(self,**kw):
        super().__init__(**kw)
        self.table = []
        self.times = []
        self.rawtimes = []
        self.days = {}
        self.message = ""
    def doThing(self,dt,times,days,table):
        self.ids.gv.clear_widgets()
        cdt = datetime.now()
        day = days[cdt.today().weekday()]
        currtime = int("{:02d}{:02d}".format(cdt.hour,cdt.minute))
        for row in table:
                for i in range(len(row)):
                    entry = row[i]
                    color = [0,0,0,0]
                    if day == row[0]:
                        if times[i][0] <= currtime <=  times[i][1]:
                            color = [1,1,0,1]
                        else:
                            color = [0,1,0,1] 
                    self.ids.gv.add_widget(Button(text=entry,background_color=color),)
        self.ids.gv.add_widget(Button(text="Quit"))

class TimeTableApp(App):
    def build(self):
        self.h = HomeScreen(name='home')
        self.table = []
        self.service = None
        self.server = server = OSCThreadServer()
        server.listen(
            address=b'localhost',
            port=3002,
            default=True,
        )
        server.bind(b'/message', self.callback)
        self.client = OSCClient(b'localhost', 3000)
        if platform == 'android':
            SERVICE_NAME = u'{packagename}.Service{servicename}'.format(packagename=u'org.kivy.timetable',servicename=u'Timetablepong')
            service = autoclass(SERVICE_NAME)
            self.mActivity = autoclass(u'org.kivy.android.PythonActivity').mActivity
            argument = ''
            service.start(self.mActivity, argument)
            self.service = service
        while self.table == []:
            if DEBUG : print("ui pinging server for data")
            self.client.send_message(b'/ping', [])
            time.sleep(1)
        return self.h
    def callback(self, message):
        if DEBUG : print("app recieved data")
        message = message.decode("utf-8")
        splitt = message.split(";")
        if splitt[0] == '0':
          self.times = ast.literal_eval(splitt[1])
          self.table = ast.literal_eval(splitt[2])
          self.days = ast.literal_eval(splitt[3])
          if self.times:
            self.h.doThing(0,times=self.times,days=self.days,table=self.table)
        else:
          # ping for data only every 10 mins
          if datetime.now().minute % 10 == 0:
            self.client.send_message(b'/ping', [])
        if DEBUG : print('times is ', self.times,'days is' , self.days)
        
if __name__=='__main__':
    from android.permissions import request_permissions,Permission,check_permission            #type: ignore
    # since service needs these perms we need to ask through ui 
    request_permissions([Permission.WRITE_EXTERNAL_STORAGE,Permission.READ_EXTERNAL_STORAGE])
    TimeTableApp().run()