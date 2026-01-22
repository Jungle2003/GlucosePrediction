import pandas as pd
import xml.etree.ElementTree as ET
import os

# 配置路径
xml_file = 'ohio.xml'
output_file = 'ohio.csv'

# 用户指定的常量
FIXED_ID = 302
FIXED_AGE = 35.0
FIXED_BMI = 26.3

def parse_ohio_xml(xml_path):
    if not os.path.exists(xml_path):
        print(f"Error: File not found {xml_path}")
        return None

    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # 查找 glucose_level 节点
    glucose_level_node = root.find('glucose_level')
    if glucose_level_node is None:
        print("Error: 'glucose_level' node not found in XML")
        return None
        
    data = []
    
    # 遍历所有 event 节点
    for event in glucose_level_node.findall('event'):
        ts_str = event.get('ts')
        value_str = event.get('value')
        
        if ts_str and value_str:
            data.append({
                'time': ts_str,
                'gl': float(value_str)
            })
            
    df = pd.DataFrame(data)
    return df

def process_data(df):
    if df is None or df.empty:
        return None
        
    # 1. 转换时间格式 (DD-MM-YYYY HH:MM:SS -> YYYY-MM-DD HH:MM:SS)
    df['time'] = pd.to_datetime(df['time'], format='%d-%m-%Y %H:%M:%S')
    
    # 2. 添加固定列
    df['id'] = FIXED_ID
    df['age'] = FIXED_AGE
    df['bmi'] = FIXED_BMI
    
    # 3. 列重排以匹配目标格式: id, time, gl, age, bmi
    df = df[['id', 'time', 'gl', 'age', 'bmi']]
    
    # 4. 按时间排序
    df = df.sort_values('time')
    
    return df

if __name__ == "__main__":
    print(f"Processing {xml_file}...")
    
    df_raw = parse_ohio_xml(xml_file)
    
    if df_raw is not None:
        df_processed = process_data(df_raw)
        
        if df_processed is not None:
            # 保存为 CSV
            df_processed.to_csv(output_file, index=False)
            print(f"Successfully processed {len(df_processed)} records.")
            print(f"Saved to {os.path.abspath(output_file)}")
            print("\nPreview:")
            print(df_processed.head())
            print(df_processed.dtypes)
        else:
            print("Failed to process data.")
    else:
        print("Failed to parse XML.")
