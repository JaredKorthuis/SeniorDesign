import wx
import os
import wx.xrc
import wx.richtext as rt
import ConfigParser

from numpy import arange, sin, pi
import matplotlib
matplotlib.use('WX')
from matplotlib.backends.backend_wx import FigureCanvasWx as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx

from matplotlib.figure import Figure
import wx.animate as animate

from jared_algorithm import TableData
from jared_save_data import Saving_File_Data

import wx
import wx.lib.mixins.inspection as WIT

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

##############################
## MAINFRAME OF GUI
##############################

try:
    from wx import glcanvas
    haveGLCanvas = True
except ImportError:
    haveGLCanvas = False

try:
    # The Python OpenGL package can be found at
    # http://PyOpenGL.sourceforge.net/
    from OpenGL.GL import *
    from OpenGL.GLUT import *
    haveOpenGL = True
except ImportError:
    haveOpenGL = False

#----------------------------------------------------------------------

buttonDefs = {
    wx.NewId() : ('CubeCanvas',      'Cube'),
    wx.NewId() : ('ConeCanvas',      'Cone'),
    }

def scale_bitmap(bitmap, width, height):
        image = wx.ImageFromBitmap(bitmap)
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image)
        return result

class PatientPanel(wx.Frame):
    
    instance = None
    init =0
    def __new__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = wx.Frame.__new__(self)
        elif isinstance(self.instance, wx._core._wxPyDeadObject):
            self.instance=wx.Frame.__new__(self)
        return self.instance
    def __init__(self):
        if self.init:
            return
        self.init=1
        wx.Frame.__init__(self,None, title="Blood Pressure and comparisons", size=(550,550))
        

        # Here we create a panel and a notebook on the panel
        self.Patient = wx.Panel(self)

        grid = wx.GridSizer(0,1,0,0)
        boxTop = wx.BoxSizer(wx.VERTICAL)
        boxTop2 = wx.BoxSizer(wx.HORIZONTAL)
        boxMiddle = wx.BoxSizer(wx.VERTICAL)
        boxMiddle2 = wx.BoxSizer(wx.HORIZONTAL)
        boxBottom = wx.BoxSizer(wx.HORIZONTAL)

        #lineChartOn = False
        self.att1Clicked = True
        self.att2Clicked = False

        self.quote = wx.StaticText(self.Patient, label="Patient ")
        boxTop.Add(self.quote, 0, wx.ALIGN_TOP)

        self.quote1 = wx.StaticText(self.Patient, label="Blood Pressure: ")
        boxTop2.Add(self.quote1, 0, wx.ALIGN_TOP)

        self.textBox1 = wx.TextCtrl(self.Patient,-1,"120")
        boxTop2.Add(self.textBox1, 5, wx.EXPAND|wx.ALL)

        self.buttonAtt1 = wx.Button(self.Patient, label="Graph Blood Pressure")
        boxMiddle2.Add(self.buttonAtt1, 5, wx.EXPAND|wx.ALL)
        self.buttonAtt1.Bind(wx.EVT_BUTTON, self.att1Click)

        self.quote2 = wx.StaticText(self.Patient, label="Hours Sitting/Day: ")
        boxTop2.Add(self.quote2, 0, wx.ALIGN_TOP)

        self.buttonAtt2 = wx.Button(self.Patient, label="Graph Hours Sitting/Day")
        boxMiddle2.Add(self.buttonAtt2, 5, wx.EXPAND|wx.ALL)
        self.buttonAtt2.Bind(wx.EVT_BUTTON, self.att2Click)

        self.textBox2 = wx.TextCtrl(self.Patient,-1,"6")
        boxTop2.Add(self.textBox2, 5, wx.EXPAND|wx.ALL)

        self.quote3 = wx.StaticText(self.Patient, label="Histogram/Line Chart (X axis is sample ID; Patient is furthest to the right): ")
        boxMiddle.Add(self.quote3, 0, wx.ALIGN_CENTER)

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        #t = arange(0.0, 3.0, 0.01)
        #s = sin(2 * pi * t)
        self.t = [1,2,3,4,5,6]
        self.s = [2,3,1,6,2]
        #tTemp = str(self.textBox1.GetValue())
        #tTemp2 = int(filter(str.isdigit, tTemp))
        #self.t.append(tTemp2)
        sTemp = str(self.textBox2.GetValue())
        #sTemp = '11'
        sTemp2 = int(filter(str.isdigit, sTemp))
        self.s.append(sTemp2)


        #self.quote4 = wx.StaticText(self.Patient, label="HistogramClick ")
        #boxMiddle2.Add(self.quote4, 0, wx.ALIGN_CENTER)

        self.buttonHistogram = wx.Button(self.Patient, label="Histogram")
        boxMiddle2.Add(self.buttonHistogram, 0, wx.ALIGN_BOTTOM)
        self.buttonHistogram.Bind(wx.EVT_BUTTON, self.histogramClick)

        self.canvas = FigureCanvas(self.Patient, -1, self.figure)
        self.canvas.SetInitialSize(size=wx.Size(500,165))
        #boxMiddle.Add(self.canvas, 5, wx.ALIGN_CENTER)
        #boxMiddle.Add(self.canvas, proportion=0, border=2, flag=wx.ALL | wx.EXPAND)
        #boxMiddle.Add(self.canvas, 5, flag=wx.ALL | wx.EXPAND)
        boxMiddle.Add(self.canvas, 0, wx.ALIGN_BOTTOM)

        #self.quote5 = wx.StaticText(self.Patient, label="LineChartClick ")
        #boxMiddle2.Add(self.quote5, 0, wx.ALIGN_CENTER)

        self.buttonLineChart = wx.Button(self.Patient, label="Line Chart")
        boxMiddle2.Add(self.buttonLineChart, 0, wx.ALIGN_BOTTOM)
        self.buttonLineChart.Bind(wx.EVT_BUTTON, self.lineChartClick)

        self.m_button1 = wx.Button(self.Patient, label="Doctor")
        boxBottom.Add(self.m_button1, 0, wx.ALIGN_BOTTOM)
        self.m_button1.Bind(wx.EVT_BUTTON, self.ViewDoctor)
        self.m_button2 = wx.Button(self.Patient, label="Engineer")
        boxBottom.Add(self.m_button2, 0, wx.ALIGN_BOTTOM)
        self.m_button2.Bind(wx.EVT_BUTTON, self.ViewEngineers)
        self.m_button3 = wx.Button(self.Patient, label="Simulation")
        boxBottom.Add(self.m_button3, 0, wx.ALIGN_BOTTOM)
        self.m_button3.Bind(wx.EVT_BUTTON, self.ViewSimulation)
        self.m_button4 = wx.Button(self.Patient, label="Main")
        boxBottom.Add(self.m_button4, 0, wx.ALIGN_BOTTOM)
        self.m_button4.Bind(wx.EVT_BUTTON, self.ViewBack)
        
        grid.Add(boxTop, 0, wx.ALIGN_TOP)
        grid.Add(boxTop2, 0, wx.ALIGN_TOP|wx.ALIGN_LEFT)
        grid.Add(boxMiddle, 0, wx.ALIGN_CENTER|wx.ALIGN_LEFT)
        grid.Add(boxMiddle2, 0, wx.ALIGN_CENTER|wx.ALIGN_LEFT)
        grid.Add(boxBottom, 0, wx.ALIGN_BOTTOM|wx.ALIGN_LEFT)

        self.Patient.SetSizerAndFit(grid)

        self.Patient.Layout()


    def att1Click(self, event):
        print"has successfully pressed att1"
        self.att1Clicked = True
        self.att2Clicked = False
    def att2Click(self, event):
        print"has successfully pressed att2"
        self.att1Clicked = False
        self.att2Clicked = True
    def ViewBack(self, event):
        print"has successfully gone back to the menu"
        self.Hide()
        front_page = FrontPage()
        front_page.Show()

    def ViewDoctor(self, event):
        print"has successfully entered in the new view Doctor"
        self.Hide()
        DoctorPanel().Show()

    def ViewEngineers(self,event):
        print"has successfully entered in the new view Engineers"
        self.Hide()
        EngineerPanel().Show()
    
    def ViewSimulation(self, event):
        print"has successfully entered in the view Simulation"
        self.Hide()
        SimulationPanel().Show()

    def histogramClick(self, event):
        print"has successfully pressed histogram"
        #self.figure.set_canvas(self.canvas)

        if self.att1Clicked == True:
            self.t = [1,2,3,4,5,6]
            self.s = [120,200,50,90,100]
            sTemp = str(self.textBox1.GetValue())
            sTemp2 = int(filter(str.isdigit, sTemp))
            self.s.append(sTemp2)
            
            self.axes.clear()
            self.axes = self.figure.add_subplot(111)
            self.axes.set_ylabel('B. Pressure')
            self.axes.bar(self.t, self.s)
            self.canvas.draw()
            self.Update()

        if self.att2Clicked == True:
            self.t = [1,2,3,4,5,6]
            self.s = [2,3,1,6,2]
            sTemp = str(self.textBox2.GetValue())
            sTemp2 = int(filter(str.isdigit, sTemp))
            self.s.append(sTemp2)

            self.axes.clear()
            self.axes = self.figure.add_subplot(111)
            self.axes.set_ylabel('H.S./Day')
            self.axes.bar(self.t, self.s)
            self.canvas.draw()
            self.Update()

    def lineChartClick(self, event):
        print"has successfully pressed line chart"
        if self.att1Clicked == True:
            self.t = [1,2,3,4,5,6]
            self.s = [120,200,50,90,100]
            sTemp = str(self.textBox1.GetValue())
            sTemp2 = int(filter(str.isdigit, sTemp))
            self.s.append(sTemp2)
            
            self.axes.clear()
            self.axes = self.figure.add_subplot(111)
            #self.axes.set_xlabel('my xdata')
            #self.axes.set_ylabel('my ydata')
            self.axes.set_ylabel('B. Pressure')
            self.axes.plot(self.t, self.s)
            self.axes.scatter(self.t, self.s)
            self.canvas.draw()
            self.Update()

        if self.att2Clicked == True:
            self.t = [1,2,3,4,5,6]
            self.s = [2,3,1,6,2]
            sTemp = str(self.textBox2.GetValue())
            sTemp2 = int(filter(str.isdigit, sTemp))
            self.s.append(sTemp2)

            self.axes.clear()
            self.axes = self.figure.add_subplot(111)
            self.axes.set_ylabel('H.S./Day')
            self.axes.plot(self.t, self.s)
            self.axes.scatter(self.t, self.s)
            self.canvas.draw()
            self.Update()

