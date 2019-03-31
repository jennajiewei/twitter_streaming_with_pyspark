
# coding: utf-8

# ### Stream tracking

# In[1]:

get_ipython().run_line_magic('store', '-r topic')
print("You want to track twitter of topic : {}".format(topic))


# In[2]:


import requests_oauthlib
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import socket
import json


from credentials import *


class TweetsListener(StreamListener):

  def __init__(self, csocket):
      self.client_socket = csocket

  def on_data(self, data):
      try:
          msg = json.loads( data )
          print( msg['text'].encode('utf-8') )
          self.client_socket.send( msg['text'].encode('utf-8') )
          return True
      except BaseException as e:
          print("Error on_data: %s" % str(e))
      return True

  def on_error(self, status):
      print(status)
      return True

def sendData(c_socket):
  auth = OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_secret)

  twitter_stream = Stream(auth, TweetsListener(c_socket))
  twitter_stream.filter(track=[topic])#filter contains specific content

if __name__ == "__main__":
  s = socket.socket()
  host = "127.0.0.1"
  port = 5550
  s.bind((host, port))

  print("Listening on port: %s" % str(port))

  s.listen(5)
  c, addr = s.accept()

  print( "Received request from: " + str( addr ) )
  print("Please wait 30 seconds")

  sendData( c )

