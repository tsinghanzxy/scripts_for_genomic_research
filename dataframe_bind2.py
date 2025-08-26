import pandas as pd
import re
import openpyxl
excel_file_path = '4个来源菌株 1vs.1 同源Pan基因（需合并）.xlsx'  #文件路径：非当前py目录格式按照'D:/python project/4个来源菌株 1vs.1 同源基因（需合并）.xlsx '格式
all_sheets = pd.read_excel(excel_file_path, sheet_name=None)
sheet_names = list(all_sheets.keys())
N = 6       #两两对比组数量:C(4,2)
n = 4       #不同组数量
tables = {}

for i in range(N):
    sheet_name = sheet_names[i]
    tables[sheet_name] = all_sheets[sheet_name]


data = {'Naturalwater':[],'Soil':[],'Clinical':[],'Coolingtower':[]}  #各组名字
data = pd.DataFrame(data)

def match(dataframe,group1,group2):
    formal_len1=len(data[group1])
    formal_len2=len(data[group2])
    group1=str(group1)
    group2=str(group2)
    data[group1] = data[group1].astype(str)
    data[group2] = data[group2].astype(str)
    for i in range(len(dataframe[group1])):
        if (dataframe[group1][i] in data[group1].values):
            position = data.index[data[group1] == dataframe[group1][i]].tolist()[0]
            data.at[position,group2]= dataframe[group2][i]
        elif (dataframe[group2][i] in data[group2].values):
            position = data.index[data[group2] == dataframe[group2][i]].tolist()[0]
            data.at[position,group1]= dataframe[group1][i]
        elif not (data[group1].str.contains(dataframe[group1][i], case=False).any()) :
            data.at[i+formal_len1,group1] = dataframe[group1][i]
            data.at[i+formal_len2,group2] = dataframe[group2][i]

for i in range(len(sheet_names)-1):
    match(tables[sheet_names[i]],tables[sheet_names[i]].columns[0],tables[sheet_names[i]].columns[1])

data.to_csv('output_with_num.csv')   #输出在当前py目录

df =pd.read_csv('output_with_num.csv')
df.iloc[:,1:(n+1)]=df.iloc[:,1:(n+1)].applymap(lambda x: re.sub(r'^\d+_', '', str(x)))
df.index = range(1,len(df)+1)
df=df.drop(df.columns[0], axis=1)
df=df.replace('nan'," ")
df.to_csv("output_without_num.csv",index=True)

