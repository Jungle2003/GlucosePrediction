import matplotlib.pyplot as plt
import numpy as np

def clarke_error_grid(ref_values, pred_values, title_string, unit='mg/dL'):
    """
    绘制标准的 Clarke Error Grid (CEG) 图。
    参考实现: Trevor Tsue (2017) 基于 Edgar Guevara Codina (2013) 的 Matlab 版本。
    
    参数:
    ref_values: 参考血糖值 (真实值)
    pred_values: 预测血糖值
    title_string: 图表标题
    unit: 血糖单位 ('mg/dL' 或 'mmol/L')
    """
    
    # 转换单位为 mg/dL
    if unit == 'mmol/L':
        ref = np.array(ref_values) * 18.0182
        pred = np.array(pred_values) * 18.0182
    else:
        ref = np.array(ref_values)
        pred = np.array(pred_values)

    assert len(ref) == len(pred), "Reference and prediction values must have the same length"

    # 清除当前图像
    plt.figure(figsize=(8, 8))
    
    # 设置绘图风格
    plt.gca().set_facecolor('white')
    plt.gca().set_aspect('equal')
    
    # 绘制散点
    plt.scatter(ref, pred, marker='o', color='black', s=10, alpha=0.5)
    
    # 设置标题和标签
    plt.title(title_string + " Clarke Error Grid", fontsize=14, pad=15)
    plt.xlabel(f"Reference Concentration ({unit})", fontsize=12)
    plt.ylabel(f"Prediction Concentration ({unit})", fontsize=12)
    
    # 设置坐标轴范围和刻度
    plt.xlim(0, 400)
    plt.ylim(0, 400)
    plt.xticks([0, 50, 100, 150, 200, 250, 300, 350, 400])
    plt.yticks([0, 50, 100, 150, 200, 250, 300, 350, 400])

    # 绘制区域边界线 (严格遵循标准定义)
    plt.plot([0, 400], [0, 400], ':', c='black', alpha=0.3) # 45度对角线
    
    # Zone A & B boundaries
    plt.plot([0, 175/3], [70, 70], '-', c='black', linewidth=1)
    plt.plot([175/3, 400/1.2], [70, 400], '-', c='black', linewidth=1)
    plt.plot([70, 70], [84, 400], '-', c='black', linewidth=1)
    plt.plot([0, 70], [180, 180], '-', c='black', linewidth=1)
    plt.plot([70, 290], [180, 400], '-', c='black', linewidth=1)
    plt.plot([70, 70], [0, 56], '-', c='black', linewidth=1)
    plt.plot([70, 400], [56, 320], '-', c='black', linewidth=1)
    plt.plot([180, 180], [0, 70], '-', c='black', linewidth=1)
    plt.plot([180, 400], [70, 70], '-', c='black', linewidth=1)
    plt.plot([240, 240], [70, 180], '-', c='black', linewidth=1)
    plt.plot([240, 400], [180, 180], '-', c='black', linewidth=1)
    plt.plot([130, 180], [0, 70], '-', c='black', linewidth=1)

    # 添加区域标注
    plt.text(30, 15, "A", fontsize=15, fontweight='bold')
    plt.text(370, 260, "B", fontsize=15, fontweight='bold')
    plt.text(280, 370, "B", fontsize=15, fontweight='bold')
    plt.text(160, 370, "C", fontsize=15, fontweight='bold')
    plt.text(160, 15, "C", fontsize=15, fontweight='bold')
    plt.text(30, 140, "D", fontsize=15, fontweight='bold')
    plt.text(370, 120, "D", fontsize=15, fontweight='bold')
    plt.text(30, 370, "E", fontsize=15, fontweight='bold')
    plt.text(370, 15, "E", fontsize=15, fontweight='bold')

    # 统计各区域百分比 (严格逻辑)
    zone = [0] * 5
    for i in range(len(ref)):
        # Zone A
        if (ref[i] <= 70 and pred[i] <= 70) or (pred[i] <= 1.2*ref[i] and pred[i] >= 0.8*ref[i]):
            zone[0] += 1
        # Zone E
        elif (ref[i] >= 180 and pred[i] <= 70) or (ref[i] <= 70 and pred[i] >= 180):
            zone[4] += 1
        # Zone C
        elif ((ref[i] >= 70 and ref[i] <= 290) and pred[i] >= ref[i] + 110) or ((ref[i] >= 130 and ref[i] <= 180) and (pred[i] <= (7/5)*ref[i] - 182)):
            zone[2] += 1
        # Zone D
        elif (ref[i] >= 240 and (pred[i] >= 70 and pred[i] <= 180)) or (ref[i] <= 175/3 and (pred[i] <= 180 and pred[i] >= 70)) or (ref[i] <= 70 and (pred[i] <= 180 and pred[i] >= 70)):
            zone[3] += 1
        # Zone B
        else:
            zone[1] += 1

    total = len(ref)
    percents = [(z / total) * 100 for z in zone]
    
    # 在图上显示统计结果
    stats_text = "Zone Distribution:\n" + \
                 f"Zone A: {percents[0]:.1f}%\n" + \
                 f"Zone B: {percents[1]:.1f}%\n" + \
                 f"Zone C: {percents[2]:.1f}%\n" + \
                 f"Zone D: {percents[3]:.1f}%\n" + \
                 f"Zone E: {percents[4]:.1f}%"
    
    plt.text(20, 380, stats_text, fontsize=10, verticalalignment='top', 
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
    
    plt.grid(True, linestyle='--', alpha=0.2)
    plt.tight_layout()
    
    return plt, percents