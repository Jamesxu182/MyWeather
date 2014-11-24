#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import urllib
import json
import os


class Weather():

  def __init__(self, d = {'day': ' ', 'date': ' ', 'code': '3200', 'high': '32', 'low': '32'}):
     self.day = d['day']
     self.date = d['date']
     self.code = d['code']
     self.weather = Weather.turnCode(self.code)
     self.maxdegree = d['high']
     self.mindegree = d['low']
     self.message = self.day + '\t' + self.date + '\t' + self.weather + (3 - (len(self.weather) / 8)) * '\t' + self.mindegree + 'C~' + self.maxdegree + 'C'

  def getDateMessage(self):
      return self.day + '\t' + self.date

  def getWeatherMessage(self):
      return self.weather + (25 - (len(self.weather))) * ' ' + self.mindegree + 'C~' + self.maxdegree + 'C'

  @classmethod
  def turnCode(cls, code):
      if code == '0':
          return 'tornado'
      elif code == '1':
           return 'weathertropical_storm'
      elif code == '2':
           return 'hurricane'
      elif code == '3':
          return 'severe_thunderstorms'
      elif code == '4':
          return 'thunderstorms'
      elif code == '5':
          return 'mixed_rain_and_snow'
      elif code == '6':
          return 'mixed_rain_and_sleet'
      elif code == '7':
          return 'mixed_snow_and_sleet'
      elif code == '8':
          return 'freezing_drizzle'
      elif code == '9':
          return 'drizzle'
      elif code == '10':
          return 'freezing_rain'
      elif code == '11':
          return 'showers'
      elif code == '12':
          return 'showers'
      elif code == '13':
           return 'snow_flurries'
      elif code == '14':
           return 'light_snow_showers'
      elif code == '15':
           return 'blowing_snow'
      elif code == '16':
           return 'snow'
      elif code == '17':
           return 'hail'
      elif code == '18':
           return 'sleet'
      elif code == '19':
           return 'dust'
      elif code == '20':
           return 'foggy'
      elif code == '21':
           return 'haze'
      elif code == '22':
           return 'smoky'
      elif code == '23':
           return 'blustery'
      elif code == '24':
           return 'windy'
      elif code == '25':
           return 'cold'
      elif code == '26':
           return 'cloudy'
      elif code == '27':
          return 'mostly_cloudy'
      elif code == '28':
          return 'mostly_cloudy'
      elif code == '29':
          return 'partly_cloudy'
      elif code == '30':
           return 'partly_cloudy'
      elif code == '31':
           return 'clear'
      elif code == '32':
          return 'sunny'
      elif code == '33':
           return 'fair'
      elif code == '34':
          return 'fair'
      elif code == '35':
           return 'mixed_rain_and_hail'
      elif code == '36':
          return 'hot'
      elif code == '37':
           return 'isolated_thunderstorms'
      elif code == '38':
           return 'scattered_thunderstorms'
      elif code == '39':
           return 'scattered_thunderstorms'
      elif code == '40':
          return 'scattered_showers'
      elif code == '41':
          return 'heavy_snow'
      elif code == '42':
          return 'scattered_snow_showers'
      elif code == '43':
          return 'heavy_snow'
      elif code == '44':
          return 'partly_cloudy'
      elif code == '45':
          return 'thundershowers'
      elif code == '46':
          return 'snow_showers'
      elif code == '47':
           return 'isolated_thundershowers'
      elif code == '3200':
           return 'not_available'

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
        weathers = []
        #define list to store array of class Weather object

        result = urllib2.urlopen(self.url).read()
        data = json.loads(result)
        weathers = list(data['query']['results']['channel']['item']['forecast'])

        for i, wea in enumerate(weathers):
            self.day.append(wea['day'])
            wea['date'] = wea['date'].split()[0]
            self.date.append(wea['date'])
            self.weather.append(wea['code'])
            wea['high'] = str((int(wea['high']) - 32) * 5 / 9)
            wea['low'] = self[i].mindegree = str((int(wea['low']) - 32) * 5 / 9)
            self.maxdegree.append(int(wea['high']))
            self.mindegree.append(int(wea['low']))
            self[i] = Weather(wea)

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
