import pandas as pd
import json
import openpyxl

def ChomageProcess(sheet):
    
    
    dict_data = {}
    step =  51
    row = 29
      
    col_start = 2
    col_end = 10
    
    date_list = ['2019-11', '2019-12', '2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06', '2020-07']
    age_list = ['Total', 'Less than 25 years', 'From 25 to 74 years']     
    unit_list = ['Tousand Persons', 'Percentage of active population' ]
    sex_list = ['Total', 'Males', 'Females'] 
    
    for date in date_list:
        dict_data[date] = {}
        for age in age_list:
            dict_data[date][age] = {}
    
    for age in age_list:
        for unit in unit_list:
            for sex in sex_list:
                if unit != 'Percentage of active population':
                    for col in range(col_start, col_end+1):
                        dict_data[date_list[col-col_start]][age][sex] = sheet.cell(row=row, column=col).value

                row = step + row
                
    data_json = []
    for date, info_date in dict_data.items():
        row_data = {}
        row_data['Date'] = date
        row_data['Unit'] = 1000
        list_for_age = []
        for age, info_age in info_date.items():
            male_p = round((float(info_age['Males'])/float(info_age['Total'])),2)
            female_p = round(1 - male_p, 2)
            list_for_age.append({
                'Age' : age,
                'Total' : info_age['Total'],
                'Males percentage' : male_p,
                'Females percentage' : female_p
            })
        
        row_data['Data'] = list_for_age
        data_json.append(row_data)
        

    with open('../JSON/Chomage.json', 'w') as json_file:
       json.dump(data_json, json_file, indent=4) 




book = openpyxl.load_workbook('../DataSet/Chomage.xlsx')
sheet = book.active
ChomageProcess(sheet)
    