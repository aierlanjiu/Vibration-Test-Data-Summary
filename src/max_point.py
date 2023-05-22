
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import os
from tqdm import tqdm
import numpy as np
from scipy.stats import t
import re


# 设置警告阈值为0，禁用警告
mpl.rcParams['figure.max_open_warning'] = 0   
# 定义要处理的文件夹路径
folder_path = 'root\\result\\rds_value'

colors_runup = {"15Nm": "blue", "31Nm": "orange", "50Nm": "yellow","66Nm":"brown", "100Nm":"red", "200Nm":"green", "310Nm":"purple"}
colors_rundown = {"15Nm": "green", "31Nm": "purple", "50Nm": "orange","66Nm":"yellow", "-137Nm":"red", "-206Nm":"blue"}
# 获取所有xlsx文件的文件名
xlsx_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

# 遍历指定路径下的所有xlsx文件
for filename in tqdm(xlsx_files):
    if filename.endswith(".xlsx"):
        # 读取Excel文件
        excel_file = pd.ExcelFile(os.path.join(folder_path, filename))
    if "run up" in filename:        
        colors = colors_runup
    # Check if the filename contains "run down"
    elif "run down" in filename:       
        colors = colors_rundown
    all_data = pd.read_excel(os.path.join(folder_path, f"{os.path.splitext(filename)[0]}.xlsx"))

    grouped_max = all_data.groupby(["Test Point", "Torque", "Max Vibration Speed"]).agg({"Max Vibration": "max"})
    grouped_max = grouped_max.reset_index()
    grouped_max.columns = ["Test Point", "Torque", "Max Vibration Speed", "Max Vibration"]
    grouped_by_testpoint = grouped_max.groupby("Test Point")
    # 将数据按照 Max Vibration Speed 值分类
    bins = [500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    labels = [f"{i}-{j}" for i, j in zip(bins[:-1], bins[1:])]
    grouped_max["Speed Category"] = pd.cut(grouped_max["Max Vibration Speed"], bins=bins, labels=labels)

    grouped_by_speed = grouped_max.groupby(["Speed Category"])




    for speed, data in grouped_by_speed:
        
        speed1 = str(speed)
        speed1 = re.sub(r'[^\w\s]','_',speed1)
        plt.figure(figsize=(12, 8))
        sns.jointplot(data=data, x="Max Vibration Speed", y="Max Vibration", hue="Torque", markers=["o", "s", "D", "^", "v", "P", "X"])
        plt.legend(title="Torque", loc="upper left")
        plt.subplots_adjust(top=0.9)
        plt.suptitle(f"Max Speed Scatter and Marginal Plot for {speed1}", fontsize=8)
        plt.grid(color='#D3D3D3')
        plt.savefig(os.path.join('root\\result\\visualization\\05 Max Vibration and Max Vibration Speed Margnial', f"{os.path.splitext(filename)[0]}_max_plot_{speed1}.png"))
        #plt.show()
        plt.close

    
    # 按照Test Point、Torque和Max Vibration Speed列进行分组，并计算每个组的均值、标准差和用单个标准差计算的均值的95%置信区间上下边界
    grouped_max_mean = all_data.groupby(["Test Point", "Torque", "Max Vibration Speed"])["Max Vibration"].agg(["mean", "std"])

    # 将计算出的结果按照Test Point、Torque和Max Vibration Speed保存并合并为一组数据
    grouped_max_mean = grouped_max_mean.reset_index()
    grouped_max_mean.columns = ["Test Point", "Torque", "Max Vibration Speed", "Mean max", "Standard Deviation"]

    # 按照Test Point进行分组
    grouped_by_testpoint_mean = grouped_max_mean.groupby("Test Point")



    # 遍历每个Test Point，绘制分类散点图和分类区间图
    for testpoint, data in grouped_by_testpoint_mean:
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.scatterplot(data=data, x="Max Vibration Speed", y="Mean max", hue="Torque", style="Torque", ax=ax, palette="Set1", s=90)
        plt.title(f"max Mean and Confidence Interval for {testpoint}")
        plt.xlabel("Max Vibration Speed")
        plt.ylabel("Mean max")
        plt.xlim(0, 10000)
        plt.xticks(np.arange(0, 10001, 1000))
        plt.ylim(60, 170)
        plt.yticks(np.arange(60, 171, 10))
        plt.legend(title="Torque", loc="upper left")

        
        testpoint_clean = re.sub(r'[^\w\s]','',testpoint)
        plt.grid(color='#D3D3D3') # 添加透明色网格
        plt.savefig(os.path.join('root\\result\\visualization\\04 Max mean for prototypes', f"{os.path.splitext(filename)[0]}_max_plot_{testpoint_clean}.png"))
        #plt.show()
        plt.close