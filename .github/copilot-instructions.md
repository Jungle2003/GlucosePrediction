# GlucosePrediction 项目 - AI 编码代理指令

## **项目概述**

这是一个血糖预测系统，使用血糖监测数据,进行数据处理，模型构建等工作。项目在数据管理、预处理和建模之间遵循清晰的分离原则。

## **AI编码注意事项**
每次编辑处理后，根据编辑内容，修改更新本文件中的相关部分，确保文档与代码保持同步。
任何时候都不要检索笔记本摘要

## **架构与目录结构**

### doc
**文件说明:**
- `dissertation.md`:基于此项目的毕业论文，如果你需要编辑它，请阅读已有部分的文字，确保新增内容与我的文字风格一样，并且内容连贯。
已完成章节：
  - 第1章：绪论（研究背景、CGM技术特点、血糖预测意义、国内外研究现状）
  - 第2章：实验数据集选择与标准化处理（Colas和Hall数据集、数据格式化、缺失值处理）
  - 第3章：CGM数据噪声评估与滤波处理（噪声来源分析、三种滤波方法比较、S-G滤波器选择）
额外的注意事项：
1.确保引用格式正确，你需要保证你的引用是真实的，能在互联网上找到
2.确保图表和表格符合学术标准。
3.没有AI生成的痕迹(重要)
4.大范围编辑前，请搜索与编辑内容有关的论文文献，分析他们是怎么写的

### SourceData/

该目录下保存了原始的血糖监测数据，只读，不可修改
数据格式并不一致，包括测试间隔时间不同，部分数据缺失等
同时属性名称和单位可能存在差异
数据以csv格式保存

### tarsh/
该目录用于存放垃圾文件，可以随时删除

### src/Data/

该目录用于存放经过格式化,滤波处理，合并处理后的血糖数据，用于后续的模型训练和评估

**文件说明:**
- `origin_data_plot.ipynb`: 原始数据可视化notebook，用于读取和分析colas.csv数据

### src/DataSplit/

该目录用于存放数据集划分相关的代码和数据

#### src/DataSplit/Served/
该目录用于存放专门用于迁移学习（Transfer Learning）的保留数据集。

**文件说明:**
- `split_data.ipynb`: 数据集划分脚本
    - 读取 `src/DataFillter/sg/sg_filtered_cgm_data.csv`
    - 在排序后的受试者列表中**等间隔选取** 10 个受试者作为迁移学习集
    - 将剩余受试者作为训练/测试集
    - 将血糖列名统一重命名为 `gl`
    - 导出 `served.csv` 和 `TrainTest.csv`
- `served.csv`: 包含 10 个受试者的 S-G 滤波后数据，列名：`id`, `time`, `gl`, `age`, `bmi`。

#### src/DataSplit/TrainTest/
该目录用于存放用于预训练通用模型的大规模数据集。

**文件说明:**
- `TrainTest.csv`: 包含除 Served Set 外所有受试者的 S-G 滤波后数据，列名：`id`, `time`, `gl`, `age`, `bmi`。
- `split_train_test.ipynb`: 训练/测试集划分脚本
    - 读取 `TrainTest.csv`
    - 对每个受试者，截取**最后 6 小时** (72个点) 作为测试集
    - 剩余数据作为训练集
    - 导出 `Train.csv` 和 `Test.csv`
- `Train.csv`: 训练集数据
- `Test.csv`: 测试集数据 (每个受试者最后 6 小时)

### src/DataFormat/

该目录用于数据格式化和整合，将不同来源的原始数据统一格式后合并

**文件说明:**
- `dataformat.ipynb`: 数据格式化和整合notebook
    - 读取并整合 colas.csv 和 hall.csv 两个数据集
    - 统一列名格式（age, bmi统一为小写）
    - 提取所需列：id, time, gl, age, bmi
    - 重新编号受试者ID，避免不同数据集间的ID冲突
    - 数据质量检查（缺失值、重复值、统计摘要）
    - 过滤记录时间不足1天的受试者数据
    - 严格过滤：移除存在超过10分钟数据间隔的受试者
    - 数据重采样：对保留的受试者进行线性插值，确保严格的5分钟采样间隔
    - 导出合并后的数据集到 merged_cgm_data.csv
- `plot_merged_data.ipynb`: 合并后数据可视化notebook
    - 读取 merged_cgm_data.csv
    - 按受试者编号顺序，绘制每个受试者数据量最多的一天的血糖-时间序列图
    - 包含统计信息（均值、标准差、范围）
- `merged_cgm_data.csv`: 整合后的CGM数据集，包含colas和hall的数据
- `merged_cgm_data_YYYYMMDD.csv`: 带时间戳的备份版本

**合并数据集格式说明 (merged_cgm_data.csv):**

