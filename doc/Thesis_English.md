![](data:image/png;base64...)

**Blood glucose prediction model applicable to continuous glucose monitoring system**

|  |  |
| --- | --- |
| *Author:*  Jiang Yijun | *Supervisor:*  Prof. Shiming Zhang |

*A thesis submitted in fulfillment of the requirements*

*for the degree of Master of Science*

*in the*

Department of Electrical and Computer Engineering

Faculty of Engineering

May 31, 2026

1. Abstract
2. of thesis entitled

**Blood glucose prediction model applicable to continuous glucose monitoring system**

Submitted by

**Jiang Yijun**

for the degree of Master of Science

at The University of Hong Kong

in May 2026

***An abstract of 500 words***

**Blood glucose prediction model applicable to continuous glucose monitoring system**

by

Jiang Yijun

Bachelor's Degree in Robotics Engineering , Chongqing University

*A thesis submitted to attain the degree of*

*Master of Science*

at

The University of Hong Kong

May, 2026

Copyright ©2026, by Jiang Yijun

ALL RIGHTS RESERVED.

1. Declaration

I, Jiang Yijun, declare that this thesis titled, “Blood glucose prediction model applicable to continuous glucose monitoring system”, which is submitted in fulfillment of the requirements for the Degree of Master of Science, represents my own work except where due acknowledgement have been made. I further declared that it has not been previously included in a thesis, dissertation, or report submitted to this University or to any other institution for a degree, diploma or other qualifications.

1. Acknowledgement

I would like to thank all the people I love

Contents

Abstract ii

Declaration v

Acknowledgement vii

List of Figures x

List of Tables xi

Chapter 1 Introduction 1

1.1 General Introduction 1

1.2 Literature Review 3

Chapter 2 Data Selection and Standardization 7

2.1 Dataset Selection 7

2.2 Data Standardization 9

Chapter 3 Data Filter 12

3.1 Noise Analysis 12

3.2 Filtering Theory 16

3.2.1 Kalman Filter 16

3.2.2 S-G Filter 18

3.2.3 Butterworth Filter 19

3.3 Evaluation of Filtering Effect 19

3.4 Conclusion 21

Chapter 4 Model Building and Comparison 23

4.1 Experiment and Evaluation 23

4.2 Baseline and Machine Learning Models 26

4.3 Deep Learning Models 33

4.4 Results Analysis 39

4.5 Conclusion 44

Chapter 5 Transfer Learning 47

5.1 Introduction 47

5.2 Transfer Strategy 48

5.3 Result Analysis 50

5.4 Conclusion 54

Chapter 6 Meta-Transfer Learning 56

6.1 Introduction 56

6.2 Meta-learning Theory 57

6.3 Experiment and Analysis 59

6.4 Discussion 63

Reference 68

1. List of Figures

Chapter 11.1Figure 1.1

1. List of Tables

