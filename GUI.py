#!/usr/bin/env python
#-*- coding: utf-8 -*-

from Tkinter import *
from Weathers import *
import urllib2
from threading import Thread
import tkMessageBox
from sys import exit

class MyThread(Thread):
    def run(self):
        tkMessageBox.showinfo("Error", "The City Is Not Exist!")

class Top(Frame):
  def __init__(self, master=None, content=None, chart=None, today=None):
    Frame.__init__(self, master)
    self.content = content
    self.master = master
    self.chart = chart
    self.today = today
    self.createWidget()

  def createWidget(self):
    self.e = StringVar()
    self.top = LabelFrame(self, text = 'City Name', padx = 5, pady = 5)
    #create the LabelFrame widget with string 'City Name'
    self.e.set(self.content.weathers.city)
    #set the varible of type of StringVar as self.cityname
    self.entry = Entry(self.top, width=29, textvariable=self.e)
    #create the Entry widget
    self.submitbutton = Button(self.top, text = "submit", command=self.submitcity)
    #create the Button widget
    self.submitbutton.bind("<Return>", self.submitcity)
    #bind the Button namely submit with Enter Key in keyboard
    self.entry.pack(side='left')
    self.submitbutton.pack(side="right")
    self.top.pack(fill=X)
    #place the widgets on frame namely Top

  #define the function namely submit and it is the activity of button namely submit
  def submitcity(self):
    lastcityname = self.content.weathers.city
    #backup the cityname as lastcityname
    cityname = self.entry.get().capitalize()
    #make cityname as a same formate
    if self.content.updateWeathers(cityname) == 1:
      MyThread().start()
      cityname = lastcityname
      self.e.set(lastcityname)
    else:
      self.chart.updateLineChart()
      self.today.updateToday()

class Today(Frame):
  def __init__(self, master=None, content=None):
      Frame.__init__(self, master)
      self.content = content
      self.createWidget()

  def createWidget(self):
      self.today = LabelFrame(self, text='today')
      self.img = PhotoImage(file='Today.gif')
      self.canvas = Canvas(self.today, height=90)
      self.item1 = self.canvas.create_image(150, 50, image=self.img)
      self.item2 = self.canvas.create_text(20, 10, text=self.content.weathers.day[0])
      self.item3 = self.canvas.create_text(80, 10, text=self.content.weathers.date[0])
      self.item4 = self.canvas.create_text(150, 80, text=self.content.weathers[0].mindegree + 'C ~ ' + self.content.weathers[0].maxdegree + 'C')
      self.canvas.pack(fill=X)
      self.today.pack(fill=X)

  def updateToday(self):
      self.img = PhotoImage(file='Today.gif')
      self.canvas.itemconfigure(self.item1, image=self.img)
      self.canvas.itemconfigure(self.item2, text=self.content.weathers.day[0])
      self.canvas.itemconfigure(self.item3, text=self.content.weathers.date[0])
      self.canvas.itemconfigure(self.item4, text=self.content.weathers[0].mindegree + 'C ~ ' + self.content.weathers[0].maxdegree + 'C')

class Content(Frame):
  def __init__(self, master=None):
    Frame.__init__(self, master)
    self.master = master
    self.weathers = Weathers()
    self.weathers.setDefaultCity()
    self.createWidget()
    self.initWeathers()

  def createWidget(self):
    self.labels = [];
    #self.today = LabelFrame(self, text = 'Today Weather', padx = 5, pady = 5)
    self.feture = LabelFrame(self, text = 'Feture Weather', padx = 5, pady = 5)

    #self.label.pack()

    self.labels.append(Label(self, justify = 'left', anchor = 'w', fg = 'red'))
    #self.labels[0].pack(fill=X)

    for i in range(1, 5):
      self.labels.append(Label(self.feture, justify = 'left', anchor = 'w'))
      self.labels[i].pack(fill=X)

    #self.today.pack(fill=X)
    self.feture.pack(fill=X)

  def initWeathers(self):
    try:
      self.weathers.setURL()
      self.weathers.setWeathersFromInternet()
    except urllib2.URLError:
      tkMessageBox.showinfo("Error", "Please check connect!")
      exit(0)

    for i, wea in enumerate(self.weathers, start=0):
      self.labels[i]['text'] = wea.message
      #fill in message in the text of labels

  def updateWeathers(self, cityname):
      self.weathers.setCity(cityname)
      self.weathers.setURL()
      try:

        if self.weathers.setWeathersFromInternet() == 1:
          return 1
      except urllib2.URLError:
        tkMessageBox.showinfo("Error", "Please check connect!")
        exit(0)

      for i, wea in enumerate(self.weathers, start=0):
        self.labels[i]['text'] = wea.message

      self.weathers.saveWeathers()
      return 0