class EngineerPanel(wx.Frame):
    instance = None
    init =0
    """"This allows one instance of the frame to appear retaining information during the duration of the GUI"""
    def __new__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = wx.Frame.__new__(self)
        elif isinstance(self.instance, wx._core._wxPyDeadObject):
            self.instance=wx.Frame.__new__(self)
        return self.instance
    def __init__(self):
        if self.init:
            return
        self.init=1
        wx.Frame.__init__(self,None, title="Engineering Panel", size=(550,550))

        self.Engineer = wx.Panel(self)
        
        
        grid = wx.GridSizer(0,1,0,0)
        boxTop = wx.BoxSizer(wx.VERTICAL)
        boxTop2 = wx.BoxSizer(wx.HORIZONTAL)
        boxMiddle = wx.BoxSizer(wx.VERTICAL)
        boxMiddle2 = wx.BoxSizer(wx.HORIZONTAL)
        boxMiddle3 = wx.BoxSizer(wx.VERTICAL)
        boxMiddle4 = wx.BoxSizer(wx.VERTICAL)
        boxMiddle5 = wx.BoxSizer(wx.HORIZONTAL)
        boxBottom = wx.BoxSizer(wx.HORIZONTAL)
        
        if 1:
            c = CubeCanvas(self.Engineer)
            c.SetMinSize((200, 200))
            boxTop2.Add(c, 0, wx.ALIGN_CENTER|wx.ALIGN_TOP|wx.ALL, 15)

        self.tree = wx.TreeCtrl(self.Engineer, -1, size=(150, 450), style=wx.TR_HIDE_ROOT| wx.TR_HAS_BUTTONS| wx.TR_EDIT_LABELS)
        
        root = self.tree.AddRoot('Mechanical Heart')
        wt = self.tree.AppendItem(root, 'Weight')
        thk = self.tree.AppendItem(root, 'Thickness')
        stg = self.tree.AppendItem(root, 'Strength')
        dim = self.tree.AppendItem(root, 'Dimensions')
        blp = self.tree.AppendItem(root, 'Blood Pressure')
        self.tree.AppendItem(wt, '0.0')
        self.tree.AppendItem(thk, '0.0')
        self.tree.AppendItem(stg, '0.0')
        self.tree.AppendItem(dim, '0.0')
        self.tree.AppendItem(blp, '0.0')

        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, id=1)
        boxTop.Add(self.tree, 1, wx.EXPAND)


        self.text1 = wx.StaticText(self.Engineer, -1, label="Age")
        boxMiddle3.Add(self.text1, 5, wx.EXPAND|wx.ALL | wx.ALIGN_BOTTOM)

        self.text1c = wx.TextCtrl(self.Engineer,-1,"")
        boxMiddle3.Add(self.text1c, 5, wx.ALL | wx.ALIGN_BOTTOM)

        self.text2 = wx.StaticText(self.Engineer, -1, label = "Height (cm)")
        boxMiddle3.Add(self.text2, 5, wx.EXPAND|wx.ALL)

        self.text2c = wx.TextCtrl(self.Engineer,-1,"")
        boxMiddle3.Add(self.text2c, 5,wx.EXPAND|wx.ALL)

        self.text3 = wx.StaticText(self.Engineer, -1, label = "Weight (kg)")
        boxMiddle4.Add(self.text3, 5, wx.EXPAND|wx.ALL)

        self.text3c = wx.TextCtrl(self.Engineer,-1,"")
        boxMiddle4.Add(self.text3c, 5,wx.EXPAND|wx.ALL)

        self.text4 = wx.StaticText(self.Engineer, -1, label = "Activity Level")
        boxMiddle4.Add(self.text4, 5, wx.EXPAND|wx.ALL)

        self.text4c = wx.TextCtrl(self.Engineer,-1,"")
        boxMiddle4.Add(self.text4c, 5,wx.EXPAND|wx.ALL)

        self.m_button1 = wx.Button(self.Engineer, label="Update Lifestyle Information")
        boxMiddle5.Add(self.m_button1,wx.ALIGN_BOTTOM|wx.ALL)
        self.m_button1.Bind(wx.EVT_BUTTON, self.UpdateLifeStyleInfo)

        self.m_button1 = wx.Button(self.Engineer, label="Patient")
        boxBottom.Add(self.m_button1,wx.ALIGN_BOTTOM|wx.ALL)
        self.m_button1.Bind(wx.EVT_BUTTON, self.ViewPatient)

        self.m_button2 = wx.Button(self.Engineer, label="Doctor")
        boxBottom.Add(self.m_button2,wx.ALIGN_BOTTOM|wx.ALL)
        self.m_button2.Bind(wx.EVT_BUTTON, self.ViewDoctor)

        self.m_button3 = wx.Button(self.Engineer, label="Simulation")
        boxBottom.Add(self.m_button3,wx.ALIGN_BOTTOM|wx.ALL)
        self.m_button3.Bind(wx.EVT_BUTTON, self.ViewSimulation)

        self.m_button4 = wx.Button(self.Engineer, label="Main")
        boxBottom.Add(self.m_button4,wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT|wx.ALL)
        self.m_button4.Bind(wx.EVT_BUTTON, self.ViewBack)
		

        grid.Add(boxTop, 0, wx.ALIGN_TOP)
        grid.Add(boxTop2, 0, wx.ALIGN_TOP|wx.ALIGN_CENTER)
        grid.Add(boxMiddle, 0, wx.ALIGN_TOP | wx.ALIGN_CENTER_HORIZONTAL)
        grid.Add(boxMiddle2, 0, wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT)
        grid.Add(boxMiddle3, 0, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL)
        grid.Add(boxMiddle4, 0, wx.ALIGN_TOP|wx.ALIGN_CENTER_HORIZONTAL)
        grid.Add(boxMiddle5, 0, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL)
        grid.Add(boxBottom, 0, wx.ALIGN_BOTTOM|wx.ALIGN_LEFT)
        
        self.Engineer.SetSizerAndFit(grid)
        self.Engineer.Layout()
        
    def UpdateLifeStyleInfo(self, event):
        item = self.text1c.GetValue()
        self.text1.SetLabel("Age: " + item)
        item = self.text2c.GetValue()
        self.text2.SetLabel("Height (cm): " + item)
        item = self.text3c.GetValue()
        self.text3.SetLabel("Weight (kg): " + item)
        item = self.text4c.GetValue()
        self.text4.SetLabel("Activity Level: " + item)

    def OnSelChanged(self, event):
        item =  event.GetItem()
        self.display.SetLabel(self.tree.GetItemText(item))
    def ViewBack(self, event):
        print"has successfully gone back to the menu"
        self.Hide()
        front_page = FrontPage()
        front_page.Show()

    def ViewPatient(self, event):
        print"has successfully entered in the new view Simulation"
        self.Hide()
        PatientPanel().Show()

    def ViewDoctor(self, event):
        print"has successfully entered in the new view Doctor"
        self.Hide()
        DoctorPanel().Show()

    def ViewSimulation(self,event):
        print"has successfully entered in the new view Simulation"
        self.Hide()
        SimulationPanel().Show()

