import xlrd
import math



def TableData(age,race,bmi,sys_blood,dias_blood,heart_attack,stroke,heart_failure,kidney_disease,diabetes,smoking,artery_disease,vascular_disease,cholesterol,genetic,life_change,code,drinking):
    my_data=[age,race,bmi,sys_blood,dias_blood,heart_attack,stroke,heart_failure,kidney_disease,diabetes,smoking,artery_disease,vascular_disease,cholesterol,genetic,life_change, code,drinking]
    new_array =[18.0]*18
    final_value =[5.0]*5
    value =0.0
    conclusion =0
    workbook = xlrd.open_workbook('forJaredFictionTable.xlsx')
    my_answer = 400
    worksheet = workbook.sheet_by_name('Sheet1')


    for i in range(1,6):
        for j in range(1,19):
            jared = worksheet.cell(i,j).value
           
            jared = int(jared)
            
            
            new_array[j-1] = pow((my_data[j-1]-jared),2)
           
        for k in range(0,18):
            
            value += new_array[k]
        

        final_value[i-1] = math.sqrt(value)
        value=0
        
    #for i in range(0,5):
     #   print final_value[i]
    for result in range(0,5):
        if (my_answer >= final_value[result]):
            my_answer = final_value[result]
            conclusion = result
           
    
   
    return FindResult(conclusion)
    
def FindResult(conclusion):
    if conclusion == 0:
        return 'very good'
    if conclusion == 1:
        return 'good'
    if conclusion == 2:
        return 'average'
    if conclusion == 3:
        return 'bad'
    if conclusion == 4:
        return 'very bad'
    
    
            
            
            
       
        
    
