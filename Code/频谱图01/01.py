import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import stft

input_wav = 'input_44k.wav',
output_bmp = 'spectrogram.bmp',
nperseg = 1024,  # 提高频率分辨率
noverlap = 512,  # 50%重叠
cmap = 'plasma',  # 颜色方案
dpi = 150  # 较高分辨率


def generate_spectrogram(input_wav, output_bmp, nperseg=256, noverlap=128, cmap='viridis', dpi=100):
    # 生成并保存频谱图为 BMP 格式
    # 参数：
    #   input_wav: 输入音频路径 (.wav)
    #   output_bmp: 输出图像路径 (.bmp)
    #  nperseg: FFT窗口长度 (默认256)
    # noverlap: 窗口重叠长度 (默认128)
    # cmap: 颜色映射 (默认'viridis')
    # dpi: 输出分辨率 (默认100)

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
    plt.figure(figsize=(10, 4))
    plt.pcolormesh(t, f, spectrogram, shading='gouraud', cmap=cmap)
    plt.yscale('symlog')  # 对数频率轴
    plt.ylim(20, sample_rate / 2)  # 忽略直流和超高频
    plt.colorbar(label='Intensity (dB)')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.tight_layout()

    # 4. 保存为BMP（或PNG/JPEG）
    plt.savefig(output_bmp, dpi=dpi, bbox_inches='tight', format='bmp')
    plt.close()

if __name__ == "__main__":
    generate_spectrogram('input_44k.wav','spectrogram.bmp')