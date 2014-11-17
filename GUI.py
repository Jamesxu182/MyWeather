#!/usr/bin/python
#-*- coding: utf-8 -*-

from Tkinter import *
import getWeathers
import urllib2
import socket
from SimpleDialog import *

class Top(Frame):

  def __init__(self, master=None, content=None):
    Frame.__init__(self, master)
    self.createWidget()
    self.content = content
    self.master = master

  def createWidget(self):
    self.cityname = getWeathers.getCity()
    self.e = StringVar()
    self.top = LabelFrame(self, text = 'City Name', padx = 5, pady = 5)
    self.e.set(self.cityname)
    self.entry = Entry(self.top, width=29, textvariable=self.e)
    self.submit = Button(self.top, text = "submit", command=self.submit)
    #self.submit.bind("<Enter>", self.submit)
    self.entry.pack(side="left")
    self.submit.pack(side="right")
    self.top.pack()

  def submit(self):
    self.lastcityname = self.cityname
    self.cityname = self.entry.get().capitalize()
    try:
      self.url = getWeathers.getURL(self.cityname)
    except UnboundLocalError:
        SimpleDialog(self.master, text = 'The city is not exist!', buttons = ['OK'], default = 0)
        self.cityname = self.lastcityname
    self.weathers = getWeathers.getWeathersFromInternet(getWeathers.getURL(self.cityname))

    for i, wea in enumerate(self.weathers[0:7], start=0):
      self.content.labels[i]['text'] = wea.message

class Content(Frame):
  def __init__(self, master=None):
    Frame.__init__(self, master)
    self.createWidget()

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

  def initWeathers(self, master):
    try:
      self.weathers = getWeathers.getWeathersFromInternet(getWeathers.getURL(getWeathers.getCity()));
    except urllib2.URLError:
      SimpleDialog(master, text = 'Please check connect!', buttons = ['OK'], default = 0)
    except socket.timeout:
      SimpleDialog(master, text = 'Please check connect!', buttons = ['OK'], default = 0)

    for i, wea in enumerate(self.weathers):
      self.labels[i]['text'] = wea.message

def GUI():
  root = Tk(className="MyWeather")
  root.resizable(False, False)
  content = Content(root)
  top = Top(root, content)
  top.pack()
  content.pack()
  content.initWeathers(root)
  root.mainloop()
  getWeathers.saveWeathers(top.cityname)
