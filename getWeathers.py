#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os.path
import urllib
import urllib2
import time
import sys
import BeautifulSoup
import re

#define a Weather class, including message about weather
class Weather():
  def __init__(self, day, date, weather, maxdegree, mindegree):
    self.day = str(day)
    self.date = str(date).strip('日')
    self.weather = str(weather)
    self.maxdegree = str(maxdegree)
    self.mindegree = str(mindegree)
    self.message = self.day + '\t' + self.date + '日\t' + self.weather + (25 - len(self.weather)) * ' ' + self.mindegree + '度 ~ ' + self.maxdegree + '度'

#get Weather information from internet
def getCity():
  if os.path.isfile('data.txt'):
    city = open('data.txt').readline().strip('\n').strip()
  else:
    city = 'Shanghai'
  return city

def getWeathersFromInternet(url):

  day = []
  date = []
  weather = []
  maxdegree = []
  mindegree = []
  weathers = []

  try:

    fd = urllib2.urlopen(url, timeout = 5)

  except urllib2.URLError:

    print "请检查网络连接"
    sys.exit(1)

  html = fd.read()

  soup = BeautifulSoup.BeautifulSoup(html)
  content = soup.find(id = '7d')
  #print soup.find(id='7d').prettify()
  for daytag in content.findAll('h1'):
    day.append(daytag.string)

  for datetag in content.findAll('h2'):
    date.append(datetag.string)

  for weathertag in content.findAll('p', 'wea'):
    weather.append(weathertag.string)

  sign = 0
  for degree in content.findAll('span'):
    if degree.string != None:
      if sign == 0:
        mindegree.append(degree.string)
        sign = 1
      elif sign == 1:
        maxdegree.append(degree.string)
        sign = 0

  for dayname, datename, weathername, maxdegreename, mindegreename in zip(day, date, weather, maxdegree, mindegree):
    #print dayname, datename, weathername,  mindegreename, '度 ~', maxdegreename, '度'
    weathers.append(Weather(dayname, datename, weathername, maxdegreename, mindegreename))

  return weathers

def getURL(cityname):

  url = 'http://toy1.weather.com.cn/search?cityname=' + urllib.quote(cityname) + '&callback=jQuery182005500786968241289_1411741793130'

  data = {
    'GET': 'url',
    'Host':	'toy1.weather.com.cn',
    'User-Agent': 	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',
    'Accept':	'*/*',
    'Accept-Language':	'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://www.weather.com.cn/',
    'Connection': 'keep-alive'
    }

  request = urllib2.Request(url, headers = data)
  response = urllib2.urlopen(request).read()
  ss = re.findall('\"ref\":\"(.*?)\"', response)

  for item in ss:
    if '~' + cityname + '~' in item:
      code = item.split('~')[0]
      break

  return 'http://www.weather.com.cn/weather1d/' + code + '.shtml'

#update data of the cache file
def saveWeathers(city):
  file = open('data.txt', 'w')
  file.write(city)
  file.close()
