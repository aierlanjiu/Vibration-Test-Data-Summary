import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from tqdm import tqdm
import numpy as np
from scipy.stats import t
import re
from statsmodels.nonparametric.smoothers_lowess import lowess

# 定义要处理的文件夹路径
folder_path = 'root\\result\\rds_value'

colors_runup = {"15Nm": "blue", "31Nm": "orange", "50Nm": "yellow","66Nm":"brown", "100Nm":"red", "200Nm":"green", "310Nm":"purple"}
colors_rundown = {"15Nm": "green", "31Nm": "purple", "50Nm": "orange","66Nm":"yellow", "-137Nm":"red", "-206Nm":"blue"}
# 将颜色字典中的值替换为十六进制颜色代码
colors_runup = {k: v.replace("blue", "#0000FF").replace("orange", "#FFA500").replace("yellow", "#FFFF00").replace("brown", "#A52A2A").replace("red", "#FF0000").replace("green", "#008000").replace("purple", "#800080") for k, v in colors_runup.items()}
colors_rundown = {k: v.replace("blue", "#0000FF").replace("orange", "#FFA500").replace("yellow", "#FFFF00").replace("brown", "#A52A2A").replace("red", "#FF0000").replace("green", "#008000").replace("purple", "#800080") for k, v in colors_rundown.items()}
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
        
    #print(colors)
    # 读取数据
    grouped_rms = pd.read_excel(os.path.join(folder_path, f"{os.path.splitext(filename)[0]}.xlsx"))

    # 按照Test Point/Serial分组，并计算每组的散点图和折线图

    for point in grouped_rms["Test Point"].unique():
        point_group = grouped_rms[grouped_rms["Test Point"] == point]
        for serial in point_group["Serial"].unique():
            serial_group = point_group[point_group["Serial"] == serial]
            
            # 首先创建一个空的figure
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.scatterplot(data=serial_group, x="Max Vibration Speed", y="Max Vibration", hue="Torque", style="Torque", ax=ax, palette="Set1", s=90)
            sns.lineplot(data=serial_group, x="RMS Index", y="RMS", ax=ax, hue="Torque", palette="Set1")

            point_clean = re.sub(r'[\\/:?"<>|]', '', point)
            plt.title(f"data for Serial:{serial},Test Point:{point_clean}")
            plt.xlabel("input Speed")
            plt.ylabel("Vibration dB[g]")
            plt.xlim(0, 10000)
            plt.xticks(np.arange(0, 10001, 1000))
            plt.ylim(60, 170)
            plt.yticks(np.arange(60, 171, 10))
            plt.legend(title="Torque", loc="upper left")
            plt.grid(alpha=0.2)



            # 显示图像并保存
            #plt.show()
            plt.savefig(os.path.join('root\\result\\visualization\\06 Sigle reducer line plot', f"{os.path.splitext(filename)[0]}_smooth_curve_{point_clean}_{serial}.png"), dpi=500)
            plt.close()