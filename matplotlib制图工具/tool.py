import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号

# 文件路径
file_path = r"I:\VS_code\VS_code_Projects\小工具\matplotlib制图工具\110测试——16种防晒剂的紫外数据.xlsx"

# 先检查文件是否存在
import os
if not os.path.exists(file_path):
    print(f"文件不存在: {file_path}")
    # 可以尝试列出目录内容来调试
    dir_path = os.path.dirname(file_path)
    if os.path.exists(dir_path):
        print("目录中的文件:")
        for file in os.listdir(dir_path):
            print(f"  {file}")
else:
    print("文件存在，继续执行...")

def process_sheet_data(sheet_data, sheet_name):
    """处理单个sheet的数据，提取(nm, A)数据对"""
    sheet_cleaned = {}
    
    # 提取标题行（第0行）
    headers = list(sheet_data.iloc[0])
    
    # 从第二行开始正式数据（第2行起是数据）
    data = sheet_data.iloc[2:].reset_index(drop=True)
    
    # 按列配对 (nm, A)
    for i in range(0, len(sheet_data.columns), 2):
        if i + 1 < len(headers):  # 确保不越界
            label = headers[i]  # 组名，如 "BP-1"
            nm_col = sheet_data.columns[i]
            A_col = sheet_data.columns[i + 1]
            
            if label and not pd.isna(label) and label.strip():
                try:
                    nm = pd.to_numeric(data[nm_col], errors="coerce")
                    A = pd.to_numeric(data[A_col], errors="coerce")
                    df = pd.DataFrame({"nm": nm, "A": A}).dropna()
                    if not df.empty:
                        sheet_cleaned[label] = df
                except Exception as e:
                    print(f"处理 {sheet_name} 列 {label} 时出错: {e}")
                    continue
    
    return sheet_cleaned

try:
    excel_data = pd.ExcelFile(file_path)
    
    # 查看包含的工作表
    print("工作表:", excel_data.sheet_names)
    
    # 读取Sheet1和Sheet3的数据
    sheet1 = pd.read_excel(file_path, sheet_name="Sheet1")
    sheet3 = pd.read_excel(file_path, sheet_name="Sheet3")
    
    # 处理Sheet1数据
    sheet1_cleaned = process_sheet_data(sheet1, "Sheet1")
    print(f"Sheet1 提取到 {len(sheet1_cleaned)} 组数据")
    
    # 处理Sheet3数据
    sheet3_cleaned = process_sheet_data(sheet3, "Sheet3")
    print(f"Sheet3 提取到 {len(sheet3_cleaned)} 组数据")
    
    # 创建图表
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # 绘制Sheet1的曲线
    if sheet1_cleaned:
        colors = plt.cm.tab10(np.linspace(0, 1, len(sheet1_cleaned)))
        for i, (label, df) in enumerate(sheet1_cleaned.items()):
            ax1.plot(df["nm"], df["A"], label=label, color=colors[i], linewidth=1.5)
        
        ax1.set_xlabel("波长 (nm)")
        ax1.set_ylabel("吸光度 (A)")
        ax1.set_title("Sheet1: 广谱防晒剂吸收光谱", fontsize=14, fontweight='bold')
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim(250, 410)  # 根据数据范围设置
    
    # 绘制Sheet3的曲线
    if sheet3_cleaned:
        colors = plt.cm.Set2(np.linspace(0, 1, len(sheet3_cleaned)))
        for i, (label, df) in enumerate(sheet3_cleaned.items()):
            ax2.plot(df["nm"], df["A"], label=label, color=colors[i], linewidth=1.5)
        
        ax2.set_xlabel("波长 (nm)")
        ax2.set_ylabel("吸光度 (A)")
        ax2.set_title("Sheet3: UVB防晒剂吸收光谱", fontsize=14, fontweight='bold')
        ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(250, 410)  # 根据数据范围设置
    
    plt.tight_layout()
    plt.show()
    
    # 可选：分别显示两个图表（如果需要单独查看）
    # 单独显示Sheet1
    plt.figure(figsize=(10, 6))
    if sheet1_cleaned:
        colors = plt.cm.tab10(np.linspace(0, 1, len(sheet1_cleaned)))
        for i, (label, df) in enumerate(sheet1_cleaned.items()):
            plt.plot(df["nm"], df["A"], label=label, color=colors[i], linewidth=2)
        
        plt.xlabel("波长 (nm)")
        plt.ylabel("吸光度 (A)")
        plt.title("Sheet1: 广谱防晒剂吸收光谱", fontsize=14, fontweight='bold')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.xlim(250, 410)
        plt.tight_layout()
        plt.show()
    
    # 单独显示Sheet3
    plt.figure(figsize=(10, 6))
    if sheet3_cleaned:
        colors = plt.cm.Set2(np.linspace(0, 1, len(sheet3_cleaned)))
        for i, (label, df) in enumerate(sheet3_cleaned.items()):
            plt.plot(df["nm"], df["A"], label=label, color=colors[i], linewidth=2)
        
        plt.xlabel("波长 (nm)")
        plt.ylabel("吸光度 (A)")
        plt.title("Sheet3: UVB防晒剂吸收光谱", fontsize=14, fontweight='bold')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.xlim(250, 410)
        plt.tight_layout()
        plt.show()
        
except FileNotFoundError:
    print(f"文件未找到: {file_path}")
    print("请检查文件路径是否正确")
except Exception as e:
    print(f"发生错误: {e}")
    import traceback
    traceback.print_exc()