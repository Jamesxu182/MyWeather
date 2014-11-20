#!/usr/bin/python
#-*- coding: utf-8 -*-

from Tkinter import *
import getWeathers
import urllib2
import socket
from SimpleDialog import *

#define the Top extend Frame widget, which includes a Entry widget and a Button widget
class Top(Frame):
  def __init__(self, master=None, content=None, chart=None):
    Frame.__init__(self, master)
    self.createWidget()
    self.content = content
    self.master = master
    self.chart = chart

  def createWidget(self):
    self.cityname = getWeathers.getCity()
    #get city name
    self.e = StringVar()
    self.top = LabelFrame(self, text = 'City Name', padx = 5, pady = 5)
    #create the LabelFrame widget with string 'City Name'
    self.e.set(self.cityname)
    #set the varible of type of StringVar as self.cityname
    self.entry = Entry(self.top, width=29, textvariable=self.e)
    #create the Entry widget
    self.submitbutton = Button(self.top, text = "submit", command=self.submitcity)
    #create the Button widget
    self.submitbutton.bind("<Return>", self.submitcity)
    #bind the Button namely submit with Enter Key in keyboard
    self.entry.pack(side="left")
    self.submitbutton.pack(side="right")
    self.top.pack()
    #place the widgets on frame namely Top

  #define the function namely submit and it is the activity of button namely submit
  def submitcity(self):
    self.lastcityname = self.cityname
    #backup the cityname as lastcityname
    self.cityname = self.entry.get().capitalize()
    #make cityname as a same formate
    try:
      self.url = getWeathers.getURL(self.cityname)
      #get the url of the city
      self.content.weathers = getWeathers.getWeathersFromInternet(self.url)
      #get list of weather
    except UnboundLocalError:
      self.cityname = self.lastcityname
      SimpleDialog(self.master, text = 'The city is not exist!', buttons = ['OK'], default = 0)
    except AttributeError:
      self.cityname = self.lastcityname
      SimpleDialog(self.master, text = 'The city is not exist!', buttons = ['OK'], default = 0)
    for i, wea in enumerate(self.content.weathers[0:6], start=0):
      self.content.labels[i]['text'] = wea.message
      #update the text of labels
    
    self.chart.chart.delete(ALL)
    self.chart.maxdegree = []
    self.chart.mindegree = []
    self.chart.pointmax = []
    self.chart.pointmin = [] 
    self.chart.initChart()
    self.chart.drawLineChart()

#define the Content extend Frame widget, which includes 7 Label widgets
class Content(Frame):
  def __init__(self, master=None):
    Frame.__init__(self, master)
    self.createWidget()
    self.master = master

  def createWidget(self):
    self.labels = [];
    self.today = LabelFrame(self, text = 'Today Weather', padx = 5, pady = 5)
    self.feture = LabelFrame(self, text = 'Feture Weather', padx = 5, pady = 5)
    self.weathers = [getWeathers.Weather()] * 7

    self.labels.append(Label(self.today, text = self.weathers[0].message, justify = 'left', anchor = 'w', fg = 'red'))
    self.labels[0].pack(fill=X)

    for i in range(1, 6):
      self.labels.append(Label(self.feture, text = self.weathers[i].message, justify = 'left', anchor = 'w'))
      self.labels[i].pack(fill=X)

    self.today.pack()
    self.feture.pack()

  def initWeathers(self):
    try:
      self.weathers = getWeathers.getWeathersFromInternet(getWeathers.getURL(getWeathers.getCity()));
      #get list of weather from internet
    except urllib2.URLError:
      SimpleDialog(self.master, text = 'Please check connect!', buttons = ['OK'], default = 0)
    except socket.timeout:
      SimpleDialog(self.master, text = 'Please check connect!', buttons = ['OK'], default = 0)

    for i, wea in enumerate(self.weathers):
      if i >= 6:
        break
      self.labels[i]['text'] = wea.message
    #fill in message in the text of labels

