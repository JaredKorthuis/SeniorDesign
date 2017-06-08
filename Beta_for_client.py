import wx
import os
import wx.xrc
import wx.lib.agw.multidirdialog as MDD
import ConfigParser
import wx.richtext as rt
import wx.animate as animate
import sys
import numpy as np
from numpy import arange, sin, pi
import matplotlib
import traceback
matplotlib.use('WX')
from matplotlib.backends.backend_wx import FigureCanvasWx as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx

from matplotlib.figure import Figure

import wx.lib.mixins.inspection as WIT
from jared_algorithm import TableData
from jared_save_data import Saving_File_Data

##############################
## MAINFRAME OF GUI
##############################
def scale_bitmap(bitmap, width, height):
        image = wx.ImageFromBitmap(bitmap)
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image)
        return result

class PageFour(wx.Panel):
    
    
    instance = None
    init =0
    """This allows only one instance to happen on this panel"""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.init=1
        self.setLocal()
        
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
        self.boxTop.Add(self.quote, 0, wx.ALIGN_TOP)

       
        self.m_buttonVelocity = wx.Button(self, label="Velocity")
        self.boxTop2.Add(self.m_buttonVelocity, 0, wx.ALIGN_TOP)
        self.m_buttonVelocity.Bind(wx.EVT_BUTTON, self.VelocityClick)

        
        self.m_buttonVal2 = wx.Button(self, label="Smallest Diameter")
        self.boxTop2.Add(self.m_buttonVal2, 0, wx.ALIGN_TOP)
        self.m_buttonVal2.Bind(wx.EVT_BUTTON, self.Val2Click)

        self.gifs=["velocity = .4, output pressure.gif","vinitial = 1, output pressure.gif","vinitial =.6, output pressure.gif","vinitial = .4, output deformation.gif","vinitial = 1, output deformation.gif","vinitial = .4, output velocity.gif","vinitial = 1, output velocity.gif","vinitial=.6, output velocity.gif"]
        self.my_combo=wx.ComboBox(self,-1,choices=self.gifs, style=wx.CB_READONLY)
        self.my_combo.Bind(wx.EVT_COMBOBOX,self.OnSelect)

        self.gif_name ='velocity = .4, output pressure.gif'
        #self.gif_name =wx.Image('bob.gif',wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        #self.gif_name = scale_bitmap(self.gif_name,400,400)
        #self.gif_bitmap = wx.StaticBitmap(self,-1,self.gif_name,(10,5), (self.gif_name.GetWidth(),self.gif_name.GetHeight()))
        self.gif = animate.GIFAnimationCtrl(self,1, self.gif_name,size=(720,500))
        #self.gif_name =wx.Image('bob.gif',wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        #self.gif_name = scale_bitmap(self.gif_name,900,900)
        
        
        
        
               
        self.boxMiddle2.Add(self.gif, 0, wx.EXPAND|wx.ALL)
        self.gif.Play()
        self.png2 = wx.Image(os.getcwd()+"\High_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
       
        self.png2 = scale_bitmap(self.png2, 425, 450)
        self.image2 = wx.StaticBitmap(self, -1, self.png2, (10, 5), (self.png2.GetWidth(), self.png2.GetHeight()))
        
        self.boxMiddle2.Add(self.image2, 0, wx.EXPAND|wx.ALL)

        self.quote5 = wx.StaticText(self, label="Velocity: ")
        self.boxLeft.Add(self.quote5, 0, wx.ALIGN_CENTER)

        self.textBox1 = wx.TextCtrl(self,-1,"Velocity")
        self.boxLeft.Add(self.textBox1, 5, wx.EXPAND|wx.ALL)

        self.quote6 = wx.StaticText(self, label="Smallest Diameter: ")
        self.boxLeft.Add(self.quote6, 0, wx.ALIGN_CENTER)

        self.textBox2 = wx.TextCtrl(self,-1,"Smallest Diameter")
        self.boxLeft.Add(self.textBox2, 5, wx.EXPAND|wx.ALL)

       

        self.number_of_gifs =2
        """Adding the buttons and static texts into alignment on panel"""
        self.final_box_h=wx.BoxSizer(wx.HORIZONTAL)
        final_box = wx.BoxSizer(wx.VERTICAL)
        final_box.Add(self.boxTop,0,wx.ALIGN_TOP|wx.EXPAND)
        final_box.Add(self.boxTop2,0,wx.ALIGN_TOP|wx.ALIGN_LEFT|wx.EXPAND)
        final_box.Add(self.my_combo,0,wx.ALIGN_CENTER)
        final_box.Add(self.boxLeft,0,wx.ALIGN_TOP|wx.ALIGN_LEFT|wx.EXPAND)
        #final_box.Add(self.boxMiddle,0,wx.ALIGN_CENTER|wx.ALIGN_LEFT|wx.EXPAND)
        final_box.Add(self.boxMiddle2,0,wx.ALIGN_CENTER|wx.ALIGN_RIGHT|wx.EXPAND)

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
        self.png2 = wx.Image(os.getcwd()+"\Low_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.png2 = scale_bitmap(self.png2, 300, 80)
        self.image2.SetBitmap(self.png2)
        self.Update()
    def Val2Click(self,event):
        print"has successfully pressed Val2"
        value = int(self.textBox2.GetValue())
        if (value > 5):
            print"Val2 1"
            self.png1 = wx.Image(os.getcwd()+"\Low_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.png1 = scale_bitmap(self.png1, 300, 150)
            self.image1.SetBitmap(self.png1)
        elif (value >= 2) and (value <= 5):
            print"Val2 2"
            self.png1 = wx.Image(os.getcwd()+"\Normal_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.png1 = scale_bitmap(self.png1, 300, 150)
            self.image1.SetBitmap(self.png1)
        elif (value < 2):
            print"Val2 3"
            self.png1 = wx.Image(os.getcwd()+"\High_Blood_Pressure.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.png1 = scale_bitmap(self.png1, 300, 150)
            self.image1.SetBitmap(self.png1)
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

        
        races_available = ['African', 'Hispanic', 'Asian', 'Indian', 'Caucasian']

        feet = ['3','4','5','6','7']
        inches = ['0','1','2','3','4','5','6','7','8','9','10','11']
        

        
        self.race_text= wx.StaticText(self,-1,u"Race")
        text3_horizontal.Add(self.race_text)
        self.race_text.SetFont(font)
        
        text3_horizontal.AddSpacer(5)
        self.race = wx.ComboBox(self,value="your race?",choices=races_available)
        text3_horizontal.Add(self.race,wx.ALL)
        
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
        self.setLocale()
         
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


        self.good_final_sizer.Add(self.good_sub_horizontal,0,wx.ALIGN_TOP)
        
        self.good_final_sizer.Add(self.good_horizontal_box,0,wx.ALIGN_CENTER)
        
     
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
        
        BadText = wx.StaticText(self.panelBad,0,u"Your blood pressure is not healthy. You might have one of these issues")
     
        self.bad_title_box.Add(BadText,wx.EXPAND|wx.ALL)
       
        BadText.SetFont(font)
        
        hyper_tension_text = wx.StaticText(self.panelBad,-1,"You might have Hypertension                                           or Hypotension")
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
        
        
       
        
        self.bad_final_box_sizer.Add(self.bad_title_box, wx.ALIGN_TOP|wx.ALL)
        self.bad_final_box_sizer.AddSpacer(25)
        self.bad_final_box_sizer.Add(self.bad_vertical_box_sizer,wx.ALIGN_CENTER|wx.ALL)
        
        self.bad_final_box_sizer_hor.Add(self.bad_final_box_sizer,0,wx.ALL|wx.ALIGN_CENTER)
       
        

#########THIS IS THE AVERAGE HEALTH DISPLAY#######################################
        self.avg_title_box = wx.BoxSizer(wx.VERTICAL)
        self.avg_horizontal_box = wx.BoxSizer(wx.HORIZONTAL)
        self.avg_vertical_box = wx.BoxSizer(wx.VERTICAL)
        self.avg_final_box_sizer = wx.BoxSizer(wx.VERTICAL)
        self.avg_sub_horizontal_box_bottom_avg = wx.BoxSizer(wx.HORIZONTAL)
        self.avg_text = wx.StaticText(self.panelAvg,0,u"Your blood pressure is average. Here is some advice on how to improve")
        
        
        self.avg_title_box.Add(self.avg_text,wx.ALL)
        self.avg_text.SetFont(font)

        avg_image1 = wx.Image("avg_heart_info_1.jpg",wx.BITMAP_TYPE_ANY)
        avg_image2 = wx.Image("blood_pressure_graph.jpg",wx.BITMAP_TYPE_ANY)
        
        self.avg_text_img = wx.StaticText(self.panelAvg,-1,"Your Diet might have to change  ")
        self.avg_text_img.SetFont(font)
        self.avg_title_box.Add(self.avg_text_img,0,wx.ALL)

        
        self.avg_image1 = avg_image1.Scale(250,250)
        self.avg_image2 = avg_image2.Scale(500,300)

        self.imageCtrl  = wx.StaticBitmap(self.panelAvg, wx.ID_ANY,wx.BitmapFromImage(self.avg_image1))
        self.imageCtrl2 = wx.StaticBitmap(self.panelAvg, wx.ID_ANY, wx.BitmapFromImage(self.avg_image2))

        
        self.avg_horizontal_box.Add(self.imageCtrl,0,wx.ALIGN_CENTER | wx.ALL)
        self.avg_horizontal_box.Add(self.imageCtrl2, 0, wx.ALIGN_CENTER | wx.ALL,border=5)
        self.avg_vertical_box.Add(self.avg_horizontal_box,-1,wx.ALL)


        


        self.avg_final_box_sizer.Add(self.avg_title_box,0,wx.ALL)
        
        self.avg_final_box_sizer.Add(self.avg_horizontal_box,0,wx.ALL|wx.EXPAND|wx.ALIGN_CENTER)
        
        
       
        
        
###########################DEFINITIONS###################################################        
    def setLocale(self):
        locale = wx.Locale(wx.LANGUAGE_ENGLISH)
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
        self.setLocal()
        
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
        self.avg_text = wx.StaticText(self.panelAvg,0,u"Your Heart is getting close to needing surgery")
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
               
        self.avg_image1 = avg_image1.Scale(400,400)
       

        self.imageCtrl  = wx.StaticBitmap(self.panelAvg, wx.ID_ANY,wx.BitmapFromImage(self.avg_image1))
       
        self.avg_vertical_box_right.Add(self.imageCtrl,0,wx.ALIGN_RIGHT | wx.ALL|wx.EXPAND|wx.RIGHT)
       
              
        self.avg_horizontal_box.Add(self.avg_vertical_box,0,wx.ALL|wx.EXPAND)
        self.avg_horizontal_box.AddSpacer(60)
        self.avg_horizontal_box.Add(self.avg_vertical_box_right,0,wx.ALL|wx.EXPAND)
        self.final_vert_box = wx.BoxSizer(wx.VERTICAL)
        self.final_vert_box.Add(self.avg_horizontal_box,wx.ALL|wx.EXPAND|wx.ALIGN_CENTER)
        self.avg_final_box_sizer.AddSpacer(45)
        self.avg_final_box_sizer.Add(self.avg_title_box,0,wx.ALL|wx.ALIGN_CENTER|wx.ALIGN_TOP)
        self.avg_final_box_sizer.Add(self.final_vert_box,0,wx.ALL|wx.ALIGN_CENTER)
        self.avg_final_box_sizer.AddSpacer(20)
        
        
############################AVERAGE HEART FOR NEEDING FULL REPLACEMENT#########################################
        self.avgreplace_title_box = wx.BoxSizer(wx.VERTICAL)
        self.avgreplace_horizontal_box = wx.BoxSizer(wx.HORIZONTAL)
        self.avgreplace_vertical_box = wx.BoxSizer(wx.VERTICAL)
        self.avgreplace_vertical_box_right = wx.BoxSizer(wx.VERTICAL)
        self.avg_replace_final_box_sizer = wx.BoxSizer(wx.VERTICAL)
        self.avgreplace_sub_horizontal_box_bottom_avg = wx.BoxSizer(wx.HORIZONTAL)
        self.avgreplace_text = wx.StaticText(self.panelAvgReplace,0,u"Your Heart is getting close to needing surgery")
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
        
        self.avgreplace_image1 = avgreplace_image1.Scale(400,400)
       

        self.imageCtrlReplace  = wx.StaticBitmap(self.panelAvgReplace, wx.ID_ANY,wx.BitmapFromImage(self.avgreplace_image1))
        
        
        self.avgreplace_vertical_box_right.Add(self.imageCtrlReplace,0,wx.ALIGN_RIGHT | wx.ALL|wx.EXPAND|wx.RIGHT)
        

             
        self.avgreplace_horizontal_box.Add(self.avgreplace_vertical_box,0,wx.ALL|wx.EXPAND)
        self.avgreplace_horizontal_box.AddSpacer(60)
        self.avgreplace_horizontal_box.Add(self.avgreplace_vertical_box_right,0,wx.ALL|wx.EXPAND)
        self.finalreplace_vert_box = wx.BoxSizer(wx.VERTICAL)
        self.finalreplace_vert_box.Add(self.avgreplace_horizontal_box,wx.ALL|wx.EXPAND|wx.ALIGN_CENTER)
        self.avg_replace_final_box_sizer.AddSpacer(45)
        self.avg_replace_final_box_sizer.Add(self.avgreplace_title_box,0,wx.ALL|wx.ALIGN_CENTER|wx.ALIGN_TOP)
        self.avg_replace_final_box_sizer.Add(self.finalreplace_vert_box,0,wx.ALL|wx.ALIGN_CENTER)
        self.avg_replace_final_box_sizer.AddSpacer(20)
        
#########################HEART  REPLACEMENT###########################################################

        self.badheart_title_box = wx.BoxSizer(wx.VERTICAL)
        self.badheart_horizontal_box = wx.BoxSizer(wx.HORIZONTAL)
        self.badheart_vertical_box = wx.BoxSizer(wx.VERTICAL)
        self.badheart_vertical_box_right = wx.BoxSizer(wx.VERTICAL)
        self.bad_final_box_sizer = wx.BoxSizer(wx.VERTICAL)
        self.badheart_sub_horizontal_box_bottom_avg = wx.BoxSizer(wx.HORIZONTAL)
        self.badheart_text = wx.StaticText(self.panelBadHeart,0,u"Your Heart may need to be completely replaced")
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
        
        
        self.badheart_image1 = badheart_image1.Scale(400,200)
        self.badheart_image2 = badheart_image2.Scale(400,200)

        self.imageCtrlbadheart  = wx.StaticBitmap(self.panelBadHeart, wx.ID_ANY,wx.BitmapFromImage(self.badheart_image1))
        self.imageCtrl2badheart = wx.StaticBitmap(self.panelBadHeart, wx.ID_ANY, wx.BitmapFromImage(self.badheart_image2))

    
        self.badheart_vertical_box_right.Add(self.imageCtrlbadheart,wx.ALL|wx.ALIGN_CENTER)
        self.badheart_vertical_box_right.Add(self.imageCtrl2badheart,wx.ALL|wx.ALIGN_CENTER)
        self.Refresh()
        

        
      
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

        self.badvalve_text = wx.StaticText(self.panelBadValve,0,u"Your Heart may need to have a valve replacement")
        with open('bad_heart_replace.txt') as MyInfo:
            data="".join(line.rstrip() for line in MyInfo)
        
        #self.badvalve_final_box_sizer.Add(self.badvalve_text,wx.ALL|wx.ALIGN_TOP|wx.EXPAND)
        self.badvalve_text.SetFont(font)
        
        self.badvalve_information = rt.RichTextCtrl(self.panelBadValve, value='',style=wx.VSCROLL|wx.NO_BORDER|wx.TE_READONLY,size=(400,500))
        self.badvalve_information.WriteText(data)
        self.badvalve_information.SetFont(font2)
        self.badvalve_horizontal_box.Add(self.badvalve_information,wx.EXPAND|wx.ALL)
        
        badvalvehyp_link = wx.HyperlinkCtrl(self.panelBadValve,-1,url="http://www.heart.org/HEARTORG/Conditions/More/HeartValveProblemsandDisease/Options-for-Heart-Valve-Replacement_UCM_450816_Article.jsp#.VvsJ0vlViko",label="For more information click on me")
        
        Img = wx.Image("artificial_heart_bad_valve.jpg",wx.BITMAP_TYPE_ANY)
        
        self.Bad_valve_img = Img.Scale(400,200)
        
        self.imageCtrlbadheartvalve  = wx.StaticBitmap(self.panelBadValve, wx.ID_ANY,wx.BitmapFromImage(self.Bad_valve_img))

        self.badvalve_horizontal_box.Add(self.imageCtrlbadheartvalve,wx.ALL|wx.EXPAND)

        self.badvalve_final_box_sizer.Add(self.badvalve_text,0,wx.EXPAND|wx.ALL)
        self.badvalve_final_box_sizer.Add(self.badvalve_horizontal_box,0,wx.EXPAND|wx.ALL)
        self.badvalve_final_box_sizer.Add(badvalvehyp_link,0,wx.EXPAND|wx.ALL)



        self.panelBadValve.SetSizerAndFit(self.badvalve_final_box_sizer)
        self.panelBadValve.SetSizerAndFit(self.badvalve_final_box_sizer)
        self.panelBadValve.Layout()
        
        
	
    def setLocal(self):
        locale = wx.Locale(wx.LANGUAGE_ENGLISH)
    
        
        
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
        locale = wx.Locale(wx.LANGUAGE_ENGLISH)
        self.init=1
        wx.Frame.__init__(self,None, title="Blood Pressure and comparisons", size=(830,650))
        
        # Here we create a panel and a notebook on the panel
        self.p = wx.Panel(self)
        self.nb = wx.Notebook(self.p)
        
        # create the page windows as children of the notebook
        page1 = PageOne(self.nb)
        page2 = PageTwo(self.nb)
        page3 = PageThree(self.nb)
        page4 = PageFour(self.nb)
       
        # add the pages to the notebook with the label to show on the tab
        self.nb.AddPage(page1, "Patient education")
        self.nb.AddPage(page2, "Heart Condition")
        self.nb.AddPage(page3, "Artificial Heart Education")
        self.nb.AddPage(page4, "Simulation")
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


        
        


if __name__ == "__main__":
    app = wx.App()
    frame = DoctorPanel()
    frame.Show()
    app.MainLoop()
