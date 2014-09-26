#!/usr/bin/env python
#-*- coding: utf-8 -*-

import getWeathers
import Tkinter

def GUI():

  getWeathers.judgeMessageSource()
  #getWeathers.getWeathersFromInternet()

  app = Tkinter.Tk(screenName = 'Weather', className = 'Weather')
  top = Tkinter.LabelFrame(app, text = 'Please type the city you are living in', padx = 5, pady = 5)
  today = Tkinter.LabelFrame(app, text = 'Today Weather of Hefei', padx = 5, pady = 5)
  feture = Tkinter.LabelFrame(app, text = 'Feture Weatehr of Hefei', padx = 5, pady = 5)

  entry = Tkinter.Entry(top, width = 30)
  button = Tkinter.Button(top, text='Submit')
  entry.grid(row = 0, column = 0)
  button.grid(row = 0, column = 1)
  top.pack(fill=Tkinter.X)

  Tkinter.Label(today, text = getWeathers.weathers[0].message, bg = 'black', fg = 'red', justify = 'left', anchor = 'w').pack(fill=Tkinter.X)
  today.pack(fill=Tkinter.X)

  for wea in getWeathers.weathers[1:]:
    Tkinter.Label(feture, text = wea.message, justify = 'left', anchor = 'w').pack(fill=Tkinter.X)
    feture.pack(fill=Tkinter.X)

    getWeathers.saveWeathers()

  app.mainloop()
