import numpy as np
import scipy.io.wavfile as wav#这里略微改动了函数
import matplotlib.pyplot as plt
from scipy.signal import stft

# 参数配置
wavPath = "music03.wav"
binPath = "S03.bin"
imgPath = 'P03.png'
spectrogram_params = {
    'nperseg': 1024,
    'noverlap': 512,
    'cmap': 'plasma',
    'dpi': 150
}


def save_audio(wav_path=wavPath, bin_path=binPath):
    """读取并保存音频数据"""
    rate, data = wav.read(wav_path)  # 使用wavfile保持一致性
    if data.ndim > 1:
        data = data[:, 0]
    data = data.astype(np.float32) / np.max(np.abs(data))
    data.tofile(bin_path)
    return rate, data


def generate_spectrogram(input_wav, output_png, nperseg=256, noverlap=128, cmap='viridis', dpi=100):
    """
    生成并保存频谱图为PNG格式

    参数：
        input_wav: 输入音频路径(.wav)
        output_png: 输出图像路径(.png)
        nperseg: FFT窗口长度(默认256)
        noverlap: 窗口重叠长度(默认128)
        cmap: 颜色映射(默认'viridis')
        dpi: 输出分辨率(默认100)
    """
    # 1. 读取音频
    sample_rate, data = wav.read(input_wav)
    if data.ndim > 1:  # 转为单声道
        data = data.mean(axis=1)
    data = data.astype(np.float32) / np.max(np.abs(data))  # 归一化到[-1,1]

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

    # 4. 保存为PNG
    plt.savefig(output_png, dpi=dpi, bbox_inches='tight', format='png')
    plt.close()


if __name__ == "__main__":
    sample_rate, _ = save_audio()
    generate_spectrogram(
        input_wav=wavPath,
        output_png=imgPath,  # 参数名对齐
        nperseg=spectrogram_params['nperseg'],
        noverlap=spectrogram_params['noverlap'],
        cmap=spectrogram_params['cmap'],
        dpi=spectrogram_params['dpi']
    )