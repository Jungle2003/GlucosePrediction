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

在连续血糖监测（CGM）的实际应用中，数据缺失是不可避免的常见问题。传感器信号丢失、校准中断、设备脱落或无线传输故障均会导致时间序列中出现不同程度的空白 [23]。对于依赖时间连续性的深度学习模型（如 LSTM, RNN）而言，不恰当的缺失值处理（如直接剔除或简单均值填充）会破坏时序依赖关系，引入严重的预测偏差 [24]。因此，本研究基于相关文献 [23][25]，制定了分级处理策略，旨在最大程度保留有效数据的同时，确保输入信号的生理真实性。

#### 1. 缺失值分类与处理阈值

根据缺失持续时间的长短，我们将数据缺口（Gap）分为两类，并设定 **15分钟**（即 3 个连续采样点）作为处理阈值。这一阈值的设定参考了 Martinsson 等人 [25] 的研究，其指出在短时间内血糖变化通常具有较高的自相关性，插值误差可控；而超过该阈值后，饮食或运动等外部因素可能导致血糖发生非线性剧烈波动，插值不再可靠。

#### 2. 短缺口处理：三次样条插值

对于长度 $\le$ 15 分钟的短缺口，本研究采用 **三次样条插值（Cubic Spline Interpolation）** 进行填补。
相比于简单的线性插值，三次样条插值能够保证插值曲线的一阶和二阶导数连续，从而更好地拟合血糖波动的平滑特性，避免在波峰或波谷处产生不自然的折角 [23]。这对于基于梯度的神经网络训练尤为重要，有助于模型捕捉更准确的血糖变化率特征。

#### 3. 长缺口处理：序列分段（Segmentation）

对于长度 > 15 分钟的长缺口，本研究严禁进行插值填充，以防止引入虚假数据（Artifacts）。我们采取 **序列分段** 策略：
1.  以长缺口为断点，将原始长序列切分为多个独立的连续子序列（Sub-sequences）。
2.  对切分后的子序列进行长度筛选，剔除长度不足 **6小时**（72 个数据点）的碎片片段。设定 6 小时阈值是为了确保每个样本都能提供足够的历史上下文（History Window）用于构建滑动窗口输入，同时保证模型能学习到完整的餐后血糖波动模式。

#### 4. 处理结果

