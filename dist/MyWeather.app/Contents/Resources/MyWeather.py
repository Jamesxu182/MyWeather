#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import BeautifulSoup
import Tkinter
import sys

class Weather():
  def __init__(self, day, date, weather, maxdegree, mindegree):
    self.day = day
    self.date = date
    self.weather = weather
    self.maxdegree = maxdegree
    self.mindegree = mindegree
    self.message = str(self.day) + ' ' + str(self.date) + ' ' + str(self.weather) + ' ' + str(self.mindegree) + '度 ~ ' + str(self.maxdegree) + '度'

def getWeathers():

  day = []
  date = []
  weather = []
  maxdegree = []
  mindegree = []
  weathers = []

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
        maxdegree.append(degree.string)
        sign = 1
      elif sign == 1:
        mindegree.append(degree.string)
        sign = 0

  for dayname, datename, weathername, maxdegreename, mindegreename in zip(day, date, weather, maxdegree, mindegree):
    #print dayname, datename, weathername,  mindegreename, '度 ~', maxdegreename, '度'
    weathers.append(Weather(dayname, datename, weathername, maxdegreename, mindegreename))

  return weathers

if __name__ == '__main__':

  top = Tkinter.Tk(screenName = 'Weather', className = 'Weather')

  weathers = getWeathers()

  Tkinter.Label(top, text = weathers[0].message, bg = 'black', fg = 'red', justify = 'left').pack()

  for wea in weathers[1:]:
    Tkinter.Label(top, text = wea.message, justify = 'left').pack()

  top.mainloop()
