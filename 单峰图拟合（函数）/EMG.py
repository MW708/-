import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import erfc
import os

# 重新读取Excel文件的Sheet3
file_path = r"I:\VS_code\VS_code_Projects\小工具\单峰图拟合（函数）\110测试——16种防晒剂的紫外数据.xlsx"
sheet3 = pd.read_excel(file_path, sheet_name="Sheet3")

# 定义指数修饰高斯函数（EMG）
def emg(x, A, mu, sigma, lam):
    return (A * lam / 2) * np.exp((lam / 2) * (2 * mu + lam * sigma ** 2 - 2 * x)) * \
        erfc((mu + lam * sigma ** 2 - x) / (np.sqrt(2) * sigma))


# 数据清洗（使用您之前的代码）
sheet3_cleaned = {}
headers3 = list(sheet3.iloc[0])
data3 = sheet3.iloc[2:].reset_index(drop=True)

for i in range(0, len(sheet3.columns) - 1, 2):
    label = headers3[i]
    nm_col = sheet3.columns[i]
    A_col = sheet3.columns[i + 1]

    if label and not pd.isna(label):
        nm = pd.to_numeric(data3[nm_col], errors="coerce")
        A = pd.to_numeric(data3[A_col], errors="coerce")
        df = pd.DataFrame({"nm": nm, "A": A}).dropna()
        sheet3_cleaned[label] = df

# 创建输出目录
output_dir = "detailed_fits"
os.makedirs(output_dir, exist_ok=True)

fit_results = {}

# 设置中文字体（如果需要显示中文）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

for label, df in sheet3_cleaned.items():
    x = df["nm"].values
    y = df["A"].values

    # 初始猜测参数
    p0 = [max(y), x[np.argmax(y)], 10, 0.05]

    try:
        # 执行拟合
        popt, pcov = curve_fit(emg, x, y, p0=p0, maxfev=20000)
        fit_results[label] = popt

        # 创建包含子图的详细图表
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

        # 子图1: 拟合曲线
        ax1.scatter(x, y, s=20, alpha=0.7, color='blue', label='Experimental data')
        x_fine = np.linspace(min(x), max(x), 500)  # 更平滑的拟合曲线
        ax1.plot(x_fine, emg(x_fine, *popt), '-', color='red', linewidth=2, label='EMG fit')
        ax1.set_xlabel("Wavelength (nm)", fontsize=12)
        ax1.set_ylabel("Absorbance (A)", fontsize=12)
        ax1.set_title(f"EMG Fit: {label}", fontsize=14, fontweight='bold')
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)

        # 子图2: 残差图
        y_pred = emg(x, *popt)
        residuals = y - y_pred
        ax2.scatter(x, residuals, s=20, alpha=0.7, color='green', label='Residuals')
        ax2.axhline(y=0, color='red', linestyle='--', linewidth=1, label='Zero line')
        ax2.set_xlabel("Wavelength (nm)", fontsize=12)
        ax2.set_ylabel("Residuals", fontsize=12)
        ax2.set_title("Residuals Plot", fontsize=12, fontweight='bold')
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)

        # 计算统计指标
        rmse = np.sqrt(np.mean(residuals ** 2))
        r_squared = 1 - np.sum(residuals ** 2) / np.sum((y - np.mean(y)) ** 2)

        # 计算参数的标准误差
        perr = np.sqrt(np.diag(pcov)) if pcov is not None else [0, 0, 0, 0]

        # 在图上添加详细文本信息
        text_str = f"""Fit Parameters:
Amplitude (A) = {popt[0]:.6f} ± {perr[0]:.6f}
Position (μ) = {popt[1]:.4f} ± {perr[1]:.4f} nm
Width (σ) = {popt[2]:.4f} ± {perr[2]:.4f}
Decay (λ) = {popt[3]:.6f} ± {perr[3]:.6f}

Fit Quality:
R² = {r_squared:.6f}
RMSE = {rmse:.6f}
Data Points = {len(x)}
Peak Position = {popt[1]:.2f} nm
Peak Height = {popt[0]:.4f}"""

        # 添加文本框
        plt.figtext(0.72, 0.25, text_str,
                    bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.9),
                    fontfamily='monospace', fontsize=9)

        plt.tight_layout()

        # 保存图片
        filename = f"detailed_{label.replace(' ', '_').replace('/', '_')}.png"
        plt.savefig(os.path.join(output_dir, filename), dpi=300, bbox_inches='tight')

        # 显示图片
        plt.show()

        print(f"✓ Saved detailed plot: {filename}")
        print(f"  Fit parameters: A={popt[0]:.4f}, μ={popt[1]:.2f}nm, σ={popt[2]:.2f}, λ={popt[3]:.4f}")
        print(f"  Fit quality: R²={r_squared:.4f}, RMSE={rmse:.4f}")
        print("-" * 60)

    except RuntimeError as e:
        print(f"✗ Fit failed for {label}: {e}")
        continue

# 输出汇总表格
if fit_results:
    print("\n" + "=" * 80)
    print("FITTING RESULTS SUMMARY")
    print("=" * 80)

    fit_table = pd.DataFrame(fit_results, index=["A", "μ", "σ", "λ"]).T
    print(fit_table)

    # 保存拟合结果到CSV文件
    fit_table.to_csv(os.path.join(output_dir, "fitting_parameters_summary.csv"))
    print(f"\n✓ Fitting parameters saved to: {output_dir}/fitting_parameters_summary.csv")
else:
    print("No successful fits!")

print(f"\nAll detailed plots saved to: {output_dir}/")