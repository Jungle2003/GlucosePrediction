# GlucosePrediction 血糖预测系统

基于连续血糖监测 (CGM) 数据的血糖预测系统，涵盖数据预处理、多种预测模型构建与对比、特征工程、迁移学习以及元学习 (Meta-Learning) 等完整实验流程。

## 项目概述

- 模拟商用血糖仪使用场景：仅依赖基础血糖时间序列与简单人口统计特征（年龄、BMI），不依赖饮食、运动、胰岛素等多模态信息
- 通过数据预处理与多种模型的构建与对比，筛选出体积小、易部署的模型
- 通过特征工程丰富时间序列特征，寻找性能最优的特征组合
- 模拟真实使用场景：基于 Transformer 预训练模型，在少量个人数据上通过迁移学习与元学习进行个性化微调，提升模型的泛化能力

### 主要功能

1. **数据集选择**：选用主流 CGM 数据集（Colas、Hall、Ohio T1D），包含**1型、2型糖尿病患者和健康个体**作为实验基础（`SourceData/`）
2. **原始数据可视化与噪声评估**：对数据集进行初步可视化，评估数据中的噪声情况（`src/Data/`）
3. **数据格式化与重采样**：过滤异常值与缺失段，重采样统一时间间隔，合并为统一格式（`src/DataFormat/`）
4. **数据滤波**：使用卡尔曼、Savitzky-Golay、巴特沃斯三种滤波方法处理数据，对比评估后选用 S-G 滤波（`src/DataFillter/`）
5. **数据集划分**：将处理后数据划分为训练集、测试集和迁移学习保留集（`src/DataSplit/`）
6. **预测模型构建**：实现 ARIMA、Linear、KNN、RandomForest、XGBoost、CNN、RNN、LSTM、Transformer 共 9 种模型进行对比实验（`src/Prediction/`）
7. **特征工程**：提取统计、时间、差分、趋势等多组特征，通过消融实验评估各特征组合的影响（`src/feature/`）
8. **迁移学习**：基于 Transformer 预训练模型，采用冻结编码器 + 微调 Head 的策略进行个性化迁移（`src/Transfer/`）
9. **元迁移学习**：实现 Reptile 元学习算法获得优质初始化参数，后续进行迁移学习微调，在极端少样本场景下与标准迁移学习进行对比（`src/Transfer/`）

## 目录结构

```
GlucosePrediction/
├── .github/                      # GitHub 配置
│   └── copilot-instructions.md   # AI 编码代理指令
├── doc/                          # 文档目录
│   └── dissertation.md           # 毕业论文
├── pictures/                     # 图片资源
├── SourceData/                   # 原始数据（只读）
│   ├── colas.csv
│   └── hall.csv
├── src/                          # 源代码目录
│   ├── Data/                     # 原始数据可视化
│   │   └── origin_data_plot.ipynb
│   ├── DataFormat/               # 数据格式化与整合
│   │   ├── dataformat.ipynb
│   │   ├── plot_merged_data.ipynb
│   │   └── merged_cgm_data.csv
│   ├── DataFillter/              # 数据滤波处理
│   │   ├── filter_comparison.ipynb
│   │   ├── kalman/               # 卡尔曼滤波
│   │   ├── sg/                   # Savitzky-Golay 滤波（推荐）
│   │   └── butterworth/          # 巴特沃斯滤波
│   ├── DataSplit/                # 数据集划分
│   │   ├── Served/               # 迁移学习保留集（10 个受试者）
│   │   │   ├── split_data.ipynb
│   │   │   └── served.csv
│   │   └── TrainTest/            # 训练/测试集
│   │       ├── split_train_test.ipynb
│   │       ├── Train.csv
│   │       └── Test.csv
│   ├── Prediction/               # 预测模型
│   │   ├── ARIMA/
│   │   ├── Linear/
│   │   ├── KNN/
│   │   ├── RandomForest/
│   │   ├── XGBoost/
│   │   ├── CNN/                  # 含预训练模型 cnn_model.pth
│   │   ├── RNN/                  # 含预训练模型 rnn_model.pth
│   │   ├── LSTM/                 # 含预训练模型 lstm_model.pth
│   │   └── Transformer/          # 含预训练模型 transformer_model.pth
│   ├── feature/                  # 特征工程
│   │   └── feature_engineering.ipynb
│   └── Transfer/                 # 迁移学习与元学习
│       ├── transformer_transfer_learning.ipynb
│       ├── transformer_meta_transfer_learning.ipynb
│       └── models/               # 微调后的个性化模型
├── utils/                        # 工具函数
│   └── ceg_utils.py              # Clarke Error Grid 工具
└── trash/                        # 临时文件
```

