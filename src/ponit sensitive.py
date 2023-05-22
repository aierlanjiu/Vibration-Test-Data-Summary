import pandas as pd
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from tqdm import tqdm
import numpy as np
from scipy.stats import t
import re
import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 定义要处理的文件夹路径
folder_path = 'root\\result\\rds_value'

# 获取所有xlsx文件的文件名
xlsx_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

# 遍历指定路径下的所有xlsx文件
for filename in tqdm(xlsx_files):
    if filename.endswith(".xlsx"):
        # 读取Excel文件
        df = pd.ExcelFile(os.path.join(folder_path, filename))
    # 读取Excel文件
    df = pd.read_excel(os.path.join(folder_path, f"{os.path.splitext(filename)[0]}.xlsx"))

    # 根据测点名称分组，计算低扭矩和高扭矩下的振动RMS均值
    # 提取数字部分
    df['Torque'] = df['Torque'].apply(lambda x: re.findall(r'\d+\.?\d*', str(x))[0])
    # 将Torque列转换为float类型
    df['Torque'] = df['Torque'].astype(float)
    
    grouped = df.groupby(['Test Point', df['Torque'].abs() > 50])['RMS'].mean().reset_index()

    # 按照低扭矩和高扭矩分别排序
    low_torque = grouped[grouped['Torque'] == False].sort_values(by='RMS', ascending=False)
    high_torque = grouped[grouped['Torque'] == True].sort_values(by='RMS', ascending=False)

    # 打印排序结果
    print(filename+'低扭矩敏感测点排序：')
    print(low_torque['Test Point'].values)
    print(filename+'高扭矩敏感测点排序：')
    print(high_torque['Test Point'].values)

    # 绘制两张图
    sns.set(style="ticks")

    # 低扭矩图
    low_torque_plot = sns.catplot(x="Test Point", y="RMS", hue="Torque", kind="bar", data=grouped[grouped['Torque'] == False], height=4, aspect=3)
    plt.title(f"low torque RMS mean {filename}")
    plt.ylim(min(grouped['RMS'])-2, max(grouped['RMS'])+2)
    plt.yticks(np.arange(min(grouped['RMS'])-2, max(grouped['RMS'])+2, (max(grouped['RMS'])+2-min(grouped['RMS'])-2)/5))
    plt.savefig(os.path.join('root\\result\\visualization\\07 dataoverview\\dataoverview\\01 testpoint comparision\\', filename.replace('.xlsx', '_low_torque.png')))
    #plt.show()

    # 高扭矩图
    high_torque_plot = sns.catplot(x="Test Point", y="RMS", hue="Torque", kind="bar", data=grouped[grouped['Torque'] == True], height=4, aspect=3)
    plt.title(f"high torque RMS mean {filename}")
    plt.ylim(min(grouped['RMS'])-2, max(grouped['RMS'])+2)
    plt.yticks(np.arange(min(grouped['RMS'])-2, max(grouped['RMS'])+2, (max(grouped['RMS'])+2-min(grouped['RMS'])-2)/5))
    plt.savefig(os.path.join('root\\result\\visualization\\07 dataoverview\\dataoverview\\01 testpoint comparision\\', filename.replace('.xlsx', '_high_torque.png')))
    #plt.show()