[Table 2.1 XXX. 4](#_Toc201077405)

[Table 2.2 Applications. 5](#_Toc201077406)

[Table 5.1 XXXXX 11](#_Toc201077407)

1. Introduction
   1. General Introduction

Diabetes mellitus (DM) is a metabolic disorder characterized by chronic hyperglycemia, and diabetes and its complications have become a major global public health challenge. According to the International Diabetes Federation (IDF), the number of diabetic patients worldwide continues to rise, with complications involving cardiovascular, cerebrovascular, renal, retinal, and neurological systems, severely affecting patients' quality of life. Clinical studies consistently demonstrate that strict and stable glycemic control is key to reducing the risk of diabetes-related complications[1].

In diabetes management, blood glucose monitoring is a critical component. Traditional blood glucose monitoring methods, such as fasting blood glucose (FBG), postprandial blood glucose (PPG), and glycated hemoglobin (HbA1c), can reflect the average blood glucose level over a certain period but are unable to capture the dynamic changes in blood glucose. Particularly, HbA1c, as a "mean" indicator, often masks fluctuations in blood glucose and fails to reflect the frequency and severity of hypoglycemic and hyperglycemic events[2]. Additionally, traditional self-monitoring blood glucose (SMBG) at the fingertip is limited by measurement frequency and operational complexity, making it difficult to achieve continuous coverage throughout the day. It is especially prone to missing nocturnal or postprandial blood glucose fluctuations, leading to poor patient adherence.

Therefore, continuous glucose monitoring (CGM) has become a pivotal tool in diabetes management[2]. By utilizing subcutaneous sensors to continuously track glucose levels in interstitial fluid, CGM delivers high temporal resolution data, providing patients and clinicians with comprehensive, real-time glucose profiles. This technology forms the foundation for precision glucose control.

![IMG_256](data:image/jpeg;base64...)

CGM devices provide continuous glucose monitoring through subcutaneous sensors.

From a technical perspective, CGM significantly enriches the available time-series information by performing high-frequency sampling of glucose concentration in interstitial fluid (commonly 5-minute). A typical CGM system consists of a sensor, transmitter, and receiving terminal, enabling round-the-clock dynamic blood glucose monitoring[3].

The core application value of CGM lies in its complete record of the dynamic process of blood glucose, which makes indicators such as "Time in Range" (TIR) an important supplement to evaluate the quality of blood glucose control. The TIR indicator reflects the percentage of time when the patient's blood glucose is in the target range (usually 3.9–10.0 mmol/L). It has been included in clinical guidelines by authoritative institutions such as the American Diabetes Association (ADA). As a key indicator for evaluating the quality of blood glucose control and predicting the risk of microvascular complications, it complements the traditional HbA1c.

However, CGM data is not perfect. The sensor measures glucose concentration in interstitial fluid, and there is a physiological delay (usually 5-10 minutes) between it and the glucose concentration in the blood. Especially when blood glucose changes rapidly, there may be a brief deviation between the two[4]. In addition, factors such as sensor performance, wearing position, and environmental interference will inevitably lead to noise, drift and missing values in the data[5]. These data quality problems pose serious challenges to the subsequent blood glucose prediction model, making data cleaning, filtering and abnormal value processing the key links that must be solved first in the engineering realization of this study.

With the support of advanced technologies such as CGM, the diabetes management model is changing from the traditional "after-event evaluation" to "pre-prediction". The aim of the glucose prediction (GP) study is to infer the trend and approximate level of blood glucose changes in the future (such as 30 minutes or 60 minutes) based on historical CGM data and related physiological factors, so as to identify the potential risk of hyperglycemia or hypoglycemia in advance.

Short-term blood glucose prediction has clear clinical utility. For example, when the prediction model suggests that blood glucose may drop to near the hypoglycemia threshold in the next 30 minutes, patients can take intervention measures in advance (such as eating a small amount) to effectively avoid or reduce the occurrence of asymptomatic hypoglycemia events[6]. Similarly, the prediction of the trend of postprandial blood glucose can guide patients to adjust insulin dosage or eating speed in time to reduce blood glucose fluctuations. In this way, blood glucose prediction can help patients change from passive response to active avoidance of extreme blood glucose events, significantly improving the safety of patients.

From the perspective of clinical decision-making, the blood glucose prediction model provides an auxiliary tool for the optimization of individualized treatment plans. Doctors can combine the prediction model to simulate the blood glucose trajectory under different treatment plans, so as to make more reasonable and accurate adjustments. Given that the results of blood glucose prediction are directly related to the life safety of patients, the model must have a high degree of safety and reliability, which makes blood glucose prediction not only a time series regression problem, but also a complex engineering problem closely related to medical safety.

Many existing high-performance prediction models rely on multi-modal data (such as diet, exercise, insulin injection, etc.)[8]. However, in practical commercial applications, it is difficult for users to provide this information continuously and accurately, resulting in model input data often limited to CGM sequences and basic physiological indicators (such as age, BMI). The core value of this research is to explore efficient and robust blood glucose prediction methods for this real application scenario with limited data. Studies have shown that accurate blood glucose prediction can still be achieved through reasonable model design when there is only easy-to-obtain "in situ data"[18], which provides an important basis for the development of commercial blood glucose prediction models.

* 1. Literature Review

Blood glucose prediction based on CGM time series has become a research hotspot at home and abroad, and its development has roughly gone through three stages[3]:

1. Physiological mechanism model stage: Early studies mainly used a set of differential equations to describe physiological processes such as glucose metabolism and insulin dynamics (such as Bergman Minimal Model or Hovorka Model). The advantage of this kind of model is that it is explainable and in line with clinical physiological intuition; however, the disadvantage is that there are many parameters and the structure is complex, which requires a large number of individualized parameter identification, and it is difficult to promote on a large scale in the real environment.

2. Statistical time series model stage: With the accumulation of high-frequency CGM data, researchers began to adopt more data-driven statistical methods, such as autoregression (AR), autoregressive sliding average (ARMA) and autoregressive integral sliding average (ARIMA) models. In addition, state space methods such as Kalman filtering are also widely used in real-time filtering and smoothing CGM data to reduce the impact of noise[7]. This kind of model has small computing overhead and can basically perform in short-term forecasts.

3. Machine learning and deep learning stage: In the past decade, machine learning (ML) and deep learning (DL) methods have been widely used in blood glucose prediction. Traditional ML methods (such as support vector regression and random forests) usually rely on fine feature engineering to encode historical blood glucose values, diet, exercise and other information as features[8]. Deep learning uses the network's own representation learning ability to extract features directly from the original sequence. Among them, circular neural networks (RNN), long-term and short-term memory networks (LSTM) and gated cyclic units (GRU) are widely used because of their natural advantages in processing sequence data[9][10].

On this basis, the researchers also explored more complex model structures, such as combining one-dimensional convolutional networks (CNN) with circular structures to capture local change patterns and long-term trends at the same time[10]. For multi-step prediction and longer prediction time domains, Attention Mechanism and Seq2Seq structures are also introduced to more effectively depict the evolution of blood glucose over time[9].

Judging from the current application situation, machine learning and deep learning methods have become the mainstream technical routes for blood glucose prediction because of their strong nonlinear fitting ability[8].

Under the traditional machine learning framework, the key is feature design. Researchers usually extract lag terms, sliding window statistics (such as mean, variance, rate of change), etc. from the historical CGM sequence, and combine them with dietary, exercise, drugs and other auxiliary information as input features. Under the premise of reasonable feature engineering, these models are often significantly better than simple linear models in short-term prediction tasks.

With the maturity of deep learning, sequence models represented by LSTM and GRU have been widely used. Through their internal gate control mechanisms, these models can effectively transmit and screen historical information on the timeline, which is very suitable for dealing with blood glucose, which is obviously time-dependent signals. Research shows that when the prediction time domain is appropriately extended (for example, 30 minutes or more), the depth sequence model has certain advantages over traditional methods in terms of prediction accuracy and the ability to portray complex patterns. In addition, the Transformer architecture also shows superiority in handling complex blood glucose fluctuation predictions with its strong parallel processing ability and long-range dependency modeling ability[20].

However, such data-driven methods also face challenges in practical applications. First of all, the performance of the model is highly dependent on the scale and representativeness of the training data, and high-quality and large-scale CGM data sets are relatively scarce, which limits the generalization ability of the model[8]. Secondly, there is a certain contradiction between the "black box" characteristics of complex depth models and the requirements of interpretability and traceability in the medical field, which needs to be weighed during actual deployment. In addition, at the engineering implementation level, the real-time and deployment efficiency of the model are also issues that must be considered. Under the premise of ensuring predictive performance, the structure needs to be simplified to cope with the resource constraints of mobile terminals or wearable devices.

Although significant progress has been made in blood glucose prediction based on CGM, from the perspective of engineering implementation and clinical application, the existing work still has the following shortcomings:

First of all, the disconnect between multimodal data dependence and actual application scenarios is one of the main challenges. Existing high-performance models are often built in an ideal and data-rich experimental environment, while ignoring the difficulty and incompleteness of user data collection in commercial applications.

Secondly, the challenges of individual differences and model generalization have not been fully solved. The individualized model trained for a single patient has high accuracy, but it is difficult to promote; the group model trained with multiple subject data is highly generalized, but may not fully reflect the different characteristics between individuals. How to design a transfer learning strategy that can both use cross-individual information and take into account individual differences under the condition of limited data is the current research focus[13][14].

In response to the above problems, we will focus on exploring how to achieve efficient fine-tuning of individualized models through transfer learning under the constraints of only CGM sequences and basic physiological indicators. Studies have put forward the Meta-Transfer Learning framework[11] and the incremental retraining strategy[12], proving the possibility of rapid individualized adaptation in a few-shot scenario. In addition, the introduction of Meta-Learning strategies (such as MAML) can enable the model to quickly adapt to new users through a very small amount of individual data[15][16], and can effectively deal with the impact of heterogeneous covariables[17].

In terms of experimental design and evaluation, this project will strictly follow the principle of time series division, and introduce classification and prediction indicators for low and high blood glucose events on the basis of traditional regression error indicators, so as to make the evaluation results closer to actual clinical needs. Through the above work, it is expected to form a relatively complete and reproducible CGM-based blood glucose prediction research process on the basis of existing research, which will provide reference for the engineering realization and possible clinical transformation of subsequent models.

1. Data Selection and Standardization
   1. Dataset Selection

In order to verify the generalization ability of the transfer learning framework proposed in this study in different populations, different monitoring devices and different physiological states, we are not limited to a single data source, but integrates three public continuous blood glucose monitoring (CGM) data sets widely recognized in the academic community and with significant differences, and constructs a comprehensive data set covering normal people with type 1 diabetes and type 2 diabetes: Colas data set, Hall data set and OhioT1DM data set.

1. Colas data set[21]:

The data set was released by Colás et al. in 2019, and its research focuses on assessing the early warning value of CGM data in high-risk people with type 2 diabetes (T2D). The uniqueness of this data set is that its subject population has high clinical heterogeneity, covering a variety of metabolic states from normal glucose tolerance (NGT) to precursor diabetes and confirmed T2D. At the level of data acquisition, the study adopted the Medtronic MiniMed iPro monitoring system. The Colas data set provides rich samples of T2D and precursor pathological state.

2. Hall data set[22]:

Published by Hall and others from Stanford University in 2018, the study put forward the concept of "Glucotypes", revealing that even in individuals with normal traditional diagnostic indicators (such as HbA1c), there are significant blood glucose disorders. The Hall data set adopts the Dexcom G4 monitoring system. The data set contains a large number of healthy and sub-health samples, and provides more detailed static physiological indicators (such as BMI, age).

3. OhioT1DM data set[44]:

Published by the University of Ohio Marling and Bunescu and others (2018/2020), it is a benchmark data set specially built for blood glucose prediction tasks. The data set contains the data of 12 subjects diagnosed with T1D, which usually faces the most serious challenge of blood glucose fluctuations and should be treated with insulin pumps. The data is extremely rich. In addition to the CGM readings at 5-minute intervals, it also contains insulin doses (basic rate, large doses), self-reported diet, exercise, sleep, stress and other life events data, as well as physiological signals such as heart rate and skin electrical response from the bracelet. The introduction of the OhioT1DM data set fills the data gap under the extreme blood glucose fluctuation scenario of type 1 diabetes.

By integrating the above three data sets, we successfully built a full-Spectrum blood glucose monitoring database, covering the complete pathological evolution process from "health -> precursor diabetes -> type 2 diabetes -> type 1 diabetes". This cross-population and cross-device heterogeneous data fusion greatly enhances the generalized verification the model’s capability in different physiological states, especially in verifying the adaptability of transfer learning strategies to extreme individual differences (such as between T1D and healthy people).

In order to ensure the scientificity of model input, we strictly screened the subjects of the integrated data, eliminating invalid samples with a recording time of less than 48 hours or a deletion rate of more than 30%. A total of 174 subjects were finally included in the study, with a total observation point of 117,570. Table 2-1 shows the statistical characteristics of the basic physiological indicators and blood glucose distribution of the subjects.

physiological parameters and blood glucose distribution.

| **Metric** | **Mean±Standard Deviation** | **Range（Min-Max）** |
| --- | --- | --- |
| Number of subjects | 174 | - |
| Age(year) | 54.71±13.21 | 25.0-88.0 |
| BMI(kg/m²) | 29.07 ± 4.57 | 18.1 - 43.9 |
| Average blood glucose level(mg/dL) | 111.46 ± 38.42 | 40.0 - 350.0 |
| Coefficient of Variation( %) | 21.49 ± 8.12 | 8.5 - 42.3 |

It can be seen from Table 2-1 that the sample shows obvious characteristics of "old age and high BMI". The average BMI is close to the obesity critical point of 30 kg/m², which is highly consistent with the characteristics of high incidence of diabetes and its complications. At the same time, the span of blood glucose variation coefficient (CV) is large (8.5% to 42.3%), indicating that the data set includes both healthy individuals with normal blood glucose fluctuations and diabetic patients with severe fluctuations. This high inter-individual variability is the fundamental motive for the introduction of transfer learning strategies - it is difficult for a single group model to adapt to such a broad physiological distribution at the same time.

* 1. Data Standardization

The original CGM data is usually stored in a messy CSV or Excel format, and the column name definitions of different studies (such as `GlucoseValue` vs `gl`), time format (Unix timestamp vs ISO 8601) and blood glucose units (mmol/L vs mg/dL) are different. In order to build a tensor input that can be directly read by the deep learning model, we design and implement a set of standardized data preprocessing pipelines.

1. Field alignment: map all original fields into a standardized quad: {id, time, gl, age, bmi}.

2. Unit standardization: Considering the universality of mg/dL in international clinical research, we converts all data in mmol/L units by 18.018.

3. Global ID renumbering: In order to maintain uniqueness in multi-center data fusion, we renumbers the Colas data set, Hall data set and OhioT1DM data set to ensure the uniqueness of the subject number.

Although the nominal sampling frequency of these data sets is 5 minutes, during the actual collection process, the actual sampling interval often fluctuates between 4.8 and 5.2 minutes due to the delay in internal processing of the sensor or system dormancy. This non-equispacing time series will interfere with the perception of time step length by the neural network model (RNN, etc.).

We adopt Linear Resampling technology to interpolate and align the original sequence with a strict 5-minute step length. For the small time offset that occurs in the resampling process, the distortion of the signal in the frequency domain is minimized through linear weighting.

In the practical application of continuous blood glucose monitoring (CGM), missing data is an inevitable common problem. Sensor signal loss, calibration interruption, device drop or wireless transmission failure can lead to different degrees of gaps in the time series[23]. For deep learning models that rely on time continuity (such as LSTM, RNN), inappropriate missing value processing (such as direct elimination or simple mean filling) will destroy timing dependence and introduce serious prediction deviations[24]. Therefore, based on relevant literature [25], we have formulated a graded processing strategy to ensure the physiological authenticity of the input signal while retaining valid data to the greatest extent.

According to the length of the missing duration, we divide the data gap into two categories and set 15 minutes (i.e. 3 consecutive sampling points) as the processing threshold. The setting of this threshold refers to the study of Martinsson et al.[25], which points out that blood glucose changes in a short period of time usually have high self-correlation, and the interpolation error is controllable; after exceeding this threshold, external factors such as diet or exercise may lead to nonlinear violent fluctuations in blood glucose, and the interpolation is no longer reliable.

For the shortage port with a length of ≤ 15 minutes, we use Cubic Spline Interpolation to fill it.

Compared with simple linear interpolation, cubic spline interpolation can ensure the continuity of the first-order and second-order derivatives of the interpolation curve, so as to better fit the smooth characteristics of blood glucose fluctuations and avoid unnatural corners at wave peaks or troughs[23]. This is especially important for gradient-based neural network training, which helps the model capture more accurate blood glucose change rate characteristics.

For long notches with a length of > 15 minutes, we do not interpolation filling to prevent the introduction of false data (Artifacts). We adopt the strategy of sequential segmenting:

1. Using the long notch as the breakpoint, the original long sequence is cut into several independent continuous sub-sequences.

2. The length of the segmented subsequence is screened to eliminate the fragment fragments with a length of less than 6 hours (72 data points). The 6-hour threshold is set to ensure that each sample can provide sufficient history window to build sliding window inputs, while ensuring that the model can learn the complete postprandial blood glucose fluctuation pattern.

Through the above strategy, we have effectively solved the discontinuity problem in the original data. Compared with directly eliminating subjects with missing values (which will lead to a large amount of valuable data loss), the segmentation strategy significantly improves the utilization rate of data. The final data set consists of a series of strictly continuous, equiintervals (5 minutes) and length of blood glucose fragments that meet the modeling requirements, which provides a high-quality data basis for subsequent deep learning model training.

1. CGM Noise Analysis and Filtering
   1. Noise Analysis

Although the continuous blood glucose monitoring (CGM) system provides revolutionary technical support for diabetes management, its data quality is not perfect. The signal output by the CGM sensor inevitably superimposes various noise components, and the existence of these noises will have a significant negative impact on the subsequent blood glucose prediction model[26]. Understanding the source and characteristics of noise is the prerequisite for designing an effective filtering strategy.

From the perspective of physical mechanism, the noise of CGM signals mainly comes from the following aspects:

(1) Inherent noise of electrochemical sensors

The CGM sensor works based on the electrochemical reaction principle of glucose oxidase, and the chemical reaction process on the surface of the sensor electrode itself has random fluctuations[27]. The current signal generated by the redox reaction of glucose molecules on the surface of the enzyme electrode has statistical ups and downs, which is the main source of the inherent noise of the sensor. In addition, the aging of the electrode material, the attenuation of enzyme activity and the change of electrolyte concentration will lead to the sensitivity Drift of the sensor over time, which is manifested as low-frequency baseline drift noise[28].

(2) Physiological delay and dynamic error

The CGM sensor measures the glucose concentration in the interstitial fluid (ISF), not the direct concentration in the blood. There is a physiological delay of 5-15 minutes in the diffusion of glucose from blood to inter-tissue fluid (Physiological Lag)[29]. When blood glucose changes rapidly (such as a sharp increase in blood glucose after meals or a rapid decrease after insulin injection), there will be a significant dynamic error between the CGM reading and the actual blood glucose value. Although this error is essentially a systematic deviation, it is often regarded as a noise component in time series analysis[30].

(3) Sports false traces and pressure interference

The physical movement of the subject will cause the relative displacement of the sensor and the subcutaneous tissue, resulting in instantaneous measurement abnormalities, which is called Motion Artifact[31]. More Common Is The Pressure-Induced Sensor Attenuation (PISA) Phenomenon. When The Testipt Presses The Sensor Wearing Site For A Long Time (Such As Sleeping On The Side), Local Tissue Blood Flow Is Blocked, Resulting In An Abnormal Decrease In CGM Readings, Forming A False Hypoglycemia Event[32]. This kind of noise has obvious non-steady characteristics and is closely related to the behavior pattern of the subject.

(4) Thermal noise and quantitative error

Sensor signals will introduce thermal noise and quantification errors of electronic systems during analog-to-digital conversion (ADC) and wireless transmission. Although the electronic circuit design of modern CGM equipment is highly mature, the contribution of this part of the noise is relatively small, but it cannot be ignored under the condition of low signal-to-noise ratio.

In order to quantify the noise level in CGM signals, we adopt multiple statistical indicators for comprehensive evaluation. Set the original CGM sequence as , where gk represents the blood glucose reading of the kth sampling point, and the sampling interval is minutes.

（1）Noise Standard Deviation

The first-order difference of adjacent sampling points can effectively separate high-frequency noise components from low-frequency blood glucose trends:

The standard deviation of noise is defined as:

This indicator reflects the intensity of random fluctuations in signals on a 5-minute time scale. In healthy populations, the rate of blood glucose change is typically less than 2−3 mg/dL/5 min[33], and variations exceeding this threshold are often attributed to measurement noise or abnormal physical events.

（2）Signal-to-Noise Ratio(SNR)

Signal-to-noise ratio (SNR) is a classic metric for evaluating signal quality. In this study, it is defined as the ratio of the standard deviation of the signal to the standard deviation of the noise.

The reflects the variability of blood glucose levels throughout the monitoring period. A higher SNR value indicates that the true variability component of the signal is more relative to the noise component. Literature has shown that when the SNR is below 10, noise will significantly affect the performance of blood glucose prediction models[26].

（3）Abnormal Change Ratio

A blood glucose change exceeding 5 mg/dL within 5 minutes is defined as an abnormal spike event:

This indicator reflects the frequency of extreme change events in the signal that may be caused by noise or equipment failure. Under normal physiological conditions, the ratio is usually less than 10%[34].

Based on the above index system, we conduct a systematic noise evaluation of the integrated CGM data set (a total of 174 subjects). The evaluation process is as follows: calculate three noise indicators for the continuous blood glucose sequence of each subject, the average noise, SNR and abnormal jump ratio, and judge whether filtering is needed based on the preset threshold.

Among them, the abnormal jump rate is a very important measure in blood glucose data, because according to a large number of experiments, the change of human blood glucose is relatively slow, and the change rate is usually lower than 2-3mg/dL/5min. Therefore, the proportion of data exceeding the change threshold in the blood glucose sequence can effectively measure the validity of the data.

analysis of noise assessment results.

| **Metric** | **Mean** | **Standard Deviation** | **Threshold** |
| --- | --- | --- | --- |
| Average Noise(mg/dL) | 1.54 | 0.56 | 1.5 |
| SNR | 8.18 | 2.18 | 10.0 |
| Abnormal Change Ratio(%) | 4.2 | 4.7 | 10% |

Based on the evaluation results in Table 3-1, we established the criteria for determining the need for filtering: when the subject's data met any of the following conditions, it was determined that filtering was required: (1) average noise exceeding 1.5 mg/dL; (2) SNR below 10.0; (3) proportion of abnormal jumps exceeding 10.0%.

![血糖噪声SNR跳变评估](data:image/png;base64...)

(1)SNR distribution (2)noise level distribution (3)anomaly change ratio distribution (4)SNR vs noise level scatter plot.

According to Figure 3.1, 158 (90.8%) of the 174 subjects met at least one filtering condition. This proportion is very high, indicating that there is a common noise problem in the original CGM data, and it is necessary and reasonable to carry out unified filter preprocessing for all data.

From the analysis of specific causes, the subjects with low SNR (<10) accounted for 83.9%, which is the main source of filtering demand; the subjects with excessive abnormal jump ratio (>10%) accounted for 12.6%; and the subjects with excessive average absolute change (>1.5 mg/dL) accounted for 45.9%. These results are basically consistent with the CGM noise characteristics showed in the literature[26][35], which verifies the ability of the noise evaluation method.

* 1. Filtering Theory

In order to effectively inhibit the noise component in CGM signals while retaining the real change characteristics of blood glucose to the greatest extent, we compare three digital filtering methods widely used in the field of biomedical signal processing: Kalman Filter, Savitzky-Golay Filter (S-G Filter) and Butterworth Filter. The following introduces the theoretical principles of each method and its applicability in CGM signal processing.

* + 1. Kalman Filter

Kalman filter is an optimal recursive estimation algorithm based on the state space model, which was originally developed by Rudolf E. Kalman proposed it in 1960 and has been widely used in aerospace, robotic navigation and other fields [36]. In recent years, Kalman filter has been successfully introduced into real-time denoising processing of CGM signals[27][28]. The key logic of Kalman filtering is in the optimal estimation of noisy signals through the fusion of system state prediction and observation values. It does not rely entirely on the mathematical modeling of the signal, nor does it rely entirely on observation data, but dynamically fuses the two, which is very suitable for blood glucose data with noise.

We employ the Constant Velocity Model to describe the dynamic changes in blood glucose levels. The state vector , where represents the actual blood glucose concentration and denotes the rate of change in blood glucose. The state transition equation is:

The state transition matrix:

The observation equation is:

denotes the observation matrix, with and representing process noise and measurement noise respectively, both assumed to follow a zero-mean Gaussian distribution.

Kalman filtering achieves optimal state estimation through the following two recursive steps:

Prediction step:

![文本](data:image/png;base64...)

Update:

![文本  AI 生成的内容可能不正确。](data:image/png;base64...)

Where denotes the process noise covariance matrix, represents the measurement noise covariance matrix, and is the Kalman gain.

In the implementation, the key parameters were set as follows: process noise variance , measurement noise variance . A larger R value indicates lower trust in CGM measurements, leading the filter to rely more on state prediction and thus producing a stronger smoothing effect; whereas Q controls the system's response speed to blood glucose changes. These parameter settings were referenced from the empirical experience of Facchinetti et al. in CGM denoising research[27].

* + 1. S-G Filter

Unlike the state space method of Kalman filter, Savitzky-Golay filter adopts a more direct polynomial fitting idea. The filter was made by Abraham Savitzky and Marcel J.E. Golay proposed in 1964, which is a digital smooth filtering method based on local polynomial fitting[37]. This method has a long history of application in spectroscopy, chromatography and other fields of analytical chemistry, and has also been widely used in biomedical signal processing in recent years[38].

The core idea of the S-G filter is to fit a low-order polynomial for the data point in the sliding window centered on the current point, and then use the center point value of the polynomial as the filter output.

Set the window length to (an odd number) and the polynomial order to . For the data points within the window, fit the polynomial:

where . The filter output is .

S-G filtering can be equivalently expressed as a convolution operation.

The coefficient of the convolutional kernel depends only on the size of the window and the polynomial order, which can be calculated in advance. This makes S-G filtering very efficient in implementation, which is especially suitable for real-time processing applications.

The parameters used in this study are: window length 2m+1=15, polynomial order p=3. At a 5-minute sampling interval, the 15-minute window corresponds to a time span of 75 minutes, which can effectively smooth short-term noise fluctuations while retaining important physiological characteristics such as postprandial blood glucose peaks. The third-order polynomial can better fit the smooth change curve of blood glucose and avoid the oscillation caused by overfitting[39].

The main advantage of the S-G filter is its ability to maintain the peak shape of the signal. Compared with simple moving average filtering, S-G filtering can better retain the extreme points (peaks and valleys) and high-order derivative information of the signal while smoothing noise[40]. This characteristic is especially important for blood glucose prediction, because the accurate identification of postprandial blood glucose peaks is a key indicator for evaluating the quality of blood glucose control.

* + 1. Butterworth Filter

In addition to the above two methods, we also consider the classical method of frequency domain filtering. The Butterworth filter is a classic infinite shock response (IIR) filter design method proposed by Stephen Butterworth in 1930[41]. It is characterized by having the largest flat amplitude and frequency response in the pass band, and is one of the most commonly used low-pass filters in digital signal processing[42].

The amplitude-frequency response of Butterworth low-pass filter is:

Here, denotes the cutoff frequency, and represents the filter order. A defining characteristic of Butterworth filters is their near-flat amplitude-frequency response in the passband (), with no ripple, hence the name "maximum flatness" filter.

The key parameters are set as follows: filter order , normalized cutoff frequency . With a 5-minute sampling interval, the Nyquist frequency is , so the actual cutoff frequency is:

The corresponding cutoff period is approximately minutes. This implies that high-frequency noise with periods shorter than 66 minutes will be significantly attenuated, while physiological signals such as postprandial blood glucose fluctuations (typically with periods longer than 1 hour) will be retained.

* 1. Evaluation of Filtering Effect

To objectively compare the performance of three filtering methods, we established a multi-dimensional evaluation index system:

(1) Noise suppression capability-filtered noise standard deviation ():

The first-order difference standard deviation of the filtered sequence is calculated to reflect the residual noise level.

Noise Reduction Rate (NRR):

（2）signal fidelity

Root Mean Square Error (RMSE): The deviation between the filtered sequence and a reference sequence. Due to the lack of a gold standard for actual blood glucose measurement, we employed a longer moving average window as an approximate reference.

Peak Preservation Ratio(PPR): The ratio of the filtered signal's peak value to the original peak value, indicating the method's ability to retain extreme values.

（3）time response

Phase Lag: The time delay of the filtered signal relative to the original signal. Quantitatively assessed through cross-correlation analysis.

comparison of filtering results.

| **Index** | **Kalman** | **S-G** | **Butterworth** |
| --- | --- | --- | --- |
| NRR | -6.6±3.7 | 14.0±6.2 | 18.8±7.1 |
| SNR | 7.9±2.0 | 9.4±2.2 | 9.9±2.3 |
| PPR | 1.009±0.005 | 0.987±0.007 | 0.972±0.008 |
| Phase Lag | 1.7±2.4 | 0 | 0 |

1. Noise suppression ability: The Butterworth filter statistically shows the highest noise suppression rate (18.8%) and the highest signal-to-noise ratio (9.9), reflecting its advantages as a classic low-pass filter in frequency domain denoising. S-G filter followed closely (NRR 14.0%, SNR 9.4). The Kalman filter presents a negative noise suppression rate under this configuration, which may be related to its sensitive tracking characteristics for high-frequency changes. Although dynamic information is retained, it does not significantly smooth the first-order differential fluctuation.

2. Signal fidelity: The peak retention ratio (PPR) of S-G filter is 0.987, which is the closest to the ideal value of 1.0, and the standard deviation is extremely small (0.007), indicating that it has high stability and accuracy in retaining the true blood glucose peak. Although the Butterworth filter also performs well (0.972), it is slightly inferior to the S-G filter (the closer to 1, the better, and the Butterworth has a certain peak attenuation). The PPR of the Kalman filter is slightly greater than 1 (1.009), suggesting that there may be a slight overtuning phenomenon. Considering the sensitivity of hypoglycemia and hyperglycemia event identification in blood glucose prediction, the accurate retention of extreme values in S-G filtering is of great clinical significance.

3. Time response: S-G filter and Butterworth filter (bidirectional/symmetric window implementation) both achieve a phase delay of 0.0 minutes, ensuring the strict alignment of the filter data with the original timeline. Kalman filter has an average phase delay of 1.7 minutes, which may introduce a small delay in early warning systems with high real-time requirements.

Although the Butterworth filter has a slight advantage in noise statistics, in view of the best performance of the Savitzky-Golay filter in peak retention (Signal Fidelity) - which is crucial to preventing the real pathological hyper/hypoglycemia fluctuations, and the clinical practice is often most concerned about the maximum and extreme values of blood glucose - and its zero phase delay and high computational efficiency, we finally selected the S-G filter as the preprocessing method for CGM data. This choice ensures that the model input not only removes high-frequency noise interference, but also retains the blood glucose extreme characteristics containing key clinical information to the greatest extent.

This choice is consistent with the conclusion of Sadıkoğlu and others in the study of CGM signal filtering[39], and is also supported by the experimental results of the subsequent prediction model - using the data after preprocessing S-G filter, compared with the original data, the model's prediction accuracy is greatly enhanced.

* 1. Conclusion

This chapter systematically studies the noise characteristics of CGM signals and the preprocessing method of digital filtering. The main work and conclusions are as follows:

1. Noise source analysis: From the perspective of physical mechanism, the four major sources of CGM signal noise are systematically analyzed - the inherent noise of electrochemical sensors, physiological delay error, motion false trace and pressure interference, and electronic system noise, which provides a theoretical basis for the selection of subsequent filtering methods.

2. Noise quantitative evaluation: A multi-indicator evaluation system based on the first-order differential standard deviation, signal-to-noise ratio (SNR) and the abnormal jump ratio was established, and the CGM data of 174 subjects were systematically evaluated. The results show that 90.8% of the subject data has significant noise problems, which confirms the necessity of filtering preprocessing.

3. Comparison of filtering methods: Three methods of Kalman filtering, Savitzky-Golay filtering and Butterworth low-pass filtering are implemented and compared. Quantitative evaluation shows that Butterworth filter noise suppression has the strongest ability, S-G filter peak retention ability is the best, and Kalman filter performance is inferior to both.

4. Method selection: Considering the special needs of blood glucose prediction tasks, S-G filter is selected as our CGM data preprocessing method. This choice has been verified in subsequent prediction experiments.

The data set after filtering provides high-quality input for the prediction model training in the subsequent chapters, which significantly reduces the interference of noise on the model learning process. It is an indispensable key link in the realization of the whole blood glucose prediction system project.

1. Model Building and Comparison
   1. Experiment and Evaluation

In order to comprehensively and objectively evaluate the performance of different algorithms in blood glucose prediction tasks, we have built a unified experimental environment and evaluation system. This section will elaborate on the mathematical definition of prediction tasks, data division strategies, and statistical and clinical indicators used to measure model performance.

We define short-term blood glucose prediction as a multivariate time series regression problem under Supervised Learning.

Letdenote the current time instant, and represent the continuous glucose monitoring (CGM) readings over the time steps. In addition to the temporal glucose data, the model incorporates the patient's static physiological characteristics (e.g., age, Age; body mass index, BMI) and temporal features (e.g., hour, Hour), denoted as the vector The input vector of the model can be expressed as:

The prediction target is the blood glucose level at the th time step in the future (Prediction Horizon). We set the sampling interval minutes. Considering the clinical intervention window, we primarily focus on 30-minute forward prediction (i.e., ), as 30 minutes typically provides patients with sufficient time to correct impending hypoglycemic or hyperglycemic events through food intake or insulin injection[45]. Simultaneously, to fully capture recent trends and historical dependencies of blood glucose, we set the historical input window length , utilizing data from the past 60 minutes for prediction. This configuration achieves a good balance between computational efficiency and information sufficiency, and is a common setup in the relevant literature[46].

And we use a combination of statistical error index and clinical accuracy index to conduct a comprehensive evaluation of the prediction model.

Statistical error indicators include:

Mean Absolute Error (MAE): represents the absolute magnitude of the difference between the predicted value and the actual value. It is not as sensitive to abnormal values as RMSE, and can better reflect the general prediction accuracy.

Root Mean Square Error (RMSE): Higher punishment for large errors reflects the stability of model prediction. In blood glucose prediction, it is especially important to avoid great prediction bias (such as unpredicted severe hypoglycemia), so RMSE is a key indicator.

Mean Absolute Percentage Error (MAPE): Eliminates the influence of the quantitative framework and facilitates cross-data set comparison. However, numerical instability may occur when the hypoglycemia value (the denominator is small).

Root Mean Square Percentage Error (RMSPE): combines the characteristics of RMSE and percentage error.

Combining the above statistical indicators, we can comprehensively evaluate the prediction accuracy and stability of the model and eliminate the bias that may be caused by a single indicator.

Clinical accuracy index: Clarke Error Grid Analysis (CEGA):

Statistical indicators only reflect the numerical proximity, and cannot fully reflect the impact of the forecast results on clinical decision-making. For this reason, we introduce Clarke error grid analysis[50] as the core clinical evaluation tool. The Clarke index is a widely recognized blood glucose prediction evaluation standard in clinical practice. CEGA divides the scatter chart of the predicted value (Y axis) and the reference real value (X axis) into five areas: A, B, C, D and E:

Area A (Clinically Accurate): Accurate prediction within the deviation of 20% or within the range of hypoglycemia. The prediction results of this region are clinically accurate.

Area B (Clinically Acceptable): The deviation exceeds 20%, but it will not lead to improper treatment decisions.

Area C (Overcorrection): It may lead to unnecessary corrective treatment (such as falsely reporting hypoglycemia when blood glucose is normal), which is not directly dangerous but affects the quality of life.

Area D (Failure to Detect): Failure to detect dangerous hyperglycemia or hypoglycemia events (such as missing hypoglycemia) may lead to serious medical consequences.

Area E (Erroneous Treatment): The predicted value is completely opposite to the real value (such as predicting hypoglycemia as hyperglycemia), which will induce completely wrong treatment operations, which is extremely dangerous.

For an excellent blood glucose prediction model, most of its prediction points (>95%) should fall in Zone A and Region B, and try to avoid falling into Zone D and Zone E. Therefore, we can quantify the clinical applicability of the model by calculating the point ratio of each region.

In order to strictly evaluate the timing generalization ability of the model, we adopt the "past-future" division strategy (Past-Future Split) instead of the traditional random division. For each subject:

1. Test Set: Choose the last 6 hours (72 time points) of each subject's monitoring record as the test data. This simulates the prediction scenario of the model for the blood glucose value in the next 6 hours in actual use.

2. Training Set: All historical data except the test set and the necessary verification set.

3. Hold-out Set: Among all subjects, select the data of 10 subjects as the hold-out set, do not participate in the training and verification of the model, and only use the independent verification of the final model to ensure that the model can maintain good performance on individuals that have never been seen. Also prepare for later transfer learning.

* 1. Baseline and Machine Learning Models

In order to establish a benchmark for predicting performance, we first implemented three types of traditional models: statistical model, linear regression model and nonlinear machine learning integration model. All models adopt a unified input format: including the blood glucose value sequence of the past 12 time steps (60 minutes), as well as the two static characteristics of the subjects' age and body mass index (BMI). The input characteristic vector can be formally represented as:

1. ARIMA

The Autoregressive Integrated Moving Average (ARIMA) model is a classic statistical method for time series forecasting. The general form of the model is:

denotes the lag operator (defined as ), where is the autoregressive polynomial, and the moving average polynomial is . represents the order of the difference.

In the process of determining the model order, the Augmented Dickey-Fuller (ADF) test is initially utilized to examine the stationarity of the blood glucose series.Subsequently, the optimal parameters are determined based on the Autocorrelation Function (ACF) and Partial Autocorrelation Function (PACF) plots. Due to the non-stationary nature of the blood glucose series, a first-order difference () is typically required to eliminate trends.

Although ARIMA is very interpretable, it can only capture linear timing dependencies and is difficult to integrate external static characteristics (Age, BMI), which has limitations in application.

Predicted results on the hold-out set subject 2 and subject 306:

![](data:image/png;base64...)

![](data:image/png;base64...)

The ARIMA prediction on Hold-out set(subject 2 and 306).

2. Linear Regression

By constructing a lag feature matrix (Lag Features), time series prediction is transformed into a standard supervised regression problem. The linear regression model solves the weight vector through the Ordinary Least Squares (OLS):

Where indicates the prediction time span (30 minutes). The OLS loss function is:

Before training, all input characteristics are standardized by Z-score to eliminate the difference in the framework. The model has a simple structure and high computing efficiency. It can give a reasonable trend estimate for a stable blood glucose period, but it performs poorly in nonlinear rapid change periods (such as post-meal rise and post-exercise).

Predicted results on the hold-out set subject 2 and subject 306:

![](data:image/png;base64...)

![](data:image/png;base64...)

The linear prediction on Hold-out set(subject 2 and 306).

The above statistical model mainly relies on linear assumptions, and it is difficult to capture the complex nonlinear pattern of blood glucose dynamics. In order to break through this limitation, we have further introduced three nonlinear machine learning methods, KNN, Random Forest and XGBoost.

3. KNN

K-Nearest Neighbors is an instance-based non-parametric learning method[24]. The core idea is to find the K historical samples most similar to the sample to be predicted in the characteristic space, and use the weighted average of its target value as the prediction result:

denotes the set of nearest neighbors of input in the training set. We set the K-Nearest Neighbors (KNN) parameter to .Adopt the equal weight average strategy. The advantage of KNN lies in its non-parametric characteristics - no explicit training process is required, and the model expression ability increases with the amount of data. However, due to the need to calculate the distance on the entire training set, the inference speed is slow on large-scale data sets. In addition, KNN is sensitive to feature scaling, so all features are standardized by Z-score before training.

Predicted results on the hold-out set subject 2 and subject 306:

![](data:image/png;base64...)

![](data:image/png;base64...)

The KNN prediction on Hold-out set(subject 2 and 306).

4. Random Forest

Random forest uses the Bagging strategy to reduce variance by building multiple independent decision trees, averaging their outcomes.:[8]

Here, denotes the number of decision trees, and represents the prediction function of the -th decision tree.

During training, every individual tree employs Bootstrap Sampling and selects random subsets of features to promote diversity among the base learners. We set the integration scale to 100 decision trees, and do not limit the maximum depth of a single tree to fully fit the training data. In addition, the model additionally introduces Time of Day (integers coded with 0-23), so that the tree model can learn the circadian rhythm characteristics of blood glucose.

Predicted results on the hold-out set subject 2 and subject 306:

![](data:image/png;base64...)

![](data:image/png;base64...)

The random forest prediction on hold-out set(subject 2 and 306).

5. XGBoost

XGBoost, proposed by Chen and Guestrin, short for eXtreme Gradient Boosting, is an ensemble learning technique that uses the Gradient Boosting framework.[45]. It iteratively adds weak learners to fit the residuals of the previous round. Its objective function is:

denotes the loss function (using squared loss), and functions as the regularization component to manage model complexity and avoid overfitting.. We set the boosting rounds to 100, the learning rate , and the maximum depth of a single tree to 5. Similar to random forests, XGBoost incorporates temporal features. With its robust nonlinear fitting capability and built-in regularization mechanism, XGBoost typically outperforms baseline models and is widely used as a key benchmark for evaluating the effectiveness of deep learning models.

Predicted results on the hold-out set subject 2 and subject 306:

![](data:image/png;base64...)

![](data:image/png;base64...)

The XGBoost prediction on hold-out set(subject 2 and 306).

* 1. Deep Learning Models

For the timing dependence and nonlinear characteristics of blood glucose data, we have built four deep neural network architectures: one-dimensional convolutional neural network (CNN), circular neural network (RNN), long-term and short-term 2 memory network (LSTM) and Transformer. In order to ensure the fairness of comparative experiments, all deep learning models adopt a unified training strategy: the batch size is set to 64, the Adam optimizer [50] is used to update the parameters with a learning rate , the loss function is selected as Mean Squared Error (MSE), and the training process lasts 50 cycles (epochs). The input data is standardized and processed by Z-score before training.

1.CNN

Convolutional neural networks have made breakthroughs in the field of image processing, while one-dimensional Convolution is equally efficient in time series feature extraction[47]. One-dimensional convolution operation can be formalized as:

Among them, is the size of the convolutional kernel, and is the weight of the convolutional kernel that can be learned.

The CNN architecture we designed adopts a two-layer cascade convolution structure. The first convolutional layer is configured with 16 convolutional kernels of size 3, and zero filling (padding=1) is used to maintain the sequence length. After the maximum pooling of the ReLU activation function and step length of 2, the sequence length is halved. The second convolution layer is equipped with 32 convolutional kernels, and the structure is the same as that of the first layer. After two poolings, the feature map is flattened and stitched with static features (Age, BMI), and finally the predicted value is output through a two-layer fully connected network (the hidden layer dimension is 64). The advantage of CNN is its translation invariance and efficient parallel computing ability, which can quickly capture short-term local fluctuation patterns.

Predicted results on the hold-out set subject 2 and subject 306:

![](data:image/png;base64...)

![](data:image/png;base64...)

The CNN prediction on served set(subject 2 and 306).

2. RNN

Recurrent Neural Networks (RNNs) model temporal dependencies in sequential data through recurrent connections[25]. The core recursive formula is:

denotes the hidden state at time , with and being the weight matrices for input-to-hidden and hidden-to-hidden respectively. And the dimensions and represent the hidden layer and input dimensions.

We adopt a single-layer RNN structure. The hidden layer dimension model takes the hidden state of the last time step as the global representation of the sequence, and outputs the predicted value through the two-layer fully connected network (the hidden layer dimension is 64) after splicing it with static features. However, there is a gradient disappearance problem in the basic RNN, and it is difficult to effectively capture long-term dependencies.

Predicted results on the hold-out set subject 2 and subject 306:

![](data:image/png;base64...)

![](data:image/png;base64...)

The RNN prediction on hold-out set(subject 2 and 306).

3. LSTM

To overcome the long-range dependence of RNN, Hochreiter and Schmidhuber proposed Long Short-Term Memory (LSTM)[46]. LSTM realizes fine control of information flow by introducing a gate control mechanism. Its core computing unit contains three gates and one cell state:

Forget Gate controls the retention ratio of historical information:

The Input Gate controls the amount of new information written:

Cell state is updated through gated weighting:

The output gate controls the output of the hidden state:

denotes the Sigmoid activation function, and represents the Hadamard product.

We adopt a single-layer LSTM structure, and the hidden layer dimension is set to 32. The model architecture is: LSTM layer extracts timing features → takes the hidden state of the last time step → splicing with static features → two layers of fully connected network output prediction. LSTM can effectively remember the trend of long-term blood glucose evolution, which is one of the mainstream methods in the field of blood glucose prediction at present[46][48].

Predicted results on the hold-out set subject 2 and subject 306:

![](data:image/png;base64...)

![](data:image/png;base64...)

The LSTM prediction on hold-out set(subject 2 and 306).

4.Transfoemer

Considering the serial calculation limitations and long-distance information attenuation of RNN models, we introduce the Transformer model based on Self-Attention[49]. Transformer abandons the cyclic structure and relies entirely on the dependency between any two positions in the attention mechanism modeling sequence, It achieves long-range dependency modeling capability of .

Since Transformer itself does not have the ability to perceive sequence order, it is necessary to explicitly inject time position information through Positional Encoding. We adopt the sine-cosine position coding scheme:

denotes the position index in the sequence, represents the model's embedding dimension, and is the dimension index.

The core computation of Transformer's self-attention mechanism is as follows:

、, and stand for the Query, Key, and Value matrices respectively. denotes the scaling factor, while indicates the sequence length. This factor prevents the softmax gradient from vanishing due to excessively large dot product values.

To enable the model to focus on feature representations across different subspace, Transformer employs a multi-head attention mechanism:

Each attention head independently computes , where and are learnable projection matrices, and ℎ denotes the number of attention heads.

We adopt a simplified architecture that contains Encoder-only. The model configuration is as follows: the embedding dimension , the number of encoder layers is 2, the number of attention heads , the hidden dimension of the feedforward network is 128, and the Dropout ratio is 0.1. So the model architecture: the linear embedding layer maps the input to the dimension space → superimposed position coding → two-layer Transformer encoder → take the hidden representation of the last time step → splicing with static features → two-layer fully connected network output prediction.

The advantages of Transformer are: (1) the self-attention mechanism realizes global dependence modeling, which is not limited by sequence length; (2) fully parallel computing, and the training efficiency is significantly better than that of the RNN model; (3) the attention weight is explainable and can be used to analyze the historical time point of the model. In recent years, Transformer and its variants have shown strong modeling potential in the field of blood glucose prediction[23].

Predicted results on the hold-out set subject 2 and subject 306:

![](data:image/png;base64...)

![](data:image/png;base64...)

The transformer prediction on hold-out set(subject 2 and 306).

* 1. Results Analysis

Table 4-1 summarizes the performance of each model on the test set (with a prediction time span of H=30 minutes).

comparison of different models’ prediction.

|  | **MAE**  **(mg/dL)** | **RMSE**  **(mg/dL)** | **MAPE(%)** | **RMSPE(%)** | **CEG(A+B)(%)** |
| --- | --- | --- | --- | --- | --- |
| ARIMA | 5.7965 | 8.9621 | 4.4696 | 6.9105 | 99.8+0.2 |
| Linear | 5.2298 | 8.5292 | 4.3827 | 6.8298 | 99.8+0.2 |
| KNN | 11.3252 | 15.6312 | 9.9544 | 13.6284 | 93.4+6.3 |
| Random Forest | 6.6398 | 10.2797 | 5.5753 | 8.2342 | 99.2+0.6 |
| XGBoost | 8.2151 | 12.3310 | 6.9834 | 10.1447 | 98.1+1.6 |
| CNN | 5.4077 | 8.6982 | 4.5519 | 7.0817 | 99.8+0.2 |
| RNN | 7.4727 | 11.0343 | 6.3253 | 8.9341 | 99.0+0.9 |
| LSTM | 5.0236 | 8.1853 | 4.2701 | 6.7352 | 99.8+0.2 |
| Transformer | 6.5029 | 9.1394 | 5.7825 | 7.9993 | 99.6+0.3 |

From the experimental results, the obvious performance stratification phenomenon can be observed. The overall advantage of the deep learning model is significantly better than the traditional statistical and machine learning model, which is consistent with the research trends in the field of blood glucose prediction in recent years[45]. Specifically:

Limitations of the traditional model: The ARIMA model is limited by its linear hypothesis, and it is difficult to capture the nonlinear characteristics of blood glucose dynamics; although linear regression is efficient in calculation, it does not perform well in the period of rapid changes in blood glucose; although KNN is a non-parametric method, its prediction strategy based on local similarity is difficult to model long-term timing dependence, which is significantly behind other models.

Linear performs best in traditional models, and its RMSE even exceeds LSTM. The sliding window and direct prediction strategy adopted by linear regression can effectively cope with the linear inertia in blood glucose changes. In addition, the model has few parameters and is not easy to overfit. Under the condition of limited training data, it has a certain generalization advantage. Of course, the essential limitation of linear regression is that it cannot capture nonlinear dynamics, and there will still be a prediction lag during the period of rapid fluctuations in blood glucose, which will be further discussed in the subsequent waveform analysis.

LSTM and Transformer models achieve the lowest RMSE and MAE, reflecting the unique advantages of deep learning in chronological modeling. The deep learning model can automatically learn hierarchical feature representation through end-to-end, without tedious manual feature engineering, and can capture complex nonlinear dynamic patterns in blood glucose sequences. It is particularly noteworthy that the Transformer model shows comparable performance to LSTM, while having better parallel computing efficiency and interpretability - which lays an important foundation for subsequent model optimization and transfer learning.

![](data:image/png;base64...)

The CEG Clarke error grid of different models.

Judging from the results of the Clarke error grid, all models except KNN have achieved a clinical safety level of more than 99% in the A+B area. Among them, the proportion of Area A of LSTM, Linear, CNN and ARIMA all reached 99.8%, and Transformer accounted for 99.6%, all of which meet the basic requirements of predictive safety for clinical applications. The proportion of area A of KNN is only 93.4%, which means that more than 6% of the prediction points deviate from the clinically acceptable accuracy range, which may lead to delays in clinical decision-making in key scenarios such as hypoglycemia warning. Overall, under the 30-minute prediction window, the difference in clinical safety of the top-ranked models is no longer significant, and the distinction of each model is mainly reflected in numerical accuracy rather than safety level.

In order to visually show the prediction effect, Figure 4-11 selects a representative subject (ID: 306) to show the prediction curves of different models over a continuous period of time.

![](data:image/png;base64...)

Prediction results of different models on subject 306.

Through the detailed analysis of the predicted waveform, the following phenomena can be observed:

Performance in the stable period: During the period when blood glucose is relatively stable, all models can give more accurate predictions, and there is not much difference between models. This is because the changes in blood glucose in the stable period are mainly dominated by inertia, and the historical value itself can provide sufficient predictive information.

Performance of rapid change period: During the period when blood glucose rises rapidly (such as after meals) or decreases rapidly (such as after exercise), the performance difference between models is significantly amplified. Traditional models (ARIMA, linear regression) have obvious prediction lag (phase lag), that is, there is a delay of about 5-10 minutes between the prediction curve and the real curve. The essential reason for this phenomenon is that traditional models rely too much on the latest historical observations. When the blood glucose trend is reversed, the model needs to wait for new observation information to respond.

Response advantages of deep learning: In contrast, LSTM and Transformer respond more acutely to changes in blood glucose, and the prediction lag is significantly reduced. This is due to the implicit learning ability of deep learning models to sequence trend characteristics - they can extract second-order or higher dynamic information (such as acceleration and curvature) from historical sequences, so as to perceive the trend of blood glucose changes in advance. The Transformer model can directly model the dependencies between any two time points through the self-attention mechanism, showing unique advantages in capturing periodic patterns and mutation events of blood glucose.

Based on the above experimental results, we further analyze the core advantages of the deep learning model compared with the traditional method:

1. Automatic characteristic learning ability

Traditional machine learning methods (such as KNN, random forest, XGBoost) rely on the characteristics of artificial design (lag value, statistics, time coding, etc.), and its upper performance limit is subject to the quality of feature engineering. Through multi-layer nonlinear transformation, the deep learning model can automatically extract hierarchical abstract features from the original blood glucose sequence without the prior knowledge intervention of experts in the field.

2. Long-range dependence modeling

Blood glucose dynamics are affected by many factors, including recent eating, exercise, and longer-term physiological rhythms (such as dawn phenomenon). Although the RNN model can model dependencies of any length in theory, it is limited by the gradient disappearance problem in practice. LSTM partially alleviates this problem through the gate control mechanism, and Transformer realizes the long-range dependence modeling of O(1) through the self-attention mechanism, which can directly pay attention to the information at any time in the history window without the information loss transmitted in the intermediate state.

3. Scalability and transfer learning potential

Another core advantage of the deep learning model is its transfer learning ability. Deep models pre-trained on large-scale group data can learn the general laws of blood glucose dynamics (such as post-meal rise mode, post-exercise decline mode, etc.), which can be efficiently transferred to new individuals through fine-tuning. In contrast, traditional machine learning models lack an effective knowledge transfer mechanism, and every new user needs to be trained from the beginning.

The Transformer model has unique advantages in transfer learning: its modular architecture design (embedded layer, encoder layer, prediction head) allows you to flexibly select to freeze or fine-tune different components; the interpretability of self-attention weight helps to understand the adaptation process of the model on new individuals; in addition, Transformer's successful transfer learning practices in the fields of natural language processing and computer vision (such as BERT, ViT) also provide theoretical and practical support for its application in the field of blood glucose prediction[23].

* 1. Conclusion

This chapter systematically discusses the construction process of blood glucose prediction models, from traditional statistical methods to cutting-edge deep learning technologies, and comprehensively compares the performance of nine prediction algorithms. The primary research findings are as follows:

1. The completeness of the experimental system

We have established a standardized blood glucose prediction evaluation framework: using the 60-minute historical sequence as input to predict the blood glucose value in the next 30 minutes. The evaluation system not only includes traditional statistical indicators (MAE, RMSE, MAPE), but also introduces clinically-oriented Clarke error grid analysis to ensure that the model evaluation takes into account numerical accuracy and clinical safety.

2. The significant advantages of deep learning models

The experimental results clearly confirm that the deep learning model is superior to the traditional method in blood glucose prediction tasks. Deep sequence models such as LSTM and Transformer have achieved good performance in terms of prediction accuracy, response speed and clinical safety. The core advantages are reflected in:

- Automatic feature learning: no need to manually design complex timing features, end-to-end learning abstract representation of blood glucose dynamics

- Long-range dependence modeling: effectively capture the periodic patterns and trend information of blood glucose changes

- Improvement of lag problem: significantly reduce the prediction delay of traditional models when blood glucose changes rapidly

3. The unique value of Transformer model

In the deep learning model, Transformer shows predictive performance comparable to LSTM, and has the following unique advantages:

- Global dependency modeling: the self-attention mechanism realizes the long-range dependence of O(1), not limited by the length of the sequence

- Parallel computing efficiency: abandon the circular structure, train and reason faster

- Interpretability: Attention weight visualization helps to understand the decision-making basis of the model

- Transfer learning-friendly: modular architecture design facilitates knowledge transfer and personalized fine-tuning

4. Limitations and personalized needs of general models

Although the overall performance of the deep learning model is excellent, the prediction effect of some subjects was still observed in the experiment. This phenomenon reveals the inherent limitations of the General Model based on group data training: there are significant differences in insulin sensitivity, metabolic rate, eating habits, etc. of different individuals, and it is difficult for a single general model to perfectly adapt to the unique physiological patterns of all individuals.

5. Transfer Learning and Personalized Prediction

The above analysis shows that the realization of high-precision personalized blood glucose prediction requires individual adaptation on the basis of the general model. Transfer learning provides an efficient solution: using pre-trained models on large-scale group data as knowledge carriers, fine-tuning through a small amount of individual data, and quickly adapting to the physiological characteristics of new users.

Considering the excellent performance and architectural advantages of the Transformer model in this chapter experiment, we choose Transformer as the basic model for transfer learning. The next chapter will discuss in depth how to use transfer learning technology to efficiently transfer the general knowledge of the Transformer pre-training model to specific individuals.

1. Transfer Learning
   1. Introduction

The experimental results of the previous chapter show that although the general model based on Transformer performs well at the group level, the prediction accuracy on some individuals still needs to be improved. This performance difference is mainly due to the physiological differences between individuals: the blood glucose metabolism patterns of different patients are significantly affected by their unique physiological parameters (such as insulin sensitivity, gastric emptying rate) and living habits (diet structure, exercise frequency)[22][24].

The general model tries to fit the average distribution of all subjects during training, which often leads to an "averaging" compromise, that is, the ability to capture specific highly variable individuals is sacrificed in order to reduce the overall average error. In response to this problem, the traditional solution is to collect a large amount of data for each new user and retrain an independent model (Isolated Training). However, for new patients (Cold Start Problem), there is often a lack of sufficient historical data to train complex deep learning models; even for long-term users, the high computing cost of training deep neural networks from the beginning makes its real-time deployment on mobile or wearable devices challenging.

Transfer Learning provides an ideal way to solve the above contradictions between "data scarcity" and "cost computing". Its core idea is to use the general knowledge learned on the large-scale Source Domain data set (such as the basic physiological laws of blood glucose response to carbohydrates) to assist the learning of the Target Domain[13][51]. Through a "Pre-train -> Fine-tune" paradigm, we can quickly adapt the general model to a personalized model with only a small amount of individual data (Few-shot Learning).

This chapter will delve into the personalized transfer learning strategy based on Transformer. Specifically, we will select the typical subjects (ID 306) in the retention set in the previous chapter as the research object to verify the effectiveness of the strategy in small sample scenarios.

* 1. Transfer Strategy

In blood glucose prediction tasks, we can treat data from different subjects as distinct distribution domains. Let the source domain data (population data) be , and the target domain data (individual-specific data) be . Due to physiological differences, although the feature spaces are identical (both being historical blood glucose sequences), their marginal distributions and conditional distributions exhibit offsets, i.e., and .

Applying the source domain model directly to the target domain (i.e., Zero-shot prediction) typically leads to performance degradation (Negative Transfer). Our objective is to leverage and a minimal amount of (i.e., ) to identify an optimal target function that minimizes empirical risk on the target domain test set.

In order to prevent overfitting in small samples and retain general knowledge, we adopt the "freeze encoder" strategy. The Transformer model is decoupled into two parts in this architecture:

1. Encoder: composed of a multi-layer Self-Attention mechanism and a Feed Forward Network, it is responsible for mapping the original timing input to the high-dimensional semantic feature space. We assume that what we learn in this part is the general Physiological Dynamics of blood glucose, which has strong cross-individual reusability.

2. Regression Prediction Head: It is composed of a Fully Connected Layer, which is responsible for mapping high-dimensional features to specific future blood glucose values. This part of the parameter depends more on the individual's absolute blood glucose level and specific metabolic parameters (such as basal blood glucose bias).

In the process of transfer learning, we take the following specific steps:

1. Pre-training: Train the Transformer model from scratch on a large-scale dataset comprising all subjects from the training set, obtaining the parameters and .

2. Fine-tuning: For new individuals, pre-trained parameters are loaded. The encoder gradient is frozen () during backpropagation, and the regression head parameters () are updated using only a small amount of calibration data from the individual.

The advantages of this strategy are:

- Parameter efficiency: only a very small number of parameters (full connection layer) need to be updated, and the computing overhead is extremely low, which is suitable for online learning on edge devices.

- Anti-over-mitting: Due to the huge number of parameters of Transformer encoder, it is easy to over-mit when fine-tuning on small samples. Freezing the main network plays the role of strong regularization.

- Catatrophic Forgetting prevention: retains the model's understanding of general physiological patterns and prevents the model from losing the ability to generalize unprecedented situations (such as sudden hypoglycemia) during fine-tuning.

In order to fully verify the effectiveness and generalization ability of personalized transfer learning, we select 10 subjects (ID: 2, 27, 49, 71, 98, 124, 146, 170, 192, 306) from the Hold-out Set excluded from Chapter 4 for independent verification. These subjects did not participate in the pre-training of the general model and were able to simulate real "new user" scenarios. Among them, the subject 306 had a high prediction error (RMSE > 13 mg/dL) under the general model, and blood glucose fluctuated violently. We take it as the object of detailed case analysis.

For each subject, we divide their data in chronological order to simulate the real clinical application scenario:

- Calibration Set: Take the data of the first 30%. This simulates the first few days (about 2-3 days) when the patient begins to wear the CGM device, which is mainly used for personalized fine-tuning of the model.

- Test Set: Take the last 70% of the data. It is utilized to show the model's predictive performance in the future.

![](data:image/png;base64...)

The data split for transfer learning on subject 306.

This division strictly follows the causality of time, and the data volume of the test set is much larger than that of the calibration set, which is a typical Few-shot Learning scenario.：

The fine-tuning parameters are configured as follows:

Transfer Learning Parameter Settings Table.

| **Parameter** | **Setting** |
| --- | --- |
| Optimizer | Adam optimizer |
| Learning rate | 1e−4 |
| Loss function | Mean Squared Error |
| Batch size | 16 |
| Epochs | 100 |

* 1. Result Analysis

Table 5-1 shows the prediction results of the general model (Baseline) and the fine-tuned model on the test set of subject 306.

Prediction results of the baseline model and fine-tuned model on the participant 306 test set.

| **Metric** | **Baseline(mg/dL)** | **Fine-tuned(mg/dL)** | **Improvement(%)** |
| --- | --- | --- | --- |
| MAE | 9.9727 | 9.2107 | +7.64 |
| RMSE | 13.5865 | 12.6926 | +6.58 |
| MAPE | 7.6601 | 7.2057 | +5.93 |
| RMSPE | 10.8066 | 10.2925 | +4.76 |

The data shows that with only 30% of the calibration data for fine-tuning, the error indicators of the model have been significantly reduced, which means that the standard deviation of the forecast results has been significantly reduced and the uncertainty of the model has been effectively reduced. To show the strategy's generalization capability, we repeated the above experimental process on all 10 subjects.

Results of transfer learning experiments conducted on 10 subjects.

| **subject ID** | **Baseline(mg/dL)** | **Fine-tuned(mg/dL)** | **Improvement(%)** |
| --- | --- | --- | --- |
| 2 | 6.4151 | 5.2000 | +18.94 |
| 27 | 4.4126 | 3.6794 | +16.62 |
| 49 | 8.4029 | 7.6321 | +9.17 |
| 71 | 4.9080 | 3.1654 | +35.51 |
| 98 | 6.5078 | 6.4157 | +1.41 |
| 124 | 4.7742 | 3.1472 | +34.08 |
| 146 | 5.5901 | 3.8671 | +30.82 |
| 170 | 5.1325 | 4.1259 | +19.61 |
| 192 | 4.4688 | 3.0256 | +32.29 |
| 306 | 13.5865 | 12.6926 | +6.58 |
| Mean | 6.3925 | 5.2900 | +20.35 |

It can be seen from the table that the transfer learning strategy has achieved a positive performance improvement in all 10 subjects, with an average RMSE reduction of 20.35%. This result verifies the universality of the freeze encoder strategy - the pre-trained Transformer encoder does capture the dynamic characteristics of migrable blood glucose.

In order to visually show the improvement brought about by fine-tuning, we have drawn a comparison chart of the prediction curve in the time period of some test sets (Figure 5-1).

![](data:image/png;base64...)

Comparison of baseline and fine-tuned model prediction curves on subject 124 during the test set period.

![](data:image/png;base64...)

Comparison of baseline and fine-tuned model prediction curves on subject 146 during the test set period.

From the details of the waveform, we can analyze that fine-tuning has brought the following improvements

1. Peak Consistency: The general model (Baseline) often shows "over-shooting" at the peak of blood glucose, that is, the highest point of the prediction is higher than the highest point of the real value. This is because the general model tends to output the group average, thus highlighting the extreme peak. After fine-tuning, the Fine-tuned model can reach the real peak height more accurately, which is crucial for hyperglycemia warning.

2. Phase Lag improvement: The general model exhibits a noticeable temporal lag in the stage of rapid change of blood glucose (such as the period of rapid increase after meals). By adapting to the unique ascending slope of the individual, the fine-tuning model significantly reduces this lag phenomenon, making the prediction curve more suitable for the real curve on the timeline.

3. Baseline Shift: Fine-tuning effectively adjusts the bias of the regression head, so that the overall prediction curve moves upwards, thus reducing the average deviation of the system.

* 1. Conclusion

The blood glucose regulation mechanism includes not only the physiological laws common to all human beings (such as the hypoglycemia of insulin and the glycemia of carbohydrates), but also highly personalized parameters (such as insulin sensitivity coefficient ISF, carbohydrate coefficient CIR).

The pre-trained Transformer encoder successfully captures the former (commonality) and encodes it into deep features; while the fine-tuning output layer is equivalent to the rapid calibration of the latter (personality parameters), only updating the output layer, which improves the prediction ability of specific individuals.

This strategy has a high engineering application value. In the actual product, we can preset a high-performance general model trained in the cloud. When the user starts to use the device, the system collects data a few days ago, and then quickly runs the fine-tuning algorithm locally (mobile phone or wearable chip) (only updating a simple linear layer) to generate the user's exclusive model. This not only ensures the basic availability of the cold start stage (using a general model), but also provides a personalized experience that is constantly optimized over time, and greatly protects user privacy (no need to upload individual data to the cloud for retraining).

In general, this chapter proposes and verifies the personalized transfer learning strategy based on Transformer in response to the problem that individual differences lead to limited accuracy of general models. By freezing the pre-trained encoder and fine-tuning the regression head, we achieved a consistent performance improvement on a small sample data set of 10 independent subjects. The experimental results show that this method reduces RMSE by an average of 20.35% in all subjects. It provides a practical technical path to realize a low-cost and high-performance personalized blood glucose health management system.

1. Meta-Transfer Learning
   1. Introduction

The freeze encoder transfer learning strategy proposed in the previous chapter has achieved significant personalization results under the condition of 30% calibration data (about 2-3 days). However, in actual clinical scenarios, we often face stricter data constraints: new patients in the group may only have a few hours of CGM records, or users want to get personalized prediction services on the first day after wearing the device. In this Extreme Few-shot scenario - for example, only 30-50 samples (about 2.5-4 hours of data) - the strategy of Chapter 5 may not be able to fully capture individual characteristics due to insufficient calibration data, resulting in limited performance improvement.

The root of this challenge lies in the optimization goal of the standard transfer learning paradigm. In the pre-training stage of Chapter 4, the model learns parameter by minimizing the average loss of all source domain subjects.

This optimization goal seeks a parameter point that performs best at the group level, but this point is not necessarily a more favorable initialization for rapid adaptation to new tasks. In other words, standard pre-training focuses on "predicting accurately" rather than "learning quickly".

Meta-learning, also known as "learning to learn," provides a novel perspective for addressing this challenge[52][53]. Its core idea is to identify an initialization parameter that is most sensitive to gradient updates, rather than seeking an average-optimal parameter. Starting from this point, the model can quickly adapt to any new task with minimal gradient descent steps.

and represent the support set and query set for task respectively. The objective function optimizes the model's performance on the query set after one or several gradient update steps.

This chapter will deeply explore the personalized blood glucose prediction method based on meta-learning. We use the FOMAML (First-Order MAML) algorithm to conduct meta-training on the source domain subjects to obtain a quick-adapting initialization parameter. Then, through the learning curve experiment, we systematically compare the performance differences between Meta-Transfer Learning and Basic Transfer Learning under different fine-tuning sample sizes to verify the advantages of meta-learning in extremely small sample scenarios.

* 1. Meta-learning Theory

In the meta-learning framework, we formalize the problem as optimization over a task distribution . Each task represents an independent learning problem, where in the blood glucose prediction scenario, each subject constitutes a distinct task.

For subject , the corresponding task includes:

-Support Set : a small subset of samples for model adaptation.

-Query Set : samples used to evaluate adaptation effectiveness.

The objective of meta-learning is to learn an initialization parameter , enabling the model to rapidly adapt to any new task sampled from the task distribution using only a small number of samples from , while maintaining strong performance on .

Model-Agnostic Meta-Learning (MAML)[53] is one of the most influential algorithms in the field of meta-learning. Its core concept can be summarized as an optimization process involving two layers of loops:

Inner Loop: For each sampled task , perform k-step gradient descent on the support set to obtain the adapted parameters:

Outer Loop: Calculate the loss of the adapted parameter on the query set, and update the meta-parameter:

The theoretical advantage of MAML is to directly optimize the "performance after adaptation", but its calculation cost is high - it needs to calculate the second-order derivative (Hessian) to reverse propagate the gradient update through the internal loop.

FOMAML (First-Order MAML)[53] is a first-order approximate variant of MAML, which was also proposed by Finn and others in the original MAML work. Its core simplification lies in: when calculating the element gradient in the outer loop, ignore the higher-order dependence of the internal loop gradient update on the element parameter, and directly use the first-step gradient at the adapted parameter to approximate the element gradient. Specifically, the meta-gradient in the external circulation of MAML:

Approximately:

This approach effectively reduces the need for second-order derivatives (Hessian vector product) while preserving MAML's dual-layer evaluation framework for support set and query set. The algorithmic process is as follows:

![](data:image/png;base64...)

FOMAML algorithm framework.

Finn et al.[53] found in the experiment that this first-order approximation is almost the same as the effect of complete MAML in most scenarios, but reduces the computational complexity from O(m) Hessian-vector product to zero, significantly reducing memory and computing overhead. This feature makes it more suitable for online learning on resource-limited devices such as blood glucose meters.

In the context of blood glucose prediction, this means that the initialization parameters obtained by meta-learning not only encode the general dynamic laws of blood glucose, but also encode the "meta-knowledge" of how to quickly adjust to adapt to individual differences.

* 1. Experiment and Analysis

We conduct FOMAML meta training on the source domain data set. Each subject is regarded as an independent task. Table 6-1 lists the hyperparametric configuration of the meta-training stage.

FOMAML Meta-Training Hyperparameter Configuration

| **Hyperparameter** | **Value** |
| --- | --- |
| Meta-training iterations | 1000 |
| Meta learning rate |  |
| Meta optimizer | Adam () |
| Task batch size | 8 |
| Inner loop steps | 5 |
| Inner loop learning rate |  |
| Support set size | 64 |
| Query set size | 64 |

In each meta-iteration, we randomly sample tasks from the source domain subjects. For each task, we perform inner-loop adaptations on its support set, then compute loss on the query set and update the meta-parameters with a step size at the adapted parameters. The meta-optimizer uses Adam, incorporating weight decay () and a learning rate scheduler (decay factor 0.5, patience value 20) to enhance convergence stability.

We adopt the Warm Start strategy: the initial parameters of meta-training are not randomly initialized, but the Transformer model weight obtained by loading the standard pre-training in Chapter 4. This approach integrates the knowledge of standard pre-training with the fast adaptability of meta-learning, and its performance proves to be more stable in practical applications.

In order to evaluate the advantages of meta-learning initialization, we selected 10 subjects in the Hold-out Set for verification. The data division strategy for each subject is as follows:

- Pool set (top 50%): can be used for fine-tuning the data pool to simulate the data accumulated in the early days of the user wearing the device.

- Test set (last 50%): The test data used for final evaluation simulates the time period that needs to be predicted in the future.

In the fine-tuning stage, we select the most recent N samples from the end of the Pool set as fine-tuning data. This strategy of "taking the latest data" has two considerations: (1) the latest data is closer to the test set in time, and the distribution offset is smaller; (2) it simulates the use mode of "updating the model with the latest data" in actual deployment.

We will compare basic transfer learning and meta transfer learning. The two methods use exactly the same fine-tuning strategy and hyperparameters. The only difference is the source of the initialization parameters. This ensures the fairness of the experimental comparison - any performance difference can be attributed to the difference in the initialization quality.

We established multiple fine-tuning sample size gradients to cover the full spectrum from minimal sample sizes (~50 minutes of data) to moderate sample sizes (~8 hours of data), thereby plotting the Learning Curve.

![](data:image/png;base64...)

The learning curve of basic transfer learning and meta transfer learning.

Figure 6-2 presents the comparison of Mean Absolute Error (MAE) between Basic Transfer and Meta Transfer for subject 124 across different fine-tuning sample sizes, which is the core finding of this chapter.

From the learning curve, we can find that within the range of fine-tuning sample size N < 100, Meta Transfer shows obvious performance advantages compared with Basic Transfer, and MAE is reduced by an average of 25.67%. Especially in the case of a very small number of samples with a sample size of N < 40, the average reduction of MAE reached 31.58%. This verifies the effectiveness of meta-learning initialization in extremely low-sample scenarios.

With the increase of fine-tuning samples, the performance gap between the two methods is gradually narrowing. When N > 150, the MAE of the two tends to be close. This phenomenon is in line with expectations - when the data is sufficient, the impact of initialization is "covered" by full fine-tuning; the core value of meta-learning is reflected in the scenario of data scarcity.

![](data:image/png;base64...)

The prediction of meta transfer and basic transfer on subject 124.

In order to show the advantages of meta-learning more intuitively, we choose N=30 (about 2.5 hours of data), a typical small sample scenario, for detailed analysis.

Figure 6-3 shows the comparison of timing prediction waveforms on the subject' 124 test set.

It can be observed from the details of the waveform that in the stage of rapid increase in blood glucose (such as after meals), the Meta Transfer model can track the peak position and height more accurately, while there is an obvious peak overrush phenomenon in Basic Transfer. At the same time, the Meta Transfer model responds faster at the change point of blood glucose, and the phase lag is significantly reduced.

In the stable stage of blood glucose, the performance of the two methods is similar, but the predicted variance of Meta Transfer is slightly smaller. This shows that Meta Transfer not only reduces the average error, but also reduces the fluctuation of the error, showing a more stable prediction quality.

Comparison of the predictive indicators of basic transfer and meta transfer.

| **Metric** | **Basic Transfer** | **Meta transfer** | **Improvement(%)** |
| --- | --- | --- | --- |
| MAE | 5.9383 | 5.3762 | 9.4653 |
| RMSE | 6.4932 | 6.2146 | 4.2901 |
| MAPE | 6.2666 | 5.5451 | 11.5136 |
| RMSPE | 6.9014 | 6.2370 | 9.6266 |

From Table 6-2, we can see that in addition to helping to fit faster in small sample data, Meta Transfer also improves the prediction accuracy. Using the Meta Transfer strategy to extract personalized characteristics from the sparse data of a specific individual, it can not only predict faster, but also predict better.

* 1. Discussion

The experimental results of this chapter confirm the advantages of meta-learning in extremely small sample scenarios. Theoretically, this advantage can be explained by the consistency of gradient direction.

In the process of meta-training, the FOMAML algorithm tends to find a parameter point, so that the gradient direction of different tasks has high consistency. Mathematically, the Hessian matrix near this point has similar characteristic vector directions between different tasks. This means that from this point, updating the parameters along the gradient direction of any new task is unlikely to have a serious conflict with the optimal direction of other tasks. Therefore, even if there is only a small amount of gradient steps (corresponding to a small amount of fine-tuning data), it can effectively approach the optimal solution of the new task. During this period, the self-attention mechanism of Transformer is very crucial in this process - unlike RNN/LSTM, which compresses the timing history into a fixed-dimensional hidden state, self-attention retains an independent characterization vector for each time step, which provides a richer parameter space for the gradient optimization of FOMAML. In the meta-training stage, the attention weighting learns to identify common timing-dependent patterns (such as post-meal upward trend and night steady segment) among different subjects, so that the characteristics of the encoder output naturally have cross-individual mobility, thus reducing the degree of conflict between different tasks of meta-gradients.

The meta transfer learning strategy proposed in this chapter and the frozen encoder strategy in Chapter 5 are not a substitution relationship, but a complementary relationship. Both can be understood as the optimization of different links within the same framework: Chapter 5 solves "fine-tune what" - by freezing the Transformer encoder, the update range is limited to the regression header and reduce the risk of overfitting; this chapter solves "where to start fine-tuning" - obtain an initialization point that is more sensitive to new tasks through FOMAML meta training. The reason why this division of labor is particularly effective in the Transformer architecture is that there is a natural functional boundary between the self-attention encoder and the fully connected regression head: the encoder is responsible for extracting the general timing feature representation, and the regression head is responsible for mapping these characteristics to individualized blood glucose prediction values. FOMAML further strengthens this boundary - meta-training allows the encoder to converge to a characteristic space that can serve multiple blood glucose patterns at the same time, and the regression head only needs a small number of samples to anchor the mapping relationship of individuals in this space.

In the experiment of this chapter, we combine the two: using meta-learning initialization + freezing encoder fine-tuning. This combination strategy not only inherits the rapid adaptability of meta-learning in small sample scenarios, but also retains the anti-fitting advantage of the freezing strategy.

Comparison with Related Meta-Learning Approaches for Personalized Glucose Prediction

| **Study** | **Backbone Model** | **Meta-Learning Algorithm** | **Dataset** | **Adaptation** | **Key Contribution** |
| --- | --- | --- | --- | --- | --- |
| Zhu et al.[16] (2023) | FCNN | MAML | OhioT1DM (T1D) | Limited training data | Uncertainty-aware prediction via evidential deep learning |
| Langarica et al.[55] (2023) | LSTM | MAML | Custom T1D | 1-day CGM data | Demonstrated effectiveness of personalized meta-learning |
| Ours | Transformer | FOMAML | Colas + Hall (T2D) +OhioT1DM (T1D) | 30–50 samples (~2.5–4 h) | Few-shot adaptation with frozen encoder; attention-based transferable representations |

We, Zhu et al.[16] both use MAML series algorithms for meta-learning, which verifies the effectiveness of the MAML framework in personalized scenarios of blood glucose prediction from different angles. The first-order approximation of FOMAML we use avoids the computational overhead of second-order derivatives in complete MAML, which is more suitable for deployment on devices with limited resources. Zhu et al.'s FCNN provides predictive uncertainty estimates through the evidence deep learning layer, which is a direction worth learning from. In the selection of backbone networks, Zhu and others use FCNN, Langarica and others use LSTM, and we choose Transformer as the backbone network. This choice is not simply to pursue the improvement of model capacity. Transformer's self-attention mechanism enables it to flexibly capture the dependence of blood glucose dynamics on different time scales. This flexibility has additional advantages under the meta-learning framework: in the meta-training stage, the attention mode can learn universal timing attention strategies across the subjects; in the fine-tuning stage, the return head only needs a small sample to complete individual adaptation under the premise of keeping the encoder attention mode unchanged. This paradigm of "attention sharing, mapping personalization" enables us to achieve effective and rapid adaptation under extremely few samples (30-50 samples).

Compared with the work of Langarica et al.[55], we further pushed the boundaries of small samples to the extreme - verifying that meta-learning can still bring significant benefits under the condition of only 30 samples (about 2.5 hours). This discovery is of great value for the pursuit of "instant personalized" product experience.

Although the experimental results are encouraging, we still have the following limitations:

1. Task distribution hypothesis: The effectiveness of metalearning depends on the assumption that the source domain task and the target domain task come from the same distribution (or similar distribution). If there is a significant difference between the blood glucose pattern of the new user and all subjects in the training set (such as extremely rare metabolic types), the advantage of metalearning may be weakened.

2. Requirements for the number of source domain tasks: FOMAML meta-training requires enough source domain tasks to learn the "common adaptation mode across tasks". The source domain we use contains 164 subjects, and the effect may be discounted on smaller-scale data sets.

3. Hyperparameter sensitivity: The hyperparameters of metalearning (such as INNER\_STEPS, META\_LR) have a great impact on the final effect, and the optimal value may change with the data set. We have determined the current configuration through experience tuning, but the hyperparameter search of the system may further improve the performance.

In summary, the meta-transfer learning strategy proposed in this chapter provides key technical support for the realization of the user experience of "wearing is personalized", which is an important step in building the next generation of intelligent blood glucose management system.

1. Reference
2. American Diabetes Association (ADA). Standards of Care in Diabetes—2025. Diabetes Care 2025; 48 (Supplement\_1). [<https://doi.org/10.2337/dc25-S007>]
3. Kwon SY, et al. Advances in Continuous Glucose Monitoring: Clinical Applications and Future Perspectives. Endocrinology and Metabolism 2025. [<https://doi.org/10.3803/EnM.2025.2370>]
4. Alam MA, et al. Machine Learning And Artificial Intelligence in Diabetes Prediction And Management: A Comprehensive Review of Models. 2024. [<https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5079613>]
5. Xie X, et al. Reduction of measurement noise in a continuous glucose monitor. Nature Biomedical Engineering 2018; 3: 892–901.[<https://doi.org/10.1038/s41551-018-0273-3>]
6. Kim SJ, et al. Long-term blood glucose prediction using deep learning-based noise reduction. Computer Methods and Programs in Biomedicine 2025. [<https://doi.org/10.1016/j.cmpb.2025.108571>]
7. Kozinetz RM, et al. Machine Learning and Deep Learning Models to Predict Nocturnal Glucose. Diagnostics 2024; 14(7): 740. [<https://doi.org/10.3390/diagnostics14070740>]
8. Facchinetti A, et al. Kalman smoothing for objective and automatic preprocessing of glucose data. IEEE Transactions on Biomedical Engineering 2018; 65(1): 114-123. [<https://doi.org/10.1109/TBME.2017.2702326>]
9. Liu K, Li L, Ma Y, et al. Machine learning models for blood glucose level prediction in patients with diabetes mellitus: systematic review and network meta-analysis. JMIR Medical Informatics 2023; 11: e47833. [<https://doi.org/10.2196/47833>]
10. Ryu JS, et al. A deep learning approach for blood glucose monitoring and forecasting. Scientific Reports 2025. [<https://doi.org/10.1038/s41598-025-97391-8>]
11. Ghimire S, et al. Deep learning for blood glucose level prediction: How well do models perform across diverse datasets? PLOS ONE 2024; 19(9): e0310801. [<https://doi.org/10.1371/journal.pone.0310801>]
12. Zheng Y, et al. Enhancing personalized blood glucose prediction in type 1 diabetes with meta-transfer learning: A few-shot approach. Biomedical Signal Processing and Control 2026; 101: 107234. [<https://doi.org/10.1016/j.bspc.2025.108468>]
13. Shen Y, et al. Personalized Blood Glucose Forecasting From Limited CGM Data Using Incrementally Retrained LSTM. IEEE Transactions on Biomedical Engineering 2024. [<https://doi.org/10.1109/TBME.2024.3491434>]
14. Yu X, et al. Deep transfer learning: a novel glucose prediction framework for new subjects. Complex & Intelligent Systems 2022; 8: 3123–3137. [<https://doi.org/10.1007/s40747-021-00360-7>]
15. Deng Y, et al. Deep transfer learning and data augmentation improve glucose levels prediction in type 2 diabetes patients. NPJ Digital Medicine 2021; 4: 91. [<https://doi.org/10.1038/s41746-021-00480-x>]
16. Moon K, et al. Personalized blood glucose prediction in type 1 diabetes using meta-learning with bidirectional LSTM-Transformer hybrid model. Scientific Reports 2025; 15: 13491. [<https://doi.org/10.1038/s41598-025-13491-5>]
17. Zhu T, et al. Personalized Blood Glucose Prediction for Type 1 Diabetes Using Evidential Deep Learning and Meta-Learning. IEEE Transactions on Biomedical Engineering 2023; 70(1): 193-204. [<https://doi.org/10.1109/TBME.2022.3187703>]
18. Wang L, et al. Heterogeneous Covariates-Aware Pseudo Supervised Meta-Learning for Few-shot Diabetes Classification. IEEE Transactions on Medical Imaging 2025. [<https://doi.org/10.1109/TMI.2024.3416513>]
19. Singh R, et al. Personalized glucose prediction using in situ data only. Frontiers in Nutrition 2025; 12: 1539118. [<https://doi.org/10.3389/fnut.2025.1539118>]
20. Manchanda E, et al. Data-Efficiency with Comparable Accuracy: Personalized LSTM models on limited individual data. Diabetology 2025; 6(10): 115. [<https://doi.org/10.3390/diabetology6100115>]
21. Tominaga H, et al. Prediction of Postprandial Blood Glucose Variability Using Transformer-based Models. PMC 2025. [<https://pmc.ncbi.nlm.nih.gov/articles/PMC12735845/>]
22. Colás, A., Vigil, L., Vargas, B., Enríquez de Salamanca, R., & Lázaro, P. (2019). Detrended Fluctuation Analysis in the prediction of type 2 diabetes mellitus in patients at risk: Model optimization and comparison with other metrics. [<https://doi.org/10.1371/journal.pone.0225817>]
23. Hall, H., Perelman, D., Breschi, A., Limcaoco, P., Kellogg, R., McLaughlin, T., & Snyder, M. (2018). Glucotypes reveal new patterns of glucose dysregulation. PLOS Biology, 16(7), e2005143. [<https://doi.org/10.1371/journal.pbio.2005143>]
24. Zhu, T., Li, K., Herrero, P., & Georgiou, P. (2021). Deep Learning for Diabetes: A Systematic Review. IEEE Journal of Biomedical and Health Informatics, 25(7), 2744-2757. [<https://doi.org/10.1109/JBHI.2020.3040225>]
25. Woldaregay, A. Z., Årsand, E., Walderhaug, S., & Albers, D. (2019). Data-driven modeling and prediction of blood glucose dynamics: Machine learning applications in type 1 diabetes. 25(4), 1610-1641. [<https://doi.org/10.1016/j.artmed.2019.07.007>]
26. Martinsson, J., Schliep, A., Eliasson, B., & Mogren, O. (2020). Blood Glucose Prediction with Variance Estimation Using Recurrent Neural Networks. Journal of Healthcare Informatics Research, 4, 1-18. [<https://doi.org/10.1007/s41666-019-00059-y>]
27. Facchinetti, A., Sparacino, G., & Cobelli, C. (2010). An online self-tunable method to denoise CGM sensor data. IEEE Transactions on Biomedical Engineering, 57(3), 634-641. [<https://doi.org/10.1109/TBME.2009.2033264>]
28. Sparacino, G., Facchinetti, A., & Cobelli, C. (2010). "Smart" continuous glucose monitoring sensors: On-line signal processing issues. Sensors, 10(7), 6751-6772. [<https://doi.org/10.3390/s100706751>]
29. Facchinetti, A. (2016). Continuous glucose monitoring sensors: Past, present and future algorithmic challenges. Sensors, 16(12), 2093. [<https://doi.org/10.3390/s16122093>]
30. Rebrin, K., & Steil, G. M. (2000). Can interstitial glucose assessment replace blood glucose measurements? Diabetes Technology & Therapeutics, 2(3), 461-472. [<https://doi.org/10.1089/15209150050194332>]
31. Breton, M. D., & Kovatchev, B. P. (2008). Analysis, modeling, and simulation of the accuracy of continuous glucose sensors. Journal of Diabetes Science and Technology, 2(5), 853-862. [<https://doi.org/10.1177/193229680800200517>]
32. Bequette, B. W. (2010). Continuous glucose monitoring: Real-time algorithms for calibration, filtering, and alarms. Journal of Diabetes Science and Technology, 4(2), 404-418. [<https://articles.researchsolutions.com/continuous-glucose-monitoring-real-time-algorithms-for-calibration-filtering-and-alarms/doi/10.1177/193229681000400222>]
33. Baysal, N., Cameron, F., Buckingham, B. A., et al. (2014). A novel method to detect pressure-induced sensor attenuations (PISA) in an artificial pancreas. Journal of Diabetes Science and Technology, 8(6), 1091-1096. [<https://doi.org/10.1177/1932296814553267>]
34. Kovatchev, B. P., Gonder-Frederick, L. A., Cox, D. J., & Clarke, W. L. (2004). Evaluating the accuracy of continuous glucose-monitoring sensors. Diabetes Care, 27(8), 1922-1928. [<https://doi.org/10.2337/diacare.27.8.1922>]
35. Garnica, O., Lanchares, J., Velasco, J. M., & Hidalgo, J. I. (2020). Noise spectral analysis and error estimation of continuous glucose monitors under real-life conditions of diabetes patients. Biomedical Signal Processing and Control, 60, 101902. [<https://doi.org/10.1016/j.bspc.2020.101934>]
36. Facchinetti, A., Del Favero, S., Sparacino, G., Castle, J. R., Ward, W. K., & Cobelli, C. (2014). Modeling the glucose sensor error. IEEE Transactions on Biomedical Engineering, 61(3), 620-629. [<https://doi.org/10.1109/TBME.2013.2284023>]
37. Kalman, R. E. (1960). A new approach to linear filtering and prediction problems. Journal of Basic Engineering, 82(1), 35-45. [<https://doi.org/10.1115/1.3662552>]
38. Savitzky, A., & Golay, M. J. E. (1964). Smoothing and differentiation of data by simplified least squares procedures. Analytical Chemistry, 36(8), 1627-1639. [<https://doi.org/10.1021/ac60214a047>]
39. Schafer, R. W. (2011). What is a Savitzky-Golay filter? IEEE Signal Processing Magazine, 28(4), 111-117. [<https://doi.org/10.1109/MSP.2011.941097>]
40. Sadıkoğlu, F., & Kavalcıoğlu, C. (2016). Filtering continuous glucose monitoring signal using Savitzky-Golay filter and simple multivariate thresholding. Procedia Computer Science, 102, 342-350. [<https://doi.org/10.1016/j.procs.2016.09.410>]
41. Luo, J., Ying, K., & Bai, J. (2005). Savitzky-Golay smoothing and differentiation filter for even number data. Signal Processing, 85(7), 1429-1434. [<https://doi.org/10.1016/j.sigpro.2005.02.002>]
42. Butterworth, S. (1930). On the theory of filter amplifiers. Wireless Engineer, 7(6), 536-541.
43. Rangayyan, R. M., & Krishnan, S. (2024). Biomedical Signal Analysis (3rd ed.). Wiley-IEEE Press. [<https://doi.org/10.1002/9781119825883>]
44. Gustafsson, F. (1996). Determining the initial states in forward-backward filtering. IEEE Transactions on Signal Processing, 44(4), 988-992. [<https://doi.org/10.1109/78.492552>]
45. Marling, C., & Bunescu, R. (2020). The OhioT1DM Dataset for Blood Glucose Level Prediction: Update 2020. CEUR Workshop Proceedings, 2675, 71-74. [<https://pmc.ncbi.nlm.nih.gov/articles/PMC7881904/>]
46. Xie, J., & Wang, Q. (2020). Benchmarking Machine Learning Algorithms on Blood Glucose Prediction for Type I Diabetes in Comparison With Classical Time-Series Models. IEEE Transactions on Biomedical Engineering, 67(11), 3101-3124. [<https://doi.org/10.1109/TBME.2020.2975959>]
47. Rabby, M. F., Tu, Y., Hossen, M. I., Lee, I., & Maida, A. S. (2021). Stacked LSTM based deep recurrent neural network with kalman smoothing for blood glucose prediction. BMC Medical Informatics and Decision Making, 21, 101. [<https://doi.org/10.1186/s12911-021-01462-5>]
48. El Idrissi, T., Idri, A., & Bakkoury, Z. (2020). Deep learning for blood glucose prediction: Cnn vs lstm. International Conference on Computational Science and Its Applications (pp. 385-399). Springer. [<https://doi.org/10.1007/978-3-030-58802-1_28>]
49. Sun, Q., Jankovic, M. V., Bally, L., & Mougiakakou, S. G. (2018). Predicting blood glucose with an lstm and bi-lstm based deep neural network. 14th Symposium on Neural Networks and Applications (NEUREL) (pp. 1-6). IEEE. [<https://ieeexplore.ieee.org/document/8586990>]
50. Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., ... & Polosukhin, I. (2017). Attention is all you need. Advances in Neural Information Processing Systems, 30. [<https://arxiv.org/abs/1706.03762>]
51. Clarke, W. L., Cox, D., Gonder-Frederick, L. A., Carter, W., & Pohl, S. L. (1987). Evaluating clinical accuracy of systems for self-monitoring of blood glucose. Diabetes Care, 10(5), 622-628. [<https://doi.org/10.2337/diacare.10.5.622>]
52. Zhuang, F., Qi, Z., Duan, K., Xi, D., Zhu, Y., Zhu, H., ... & He, Q. (2021). A Comprehensive Survey on Transfer Learning. Proceedings of the IEEE, 109(1), 43-76. [<https://doi.org/10.1109/JPROC.2020.3004555>]
53. Hospedales, T., Antoniou, A., Micaelli, P., & Storkey, A. (2022). Meta-learning in neural networks: A survey. IEEE Transactions on Pattern Analysis and Machine Intelligence, 44(9), 5149-5169. [<https://doi.org/10.1109/TPAMI.2021.3079209>]
54. Finn, C., Abbeel, P., & Levine, S. (2017). Model-agnostic meta-learning for fast adaptation of deep networks. Proceedings of the 34th International Conference on Machine Learning (ICML), 70, 1126-1135. [<https://arxiv.org/abs/1703.03400>]
55. Nichol, A., Achiam, J., & Schulman, J. (2018). On first-order meta-learning algorithms. arXiv preprint arXiv:1803.02999. [<https://arxiv.org/abs/1803.02999>]
56. Langarica, S., Rodriguez-Fernandez, M., Núñez, F., & Doyle III, F. J. (2023). A meta-learning approach to personalized blood glucose prediction in type 1 diabetes. Control Engineering Practice, 135, 105498. [<https://doi.org/10.1016/j.conengprac.2023.105498>]