## 数据处理流程

### 1. 数据格式化

```
SourceData/*.csv → src/DataFormat/dataformat.ipynb → merged_cgm_data.csv
```

- 整合 Colas、Hall 和 Ohio T1D 三个数据集
- 统一列名格式：`id`, `time`, `gl`, `age`, `bmi`
- 重新编号受试者 ID，确保唯一性
- 过滤记录时间不足 1 天或存在超过 10 分钟数据间隔的受试者
- 线性插值确保严格的 5 分钟采样间隔

### 2. 数据滤波

```
merged_cgm_data.csv → 滤波器 → *_filtered_cgm_data.csv
```

| 滤波方法 | 参数 | 特点 |
|---------|------|------|
| 卡尔曼滤波 | 恒定速度模型 | 实时性好 |
| **S-G 滤波** | **Window=15, Poly=3** | **保留峰值特征，推荐使用** |
| 巴特沃斯滤波 | Order=2, Cutoff=0.15 | 有效去除高频噪声，零相位滞后 |

### 3. 数据集划分

```
sg_filtered_cgm_data.csv → split_data.ipynb → served.csv + TrainTest.csv
TrainTest.csv → split_train_test.ipynb → Train.csv + Test.csv
```

- **Served Set**: 等间隔选取 10 个受试者用于迁移学习
- **Train Set**: 训练集（每个受试者除最后 6 小时外的数据）
- **Test Set**: 测试集（每个受试者最后 6 小时 / 72 个点）

## 预测模型

### 传统机器学习模型

| 模型 | 文件路径 | 关键配置 |
|-----|---------|---------|
| ARIMA | `src/Prediction/ARIMA/` | 滚动预测，ADF 检验 + ACF/PACF 定阶 |
| Linear Regression | `src/Prediction/Linear/` | 直接多步预测，滑动窗口 |
| KNN | `src/Prediction/KNN/` | K=5，直接多步预测 |
| Random Forest | `src/Prediction/RandomForest/` | 100 棵决策树 |
| XGBoost | `src/Prediction/XGBoost/` | 100 轮, lr=0.1, max_depth=5 |

### 深度学习模型

| 模型 | 文件路径 | 关键配置 |
|-----|---------|---------|
| CNN | `src/Prediction/CNN/` | 两层 Conv1d (16→32 通道) |
| RNN | `src/Prediction/RNN/` | 隐藏维度 32 |
| LSTM | `src/Prediction/LSTM/` | 隐藏维度 32 |
| Transformer | `src/Prediction/Transformer/` | d_model=64, nhead=4, nlayers=2 |

深度学习模型统一配置：batch_size=64, Adam 优化器, lr=0.001, MSE 损失, 50 epochs

所有模型均融合 Age、BMI 静态特征，支持配置预测步长 (Prediction Horizon)。

### 评估指标

- **MAE** (Mean Absolute Error)
- **RMSE** (Root Mean Square Error)
- **MAPE** (Mean Absolute Percentage Error)
- **RMSPE** (Root Mean Square Percentage Error)
- **Clarke Error Grid**（临床评估，A+B 区占比）

## 特征工程

`src/feature/feature_engineering.ipynb` 基于 LSTM 模型，通过消融实验对比不同特征组合的效果：