| 列名 | 数据类型 | 说明 | 示例值 |
|------|---------|------|--------|
| `id` | int | 受试者唯一标识符，已重新编号确保唯一性 | 1, 2, 3... |
| `time` | datetime | 血糖测量时间戳，格式：YYYY-MM-DD HH:MM:SS | 2012-01-01 00:00:00 |
| `gl` | float | 血糖值 (mg/dL) | 86.0, 93.0 |
| `age` | float | 受试者年龄 (岁) | 77.0, 59.0 |
| `bmi` | float | 体重指数 (Body Mass Index) | 25.4, 21.7 |

**数据特征:**
- 按 `id` 和 `time` 升序排序
- 所有受试者均为严格的5分钟采样间隔
- 每个受试者有多个时间点的连续血糖监测数据
- 经处理后无缺失值（通过插值填补小间隙，大间隙受试者已被移除）
- ID已重新编号：colas受试者从1开始，hall受试者紧接其后连续编号

**使用建议:**
- 读取时指定 `time` 列为datetime类型：`pd.read_csv('merged_cgm_data.csv', parse_dates=['time'])`
- 按受试者分组处理：`df.groupby('id')`
- 时序分析时需要先按 `id` 和 `time` 排序

### src/DataFillter/

该目录用于存放数据滤波和去噪相关的代码，按滤波方法分子目录存放

**文件说明:**
- `filter_comparison.ipynb`: 滤波效果对比notebook
    - 读取原始数据及三种滤波器的输出结果
    - 在同一张图上绘制 Raw, Kalman, S-G, Butterworth 的曲线进行对比
    - 帮助选择最适合的预处理方法

#### src/DataFillter/kalman/
- `kalman.ipynb`: 卡尔曼滤波处理notebook
    - 读取 `merged_cgm_data.csv`
    - 实现基于恒定速度模型(Constant Velocity Model)的卡尔曼滤波器
    - 对每个受试者的血糖数据进行平滑处理，减少传感器噪声
    - 可视化对比滤波前后的效果（Raw vs Filtered）
    - 导出滤波后的数据到 `kalman_filtered_cgm_data.csv`
- `kalman_filtered_cgm_data.csv`: 经过卡尔曼滤波处理后的数据集，包含 `gl_kalman` 列

#### src/DataFillter/sg/
- `savitzky_golay.ipynb`: Savitzky-Golay 滤波处理notebook
    - 读取 `merged_cgm_data.csv`
    - 使用 `scipy.signal.savgol_filter` 实现滤波 (Window=15, Poly=3)
    - 优势：能很好地保留血糖波动的峰值特征
    - 导出滤波后的数据到 `sg_filtered_cgm_data.csv`
- `sg_filtered_cgm_data.csv`: 经过S-G滤波处理后的数据集，包含 `gl_sg` 列

#### src/DataFillter/butterworth/
- `butterworth.ipynb`: 巴特沃斯低通滤波处理notebook
    - 读取 `merged_cgm_data.csv`
    - 使用 `scipy.signal.filtfilt` 实现双向零相位滤波 (Order=2, Cutoff=0.15)
    - 优势：有效去除高频噪声且无相位滞后
    - 导出滤波后的数据到 `butterworth_filtered_cgm_data.csv`
- `butterworth_filtered_cgm_data.csv`: 经过巴特沃斯滤波处理后的数据集，包含 `gl_butter` 列

### src/Prediction/

该目录用于存放各种预测模型的实现代码

#### src/Prediction/ARIMA/
- `arima_prediction.ipynb`: ARIMA 血糖预测模型notebook
    - 使用 statsmodels 实现 ARIMA 滚动预测
    - 包含平稳性检验 (ADF Test) 和参数定阶 (ACF/PACF)
    - 评估指标：MAE, RMSE, MAPE, RMSPE
    - 可视化：预测对比图及 Clarke Error Grid 临床评估

#### src/Prediction/CNN/
- `cnn_prediction.ipynb`: CNN 血糖预测模型notebook (PyTorch实现)
    - 使用 PyTorch 构建一维卷积神经网络 (Conv1d)
    - 自定义 Dataset 和 DataLoader 处理时序数据
    - 特征融合：卷积提取时序特征 + 全连接层融合 Age, BMI 静态特征
    - 包含完整的训练循环、Loss可视化及模型保存/加载机制 (`cnn_model.pth`)
    - 评估指标：MAE, RMSE, MAPE, RMSPE
    - 可视化：时序对比图、误差分析及 Clarke Error Grid 临床评估
    - 模拟真实场景：加载保存的模型对 Served Set 进行预测

#### src/Prediction/KNN/
- `knn_prediction.ipynb`: KNN 血糖预测模型notebook (直接多步预测版)
    - 读取 `Train.csv`, `Test.csv` 和 `served.csv`
    - 构建滑动窗口数据集，支持配置预测步长 (Horizon) 进行直接预测
    - 融合 Age, BMI 静态特征
    - 数据标准化处理
    - 训练 KNeighborsRegressor 模型

