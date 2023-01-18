#!/usr/bin/env python
# coding: utf-8

# | ![nsdf](https://www.sci.utah.edu/~pascucci/public/NSDF-smaller.PNG)  | [National Science Data Fabric](https://nationalsciencedatafabric.org/) [Jupyter notebook](https://jupyter.org/) <br> created by  [Valerio Pascucci](http://cedmav.com/) and  [Giorgio Scorzelli](https://www.sci.utah.edu/people/scrgiorgio.html)  |  
# |---|:---:|
# 
# #####  [MIT Open sourece license](https://opensource.org/licenses/MIT)
# 
# 
# <font size="1">
# Copyright 2022 COPYRIGHT V. Pascucci NSDF
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# </font>

# In[35]:


import bokeh
from bokeh.plotting import figure, output_file, save
from IPython.display import display, HTML
from influxdb import InfluxDBClient
import numpy as np
import pandas as pd
    
display(HTML("<style>.container { width:100% !important; }</style>"))





# In[36]:


#2D array of 2 number each [bandwith,latency].
osgInfo = [[[10,2.1],[2,3],[2,0.1]],
          [[11,1.2],[2,2],[1,0.2]],
           [[14,0.2],[2,1],[12,0.3]],
           [[13,0.1],[2,0],[8,0.4]]]


# In[37]:


import yaml

from bokeh.layouts import row,column
from bokeh.models.widgets import Div, Button
from bokeh.models import ColumnDataSource, Slider , Dropdown, Select
from bokeh.plotting import figure
from bokeh.themes import Theme
from bokeh.io import show, output_notebook, curdoc
from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature
from bokeh.io import output_file, show
from bokeh.layouts import row
from bokeh.plotting import figure
from bokeh.models import LinearColorMapper, ColorBar

from influxdb import InfluxDBClient
import numpy as np
import pandas as pd

from IPython.display import clear_output
from IPython.display import IFrame
import numpy as np
import scipy.stats as stats
import math

import requests
from requests.exceptions import HTTPError
import traceback
from bokeh.io import export_png
from bokeh.plotting import figure


# In[38]:


def three_d_array(value, *dim):
    """
    Create 3D-array
    :param dim: a tuple of dimensions - (x, y, z)
    :param value: value with which 3D-array is to be filled
    :return: 3D-array
    """

    return [[[value for _ in range(dim[2])] for _ in range(dim[1])] for _ in range(dim[0])]


# In[39]:


def in_notebook():
    from IPython import get_ipython
    if get_ipython():
        return True
    else:
        return False    


# In[48]:


client = InfluxDBClient(host='graph.t2.ucsd.edu', port=8086, username='cachemon', password='')
client.switch_database('cachemon_db')
timet = "80m"


x_axis_labels = ['stashcache.t2.ucsd.edu','osg.newy32aoa.nrp.internet2.edu','fiona-r-uva.vlan7.uvalight.net','stashcache.gravity.cf.ac.uk','osg-chicago-stashcache.nrp.internet2.edu','osg.kans.nrp.internet2.edu','osg-houston-stashcache.nrp.internet2.edu','osg.kans.nrp.internet2.edu','dtn2-daejeon.kreonet.net','osg.newy32aoa.nrp.internet2.edu','osg-sunnyvale-stashcache.nrp.internet2.edu','stashcache.t2.ucsd.edu'] # cache

#x_axis_labels = ['stashcache.t2.ucsd.edu'] # cache

y_axis_labels = ['root://stash.osgconnect.net:1094','root://sc-origin2000.chtc.wisc.edu:1094','root://gandalf.phys.uconn.edu:1094',
                 'root://cn447.storrs.hpc.uconn.edu:1094', 'root://origin.ligo.caltech.edu:1094','root://dtn1902.jlab.org:2094',
                 'root://stash-origin.icecube.wisc.edu:1094','root://stashcache.fnal.gov:1094'] #origin


x_axis_labels = list(set(x_axis_labels))
y_axis_labels = list(set(y_axis_labels))

y_axis_labels.sort()
x_axis_labels.sort()

n = 2

dataOSDG = three_d_array(1, *(len(y_axis_labels), len(x_axis_labels), 2))




