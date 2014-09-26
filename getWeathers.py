#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os.path
import urllib2
import time
import sys
import BeautifulSoup

weathers = []

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
def getWeathersFromInternet():

  day = []
  date = []
  weather = []
  maxdegree = []
  mindegree = []

  url = 'http://www.weather.com.cn/weather1d/101220101.shtml'
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

#get Weather message from cache file
def getWeathersFromFile():

  file = open('data.txt')

  for i in range(6):
    day = file.readline().strip('\n').strip()
    date = file.readline().strip('\n').strip()
    weather = file.readline().strip('\n').strip()
    maxdegree = file.readline().strip('\n').strip()
    mindegree = file.readline().strip('\n').strip()
    weathers.append(Weather(day, date, weather, maxdegree, mindegree))

  return weathers
  
#judge the weather from internet or cache file
def judgeMessageSource():

    nowday = time.localtime().tm_mday

    if os.path.isfile('data.txt'):
      weathers = getWeathersFromFile()

      if int(weathers[0].date) != nowday:
        weathers = []
        weahters = getWeathersFromInternet()

    else:
      weathers = getWeathersFromInternet()

#update data of the cache file
def saveWeathers():

  file = open('data.txt', 'w')
  for wea in weathers:
    file.write(wea.day + '\n')
    file.write(wea.date + '\n')
    file.write(wea.weather + '\n')
    file.write(wea.maxdegree + '\n')
    file.write(wea.mindegree + '\n')
