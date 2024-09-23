#-----------------------------------#
#Developed by Zetian and Zheng
#Data 2022.5
#Function: get data from files
#----------------------------------#
import os
from pandas import DataFrame
import pandas as pd
import re

lines0 = input('What is the solving name? ')
Var_name = ["Partial pressure", "Average loading absolute [milligram/gram framework]"]
Comp_num = int(input('Components number? '))
Var_state = 0

pressure_list = os.listdir(lines0)
pnum = len(pressure_list)

# 初始化输出数据结构
out_data = [[] for _ in range(len(Var_name) * Comp_num + 4)]
delete_num = 8  # 确认文件夹中无用文件数量

for i in range(pnum):
    path_now = os.path.join(lines0, pressure_list[i])
    temp_list = os.listdir(path_now)
    
    for temp_item in temp_list:
        path_temp = os.path.join(path_now, temp_item)
        sample_list = os.listdir(path_temp)[0:len(os.listdir(path_temp))-delete_num]
        
        for sample in sample_list:
            path_sample = os.path.join(path_temp, sample)
            out_data[0].append(pressure_list[i])
            out_data[1].append(temp_item)
            out_data[2].append(sample)
            
            # 检查 Output 文件夹
            if 'Output' in os.listdir(path_sample):
                output_path = os.path.join(path_sample, 'Output', 'System_0')
                filenames = os.listdir(output_path)
                
                for In, file in enumerate(filenames):
                    with open(os.path.join(output_path, file), 'rb') as f:
                        if In > 0:
                            out_data[0].append(pressure_list[i])
                            out_data[1].append(temp_item)
                            out_data[2].append(sample)
                        out_data[3].append(file)
                        
                        lines = f.readlines()
                        for m, var in enumerate(Var_name):
                            for line in lines:
                                if var.encode() in line:
                                    loc_num1 = re.search(r'\d', str(line)).span()
                                    if Var_state < Comp_num:
                                        out_data[Comp_num * m + Var_state + 4].append(
                                            str(line)[loc_num1[0]:len(str(line))-3])
                                        Var_state += 1
                                    
                            if Var_state == 0:
                                for n in range(Comp_num):
                                    out_data[Comp_num * m + n + 4].append('No this Variables')
                            elif Var_state < Comp_num:
                                for n in range(Comp_num - Var_state):
                                    out_data[Comp_num * m + Var_state + n + 4].append('No this Variables')
                                Var_state = 0
                            else:
                                Var_state = 0
            else:
                out_data[3].append('No Output fold')
                for m in range(len(Var_name)):
                    for n in range(Comp_num):
                        out_data[Comp_num * m + n + 4].append('No Output')

# 生成 DataFrame 并导出为 Excel
Var_name_real = [f'{var}_Comp.{i+1}' for var in Var_name for i in range(Comp_num)]
tot_name = ["Pressure", "Temperature", "Sample Name", "Filename"] + Var_name_real
out_data = list(map(list, zip(*out_data)))  # 转置

zaa = pd.DataFrame(out_data, columns=tot_name)
zaa.to_excel('MOF.xlsx', index=False)

print("finished")
