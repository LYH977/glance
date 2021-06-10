import pyrebase
import os


firebaseConfig = {
  'apiKey': os.environ['FB_APIKEY'],
  'authDomain': os.environ['FB_AUTHDOMAIN'],
  'databaseURL': os.environ['FB_DBURL'],
  'projectId': os.environ['FB_PID'],
  'storageBucket': os.environ['FB_STORAGEBUCKET'],
  'messagingSenderId': os.environ['FB_MSGSID'],
  'appId': os.environ['FB_APPID']
}

firebase=pyrebase.initialize_app(firebaseConfig)

#define storage
storage=firebase.storage()

#upload a file
# file='cat.jpg'
# cloud_file_name='images/test.jpg'
# storage.child(cloud_file_name).put(file)

#get url of the file we just uploaded
# print(storage.child(cloud_file_name).get_url(None))

