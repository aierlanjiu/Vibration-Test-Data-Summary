# 导入必要的库
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from tqdm import tqdm
from scipy.stats import norm
import re
from scipy.interpolate import UnivariateSpline
from sklearn.model_selection import KFold
from openpyxl import Workbook


#读取文件夹内所有xlsx文件，并生成一个新的xlsx保存目标线
folder_path = 'root\\result\\rds_value'
xlsx_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]
workbook = Workbook()
worksheet = workbook.active
workbook.save('root\\result\\targetline\\targetline_V2.xlsx')

for filename in tqdm(xlsx_files):
    if filename.endswith(".xlsx"):

        file_path = os.path.join(folder_path, f"{os.path.splitext(filename)[0]}.xlsx")
        #对数据进行筛选清洗
        df = pd.read_excel(file_path,engine='openpyxl')
        filename_clean = re.sub(r'.xlsx$', '', filename)
        df_top = df[df['Test Point'].str.contains('top')] 
        df = df_top.drop(['Sheet Name','Serial'], axis=1)
        df_max = df.groupby(['Test Point', 'Torque', 'Max Vibration Speed'])['Max Vibration'].max().reset_index()
        df_max_t = df.groupby(['Torque'])['Max Vibration'].mean().sort_values(ascending=False).head(7).reset_index()
        df_max_dm = df_max.drop(['Max Vibration', 'Max Vibration Speed'], axis=1)
        df_rms = df.groupby(["Test Point", "Torque", "RMS Index"])["RMS"].agg(
        ["mean", "std", lambda x: norm.interval(0.99379, loc=x.mean(), scale=x.std() / np.sqrt(len(x)))[1],
        lambda x: norm.interval(0.99379, loc=x.mean(), scale=x.std() / np.sqrt(len(x)))[0]])
        df_rms = df_rms.reset_index()
        df_rms.columns = ["Test Point", "Torque", "RMS Index", "Mean RMS", "Standard Deviation", "upper_bound","lower_bound"]      
        for testpoint in df_rms['Test Point'].unique():
            df_rms_testpoint = df_rms[df_rms['Test Point'] == testpoint]
            df_max_testpoint = df_max[df_max['Test Point'] == testpoint]
            for index, torque in enumerate(df_max_t['Torque']):
                df_rms_testpoint_torque = df_rms_testpoint[df_rms_testpoint['Torque'] == torque]
                df_max_testpoint_torque = df_max_testpoint[df_max_testpoint['Torque'] == torque]
                fig, ax = plt.subplots(figsize=(12, 8))
                sns.lineplot(data=df_rms_testpoint_torque, x="RMS Index", y="Mean RMS", ax=ax, color='green', label='Mean RMS')
                sns.scatterplot(data=df_max_testpoint_torque, x="Max Vibration Speed", y="Max Vibration", ax=ax,s=30, color='gray',label='Max Vibration')
                
                #拟合最大振动及其转速点的趋势线
                x = df_max_testpoint_torque['Max Vibration Speed']
                y = df_max_testpoint_torque['Max Vibration']
                x_new = np.concatenate([x])
                y_new = np.concatenate([y])
                max_x_new = np.max(x_new)
                max_y_new = np.max(y_new)
                x_new, indices = np.unique(x_new, return_index=True)
                y_new = y_new[indices]
                sort_indices = np.argsort(x_new)
                x_new, y_new = x_new[sort_indices], y_new[sort_indices]
                x_new_filtered = x_new
                y_new_filtered = y_new
                max_x_new_filtered = np.max(x_new_filtered)
                new_x = np.linspace(200, max_x_new, num=3000)
                new_x_filtered = np.linspace(5000, max_x_new_filtered, num=6000)
                x_new_1 = x_new[x_new < 5000]
                y_new_1 = y_new[x_new < 5000]
                x_new_2 = x_new_filtered[x_new_filtered >= 5000]
                y_new_2 = y_new_filtered[x_new_filtered >= 5000]
                kf = KFold(n_splits=5, shuffle=True, random_state=42)
                s_values = np.logspace(-10, 5, num=11, base=10.0)
                best_s_1 = None
                best_score_1 = None
                for s in s_values:
                    scores = []
                    for train_index, val_index in kf.split(x_new_1):
                            f = UnivariateSpline(x_new_1[train_index], y_new_1[train_index], s=s)
                            y_pred = f(x_new_1[val_index])
                            score = np.max(np.abs(np.gradient(y_pred)))
                            scores.append(score)
                    mean_score = np.mean(scores)
                    if best_score_1 is None or mean_score < best_score_1:
                        best_score_1 = mean_score
                        best_s_1 = s
                f_1 = UnivariateSpline(x_new_1, y_new_1, s=best_s_1)
                best_s_2 = None
                best_score_2 = None
                for s in s_values:
                    scores = []
                    for train_index, val_index in kf.split(x_new_2):
                        f = UnivariateSpline(x_new_2[train_index], y_new_2[train_index], s=s)
                        y_pred = f(x_new_2[val_index])
                        score = np.max(np.abs(np.gradient(y_pred)))
                        scores.append(score)
                    mean_score = np.mean(scores)
                    if best_score_2 is None or mean_score < best_score_2:
                        best_score_2 = mean_score
                        best_s_2 = s
                f_2 = UnivariateSpline(x_new_2, y_new_2, s=best_s_2)
                new_y_1 = f_1(new_x[new_x < 5000])
                new_y_2 = f_2(new_x[new_x >= 5000])
                new_y = np.concatenate([new_y_1, new_y_2])
                #对拟合后的曲线做修正补偿
                maxvib = df_max_testpoint_torque.loc[df_max_testpoint_torque["Max Vibration Speed"] < 8000, "Max Vibration"].max()
                RMS_Index_maxvib = df_max_testpoint_torque.loc[df_max_testpoint_torque["Max Vibration"] == maxvib, "Max Vibration Speed"].values[0]
                move_max = maxvib - f_2(RMS_Index_maxvib)
                f = UnivariateSpline(new_x, new_y, s=np.mean([best_s_1,best_s_2]))
                new_y = f(new_x)+move_max

                #拟合RMS的4σ边界线
                x2 = df_rms_testpoint_torque['RMS Index']
                y2 = df_rms_testpoint_torque['upper_bound']
                max_x2 = np.max(x2)
                mean_s = np.mean([best_s_1, best_s_2])
                new_x2 = np.linspace(200, max_x2, num=5000)
                f = UnivariateSpline(x2, y2, s=mean_s)
                new_y2 = f(new_x2)
                #修正拟合曲线
                maxbound = df_rms_testpoint_torque.loc[df_rms_testpoint_torque["RMS Index"] < 8000, "upper_bound"].max()
                RMS_Index_max = df_rms_testpoint_torque.loc[df_rms_testpoint_torque["upper_bound"] == maxbound, "RMS Index"].values[0]
                move = maxbound - f(RMS_Index_max)
                f = UnivariateSpline(new_x2, new_y2, s=mean_s)
                new_y2 = f(new_x2)+move   


                #保存目标线到excel
                targetline = {'input speed': new_x, 'target': new_y,'target+5': new_y+5}
                df_target = pd.DataFrame(targetline)
                testpoint_clean = re.sub(r'[^\w\s]','',testpoint)
                with pd.ExcelWriter('root\\result\\targetline\\targetline_V2.xlsx', mode='a', engine='openpyxl') as writer:
                    df_target.to_excel(writer, sheet_name=f'{testpoint_clean}_{torque}_{filename_clean}', index=False)
                
                #保存预测曲线图
                sns.lineplot(x=new_x, y=new_y, ax=ax,label='Target Line')
                sns.lineplot(x=new_x,y=new_y+5,ax=ax,label='Target line with modified', linestyle='--')
                ax.fill_between(new_x, new_y, new_y+5, color='yellow', alpha=0.2,label='modified value')
                plt.fill_between(df_rms_testpoint_torque["RMS Index"], df_rms_testpoint_torque["lower_bound"], df_rms_testpoint_torque["upper_bound"], color='lightgreen', alpha=0.2,label='RMS 4σ band')
                plt.plot(new_x2, new_y2, color='skyblue', linewidth=1,label='upper bound')
                plt.legend(title="Legend", loc="upper left")
                plt.title(f"targetline {filename_clean}{torque}{testpoint_clean}")
                plt.xlabel("Input Speed")
                plt.ylabel("Housing Vibration dB[g]")
                plt.xlim(0, 10000)
                plt.xticks(np.arange(0, 10001, 1000))
                plt.ylim(60, 166)
                plt.yticks(np.arange(60, 166, 10))
                
                plt.grid(color='#D3D3D3') # 添加透明色网格
                plt.savefig(os.path.join('root\\result\\visualization\\07 dataoverview\\dataoverview\\04 targetline', f"{os.path.splitext(filename)[0]}_targetline_{testpoint_clean}_{torque}.png"))
                plt.close()