for originb in y_axis_labels:
    for cachen in x_axis_labels:
        
        indexcache = x_axis_labels.index(cachen)
        indexorigin = y_axis_labels.index(originb)
        
        try:
                sql = "SELECT * FROM heatmappar where origin='" + originb + "|" + cachen + "' order by time desc limit 1"
                print(sql)
                results = client.query(sql)
                points = results.get_points() 
                
                for point in points:
                    measure=point['value']
                    if(measure == 0):
                        measure = 1;
                    dataOSDG[indexorigin][indexcache][0] = (measure/10000000)
              
                    
        except Exception as e:
                print(e)
                traceback.print_exc()
                data[indexorigin][indexcache][0] = -100           
    
        try:                      
                results = client.query("SELECT * FROM heatmaplt where origin='" + originb + "|" + cachen + "' order by time desc limit 1")
                points = results.get_points() 
                for point in points:
                    measure=point['value']
                    if(measure == 0):
                        measure = 1;
                    dataOSDG[indexorigin][indexcache][1] = measure
        except Exception as e:
                print(e)
                traceback.print_exc()
                data[indexorigin][indexcache][1] = -100                           

            

button_length = 0
for i in y_axis_labels:
    l = len (i)
    if l > button_length:
        button_length = l
button_length = button_length - 12
button_length *=7
print("<<<<",button_length)
print(dataOSDG)

        
width=110
height=60

osgInfo = dataOSDG

def bkapp(doc,osgInfo=osgInfo,y_axis_labels=y_axis_labels,button_length=button_length,x_axis_labels=x_axis_labels):
    class Current_values:
        osgInfo  = osgInfo

    title  = Button(label="Open Science Data Federation - Avg of 10 transfers - MegaBytes per second ", button_type='primary', height = 50)
    import datetime

    current_time = datetime.datetime.now()
    title2 = Button(label="PRP " + str(current_time), button_type='primary', height = 30)
    def handler(event):
        print(dir(event))
        print(event.event_name)
        print (osgInfo)

    title.on_click(handler)
    print(">>>>>>>>>>>>>>>>>",len(osgInfo),len(y_axis_labels))
    # calculate the ranges of the OSG values
    minb = max(osgInfo[0][0][0],0)
    minl = osgInfo[0][0][1]
    maxb = 0
    maxl = 0
    for my_row in osgInfo:
        for b,l in my_row:
            #print (b,l)
            minb = min(minb,max(b,0))
            minl = min(minl,l)
            maxb = max(maxb,b)
            maxl = max(maxl,l)
            
            #minb = 1
            #minl = 1
            #maxb = 997
            #maxl = 10
    print(minb,maxb,minl,maxl)

    color = LinearColorMapper(palette = "Greens256",low = 0, high = maxb)
    from bokeh.palettes import Greens256

    Greens256 = list(Greens256)
    Greens256.reverse()
    color = LinearColorMapper(palette = Greens256,low = 0, high = maxb)

    mu = 0
    variance = 1
    sigma = math.sqrt(variance)
    xCoords = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    yCoords = stats.norm.pdf(xCoords, mu, sigma)
    yamx = max(yCoords)
    yCoords = yCoords/yamx
    
    def osgPlotYaxis(osgInfo=osgInfo, showYaxis = False, width=270, height=250, 
        info=[0.0001,1]):        
        s1 = figure(width=width, height=height, 
                    background_fill_color=None,
                    toolbar_location=None,
                    min_border=0,
                    y_range = (-0.1,maxl))
        s1.xaxis.visible = False
        s1.yaxis.visible = False
        s1.xgrid[0].grid_line_color=None
        s1.ygrid[0].grid_line_color=None
        if showYaxis:
            s1.yaxis.visible = True            
            s1.yaxis.axis_label = "Latency s"
        #s1.circle(x, y0, size=12, color="#53777a", alpha=0.8)
        s1.circle([0], [0], size=0, color=None)
        return s1

    def osgPlot(osgInfo=osgInfo, showYaxis = False, width=250, height=250, 
               info=[0.0001,1]):        
        # create one plot
        x = list(range(11))
        y0 = x
        y1 = [10 - i for i in x]
        y2 = [abs(i - 5) for i in x]
        if info[0] == -1:
            s1 = figure(width=width, height=height, 
                        background_fill_color="red",
                        toolbar_location=None,
                        min_border=0,
                        y_range = (-0.1,maxl))
        else:
            col_index = int((info[0]/maxb)*(len(color.palette)-1))
            s1 = figure(width=width, height=height, 
                        background_fill_color=color.palette[col_index],
                        toolbar_location=None,
                        min_border=0,
                        y_range = (0,maxl))
        s1.xaxis.visible = False
        s1.yaxis.visible = False
        s1.xgrid[0].grid_line_color=None
        s1.ygrid[0].grid_line_color=None
        s1.line(xCoords, yCoords*info[1], line_width=2,
                #color="#53777a", 
                color="orange")
        return s1

    def osgPlotsRow(osgInfo=osgInfo,osgRow = osgInfo[0],origin_name = "root://stash.osgconnect.net:1094"):       
        x = list(range(11))
        y0 = x
        y1 = [10 - i for i in x]
        y2 = [abs(i - 5) for i in x]

        # create a row of  plots
        plots = [Button(label=origin_name, button_type='default', height = 60,width=button_length),
                 osgPlotYaxis(width=60, height=height,showYaxis = True,info=osgRow[0])]
        for info in osgRow:
            plots.append(osgPlot(width=width, height=height,info=info))
        return(row(plots))        

    def osgPlots(osgInfo=osgInfo,y_axis_labels=y_axis_labels):       
        cb_width = 120
        #color = LinearColorMapper(palette = "Cividis256",low = 0, high = maxb)
        all_plots1 = column([osgPlotsRow(),osgPlotsRow(),osgPlotsRow(),osgPlotsRow()])
        myPlots = []
