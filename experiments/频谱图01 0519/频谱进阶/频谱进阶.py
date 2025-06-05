# -*- coding: utf-8 -*-
# 指定文件编码为UTF-8，确保中文路径处理兼容性

import numpy as np  # 基础科学计算库，用于数组操作
import matplotlib.pyplot as plt  # 图表绘制库，用于创建频谱图
from scipy.io import wavfile  # 从SciPy导入音频文件读取功能
from scipy.signal import stft  # 短时傅里叶变换，用于频谱分析
import warnings  # Python内置警告模块，处理可能出现的警告信息

# === 默认参数设置 ===
input_wav = r'D:\CUDA\ceshi.wav'  # 默认音频文件路径
nperseg = 1024  # FFT窗口长度（采样点数），影响频率分辨率和时间分辨率
noverlap = 512   # FFT窗口重叠长度（采样点数），减少频谱边界效应，提高时间连续性
dpi = 150         # 输出图像分辨率（每英寸点数），数值越高图像越清晰

def generate_single_spectrum(input_wav, target_time, nperseg=1024, noverlap=512, dpi=150):
    
    #核心功能：分析音频在指定时间点的频谱特征
    
    #参数说明:
    #    input_wav: 输入音频文件路径(.wav格式)
    #    target_time: 目标时间点（单位：秒）  
    #    nperseg: FFT窗口长度（默认1024点）
    #    noverlap: 窗口重叠长度（默认512点）
    #    dpi: 输出图像分辨率（默认150）
    
    # 返回:
    #    fig: 包含频谱图的matplotlib图形对象
    #    freq: 频率数组（各频率点）
    #    spectrum: 幅度数组（各频率对应的声音强度）
    
    try:
        # === 1. 音频读取与预处理 ===
        # 忽略WAV文件读取时可能出现的无关警告
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")  # 忽略特定警告
            
            # 从磁盘读取音频文件
            sample_rate, data = wavfile.read(input_wav)  # 返回采样率和原始数据
            
            # 处理多声道音频（立体声转单声道）
            if data.ndim > 1:  # 检查是否为多声道
                data = data.mean(axis=1)  # 左右声道取平均值转为单声道
            
            # 音频数据归一化处理：将不同位深度的音频统一到[-1,1]范围
            # 步骤1: 转换为float32浮点数，避免整型计算精度损失
            # 步骤2: 获取音频数据的最大可能值（如16位音频是32768）
            # 步骤3: 除以最大值，归一化到[-1,1]范围
            data = data.astype(np.float32) / np.iinfo(data.dtype).max

        # === 2. 短时傅里叶变换(STFT)计算 ===
        # 关键概念：
        #   STFT将音频分割成多个小片段(窗口)，逐段进行傅里叶变换
        #   返回三个数组：频率点(f)、时间点(t)、复数频谱(Zxx)
        f, t, Zxx = stft(
            data,               # 预处理后的音频数据
            fs=sample_rate,     # 音频采样率(Hz)
            nperseg=nperseg,    # FFT窗口长度(点数)
            noverlap=noverlap,  # 窗口重叠点数
            window='hann'       # 汉宁窗函数，减少频谱泄漏
        )
        
        # === 3. 定位目标时间点 ===
        # 计算时间点之间的索引差：目标时间点(target_time)与所有时间点(t)的绝对差值
        time_diffs = np.abs(t - target_time)  
        
        # 找到最接近的时间点索引：返回差值最小的索引位置
        closest_idx = np.argmin(time_diffs)  
        
        # 提取对应时间点的频谱：
        #   Zxx包含所有时间点的频谱信息(形状为[频率点数×时间点数])
        #   Zxx[:, closest_idx]表示选择第closest_idx个时间点的所有频率
        #   np.abs()取幅度值，忽略相位信息
        spectrum = np.abs(Zxx[:, closest_idx])
        
        # 计算实际找到的时间点(因为时间点不连续，可能略有偏差)
        actual_time = t[closest_idx]  

        # 打印实际找到的时间点
        print(f"target: {target_time}s , actual: {actual_time:.3f}s")
        
        # === 4. 创建频谱图表 ===
        fig = plt.figure(figsize=(10, 6), dpi=dpi)  # 创建10×6英寸图表
        ax = fig.add_subplot(111)  # 添加单一子图(1行1列第1个)
        
        # 绘制频谱曲线：X轴为频率(Hz)，Y轴为幅度
        ax.plot(f, spectrum, color='blue', linewidth=2)
        
        # 设置对数频率轴：更符合人耳对频率的感知特性
        #   人耳对低频变化更敏感，高频变化不敏感
        ax.set_xscale('log')  
        
        # 设置坐标轴范围：
        #   X轴: 20Hz(人耳可闻低频极限)到采样率的一半(Nyquist频率)
        #   Y轴: 0到频谱最大值的1.1倍，留出10%的空间使图表更美观
        ax.set_xlim(20, sample_rate/2)  
        ax.set_ylim(0, np.max(spectrum)*1.1)  
        
        # 添加标签和标题：描述性文本使图表更易读
        ax.set_title(f'{actual_time:.3f}s:')  # 显示实际时间点
        ax.set_xlabel('f (Hz)')  
        ax.set_ylabel('A')  
        
        # 添加网格线：使读数更准确，指定网格同时出现在主刻度和小刻度位置
        ax.grid(True, which='both', linestyle='--', alpha=0.7)  
        
        # 添加时间点标记：
        #   在图表右上角(98%位置)显示实际时间点
        #   bbox参数创建白色半透明背景框，提高文本可读性
        ax.text(
            0.98, 0.98,  # X和Y位置(0-1表示比例位置)
            f't = {actual_time:.3f}s',  # 显示文本
            transform=ax.transAxes,  # 使用坐标系相对位置
            ha='right',  # 水平对齐方式(右对齐)
            va='top',    # 垂直对齐方式(顶部对齐)
            bbox=dict(   # 文本背景框设置
                boxstyle='round',  # 圆角矩形
                facecolor='white', # 白色填充
                alpha=0.8          # 80%透明度
            )
        )
        
        plt.tight_layout()  # 自动调整元素间距，避免重叠
        print(f"{actual_time}s:successful")
        
        return fig, f, spectrum  # 返回图表对象、频率数组和频谱数组
        
    except Exception as e:
        # 捕获并处理任何异常，提高程序健壮性
        print(f"error: {str(e)}")
        raise  # 重新抛出异常，便于调试