class LineChart(Frame):
  def __init__(self, master=None, content=None):
    Frame.__init__(self, master)
    self.createWidget()
    self.initChart()
    self.content = content
    self.maxdegree = []
    self.mindegree = []
    self.pointmax = []
    self.pointmin = []
 
    
  def createWidget(self):
    self.chartframe = LabelFrame(self, text = 'LineChart', padx = 5, pady = 5);
    self.chart = Canvas(self.chartframe, height=200)
    self.chartframe.pack()
    self.chart.pack()

  def initChart(self):
    self.chart.create_line(20, 20, 20, 180, fill='black')
    #y
    self.chart.create_line(10, 170, 270, 170, fill='black')
    #x
    self.chart.create_line(15, 25, 20, 20, fill='black');
    self.chart.create_line(25, 25, 20, 20, fill='black');
    #y 
    self.chart.create_line(265, 165, 270, 170, fill='black');
    self.chart.create_line(265, 175, 270, 170, fill='black');
    
    for i in range(0, 6):
      self.chart.create_line(40 * i + 40, 170, 40 * i + 40, 165, fill='black')
      
  def drawLineChart(self):
      for wea in self.content.weathers:
        try:
            self.maxdegree.append(int(wea.maxdegree))
            self.mindegree.append(int(wea.mindegree))
        except ValueError:
            SimpleDialog(self.master, text = 'Please check connect!', buttons = ['OK'], default = 0)
      try:        
        self.minmin = sorted(self.mindegree)[0]
        self.minmax = sorted(self.maxdegree)[0]
      except IndexError:
          SimpleDialog(self.master, text = 'Please check connect!', buttons = ['OK'], default = 0)
          
      for i, d in enumerate(self.maxdegree):
          self.pointmax.append((170 - ((d - self.minmax) * 10) - 10, 40 + i * 40))
      
      for i, d in enumerate(self.mindegree):
          self.pointmin.append((170 - ((d - self.minmax) * 10) - 10, 40 + i * 40))
      
      for i, wea in enumerate(self.content.weathers, start=0):
          if i >= 6:
              break
          self.chart.create_text(40 * i + 40, 175, text=wea.date)
      
      for i in range(1, len(self.pointmax) - 1):
          self.chart.create_line(20, self.pointmax[i - 1][0], 25, self.pointmax[i - 1][0], fill='blue')
          #self.chart.create_text(25, self.pointmax[i - 1][0], text=self.content.weathers[i].maxdegree, fill='blue')
          self.chart.create_line(self.pointmax[i - 1][1], self.pointmax[i - 1][0], self.pointmax[i][1], self.pointmax[i][0], fill='blue')      
      try:
          self.chart.create_line(20, self.pointmax[len(self.pointmax) - 2][0], 25, self.pointmax[len(self.pointmax) - 2][0], fill='blue')  
      except:
          SimpleDialog(self.master, text = 'Please check connect!', buttons = ['OK'], default = 0)
          
      #self.chart.create_text(25, self.pointmax[len(self.pointmax) - 1][0], text=self.content.weathers[i].maxdegree, fill='blue');
        
      for i in range(1, len(self.pointmin) - 1):
          self.chart.create_line(15, self.pointmin[i - 1][0], 20, self.pointmin[i - 1][0], fill='red')
          #self.chart.create_text(15, self.pointmin[i - 1][0], text=self.content.weathers[i].mindegree, fill='red'); 
          self.chart.create_line(self.pointmin[i - 1][1], self.pointmin[i - 1][0], self.pointmin[i][1], self.pointmin[i][0], fill='red')
      try:
          self.chart.create_line(15, self.pointmin[len(self.pointmin) - 2][0], 20, self.pointmin[len(self.pointmin) - 2][0], fill='red') 
      except:
          SimpleDialog(self.master, text = 'Please check connect!', buttons = ['OK'], default = 0)
        #self.chart.create_text(15, self.pointmax[len(self.pointmin) - 1][0], text=self.content.weathers[i].mindegree, fill='red');

           
def GUI():
  root = Tk(className="MyWeather")
  #create the window whose title is 'MyWeather'
  root.resizable(False, False)
  #make the window namely root unresizalbe
  content = Content(root)
  #create the Frame Contnet
  chart = LineChart(root, content)
  top = Top(root, content, chart)
  #create the Frame Top
  top.pack()
  content.pack()
  chart.pack()
  #place the frame on Tk
  content.initWeathers()
  chart.drawLineChart()
  #get message and put on labels of frame content
  root.mainloop()
  getWeathers.saveWeathers(top.cityname)
  #store the city name into a file namely 'data.txt'
