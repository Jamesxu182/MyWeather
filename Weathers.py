#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import urllib
import HTMLParser
import json
import os

class MyParser(HTMLParser.HTMLParser):
    def handle_starttag(self, tag, attr):
        if tag == 'img':
            #print attr[0][1]
            urllib.urlretrieve(attr[0][1], 'Today.gif')

class Weather():

  def __init__(self, d = {'day': ' ', 'date': '0 0 0', 'code': '3200', 'high': '32', 'low': '32', 'text': ' '}):
     self.day = d['day']
     self.date = d['date']
     self.maxdegree = d['high']
     self.mindegree = d['low']
     self.text = d['text']
     self.message = self.day + '\t' + self.date.split()[0]+ '\t' + self.text + (2 - (len(self.text) / 9)) * '\t' + self.mindegree + 'C~' + self.maxdegree + 'C'

class Weathers(list):
    def __init__(self, iterable=[]):
        list.__init__(self, iterable)
        for i in range(5):
            self.append(Weather())

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
        self.text = []
        weathers = []
        #define list to store array of class Weather object

        result = urllib2.urlopen(self.url).read()
        data = json.loads(result)

        if data['query']['count'] == 0:
            return 1

        html =  dict(data['query']['results']['channel']['item'])['description']

        parser = MyParser()
        parser.feed(html)
        #download the image from internet namely Today.gif

        weathers = list(data['query']['results']['channel']['item']['forecast'])

        for i, wea in enumerate(weathers):
            self.day.append(wea['day'])
            wea['date'] = wea['date']
            self.date.append(wea['date'])
            self.weather.append(wea['code'])
            wea['high'] = str((int(wea['high']) - 32) * 5 / 9)
            wea['low'] = self[i].mindegree = str((int(wea['low']) - 32) * 5 / 9)
            self.maxdegree.append(int(wea['high']))
            self.mindegree.append(int(wea['low']))
            self.text.append(wea['text'])
            self[i] = Weather(wea)

        return 0

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
        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + self.city + "')"
        yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"

        self.url = yql_url

    #update data of the cache file
    #store the name of city into local filename namely 'data.txt'
    def saveWeathers(self):
        file = open('data.txt', 'w')
        file.write(self.city)
        file.close()

if __name__ == '__main__':
    weathers = Weathers()
    weathers.setDefaultCity()
    weathers.setCity('Hefei')
    weathers.setURL()
    weathers.setWeathersFromInternet()

    for wea in weathers:
        print wea.message