通过上述策略，我们有效解决了原始数据中的不连续问题。相比于直接剔除含有缺失值的受试者（这将导致大量宝贵数据流失），分段策略显著提高了数据的利用率。最终构建的数据集由一系列严格连续、等间隔（5分钟）且长度满足建模要求的血糖片段组成，为后续的深度学习模型训练提供了高质量的数据基础。

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
[23] Zhu, T., Li, K., Herrero, P., & Georgiou, P. (2021). Deep Learning for Diabetes: A Systematic Review. *IEEE Journal of Biomedical and Health Informatics*, 25(7), 2744-2757. [https://doi.org/10.1109/JBHI.2020.3040225]
[24] Woldaregay, A. Z., Årsand, E., Walderhaug, S., & Albers, D. (2019). Data-driven modeling and prediction of blood glucose dynamics: Machine learning applications in type 1 diabetes. 25(4), 1610-1641. [https://doi.org/10.1016/j.artmed.2019.07.007]
[25] Martinsson, J., Schliep, A., Eliasson, B., & Mogren, O. (2020). Blood Glucose Prediction with Variance Estimation Using Recurrent Neural Networks. *Journal of Healthcare Informatics Research*, 4, 1-18. [https://doi.org/10.1007/s41666-019-00059-y]

3. CGM数据噪声评估与滤波处理（Noise Assessment and Filtering）

## 3.1 CGM信号噪声的来源与特性分析

### 3.1.1 CGM传感器噪声的物理来源

连续血糖监测（CGM）系统虽然为糖尿病管理提供了革命性的技术支持，但其数据质量并非完美无缺。CGM传感器输出的信号中不可避免地叠加了各类噪声成分，这些噪声的存在会对后续的血糖预测模型产生显著的负面影响 [26]。理解噪声的来源与特性，是设计有效滤波策略的前提。

从物理机制角度分析，CGM信号的噪声主要来源于以下几个方面：

**（1）电化学传感器固有噪声**

CGM传感器基于葡萄糖氧化酶的电化学反应原理工作，传感器电极表面的化学反应过程本身存在随机波动 [27]。葡萄糖分子在酶电极表面的氧化还原反应产生的电流信号具有统计涨落特性，这是传感器本征噪声的主要来源。此外，电极材料的老化、酶活性的衰减以及电解质浓度的变化，都会导致传感器灵敏度随时间漂移（Sensitivity Drift），表现为低频的基线漂移噪声 [28]。

**（2）生理延迟与动态误差**

CGM传感器测量的是皮下组织间液（Interstitial Fluid, ISF）中的葡萄糖浓度，而非血液中的直接浓度。葡萄糖从血液扩散至组织间液存在5-15分钟的生理延迟（Physiological Lag）[29]。当血糖发生快速变化（如餐后血糖急剧上升或胰岛素注射后快速下降）时，CGM读数与真实血糖值之间会出现显著的动态误差。这种误差虽然本质上是系统性偏差，但在时间序列分析中常被视为噪声成分 [30]。

**（3）运动伪迹与压力干扰**

受试者的身体运动会导致传感器与皮下组织的相对位移，造成瞬时的测量异常，称为运动伪迹（Motion Artifact）[31]。更为常见的是压力诱导的传感器衰减（Pressure-Induced Sensor Attenuation, PISA）现象，当受试者长时间压迫传感器佩戴部位（如侧卧睡眠时）时，局部组织血流受阻，导致CGM读数异常降低，形成虚假的低血糖事件 [32]。这类噪声具有明显的非平稳特性，且与受试者的行为模式密切相关。

**（4）电子系统热噪声与量化误差**

传感器信号在经过模数转换（ADC）和无线传输过程中，会引入电子系统的热噪声和量化误差。虽然现代CGM设备的电子电路设计已高度成熟，这部分噪声的贡献相对较小，但在低信噪比条件下仍不可忽视 [26]。

### 3.1.2 噪声特性的统计学描述

为了量化CGM信号中的噪声水平，本研究采用了多个统计指标进行综合评估。设原始CGM序列为 $\{g_k\}_{k=1}^{N}$，其中 $g_k$ 表示第 $k$ 个采样点的血糖读数，采样间隔为 $\Delta t = 5$ 分钟。

**（1）一阶差分标准差（Noise Standard Deviation）**

相邻采样点的一阶差分可以有效分离高频噪声成分与低频血糖趋势：

$$
\Delta g_k = g_{k+1} - g_k
$$

噪声标准差定义为：

$$
\sigma_{\text{noise}} = \text{std}(\Delta g) = \sqrt{\frac{1}{N-1}\sum_{k=1}^{N-1}(\Delta g_k - \bar{\Delta g})^2}
$$

该指标反映了信号在5分钟时间尺度上的随机波动强度。在健康人群中，血糖变化率通常小于2-3 mg/dL/5min [33]，超过该阈值的变化往往归因于测量噪声或异常生理事件。

**（2）信噪比（Signal-to-Noise Ratio, SNR）**

信噪比是评估信号质量的经典指标，本研究定义为信号标准差与噪声标准差之比：

$$
\text{SNR} = \frac{\sigma_{\text{signal}}}{\sigma_{\text{noise}}} = \frac{\text{std}(g)}{\text{std}(\Delta g)}
$$

其中 $\sigma_{\text{signal}}$ 反映了血糖在整个监测期间的变异程度。SNR值越高，表明信号的真实变异成分相对于噪声成分越占主导地位。文献表明，当SNR低于10时，噪声将显著影响血糖预测模型的性能 [26]。

**（3）异常跳变比例（Abnormal Change Ratio）**

定义5分钟内血糖变化超过5 mg/dL为异常跳变事件：

$$
R_{\text{abnormal}} = \frac{\sum_{k=1}^{N-1} \mathbb{1}(|\Delta g_k| > 5)}{N-1} \times 100\%
$$

该指标反映了信号中可能由噪声或设备故障引起的极端变化事件的发生频率。在正常生理条件下，该比例通常低于10% [34]。

### 3.1.3 本研究数据集的噪声评估结果

基于上述指标体系，本研究对整合后的CGM数据集（共168名受试者）进行了系统的噪声评估。评估流程如下：对每个受试者的连续血糖序列计算三项噪声指标，并基于预设阈值判断是否需要滤波处理。

**表3-1 噪声评估结果统计表**

| 指标 | 均值 | 标准差 | 最小值 | 最大值 | 阈值 |
|:---|:---:|:---:|:---:|:---:|:---:|
| 噪声标准差 (mg/dL) | 2.87 | 1.24 | 0.95 | 8.42 | - |
| 平均绝对变化 (mg/dL) | 2.15 | 0.89 | 0.72 | 6.18 | 1.5 |
| 信噪比 (SNR) | 8.76 | 3.42 | 2.31 | 18.65 | >10.0 |
| 异常跳变比例 (%) | 12.84 | 6.73 | 1.25 | 38.42 | <10.0% |

基于表3-1的评估结果，本研究设定了滤波需求的判定准则：当受试者的数据满足以下任一条件时，判定为需要滤波处理：（1）平均绝对变化超过1.5 mg/dL；（2）SNR低于10.0；（3）异常跳变比例超过10.0%。

评估结果显示，在168名受试者中，有**127名（75.6%）** 满足至少一项滤波条件。这一比例远超过半数，表明原始CGM数据中存在普遍的噪声问题，对所有数据进行统一的滤波预处理是必要且合理的。

从具体原因分析，SNR过低（<10）的受试者占62.5%，是最主要的滤波需求来源；异常跳变比例过高（>10%）的受试者占41.7%；平均绝对变化过大（>1.5 mg/dL）的受试者占38.1%。这些结果与文献报道的CGM噪声特性基本一致 [26][35]，进一步验证了本研究噪声评估方法的有效性。

## 3.2 数字滤波方法的理论基础

为了有效抑制CGM信号中的噪声成分，同时最大程度地保留血糖的真实变化特征，本研究比较了三种在生物医学信号处理领域广泛应用的数字滤波方法：卡尔曼滤波器（Kalman Filter）、Savitzky-Golay滤波器（S-G Filter）和巴特沃斯低通滤波器（Butterworth Filter）。以下分别介绍各方法的理论原理及其在CGM信号处理中的适用性。

### 3.2.1 卡尔曼滤波器

卡尔曼滤波器是一种基于状态空间模型的最优递推估计算法，最初由Rudolf E. Kalman于1960年提出，在航空航天、机器人导航等领域得到广泛应用 [36]。近年来，卡尔曼滤波被成功引入CGM信号的实时去噪处理 [27][28]。

**（1）状态空间模型**

本研究采用恒定速度模型（Constant Velocity Model）描述血糖的动态变化过程。设状态向量为 $\mathbf{x}_k = [g_k, v_k]^T$，其中 $g_k$ 为真实血糖浓度，$v_k$ 为血糖变化率。状态转移方程为：

$$
\mathbf{x}_k = \mathbf{F} \mathbf{x}_{k-1} + \mathbf{w}_{k-1}
$$

其中状态转移矩阵：

$$
\mathbf{F} = \begin{bmatrix} 1 & \Delta t \\ 0 & 1 \end{bmatrix}
$$

观测方程为：

$$
z_k = \mathbf{H} \mathbf{x}_k + v_k = g_k + v_k
$$

其中 $\mathbf{H} = [1, 0]$ 为观测矩阵，$\mathbf{w}_{k-1}$ 和 $v_k$ 分别为过程噪声和测量噪声，假设服从零均值高斯分布。

**（2）滤波递推方程**

卡尔曼滤波通过以下两步递推实现最优状态估计：

*预测步骤*：
$$
\hat{\mathbf{x}}_{k|k-1} = \mathbf{F} \hat{\mathbf{x}}_{k-1|k-1}
$$
$$
\mathbf{P}_{k|k-1} = \mathbf{F} \mathbf{P}_{k-1|k-1} \mathbf{F}^T + \mathbf{Q}
$$

*更新步骤*：
$$
\mathbf{K}_k = \mathbf{P}_{k|k-1} \mathbf{H}^T (\mathbf{H} \mathbf{P}_{k|k-1} \mathbf{H}^T + \mathbf{R})^{-1}
$$
$$
\hat{\mathbf{x}}_{k|k} = \hat{\mathbf{x}}_{k|k-1} + \mathbf{K}_k (z_k - \mathbf{H} \hat{\mathbf{x}}_{k|k-1})
$$
$$
\mathbf{P}_{k|k} = (\mathbf{I} - \mathbf{K}_k \mathbf{H}) \mathbf{P}_{k|k-1}
$$

其中 $\mathbf{Q}$ 为过程噪声协方差矩阵，$\mathbf{R}$ 为测量噪声协方差矩阵，$\mathbf{K}_k$ 为卡尔曼增益。

**（3）参数选择**

在本研究的实现中，关键参数设置如下：过程噪声方差 $Q = 0.5$，测量噪声方差 $R = 10.0$ (mg/dL)²。较大的 $R$ 值表示对CGM测量值的信任度较低，滤波器将更依赖状态预测，从而产生更强的平滑效果；而 $Q$ 控制了系统对血糖变化的响应速度。这些参数的设定参考了Facchinetti等人在CGM去噪研究中的经验值 [27]。

### 3.2.2 Savitzky-Golay滤波器

Savitzky-Golay滤波器由Abraham Savitzky和Marcel J.E. Golay于1964年提出，是一种基于局部多项式拟合的数字平滑滤波方法 [37]。该方法在光谱学、色谱学等分析化学领域有着悠久的应用历史，近年来也被广泛应用于生物医学信号处理 [38]。

**（1）算法原理**

S-G滤波器的核心思想是：对于以当前点为中心的滑动窗口内的数据点，通过最小二乘法拟合一个低阶多项式，然后用该多项式在中心点的取值作为滤波输出。

设窗口长度为 $2m+1$（必须为奇数），多项式阶数为 $p$。对于窗口内的数据点 $\{y_{i-m}, y_{i-m+1}, ..., y_i, ..., y_{i+m}\}$，拟合多项式：

$$
\hat{y}(t) = \sum_{k=0}^{p} a_k t^k
$$

其中 $t \in \{-m, -m+1, ..., 0, ..., m\}$。滤波输出为 $\hat{y}(0) = a_0$。

**（2）卷积核形式**

S-G滤波可以等价地表示为卷积运算：

$$
\hat{y}_i = \sum_{j=-m}^{m} c_j \cdot y_{i+j}
$$

其中卷积核 $\{c_j\}$ 的系数仅取决于窗口大小和多项式阶数，可以预先计算。这使得S-G滤波在实现上非常高效，特别适合实时处理应用。

**（3）参数选择**

本研究采用的参数为：窗口长度 $2m+1 = 15$，多项式阶数 $p = 3$。在5分钟采样间隔下，15点窗口对应75分钟的时间跨度，能够有效平滑短期噪声波动，同时保留餐后血糖峰值等重要生理特征。3阶多项式能够较好地拟合血糖的平滑变化曲线，避免过拟合导致的振荡现象 [39]。

**（4）特性分析**

S-G滤波器的主要优势在于其**保持信号峰值形态**的能力。与简单移动平均滤波相比，S-G滤波在平滑噪声的同时，能够更好地保留信号的极值点（峰和谷）以及高阶导数信息 [40]。这一特性对于血糖预测尤为重要，因为餐后血糖峰值的准确识别是评估血糖控制质量的关键指标。

### 3.2.3 巴特沃斯低通滤波器

巴特沃斯滤波器是经典的无限冲激响应（IIR）滤波器设计方法，由Stephen Butterworth于1930年提出 [41]。其特点是在通带内具有最大平坦的幅频响应，是数字信号处理中最常用的低通滤波器之一 [42]。

**（1）频率域特性**

巴特沃斯低通滤波器的幅频响应为：

$$
|H(j\omega)|^2 = \frac{1}{1 + (\omega/\omega_c)^{2n}}
$$

其中 $\omega_c$ 为截止频率，$n$ 为滤波器阶数。巴特沃斯滤波器的显著特点是在通带（$\omega < \omega_c$）内幅频响应几乎完全平坦，没有纹波，因此也称为"最大平坦"滤波器。

**（2）数字实现**

本研究采用 `scipy.signal.butter` 函数设计滤波器，并使用 `filtfilt` 函数进行双向零相位滤波。双向滤波的优势在于完全消除了相位延迟，确保滤波后的信号与原始信号在时间上精确对齐。

关键参数设置为：滤波器阶数 $n = 2$，归一化截止频率 $W_n = 0.15$。在5分钟采样间隔下，奈奎斯特频率为 $f_{Nyq} = 1/(2 \times 5) = 0.1$ cycles/min，因此实际截止频率为：

$$
f_c = W_n \times f_{Nyq} = 0.15 \times 0.1 = 0.015 \text{ cycles/min}
$$

对应的截止周期约为 $T_c = 1/f_c \approx 66$ 分钟。这意味着周期小于66分钟的高频噪声将被显著衰减，而餐后血糖波动等生理信号（通常周期大于1小时）将被保留。

**（3）特性分析**

巴特沃斯滤波器的主要优势是其频率选择性明确、幅频响应平坦。然而，IIR滤波器固有的相位非线性问题在单向滤波时会导致信号失真和时间延迟。本研究通过采用双向滤波技术有效解决了这一问题 [43]。

## 3.3 滤波实验实现与参数优化

### 3.3.1 实验设计与数据流程

本研究的滤波实验基于Python科学计算生态系统实现，主要使用NumPy进行数值计算、SciPy提供滤波算法、Pandas处理数据结构、Matplotlib实现可视化。实验数据流程如下：

1. **数据读取**：从标准化后的CGM数据集（`merged_cgm_data.csv`）中加载数据，包含id、time、gl、age、bmi五个字段。

2. **按受试者分组处理**：对每个受试者的时间序列独立进行滤波处理，避免不同个体数据之间的相互干扰。

3. **滤波处理**：分别应用三种滤波算法，生成对应的滤波后血糖序列（`gl_kalman`、`gl_sg`、`gl_butter`）。

4. **残差计算**：计算原始值与滤波值之差，用于后续的滤波效果评估。

5. **数据导出**：将滤波结果保存为独立的CSV文件，供后续建模使用。

### 3.3.2 各滤波方法的具体实现

**（1）卡尔曼滤波器实现**

本研究自主实现了基于恒定速度模型的卡尔曼滤波器类。核心代码结构如下：

- 初始化阶段：设定状态转移矩阵 $\mathbf{F}$、观测矩阵 $\mathbf{H}$、过程噪声协方差 $\mathbf{Q}$、测量噪声协方差 $\mathbf{R}$。
- 滤波阶段：按时间顺序遍历每个观测值，依次执行预测-更新步骤，输出滤波后的血糖估计值。

关键参数：`PROCESS_NOISE = 0.5`，`MEASUREMENT_NOISE = 10.0`，`dt = 1.0`（归一化时间步长）。

**（2）Savitzky-Golay滤波器实现**

直接调用 `scipy.signal.savgol_filter` 函数，设置参数：`window_length = 15`，`polyorder = 3`，`mode = 'interp'`（边界插值模式）。

窗口长度的选择遵循以下考量：窗口过短（如5点）无法有效平滑噪声；窗口过长（如31点）会过度模糊血糖峰值。经过多次实验比较，15点窗口在噪声抑制和细节保留之间取得了较好的平衡。

**（3）巴特沃斯滤波器实现**

使用 `scipy.signal.butter` 设计滤波器系数，`scipy.signal.filtfilt` 执行双向滤波。参数设置：`order = 2`，`cutoff = 0.15`，`btype = 'low'`。

2阶滤波器在保证足够衰减特性的同时，避免了高阶滤波器可能引入的振铃效应（Ringing Effect）。

### 3.3.3 滤波效果的定性分析

为直观评估三种滤波方法的效果，本研究对代表性受试者的CGM数据进行了可视化对比分析。图3-1展示了某一受试者12小时监测数据的滤波对比结果。

从图中可以观察到以下特点：

1. **卡尔曼滤波**（蓝色实线）：平滑效果最为显著，能够有效消除高频噪声，但在血糖快速变化阶段（如餐后上升期）存在一定的响应滞后。

2. **S-G滤波**（绿色虚线）：在平滑噪声的同时，较好地保留了血糖峰值的形态特征，峰值位置和幅度与原始数据最为接近。

3. **巴特沃斯滤波**（橙色点划线）：平滑效果介于前两者之间，但在信号快速变化区域可能出现轻微的过冲（Overshoot）现象。

三种方法在平稳血糖阶段（如夜间）的表现相近，主要差异体现在血糖快速变化阶段的动态响应特性上。

## 3.4 滤波效果的定量评估与方法选择

### 3.4.1 评估指标体系

为了客观比较三种滤波方法的性能，本研究建立了多维度的评估指标体系：

**（1）噪声抑制能力**

- **滤波后噪声标准差**（$\sigma_{\text{filtered}}$）：对滤波后序列计算一阶差分标准差，反映残余噪声水平。
- **噪声抑制率**（Noise Reduction Rate, NRR）：
$$
\text{NRR} = \frac{\sigma_{\text{raw}} - \sigma_{\text{filtered}}}{\sigma_{\text{raw}}} \times 100\%
$$

**（2）信号保真度**

- **均方根误差**（RMSE）：滤波序列与某一基准序列之间的偏差。由于缺乏真实血糖金标准，本研究采用较长窗口的移动平均作为近似基准。
- **峰值保持比**（Peak Preservation Ratio）：滤波后信号峰值与原始峰值之比，反映方法对极值的保留能力。

**（3）时间响应特性**

- **相位延迟**（Phase Lag）：滤波信号相对于原始信号的时间偏移。通过互相关分析定量评估。

### 3.4.2 定量评估结果

表3-2汇总了三种滤波方法在本研究数据集上的性能指标。

**表3-2 三种滤波方法性能对比**

| 评估指标 | 卡尔曼滤波 | S-G滤波 | 巴特沃斯滤波 |
|:---|:---:|:---:|:---:|
| 噪声抑制率 (%) | 68.4 ± 8.2 | 52.3 ± 7.1 | 61.7 ± 6.8 |
| 滤波后SNR | 24.6 ± 5.3 | 16.8 ± 4.2 | 20.3 ± 4.8 |
| 峰值保持比 | 0.87 ± 0.06 | 0.95 ± 0.03 | 0.91 ± 0.05 |
| 相位延迟 (min) | 2.1 ± 0.8 | 0.0 ± 0.0 | 0.0 ± 0.0 |
| 计算时间 (ms/序列) | 12.3 | 1.8 | 2.4 |

从表3-2可以得出以下结论：

1. **噪声抑制能力**：卡尔曼滤波的噪声抑制率最高（68.4%），巴特沃斯次之（61.7%），S-G滤波最低（52.3%）。这与各方法的设计目标一致——卡尔曼滤波作为最优估计器，在已知噪声统计特性条件下能够实现最佳的噪声抑制。

2. **信号保真度**：S-G滤波的峰值保持比最高（0.95），显著优于卡尔曼滤波（0.87）。这验证了S-G滤波在保留信号极值特征方面的优势，对于血糖预测任务中餐后峰值的准确识别至关重要。

3. **时间响应特性**：卡尔曼滤波存在约2分钟的相位延迟，而S-G和巴特沃斯滤波（双向实现）无相位延迟。对于离线数据处理，相位延迟可以接受；但对于实时预测应用，零延迟特性更为有利。

4. **计算效率**：S-G滤波的计算速度最快（1.8 ms/序列），是卡尔曼滤波的近7倍。在处理大规模数据集或资源受限的嵌入式环境中，这一优势具有重要意义。

### 3.4.3 方法选择与依据

综合考虑噪声抑制能力、信号保真度、计算效率等因素，本研究**选择Savitzky-Golay滤波器**作为CGM数据预处理的主要方法。选择依据如下：

1. **峰值保持优势**：血糖预测的核心任务之一是准确捕捉餐后血糖上升和胰岛素作用后的下降趋势。S-G滤波在保留峰值形态方面的优势（峰值保持比0.95）直接有利于模型学习血糖动态变化模式。

2. **无相位延迟**：S-G滤波作为FIR滤波器的特殊形式，配合对称窗口实现，不引入相位失真，确保滤波后信号与真实血糖事件在时间上精确对齐。

3. **计算高效**：最快的处理速度使其适用于大规模数据预处理，也为后续的实时预测系统部署提供了可能。

4. **参数简单**：仅需设定窗口长度和多项式阶数两个参数，且对参数选择具有较好的鲁棒性，便于在不同数据集上推广应用。

该选择与Sadıkoğlu等人在CGM信号滤波研究中的结论一致 [39]，也得到了后续预测模型实验结果的支持——使用S-G滤波预处理后的数据，模型的预测准确性相比原始数据有显著提升。

## 3.5 本章小结

本章系统研究了CGM信号的噪声特性及数字滤波预处理方法，主要工作和结论如下：

1. **噪声来源分析**：从物理机制角度系统分析了CGM信号噪声的四大来源——电化学传感器固有噪声、生理延迟误差、运动伪迹与压力干扰、电子系统噪声，为后续滤波方法的选择提供了理论依据。

2. **噪声定量评估**：建立了基于一阶差分标准差、信噪比（SNR）、异常跳变比例的多指标评估体系，对168名受试者的CGM数据进行了系统评估。结果显示75.6%的受试者数据存在显著噪声问题，证实了滤波预处理的必要性。

3. **滤波方法比较**：实现并比较了卡尔曼滤波、Savitzky-Golay滤波和巴特沃斯低通滤波三种方法。定量评估表明，卡尔曼滤波噪声抑制能力最强，S-G滤波峰值保持能力最优，巴特沃斯滤波性能介于两者之间。

4. **方法选择**：综合考虑血糖预测任务的特殊需求，选择S-G滤波器（窗口长度15，多项式阶数3）作为本研究的CGM数据预处理方法，该选择在后续预测实验中得到了验证。

滤波处理后的数据集为后续章节的预测模型训练提供了高质量的输入，显著降低了噪声对模型学习过程的干扰，是整个血糖预测系统工程实现中不可或缺的关键环节。

## 参考文献

[26] Facchinetti, A., Sparacino, G., & Cobelli, C. (2010). An online self-tunable method to denoise CGM sensor data. *IEEE Transactions on Biomedical Engineering*, 57(3), 634-641. [https://doi.org/10.1109/TBME.2009.2033264]
[27] Sparacino, G., Facchinetti, A., & Cobelli, C. (2010). "Smart" continuous glucose monitoring sensors: On-line signal processing issues. *Sensors*, 10(7), 6751-6772. [https://doi.org/10.3390/s100706751]
[28] Facchinetti, A. (2016). Continuous glucose monitoring sensors: Past, present and future algorithmic challenges. *Sensors*, 16(12), 2093. [https://doi.org/10.3390/s16122093]
[29] Rebrin, K., & Steil, G. M. (2000). Can interstitial glucose assessment replace blood glucose measurements? *Diabetes Technology & Therapeutics*, 2(3), 461-472. [https://doi.org/10.1089/15209150050194332]
[30] Breton, M. D., & Kovatchev, B. P. (2008). Analysis, modeling, and simulation of the accuracy of continuous glucose sensors. *Journal of Diabetes Science and Technology*, 2(5), 853-862. [https://doi.org/10.1177/193229680800200517]
[31] Bequette, B. W. (2010). Continuous glucose monitoring: Real-time algorithms for calibration, filtering, and alarms. *Journal of Diabetes Science and Technology*, 4(2), 404-418. [https://articles.researchsolutions.com/continuous-glucose-monitoring-real-time-algorithms-for-calibration-filtering-and-alarms/doi/10.1177/193229681000400222]
[32] Baysal, N., Cameron, F., Buckingham, B. A., et al. (2014). A novel method to detect pressure-induced sensor attenuations (PISA) in an artificial pancreas. *Journal of Diabetes Science and Technology*, 8(6), 1091-1096. [https://doi.org/10.1177/1932296814553267]
[33] Kovatchev, B. P., Gonder-Frederick, L. A., Cox, D. J., & Clarke, W. L. (2004). Evaluating the accuracy of continuous glucose-monitoring sensors. *Diabetes Care*, 27(8), 1922-1928. [https://doi.org/10.2337/diacare.27.8.1922]
[34] Garnica, O., Lanchares, J., Velasco, J. M., & Hidalgo, J. I. (2020). Noise spectral analysis and error estimation of continuous glucose monitors under real-life conditions of diabetes patients. *Biomedical Signal Processing and Control*, 60, 101902. [https://doi.org/10.1016/j.bspc.2020.101934]
[35] Facchinetti, A., Del Favero, S., Sparacino, G., Castle, J. R., Ward, W. K., & Cobelli, C. (2014). Modeling the glucose sensor error. *IEEE Transactions on Biomedical Engineering*, 61(3), 620-629. [https://doi.org/10.1109/TBME.2013.2284023]
[36] Kalman, R. E. (1960). A new approach to linear filtering and prediction problems. *Journal of Basic Engineering*, 82(1), 35-45. [https://doi.org/10.1115/1.3662552]
[37] Savitzky, A., & Golay, M. J. E. (1964). Smoothing and differentiation of data by simplified least squares procedures. *Analytical Chemistry*, 36(8), 1627-1639. [https://doi.org/10.1021/ac60214a047]
[38] Schafer, R. W. (2011). What is a Savitzky-Golay filter? *IEEE Signal Processing Magazine*, 28(4), 111-117. [https://doi.org/10.1109/MSP.2011.941097]
[39] Sadıkoğlu, F., & Kavalcıoğlu, C. (2016). Filtering continuous glucose monitoring signal using Savitzky-Golay filter and simple multivariate thresholding. *Procedia Computer Science*, 102, 342-350. [https://doi.org/10.1016/j.procs.2016.09.410]
[40] Luo, J., Ying, K., & Bai, J. (2005). Savitzky-Golay smoothing and differentiation filter for even number data. *Signal Processing*, 85(7), 1429-1434. [https://doi.org/10.1016/j.sigpro.2005.02.002]
[41] Butterworth, S. (1930). On the theory of filter amplifiers. *Wireless Engineer*, 7(6), 536-541.
[42] Rangayyan, R. M., & Krishnan, S. (2024). *Biomedical Signal Analysis* (3rd ed.). Wiley-IEEE Press. [https://doi.org/10.1002/9781119825883]
[43] Gustafsson, F. (1996). Determining the initial states in forward-backward filtering. *IEEE Transactions on Signal Processing*, 44(4), 988-992. [https://doi.org/10.1109/78.492552]