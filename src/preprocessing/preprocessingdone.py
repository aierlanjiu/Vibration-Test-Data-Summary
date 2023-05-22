#这段代码实现了对多个Excel文件中的数据进行读取、处理的功能。具体步骤包括：

#检查指定路径下所有的Excel文件，并遍历每个文件中的sheet。
#对于每个包含所需“Curve”列的sheet，根据扭矩和振动测试点分别建立新的sheet。
#将所有的RMS计算结果存储在一个DataFrame中，并按Serial、test Point、Torque和RMS Index进行排序。

#注意事项：

#需要先安装tqdm、numpy、scipy、matplotlib、pandas和seaborn等库，才能运行该代码。
#在运行程序前，需要先将要处理的Excel文件都放在同一个文件夹下，并将该文件夹路径赋给变量folder_path。
#在代码中使用了一些硬编码的参数，如Curve列的不同字符、振动测试点等，请根据实际情况修改。



import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from tqdm import tqdm
import numpy as np
from scipy.stats import norm
import re



# 定义要查找的“Curve”列中的不同字符
curve_characters_torque_runup = ["15Nm", "31Nm", "50Nm", "66Nm", "100Nm", "200Nm", "310Nm"]
curve_characters_torque_rundown = ["15Nm", "31Nm", "66Nm", "50Nm", "-137Nm","-206Nm"]
colors_runup = {"15Nm": "blue", "31Nm": "orange", "50Nm": "yellow","66Nm":"brown", "100Nm":"red", "200Nm":"green", "310Nm":"purple"}
colors_rundown = {"15Nm": "blue", "31Nm": "orange", "50Nm": "yellow","66Nm":"brown", "-137Nm":"red", "-206Nm":"green"}
curve_characters_testpoint = ["input shaft:+Y", "middle shaft:+X",
                              "middle shaft:+Y", "middle shaft:+Z", "top:+X", "top:+Y", "top:+Z"]


# 定义要处理的文件夹路径
folder_path = 'root\\data\\cleaned_data'
# Define the possible values of curve_characters_torque
# 获取所有xlsx文件的文件名
xlsx_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

# 遍历指定路径下的所有xlsx文件
for filename in tqdm(xlsx_files):
    if filename.endswith(".xlsx"):
        # 读取Excel文件
        excel_file = pd.ExcelFile(os.path.join(folder_path, filename))
    # Check if the filename contains "run up"
    if "run up" in filename:
        curve_characters_torque = curve_characters_torque_runup
        colors = colors_runup
    # Check if the filename contains "run down"
    elif "run down" in filename:
        curve_characters_torque = curve_characters_torque_rundown
        colors = colors_rundown
    # If neither "run up" nor "run down" is present in the filename, skip this file
    else:
        continue


    # 创建一个空的DataFrame，用于存储所有的RMS均值和置信区间
    all_data = pd.DataFrame()
    curves = set()
    for sheet_name in tqdm(excel_file.sheet_names):
        # 读取sheet数据
        sheet_df = pd.read_excel(excel_file, sheet_name=sheet_name)
        # 如果Curve列存在并且第一个元素包含空格
        if "Curve" in sheet_df.columns and " " in sheet_df["Curve"][0]:
            # 将第一个Curve拆分并获取倒数第4个元素
            curve_element = sheet_df["Curve"][0].split()[4]
            if 'run' not in curve_element:
                # 添加到curves集合中
                curves.add(curve_element)
                

    # 将curves转换为元组(tuple)
    curves_tuple = tuple(curves)
    print(curves_tuple)
    print(len(curves_tuple))
    

    for sheet_name in tqdm(excel_file.sheet_names, bar_format="{l_bar}{bar:30}{r_bar}{bar:-30b}", colour='green'):


        # 读取当前sheet的数据
        sheet_df = pd.read_excel(excel_file, sheet_name=sheet_name)

        # 检查当前sheet是否包含所需的“Curve”列
        if "Curve" not in sheet_df.columns:
            continue
        
        serial_sheet_name = "" # Initialize the variable to an empty string

        # 检查当前sheet的“Curve”列是否包含所需的字符
        if any(characters in str(sheet_df["Curve"][0]) for characters in curve_characters_torque):
            # 将当前sheet分为不同扭矩的sheet
            for torque in curve_characters_torque:
                if torque in str(sheet_df["Curve"][0]):
                    torque_sheet_name = f"{sheet_name}_{torque}"
                    # 将当前扭矩的sheet分为不同振动测试点的sheet
                    for testpoint in curve_characters_testpoint:
                        if testpoint in str(sheet_df["Curve"][0]):
                            testpoint_sheet_name = f"{torque_sheet_name}_{testpoint}"
                            for serial in curves_tuple:
                                # 按照减速器箱体分类
                                if serial in curves_tuple:
                                    serial_sheet_name = f"{serial_sheet_name}_{serial}"
                                    for i in range(len(sheet_df["RMS"])):
                                        # 计算RMS
                                        rms = sheet_df["RMS"][i]
                                        # 计算RMS索引
                                        rms_index = (sheet_df["Step Start Speed"][i] + sheet_df["Step End Speed"][i])/2
                                        max_vibration_value = sheet_df["Max Vibration"][i]
                                        max_vibration_speed = sheet_df["Max Vibration Speed"][i]
                                        start_speed = sheet_df["Step Start Speed"][i]
                                        stop_speed = sheet_df["Step End Speed"][i]
                                        start_v = sheet_df["start_v"][i]
                                        stop_v = sheet_df["stop_v"][i]
                                        # 将计算结果添加到all_rms DataFrame中
                                        new_data = pd.DataFrame({"Sheet Name": sheet_name, "Test Point": testpoint, "Torque": torque, "Serial":serial,
                                        "RMS Index": rms_index, "RMS": rms,"Max Vibration":max_vibration_value,"Max Vibration Speed":max_vibration_speed,
                                        "Step Start Speed":start_speed, "start_v":start_v, "Step End Speed":stop_speed, "stop_v":stop_v}, index=[0])
                                        all_data = pd.concat([all_data, new_data], ignore_index=True)

    # 将all_rms DataFrame中的数据按照Test Point、Torque和RMS Index进行排序
    all_data = all_data.sort_values(by=["Serial", "Test Point", "Torque", "RMS Index"])

    # 将all_rms DataFrame中的数据保存到Excel文件中
    all_data.to_excel(os.path.join('root\\result\\rds_value\\', f"{os.path.splitext(filename)[0]}_results.xlsx"), index=False)


