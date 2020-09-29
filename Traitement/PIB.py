import pandas as pd
import json



def PibProcess(df):
 
    data_json = {}
    data_info = []
    df = df.loc[df['LOCATION'] == 'FRA']   
    
    
    last_value = round(597.208,3)
    for _index, line in df.iterrows():
        last_value = round((float(line['Value'])/100 + 1) * last_value ,3)
        
        data_info.append({ 'Time' :  line['TIME'], 'Var Trim' :  line['Value'], 'PIB Trim' :  last_value})
    
    data_json = data_info
               
    with open('../JSON/PIB.json', 'w') as json_file:
        json.dump(data_json, json_file, indent=4) 

df = pd.read_csv('../DataSet/PIB.csv', low_memory=False)
PibProcess(df)
    