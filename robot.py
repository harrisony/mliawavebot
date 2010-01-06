import logging
from waveapi import events
from waveapi import model
from waveapi import robot
import random
import re
import urllib2
from BeautifulSoup import BeautifulSoup
from google.appengine.api import memcache

def OnRobotAdded(properties, context):
  """Invoked when the robot has been added."""
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().GetDocument().SetText("Hi and welcome to MLIA Bot \n\n Usage: type MLIA in a new blip or AWOD for the average word of the day")
def OnBlipSumbitted(properties,context):
    blip = context.GetBlipById(properties['blipId'])
    contents = blip.GetDocument().GetText()
    if contents[:4].upper() == "MLIA":
        r1 = random.randint(1,100) # Page number #FIXME: Should be proper # The first 100 are good
        r2 = random.randint(0,12) # Item number   
        url = "http://mylifeisaverage.com/index.php?page=%i" % r1
        html = urllib2.urlopen(url).read() # I'm really sorry MLIA crew but you guys having an API would be totally cooler :)
        soupage = BeautifulSoup(html)
        a = soupage.findAll('div', id=re.compile('xnews*'))
        ab = a[r2].div.string
        blip.GetDocument().SetText(str(ab))
    elif contents[:4].upper() == "AWOD":
        #TODO: find if in memcache cache.
	url = "http://mylifeisaverage.com"
	html = urllib2.urlopen(url).read()
	soupage = BeautifulSoup(html)
	a = soupage.find('div',id='wotd').h1.string.strip()
        blip.GetDocument().SetText(str(a))


if __name__ == '__main__':
  myRobot = robot.Robot('mliawavebot', 
      image_url='http://mliawavebot.appspot.com/static/icon.png',
      version='3',
      profile_url='http://harrisony.com/blog/2009/10/mlia-google-wave/')
  myRobot.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)
  myRobot.RegisterHandler(events.BLIP_SUBMITTED, OnBlipSumbitted)
  myRobot.Run(debug=True)
