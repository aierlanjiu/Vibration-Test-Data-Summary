# 减速器振动测试台数据分析

这个工程旨在通过对减速器（gearbox）在振动测试台上的测试数据进行筛选、清洗、统计、可视化和趋势分析，为我们更好地理解当前减速器设计状态的噪声振动机制及噪声水平评估提供支持。同时也为整个团队及相关合作伙伴提供依据，以改进产品设计方案和优化生产流程。下面是一个概览：

## 数据来源
我们采集了减速器在不同加载条件下表面不同测点处的齿轮阶次振动信号，并从相应的原始数据提供方处获得Excel格式的数据。所有原始数据均存储在'data'文件夹内以便以后重新查看或分析。
我们在进行测试代码编写和功能调试时，使用了已经脱敏处理过的振动信号数据。这些数据仅用于测试、验证代码是否正常运行等技术性目的，并不能直接用于任何对标或参考分析（Benchmarking）的工作。同时，请注意所述数据不包含任何敏感信息以及可以还原到实际测试对象身份的相关特征。我们已经采用一系列科技方法和数据管理程序来确保这些数据在任何情况下都得到有效的借款。如有疑问或需要更多详细信息，请联系我。

## 筛选与清洗
我们以一种标准的方式对数据进行处理，将海量的数据分类筛选提取有效特征以便后续分析。主要利用Python Pandas库对各工况下不同测点的齿轮阶次振动信号进行筛选和基础的清洗。

## 统计分析
我们希望了解在不同工况条件下，敏感振动测点的最大振动值及对应的转速。因此，我们计算同一工况、同一扭矩、同一测点的每500rpm的RMS值，并利用正态分布区间预测技术或基于组合图像（contour plot）来预估相关数据的分布情况和拟合范围。接着，我们使用Python Matplotlib和Seaborn库进行可视化，生成各种散点图、箱线图、直方图、概率图等，以帮助我们发现异常或趋势性特征。

## 振动机制识别
通过将振动曲线数据归纳到边际图、轴心图、高斯混合模型等多维特定空间中，我们能够更好地理解振动过程产生的机制和规律。例如，可以识别出振动峰值处及其两侧的振动过渡区、振幅参数与谐波关系的相容性、以及最敏感振动点的位置等信息。我们可以使用MATLAB或Python的scikit-learn, scipy等库来分类处理这些数据。
整理数据：将采集到的原始振动曲线数据按照一定标准组织，排除不符合需求的数据，并完成分类规定。简单来说就是以下这些步骤：

清洗数据：对于存在错误、重复或缺失值的数据，采取删除、填充或插值等方式进行处理，以确保数据的完整性和准确性。
转换数据：对数据进行归一化、标准化、特征选择等变换，使其更加利于后续处理和分析。
分析数据：应用统计学和机器学习等方法对数据进行建模、聚类、分类和预测等分析操作，以便发现数据背后的规律、趋势和异常等问题。
形成结论：根据数据分析结果，制定相应的结论和建议，并在必要时对数据处理和分析的过程进行进一步优化和改进。

## 趋势分析与优化建议
最后，我们对各单台减速器振动数据的可视化图像及其分析结果进行了梳理。针对具有明显共性或趋势的数据特点（例如最敏感振动测点，最敏感扭矩，对应扭矩下的敏感转速区），我们尝试使用MATLAB或Python的scipy等库将不同扭矩下不同测点最大振动值拟合到趋势线上，并导出根据趋势线给出的目标值，以用于制定有效的优化措施和改进建议。

## 额外说明
本项目的代码均是通过gpt模型生成，再经人工调试和改进得到。虽然我们的开发者没有Python编程基础，但通过与gpt模型的交流，他们掌握了一些关于Python编程的皮毛。
因此，在本项目中，你可能会看到许多存在代码重复计算的问题，而且有些代码并不简洁精炼。但我们保证所有的代码都可以正常运行并完成所需功能。（有些代码的运行可能会由于数据过多。而需要2小时以上来运行。）
另外，本项目还包含自动生成PPT的功能，可以帮助用户更好地理解数据并展示结果。这包括使用Python编程语言创建表格、制图、添加文字等过程来自动化生成PPT文件。

最后，我们致力于共享和开放本项目的源代码，并欢迎社区成员贡献代码和提出改进建议。
<img src="./result/visualization/06 Sigle reducer line plot/9.62 order run down_frames_results_smooth_curve_input shaft+Y_2302211000033.png" alt="单体减速器振动"/>
<img src="./result/visualization/03 RMS boxplot for prototypes/9.62 order run down_frames_results_box_plot_15Nm_input shaft+Y.png" />
<img src="./result/visualization/07 dataoverview/dataoverview/04 targetline/9.62 order run down_frames_results_targetline_topX_15Nm.png" alt="基于最大振动值的趋势线预测"/>
<img src="./result/visualization/07 dataoverview/dataoverview/05 torque correlation/9.62 order run down topX.png" alt="不同扭矩间振动相关性"/>



# 项目文件结构

此项目包含如下文件和文件夹：

- `data` - 包含原始数据和经过筛选清洗后得到的数据。
  - `raw_data` - 存放原始数据的文件夹。
  - `cleaned_data` - 存放筛选清洗后的数据的文件夹。
- `result` - 存放计算出的预测结果和可视化结果。
  - `rds_value` - 存放RMS值及正态分布区间预测结果的文件夹（每500rpm）。
  - `targetline` - 存放拟合的趋势线预测目标值的文件夹。
  - `visualization` - 存放不同扭矩下、不同工况下振动散点图、边际图和振动敏感转速区识别等结果的文件夹。
- `src` - 存放项目中用到的Python模块。
  - `preprocessing.py` - 数据预处理模块（导入Excel、筛选清洗）。
  - `rds_predict.py` - RMS值预测及正态分布区间计算模块。
  - `max_point.py` - 最大振动点及其转速边际图绘制模块。
  - `serial.py` - 绘制不同扭矩下、不同工况下振动散点图模块。
  - `fitting_curve.py` - 拟合趋势线并生成目标值模块。
  - `torque_corr.py` - 计算不同扭矩的振动相关性模块。
  - `conditions.py` - 根据特殊测点排列各工况振动敏感度，推荐关注的扭矩和转速模块。
  - `point_sensitive.py` - 敏感测点排序模块。
  - `serial_sensitive.py` - 按照振动量级对测试的减速器进行排序模块。
- `test` - 存放项目测试代码的文件夹。
- `main.py` - 项目主程序入口文件。
- `requirements.txt` - Python依赖库清单。
### 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=aierlanjiu/Vibration-Test-Data-Summary&type=Date)](https://star-history.com/#aierlanjiu/Vibration-Test-Data-Summary&Date)





