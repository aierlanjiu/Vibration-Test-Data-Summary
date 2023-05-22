import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    df_top_grouped = df_top.groupby('Serial')['Max Vibration'].mean().sort_values(ascending=False)
    print(f"{filename}整体振动量级排序：{df_top_grouped.index}")
    df_top = df_top.drop(['Sheet Name'], axis=1)
    df_top = df_top.groupby(['Serial', 'Torque','Max Vibration Speed'])['Max Vibration'].mean().reset_index()
    
    df_top = df_top.groupby("Torque")
    df_top.columns = ["Serial", "Torque","Max Vibration Speed","Max Vibration"]
    for torque,df_t in df_top:
        sns.scatterplot(data=df_t, x='Max Vibration Speed', y='Max Vibration', hue='Serial', hue_order=df_top_grouped.index, style='Serial',palette="Set1", s=30,alpha=0.7)
        plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0., fontsize=5)
        plt.suptitle(f"{filename}Max Vibration mean @ topS for {torque}", fontsize=10)
        plt.grid(color='#D3D3D3') # 添加透明色网格
        plt.savefig(os.path.join('root\\result\\visualization\\07 dataoverview\\dataoverview\\02 serial comparision\\', filename.replace('_frames_results.xlsx', f"_torque_{torque}.png")))
        
        plt.close()  # 关闭当前图形窗口，以便下一次循环时重新创建