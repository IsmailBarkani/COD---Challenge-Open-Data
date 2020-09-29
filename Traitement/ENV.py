import pandas as pd
import json



def dataSetProcess2(df, code_dict, data_json, dataSet_dict1):
    
    dataSet_dict = {}
    date_list = ['2019-12', '2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06', '2020-07', '2020-08', '2020-09']
    
    for _index, line in df.iterrows():  
        if line['lib_zone'] not in dataSet_dict:
            dataSet_dict[line['lib_zone']] = {} 
            
        year_Month = line['date_ech'][0:7]
        year_Month = year_Month.replace('/', '-')
        
        if year_Month in date_list:
            if year_Month not in dataSet_dict[line['lib_zone']]:
                dataSet_dict[line['lib_zone']][year_Month] = []
                
            dataSet_dict[line['lib_zone']][year_Month].append(line['valeur'])
            
    for city, data_city in dataSet_dict.items():  
        if city not in dataSet_dict1:
            data_row = {}
            data_row['City'] = city
            data_row['code'] = code_dict[city]
            data_list = []
            for year_Month, list_value in data_city.items():
                data_list.append({
                        'Year_Month' : year_Month,
                        'ATMo' : int(sum(list_value)/len(list_value)) 
                    })
            
            data_row['Info']= sorted(data_list, key = lambda i: i['Year_Month']) 
            data_json.append(data_row)
            
    return data_json
                    
    
    
def get_ATMO(list_indice):
    border_indices =[
        [29, 54, 84, 109, 134, 164, 199, 274, 399],
        [29, 54, 79, 104, 129, 149, 179, 209, 239],
        [9, 19, 29, 39, 49, 64, 79, 99, 124],
        [39, 79, 119, 159, 199, 249, 299, 399, 499] ]
    
    result = [ 10, 10, 10, 10 ]
    for k in range(4):
        for  i, indice in enumerate(border_indices[k]):
            if list_indice[k] < indice :
               result[k] =  i + 1
               break
    
    
    atmo = max(result)
    return atmo


def dataSetProcess1(df, code_dict):
    
    dataSet_dict = {}
    df = df.loc[df['Country'] == 'FR']
    
    for city in set(df['City']):
        
        df_city = df.loc[df['City'] == city]
        
        for date in set(df_city['Date']):
            
            df_city_date = df_city.loc[df_city['Date'] == date]
            count_indices = 0
            line_city = {}
            for _index, line in df_city_date.iterrows():  
                if line['Specie']  in ['no2', 'o3', 'pm10', 'so2']:
                    line_city[line['Specie']] = line['median']
                    count_indices = count_indices + 1
                
            if  count_indices == 4:

                if city not in dataSet_dict:
                    dataSet_dict[city] = {}
                    
                if date[0:7] not in dataSet_dict[city]:
                    dataSet_dict[city][date[0:7]] = []
                    
                dataSet_dict[city][date[0:7]].append(line_city)
        
     
    
     

    
    data_json = []
    for city, city_value in dataSet_dict.items():  
        data_row = {}
        data_row['City'] = city
        data_row['code'] = code_dict[city]
        data_list = []
        
        for year_Month, list_values in city_value.items():
            
            n = len(list_values)
            city_ind = {}
          
            for sp  in ['no2', 'o3', 'pm10', 'so2']:
                city_ind[sp] = 0
           
            for indices in list_values:
                for sp, value in indices.items():
                    city_ind[sp] = city_ind[sp] + value
           
            for sp  in ['no2', 'o3', 'pm10', 'so2']:
                city_ind[sp] = (int)(city_ind[sp]/n)
            
           
            data_list.append({
                'Year_Month' : year_Month,
                'ATMo' : get_ATMO([city_ind['no2'], city_ind['o3'], city_ind['pm10'], city_ind['so2']]) 
            })
            
        data_row['Info']= sorted(data_list, key = lambda i: i['Year_Month']) 
        data_json.append(data_row)
        
    return data_json, dataSet_dict


def get_code_city():
    code_file = open('../DataSet/code_city.json', encoding="utf-8") 
    code_array = json.load(code_file)
    code_dict = {} 
    for item in code_array:
          code_dict[item['nom']] = item['code'] 
        
    return code_dict
    

df1 = pd.read_csv('../DataSet/environnement.csv', low_memory=False)

code_dict = get_code_city()

data_json, dataSet_dict1 = dataSetProcess1(df1, code_dict)

 
   
df2 = pd.read_csv('../DataSet/ind_hdf_agglo.csv', low_memory=False)
data_json = dataSetProcess2(df2, code_dict, data_json, dataSet_dict1)


with open('../JSON/Environnement_FR.json', 'w', encoding="utf-8") as json_file:
    json.dump(data_json, json_file, indent=4) 