class LineChart(Frame):
  def __init__(self, master=None, content=None):
    Frame.__init__(self, master)
    self.content = content
    self.createWidget()
    self.initChart()
    self.drawLineChart()

  def createWidget(self):
    self.chartframe = LabelFrame(self, text = 'LineChart', padx = 5, pady = 5);
    self.chart = Canvas(self.chartframe, height=200)
    self.chartframe.pack(fill=X)
    self.chart.pack()
    img = PhotoImage(file='./icon/purple_retina.gif')
    self.label = Label(self)
    self.label.configure(image=img)
    self.label.image = img
    self.label.pack(side='right')

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

    for i in range(0, 5):
      self.chart.create_line(40 * i + 60, 170, 40 * i + 60, 165, fill='black')

  def drawLineChart(self):
      self.pointmax = []
      self.pointmin = []
      self.minmin = sorted(self.content.weathers.mindegree)[0]
      self.maxmax = sorted(self.content.weathers.maxdegree)[len(self.content.weathers.maxdegree) - 1]
      self.gap = 150 / (self.maxmax - self.minmin) - 1

      for i, d in enumerate(self.content.weathers.maxdegree[0:6]):
          self.pointmax.append((170 - ((d - self.minmin) * self.gap) - 10, 60 + i * 40))

      for i, d in enumerate(self.content.weathers.mindegree[0:6]):
          self.pointmin.append((170 - ((d - self.minmin) * self.gap) - 10, 60 + i * 40))

      for i, wea in enumerate(self.content.weathers, start=0):
          self.chart.create_text(40 * i + 60, 175, text=wea.date.split()[0])

      for i in range(1, len(self.pointmax)):
          self.chart.create_line(20, self.pointmax[i - 1][0], 25, self.pointmax[i - 1][0], fill='red')
          self.chart.create_text(30, self.pointmax[i - 1][0], text=self.content.weathers[i - 1].maxdegree, fill='red')
          self.chart.create_line(self.pointmax[i - 1][1], self.pointmax[i - 1][0], self.pointmax[i][1], self.pointmax[i][0], fill='red')

      self.chart.create_line(20, self.pointmax[len(self.pointmax) - 1][0], 25, self.pointmax[len(self.pointmax) - 1][0], fill='red')
      self.chart.create_text(30, self.pointmax[len(self.pointmax) - 1][0], text=self.content.weathers[len(self.pointmax) - 1].maxdegree, fill='red');

      for i in range(1, len(self.pointmin)):
          self.chart.create_line(15, self.pointmin[i - 1][0], 20, self.pointmin[i - 1][0], fill='blue')
          self.chart.create_text(10, self.pointmin[i - 1][0], text=self.content.weathers[i - 1].mindegree, fill='blue');
          self.chart.create_line(self.pointmin[i - 1][1], self.pointmin[i - 1][0], self.pointmin[i][1], self.pointmin[i][0], fill='blue')

      self.chart.create_line(15, self.pointmin[len(self.pointmin) - 1][0], 20, self.pointmin[len(self.pointmin) - 1][0], fill='blue')
      self.chart.create_text(10, self.pointmin[len(self.pointmin) - 1][0], text=self.content.weathers[len(self.pointmin) - 1].mindegree, fill='blue');

  def updateLineChart(self):
      self.chart.delete(ALL)
      self.initChart()
      self.drawLineChart()

def GUI():
  root = Tk(className='MyWeather')
  root.resizable(width = False, height = False)

  content = Content(root)
  today = Today(root, content)
  chart = LineChart(root, content)
  top = Top(root, content, chart, today)

  top.pack(fill=X)
  today.pack(fill=X)
  content.pack(fill=X)
  chart.pack(fill=X)

  root.mainloop()
