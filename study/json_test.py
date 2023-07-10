import json

file_path = "./config/oem2.json"

with open(file_path) as file:
    data = json.load(file)
    json_test = data['OEM']
    
    # print(json_test[0]['vehicles'][0]['name'])
    # print(json_test[0]['vehicles'][1]['name'])
    print (json_test[0]['vehicles'][0]['name']) 
    print (json_test[0]['vehicles'][1]['name']) 
    
    
# for k in json_test:
    # for i in range(0,2):
    #     print(k['vehicles'][i]['name'])
    #     Test = k['vehicles'][i]['name']
        # print(Test[0])
    # list1 = (k['vehicles'][0]['name'])
    # list2 = (k['vehicles'][1]['name'])
    # list3 = list1 + list2
    # print(list3)
        
    # for vehicle in k['vehicles']:
    #     test = vehicle['name']
        # print(test[1])

    # for i,e in enumerate(json_test):
    #     # print(i, e['vehicles'][1]['can1'])
    #     print(i, e['vehicles'][0]['can1'])
    
    
import pandas as pd

# a = pd.read_csv('./data.csv',usecols =['x'])
# b = pd.read_csv('./data.csv',usecols =['y'])

# df =  pd.read_csv('./data.csv')
# # print(df.loc[:,['x','y']])

# x= df.loc[:,'x']
# y= df.loc[:,'y']
# for i in range(len(x)):
#     array = [x[i],y[i]]
#     # print(x[i], y[i])
