import wx
import os
import wx.lib.agw.multidirdialog as MDD
import ConfigParser





def Saving_File_Data(file_name,high_blood,low_blood,weight,feet,inch,race,age,heart_attk,stroke,heart_fail,kidney,diabetus,smoking,artery,vasc,chol,genes,life_change,zip_code,drinking):
    config = ConfigParser.RawConfigParser()
    config.add_section('Doctor')
    config.set('Doctor', 'high_blood',high_blood)
    config.set('Doctor', 'low_blood',low_blood)
    config.set('Doctor', 'weight', weight)
    config.set('Doctor', 'feet', feet)
    config.set('Doctor', 'inch', inch)
    config.set('Doctor', 'race', race)
    config.set('Doctor', 'age' , age)
    config.set('Doctor', 'heart_attk', heart_attk)
    config.set('Doctor', 'stroke', stroke)
    config.set('Doctor', 'heart_fail', heart_fail)
    config.set('Doctor', 'kidney', kidney)
    config.set('Doctor', 'diabetus', diabetus)
    config.set('Doctor', 'smoking', smoking)
    config.set('Doctor', 'artery', artery)
    config.set('Doctor', 'vasc', vasc)
    config.set('Doctor', 'chol', chol)
    config.set('Doctor', 'genes', genes)
    config.set('Doctor', 'life_change', life_change)
    config.set('Doctor', 'zip_code', zip_code)
    config.set('Doctor', 'drinking', drinking)

   
    with open(file_name, 'wb') as configfile:
        config.write(configfile)

    
    
