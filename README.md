# kivyTimeTable
<hr>
A time table app to notify the user about their class timings 
<br>


## Features
This project incorporates some features i wanted to see in a time table app, Including but not limited to :
- User replaceable time table (read below how to replace), generated with csv file
- Background service which notifies the user what class is currently going on aswell as which class is next

<br>


## How to use your own time table:
The app supports usage of Custom time tables. On the first run, you must allow permission to access downloads folder. after which a csv file with the name timeTable.csv will appear in the downloads folder. Note that the code only recognises tables similar to the sample one, and the row x column value must be same. The code is pretty straightforward so do feel free to build your own version with [the colab link provided](https://gist.github.com/nandanhere/5ba4d76cad282a0c0b64a1ec1b8530e1)

        
## Notes on the Service for the app:
### 1 : How to properly name the service
The [service.py](https://github.com/nandanhere/kivyTimeTable/blob/main/service.py) is based on [Tshirtman's reference app](https://github.com/tshirtman/kivy_service_osc) but with a few modifications.
I found it very confusing to change the service name and couldnt find a resource to tell how to do it. To do the same, in [main.py](https://github.com/nandanhere/kivyTimeTable/blob/main/main.py), line 91

    Replace servicename with the name of your choice, but only the first letter capitalised 

If this does not work, go to the directory 

    /APP_ROOT_FOLDER/.buildozer/android/platform/build-armeabi-v7a/dists/PACKAGE_NAME__armeabi-v7a/AndroidManifest.xml
  
and find the name of the service in the manifest. In the case of this project, it is 

        <service android:name="org.kivy.timetable.ServiceTimetablepong"
                 android:process=":service_timeTablePong" />
### 2 : Giving Services permissions
In this app, the background service handles the data and notification providing. Since i also wanted to implement a custom table, file access/permissions was neccesary. Note that You cant directly modify the AndroidManifest.xml file since buildozer will write on top of it. instead, you must go to the 
    /content/.buildozer/android/platform/python-for-android/pythonforandroid/bootstraps/sdl2/build/templates/AndroidManifest.tmpl.xml
folder, where the template file which buildozer uses is present.
-   either replace this file with the one provided in the repo
-   or you can add your own permissions at the \<services> part of the file
Rebuild after this and you will get permissions for the service. note that user must grant permissions for this and you have to call the appropriate function to ask for permissions in the ui part of the code.(see [main.py](https://github.com/nandanhere/kivyTimeTable/blob/main/main.py)])
### 3 : Enabling the service as a foreground service:
If the app service is not kept in foreground, android will kill the app as soon as we switch apps or lock the device. In this case i followed the instructions of [this stackoverflow question](https://stackoverflow.com/questions/64473316/foreground-service-in-android-using-kivy). The file Service.tmpl.java must be replaced in 

     .buildozer/android/platform/build-armeabi-v7a/dists/timetable__armeabi-v7a/templates/Service.tmpl.java 
doing so will enable the app. note that this is buggy for kivytimetable since if you close the app, the service acts weird.
## Notes on the Expandable notifications for the app:
The [service.py](https://github.com/nandanhere/kivyTimeTable/blob/main/service.py) periodically sends a notification to the user , with the format 

    You have X class from t1 to t2. Next you have Y from t2 onwards.

Sometimes the message is too long to read. with standard plyer notification this notification is not expandable. So to fix this issu, use the [replaceNotification.py](https://github.com/nandanhere/kivyTimeTable/blob/main/replaceNotification.py) file provided in the repo, and do the following Go to the 

    /content/.buildozer/android/platform/build-armeabi-v7a/dists/(PACKAGE_NAME)__armeabi-v7a/_python_bundle/_python_bundle/site-packages/plyer/platforms/android/notification.py
File and replace its contents with the file provided. Rebuild to get the required result

To See the adb runtime log use the command 

     adb logcat -s timeTablePong:V python:V
