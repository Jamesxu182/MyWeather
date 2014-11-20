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
  def __init__(self, day = '  ', date = '  ', weather = '    ', maxdegree = '  ', mindegree = '  '):
    self.day = str(day)
    self.date = str(date).strip('日')
    self.weather = str(weather)
    self.maxdegree = str(maxdegree)
    self.mindegree = str(mindegree)
    self.message = self.day + '\t' + self.date + '日\t' + self.weather + (25 - len(self.weather)) * ' ' + self.mindegree + '度 ~ ' + self.maxdegree + '度'

#get city name from local file, else set city name is default 'Hefei'
def getCity():
  if os.path.isfile('data.txt'):
  #judge whether exist the file namely 'data.txt'
    city = open('data.txt').readline().strip('\n').strip()
    #if there is a file namely 'data.txt', open the file and read the name of city
  else:
    city = 'Hefei'
    #if there is not the file namely 'data.txt', set the variable default as string of 'Hefei'
  return city
  #return the name of city as type of string

#get Weather information from internet
#if there isn't Internet Connect, it will raise error
#if there is Internet Connect, function will return array of class Weather which get message from internet
def getWeathersFromInternet(url):

  day = []
  #define list to store day message
  date = []
  #define list to store date message
  weather = []
  #define list to store weather message
  maxdegree = []
  #define list to store maxdegree message
  mindegree = []
  #define list to store minidegree message
  weathers = []
  #define list to store array of class Weather object

  fd = urllib2.urlopen(url, timeout = 5)
  #download the page from url, and set timeout equal 5

  html = fd.read()
  #html which is type of string includes the content of page

  soup = BeautifulSoup.BeautifulSoup(html)
  #build a class called BeatifulSoup, through this class to deal with HTML
  content = soup.find(id = '7d')
  #find the DOM structure whose id equal '7d'
  #print soup.find(id='7d').prettify()
  for daytag in content.findAll('h1'):
    day.append(daytag.string)
  #get all tag called 'h1', get the content between tags and add to the list of day

  for datetag in content.findAll('h2'):
    date.append(datetag.string)
  #get all tag called 'h2', get the content between tags and add to the list of date

  for weathertag in content.findAll('p', 'wea'):
    weather.append(weathertag.string)
  #get all tag called 'p' and di = 'wea', get the content between tags and add to the list of date

  sign = 0
  for degree in content.findAll('span'):
    if degree.string != None:
      if sign == 0:
        mindegree.append(degree.string)
        sign = 1
      elif sign == 1:
        maxdegree.append(degree.string)
        sign = 0
  #get the maxdegree and mindegree and store to array of mindegree and array of maxdegree

  for dayname, datename, weathername, maxdegreename, mindegreename in zip(day, date, weather, maxdegree, mindegree):
    weathers.append(Weather(dayname, datename, weathername, maxdegreename, mindegreename))
  #put all message store into the array of Weathers consisted by class Weather

  return weathers
  #return the array of class weathers

#encode the cityname and put it into url, and request the recievement.
#analyze the recievement, get the new url, and return the new url.
def getURL(cityname):

  url = 'http://toy1.weather.com.cn/search?cityname=' + urllib.quote(cityname) + '&callback=jQuery182005500786968241289_1411741793130'
  #encode the city name and add into the url

  #define headers message as type dict namely date
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
  #build the request
  response = urllib2.urlopen(request, timeout=5).read()
  #get the content of page as type of string
  #the content include the code of the city you want to search

  ss = re.findall('\"ref\":\"(.*?)\"', response)
  #use re to get all code and store into list of ss

  for item in ss:
    if '~' + cityname + '~' in item:
      code = item.split('~')[0]
      break
  #get the code of the city directly

  return 'http://www.weather.com.cn/weather1d/' + code + '.shtml'
  #return the url of the city you want to search

#update data of the cache file
#store the name of city into local filename namely 'data.txt'
def saveWeathers(city):
  file = open('data.txt', 'w')
  file.write(city)
  file.close()
