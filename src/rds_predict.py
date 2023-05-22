
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from tqdm import tqdm
import numpy as np
from scipy.stats import norm
import re

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
        cols = 4
    # Check if the filename contains "run down"
    elif "run down" in filename:       
        colors = colors_rundown
        cols = 3
    # 读取数据
    all_rms = pd.read_excel(os.path.join(folder_path, f"{os.path.splitext(filename)[0]}.xlsx"))

    

    # 按照Test Point、Torque和RMS Index列进行分组，并计算每个组的均值、标准差和用单个标准差计算的均值的95%置信区间上下边界
    grouped_rms = all_rms.groupby(["Test Point", "Torque", "RMS Index"])["RMS"].agg(
        ["mean", "std", lambda x: norm.interval(0.99379, loc=x.mean(), scale=x.std() / np.sqrt(len(x)))[1],
        lambda x: norm.interval(0.99379, loc=x.mean(), scale=x.std() / np.sqrt(len(x)))[0]])

    # 将计算出的结果按照Test Point、Torque和RMS Index保存并合并为一组数据
    grouped_rms = grouped_rms.reset_index()
    grouped_rms.columns = ["Test Point", "Torque", "RMS Index", "Mean RMS", "Standard Deviation", "upper_bound",  "lower_bound"]
    
    # 按照Test Point进行分组
    grouped_by_testpoint = grouped_rms.groupby("Test Point")



    # 遍历每个Test Point，绘制单扭矩单测点散点图和分类区间图
    for testpoint, data in grouped_by_testpoint:
        # 创建大图和子图
        fig, axs = plt.subplots(nrows=2, ncols=cols, figsize=(28, 16))
        axs = axs.reshape(-1)

        for i, (torque, color) in enumerate(colors.items()):
            if i >= 7:
                break
            torque_data = data[data["Torque"] == torque]
            sns.scatterplot(data=torque_data, x=torque_data["RMS Index"], y=torque_data["Mean RMS"], hue="Torque", style="Torque", ax=axs[i], s=40)
            axs[i].set_title(f"RMS Mean and Confidence Interval for {torque}", fontdict={'fontsize': 16})
            axs[i].set_xlabel("RMS Index", fontdict={'fontsize': 12})
            axs[i].set_ylabel("Mean RMS", fontdict={'fontsize': 12})
            #axs[i].set_xlim(0, 10000)
            axs[i].set_xticks(np.arange(0, 10001, 2000))
            #axs[i].set_ylim(80, 150)
            axs[i].set_yticks(np.arange(80, 151, 10))
            axs[i].grid(alpha=0.5)
            axs[i].tick_params(labelsize=10)
            axs[i].errorbar(x=torque_data["RMS Index"], y=torque_data["Mean RMS"], yerr=[torque_data["Mean RMS"]-torque_data["lower_bound"], torque_data["upper_bound"]-torque_data["Mean RMS"]], fmt='o', capsize=2, linewidth=1, markersize=0.5)
            

        # 调整子图之间的间距和边距
        plt.subplots_adjust(wspace=0.3, hspace=0.3, left=0.05, right=0.95, top=0.95, bottom=0.05)

        # 保存图形并显示
        testpoint = re.sub(r'[^\w\s]','',testpoint)
        plt.savefig(os.path.join('root\\result\\visualization\\01 RMS mean summary for torques', f"{os.path.splitext(filename)[0]}_RMS_plot_{testpoint}.png"), dpi=300)
        plt.close()



     # 按照RMS Index分组，并计算每组的箱型图
    for torque in tqdm(all_rms["Torque"].unique()):
        torque_group = all_rms[all_rms["Torque"] == torque]
        for point in torque_group["Test Point"].unique():
            point_group = torque_group[torque_group["Test Point"] == point]
            # 首先创建一个空的figure
            fig, ax = plt.subplots()

            rms_data = []
            rms_labels = []
            for rms in point_group["RMS Index"].unique():
                rms_group = point_group[point_group["RMS Index"] == rms]
                rms_data.append(rms_group["RMS"].tolist())
                rms_labels.append(rms)
            
            #bplot = plt.boxplot(rms_data, patch_artist=True, labels=rms_labels, positions=np.arange(len(rms_data))+1, widths=0.3)
            bplot = sns.boxplot(data=rms_data, palette="Oranges", width=0.5, flierprops=dict(markerfacecolor='gray', markersize=3,alpha=0.6, linewidth=1))
            bplot.set_xticklabels(rms_labels, rotation=90)
            sns.set_style("whitegrid")
            bplot.set(xlabel='RMS Index', ylabel='RMS')
            bplot.grid(alpha=0.2)
            point_clean = re.sub(r'[\\/:?"<>|]', '', point)
            plt.title(f"Torque: {torque}, Test Point: {point_clean}")
            plt.savefig(os.path.join('root\\result\\visualization\\03 RMS boxplot for prototypes', f"{os.path.splitext(filename)[0]}_box_plot_{torque}_{point_clean}.png"), dpi=500)
            plt.close()



    # 遍历每个Test Point，绘制分类散点图和分类区间图
    for testpoint, data in grouped_by_testpoint:
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.scatterplot(data=data, x="RMS Index", y="Mean RMS", hue="Torque", style="Torque", ax=ax, palette="Set1", s=50)
        plt.title(f"RMS Mean and Confidence Interval for {testpoint}")
        plt.xlabel("RMS Index")
        plt.ylabel("Mean RMS")
        plt.xlim(0, 10000)
        plt.xticks(np.arange(0, 10001, 1000))
        plt.ylim(60, 160)
        plt.yticks(np.arange(60, 161, 10))
        plt.legend(title="Torque", loc="upper left")

        # 绘制均值的95%置信区间的上下边界
        for torque, color in colors.items():
            torque_data = data[data["Torque"] == torque]

            plt.errorbar(x=torque_data["RMS Index"], y=torque_data["Mean RMS"], yerr=[torque_data["Mean RMS"]-torque_data["lower_bound"], torque_data["upper_bound"]-torque_data["Mean RMS"]], fmt='o', capsize=2, linewidth=1, markersize=0.5,ecolor=color, alpha=0.4)

        testpoint = re.sub(r'[^\w\s]','',testpoint)
        plt.grid(color='#D3D3D3') # 添加透明色网格
        plt.savefig(os.path.join('root\\result\\visualization\\02 RMS mean for protypes on special torque', f"{os.path.splitext(filename)[0]}_RMS_plot_{testpoint}.png"))
        #plt.show()
        plt.close()