#### src/Prediction/Linear/
- `linear_prediction.ipynb`: Linear Regression 血糖预测模型notebook (直接多步预测版)
    - 读取 `Train.csv`, `Test.csv` 和 `served.csv`
    - 构建滑动窗口数据集，支持配置预测步长 (Horizon) 进行直接预测
    - 融合 Age, BMI 静态特征
    - 数据标准化处理
    - 训练 LinearRegression 模型
    - 评估指标：MAE, RMSE, MAPE, RMSPE
    - 可视化：时序对比图、误差分析及 Clarke Error Grid 临床评估

#### src/Prediction/RandomForest/
- `random_forest_prediction.ipynb`: Random Forest 血糖预测模型notebook
    - 使用 RandomForestRegressor
    - 融合 Age, BMI, Hour 特征
    - 包含数据标准化 (为了与KNN流程一致)
    - 评估指标：MAE, RMSE, MAPE, RMSPE
    - 可视化：时序对比图、误差分析及 Clarke Error Grid 临床评估

#### src/Prediction/RNN/
- `rnn_prediction.ipynb`: RNN 血糖预测模型notebook (PyTorch实现)
    - 使用 PyTorch 构建循环神经网络 (RNN)
    - 自定义 Dataset 和 DataLoader 处理时序数据
    - 特征融合：RNN提取时序特征 + 全连接层融合 Age, BMI 静态特征
    - 包含完整的训练循环、Loss可视化及模型保存/加载机制 (`rnn_model.pth`)
    - 评估指标：MAE, RMSE, MAPE, RMSPE
    - 可视化：时序对比图、误差分析及 Clarke Error Grid 临床评估
    - 模拟真实场景：加载保存的模型对 Served Set 进行预测

#### src/Prediction/LSTM/
- `lstm_prediction.ipynb`: LSTM 血糖预测模型notebook (PyTorch实现)
    - 使用 PyTorch 构建长短期记忆网络 (LSTM)
    - 自定义 Dataset 和 DataLoader 处理时序数据
    - 特征融合：LSTM提取时序特征 + 全连接层融合 Age, BMI 静态特征
    - 包含完整的训练循环、Loss可视化及模型保存/加载机制 (`lstm_model.pth`)
    - 评估指标：MAE, RMSE, MAPE, RMSPE
    - 可视化：时序对比图、误差分析及 Clarke Error Grid 临床评估
    - 模拟真实场景：加载保存的模型对 Served Set 进行预测

#### src/Prediction/Transformer/
- `transformer_prediction.ipynb`: Transformer 血糖预测模型notebook (PyTorch实现)
    - 使用 PyTorch 构建 Transformer 模型 (Encoder-only)
    - 包含位置编码 (Positional Encoding)
    - 自定义 Dataset 和 DataLoader 处理时序数据
    - 特征融合：Transformer提取时序特征 + 全连接层融合 Age, BMI 静态特征
    - 包含完整的训练循环、Loss可视化及模型保存/加载机制 (`transformer_model.pth`)
    - 评估指标：MAE, RMSE, MAPE, RMSPE
    - 可视化：时序对比图、误差分析及 Clarke Error Grid 临床评估
    - 模拟真实场景：加载保存的模型对 Served Set 进行预测

#### src/Prediction/XGBoost/
- `xgboost_prediction.ipynb`: XGBoost 血糖预测模型notebook
    - 使用 XGBRegressor
    - 融合 Age, BMI, Hour 特征
    - 无需数据标准化    - 评估指标：MAE, RMSE, MAPE, RMSPE
    - 可视化：时序对比图、误差分析及 Clarke Error Grid 临床评估

### src/feature/
该目录用于特征工程实验

**文件说明:**
- `feature_engineering.ipynb`: 特征工程实验notebook
    - 基于 LSTM 模型探究不同特征对血糖预测的影响
    - 模块化 `FeatureExtractor` 类，支持灵活添加特征组
    - 特征组：base(基础)、stat(统计)、time(时间)、diff(差分)、trend(趋势)、quantile(分位数)
    - 特征相关性分析：相关系数、热力图、时间滞后分析
    - 特征分布可视化
    - 消融实验：对比不同特征组合的预测效果
    - 最佳特征组合详细分析：训练曲线、散点图、误差分布、Clarke Error Grid

### src/Transfer/
该目录用于存放迁移学习/微调相关的代码和模型

**文件说明:**
- `transfer_learning.ipynb`: LSTM 迁移学习主流程notebook
    - 加载预训练 LSTM 模型 (`lstm_model.pth`)
    - 针对特定受试者 (ID=258) 进行个性化微调
    - 数据划分：前 50% 微调集，后 50% 测试集
    - 冻结策略：冻结 LSTM 层，只训练全连接层
    - 超参数：lr=1e-4, epochs=30
    - Baseline vs Fine-tuned 对比评估
    - 可视化：训练曲线、时序对比、误差分布、Clarke Error Grid

#### src/Transfer/models/
- `subject_258_finetuned.pth`: 针对受试者 258 微调后的个性化模型


## **输出及编码要求**
要求代码中的注释用中文
如果绘制图表，图表中的文字请使用英文
绘图和表格，遵从科研绘图的一般标准