# === 主程序入口 ===
if __name__ == "__main__":
    # 定义感兴趣的时间点（单位：秒）
    target_time = 2.3  # 例如：分析第2.3秒的频谱
    
    # 生成频谱图：调用核心函数
    fig, freq, spectrum = generate_single_spectrum(
        r'D:\CUDA\ceshi.wav',  # 音频文件路径
        target_time=target_time,  # 目标时间点
        nperseg=512,       # FFT窗口长度
        noverlap=256,      # FFT窗口重叠点数
        dpi=150            # 图像分辨率
    )
    
    # 保存频谱图：将图表输出为图像文件
    output_img = r'D:\CUDA\spectrum_at_time.png'  # 输出路径
    fig.savefig(output_img, bbox_inches='tight')  # 紧凑布局保存
    plt.close(fig)  # 关闭图表，释放内存
    print(f"saved to: {output_img}")
    
    # === 可选频谱分析示例 ===
    
    # 1. 找主峰频率（最高幅度对应的频率）
    peak_freq_idx = np.argmax(spectrum)  # 找到最大幅度对应的索引
    peak_freq = freq[peak_freq_idx]  # 从频率数组获取对应频率
    print(f"f: {peak_freq:.1f} Hz")
    
    # 2. 分析特定频率范围的频谱能量（例如人声范围）
    vocal_range = (85, 255)  # 人声主要频率范围(男声基频)
    # 筛选出指定频率范围内的频谱点
    in_range = spectrum[(freq >= vocal_range[0]) & (freq <= vocal_range[1])]
    vocal_energy = np.mean(in_range)  # 计算平均值作为能量指标
    print(f"pingjunenergy: {vocal_energy:.4f}")
    
    # 3. 能量比例计算（例如高音部分占总能量比例）
    total_energy = np.sum(spectrum)  # 总能量
    high_freq_range = (2000, sample_rate/2)  # 高音频率范围(2kHz以上)
    # 筛选高音区频谱点
    high_freq_energy = np.sum(spectrum[(freq >= high_freq_range[0])])
    high_freq_ratio = high_freq_energy / total_energy * 100  # 百分比
    print(f"gaoyinzhanbi: {high_freq_ratio:.1f}%")