#         for myrow in osgInfo:
#              myPlots.append(osgPlotsRow(osgRow= myrow))
        for i in range(len(osgInfo)):
             #myPlots.append(osgPlotsRow(osgRow= osgInfo[i]))
             myPlots.append(osgPlotsRow(osgRow= osgInfo[i],origin_name =(y_axis_labels[i])[7:-5]))

        names = [Button(label=" ", button_type='default', height = 30,width=220)]
        for i in x_axis_labels:
            names.append(Button(label=i, button_type='default', #height = 30,
                                width=50))
        
        
        import numpy as np

        from bokeh.io import curdoc, show
        from bokeh.models import ColumnDataSource, Grid, LinearAxis, Plot, Text, Circle

        plot = Plot(
            title=None, width=800, height=300,
            min_border=0, toolbar_location=None)
        
        import numpy as np

        from bokeh.io import curdoc, show
        from bokeh.models import ColumnDataSource, Grid, LinearAxis, Plot, Text

        N = 9
        x = np.linspace(-2, 2, N)
        y = x**2
        a = "abcdefghijklmnopqrstuvwxyz"
        text = [a[i*3:i*3+3] for i in range(N)]
        x = [100, 200]
        y = [100, 100]
        text = ["aaa","bbb"]
        
        xVal = 0
        x =[]
        y = []
        text = []
        for  i in x_axis_labels:
            x.append(xVal)
            xVal += 72
            y.append(0.99)
            text.append(i)
        source = ColumnDataSource(dict(x=x, y=y, text=text))
        print(source)
        labelsHeight = 350

        plot = figure(width=1000, height=labelsHeight,min_border=0, toolbar_location=None,
                     y_range = (0,1))

        plot.xaxis.visible = False
        plot.yaxis.visible = False
        plot.xgrid[0].grid_line_color=None
        plot.ygrid[0].grid_line_color=None
    
    
        glyph = Text(x="x", y="y", text="text", angle=3.14/2, text_color="#96deb3")
        glyph = Text(x="x", y="y", text="text", angle=-3.14/2, text_color="#000000")
        plot.add_glyph(source, glyph)
  
        myPlots.append(row(Button(label=" ", button_type='default', height = labelsHeight,width=250),plot))        
        
        
        print(myPlots)
        all_plots = column(myPlots)
        
        cb = ColorBar(color_mapper = color, location = (5,6))

        d = [[0,0],
             [0.1,0.1],
             [0.5,0.5],
             [1,1]]
        s1 = figure(width=100, height=len(osgInfo)*height, 
                    x_range = (0,1),
                    y_range = (0,maxb),
                   toolbar_location=None,
                   title="Network throughput Mega bytes per seconds", title_location="right")
        s1.circle([0], [0], size=0, color=None)
        s1.title.align="center"
        s1.xgrid[0].grid_line_color=None
        s1.ygrid[0].grid_line_color=None
        #s1.ygrid[0].grid_line_alpha=1
        s1.axis.visible = False
        s1.outline_line_color = None
        print (cb.width)
        s1.add_layout(cb, 'left')
        #export_png(all_plots, s1]), filename="plot.png")
        print("saving")
        return row([all_plots, s1])

    doc.add_root(column(title,osgPlots(),title2))
    export_png(doc, filename="plot.png")
    

ShowWebpage = True

if in_notebook():
    ShowWebpage = False

if ShowWebpage:
    pass
else:
    pass
output_notebook()


if ShowWebpage:
    bkapp(curdoc())
else:
    show(bkapp)
