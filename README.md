# GlucosePrediction 血糖预测系统

基于连续血糖监测(CGM)数据的血糖预测系统，实现数据处理、多种预测模型构建与评估、迁移学习等功能。

## 项目概述

模拟商用血糖仪使用场景，即缺少多模态特征（如饮食，运动，胰岛素等），仅有基础血糖时间序列，和简单身高体重BMI等信息，同时需要低成本的构建方式，来进行血糖预测。
通过数据预处理，多种模型构建与对比，找到体积小，易部署的模型；通过特征工程，丰富时间序列特征，找到性能优异的特征组合；最后模拟真实使用场景，在少量个人血糖数据上，进行迁移学习微调，提升模型的泛化能力

### 主要功能

1.数据集选择：选用主流的CGM数据集为基础，进行后续的实验。（SourceData）
2.原始数据可视化与噪声评估：对数据集进行初步的可视化，以及评估数据中的噪声情况。（src/Data）
3.数据集过滤与重采样：对数据集进行过滤，去除异常值与缺失段，并进行重采样以统一时间间隔，最后拼接为一个csv。（src/DataFormat）
4.数据滤波：使用多种流行滤波方法对数据进行滤波处理，并评估滤波效果。（src/DataFillter）
5.数据集分割：将处理后的数据集分割为测试集/训练集/保留集，便于后续的模型训练/评估和迁移。（src/DataSplit）
6.血糖预测模型构建：使用多种主流机器学习和深度学习模型，进行血糖预测实验，包含ARIMA,CNN,KNN,Linear,LSTM,RandomForest,RNN,Transformer,XGBoost等。（src/Prediction）
7.特征工程：对血糖时间序列模型进行特征工程，提取多种时间序列特征，并评估其对模型性能的影响。（src/feature）
8.迁移学习：选定基础模型，在保留集上进行微调，模拟商用血糖仪使用场景。尝试创新的迁移策略，评估对模型泛化能力的影响（src/Transfer）

## 目录结构

```
GlucosePrediction/
├── doc/                          # 文档目录
│   └── dissertation.md           # 毕业论文
├── SourceData/                   # 原始数据（只读）
│   ├── colas.csv
│   └── hall.csv
├── src/                          # 源代码目录
│   ├── Data/                     # 数据可视化
│   ├── DataFormat/               # 数据格式化与整合
│   ├── DataFillter/              # 数据滤波处理
│   │   ├── kalman/               # 卡尔曼滤波
│   │   ├── sg/                   # Savitzky-Golay滤波
│   │   └── butterworth/          # 巴特沃斯滤波
│   ├── DataSplit/                # 数据集划分
│   │   ├── Served/               # 迁移学习保留集
│   │   └── TrainTest/            # 训练/测试集
│   ├── Prediction/               # 预测模型
│   │   ├── ARIMA/
│   │   ├── Linear/
│   │   ├── KNN/
│   │   ├── RandomForest/
│   │   ├── XGBoost/
│   │   ├── CNN/
│   │   ├── RNN/
│   │   ├── LSTM/
│   │   └── Transformer/
│   ├── feature/                  # 特征工程
│   └── Transfer/                 # 迁移学习
├── utils/                        # 工具函数
│   └── ceg_utils.py              # Clarke Error Grid工具
└── trash/                        # 临时文件
```

## 数据处理流程

### 1. 数据格式化

```
SourceData/*.csv → src/DataFormat/dataformat.ipynb → merged_cgm_data.csv
```

- 整合 Colas 和 Hall 两个数据集
- 统一列名格式：`id`, `time`, `gl`, `age`, `bmi`
- 重新编号受试者ID，确保唯一性
- 过滤记录时间不足的受试者
- 线性插值确保严格的5分钟采样间隔

### 2. 数据滤波

```
merged_cgm_data.csv → 滤波器 → *_filtered_cgm_data.csv
```

| 滤波方法 | 特点 |
|---------|------|
| 卡尔曼滤波 | 基于恒定速度模型，实时性好 |
| S-G滤波 | 保留峰值特征，推荐使用 |
| 巴特沃斯滤波 | 有效去除高频噪声，零相位滞后 |

