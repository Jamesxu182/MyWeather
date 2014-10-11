#!/usr/bin/python
#-*- coding : utf-8 -*-

from Tkinter import *
import getWeathers


class Top(Frame):

  def __init__(self, master=None, content=None):
    Frame.__init__(self, master)
    self.createWidget()
    self.content = content

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
    self.cityname = self.entry.get().capitalize()
    self.url = getWeathers.getURL(self.cityname)
    self.weathers = getWeathers.getWeathersFromInternet(getWeathers.getURL(self.cityname))

    for i, wea in enumerate(self.weathers[0:7], start=0):
      self.content.labels[i]['text'] = wea.message

class Content(Frame):
  def __init__(self, master=None):
    Frame.__init__(self, master)
    self.createWidget()

  def createWidget(self):
    self.url = getWeathers.getURL(getWeathers.getCity())
    self.weathers = getWeathers.getWeathersFromInternet(self.url)
    self.today = LabelFrame(self, text = 'Today Weather', padx = 5, pady = 5)
    self.feture = LabelFrame(self, text = 'Feture Weather', padx = 5, pady = 5)

    self.labels = []
    self.labels.append(Label(self.today, text = self.weathers[0].message, justify = 'left', anchor = 'w', fg = 'red'))
    self.labels[0].pack(fill=X)

    for i, wea in enumerate(self.weathers[1:7], start = 1):
      self.labels.append(Label(self.feture, text = self.weathers[i].message, justify = 'left', anchor = 'w'))
      self.labels[i].pack(fill=X)

    self.today.pack()
    self.feture.pack()

def GUI():
  root = Tk(className="MyWeather")
  root.resizable(False, False)
  content = Content(root)
  top = Top(root, content)
  top.pack()
  content.pack()
  root.mainloop()
  getWeathers.saveWeathers(top.cityname)
