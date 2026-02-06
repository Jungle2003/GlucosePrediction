import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.signal import savgol_filter
import os

# 配置
# Window 15 = 15*5min = 75min
WINDOW_LENGTH = 15 
POLYORDER = 3

input_file = 'ohio.csv'
output_file = 'ohio_sg_filtered.csv'

def apply_sg_filter(data, window_length=15, polyorder=3):
    if len(data) < window_length:
        return data
    return savgol_filter(data, window_length, polyorder, mode='interp')

if __name__ == "__main__":
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        exit(1)

    print(f"Reading {input_file}...")
    df = pd.read_csv(input_file)
    df['time'] = pd.to_datetime(df['time'])
    
    # 确保排序
    df = df.sort_values('time')
    
    print("Applying S-G Filter...")
    
    # 执行滤波 (处理整个序列，因为是单个受试者且连续)
    gl_values = df['gl'].values
    if len(gl_values) >= WINDOW_LENGTH:
        filtered_values = apply_sg_filter(gl_values, window_length=WINDOW_LENGTH, polyorder=POLYORDER)
        df['gl'] = filtered_values  # 直接覆盖 gl 列，模拟 served.csv 格式 (即 gl 列存储处理后的数据)
        print("Filter applied.")
    else:
        print("Data too short for filter criteria.")

    # 导出
    df.to_csv(output_file, index=False)
    print(f"Saved filtered data to {output_file}")
    
    # 简易绘图检查
    plt.figure(figsize=(10, 5))
    plt.plot(gl_values[:500], label='Original', alpha=0.5)
    plt.plot(filtered_values[:500], label='S-G Filtered', linewidth=2)
    plt.title('S-G Filter Check (First 500 points)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('ohio_sg_check.png')
    print("Saved check plot to ohio_sg_check.png")