### 3. 数据集划分

```
sg_filtered_cgm_data.csv → split_data.ipynb → served.csv + TrainTest.csv
TrainTest.csv → split_train_test.ipynb → Train.csv + Test.csv
```

- **Served Set**: 10个受试者用于迁移学习
- **Train Set**: 训练集（每个受试者除最后6小时外的数据）
- **Test Set**: 测试集（每个受试者最后6小时数据）

## 预测模型

### 传统机器学习模型

| 模型 | 文件路径 | 说明 |
|-----|---------|------|
| ARIMA | `src/Prediction/ARIMA/` | 自回归积分滑动平均模型 |
| Linear Regression | `src/Prediction/Linear/` | 线性回归 |
| KNN | `src/Prediction/KNN/` | K近邻算法 |
| Random Forest | `src/Prediction/RandomForest/` | 随机森林 |
| XGBoost | `src/Prediction/XGBoost/` | 极端梯度提升 |

### 深度学习模型

| 模型 | 文件路径 | 说明 |
|-----|---------|------|
| CNN | `src/Prediction/CNN/` | 一维卷积神经网络 |
| RNN | `src/Prediction/RNN/` | 循环神经网络 |
| LSTM | `src/Prediction/LSTM/` | 长短期记忆网络 |
| Transformer | `src/Prediction/Transformer/` | 基于注意力机制的模型 |

### 评估指标

- **MAE** (Mean Absolute Error)
- **RMSE** (Root Mean Square Error)
- **MAPE** (Mean Absolute Percentage Error)
- **RMSPE** (Root Mean Square Percentage Error)
- **Clarke Error Grid** (临床评估)

## 快速开始

### 环境要求

- Python 3.8+
- PyTorch
- pandas
- numpy
- scikit-learn
- statsmodels
- matplotlib
- xgboost

### 安装依赖

```bash
pip install torch pandas numpy scikit-learn statsmodels matplotlib xgboost scipy
```

### 运行流程

1. **数据格式化**：运行 `src/DataFormat/dataformat.ipynb`
2. **数据滤波**：运行 `src/DataFillter/sg/savitzky_golay.ipynb`
3. **数据划分**：依次运行 `src/DataSplit/` 下的 notebook
4. **模型训练**：选择 `src/Prediction/` 下的模型进行训练
5. **迁移学习**（可选）：运行 `src/Transfer/transfer_learning.ipynb`

## 数据格式

### 合并数据集格式 (merged_cgm_data.csv)

| 列名 | 数据类型 | 说明 | 示例 |
|------|---------|------|------|
| `id` | int | 受试者唯一标识符 | 1, 2, 3... |
| `time` | datetime | 血糖测量时间戳 | 2012-01-01 00:00:00 |
| `gl` | float | 血糖值 (mg/dL) | 86.0, 93.0 |
| `age` | float | 受试者年龄 (岁) | 77.0, 59.0 |
| `bmi` | float | 体重指数 | 25.4, 21.7 |

### 读取数据示例

```python
import pandas as pd

# 读取数据
df = pd.read_csv('src/DataFormat/merged_cgm_data.csv', parse_dates=['time'])

# 按受试者分组处理
for subject_id, group in df.groupby('id'):
    print(f"Subject {subject_id}: {len(group)} records")
```

## 特征工程

`src/feature/feature_engineering.ipynb` 提供了模块化的特征提取工具：

| 特征组 | 说明 |
|-------|------|
| base | 基础血糖值特征 |
| stat | 统计特征（均值、标准差等） |
| time | 时间特征（小时、星期几等） |
| diff | 差分特征（变化率） |
| trend | 趋势特征 |
| quantile | 分位数特征 |

## 迁移学习

支持基于预训练模型进行个性化微调：

1. 加载预训练的 LSTM 模型
2. 冻结 LSTM 层，只训练全连接层
3. 使用特定受试者数据进行微调
4. 评估 Baseline vs Fine-tuned 效果

## 许可证

本项目仅供学术研究使用。

## 联系方式

如有问题，请通过 Issue 联系。
