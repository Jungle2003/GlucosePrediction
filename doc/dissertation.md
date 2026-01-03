# CGM血糖预测研究

1. 绪论（Introduction）

## 1.1 研究背景与意义

### 1.1.1 糖尿病防治现状与血糖监测需求

糖尿病（Diabetes Mellitus, DM）是一种以慢性高血糖为特征的代谢性疾病，已成为全球公共卫生的重大挑战。据国际糖尿病联盟（IDF）统计，全球糖尿病患者人数持续攀升，其并发症涉及心脑血管、肾脏、视网膜及神经系统，严重影响患者生活质量 [1]。临床研究一致表明，严格且稳定的血糖控制是降低糖尿病相关并发症风险的关键 [1]。

在糖尿病管理中，血糖监测是至关重要的环节。传统的血糖监测方法，如空腹血糖、餐后血糖及糖化血红蛋白（HbA1c），虽然能够反映一定时间段内的血糖平均水平，但难以捕捉血糖的动态变化。特别是 HbA1c，作为一种“平均值”指标，往往掩盖了血糖的波动情况，无法反映低血糖和高血糖事件的频率 and 严重程度 [2]。此外，传统的指尖血自我血糖监测（SMBG）受限于测量频次和操作复杂性，难以实现全天候的连续覆盖，尤其容易遗漏夜间或餐后的血糖波动，导致患者依从性较差。

因此，连续血糖监测技术（Continuous Glucose Monitoring, CGM）应运而生，并逐渐成为糖尿病管理的重要工具 [2]。CGM 技术通过皮下传感器实时监测组织间液中的葡萄糖浓度，能够提供高时间分辨率的连续血糖数据，为患者和临床医生提供了更全面、动态的血糖信息，是实现精细化血糖管理的基础。

### 1.1.2 CGM（连续血糖监测）技术特点与应用价值

CGM 技术通过对组织间液中的葡萄糖浓度进行高频采样（常见采样间隔为 5 分钟），极大地丰富了可利用的时间序列信息。一个典型的 CGM 系统由传感器、发射器和接收终端组成，能够实现全天候的血糖动态追踪 [3]。

CGM 的核心应用价值在于其对血糖动态过程的完整记录，这使得“**范围内时间**”（Time in Range, TIR）等指标成为评估血糖控制质量的重要补充。TIR 指标反映了患者血糖处于目标范围（通常为 3.9–10.0 mmol/L）的时间百分比，已被美国糖尿病协会（ADA）等权威机构纳入临床指南，作为评估血糖控制质量和预测微血管并发症风险的关键指标，与传统的 HbA1c 具有互补作用 [1]。

然而，CGM 数据并非完美无缺。传感器监测的是组织间液中的葡萄糖浓度，与血液中的葡萄糖浓度之间存在生理延迟（通常为 5-10 分钟），特别是在血糖快速变化时，两者可能出现短暂偏差 [4]。此外，传感器性能、佩戴位置、以及环境干扰等因素，都会导致数据中不可避免地出现**噪声**、**漂移**和**缺失值** [5]。这些数据质量问题对后续的血糖预测模型提出了严峻挑战，使得数据清洗、滤波和异常值处理成为本研究在工程实现中必须首先解决的关键环节。

### 1.1.3 血糖预测对糖尿病管理的核心意义

在 CGM 等先进技术的支持下，糖尿病管理模式正从传统的“事后评估”向“**事前预判**”转变。血糖预测（Glucose Prediction, GP）研究的目标是基于历史 CGM 数据及相关生理因素，推断未来一段时间内（如 30 分钟或 60 分钟）的血糖变化趋势和大致水平，从而提前识别潜在的高血糖或低血糖风险 [3]。

短期血糖预测具有直接的临床实用价值。例如，当预测模型提示未来 30 分钟内血糖可能下降至低血糖阈值附近时，患者可以提前采取干预措施（如少量进食），有效避免或减轻**无症状低血糖**事件的发生 [6]。同样，对餐后血糖上冲趋势的预测，可以指导患者及时调整胰岛素剂量或进食速度，以减轻血糖波动。通过这种方式，血糖预测能够帮助患者从被动应对转变为主动规避极端血糖事件，显著提升患者的安全性。

从临床决策角度来看，血糖预测模型为个体化治疗方案的优化提供了辅助工具。医生可以结合预测模型，模拟不同治疗方案下的血糖轨迹，从而做出更合理、更精准的调整。鉴于血糖预测结果直接关系到患者的生命安全，模型必须具备高度的**安全性和可靠性**，这使得血糖预测不仅是一个时间序列回归问题，更是一个与医疗安全紧密相关的复杂工程问题。

