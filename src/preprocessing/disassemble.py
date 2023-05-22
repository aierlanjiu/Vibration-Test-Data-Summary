#这段代码的作用是读取名为"LP11_processed.xlsx"的Excel文件，然后根据Curve列中的Order和Direction筛选数据帧，并将筛选后的数据帧写入四个新的Excel文件中。具体来说，它会将Curve列包含Order 26的数据帧分别写入"26order run upframes.xlsx"和"26order run downframes.xlsx"文件中，将Curve列包含Order 9.62的数据帧分别写入"9.62order run upframes.xlsx"和"9.62order run downframes.xlsx"文件中。

#如果你想要使用这段代码，需要将它保存到名为"disassemble.py"的文件中，并将"LP11processed.xlsx"文件放在同一目录下。然后运行这个文件，就会生成四个新的Excel文件，分别包含筛选后的数据帧。

# 导入所需的库
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

# 定义函数，用于过滤数据帧并将数据帧写入Excel文件
def filter_and_write_frames(filename, order, direction, frames):
    filtered_frames = {name: frame for name, frame in frames.items() if order in str(frame["Curve"][0]) and direction in str(frame["Curve"][0])}
    wb = Workbook()
    for name, frame in filtered_frames.items():
        wb.create_sheet(name)
        sheet = wb[name]
        for r in dataframe_to_rows(frame, index=False, header=True):
            sheet.append(r)
    wb.save(filename)

# 读取Excel文件
df = pd.read_excel("root/data/raw_data/LP11_processed.xlsx", sheet_name=None)

# 过滤Curve列包含Order 26的数据帧并将数据帧写入Excel文件
filter_and_write_frames("root\\data\\cleaned_data\\26 order run up_frames.xlsx", "Order 26", "Running Up", df)
filter_and_write_frames("root\\data\\cleaned_data\\26 order run down_frames.xlsx", "Order 26", "Running Down", df)

# 过滤Curve列包含Order 9.62的数据帧并将数据帧写入Excel文件
filter_and_write_frames("root\\data\\cleaned_data\\9.62 order run up_frames.xlsx", "Order 9.62", "Running Up", df)
filter_and_write_frames("root\\data\\cleaned_data\\9.62 order run down_frames.xlsx", "Order 9.62", "Running Down", df)