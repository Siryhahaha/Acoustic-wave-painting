# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import stft
import warnings

# 默认参数设置
input_wav = r'D:\CUDA\123.wav'
output_img = r'D:\CUDA\spectrogram.png'  # 改为PNG格式
nperseg = 1024   # 提高频率分辨率
noverlap = 512   # 50%重叠
cmap = 'plasma'  # 颜色方案
dpi = 150        # 较高分辨率

def generate_spectrogram(input_wav, output_img, nperseg=1024, noverlap=512, cmap='plasma', dpi=150):
    #
    #生成并保存频谱图
    #
    #参数：
   #     input_wav: 输入音频路径 (.wav)
    #    output_img: 输出图像路径 (支持png/jpg等)
    #    nperseg: FFT窗口长度 (默认1024)
    #    noverlap: 窗口重叠长度 (默认512)
    #    cmap: 颜色映射 (默认'plasma')
    #    dpi: 输出分辨率 (默认150)
    #
    try:
        # 忽略WAV文件的小警告
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            
            # 1. 读取音频
            sample_rate, data = wavfile.read(input_wav)
            if data.ndim > 1:  # 转为单声道
                data = data.mean(axis=1)
            data = data.astype(np.float32) / np.iinfo(data.dtype).max  # 归一化到[-1,1]

        # 2. 计算STFT
        f, t, Zxx = stft(data, 
                         fs=sample_rate, 
                         nperseg=nperseg, 
                         noverlap=noverlap,
                         window='hann')
        spectrogram = 20 * np.log10(np.abs(Zxx) + 1e-9)  # 转分贝

        # 3. 绘制并保存
        plt.figure(figsize=(10, 6))
        plt.pcolormesh(t, f, spectrogram, shading='gouraud', cmap=cmap)
        plt.yscale('symlog')  # 对数频率轴
        plt.ylim(20, sample_rate/2)  # 忽略直流和超高频
        plt.colorbar(label='Intensity (dB)')
        plt.title('Spectrogram')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.tight_layout()

        # 4. 保存为PNG（或其他支持的格式）
        plt.savefig(output_img, dpi=dpi, bbox_inches='tight')
        plt.close()
        print(f"Spectrogram successfully saved to {output_img}")
        
    except Exception as e:
        print(f"Error generating spectrogram: {str(e)}")
        raise

# 调用函数
if __name__ == "__main__":
    generate_spectrogram(input_wav, output_img, nperseg, noverlap, cmap, dpi)