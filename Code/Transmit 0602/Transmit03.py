import numpy as np
import scipy.io.wavfile as wav  #这里略微改动了函数
import matplotlib.pyplot as plt
from scipy.signal import stft

"""
本文件植入了🐎的函数,三个函数分别是:
根据wav031生成bin03,根据bin03生成wav032(理论上和wav031是一样的),使用马的代码读取wav032然后生成图片
核心是第二三个函数,我把第一个函数注释了
"""

# 参数配置
wav1Path = "music03_1.wav"
wav2Path = "music03_2.wav"
binPath = "S03.bin"
imgPath = 'P03.png'
#其他没用到的参数删了

def save_audio(wav_path=wav1Path, bin_path=binPath):
    #读取并保存音频数据
    rate, data = wav.read(wav_path)
    if data.ndim > 1:
        data = data[:, 0]
    data = data.astype(np.float32) / np.max(np.abs(data))
    data.tofile(bin_path)
    return rate, data

def load_and_plot(rate, bin_path=binPath):
    #加载二进制文件到wav2
    audio = np.fromfile(bin_path, dtype=np.float32)
    audio_int = (audio * 32767).astype(np.int16)
    wav.write(wav2Path, rate, audio_int)

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
    plt.show()
    plt.savefig(output_png, dpi=dpi, bbox_inches='tight', format='png')
    plt.close()


if __name__ == "__main__":
    sample_rate = 441000
    # sample_rate, audio_data = save_audio()    #本句可注释
    load_and_plot(sample_rate, binPath)
    generate_spectrogram(input_wav=wav2Path,output_png=imgPath)