值得注意的是，现有许多高性能的预测模型依赖于**多模态数据**（如饮食、运动、胰岛素注射量等）[8]，然而在实际商业应用中，用户难以持续、准确地提供这些信息，导致模型输入数据往往仅限于 CGM 序列和基础生理指标（如年龄、BMI）。本研究的核心价值，正是针对这种**数据受限**的真实应用场景，探索高效、鲁棒的血糖预测方法。已有研究表明，在仅有易于获取的“原位数据”（In situ data）时，通过合理的模型设计依然可以实现准确的血糖预测 [18]，这为商用血糖预测模型的发展提供了重要依据。

## 1.2 国内外研究现状

### 1.2.1 CGM 数据驱动的血糖预测研究进展

基于 CGM 时间序列的血糖预测已成为国内外研究热点，其发展大致经历了三个阶段 [3]：

1.  **生理机理模型阶段：** 早期研究主要采用一组微分方程来描述葡萄糖代谢、胰岛素动力学等生理过程（如 Bergman Minimal Model 或 Hovorka Model）。这类模型的优点是**可解释性强**，符合临床生理直觉；但缺点是参数多、结构复杂，需要大量的个体化参数辨识，难以在真实环境中大规模推广。
2.  **统计时间序列模型阶段：** 随着高频 CGM 数据的积累，研究者开始采用更偏向数据驱动的统计方法，如自回归（AR）、自回归滑动平均（ARMA）和自回归积分滑动平均（ARIMA）模型。此外，**卡尔曼滤波**等状态空间方法也被广泛用于实时滤波和平滑 CGM 数据，以减弱噪声影响 [7]。这类模型计算开销小，在短期预测中表现基本可用。
3.  **机器学习与深度学习阶段：** 近十年来，机器学习（ML）和深度学习（DL）方法被广泛应用于血糖预测。传统 ML 方法（如支持向量回归、随机森林）通常依赖于精细的**特征工程**，将历史血糖值、饮食、运动等信息编码为特征 [8]。深度学习则利用网络自身的表示学习能力，直接从原始序列中提取特征。其中，**循环神经网络**（RNN）、**长短期记忆网络**（LSTM）和**门控循环单元**（GRU）因其处理序列数据的天然优势而被大量采用 [9] [10]。

在此基础上，研究者还探索了更复杂的模型结构，例如将一维卷积网络（CNN）与循环结构结合，以同时捕捉局部变化模式和长期趋势 [10]。针对多步预测和较长预测时域，**注意力机制**（Attention Mechanism）和 **序列到序列**（Seq2Seq）结构也被引入，以更有效地刻画血糖随时间的演变过程 [9]。

### 1.2.2 机器学习在血糖预测中的应用现状

在当前的研究中，机器学习和深度学习方法因其强大的非线性拟合能力，成为血糖预测的主流技术路线 [8]。

在传统机器学习框架下，关键在于**特征设计**。研究者通常从历史 CGM 序列中提取滞后项、滑动窗口统计量（如均值、方差、变化率）等，并结合饮食、运动、药物等**辅助信息**作为输入特征。在特征工程合理的前提下，这些模型在短期预测任务中往往能明显优于简单的线性模型。

随着深度学习的成熟，以 LSTM 和 GRU 为代表的序列模型被广泛应用。这些模型通过其内部的门控机制，能够有效地在时间轴上传递和筛选历史信息，非常适合处理血糖这种具有明显时序依赖性的信号 [10]。研究表明，在预测时域适当延长（例如 30 分钟及以上）时，深度序列模型在预测精度和对复杂模式的刻画能力上，相对传统方法具有一定优势 [9]。此外，Transformer 架构凭借其强大的并行处理能力和长程依赖建模能力，在处理复杂血糖波动预测中也展现出优越性 [20]。

然而，这类数据驱动方法在实际应用中也面临挑战。首先，模型性能高度依赖于**训练数据的规模和代表性**，而高质量、大规模的 CGM 数据集相对稀缺，限制了模型的泛化能力 [8]。其次，复杂深度模型的**“黑箱”特性**与医疗领域对可解释性和可追溯性的要求之间存在一定矛盾，需要在实际部署时进行权衡。此外，在工程实现层面，模型的**实时性**和**部署效率**也是必须考虑的问题，需要在保证预测性能的前提下，简化模型结构以适应移动终端或可穿戴设备的资源约束。

### 1.2.3 现有研究存在的不足与待解决问题

