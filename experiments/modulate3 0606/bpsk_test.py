import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import soundfile as sf  # 用于处理音频文件
import os
import time
from tqdm import tqdm  # 进度条支持
from scipy.io import wavfile as wav


# 配置音频处理参数
class AudioConfig:
    def __init__(self, target_sample_rate=16000, noise_level=0.2, fft_size=1024):
        """
        音频处理配置
        :param target_sample_rate: 目标采样率(Hz)
        :param noise_level: 噪声级别(0-1)
        :param fft_size: FFT处理窗口大小
        """
        self.target_sample_rate = target_sample_rate
        self.noise_level = noise_level
        self.fft_size = fft_size
        self.noise_reduction_db = 15  # 降噪幅度(dB)


def add_audio_noise(audio_data, noise_level):
    """
    添加可控级别的噪声到音频信号
    :param audio_data: 原始音频数据(归一化到[-1,1])
    :param noise_level: 噪声级别(0-1)
    :return: 带噪音频
    """
    # 计算原始信号功率
    signal_power = np.mean(audio_data ** 2)

    # 生成具有相同功率的噪声
    noise = np.random.normal(0, np.sqrt(signal_power), len(audio_data))

    # 按噪声级别混合
    noisy_audio = (1 - noise_level) * audio_data + noise_level * noise

    # 归一化防止削波
    max_amp = np.max(np.abs(noisy_audio))
    if max_amp > 1.0:
        noisy_audio /= max_amp * 1.05

    return noisy_audio


