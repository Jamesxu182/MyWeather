#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getWeathers
from reportlab.graphics.shapes import *
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics import renderPDF

dates = []
maxdegrees = []
mindegrees = []
datas = []
weathers = getWeathers.getWeathersFromInternet()

for wea in weathers:
  dates.append(int(wea.date))
  maxdegrees.append(int(wea.maxdegree))
  mindegrees.append(int(wea.mindegree))

datas = [zip(dates, maxdegrees), zip(dates, mindegrees)]

drawing = Drawing(400, 200)

lp = LinePlot()
lp.x = 50
lp.y = 50
lp.height = 125
lp.width = 300
lp.data = datas
lp.lines[0].strokeColor = colors.blue
lp.lines[1].strokeColor = colors.red

drawing.add(lp)
drawing.add(String(160, 10, 'Weather Chart', fontSize=14, fillColor=colors.black))

renderPDF.drawToFile(drawing, 'MyWeather.pdf', 'MyWeather')

print 'done!'