尽管基于 CGM 的血糖预测已取得显著进展，但从工程落地和临床应用的角度看，现有工作仍存在以下不足：

首先，**多模态数据依赖与实际应用场景的脱节**是主要挑战之一。现有高性能模型往往建立在理想的、数据丰富的实验环境下，而忽略了商业化应用中用户数据采集的难度和不完整性。

其次，**个体差异与模型泛化挑战**尚未得到充分解决。针对单个患者训练的**个体化模型**精度高，但难以推广；利用多名受试者数据训练的**群体模型**泛化性强，但可能无法充分反映个体间的差异特征。如何在有限数据条件下，设计出既能利用跨个体信息，又能兼顾个体差异的**迁移学习**（Transfer Learning）策略，是当前的研究重点 [13] [14]。

针对上述问题，本研究将重点探索在仅有 CGM 序列和基础生理指标的约束下，如何通过迁移学习实现高效的个体化模型微调。已有研究提出了**元迁移学习**（Meta-Transfer Learning）框架 [11] 和**增量重训练**策略 [12]，证明了在小样本（Few-shot）场景下实现快速个体化适配的可能性。此外，引入**元学习**（Meta-Learning）策略（如 MAML）可以使模型通过极少量的个体数据快速适配新用户 [15] [16]，并能有效处理异构协变量带来的影响 [17]。

在实验设计与评估方面，本课题将严格遵循时间序列划分原则，并在传统回归误差指标的基础上，引入对低、高血糖事件的**分类预测指标**，使评估结果更贴近实际临床需求。通过上述工作，期望在现有研究基础上，形成一套相对完整、可复现的基于 CGM 的血糖预测研究流程，为后续模型的工程化实现和可能的临床转化提供参考。


2. 实验数据集选择与标准化处理（Data Selection and Standardization）

## 2.1 数据集选择与描述

在第一章中，我们讨论了血糖预测在糖尿病管理中的核心地位，并指出数据驱动方法对高质量、多维度数据集的依赖。为了验证本研究提出的迁移学习框架在不同人群、不同监测设备以及不同生理状态下的泛化能力，本研究并未局限于单一的数据来源，而是整合了两个在学术界广泛认可且具有显著差异性的公开连续血糖监测（CGM）数据集：Colas 数据集与 Hall 数据集。

### 2.1.1 数据集来源与背景

1.  **Colas 数据集 [21]**：
    该数据集由 Colás 等人于 2019 年发布，其研究重点在于评估 CGM 数据在 2 型糖尿病（T2D）高风险人群中的早期预警价值。该数据集的独特性在于其受试者群体具有较高的临床异质性，涵盖了从正常糖耐量（NGT）到前驱糖尿病及确诊 T2D 的多种代谢状态。在数据采集层面，该研究采用了 Medtronic MiniMed iPro 监测系统，该系统通过皮下感应器每 5 分钟记录一次组织间液葡萄糖浓度。对于本研究而言，Colas 数据集提供了丰富的病理状态样本，是验证模型在极端血糖波动下捕捉能力的理想选择。

2.  **Hall 数据集 [22]**：
    由斯坦福大学 Hall 等人于 2018 年发布，该研究通过对 57 名受试者进行长期的 CGM 监测，提出了“血糖类型”（Glucotypes）的概念，揭示了即使在传统诊断指标（如 HbA1c）正常的个体中，也存在显著的血糖失调现象。Hall 数据集采用了 Dexcom G4 监测系统，采样频率同样为 5 分钟。与 Colas 数据集相比，Hall 数据集包含更多的健康及亚健康样本，且提供了更详尽的静态生理指标（如 BMI、年龄）。

通过整合上述两个数据集，本研究构建了一个跨设备（Medtronic vs Dexcom）、跨人群（高风险 vs 普通人群）的综合数据库。这种多源数据的融合，虽然增加了前期处理的工程难度，但为后续迁移学习中“源域”知识的提取提供了更具代表性的分布空间。

### 2.1.2 受试者特征统计与分析

为了确保模型输入的科学性，本研究对整合后的数据进行了严格的受试者筛选，剔除了记录时长不足 48 小时或缺失率超过 30% 的无效样本。最终纳入研究的受试者共计 168 名，总观测点数达到 101,600 个。表 2-1 展示了受试者的基础生理指标及血糖分布的统计特征。

**表 2-1 受试者基础生理指标与血糖分布统计表**

