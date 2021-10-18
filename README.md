# kivyTimeTable
<hr>
A time table app to notify the user about their class timings 
<br>


## Features
This project incorporates some features i wanted to see in a time table app, Including but not limited to :
- User replaceable time table (read below how to replace), generated with csv file
- Background service which notifies the user what class is currently going on aswell as which class is next

<br>

## Notes on the Service for the app:
The [service.py](https://github.com/nandanhere/kivyTimeTable/blob/main/service.py) is based on [Tshirtman's reference app]() but with a few modifications.
I found it very confusing to change the service name and couldnt find a resource to tell how to do it. To do the same, in [main.py](), line 91

    Replace servicename with the name of your choice, but only the first letter capitalised 

If this does not work, go to the directory 

    /APP_ROOT_FOLDER/.buildozer/android/platform/build-armeabi-v7a/dists/PACKAGE_NAME__armeabi-v7a/AndroidManifest.xml
  

And 