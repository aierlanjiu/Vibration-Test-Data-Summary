import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 读取Excel文件
dfgroup = pd.read_excel('root\\result\\targetline\\target group.xlsx', sheet_name=None)


# 遍历每个sheet
for sheet in dfgroup :

    # 提取数据，并计算新列
    data = dfgroup [sheet].set_index('input speed')

    # 创建包含所有唯一扭矩值的列表
    torques = sorted(data['Torque'].unique())

    # 创建一个空的DataFrame来存储每组扭矩值之间的相关系数
    correlations_df = pd.DataFrame(index=torques, columns=torques)

    # 针对每一组扭矩值，计算Target+5列与其它变量之间的相关系数，并更新correlations_df
    for i, torque1 in enumerate(torques):
        subset1 = data[data['Torque'] == torque1] 
        
        for j, torque2 in enumerate(torques):
            subset2 = data[data['Torque'] == torque2] 
            
            # 计算 subset1 和 subset2 中较短的长度
            min_length = min(len(subset1), len(subset2))
            end_speed = min(subset1.index[min_length-1], subset2.index[min_length-1])

            subset1_filtered = subset1[subset1.index < end_speed].reset_index(drop=True)
            subset2_filtered = subset2[subset2.index < end_speed].reset_index(drop=True)

            # 计算subset1和subset2之间Target+5列的相关性系数，并存储到correlations_df中
            corr_coef = subset1_filtered['target'].corr(subset2_filtered['target'], method='kendall')
            correlations_df.iat[i, j] = corr_coef
    correlations_df = correlations_df.astype(float)
    print(correlations_df)
    # 绘制矩阵图
    plt.figure(figsize=(24, 8))
    plt.subplot(1, 4, (2, 4))
    
    sns.lineplot(data=data, x='input speed', y='target+5', hue='Torque')
    plt.title(sheet)
    plt.legend(title="Legend", loc="upper left")
    plt.xlabel("Input Speed")
    plt.ylabel("Housing Vibration dB[g]")
    plt.xlim(0, 10000)
    plt.xticks(np.arange(0, 10001, 1000))
    plt.ylim(60, 166)
    plt.yticks(np.arange(60, 166, 10))
    plt.grid(color='#D3D3D3')
    plt.subplot(1, 4, 1)
    sns.heatmap(correlations_df, cmap='coolwarm', annot=True,
                xticklabels=torques, yticklabels=torques, vmin=0, vmax=1)
    plt.title('Correlation Matrix')
    

    # 保存图像
    plt.savefig(f"root//result//visualization//07 dataoverview//dataoverview//04a targetline torque//{sheet}.png")
    
    # 关闭图像，以便下一个循环可以绘制一个新的图形并使用相同的名称
    plt.close()

