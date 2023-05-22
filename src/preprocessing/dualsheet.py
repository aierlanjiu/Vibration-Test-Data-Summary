#这段代码主要用于处理一个名为'LP11.xlsx'的Excel文件。它执行以下几个操作：

#读取Excel数据获取每条曲线的相关信息。
#获取每条曲线对应的两列数据中“linear”所在行以上的数据并将其全部删除并将表格上移。
#将删除行后的Excel表格保存为_temp1.xlsx。
#遍历每张sheet，获取每条曲线的列名，按照数据起始点分成一个个步骤，计算每个步骤内振动值的rms值、最大振动值及其对应的转速，并将结果生成到新的sheet中。
#将新的sheet保存到_temp2.xlsx。
#将“Step Vibration”列中的开始值和结束值分别提取并存储在两列“start_v”和“stop_v”中，并将其加入到各自的Sheet中。
#处理完所有sheet后将处理后的Excel文件保存为_processed.xlsx。
#删除_temp1.xlsx和_temp2.xlsx临时文件。


import os
import pandas as pd
import numpy as np
from tqdm import tqdm
import time


# 设置要处理的文件名
file_name = 'root\\data\\raw_data\\LP11.xlsx'

def process_excel_file(file_path:str):
    # 读取Excel数据
    df = pd.read_excel(file_path, engine='openpyxl')

    # 定义曲线名字列表
    curve_names = []


    # 定义跳过数据的计数器和存储跳过数据名称的列表
    skipped_count = 0
    skipped_names = []


    # 遍历每条曲线
    for i in range(1, len(df.columns), 2):
        # 获取曲线名字
        curve_name = 'Curve ' + str((i+1)//2)
        curve_names.append(curve_name)

        # 获取曲线对应的两列数据
        curve_data = df.iloc[:, i-1:i+1]

        try:
            a1 = curve_data[curve_data.iloc[:, 0] == 'Standard\\Function\\label'].index[0]
            a2 = curve_data[curve_data.iloc[:, 0] == 'TestLab\\Block\\Original run'].index[0]
            a3 = curve_data[curve_data.iloc[:, 0] == 'TestLab\\Block\\Outer run slope'].index[0]
        except IndexError:
            print('One of the required labels is missing for the current data. Skipping to next data...')
            skipped_count += 1
            skipped_names.append(curve_name)
            continue

        result = curve_data.iloc[a2, 1].split()[1:-1]
        result_str = ' '.join(result)

        # 查找所在行a1 a2对应的B列的值，将这两个值相加后输出为Curve name1的值
        curve_value = str(curve_data.iloc[a1, 1] + ' ' + result_str + ' ' + curve_data.iloc[a3, 1])

        #print(curve_name + ' value: ' + str(curve_value))



        # 将每条曲线对应的两列数据中‘linear’所在行以上的数据全部删除并表格上移
        linear_index = curve_data[curve_data.iloc[:, 0] == 'Linear'].index[0]
        curve_data = curve_data.iloc[linear_index+1:, :]



        df.iloc[:curve_data.shape[0], i-1:i+1] = curve_data.values
        df = df.rename(columns={df.columns[i]: curve_value})    

    # 输出总共跳过多少组数据及哪些数据
    print(f"Skipped {skipped_count} data sets: {', '.join(skipped_names)}")   

    # 将新的表格保存
    df.to_excel(os.path.splitext(file_path)[0] + "_temp1.xlsx", index=False)



    # 读取Excel文件
    df = pd.read_excel(os.path.splitext(file_path)[0] + '_temp1.xlsx', sheet_name=None)
    new_sheet_dict = {}

    # Get total number of sheets
    total_sheets = len(df.items()) - sum('Processed' in name for name in df.keys())
    num_processed_sheets = 0

    # 遍历每个sheet
    for sheet_name, sheet_data in df.items():

        # 获取每条曲线的列名
        curve_cols = sheet_data.columns[1::2]

        # 遍历每条曲线
        for i, curve_col in enumerate(curve_cols):
            # 获取曲线的转速列和振动幅值列
            speed_col = sheet_data.columns[i*2]
            vib_col = sheet_data.columns[i*2+1]
            # 按照数据起始点到1000rpm为一个step，1000rpm之后的数据以每500rpm为一个step
            speed = sheet_data[speed_col]
            step = np.concatenate([np.arange(500, speed.max()+1, 500)])
            # 计算每个step对应的振动值的rms值及这个step中最大振动值以及最大振动值对应的转速
            rms = []
            max_vib = []
            max_vib_speed = []
            step_start_speeds = []
            step_end_speeds = []
            step_vibs = []

            for j in tqdm(range(len(step)-1), desc=f"Sheet '{sheet_name}', curve '{curve_col}', processing steps"):
                start = step[j]
                end = step[j+1]
                vib = sheet_data[vib_col][(speed >= start) & (speed < end)]
                if vib.empty:
                    rms.append(np.nan)
                    max_vib.append(np.nan)
                    max_vib_speed.append(np.nan)
                else:
                    rms.append(np.sqrt(np.mean(vib**2)))
                    max_vib.append(vib.max())
                    max_vib_speed.append(speed.loc[vib.idxmax()])
                step_start_speeds.append(start)
                step_end_speeds.append(end)
                step_vibs.append(vib.values)

            # 将这些计算结果生成一个新的sheet 保持在excel中
            new_sheet_data = pd.DataFrame({'Step': range(1, len(step)), 'RMS': rms,
                                           'Max Vibration': max_vib, 'Max Vibration Speed': max_vib_speed,
                                           'Curve': curve_col, 'Step Start Speed': step_start_speeds,
                                           'Step End Speed': step_end_speeds, 'Step Vibration': step_vibs})
            # Replace all values in Curve column after the first row with empty strings
            new_sheet_data.loc[1:, 'Curve'] = ''
            new_sheet_name = ' Curve ' + str(i+1) + ' Processed'
            new_sheet_dict[new_sheet_name] = new_sheet_data
            num_processed_sheets += 1
            # 显示进度条
            tqdm.write(f"Processed {num_processed_sheets} of {total_sheets} sheets. Sheet '{sheet_name}', curve '{curve_col}' done.\n")

    # Write all new sheets to the Excel file
    with pd.ExcelWriter(os.path.splitext(file_path)[0] + "_temp2.xlsx", engine='openpyxl') as writer:
        for sheet_name, sheet_data in new_sheet_dict.items():
            sheet_data.to_excel(writer, sheet_name=sheet_name, index=False)


    # Function to add two columns to the dataframe, then fill the columns with start_v and stop_v values for each row
    def add_columns(sheet_df):
        sheet_df['start_v'] = sheet_df['Step Vibration'].str[1:12]
        sheet_df['stop_v'] = sheet_df['Step Vibration'].str[-13:-1]

        # Drop the original 'Step Vibration' column
        sheet_df.drop(columns=['Step Vibration'], inplace=True)

        # Convert the new columns to numeric format
        sheet_df['start_v'] = pd.to_numeric(sheet_df['start_v'], errors='coerce')
        sheet_df['stop_v'] = pd.to_numeric(sheet_df['stop_v'], errors='coerce')

        return sheet_df

    # Reading all sheets of the Excel file ddd1.xlsx
    data_frames = pd.read_excel(os.path.splitext(file_path)[0] + '_temp2.xlsx', sheet_name=None)

    total_time = 0
    with tqdm(total=len(data_frames)) as pbar:
        # Writing the combined updated dataframe with two additional columns to a temporary file
        temp_file = os.path.splitext(file_path)[0] + "_temp.xlsx"
        with pd.ExcelWriter(temp_file) as writer:
            for sheet_name, sheet_df in data_frames.items():
                start_time = time.time()
                updated_sheet_df = add_columns(sheet_df)
                updated_sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)
                end_time = time.time()
                total_time += end_time - start_time
                time_per_sheet = total_time / (len(data_frames))
                pbar.update(1)
                pbar.set_description("Time per sheet: {:.2f}s".format(time_per_sheet))
        
        excel_file = os.path.splitext(file_path)[0] + "_processed.xlsx"
        # Move the temporary file to the excel file
        os.replace(temp_file, excel_file)

    # 输出总共跳过多少组数据及哪些数据
    print(f"Skipped {skipped_count} data sets: {', '.join(skipped_names)}")  


    # 删除temp1文件
    os.remove(os.path.splitext(file_path)[0] + '_temp1.xlsx')
    os.remove(os.path.splitext(file_path)[0] + '_temp2.xlsx')
# Usage:
process_excel_file(file_name)