| 特征组 | 说明 |
|-------|------|
| base | 基础血糖值特征 |
| stat | 统计特征（均值、标准差等） |
| time | 时间特征（小时、星期几等） |
| diff | 差分特征（变化率） |
| trend | 趋势特征 |
| quantile | 分位数特征 |

包含特征相关性分析（热力图、时间滞后分析）和最佳特征组合的详细评估（训练曲线、散点图、误差分布、Clarke Error Grid）。

## 迁移学习与元迁移学习

### Transformer 迁移学习

`src/Transfer/transformer_transfer_learning.ipynb`

- 加载预训练 Transformer 模型 (`transformer_model.pth`)
- **冻结策略**：冻结 Input Embedding + Transformer Encoder 层，仅训练全连接层 (Head)
- **数据划分**：前 30% 校准集，后 70% 测试集
- **超参数**：lr=1e-4, epochs=100, N_PAST=12, PREDICTION_HORIZON=6
- Baseline vs Fine-tuned 对比评估
- 可视化：训练曲线、时序波形对比、误差分布、Clarke Error Grid、Attention 热力图
- 覆盖 10 位受试者的多受试者验证

### 元迁移学习（Reptile 算法）

`src/Transfer/transformer_meta_transfer_learning.ipynb`

- 实现 **Reptile** 元学习算法，生成更优的初始化参数
- 对比 **Basic Transfer**（标准预训练初始化）与 **Meta Transfer**（元学习初始化）在微调阶段的性能差异
- **元训练超参数**：META_EPOCHS=1000, INNER_STEPS=5, INNER_LR=1e-3, META_LR=1e-4, TASK_BATCH=8
- **数据划分**：前 50% Pool（抽取微调样本），后 50% Test（固定测试集）
- 学习曲线对比：不同微调样本量 (10, 30, 50, ...) 下的 MAE/RMSE
- 极端少样本 (N=30) 下元迁移学习相对标准迁移学习的优势分析

### 微调模型文件

`src/Transfer/models/` 目录下保存了多位受试者的个性化微调模型：

| 文件 | 说明 |
|-----|------|
| `transformer_subject_*_finetuned.pth` | 基于 Transformer 针对特定受试者微调的个性化模型 |
| `subject_258_finetuned.pth` | 基于 LSTM 针对受试者 258 微调的个性化模型 |

## 快速开始

### 环境要求

- Python 3.8+
- PyTorch
- pandas, numpy
- scikit-learn
- statsmodels
- matplotlib
- xgboost
- scipy

### 安装依赖

```bash
pip install torch pandas numpy scikit-learn statsmodels matplotlib xgboost scipy
```

### 运行流程

1. **数据格式化**：运行 `src/DataFormat/dataformat.ipynb`
2. **数据滤波**：运行 `src/DataFillter/sg/savitzky_golay.ipynb`
3. **数据划分**：依次运行 `src/DataSplit/Served/split_data.ipynb` 和 `src/DataSplit/TrainTest/split_train_test.ipynb`
4. **模型训练**：选择 `src/Prediction/` 下的模型进行训练
5. **特征工程**（可选）：运行 `src/feature/feature_engineering.ipynb` 进行消融实验
6. **迁移学习**（可选）：运行 `src/Transfer/transformer_transfer_learning.ipynb` 进行个性化微调
7. **元迁移学习**（可选）：运行 `src/Transfer/transformer_meta_transfer_learning.ipynb` 进行元学习实验

## 数据格式

### 合并数据集格式 (merged_cgm_data.csv)

| 列名 | 数据类型 | 说明 | 示例 |
|------|---------|------|------|
| `id` | int | 受试者唯一标识符（重新编号） | 1, 2, 3... |
| `time` | datetime | 血糖测量时间戳 | 2012-01-01 00:00:00 |
| `gl` | float | 血糖值 (mg/dL) | 86.0, 93.0 |
| `age` | float | 受试者年龄 (岁) | 77.0, 59.0 |
| `bmi` | float | 体重指数 | 25.4, 21.7 |


## 许可证

本项目仅供学术研究使用。

## 联系方式

如有问题，请通过 Issue 联系。