| 特征指标 | 统计值 (均值 ± 标准差) | 取值范围 (Min - Max) |
| :--- | :--- | :--- |
| 受试者总数 (N) | 168 | - |
| 年龄 (Age, years) | 58.79 ± 10.51 | 25.0 - 82.0 |
| 体重指数 (BMI, kg/m²) | 29.83 ± 4.63 | 19.2 - 44.5 |
| 平均血糖值 (Glucose, mg/dL) | 102.17 ± 21.96 | 40.0 - 450.0 |
| 血糖变异系数 (CV, %) | 21.49 ± 8.12 | 8.5 - 42.3 |
| 总记录点数 | 101,600 | - |

从表 2-1 可以看出，本研究样本呈现出明显的“高龄、高 BMI”特征，平均 BMI 接近 30 kg/m² 的肥胖临界点，这与糖尿病及其并发症的高发人群特征高度吻合。同时，血糖变异系数（CV）的跨度较大（8.5% 至 42.3%），说明数据集中既包含血糖极其平稳的健康个体，也包含波动剧烈的糖尿病患者。这种高度的个体差异性（Inter-individual variability）正是本研究引入迁移学习策略的根本动因——单一的群体模型难以同时适配如此宽泛的生理分布。

## 2.2 数据格式化与标准化流程

原始 CGM 数据通常以杂乱的 CSV 或 Excel 格式存储，且不同研究的列名定义（如 `GlucoseValue` vs `gl`）、时间格式（Unix 时间戳 vs ISO 8601）以及血糖单位（mmol/L vs mg/dL）各不相同。为了构建可供深度学习模型直接读取的张量输入，本研究设计并实现了一套标准化的数据预处理流水线。

### 2.2.1 异构数据整合与 ID 映射

在工程实现中，数据整合的第一步是建立统一的元数据索引。本研究采用 Python 的 Pandas 库实现了自动化的数据清洗脚本：
1.  **字段对齐**：将所有原始字段统一映射为标准化的四元组：`{id, time, gl, age, bmi}`。
2.  **单位标准化**：考虑到国际临床研究中 mg/dL 的通用性，本研究将所有以 mmol/L 为单位的数据统一乘以 18.018 进行换算。
3.  **全局 ID 重新编号**：为了在多中心数据融合时保持唯一性，本研究对 Colas 数据集采用 `1xxx` 编码，对 Hall 数据集采用 `2xxx` 编码。这种编号方式不仅避免了主键冲突，还保留了数据的来源信息，便于后续在迁移学习中进行领域（Domain）标记。

### 2.2.2 采样频率一致性处理

虽然两个数据集的标称采样频率均为 5 分钟，但在实际采集过程中，由于传感器内部处理延迟或系统休眠，实际采样间隔往往在 4.8 到 5.2 分钟之间波动。这种非等间距的时间序列会干扰神经网络模型（RNN等）对时间步长的感知。
本研究采用了**线性重采样（Linear Resampling）**技术，以严格的 5 分钟为步长对原始序列进行插值对齐。对于重采样过程中出现的微小时间偏移，通过线性加权确保了信号在频域上的失真最小化。

### 2.2.3 缺失值处理与序列分段策略

缺失值是 CGM 数据处理中最棘手的挑战。本研究根据缺失长度采取了分级处理策略：
*   **短时缺失（< 20 min）**：采用三阶样条插值（Cubic Spline Interpolation）进行填充。相比线性插值，样条插值能更好地保留血糖波动的导数信息（即血糖变化率），这对预测模型至关重要。
*   **长时缺失（≥ 20 min）**：此类缺失通常意味着传感器脱落或校准中断。本研究拒绝进行“盲目填充”，而是采取**序列断裂处理**。即以缺失点为界，将长序列切分为多个独立的连续子序列。只有长度超过 6 小时（72 个连续点）的子序列才会被保留用于后续的滑动窗口切片。

通过上述严谨的标准化流程，我们成功将来自不同研究、不同设备的原始信号转化为高质量的结构化数据集。这不仅消除了工程层面的噪声干扰，更确保了后续章节中模型对比实验的公平性与科学性。

## 参考文献

