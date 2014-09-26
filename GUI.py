#!/usr/bin/env python
#-*- coding: utf-8 -*-

import getWeathers
import Tkinter

def GUI():

  getWeathers.judgeMessageSource()
  #getWeathers.getWeathersFromInternet()

  app = Tkinter.Tk(screenName = 'Weather', className = 'Weather')
  today = Tkinter.LabelFrame(app, text = 'Today Weather of Hefei')
  feture = Tkinter.LabelFrame(app, text = 'Feture Weatehr of Hefei')

  Tkinter.Label(today, text = getWeathers.weathers[0].message, bg = 'black', fg = 'red', justify = 'left', anchor = 'w').pack(fill=Tkinter.X)
  today.pack(fill=Tkinter.X)

  for wea in getWeathers.weathers[1:]:
    Tkinter.Label(feture, text = wea.message, justify = 'left', anchor = 'w').pack(fill=Tkinter.X)
    feture.pack(fill=Tkinter.X)

    getWeathers.saveWeathers()

  app.mainloop()
