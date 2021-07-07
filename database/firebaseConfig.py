import pyrebase
import os


firebaseConfig = {
  'apiKey': os.environ['FB_APIKEY'],          #AIzaSyDH5k2kKDRA1hDs-nO4cjpJt9mPQT57qGI
  'authDomain': os.environ['FB_AUTHDOMAIN'],  #glance-4685b.firebaseapp.com
  'databaseURL': os.environ['FB_DBURL'],      #https://glance-4685b-default-rtdb.firebaseio.com
  'projectId': os.environ['FB_PID'],          #glance-4685b
  'storageBucket': os.environ['FB_STORAGEBUCKET'],  #glance-4685b.appspot.com
  'messagingSenderId': os.environ['FB_MSGSID'],   #890425994643
  'appId': os.environ['FB_APPID']                 #1:890425994643:web:c11540eab9f1a9339fcc66
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