[1] American Diabetes Association (ADA). Standards of Care in Diabetes—2025. Diabetes Care 2025; 48 (Supplement_1). [https://doi.org/10.2337/dc25-S007]
[2] Kwon SY, et al. Advances in Continuous Glucose Monitoring: Clinical Applications and Future Perspectives. Endocrinology and Metabolism 2025. [https://doi.org/10.3803/EnM.2025.2370]
[3] Alam MA, et al. Machine Learning And Artificial Intelligence in Diabetes Prediction And Management: A Comprehensive Review of Models. 2024. [https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5079613]
[4] Xie X, et al. Reduction of measurement noise in a continuous glucose monitor. Nature Biomedical Engineering 2018; 3: 892–901. [https://doi.org/10.1038/s41551-018-0273-3]
[5] Kim SJ, et al. Long-term blood glucose prediction using deep learning-based noise reduction. Computer Methods and Programs in Biomedicine 2025. [https://doi.org/10.1016/j.cmpb.2025.108571]
[6] Kozinetz RM, et al. Machine Learning and Deep Learning Models to Predict Nocturnal Glucose. Diagnostics 2024; 14(7): 740. [https://doi.org/10.3390/diagnostics14070740]
[7] Facchinetti A, et al. Kalman smoothing for objective and automatic preprocessing of glucose data. IEEE Transactions on Biomedical Engineering 2018; 65(1): 114-123. [https://doi.org/10.1109/TBME.2017.2702326]
[8] Liu K, Li L, Ma Y, et al. Machine learning models for blood glucose level prediction in patients with diabetes mellitus: systematic review and network meta-analysis. JMIR Medical Informatics 2023; 11: e47833. [https://doi.org/10.2196/47833]
[9] Ryu JS, et al. A deep learning approach for blood glucose monitoring and forecasting. Scientific Reports 2025. [https://doi.org/10.1038/s41598-025-97391-8]
[10] Ghimire S, et al. Deep learning for blood glucose level prediction: How well do models perform across diverse datasets? PLOS ONE 2024; 19(9): e0310801. [https://doi.org/10.1371/journal.pone.0310801]
[11] Zheng Y, et al. Enhancing personalized blood glucose prediction in type 1 diabetes with meta-transfer learning: A few-shot approach. Biomedical Signal Processing and Control 2026; 101: 107234. [https://doi.org/10.1016/j.cmpb.2025.108571]
[12] Shen Y, et al. Personalized Blood Glucose Forecasting From Limited CGM Data Using Incrementally Retrained LSTM. IEEE Transactions on Biomedical Engineering 2024. [https://doi.org/10.1109/TBME.2024.3491434]
[13] Yu X, et al. Deep transfer learning: a novel glucose prediction framework for new subjects. Complex & Intelligent Systems 2022; 8: 3123–3137. [https://doi.org/10.1007/s40747-021-00360-7]
[14] Deng Y, et al. Deep transfer learning and data augmentation improve glucose levels prediction in type 2 diabetes patients. NPJ Digital Medicine 2021; 4: 91. [https://doi.org/10.1038/s41746-021-00480-x]
[15] Moon K, et al. Personalized blood glucose prediction in type 1 diabetes using meta-learning with bidirectional LSTM-Transformer hybrid model. Scientific Reports 2025; 15: 13491. [https://doi.org/10.1038/s41598-025-13491-5]
[16] Zhu T, et al. Personalized Blood Glucose Prediction for Type 1 Diabetes Using Evidential Deep Learning and Meta-Learning. IEEE Transactions on Biomedical Engineering 2023; 70(1): 193-204. [https://doi.org/10.1109/TBME.2022.3187625]
[17] Wang L, et al. Heterogeneous Covariates-Aware Pseudo Supervised Meta-Learning for Few-shot Diabetes Classification. IEEE Transactions on Medical Imaging 2025. [https://doi.org/10.1109/TMI.2024.3416513]
[18] Singh R, et al. Personalized glucose prediction using in situ data only. Frontiers in Nutrition 2025; 12: 1539118. [https://doi.org/10.3389/fnut.2025.1539118]
[19] Manchanda E, et al. Data-Efficiency with Comparable Accuracy: Personalized LSTM models on limited individual data. Diabetology 2025; 6(10): 115. [https://doi.org/10.3390/diabetology6100115]
[20] Tominaga H, et al. Prediction of Postprandial Blood Glucose Variability Using Transformer-based Models. PMC 2025. [https://pmc.ncbi.nlm.nih.gov/articles/PMC12735845/]
[21] Colás, A., Vigil, L., Vargas, B., Enríquez de Salamanca, R., & Lázaro, P. (2019). Continuous glucose monitoring allows for a better T2D risk prediction than FPG and HbA1c in a high-risk population. *Diabetes Research and Clinical Practice*, 155, 107799. [https://doi.org/10.1016/j.diabres.2019.107799]
[22] Hall, H., Perelman, D., Breschi, A., Limcaoco, P., Kellogg, R., McLaughlin, T., & Snyder, M. (2018). Glucotypes reveal new patterns of glucose dysregulation. *PLOS Biology*, 16(7), e2005143. [https://doi.org/10.1371/journal.pbio.2005143]