def spectral_subtraction(audio_data, sr, config):
    """
    使用谱减法进行降噪
    :param audio_data: 带噪音频数据(归一化到[-1,1])
    :param sr: 采样率
    :param config: 音频配置
    :return: 去噪后的音频
    """
    # 计算功率谱
    frames = len(audio_data) // config.fft_size
    window = np.hanning(config.fft_size)

    # 估计噪声谱
    noise_profile = np.zeros(config.fft_size // 2 + 1)
    n_samples = min(10, frames)  # 使用前10帧估计噪声
    for i in range(n_samples):
        start = i * config.fft_size
        end = start + config.fft_size
        segment = audio_data[start:end] * window
        noise_profile += np.abs(np.fft.rfft(segment)) ** 2
    noise_profile /= n_samples

    # 谱减处理
    enhanced = np.zeros_like(audio_data)
    for i in range(frames):
        start = i * config.fft_size
        end = start + config.fft_size
        segment = audio_data[start:end] * window

        # 计算幅度谱
        spectrum = np.fft.rfft(segment)
        magnitude = np.abs(spectrum)
        phase = np.angle(spectrum)

        # 谱减法
        noise_reduction = np.maximum(magnitude ** 2 - noise_profile, 0)
        noise_reduction = np.sqrt(noise_reduction)

        # 重建信号
        reconstructed_spectrum = noise_reduction * np.exp(1j * phase)
        reconstructed_frame = np.fft.irfft(reconstructed_spectrum)

        # 交叠相加
        enhanced[start:end] += reconstructed_frame * window

    # 归一化
    max_amp = np.max(np.abs(enhanced))
    if max_amp > 1e-6:  # 防止除零
        enhanced /= max_amp * 1.05

    return enhanced


def bin_to_noisy_audio(input_bin_path, output_bin_path, config):
    """
    二进制文件转带噪音频文件
    :param input_bin_path: 原始二进制音频文件路径
    :param output_bin_path: 输出带噪音频文件路径
    :param config: 音频配置
    :return: 带噪音频数据
    """
    # 读取二进制文件
    with open(input_bin_path, 'rb') as f:
        audio_data = np.frombuffer(f.read(), dtype=np.float32)

    print(f"添加噪声 (级别: {config.noise_level})...")
    noisy_audio = add_audio_noise(audio_data, config.noise_level)

    # 保存带噪音频
    with open(output_bin_path, 'wb') as f:
        noisy_audio.astype(np.float32).tofile(f)

    print(f"带噪音频已保存: {output_bin_path}")
    return noisy_audio


def noisy_audio_to_denoised(input_bin_path, output_bin_path, orig_data, config):
    """
    带噪音频转去噪音频
    :param input_bin_path: 带噪音频二进制文件路径
    :param output_bin_path: 输出去噪音频文件路径
    :param orig_data: 原始音频数据(用于对比)
    :param config: 音频配置
    :return: 去噪音频数据
    """
    # 读取带噪音频
    with open(input_bin_path, 'rb') as f:
        noisy_audio = np.frombuffer(f.read(), dtype=np.float32)

    # 模拟采样率(实际应用中应使用真实采样率)
    sr = config.target_sample_rate

    print(f"降噪处理 (强度: {config.noise_reduction_db}dB)...")
    # 处理过程显示进度条
    denoised_audio = spectral_subtraction(noisy_audio, sr, config)

    # 保存去噪音频
    with open(output_bin_path, 'wb') as f:
        denoised_audio.astype(np.float32).tofile(f)

    print(f"去噪音频已保存: {output_bin_path}")
    return denoised_audio


def plot_audio_process(orig_data, noisy_data, denoised_data, config, max_duration=0.03):
    """
    可视化音频处理全过程
    :param orig_data: 原始音频数据
    :param noisy_data: 带噪音频数据
    :param denoised_data: 去噪音频数据
    :param config: 音频配置
    :param max_duration: 最大显示时长(秒)
    """
    # 计算采样率和时间轴
    sr = config.target_sample_rate
    n_samples = int(max_duration * sr)

    # 截取部分数据用于绘图
    orig_segment = orig_data[:n_samples]
    noisy_segment = noisy_data[:n_samples]
    denoised_segment = denoised_data[:n_samples]
    t = np.arange(n_samples) / sr

    # 创建图表
    plt.figure(figsize=(12, 15))

    # 1. 原始音频
    plt.subplot(3, 1, 1)
    plt.plot(t, orig_segment)
    plt.title(f'原始音频 (前{max_duration * 1000:.0f}ms)')
    plt.grid(True)

    # 2. 带噪音频
    plt.subplot(3, 1, 2)
    plt.plot(t, noisy_segment, 'r')
    plt.title(f'带噪音频 (噪声级别: {config.noise_level})')
    plt.grid(True)

    # 3. 去噪音频
    plt.subplot(3, 1, 3)
    plt.plot(t, denoised_segment, 'g')
    plt.title(f'去噪音频 (降噪幅度: {config.noise_reduction_db}dB)')
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('audio_process.png', dpi=150)
    plt.show()
    print(f"可视化完成，结果保存为: audio_process.png")

    # 频谱分析
    plot_audio_spectrum(orig_segment, noisy_segment, denoised_segment, sr)


def plot_audio_spectrum(orig_data, noisy_data, denoised_data, sr):
    """
    绘制音频频谱图
    :param orig_data: 原始音频数据
    :param noisy_data: 带噪音频数据
    :param denoised_data: 去噪音频数据
    :param sr: 采样率
    """
    # 计算频谱
    f_orig, Pxx_orig = signal.welch(orig_data, sr, nperseg=1024)
    f_noisy, Pxx_noisy = signal.welch(noisy_data, sr, nperseg=1024)
    f_denoised, Pxx_denoised = signal.welch(denoised_data, sr, nperseg=1024)

    # 创建图表
    plt.figure(figsize=(12, 8))

    # 频谱对比
    plt.semilogy(f_orig, Pxx_orig, label='原始音频')
    plt.semilogy(f_noisy, Pxx_noisy, 'r', label='带噪音频')
    plt.semilogy(f_denoised, Pxx_denoised, 'g', label='去噪音频')

    plt.title('音频频谱分析')
    plt.xlabel('频率 [Hz]')
    plt.ylabel('功率谱密度 [dB/Hz]')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('audio_spectrum.png', dpi=150)
    plt.show()
    print(f"频谱分析完成，结果保存为: audio_spectrum.png")


# 主处理函数
def process_audio_pipeline(input_bin_path, config):
    """
    音频处理完整流程
    :param input_bin_path: 输入二进制音频文件路径
    :param config: 音频配置
    """
    # 生成输出路径
    base_name = os.path.splitext(os.path.basename(input_bin_path))[0]
    noisy_bin_path = f"{base_name}_noisy.bin"
    denoised_bin_path = f"{base_name}_denoised.bin"

    # 1. 加噪处理
    orig_audio = np.fromfile(input_bin_path, dtype=np.float32)
    noisy_audio = bin_to_noisy_audio(input_bin_path, noisy_bin_path, config)

    # 2. 降噪处理
    denoised_audio = noisy_audio_to_denoised(noisy_bin_path, denoised_bin_path, orig_audio, config)

    # 3. 可视化
    plot_audio_process(orig_audio, noisy_audio, denoised_audio, config)


# 与WAV文件转换的集成函数
def wav_to_bin(wav_path, bin_path):
    """将WAV文件转为二进制文件"""
    # 读取WAV文件
    data, sr = sf.read(wav_path)

    # 处理多声道音频
    if data.ndim > 1:
        data = data[:, 0]  # 取左声道

    # 归一化并转float32
    max_val = np.max(np.abs(data))
    data = data.astype(np.float32) / max_val

    # 保存二进制文件
    with open(bin_path, 'wb') as f:
        data.tofile(f)

    print(f"WAV转BIN完成: {wav_path} -> {bin_path}")
    return data, sr


def bin_to_wav(bin_path, wav_path, target_sample_rate=16000):
    """将二进制文件转为WAV文件"""
    # 读取二进制数据
    with open(bin_path, 'rb') as f:
        data = np.frombuffer(f.read(), dtype=np.float32)

    # 转换为16位PCM格式
    data_int = (data * 32767).astype(np.int16)

    # 保存为WAV文件
    sf.write(wav_path, data_int, target_sample_rate)

    print(f"BIN转WAV完成: {bin_path} -> {wav_path}")


# 使用示例
if __name__ == "__main__":
    # 配置文件参数
    audio_config = AudioConfig(
        target_sample_rate=16000,
        noise_level=0.3,  # 中等噪声级别
        fft_size=1024
    )

    wav_path = r"D:\Study\大二下\信号系统课设\Acoustic-wave-painting\docs\wav示例文件\sample-3s.wav"
    wav2_path = "最终输出音频.wav"
    input_bin = 'original.bin'
    bpsk_bin = 'bpsk_signal.bin'
    output_bin = 'demodulated.bin'

    rate, data = wav.read(wav_path)
    if data.ndim > 1:
        data = data[:, 0]
    data = data.astype(np.float32) / np.max(np.abs(data))
    data.tofile(input_bin)


    # 2. 音频处理
    process_audio_pipeline(input_bin, audio_config)

    # 3. 转换回WAV(可选)
    # bin_to_wav("output_denoised.bin", output_wav)


    audio = np.fromfile(output_bin, dtype=np.float32)
    audio_int = (audio * 32767).astype(np.int16)
    wav.write(wav2_path, 88200, audio_int)