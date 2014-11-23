#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os.path
import urllib
import urllib2
import time
import sys
import BeautifulSoup
import re

class Weather():
  def __init__(self, day = '  ', date = '  ', weather = '    ', maxdegree = '  ', mindegree = '  '):
    self.day = str(day)
    self.date = str(date).strip('日')
    self.weather = str(weather)
    self.maxdegree = str(maxdegree)
    self.mindegree = str(mindegree)
    self.message = self.day + '\t' + self.date + '日\t' + self.weather + (15 - (len(self.weather) / 3)) * ' ' + self.mindegree + '度 ~ ' + self.maxdegree + '度'


class Weathers(list):
    def __init__(self, iterable=[]):
        list.__init__(self, iterable)
        for i in range(6):
            self.append(Weather())

    #get Weather information from internet
    #if there isn't Internet Connect, it will raise error
     #if there is Internet Connect, function will return array of class Weather which get message from internet
    def setWeathersFromInternet(self):

        self.day = []
        #define list to store day message
        self.date = []
        #define list to store date message
        self.weather = []
        #define list to store weather message
        self.maxdegree = []
        #define list to store maxdegree message
        self.mindegree = []
        #define list to store minidegree message
        weathers = []
        #define list to store array of class Weather object

        fd = urllib2.urlopen(self.url, timeout = 10)
        #download the page from url, and set timeout equal 5

        html = fd.read()
        #html which is type of string includes the content of page

        soup = BeautifulSoup.BeautifulSoup(html)
        #build a class called BeatifulSoup, through this class to deal with HTML
        content = soup.find(id = '7d')
        #find the DOM structure whose id equal '7d'
        #print soup.find(id='7d').prettify()
        for daytag in content.findAll('h1'):
          self.day.append(daytag.string)
        #get all tag called 'h1', get the content between tags and add to the list of day

        for datetag in content.findAll('h2'):
          self.date.append(datetag.string)
        #get all tag called 'h2', get the content between tags and add to the list of date

        for weathertag in content.findAll('p', 'wea'):
          self.weather.append(weathertag.string)
        #get all tag called 'p' and di = 'wea', get the content between tags and add to the list of date

        sign = 0
        for degree in content.findAll('span'):
          if degree.string != None:
            if sign == 0:
              t1 = degree.string
              sign = 1
            elif sign == 1:
              t2 = degree.string
              sign = 0
              if int(t1) > int(t2):
                self.maxdegree.append(int(t1))
                self.mindegree.append(int(t2))
              else:
                self.maxdegree.append(int(t2))
                self.mindegree.append(int(t1))
        #get the maxdegree and mindegree and store to array of mindegree and array of maxdegree

        for dayname, datename, weathername, maxdegreename, mindegreename in zip(self.day, self.date, self.weather, self.maxdegree, self.mindegree):
          weathers.append(Weather(dayname, datename, weathername, maxdegreename, mindegreename))
        #put all message store into the array of Weathers consisted by class Weather

        for i, wea in enumerate(weathers[0:6]):
            self[i] = wea

    def setDefaultCity(self):
      if os.path.isfile('data.txt'):
      #judge whether exist the file namely 'data.txt'
        self.city = open('data.txt').readline().strip('\n').strip()
        #if there is a file namely 'data.txt', open the file and read the name of city
      else:
        self.city = 'Hefei'
        #if there is not the file namely 'data.txt', set the variable default as string of 'Hefei'

    def setCity(self, cityname):
      self.city = cityname

    def setURL(self):

      url = 'http://toy1.weather.com.cn/search?cityname=' + urllib.quote(self.city) + '&callback=jQuery182005500786968241289_1411741793130'
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
      response = urllib2.urlopen(request, timeout=10).read()
      #get the content of page as type of string
      #the content include the code of the city you want to search

      ss = re.findall('\"ref\":\"(.*?)\"', response)
      #use re to get all code and store into list of ss

      for item in ss:
        if '~' + self.city + '~' in item:
          code = item.split('~')[0]
          break
      #get the code of the city directly

      self.url = 'http://www.weather.com.cn/weather1d/' + code + '.shtml'

    #update data of the cache file
    #store the name of city into local filename namely 'data.txt'
    def saveWeathers(self):
      file = open('data.txt', 'w')
      file.write(self.city)
      file.close()

if __name__ == '__main__':
    weathers = Weathers()

    weathers.setCity('Hefei')
    weathers.setURL()
    print weathers.url
    weathers.setWeathersFromInternet()

    for wea in weathers:
        print wea.message
