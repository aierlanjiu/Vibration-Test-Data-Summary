import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm
import numpy as np
from tqdm import tqdm

# 定义要处理的文件夹路径
folder_path = 'root\\result\\rds_value'


# 获取所有xlsx文件的文件名
xlsx_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

# 遍历指定路径下的所有xlsx文件
for filename in tqdm(xlsx_files):
    if filename.endswith(".xlsx"):
        # 读取Excel文件
        df = pd.ExcelFile(os.path.join(folder_path, filename))
    df = pd.read_excel(os.path.join(folder_path, f"{os.path.splitext(filename)[0]}.xlsx"))

    df_top = df[df['Test Point'].str.contains('top')]

    df = df_top.drop(['Sheet Name','Test Point','Serial'], axis=1)

    df_torque = df.groupby(['Torque','Step End Speed'])['Max Vibration'].mean().sort_values(ascending=False).reset_index()
    df_torque_t = df.groupby(['Torque'])['Max Vibration'].mean().sort_values(ascending=False).head(7).reset_index()
    print(f"建议{filename}考虑的扭矩优先级:{df_torque_t['Torque']}")
    # Visualization
    fig, axs = plt.subplots(2, 4, figsize=(16, 8))
    plt.xticks(rotation=30)
    axs = axs.reshape(-1)

    axs[0].bar(df_torque_t['Torque'], df_torque_t['Max Vibration'], color='green')
    axs[0].set_xlabel('Torque')
    axs[0].tick_params(axis='x', labelsize=6,labelrotation=30)
    axs[0].set_ylabel('Max Vibration')
    axs[0].tick_params(axis='y', labelsize=8)
    axs[0].set_title('Top 5 Torque',fontsize=12)
    axs[0].set_ylim([df_torque_t['Max Vibration'].min()-1, df_torque_t['Max Vibration'].max()+1])
    for n, m in enumerate(df_torque_t['Max Vibration']):
        axs[0].text(n, m+0.1, str(round(m,2)), ha='center', fontsize=6)
    i = 1

    colors = cm.rainbow(np.linspace(0, 1, len(df_torque_t['Torque'])))

    for index, torque in enumerate(df_torque_t['Torque']):
        df_t = df_torque[df_torque['Torque'] == torque]
        df_speed = df_t.groupby(pd.cut(df_t['Step End Speed'], bins=range(0, 6001, 500)))['Max Vibration'].mean().sort_values(ascending=False).head(5).reset_index()
        print(f"建议{filename}在扭矩{torque}下重点关注的转速范围优先级：{df_speed['Step End Speed']}")
        axs[i].bar(df_speed['Step End Speed'].astype(str), df_speed['Max Vibration'], color=colors[index])
        axs[i].set_xlabel('Speed Range')
        axs[i].set_ylabel('Max Vibration')
        axs[i].set_ylim([df_speed['Max Vibration'].min()-1, df_speed['Max Vibration'].max()+1])
        axs[i].tick_params(axis='x', labelsize=6,labelrotation=30)
        axs[i].tick_params(axis='y', labelsize=8)
        axs[i].set_title('Top 5 Speed Range for Torque: {}'.format(torque),fontsize=12)
        i += 1
        for k, v in enumerate(df_speed['Max Vibration']):
            axs[index+1].text(k, v+0.1, str(round(v,2)), ha='center', fontsize=6)

    plt.tight_layout()

    # 保存图像
    
    plt.savefig(f"root\\result\\visualization\\07 dataoverview\\dataoverview\\03 suggest test condition\\conditions according to rms {filename}.png")
    plt.close()




# 遍历指定路径下的所有xlsx文件
for filename in tqdm(xlsx_files):
    if filename.endswith(".xlsx"):
        # 读取Excel文件
        df = pd.ExcelFile(os.path.join(folder_path, filename))
    df = pd.read_excel(os.path.join(folder_path, f"{os.path.splitext(filename)[0]}.xlsx"))


    df_top = df[df['Test Point'].str.contains('top')]

    df = df_top.drop(['Sheet Name','Test Point','Serial'], axis=1)

    df_torque = df.groupby(['Torque','Step End Speed'])['RMS'].mean().sort_values(ascending=False).reset_index()
    df_torque_t = df.groupby(['Torque'])['RMS'].mean().sort_values(ascending=False).head(7).reset_index()
    print(f"建议{filename}考虑的扭矩优先级:{df_torque_t['Torque']}")
    # Visualization
    fig, axs = plt.subplots(2, 4, figsize=(16, 8))
    plt.xticks(rotation=30)
    axs = axs.reshape(-1)

    axs[0].bar(df_torque_t['Torque'], df_torque_t['RMS'], color='green')
    axs[0].set_xlabel('Torque')
    axs[0].tick_params(axis='x', labelsize=6,labelrotation=30)
    axs[0].set_ylabel('RMS')
    axs[0].tick_params(axis='y', labelsize=8)
    axs[0].set_title('Top 5 Torque',fontsize=12)
    axs[0].set_ylim([df_torque_t['RMS'].min()-1, df_torque_t['RMS'].max()+1])
    for n, m in enumerate(df_torque_t['RMS']):
        axs[0].text(n, m+0.1, str(round(m,2)), ha='center', fontsize=6)
    i = 1

    colors = cm.rainbow(np.linspace(0, 1, len(df_torque_t['Torque'])))

    for index, torque in enumerate(df_torque_t['Torque']):
        df_t = df_torque[df_torque['Torque'] == torque]
        df_speed = df_t.groupby(pd.cut(df_t['Step End Speed'], bins=range(0, 6001, 500)))['RMS'].mean().sort_values(ascending=False).head(5).reset_index()
        print(f"建议{filename}在扭矩{torque}下重点关注的转速范围优先级：{df_speed['Step End Speed']}")
        axs[i].bar(df_speed['Step End Speed'].astype(str), df_speed['RMS'], color=colors[index])
        axs[i].set_xlabel('Speed Range')
        axs[i].set_ylabel('RMS')
        axs[i].set_ylim([df_speed['RMS'].min()-1, df_speed['RMS'].max()+1])
        axs[i].tick_params(axis='x', labelsize=6,labelrotation=30)
        axs[i].tick_params(axis='y', labelsize=8)
        axs[i].set_title('Top 5 Speed Range for Torque: {}'.format(torque),fontsize=12)
        i += 1
        for k, v in enumerate(df_speed['RMS']):
            axs[index+1].text(k, v+0.1, str(round(v,2)), ha='center', fontsize=6)

    plt.tight_layout()

    # 保存图像
    
    plt.savefig(f"root\\result\\visualization\\07 dataoverview\\dataoverview\\03 suggest test condition\\conditions according to max {filename}.png")
    plt.close()