class MyCanvasBase(glcanvas.GLCanvas):
    def __init__(self, parent):
        glcanvas.GLCanvas.__init__(self, parent, -1)
        self.init = False
        self.context = glcanvas.GLContext(self)
        
        # initial mouse position
        self.lastx = self.x = 30
        self.lasty = self.y = 30
        self.size = None
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)

    def OnEraseBackground(self, event):
        pass # Do nothing, to avoid flashing on MSW.

    def OnSize(self, event):
        wx.CallAfter(self.DoSetViewport)
        event.Skip()

    def DoSetViewport(self):
        size = self.size = self.GetClientSize()
        self.SetCurrent(self.context)
        glViewport(0, 0, size.width, size.height)
        
    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent(self.context)
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw()

    def OnMouseDown(self, evt):
        self.CaptureMouse()
        self.x, self.y = self.lastx, self.lasty = evt.GetPosition()

    def OnMouseUp(self, evt):
        self.ReleaseMouse()

    def OnMouseMotion(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            self.lastx, self.lasty = self.x, self.y
            self.x, self.y = evt.GetPosition()
            self.Refresh(False)

class CubeCanvas(MyCanvasBase):
    def InitGL(self):
        # set viewing projection
        glMatrixMode(GL_PROJECTION)
        glFrustum(-0.5, 0.5, -0.5, 0.5, 1.0, 3.0)

        # position viewer
        glMatrixMode(GL_MODELVIEW)
        glTranslatef(0.0, 0.0, -2.0)

        # position object
        glRotatef(self.y, 1.0, 0.0, 0.0)
        glRotatef(self.x, 0.0, 1.0, 0.0)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

    def OnDraw(self):
        # clear color and depth buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # draw six faces of a cube
        glBegin(GL_QUADS)
        glNormal3f( 0.0, 0.0, 1.0)
        glVertex3f( 0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5,-0.5, 0.5)
        glVertex3f( 0.5,-0.5, 0.5)

        glNormal3f( 0.0, 0.0,-1.0)
        glVertex3f(-0.5,-0.5,-0.5)
        glVertex3f(-0.5, 0.5,-0.5)
        glVertex3f( 0.5, 0.5,-0.5)
        glVertex3f( 0.5,-0.5,-0.5)

        glNormal3f( 0.0, 1.0, 0.0)
        glVertex3f( 0.5, 0.5, 0.5)
        glVertex3f( 0.5, 0.5,-0.5)
        glVertex3f(-0.5, 0.5,-0.5)
        glVertex3f(-0.5, 0.5, 0.5)

        glNormal3f( 0.0,-1.0, 0.0)
        glVertex3f(-0.5,-0.5,-0.5)
        glVertex3f( 0.5,-0.5,-0.5)
        glVertex3f( 0.5,-0.5, 0.5)
        glVertex3f(-0.5,-0.5, 0.5)

        glNormal3f( 1.0, 0.0, 0.0)
        glVertex3f( 0.5, 0.5, 0.5)
        glVertex3f( 0.5,-0.5, 0.5)
        glVertex3f( 0.5,-0.5,-0.5)
        glVertex3f( 0.5, 0.5,-0.5)

        glNormal3f(-1.0, 0.0, 0.0)
        glVertex3f(-0.5,-0.5,-0.5)
        glVertex3f(-0.5,-0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5,-0.5)
        glEnd()

        if self.size is None:
            self.size = self.GetClientSize()
        w, h = self.size
        w = max(w, 1.0)
        h = max(h, 1.0)
        xScale = 180.0 / w
        yScale = 180.0 / h
        glRotatef((self.y - self.lasty) * yScale, 1.0, 0.0, 0.0);
        glRotatef((self.x - self.lastx) * xScale, 0.0, 1.0, 0.0);

        self.SwapBuffers()


class SimulationPanel(wx.Frame):
    
    instance = None
    init =0
    #locale = wx.Locale(wx.LANGUAGE_ENGLISH)
    """This allows only one instance to happen on this panel"""
    def __new__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = wx.Frame.__new__(self)
        elif isinstance(self.instance, wx._core._wxPyDeadObject):
            self.instance=wx.Frame.__new__(self)
        return self.instance
    def __init__(self):
        self.setLocal()
        if self.init:
            return
        self.init=1
        wx.Frame.__init__(self,None, title="Blood Pressure and comparisons", size=(550,550))

    
        
        #self.Simulation = wx.Panel(self)


        """Store all box sizers for panel layout here"""

        grid = wx.GridSizer(0,1,0,0)

        self.boxTop = wx.BoxSizer(wx.VERTICAL)
        self.boxTop2 = wx.BoxSizer(wx.HORIZONTAL)
        self.boxMiddle = wx.BoxSizer(wx.VERTICAL)
        self.boxMiddle2 = wx.BoxSizer(wx.HORIZONTAL)
        self.boxBottom = wx.BoxSizer(wx.HORIZONTAL)
        self.boxLeft = wx.BoxSizer(wx.VERTICAL)
        

        """Set up static text and buttons onto the panel"""

        self.quote = wx.StaticText(self, label="Simulation ")
        self.boxTop.Add(self.quote, 0, wx.ALIGN_CENTER)

       
        #self.m_buttonVelocity = wx.Button(self, label="Velocity")
        #self.boxTop2.Add(self.m_buttonVelocity, 0, wx.ALIGN_TOP)
        #self.m_buttonVelocity.Bind(wx.EVT_BUTTON, self.VelocityClick)

        
        #self.m_buttonVal2 = wx.Button(self, label="Smallest Diameter")
        #self.boxTop2.Add(self.m_buttonVal2, 0, wx.ALIGN_TOP)
        #self.m_buttonVal2.Bind(wx.EVT_BUTTON, self.BPressureClick)

        self.gifs=["velocity = .4, output pressure.gif","vinitial = 1, output pressure.gif","vinitial =.6, output pressure.gif","vinitial = .4, output deformation.gif","vinitial = 1, output deformation.gif","vinitial = .4, output velocity.gif","vinitial = 1, output velocity.gif","vinitial=.6, output velocity.gif"]
        self.my_combo=wx.ComboBox(self,-1,choices=self.gifs, style=wx.CB_READONLY)
        self.my_combo.Bind(wx.EVT_COMBOBOX,self.OnSelect)

        self.gif_name ='velocity = .4, output pressure.gif'
        self.gif = animate.GIFAnimationCtrl(self,1, self.gif_name,size=(720,500))
               
        self.boxMiddle2.Add(self.gif, 0, wx.EXPAND|wx.ALL)
        self.gif.Play()
        self.png2 = wx.Image(os.getcwd()+"\High_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
       
        self.png2 = scale_bitmap(self.png2, 425, 450)
        self.image2 = wx.StaticBitmap(self, -1, self.png2, (10, 5), (self.png2.GetWidth(), self.png2.GetHeight()))
        
        self.boxMiddle2.Add(self.image2, 0, wx.EXPAND|wx.ALL)

        self.m_button1 = wx.Button(self, label="Doctor")
        self.boxBottom.Add(self.m_button1, 0, wx.ALIGN_BOTTOM)
        self.m_button1.Bind(wx.EVT_BUTTON, self.ViewDoctor)

        self.m_button2 = wx.Button(self, label="Engineer")
        self.boxBottom.Add(self.m_button2, 0, wx.ALIGN_BOTTOM)
        self.m_button2.Bind(wx.EVT_BUTTON, self.ViewEngineers)

        self.m_button3 = wx.Button(self, label="Patient")
        self.boxBottom.Add(self.m_button3, 0, wx.ALIGN_BOTTOM)
        self.m_button3.Bind(wx.EVT_BUTTON, self.ViewPatient)

        self.m_button4 = wx.Button(self, label="Main")
        self.boxBottom.Add(self.m_button4, 0, wx.ALIGN_BOTTOM)
        self.m_button4.Bind(wx.EVT_BUTTON, self.ViewBack)


        self.number_of_gifs =2
        """Adding the buttons and static texts into alignment on panel"""
        self.final_box_h=wx.BoxSizer(wx.HORIZONTAL)
        final_box = wx.BoxSizer(wx.VERTICAL)
        final_box.Add(self.boxTop,0,wx.ALIGN_TOP|wx.ALIGN_CENTER|wx.EXPAND)
        final_box.Add(self.boxTop2,0,wx.ALIGN_TOP|wx.ALIGN_LEFT|wx.EXPAND)
        #final_box.Add(self.my_combo,0,wx.ALIGN_CENTER)
        final_box.Add(self.boxLeft,0,wx.ALIGN_TOP|wx.ALIGN_LEFT|wx.EXPAND)
        #final_box.Add(self.boxMiddle,0,wx.ALIGN_CENTER|wx.ALIGN_LEFT|wx.EXPAND)
        final_box.Add(self.boxMiddle2,0,wx.ALIGN_CENTER|wx.ALIGN_RIGHT|wx.EXPAND)
        final_box.Add(self.boxBottom,0,wx.ALIGN_BOTTOM|wx.ALIGN_LEFT|wx.EXPAND)
        

        self.final_box_h.Add(final_box,0,wx.EXPAND)
        

        self.SetSizerAndFit(self.final_box_h)

        self.Layout()

    def setLocal(self):
        locale = wx.Locale(wx.LANGUAGE_ENGLISH)

    def OnSelect(self,event):
            gif = self.my_combo.GetValue()
            print gif
            self.animateGIF(gif)

    def animateGIF(self,image):
             if self.gif:
                 self.gif.Stop()
                 self.gif.Destroy()
             if self.boxMiddle.GetChildren():
                 self.boxMiddle.Hide(self.number_of_gifs-2)
                 self.boxMiddle.Remove(self.number_of_gifs-2)
                 self.number_of_gifs -=1
             self.number_of_gifs +=1
             
             self.gif = wx.animate.GIFAnimationCtrl(self,-1,image,pos=(0,150))
			 #Change to: self.gif = animate.GIFAnimationCtrl(self,1, self.gif_name,size=(720,500))
             self.gif.GetPlayer()
             self.gif.Play()
             self.boxMiddle.Add(self.gif)

    def ViewBack(self, event):
        print"has successfully gone back to the menu"
        self.Hide()
        front_page = FrontPage()
        front_page.Show()

    def ViewPatient(self, event):
        print"has successfully entered in the new view Simulation"
        self.Hide()
        PatientPanel().Show()

    def ViewDoctor(self, event):
        print"has successfully entered in the new view Doctor"
        self.Hide()
        DoctorPanel().Show()

    def ViewEngineers(self,event):
        print"has successfully entered in the new view Engineers"
        self.Hide()
        EngineerPanel().Show()
    def VelocityClick(self,event):
        print"has successfully pressed Velocity"
        value = int(self.textBox1.GetValue())
        value2 = int(self.textBox2.GetValue())
        value3 = 1.
        if(value2 <= 10.):
            value3 = value + abs(10 - value2)
        if (value3 <= 0):
           value3 = 0.1
        if (value3 < 5.):
            print"Velocity 1"
            #"velocity = .4, output pressure.gif","vinitial = 1, output pressure.gif","vinitial =.6, output pressure.gif","vinitial = .4, output deformation.gif","vinitial = 1, output deformation.gif","vinitial = .4, output velocity.gif","vinitial = 1, output velocity.gif","vinitial=.6, output velocity.gif"
            self.gif_name = "vinitial = 1, output pressure.gif"
            self.gif = animate.GIFAnimationCtrl(self,1, self.gif_name,size=(720,500))
        elif (value3 >= 5.) and (value3 < 6.):
            print"Velocity 2"
            self.png1 = wx.Image(os.getcwd()+"\V2_Low_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.png1 = scale_bitmap(self.png1, 300, 150)
            self.image1.SetBitmap(self.png1)
            self.png2 = wx.Image(os.getcwd()+"\V2_Graph_Low_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.png2 = scale_bitmap(self.png2, 300, 180)
            self.image2.SetBitmap(self.png2)
        elif (value3 >= 6.) and (value3 < 7.):
            print"Velocity 2"
            self.png1 = wx.Image(os.getcwd()+"\V3_Normal_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.png1 = scale_bitmap(self.png1, 300, 150)
            self.image1.SetBitmap(self.png1)
            self.png2 = wx.Image(os.getcwd()+"\V3_Graph_Normal_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.png2 = scale_bitmap(self.png2, 300, 180)
            self.image2.SetBitmap(self.png2)
        elif (value3 >= 7.) and (value3 < 8.):
            print"Velocity 2"
            self.png1 = wx.Image(os.getcwd()+"\V4_Normal_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.png1 = scale_bitmap(self.png1, 300, 150)
            self.image1.SetBitmap(self.png1)
            self.png2 = wx.Image(os.getcwd()+"\V4_Graph_Normal_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.png2 = scale_bitmap(self.png2, 300, 180)
            self.image2.SetBitmap(self.png2)
        elif (value3 >= 8.) and (value3 < 9.):
            print"Velocity 2"
            self.png1 = wx.Image(os.getcwd()+"\V5_Normal_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.png1 = scale_bitmap(self.png1, 300, 150)
            self.image1.SetBitmap(self.png1)
            self.png2 = wx.Image(os.getcwd()+"\V5_Graph_Normal_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.png2 = scale_bitmap(self.png2, 300, 180)
            self.image2.SetBitmap(self.png2)
        elif (value3 >= 9.) and (value3 < 10.):
            print"Velocity 2"
            self.png1 = wx.Image(os.getcwd()+"\V6_High_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.png1 = scale_bitmap(self.png1, 300, 150)
            self.image1.SetBitmap(self.png1)
            self.png2 = wx.Image(os.getcwd()+"\V6_Graph_High_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.png2 = scale_bitmap(self.png2, 300, 180)
            self.image2.SetBitmap(self.png2)
        elif (value3 >= 10.):
            print"Velocity 3"
            self.png1 = wx.Image(os.getcwd()+"\V7_High_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.png1 = scale_bitmap(self.png1, 300, 150)
            self.image1.SetBitmap(self.png1)
            self.png2 = wx.Image(os.getcwd()+"\V7_Graph_High_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.png2 = scale_bitmap(self.png2, 300, 180)
            self.image2.SetBitmap(self.png2)
        self.Update()

    def BPressureClick(self,event):
        print"has successfully pressed Val2"
        value = int(self.textBox1.GetValue())
        value2 = int(self.textBox2.GetValue())
        value3 = 1.
        if(value2 <= 10.):
            value3 = value + abs(10 - value2)
        if (value3 <= 0):
           value3 = 0.1
        if (value3 < 5.):
            print"Velocity 1"
            self.png1 = wx.Image(os.getcwd()+"\B1_Low_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.png1 = scale_bitmap(self.png1, 300, 150)
            self.image1.SetBitmap(self.png1)
            self.png2 = wx.Image(os.getcwd()+"\V1_Graph_Low_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.png2 = scale_bitmap(self.png2, 300, 180)
            self.image2.SetBitmap(self.png2)
        elif (value3 >= 5.) and (value3 < 6.):
            print"Velocity 2"
            self.png1 = wx.Image(os.getcwd()+"\B2_Low_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.png1 = scale_bitmap(self.png1, 300, 150)
            self.image1.SetBitmap(self.png1)
            self.png2 = wx.Image(os.getcwd()+"\V2_Graph_Low_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.png2 = scale_bitmap(self.png2, 300, 180)
            self.image2.SetBitmap(self.png2)
        elif (value3 >= 6.) and (value3 < 7.):
            print"Velocity 2"
            self.png1 = wx.Image(os.getcwd()+"\B3_Normal_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.png1 = scale_bitmap(self.png1, 300, 150)
            self.image1.SetBitmap(self.png1)
            self.png2 = wx.Image(os.getcwd()+"\V3_Graph_Normal_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.png2 = scale_bitmap(self.png2, 300, 180)
            self.image2.SetBitmap(self.png2)
        elif (value3 >= 7.) and (value3 < 8.):
            print"Velocity 2"
            self.png1 = wx.Image(os.getcwd()+"\B4_Normal_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.png1 = scale_bitmap(self.png1, 300, 150)
            self.image1.SetBitmap(self.png1)
            self.png2 = wx.Image(os.getcwd()+"\V4_Graph_Normal_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.png2 = scale_bitmap(self.png2, 300, 180)
            self.image2.SetBitmap(self.png2)
        elif (value3 >= 8.) and (value3 < 9.):
            print"Velocity 2"
            self.png1 = wx.Image(os.getcwd()+"\B5_Normal_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.png1 = scale_bitmap(self.png1, 300, 150)
            self.image1.SetBitmap(self.png1)
            self.png2 = wx.Image(os.getcwd()+"\V5_Graph_Normal_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.png2 = scale_bitmap(self.png2, 300, 180)
            self.image2.SetBitmap(self.png2)
        elif (value3 >= 9.) and (value3 < 10.):
            print"Velocity 2"
            self.png1 = wx.Image(os.getcwd()+"\B6_High_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.png1 = scale_bitmap(self.png1, 300, 150)
            self.image1.SetBitmap(self.png1)
            self.png2 = wx.Image(os.getcwd()+"\V6_Graph_High_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.png2 = scale_bitmap(self.png2, 300, 180)
            self.image2.SetBitmap(self.png2)
        elif (value3 >= 10.):
            print"Velocity 3"
            self.png1 = wx.Image(os.getcwd()+"\B7_High_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.png1 = scale_bitmap(self.png1, 300, 150)
            self.image1.SetBitmap(self.png1)
            self.png2 = wx.Image(os.getcwd()+"\V7_Graph_High_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.png2 = scale_bitmap(self.png2, 300, 180)
            self.image2.SetBitmap(self.png2)
        self.Update()
        




class PageOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        font = wx.Font(10, wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        
        """set up upper bounds for panel layout"""
        Main_box_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.age_box_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sub_horizontal_box_bottom = wx.BoxSizer(wx.HORIZONTAL)
        sub_vertical_box = wx.BoxSizer(wx.VERTICAL)
        sub_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        text2_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        text3_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        text4_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        text5_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        text6_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        text7_vertical = wx.BoxSizer(wx.VERTICAL)
        text8_horizontal = wx.BoxSizer(wx.HORIZONTAL)

        slider_vert = wx.BoxSizer(wx.VERTICAL)
        slider_hor1 = wx.BoxSizer(wx.HORIZONTAL)
        slider_hor2 = wx.BoxSizer(wx.HORIZONTAL)
        slider_final_combine = wx.BoxSizer(wx.VERTICAL)
        total_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        total_vertical = wx.BoxSizer(wx.VERTICAL)
        finals_box_hor = wx.BoxSizer(wx.HORIZONTAL)
        finals_box = wx.BoxSizer(wx.VERTICAL)

        

        
        
        
        self.column1_sizer = wx.BoxSizer(wx.VERTICAL)
        

        """get the frame parent for smooth transition"""

        self.doctor_frame = self.GetParent().GetParent().GetParent()

        """set Sizer for bottom of screen"""

        gSizer1 = wx.BoxSizer(wx.VERTICAL)

        """set bottom of screen buttons and event handling"""
        self.gender_text = wx.StaticText(self,-1,u"Gender")
        text2_horizontal.Add(self.gender_text,wx.ALIGN_CENTER|wx.ALL)
        text2_horizontal.AddSpacer(5)
        self.gender_text.SetFont(font)
        self.cbm = wx.CheckBox(self,-1,label='Male')
        self.cbm.SetValue(True)
        text2_horizontal.Add(self.cbm,wx.ALIGN_CENTER|wx.ALL)
        self.cbm.Bind(wx.EVT_CHECKBOX, self.check_genderm)
        self.cbf = wx.CheckBox(self, -1, label='Female')
        text2_horizontal.Add(self.cbf)
        self.cbf.Bind(wx.EVT_CHECKBOX, self.check_genderf)

        #self.column1_sizer.Add(text2_horizontal,wx.ALL)
        #self.column1_sizer.Add(text3_horizontal)
        races_available = ['African', 'Hispanic', 'Asian', 'Indian', 'Caucasian']

        feet = ['3','4','5','6','7']
        inches = ['0','1','2','3','4','5','6','7','8','9','10','11']
        

        
        self.race_text= wx.StaticText(self,-1,u"Race")
        text3_horizontal.Add(self.race_text)
        self.race_text.SetFont(font)
        
        text3_horizontal.AddSpacer(5)
        self.race = wx.ComboBox(self,value="your race?",choices=races_available)
        text3_horizontal.Add(self.race,wx.ALL)

        #self.column1_sizer.Add(text3_horizontal)

        
        self.HeightText = wx.StaticText(self,-1,u"Height")
        self.HeightText.SetFont(font)
        text4_horizontal.Add(self.HeightText)
        text4_horizontal.AddSpacer(25)
        self.StaticFeet = wx.ComboBox(self, value=u"ft",choices=feet)
        text4_horizontal.Add(self.StaticFeet)
        text4_horizontal.AddSpacer(25)
        self.StaticInch = wx.ComboBox(self, value=u"in", choices=inches)
        text4_horizontal.Add(self.StaticInch)

        
        self.WeightText = wx.StaticText(self,-1, u"Weight")
        self.WeightText.SetFont(font)
        text6_horizontal.Add(self.WeightText)
        text6_horizontal.AddSpacer(5)
        self.WeightVariable= wx.TextCtrl(self, value="lbs")
        text6_horizontal.Add(self.WeightVariable)
        text6_horizontal.AddSpacer(5)

        self.Agetext = wx.StaticText(self,-1,u"Age")
        self.Agetext.SetFont(font)
        self.age_box_sizer.Add(self.Agetext)
        self.age_box_sizer.AddSpacer(15)

        self.AgeVariable = wx.TextCtrl(self,value="years")
        self.age_box_sizer.Add(self.AgeVariable)

        self.HighBloodText = wx.StaticText(self,-1," Systolic Pressure")
        self.HighBloodText.SetFont(font)
        self.hblood = wx.TextCtrl(self,size=(55,20),value="mm hg")
        self.hblood.Bind(wx.EVT_TEXT, self.ChangeSlideHigh)
        
        slider_hor1.Add(self.HighBloodText,wx.ALL)
        
        
        self.HighBlood = wx.Slider(self,5,90,90,180,style=wx.SL_HORIZONTAL| wx.SL_AUTOTICKS | wx.SL_LABELS,size=(180,1))
        self.HighBlood.SetTickFreq(10,50)
        slider_hor1.Add(self.HighBlood)
        """THIS IS WHERE YOU CAN MANIPIULATE THE RIGHT SIDE OF THE PAGE"""
        slider_vert.AddSpacer(50)
        slider_vert.Add(self.hblood)
        slider_vert.Add(slider_hor1)
        slider_vert.AddSpacer(50)

        
        self.lblood = wx.TextCtrl(self, size=(55,20),value="mm hg")
        self.lblood.Bind(wx.EVT_TEXT, self.ChangeSlideLow)
        self.LowBloodText = wx.StaticText(self,-1,"Diastolic Pressure")
        self.LowBloodText.SetFont(font)
        
        slider_hor2.Add(self.LowBloodText)
        self.LowBlood = wx.Slider(self,100,50,50,120,style=wx.SL_HORIZONTAL|wx.SL_AUTOTICKS|wx.SL_LABELS,size=(180,1))
        self.LowBlood.SetTickFreq(10,50)
        slider_hor2.Add(self.LowBlood,wx.ALL)
        
        slider_vert.Add(self.lblood)
        slider_vert.Add(slider_hor2)
        slider_vert.AddSpacer(50)

        
        


        self.FinalResult=wx.StaticBox(self,-1,u"Additional Information")
        self.FinalResult.SetFont(font)
        
        self.finals= wx.StaticBoxSizer(self.FinalResult,wx.VERTICAL)
    
        self.check_heart_attk =wx.CheckBox(self,-1,label="Heart Attack")
        self.check_stroke     =wx.CheckBox(self,-1,label="Stroke")
        self.check_heart_fail =wx.CheckBox(self,-1,label="Heart Failure")

        self.check_kidney     =wx.CheckBox(self,-1,label="Kidney disease")
        self.check_diabetus   =wx.CheckBox(self,-1,label="Diabetes")
        self.check_smoking    =wx.CheckBox(self,-1,label="Smoking")

        self.check_artery     =wx.CheckBox(self,-1,label="Artery disease")
        self.check_vasc       =wx.CheckBox(self,-1,label="Vascular disease")
        self.check_chol       =wx.CheckBox(self,-1,label="High Cholesterol")

        self.check_genes      =wx.CheckBox(self,-1,label="Genetic disease")
        self.life_change      =wx.CheckBox(self,-1,label="Life Change")
        self.drinking         =wx.CheckBox(self,-1,label="Excessive Drinking")
        
        self.zip_code         =wx.TextCtrl(self,-1,value="zip code")
        
       
        check_box_5 = wx.BoxSizer(wx.HORIZONTAL)
        check_box_1 = wx.BoxSizer(wx.HORIZONTAL)
        check_box_2 = wx.BoxSizer(wx.HORIZONTAL)
        check_box_3 = wx.BoxSizer(wx.HORIZONTAL)
        check_box_4 = wx.BoxSizer(wx.HORIZONTAL)
        
        check_box_vertical = wx.BoxSizer(wx.VERTICAL)

        check_box_1.Add(self.check_heart_attk)
        check_box_1.AddSpacer(33)
        check_box_1.Add(self.check_stroke)
        check_box_1.AddSpacer(65)
        check_box_1.Add(self.check_heart_fail)
        
        check_box_2.Add(self.check_kidney)
        check_box_2.AddSpacer(22)
        check_box_2.Add(self.check_diabetus)
        check_box_2.AddSpacer(54)
        check_box_2.Add(self.check_smoking)

        check_box_3.Add(self.check_artery)
        check_box_3.AddSpacer(25)
        check_box_3.Add(self.check_vasc)
        check_box_3.AddSpacer(16)
        check_box_3.Add(self.check_chol)

        check_box_4.Add(self.check_genes)
        check_box_4.AddSpacer(17)
        check_box_4.Add(self.life_change)
        check_box_4.AddSpacer(38)
        check_box_4.Add(self.zip_code)
        check_box_5.Add(self.drinking)

        check_box_vertical.Add(check_box_1)
        check_box_vertical.Add(check_box_2)
        check_box_vertical.Add(check_box_3)
        check_box_vertical.Add(check_box_4)
        check_box_vertical.Add(check_box_5)
        self.finals.Add(check_box_vertical)
        
        
                                           

        finals_box_hor.Add(self.finals)
        finals_box.Add(finals_box_hor)

        slider_vert.Add(finals_box,wx.ALL|wx.ALIGN_CENTER|wx.ALIGN_RIGHT)
        

        slider_final_combine.Add(slider_vert,wx.ALL|wx.ALIGN_CENTER)
        #slider_final_combine.Add(check_box_vertical,wx.ALL)
        
        
        

        self.m_button1 = wx.Button(self, wx.ID_ANY, u"Main Menu", wx.DefaultPosition, wx.DefaultSize)
        sub_horizontal_box_bottom.Add(self.m_button1,0,wx.ALIGN_BOTTOM|wx.RIGHT, 5)
        self.m_button1.Bind(wx.EVT_BUTTON, self.doctor_frame.MainMenu)
        
        self.m_button2 = wx.Button(self, wx.ID_ANY, u"Patients", wx.DefaultPosition, wx.DefaultSize)
        sub_horizontal_box_bottom.Add(self.m_button2,0,wx.ALIGN_BOTTOM|wx.RIGHT,5)
        self.m_button2.Bind(wx.EVT_BUTTON, self.doctor_frame.Patients)

        self.m_button3 = wx.Button(self, wx.ID_ANY, u"Engineers", wx.DefaultPosition, wx.DefaultSize)
        sub_horizontal_box_bottom.Add(self.m_button3,0, wx.ALIGN_BOTTOM|wx.RIGHT,5)
        self.m_button3.Bind(wx.EVT_BUTTON, self.doctor_frame.Engineers)

        self.m_button4 = wx.Button(self, wx.ID_ANY, u"Simulation", wx.DefaultPosition, wx.DefaultSize)
        sub_horizontal_box_bottom.Add(self.m_button4,0,wx.ALIGN_BOTTOM|wx.RIGHT,5)
        self.m_button4.Bind(wx.EVT_BUTTON, self.doctor_frame.Simulation)

                       
        
       
        #self.button5 = wx.Button(self,wx.ID_ANY, u"Bad")
        #text5_horizontal.Add(self.button5)
        #self.button5.Bind(wx.EVT_BUTTON, self.SetHealth)

        #self.button6 = wx.Button(self,wx.ID_ANY,u"Good")
        #text5_horizontal.Add(self.button6)
        #self.button6.Bind(wx.EVT_BUTTON, self.good)

        #self.button7 = wx.Button(self,wx.ID_ANY,u"AVG")
        #text5_horizontal.Add(self.button7)
        #self.button7.Bind(wx.EVT_BUTTON, self.SetHealthAvg)
        
        self.calculate = wx.Button(self,wx.ID_ANY, u"Get blood pressure info")
        
        
        text5_horizontal.Add(self.calculate,3)
        self.calculate.Bind(wx.EVT_BUTTON, self.blood_pressure_solution)
        self.save_data= wx.Button(self,wx.ID_ANY, u"Save Data")
        self.save_data.Bind(wx.EVT_BUTTON,self.SaveData)

        self.load_data=wx.Button(self,wx.ID_ANY, u"Load Data")
        self.load_data.Bind(wx.EVT_BUTTON,self.onOpenFile)
        
        self.column1_sizer.AddSpacer(50)
        self.column1_sizer.Add(text2_horizontal,wx.ALL|wx.ALIGN_CENTER)
        self.column1_sizer.AddSpacer(30)
        self.column1_sizer.Add(self.age_box_sizer,wx.ALL|wx.ALIGN_CENTER)
        self.column1_sizer.AddSpacer(30)
        self.column1_sizer.Add(text6_horizontal,wx.ALL|wx.ALIGN_CENTER)
        self.column1_sizer.AddSpacer(30)
        self.column1_sizer.Add(text4_horizontal,wx.ALL|wx.ALIGN_CENTER)
        self.column1_sizer.AddSpacer(30)
        self.column1_sizer.Add(text3_horizontal,wx.ALL|wx.ALIGN_CENTER)
        self.column1_sizer.AddSpacer(30)
        self.column1_sizer.Add(text5_horizontal,wx.ALL|wx.ALIGN_CENTER)
        self.column1_sizer.Add(self.save_data,wx.ALL|wx.ALIGN_CENTER)
        self.column1_sizer.Add(self.load_data,wx.ALL|wx.ALIGN_CENTER)
        
        vertical_Box_combination = wx.BoxSizer(wx.VERTICAL)
        horizontal_combination = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_combination.Add(self.column1_sizer,wx.ALIGN_BOTTOM|wx.ALL)
        horizontal_combination.Add(slider_final_combine,wx.ALIGN_RIGHT|wx.ALL)
        vertical_Box_combination.Add(horizontal_combination,wx.EXPAND|wx.ALL)
        vertical_Box_combination.Add(sub_horizontal_box_bottom)
        """all objects added into main sizer"""
               
       
        
        
            
        
        
        
        


        
        """ Everything gets added into gridsizer to fill the panel """
        gSizer1.AddSpacer(25)
        gSizer1.Add(horizontal_combination,wx.ALL|wx.EXPAND)
       
        gSizer1.Add(sub_horizontal_box_bottom, wx.ALIGN_BOTTOM)
        complete_sizer = wx.BoxSizer(wx.VERTICAL)
        complete_sizer.Add(gSizer1,wx.ALL|wx.EXPAND|wx.ALIGN_CENTER|wx.ALIGN_RIGHT)
       
        self.SetSizerAndFit(vertical_Box_combination)
        self.Layout()      


    def SaveData(self,event):
       page_two= self.GetParent().GetPage(1)
       page_two_set = page_two.Hidden_Logic.GetValue()
       
       high_blood=(self.HighBlood.GetValue())
       low_blood=(self.LowBlood.GetValue())
       weight = (self.WeightVariable.GetValue())
       feet = (self.StaticFeet.GetValue())
       inch = (self.StaticInch.GetValue())
       
       race = (self.race.GetValue())
       age = (self.AgeVariable.GetValue())
       heart_attk =(self.check_heart_attk.GetValue())
       stroke = (self.check_stroke.GetValue())
       heart_fail = (self.check_heart_fail.GetValue())
       kidney = (self.check_kidney.GetValue())
       diabetus = (self.check_diabetus.GetValue())
       smoking = (self.check_smoking.GetValue())
       artery = (self.check_artery.GetValue())
       vasc = (self.check_vasc.GetValue())
       chol = (self.check_chol.GetValue())
       genes = (self.check_genes.GetValue())
       life_change = (self.life_change.GetValue())
       zip_code = (self.zip_code.GetValue())
       drinking = (self.drinking.GetValue())

       file_name = self.SavingFile()
       Saving_File_Data(file_name,high_blood,low_blood,weight,feet,inch,race,age,heart_attk,stroke,heart_fail,kidney,diabetus,smoking,artery,vasc,chol,genes,life_change,zip_code,drinking)

    
    def onOpenFile(self, event):
        """
        Create and show the Open FileDialog
        """
        wildcard = "Python source(*.ini)|*.ini"
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            print "You chose the following file(s):"
            for path in paths:
                print path
        dlg.Destroy()
        
        config= ConfigParser.RawConfigParser()
        config.read(path)
    
        self.HighBlood.SetValue(int(config.get('Doctor', 'high_blood')))
        self.LowBlood.SetValue(int(config.get('Doctor', 'low_blood')))
        self.WeightVariable.SetValue(config.get('Doctor', 'weight'))
        self.StaticFeet.SetValue(config.get('Doctor', 'feet'))
        self.StaticInch.SetValue(config.get('Doctor', 'inch'))
        self.race.SetValue(config.get('Doctor','race'))
        self.AgeVariable.SetValue(config.get('Doctor', 'age'))
        self.check_heart_attk.SetValue(self.boolean(config.get('Doctor','heart_attk')))
        self.check_stroke.SetValue(self.boolean(config.get('Doctor', 'stroke')))
        self.check_heart_fail.SetValue(self.boolean(config.get('Doctor', 'heart_fail')))
        self.check_kidney.SetValue(self.boolean(config.get('Doctor','kidney')))
        self.check_diabetus.SetValue(self.boolean(config.get('Doctor','diabetus')))
        self.check_smoking.SetValue(self.boolean(config.get('Doctor', 'smoking')))
        self.check_artery.SetValue(self.boolean(config.get('Doctor', 'artery')))
        self.check_vasc.SetValue(self.boolean(config.get('Doctor', 'vasc')))
        self.check_chol.SetValue(self.boolean(config.get('Doctor', 'chol')))
        self.check_genes.SetValue(self.boolean(config.get('Doctor','genes')))
        self.life_change.SetValue(self.boolean(config.get('Doctor', 'life_change')))
        self.zip_code.SetValue(config.get('Doctor', 'zip_code'))
        self.drinking.SetValue(self.boolean(config.get('Doctor', 'drinking')))
        
        

    def boolean(self,value):
        if(value =="False"):
            return False
        else:
            return True
        
   
    def SavingFile(self):
        wildcard = "Python source(*.ini)|*.ini"
        dlg = dlg = wx.FileDialog(
            self, message="Save file as ...", 
            defaultDir=os.getcwd(), 
            defaultFile="", wildcard=wildcard, style=wx.SAVE
            )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            print "You chose the following filename: %s" % path
            return path
        dlg.Destroy()      

    def SetHealth(self,event):
        print "pushed mah buttons"
    
        
        page_two= self.GetParent().GetPage(1)
        page_two.Hidden_Logic.SetValue('bad')
        page_two.Update()
        
    def good(self,event):
        print "set health good check"
        page_two= self.GetParent().GetPage(1)
        page_two.Hidden_Logic.SetValue('good')
        page_two.Update()

    def SetHealthAvg(self,event):
        print "set avg"
        page_two= self.GetParent().GetPage(1)
        page_two.Hidden_Logic.SetValue('avg')
        page_two.Update()
        
    def SetHealthGood(self,event):
        self.doctor_frame.HealthStat('good')
        

    def check_genderm(self, event):
        self.cbf.SetValue(False)
        self.thegender = 'male'
    def check_genderf(self, event):
        self.cbm.SetValue(False)
        self.thegender = 'female'
    def blood_pressure_solution(self, event):
       print "generating solution"
       self.ShowMessageDlg("The results are inaccurate and only display proof on concept results. Do not take the results as accurate","WARNING",wx.YES_NO|wx.YES_DEFAULT|wx.ICON_WARNING)
       if(self.cbm.GetValue()==True):
           gender ="Male"
       else:
           gender ="Female"
       try:
               high_blood=float(self.HighBlood.GetValue())
               low_blood=float(self.LowBlood.GetValue())
               weight = float(self.WeightVariable.GetValue())
               feet = float(self.StaticFeet.GetValue())
               inch = float(self.StaticInch.GetValue())
       
               race = int(self.RaceValue(self.race.GetValue()))
               age = float(self.AgeVariable.GetValue())
               heart_attk =int(self.check_heart_attk.GetValue())
               stroke = int(self.check_stroke.GetValue())
               heart_fail = int(self.check_heart_fail.GetValue())
               kidney = int(self.check_kidney.GetValue())
               diabetus = int(self.check_diabetus.GetValue())
               smoking = int(self.check_smoking.GetValue())
               artery = int(self.check_artery.GetValue())
               vasc = int(self.check_vasc.GetValue())
               chol = int(self.check_chol.GetValue())
               genes = int(self.check_genes.GetValue())
               life_change = int(self.life_change.GetValue())
               zip_code = int(self.zip_code.GetValue())
               drinking = int(self.drinking.GetValue())
       
       except ValueError, Argument:
               
               self.ShowMessageDlg("one of the fields has not been entered in properly","ERROR",wx.YES_NO|wx.YES_DEFAULT|wx.ICON_EXCLAMATION)
               exc_type, exc_obj, exc_tb = sys.exc_info()
               tb = sys.exc_info()[2]
               print Argument
               
               
      
       
       convert_kilo = .453592
       convert_centi = 2.54
       weight = weight*convert_kilo
       height = ((feet*12)*convert_centi+ inch*convert_centi)/100
       bmi = weight/height
       print "bmi is : %s" % bmi
       
       patient_health = TableData(age,race,bmi,high_blood,low_blood,heart_attk,stroke,heart_fail,kidney,diabetus,smoking,artery,vasc,chol,genes,life_change,zip_code,drinking)
       print "patient_health is %s" % patient_health       
       self.PatientStatus(patient_health)
    def ShowMessageDlg(self,msg,title,style):
            dlg = wx.MessageDialog(parent=None, message=msg, caption=title, style=style)
            dlg.ShowModal()
            dlg.Destroy()
    def PatientStatus(self,health):
        if(health=='very good') or (health=='good'):
            page_two= self.GetParent().GetPage(1)
            page_three =self.GetParent().GetPage(2)
            
            page_two.Hidden_Logic.SetValue('good')
            page_three.Hidden_Logic.SetValue('good')
            
            page_two.Update()
            page_three.Update()
            
        if(health =='average'):
            page_two= self.GetParent().GetPage(1)
            page_three = self.GetParent().GetPage(2)
            
            page_two.Hidden_Logic.SetValue('avg')
            if(float(self.AgeVariable.GetValue())>45):
                page_three.Hidden_Logic.SetValue('avg replace')
            else:
                page_three.Hidden_Logic.SetValue('avg')
            
                       
            page_two.Update()
            page_three.Update()
            
        if(health =='bad') or (health=='very bad'):
            page_two= self.GetParent().GetPage(1)
            page_three = self.GetParent().GetPage(2)
            
            page_two.Hidden_Logic.SetValue('bad')
            answer=int(self.AgeVariable.GetValue())
            if(answer > 45):
                print "RIGHT HERE JARED"
                page_three.Hidden_Logic.SetValue('heart replace')
            else:
                print "changing to valve replace"
                page_three.Hidden_Logic.SetValue('valve replace')
                
            page_two.Update()
            page_three.Update()
            
    def RaceValue(self,argument):
        print "in race!"
        print "argument is: %s" % argument
        if (argument=='Asian'):
            return 6
        if (argument=='Indian'):
            return 5
        if (argument=='Caucasian'):
            print "returning 3"
            return 3
        if (argument=='Hispanic'):
            return 2
        if (argument=='African'):
            return 1






        
    def ChangeSlideHigh(self,event):
        boom = self.hblood.GetValue()
        if(self.Checkfloat(boom)==True and int(boom)>90):
           
            self.HighBlood.SetValue(int(boom))
            
    def ChangeSlideLow(self,event):
        boom = self.lblood.GetValue()
        if(self.Checkfloat(boom)==True and int(boom)>50):
            self.LowBlood.SetValue(int(boom))
        
    def Checkfloat(self,value):
        try:
            float(value)
            return True
        except ValueError:
            return False
        
            
    
class PageTwo(wx.Panel):
    def __init__(self, parent):
        locale = wx.Locale(wx.LANGUAGE_ENGLISH)
        font = wx.Font(12, wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.parent = parent       
        wx.Panel.__init__(self, parent)
        Main_box_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.doctor_frame = self.GetParent().GetParent().GetParent()

        self.panelGood = wx.Panel(self)
        self.CurrentPanel = self.panelGood
        self.panelBad = wx.Panel(self)
        self.panelAvg = wx.Panel(self)
        self.panelGood.Hide()
        self.panelAvg.Hide()
        self.panelBad.Hide()
        self.Update()
        self.Hidden_Logic = wx.TextCtrl(self,-1,value=self.doctor_frame.GetHealth().lower())
        self.Hidden_Logic.Bind(wx.EVT_TEXT, self.ChangeValue)
      
        self.Hidden_Logic
        
        self.PhotoMaxSize = 240

        self.Hidden_Logic.Hide()
       


     #########THIS IS THE GOOD HEALTH DISPLAY#######################################################
        self.good_sub_horizontal_box_bottom = wx.BoxSizer(wx.HORIZONTAL)
        self.good_sub_vertical_box = wx.BoxSizer(wx.VERTICAL)
        self.good_sub_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        self.good_text2_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        self.good_text3_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        self.good_text4_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        self.good_text5_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        self.good_horizontal_box = wx.BoxSizer(wx.HORIZONTAL)
        self.good_vertical_box = wx.BoxSizer(wx.VERTICAL)


        

        """set Sizer for bottom of screen"""

        self.good_final_sizer = wx.BoxSizer(wx.VERTICAL)

        """set bottom of screen buttons and event handling"""
        
        





       

       
    
        """This is where the upper potion of page is created"""

        """First Alignment"""
        self.patient_text_word = wx.StaticText(self.panelGood, -1, u"You Have Great Blood Pressure")
        self.good_sub_horizontal.Add(self.patient_text_word, wx.ALL)
        self.patient_text_word.SetFont(font) 
       
       



        self.good_image1 = wx.Image("vein_flow.gif",wx.BITMAP_TYPE_ANY)
        self.good_image2 = wx.Image("bloodpressure_data.jpg",wx.BITMAP_TYPE_ANY)
        
        

        
        self.good_image1 = self.good_image1.Scale(300,300)
        self.good_image2 = self.good_image2.Scale(300,300)

        self.good_imageCtrl  = wx.StaticBitmap(self.panelGood, wx.ID_ANY,wx.BitmapFromImage(self.good_image1))
        self.good_imageCtrl2 = wx.StaticBitmap(self.panelGood, wx.ID_ANY, wx.BitmapFromImage(self.good_image2))

        
        self.good_horizontal_box.Add(self.good_imageCtrl,0,wx.ALIGN_CENTER | wx.ALL)
        self.good_horizontal_box.Add(self.good_imageCtrl2, 0, wx.ALIGN_CENTER | wx.ALL,border=5)
        self.good_vertical_box.Add(self.good_horizontal_box,-1,wx.ALL)



        



        self.m_button1 = wx.Button(self.panelGood, wx.ID_ANY, u"Main Menu", wx.DefaultPosition, wx.DefaultSize)
        self.good_sub_horizontal_box_bottom.Add(self.m_button1,0,wx.EXPAND|wx.RIGHT, 5)
        self.m_button1.Bind(wx.EVT_BUTTON, self.doctor_frame.MainMenu)
    
        self.m_button2 = wx.Button(self.panelGood, wx.ID_ANY, u"Patients", wx.DefaultPosition, wx.DefaultSize)
        self.good_sub_horizontal_box_bottom.Add(self.m_button2,0,wx.EXPAND|wx.RIGHT,5)
        self.m_button2.Bind(wx.EVT_BUTTON, self.doctor_frame.Patients)

        self.m_button3 = wx.Button(self.panelGood, wx.ID_ANY, u"Engineers", wx.DefaultPosition, wx.DefaultSize)
        self.good_sub_horizontal_box_bottom.Add(self.m_button3,0, wx.EXPAND|wx.RIGHT,5)
        self.m_button3.Bind(wx.EVT_BUTTON, self.doctor_frame.Engineers)

        self.m_button4 = wx.Button(self.panelGood, wx.ID_ANY, u"Simulation", wx.DefaultPosition, wx.DefaultSize)
        self.good_sub_horizontal_box_bottom.Add(self.m_button4,0,wx.EXPAND|wx.RIGHT,5)
        self.m_button4.Bind(wx.EVT_BUTTON, self.doctor_frame.Simulation)
        
        self.good_final_sizer.Add(self.good_sub_horizontal,0,wx.ALIGN_TOP)
        
        self.good_final_sizer.Add(self.good_horizontal_box,0,wx.ALIGN_CENTER)
        self.good_final_sizer.Add(self.good_sub_horizontal_box_bottom, 0,wx.ALIGN_BOTTOM)
        
                                




      



#########THIS IS THE BAD PAGE DISPLAY########################################################
        self.bad_final_box_sizer= wx.BoxSizer(wx.VERTICAL)
        self.bad_final_box_sizer_hor = wx.BoxSizer(wx.HORIZONTAL)
        self.bad_horizontal_box_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bad_vertical_box_sizer = wx.BoxSizer(wx.VERTICAL)
        self.bad_horizontal_image_box =wx.BoxSizer(wx.HORIZONTAL)
        self.bad_vertical_box_hor = wx.BoxSizer(wx.HORIZONTAL)
        self.bad_second_box = wx.BoxSizer(wx.VERTICAL)
        self.bad_title_box = wx.BoxSizer(wx.HORIZONTAL)
        self.bad_horizontal_comb = wx.BoxSizer(wx.HORIZONTAL)
        self.bad_sub_horizontal_box_bottom_bad=wx.BoxSizer(wx.HORIZONTAL)
        
        BadText = wx.StaticText(self.panelBad,0,u"People that have unhealthy blood pressure might have one of these issues")
     
        self.bad_title_box.Add(BadText,wx.EXPAND|wx.ALL)
       
        BadText.SetFont(font)
        
        hyper_tension_text = wx.StaticText(self.panelBad,-1,"they could have Hypertension                                           or Hypotension")
        hyper_tension_text.SetFont(font)
        self.bad_vertical_box_sizer.Add(hyper_tension_text,wx.ALIGN_CENTER)

        hyper_tension_image = wx.Image("hypertension.png", wx.BITMAP_TYPE_ANY)
        hypo_tension_image = wx.Image("low_blood_image.jpg",wx.BITMAP_TYPE_ANY)

        h_width=hypo_tension_image.GetWidth()
        h_height=hypo_tension_image.GetHeight()
        if h_width > h_height:
            h_new_width = self.PhotoMaxSize
            h_new_height = self.PhotoMaxSize * h_height/h_width
        else:
            h_new_width = self.PhotoMaxSize
            h_new_height = self.PhotoMaxSize * h_width/h_height
        
        width = hyper_tension_image.GetWidth()
        height = hyper_tension_image.GetHeight()
        if width > height:
            new_width = self.PhotoMaxSize
            new_height = self.PhotoMaxSize * height/width
        else:
            new_width = self.PhotoMaxSize
            new_height = self.PhotoMaxSize * width/height
        hyper_tension_image = hyper_tension_image.Scale(400,300)
        hypo_tension_image = hypo_tension_image.Scale(400,300)

        
        self.imageCtrl_hypo = wx.StaticBitmap(self.panelBad, wx.ID_ANY,wx.BitmapFromImage(hypo_tension_image))
        self.imageCtrl=wx.StaticBitmap(self.panelBad, wx.ID_ANY,wx.BitmapFromImage(hyper_tension_image))
        
     
        self.bad_horizontal_image_box.Add(self.imageCtrl,0,wx.ALIGN_CENTER | wx.ALL,border=10)
        self.bad_horizontal_image_box.Add(self.imageCtrl_hypo, 0, wx.ALIGN_CENTER | wx.ALL,border=30)
        self.bad_horizontal_comb.Add(self.bad_horizontal_image_box,-1,wx.ALL)
        self.bad_horizontal_comb.Add(self.bad_second_box,-1,wx.ALL)

        self.bad_vertical_box_sizer.Add(self.bad_horizontal_image_box)

        hyp_link = wx.HyperlinkCtrl(self.panelBad,-1,url="http://www.medicalnewstoday.com/articles/150109.php",label="Hypertension additional information")
        hypo_link = wx.HyperlinkCtrl(self.panelBad,-1,url="https://www.nlm.nih.gov/medlineplus/ency/article/007278.htm",label="Hypotension additional information")

        self.bad_vertical_box_hor.Add(hyp_link)
        self.bad_vertical_box_hor.AddSpacer(25)
        self.bad_vertical_box_hor.Add(hypo_link)
        self.bad_vertical_box_sizer.Add(self.bad_vertical_box_hor,0,wx.ALIGN_CENTER)
        
        
        self.m_button1 = wx.Button(self.panelBad, wx.ID_ANY, u"Main Menu", wx.DefaultPosition, wx.DefaultSize)
        self.bad_sub_horizontal_box_bottom_bad.Add(self.m_button1,0,wx.EXPAND|wx.RIGHT, 5)
        self.m_button1.Bind(wx.EVT_BUTTON, self.doctor_frame.MainMenu)
    
        self.m_button2 = wx.Button(self.panelBad, wx.ID_ANY, u"Patients", wx.DefaultPosition, wx.DefaultSize)
        self.bad_sub_horizontal_box_bottom_bad.Add(self.m_button2,0,wx.EXPAND|wx.RIGHT,5)
        self.m_button2.Bind(wx.EVT_BUTTON, self.doctor_frame.Patients)

        self.m_button3 = wx.Button(self.panelBad, wx.ID_ANY, u"Engineers", wx.DefaultPosition, wx.DefaultSize)
        self.bad_sub_horizontal_box_bottom_bad.Add(self.m_button3,0, wx.EXPAND|wx.RIGHT,5)
        self.m_button3.Bind(wx.EVT_BUTTON, self.doctor_frame.Engineers)

        self.m_button4 = wx.Button(self.panelBad, wx.ID_ANY, u"Simulation", wx.DefaultPosition, wx.DefaultSize)
        self.bad_sub_horizontal_box_bottom_bad.Add(self.m_button4,0,wx.EXPAND|wx.RIGHT,5)
        self.m_button4.Bind(wx.EVT_BUTTON, self.doctor_frame.Simulation)

        
        self.bad_final_box_sizer.Add(self.bad_title_box, wx.ALIGN_TOP|wx.ALL)
        self.bad_final_box_sizer.AddSpacer(25)
        self.bad_final_box_sizer.Add(self.bad_vertical_box_sizer,wx.ALIGN_CENTER|wx.ALL)
        self.bad_final_box_sizer.Add(self.bad_sub_horizontal_box_bottom_bad,-1,wx.ALIGN_BOTTOM|wx.EXPAND)
        self.bad_final_box_sizer_hor.Add(self.bad_final_box_sizer,0,wx.ALL|wx.ALIGN_CENTER)
       
        

#########THIS IS THE AVERAGE HEALTH DISPLAY#######################################
        self.avg_title_box = wx.BoxSizer(wx.VERTICAL)
        self.avg_horizontal_box = wx.BoxSizer(wx.HORIZONTAL)
        self.avg_vertical_box = wx.BoxSizer(wx.VERTICAL)
        self.avg_final_box_sizer = wx.BoxSizer(wx.VERTICAL)
        self.avg_sub_horizontal_box_bottom_avg = wx.BoxSizer(wx.HORIZONTAL)
        self.avg_text = wx.StaticText(self.panelAvg,0,u"Here is some advice on how to maintain healthy blood pressure")
        
        
        self.avg_title_box.Add(self.avg_text,wx.ALL)
        self.avg_text.SetFont(font)

        avg_image1 = wx.Image("avg_heart_info_1.jpg",wx.BITMAP_TYPE_ANY)
        avg_image2 = wx.Image("blood_pressure_graph.jpg",wx.BITMAP_TYPE_ANY)
        
        self.avg_text_img = wx.StaticText(self.panelAvg,-1,"changing of Diet will improve blood pressure  ")
        self.avg_text_img.SetFont(font)
        self.avg_title_box.Add(self.avg_text_img,0,wx.ALL)

        
        self.avg_image1 = avg_image1.Scale(250,250)
        self.avg_image2 = avg_image2.Scale(500,300)

        self.imageCtrl  = wx.StaticBitmap(self.panelAvg, wx.ID_ANY,wx.BitmapFromImage(self.avg_image1))
        self.imageCtrl2 = wx.StaticBitmap(self.panelAvg, wx.ID_ANY, wx.BitmapFromImage(self.avg_image2))

        
        self.avg_horizontal_box.Add(self.imageCtrl,0,wx.ALIGN_CENTER | wx.ALL)
        self.avg_horizontal_box.Add(self.imageCtrl2, 0, wx.ALIGN_CENTER | wx.ALL,border=5)
        self.avg_vertical_box.Add(self.avg_horizontal_box,-1,wx.ALL)


        self.m_button1 = wx.Button(self.panelAvg, wx.ID_ANY, u"Main Menu", wx.DefaultPosition, wx.DefaultSize)
        self.avg_sub_horizontal_box_bottom_avg.Add(self.m_button1,0,wx.EXPAND|wx.RIGHT, 5)
        self.m_button1.Bind(wx.EVT_BUTTON, self.doctor_frame.MainMenu)
    
        self.m_button2 = wx.Button(self.panelAvg, wx.ID_ANY, u"Patients", wx.DefaultPosition, wx.DefaultSize)
        self.avg_sub_horizontal_box_bottom_avg.Add(self.m_button2,0,wx.EXPAND|wx.RIGHT,5)
        self.m_button2.Bind(wx.EVT_BUTTON, self.doctor_frame.Patients)

        self.m_button3 = wx.Button(self.panelAvg, wx.ID_ANY, u"Engineers", wx.DefaultPosition, wx.DefaultSize)
        self.avg_sub_horizontal_box_bottom_avg.Add(self.m_button3,0, wx.EXPAND|wx.RIGHT,5)
        self.m_button3.Bind(wx.EVT_BUTTON, self.doctor_frame.Engineers)

        self.m_button4 = wx.Button(self.panelAvg, wx.ID_ANY, u"Simulation", wx.DefaultPosition, wx.DefaultSize)
        self.avg_sub_horizontal_box_bottom_avg.Add(self.m_button4,0,wx.EXPAND|wx.RIGHT,5)
        self.m_button4.Bind(wx.EVT_BUTTON, self.doctor_frame.Simulation)


        self.avg_final_box_sizer.Add(self.avg_title_box,0,wx.ALL)
        
        self.avg_final_box_sizer.Add(self.avg_horizontal_box,0,wx.ALL|wx.EXPAND|wx.ALIGN_CENTER)
        self.avg_final_box_sizer.Add( self.avg_sub_horizontal_box_bottom_avg,0,wx.ALIGN_BOTTOM|wx.ALL)
        
       
        
        
###########################DEFINITIONS###################################################        
        
    def ChangeValue(self,event):
        

        


        if(self.Hidden_Logic.GetValue().lower()=='bad'):
            print "changing to bad"
            self.CurrentPanel.Hide()
            self.CurrentPanel=self.panelBad
            self.panelBad.SetSizerAndFit(self.bad_final_box_sizer_hor)
            self.CurrentPanel.Show()
            
            
        if(self.Hidden_Logic.GetValue().lower()=='avg'):
            print "changing to average"
            self.CurrentPanel.Hide()
            self.CurrentPanel=self.panelAvg
            self.CurrentPanel.SetSizerAndFit(self.avg_final_box_sizer)
            self.CurrentPanel.Show()

        if(self.Hidden_Logic.GetValue().lower()=='good'):
            print "changing to Good"
            self.CurrentPanel.Hide()
            self.CurrentPanel=self.panelGood
            self.CurrentPanel.SetSizerAndFit(self.good_final_sizer)
            self.CurrentPanel.Show()  
       
    
#########################################################################

class PageThree(wx.Panel):
    def __init__(self, parent):
        locale = wx.Locale(wx.LANGUAGE_ENGLISH)
        font = wx.Font(15, wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        font2= wx.Font(11, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.parent = parent  
        wx.Panel.__init__(self, parent)
        self.doctor_frame = self.GetParent().GetParent().GetParent()

        self.panelGood = wx.Panel(self)
        self.CurrentPanel = self.panelGood
        self.panelBadHeart = wx.Panel(self)
        self.panelBadValve = wx.Panel(self)
        
        self.panelAvg = wx.Panel(self)
        self.panelAvgReplace = wx.Panel(self)
        
        self.panelGood.Hide()
        
        self.panelAvg.Show()
        self.panelAvgReplace.Hide()
        self.panelBadValve.Hide()
        self.panelBadHeart.Hide()
        self.Update()
        self.Hidden_Logic = wx.TextCtrl(self,-1,value=self.doctor_frame.GetHealth().lower())
        self.Hidden_Logic.Bind(wx.EVT_TEXT, self.ChangeValue)
        
        
        self.PhotoMaxSize = 240

        self.Hidden_Logic.Hide()

        #########################AVERAGE FOR VALVE REPLACEMENT#####################################################################
        self.avg_title_box = wx.BoxSizer(wx.VERTICAL)
        self.avg_horizontal_box = wx.BoxSizer(wx.HORIZONTAL)
        self.avg_vertical_box = wx.BoxSizer(wx.VERTICAL)
        self.avg_vertical_box_right = wx.BoxSizer(wx.VERTICAL)
        self.avg_final_box_sizer = wx.BoxSizer(wx.VERTICAL)
        self.avg_sub_horizontal_box_bottom_avg = wx.BoxSizer(wx.HORIZONTAL)
        self.avg_text = wx.StaticText(self.panelAvg,0,u"Things to consider about heart valve replacements")
        with open('avg_heart_valve_info1.txt') as MyInfo:
            data="".join(line.rstrip() for line in MyInfo)
        
        self.avg_title_box.Add(self.avg_text,wx.ALL)
        self.avg_text.SetFont(font)
        
        self.information = rt.RichTextCtrl(self.panelAvg, value='',style=wx.VSCROLL|wx.NO_BORDER|wx.TE_READONLY,size=(300,100))
        self.information.WriteText(data)
        self.information.SetFont(font2)
        self.avg_vertical_box.Add(self.information,wx.ALL|wx.EXPAND|wx.RIGHT)

        hyp_link = wx.HyperlinkCtrl(self.panelAvg,-1,url="http://www.heart.org/HEARTORG/Conditions/More/HeartValveProblemsandDisease/Options-for-Heart-Valve-Replacement_UCM_450816_Article.jsp#.Vt3b3PlViko",label="For more information click on me")
        self.avg_vertical_box.Add(hyp_link,0,wx.ALL|wx.EXPAND|wx.ALIGN_RIGHT)
        
        avg_image1 = wx.Image("heart-valve-replacement.jpg",wx.BITMAP_TYPE_ANY)
        #avg_image2 = wx.Image("blood_pressure_graph.jpg",wx.BITMAP_TYPE_ANY)
        
        #self.avg_text_img = wx.StaticText(self.panelAvg,-1,"Your Diet might have to change  ")
        #self.avg_text_img.SetFont(font)
        #self.avg_title_box.Add(self.avg_text_img,0,wx.ALL)

        
        self.avg_image1 = avg_image1.Scale(400,400)
        #self.avg_image2 = avg_image2.Scale(500,300)

        self.imageCtrl  = wx.StaticBitmap(self.panelAvg, wx.ID_ANY,wx.BitmapFromImage(self.avg_image1))
        #self.imageCtrl2 = wx.StaticBitmap(self.panelAvg, wx.ID_ANY, wx.BitmapFromImage(self.avg_image2))

        
        self.avg_vertical_box_right.Add(self.imageCtrl,0,wx.ALIGN_RIGHT | wx.ALL|wx.EXPAND|wx.RIGHT)
        #self.avg_horizontal_box.Add(self.imageCtrl2, 0, wx.ALIGN_CENTER | wx.ALL,border=5)
        #self.avg_vertical_box.Add(self.avg_horizontal_box,-1,wx.ALL)


        self.m_button1 = wx.Button(self.panelAvg, wx.ID_ANY, u"Main Menu", wx.DefaultPosition, wx.DefaultSize)
        self.avg_sub_horizontal_box_bottom_avg.Add(self.m_button1,0,wx.EXPAND|wx.RIGHT, 5)
        self.m_button1.Bind(wx.EVT_BUTTON, self.doctor_frame.MainMenu)
    
        self.m_button2 = wx.Button(self.panelAvg, wx.ID_ANY, u"Patients", wx.DefaultPosition, wx.DefaultSize)
        self.avg_sub_horizontal_box_bottom_avg.Add(self.m_button2,0,wx.EXPAND|wx.RIGHT,5)
        self.m_button2.Bind(wx.EVT_BUTTON, self.doctor_frame.Patients)

        self.m_button3 = wx.Button(self.panelAvg, wx.ID_ANY, u"Engineers", wx.DefaultPosition, wx.DefaultSize)
        self.avg_sub_horizontal_box_bottom_avg.Add(self.m_button3,0, wx.EXPAND|wx.RIGHT,5)
        self.m_button3.Bind(wx.EVT_BUTTON, self.doctor_frame.Engineers)

        self.m_button4 = wx.Button(self.panelAvg, wx.ID_ANY, u"Simulation", wx.DefaultPosition, wx.DefaultSize)
        self.avg_sub_horizontal_box_bottom_avg.Add(self.m_button4,0,wx.EXPAND|wx.RIGHT,5)
        self.m_button4.Bind(wx.EVT_BUTTON, self.doctor_frame.Simulation)


      
        self.avg_horizontal_box.Add(self.avg_vertical_box,0,wx.ALL|wx.EXPAND)
        self.avg_horizontal_box.AddSpacer(60)
        self.avg_horizontal_box.Add(self.avg_vertical_box_right,0,wx.ALL|wx.EXPAND)
        self.final_vert_box = wx.BoxSizer(wx.VERTICAL)
        self.final_vert_box.Add(self.avg_horizontal_box,wx.ALL|wx.EXPAND|wx.ALIGN_CENTER)
        self.avg_final_box_sizer.AddSpacer(45)
        self.avg_final_box_sizer.Add(self.avg_title_box,0,wx.ALL|wx.ALIGN_CENTER|wx.ALIGN_TOP)
        self.avg_final_box_sizer.Add(self.final_vert_box,0,wx.ALL|wx.ALIGN_CENTER)
        self.avg_final_box_sizer.AddSpacer(20)
        self.avg_final_box_sizer.Add( self.avg_sub_horizontal_box_bottom_avg,wx.ALL|wx.ALIGN_BOTTOM)
        
############################AVERAGE HEART FOR NEEDING FULL REPLACEMENT#########################################
        self.avgreplace_title_box = wx.BoxSizer(wx.VERTICAL)
        self.avgreplace_horizontal_box = wx.BoxSizer(wx.HORIZONTAL)
        self.avgreplace_vertical_box = wx.BoxSizer(wx.VERTICAL)
        self.avgreplace_vertical_box_right = wx.BoxSizer(wx.VERTICAL)
        self.avg_replace_final_box_sizer = wx.BoxSizer(wx.VERTICAL)
        self.avgreplace_sub_horizontal_box_bottom_avg = wx.BoxSizer(wx.HORIZONTAL)
        self.avgreplace_text = wx.StaticText(self.panelAvgReplace,0,u"Some patient's may need a heart replacement")
        with open('avg_heart_replace.txt') as MyInfo:
            data="".join(line.rstrip() for line in MyInfo)
        
        self.avgreplace_title_box.Add(self.avgreplace_text,wx.ALL)
        self.avgreplace_text.SetFont(font)
        
        self.avg_information = rt.RichTextCtrl(self.panelAvgReplace, value='',style=wx.VSCROLL|wx.NO_BORDER|wx.TE_READONLY,size=(300,100))
        self.avg_information.WriteText(data)
        self.avg_information.SetFont(font2)
        self.avgreplace_vertical_box.Add(self.avg_information,wx.ALL|wx.EXPAND|wx.RIGHT)

        hyp_link = wx.HyperlinkCtrl(self.panelAvgReplace,-1,url="https://www.nhlbi.nih.gov/health/health-topics/topics/tah",label="For more information click on me")
        self.avgreplace_vertical_box.Add(hyp_link,0,wx.ALL|wx.EXPAND|wx.ALIGN_RIGHT)
        
        avgreplace_image1 = wx.Image("artificial_heart_avg.jpg",wx.BITMAP_TYPE_ANY)
        #avg_image2 = wx.Image("blood_pressure_graph.jpg",wx.BITMAP_TYPE_ANY)
        
        #self.avg_text_img = wx.StaticText(self.panelAvg,-1,"Your Diet might have to change  ")
        #self.avg_text_img.SetFont(font)
        #self.avg_title_box.Add(self.avg_text_img,0,wx.ALL)

        
        self.avgreplace_image1 = avgreplace_image1.Scale(400,400)
        #self.avg_image2 = avg_image2.Scale(500,300)

        self.imageCtrlReplace  = wx.StaticBitmap(self.panelAvgReplace, wx.ID_ANY,wx.BitmapFromImage(self.avgreplace_image1))
        #self.imageCtrl2 = wx.StaticBitmap(self.panelAvg, wx.ID_ANY, wx.BitmapFromImage(self.avg_image2))

        
        self.avgreplace_vertical_box_right.Add(self.imageCtrlReplace,0,wx.ALIGN_RIGHT | wx.ALL|wx.EXPAND|wx.RIGHT)
        #self.avg_horizontal_box.Add(self.imageCtrl2, 0, wx.ALIGN_CENTER | wx.ALL,border=5)
        #self.avg_vertical_box.Add(self.avg_horizontal_box,-1,wx.ALL)


        self.m_button1 = wx.Button(self.panelAvgReplace, wx.ID_ANY, u"Main Menu", wx.DefaultPosition, wx.DefaultSize)
        self.avgreplace_sub_horizontal_box_bottom_avg.Add(self.m_button1,0,wx.EXPAND|wx.RIGHT, 5)
        self.m_button1.Bind(wx.EVT_BUTTON, self.doctor_frame.MainMenu)
    
        self.m_button2 = wx.Button(self.panelAvgReplace, wx.ID_ANY, u"Patients", wx.DefaultPosition, wx.DefaultSize)
        self.avgreplace_sub_horizontal_box_bottom_avg.Add(self.m_button2,0,wx.EXPAND|wx.RIGHT,5)
        self.m_button2.Bind(wx.EVT_BUTTON, self.doctor_frame.Patients)

        self.m_button3 = wx.Button(self.panelAvgReplace, wx.ID_ANY, u"Engineers", wx.DefaultPosition, wx.DefaultSize)
        self.avgreplace_sub_horizontal_box_bottom_avg.Add(self.m_button3,0, wx.EXPAND|wx.RIGHT,5)
        self.m_button3.Bind(wx.EVT_BUTTON, self.doctor_frame.Engineers)

        self.m_button4 = wx.Button(self.panelAvgReplace, wx.ID_ANY, u"Simulation", wx.DefaultPosition, wx.DefaultSize)
        self.avgreplace_sub_horizontal_box_bottom_avg.Add(self.m_button4,0,wx.EXPAND|wx.RIGHT,5)
        self.m_button4.Bind(wx.EVT_BUTTON, self.doctor_frame.Simulation)


      
        self.avgreplace_horizontal_box.Add(self.avgreplace_vertical_box,0,wx.ALL|wx.EXPAND)
        self.avgreplace_horizontal_box.AddSpacer(60)
        self.avgreplace_horizontal_box.Add(self.avgreplace_vertical_box_right,0,wx.ALL|wx.EXPAND)
        self.finalreplace_vert_box = wx.BoxSizer(wx.VERTICAL)
        self.finalreplace_vert_box.Add(self.avgreplace_horizontal_box,wx.ALL|wx.EXPAND|wx.ALIGN_CENTER)
        self.avg_replace_final_box_sizer.AddSpacer(45)
        self.avg_replace_final_box_sizer.Add(self.avgreplace_title_box,0,wx.ALL|wx.ALIGN_CENTER|wx.ALIGN_TOP)
        self.avg_replace_final_box_sizer.Add(self.finalreplace_vert_box,0,wx.ALL|wx.ALIGN_CENTER)
        self.avg_replace_final_box_sizer.AddSpacer(20)
        self.avg_replace_final_box_sizer.Add( self.avgreplace_sub_horizontal_box_bottom_avg,wx.ALL|wx.ALIGN_BOTTOM)
#########################HEART  REPLACEMENT###########################################################

        self.badheart_title_box = wx.BoxSizer(wx.VERTICAL)
        self.badheart_horizontal_box = wx.BoxSizer(wx.HORIZONTAL)
        self.badheart_vertical_box = wx.BoxSizer(wx.VERTICAL)
        self.badheart_vertical_box_right = wx.BoxSizer(wx.VERTICAL)
        self.bad_final_box_sizer = wx.BoxSizer(wx.VERTICAL)
        self.badheart_sub_horizontal_box_bottom_avg = wx.BoxSizer(wx.HORIZONTAL)
        self.badheart_text = wx.StaticText(self.panelBadHeart,0,u"Some people need an artificial heart replacement")
        with open('bad_heart_replace.txt') as MyInfo:
            data="".join(line.rstrip() for line in MyInfo)
        
        self.badheart_title_box.Add(self.badheart_text,wx.ALL)
        self.badheart_text.SetFont(font)
        
        self.badheart_information = rt.RichTextCtrl(self.panelBadHeart, value='',style=wx.VSCROLL|wx.NO_BORDER|wx.TE_READONLY,size=(300,100))
        self.badheart_information.WriteText(data)
        self.badheart_information.SetFont(font2)
        self.badheart_vertical_box.Add(self.badheart_information,wx.ALL|wx.EXPAND|wx.RIGHT)

        hyp_link = wx.HyperlinkCtrl(self.panelBadHeart,-1,url="https://www.nhlbi.nih.gov/health/health-topics/topics/tah",label="For more information click on me")
        self.badheart_vertical_box.Add(hyp_link,0,wx.ALL|wx.EXPAND|wx.ALIGN_RIGHT)
        
        badheart_image1 = wx.Image("artificial_heart_bad.jpg",wx.BITMAP_TYPE_ANY)
        badheart_image2 = wx.Image("artificial_heart_bad2.jpg",wx.BITMAP_TYPE_ANY)
        
        #self.avg_text_img = wx.StaticText(self.panelAvg,-1,"Your Diet might have to change  ")
        #self.avg_text_img.SetFont(font)
        #self.avg_title_box.Add(self.avg_text_img,0,wx.ALL)

        
        self.badheart_image1 = badheart_image1.Scale(400,200)
        self.badheart_image2 = badheart_image2.Scale(400,200)

        self.imageCtrlbadheart  = wx.StaticBitmap(self.panelBadHeart, wx.ID_ANY,wx.BitmapFromImage(self.badheart_image1))
        self.imageCtrl2badheart = wx.StaticBitmap(self.panelBadHeart, wx.ID_ANY, wx.BitmapFromImage(self.badheart_image2))

    
        self.badheart_vertical_box_right.Add(self.imageCtrlbadheart,wx.ALL|wx.ALIGN_CENTER)
        self.badheart_vertical_box_right.Add(self.imageCtrl2badheart,wx.ALL|wx.ALIGN_CENTER)
        self.Refresh()
        #self.avg_horizontal_box.Add(self.imageCtrl2, 0, wx.ALIGN_CENTER | wx.ALL,border=5)
        #self.avg_vertical_box.Add(self.avg_horizontal_box,-1,wx.ALL)


        self.m_button1 = wx.Button(self.panelBadHeart, wx.ID_ANY, u"Main Menu", wx.DefaultPosition, wx.DefaultSize)
        self.badheart_sub_horizontal_box_bottom_avg.Add(self.m_button1,0,wx.EXPAND|wx.RIGHT, 5)
        self.m_button1.Bind(wx.EVT_BUTTON, self.doctor_frame.MainMenu)
    
        self.m_button2 = wx.Button(self.panelBadHeart, wx.ID_ANY, u"Patients", wx.DefaultPosition, wx.DefaultSize)
        self.badheart_sub_horizontal_box_bottom_avg.Add(self.m_button2,0,wx.EXPAND|wx.RIGHT,5)
        self.m_button2.Bind(wx.EVT_BUTTON, self.doctor_frame.Patients)

        self.m_button3 = wx.Button(self.panelBadHeart, wx.ID_ANY, u"Engineers", wx.DefaultPosition, wx.DefaultSize)
        self.badheart_sub_horizontal_box_bottom_avg.Add(self.m_button3,0, wx.EXPAND|wx.RIGHT,5)
        self.m_button3.Bind(wx.EVT_BUTTON, self.doctor_frame.Engineers)

        self.m_button4 = wx.Button(self.panelBadHeart, wx.ID_ANY, u"Simulation", wx.DefaultPosition, wx.DefaultSize)
        self.badheart_sub_horizontal_box_bottom_avg.Add(self.m_button4,0,wx.EXPAND|wx.RIGHT,5)
        self.m_button4.Bind(wx.EVT_BUTTON, self.doctor_frame.Simulation)


      
        self.badheart_horizontal_box.Add(self.badheart_vertical_box,0,wx.ALL|wx.EXPAND)
        self.badheart_horizontal_box.AddSpacer(60)
        self.badheart_horizontal_box.Add(self.badheart_vertical_box_right,0,wx.ALL|wx.EXPAND)
        self.finalbadheart_vert_box = wx.BoxSizer(wx.VERTICAL)
        self.finalbadheart_vert_box.Add(self.badheart_horizontal_box,wx.ALL|wx.EXPAND|wx.ALIGN_CENTER)
        
        self.bad_final_box_sizer.AddSpacer(45)
        self.bad_final_box_sizer.Add(self.badheart_title_box,0,wx.ALL|wx.ALIGN_CENTER|wx.ALIGN_TOP)
        self.bad_final_box_sizer.AddSpacer(30)
        self.bad_final_box_sizer.Add(self.finalbadheart_vert_box,0,wx.ALL|wx.ALIGN_CENTER)
        self.bad_final_box_sizer.AddSpacer(20)
        self.bad_final_box_sizer.Add( self.badheart_sub_horizontal_box_bottom_avg,wx.ALL|wx.ALIGN_BOTTOM)
        self.panelBadHeart.SetSizerAndFit(self.bad_final_box_sizer)
        self.panelBadHeart.Layout()
    ######################ARTIFICIAL Valve REPLACE###########################################################
        self.badvalve_title_box = wx.BoxSizer(wx.VERTICAL)
        self.badvalve_horizontal_box = wx.BoxSizer(wx.HORIZONTAL)
        self.badvalve_vertical_box = wx.BoxSizer(wx.VERTICAL)
        self.badvalve_vertical_box_right = wx.BoxSizer(wx.VERTICAL)
        self.badvalve_final_box_sizer = wx.BoxSizer(wx.VERTICAL)
        self.badvalve_sub_horizontal_box_bottom_avg = wx.BoxSizer(wx.HORIZONTAL)
        self.MaxImageSize=200

        self.badvalve_text = wx.StaticText(self.panelBadValve,0,u"Some people need to have valve replacements")
        with open('bad_heart_replace.txt') as MyInfo:
            data="".join(line.rstrip() for line in MyInfo)
        
        self.badvalve_final_box_sizer.Add(self.badvalve_text,wx.ALL|wx.ALIGN_TOP|wx.EXPAND)
        self.badvalve_text.SetFont(font)
        
        self.badvalve_information = rt.RichTextCtrl(self.panelBadValve, value='',style=wx.VSCROLL|wx.NO_BORDER|wx.TE_READONLY,size=(400,500))
        self.badvalve_information.WriteText(data)
        self.badvalve_information.SetFont(font2)
        self.badvalve_horizontal_box.Add(self.badvalve_information,wx.ALIGN_CENTER_HORIZONTAL)

        badvalvehyp_link = wx.HyperlinkCtrl(self.panelBadValve,-1,url="https://www.nhlbi.nih.gov/health/health-topics/topics/tah",label="For more information click on me")
        

        
        self.Bad_valve_img = wx.StaticBitmap(self.panelBadValve,bitmap=wx.EmptyBitmap(self.MaxImageSize,self.MaxImageSize))
        self.DisplayNext()

        self.badvalve_horizontal_box.Add(self.Bad_valve_img,0,wx.ALIGN_BOTTOM|wx.EXPAND|wx.ALL|wx.ADJUST_MINSIZE,10)
        self.badvalve_final_box_sizer.Add(self.badvalve_horizontal_box,0,wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_RIGHT|wx.ALL|wx.ADJUST_MINSIZE,10)
        self.badvalve_final_box_sizer.Add(badvalvehyp_link,0,wx.ALL|wx.EXPAND|wx.ALIGN_BOTTOM)
        self.SetSizerAndFit(self.badvalve_final_box_sizer)
        self.Layout()
        wx.EVT_CLOSE(self, self.OnCloseWindow)
    def DisplayNext(self, event=None):
        Img = wx.Image("artificial_heart_bad_valve.jpg",wx.BITMAP_TYPE_ANY)
        W = Img.GetWidth()
        H = Img.GetHeight()
        if W > H:
            NewW = self.MaxImageSize
            NewH = self.MaxImageSize * H / W
        else:
            NewH = self.MaxImageSize
            NewW = self.MaxImageSize * W / H
        Img = Img.Scale(NewW, NewH)
        self.Bad_valve_img.SetBitmap(wx.BitmapFromImage(Img))
        self.Refresh()
        self.Layout()
                                             
    def OnCloseWindow(self,event):
        self.Destroy()
        
        
    def ChangeValue(self,event):
        

        if(self.Hidden_Logic.GetValue().lower()=='heart replace'):
            print "changing to bad"
            self.CurrentPanel.Hide()
            self.CurrentPanel=self.panelBadHeart
            self.CurrentPanel.SetSizerAndFit(self.bad_final_box_sizer)
            self.CurrentPanel.Layout()
            self.CurrentPanel.Show()
        if(self.Hidden_Logic.GetValue().lower()=='valve replace'):
            self.CurrentPanel.Hide()
            self.CurrentPanel=self.panelBadValve
            self.CurrentPanel.SetSizerAndFit(self.badvalve_final_box_sizer)
            self.CurrentPanel.Show()
            
        if(self.Hidden_Logic.GetValue().lower()=='avg'):
            print "changing to average"
            self.CurrentPanel.Hide()
            self.CurrentPanel=self.panelAvg
            self.CurrentPanel.SetSizerAndFit(self.avg_final_box_sizer)
            self.CurrentPanel.Show()

        if(self.Hidden_Logic.GetValue().lower()=='avg replace'):
            self.CurrentPanel.Hide()
            self.CurrentPanel=self.panelAvgReplace
            self.CurrentPanel.SetSizerAndFit(self.avg_replace_final_box_sizer)
            self.CurrentPanel.Show()

        if(self.Hidden_Logic.GetValue().lower()=='good'):
            print "changing to good"
            self.CurrentPanel.Hide()
            self.CurrentPanel=self.panelGood
            self.CurrentPanel.SetSizerAndFit(self.good_final_sizer)
            self.CurrentPanel.Layout()
            self.CurrentPanel.Show()  

    

        
class DoctorPanel(wx.Frame):
    """"""
    instance = None
    init =0
    def __new__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = wx.Frame.__new__(self)
        elif isinstance(self.instance, wx._core._wxPyDeadObject):
            self.instance=wx.Frame.__new__(self)
        return self.instance
    def __init__(self):
        if self.init:
            return
        self.init=1
        wx.Frame.__init__(self,None, title="Blood Pressure and comparisons", size=(750,600))
        
        # Here we create a panel and a notebook on the panel
        self.p = wx.Panel(self)
        self.nb = wx.Notebook(self.p)
        
        # create the page windows as children of the notebook
        page1 = PageOne(self.nb)
        page2 = PageTwo(self.nb)
        page3 = PageThree(self.nb)
       
        # add the pages to the notebook with the label to show on the tab
        self.nb.AddPage(page1, "Patient education")
        self.nb.AddPage(page2, "Heart Condition")
        self.nb.AddPage(page3, "Artificial Heart Education")

        page2.Hidden_Logic.SetValue("start")
        
        
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.p.SetSizerAndFit(sizer)
        self.p.Layout()
        self.Centre(wx.BOTH)
        
    def MainMenu(self,event):
        self.Hide()        
        Main_menu = FrontPage()
        Main_menu.Show()

    def Patients(self,event):
        self.Hide()
        self.PatientView = PatientPanel()
        self.PatientView.Show()

    def Engineers(self, event):
        self.Hide()
        self.EngineerView = EngineerPanel()
        self.EngineerView.Show()

    def Simulation(self, event):
        self.Hide()
        self.SimulationView = SimulationPanel()
        self.SimulationView.Show()

    def blood_pressure_solution(self, event):
        print "made it in here"
        
    def HealthStat(self,status):
        self.stat = status
        
        return self.stat
    def GetHealth(self):
        print "health is  "
        return 'good'

class FrontPage(wx.Frame):
    def __init__(self):
        
        wx.Frame.__init__(self, None, title="Hearty Living GUI" , size=(550,550))
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        self.m_menubar1 = wx.MenuBar(0)
        self.SetMenuBar(self.m_menubar1)
        self.FrontPanel = wx.Panel(self)


        self.gSizer1 = wx.GridSizer(0,2,0,2)

        self.m_button1 = wx.Button(self.FrontPanel,wx.ALL ,u"Patient", wx.DefaultPosition, wx.DefaultSize)
        self.gSizer1.Add(self.m_button1,0,wx.ALL|wx.ALIGN_CENTER, 5)
        self.m_button1.Bind(wx.EVT_BUTTON, self.ViewPatient)

        self.m_button2 = wx.Button(self.FrontPanel, wx.ID_ANY, u"Doctor", wx.DefaultPosition, wx.DefaultSize)
        self.gSizer1.Add(self.m_button2,0,wx.ALIGN_CENTER|wx.ALIGN_RIGHT, 5)
        self.m_button2.Bind(wx.EVT_BUTTON, self.ViewDoctor)

        self.m_button3 = wx.Button(self.FrontPanel, wx.ID_ANY, u"Engineers", wx.DefaultPosition, wx.DefaultSize)
        self.gSizer1.Add(self.m_button3,0,wx.ALIGN_CENTER|wx.ALIGN_LEFT|wx.ALIGN_BOTTOM, 5)
        self.m_button3.Bind(wx.EVT_BUTTON, self.ViewEngineers)

        self.m_button4 = wx.Button(self.FrontPanel, wx.ID_ANY, u"Simulation", wx.DefaultPosition, wx.DefaultSize)
        self.gSizer1.Add(self.m_button4,0,wx.ALIGN_CENTER|wx.ALIGN_BOTTOM, 5)
        self.m_button4.Bind(wx.EVT_BUTTON, self.ViewSimulation)
        
        self.FrontPanel.SetSizerAndFit(self.gSizer1)
        self.FrontPanel.Layout()
        
        self.Centre(wx.BOTH)
        self.FrontPanel.Show()
        

    def ViewPatient(self, event):
        print"has successfully entered in the view patient"
        self.Hide()
        patient = PatientPanel()
        patient.Show()
        
    
    def ViewDoctor(self, event):
        print"has successfully entered in the view Doctor"
        self.Hide()
        doctor = DoctorPanel()
        doctor.Show()
		
    def ViewEngineers(self,event):
        print"has successfully entered in the view Engineer"
        self.Destroy()
        self.FrontPanel.Hide()
        self.EngineerView = EngineerPanel()
        self.EngineerView.Show()

    def ViewSimulation(self, event):
        print"has successfully entered in the view Simulation"
        self.Destroy()
        self.FrontPanel.Hide()
        self.SimulationView = SimulationPanel()
        self.SimulationView.Show()
        
        


if __name__ == "__main__":
    app = wx.App()
    frame = FrontPage()
    frame.Show()
    app.MainLoop()
