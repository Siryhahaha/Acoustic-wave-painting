# -*- coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import soundfile as sf

# 公共参数配置
FS = 44100        # 采样率
CARRIER_FREQ = 5000  # 载波频率
BITRATE = 100      # 码元速率
NOISE_SNR = 15     # 信噪比(dB)
DURATION = 2.0     # 信号时长(秒)

# 自定义AWGN函数
def awgn(signal, snr_db):
    signal_power = np.mean(np.abs(signal) ** 2)
    snr = 10 ** (snr_db / 10.0)
    noise_power = signal_power / snr
    noise = np.random.normal(0, np.sqrt(noise_power), signal.shape)
    return signal + noise

# 生成不同类型基带信号（改进版）
def generate_baseband(signal_type='sine', duration=DURATION, fs=FS):
    t = np.linspace(0, duration, int(fs*duration), endpoint=False)
    total_bits = int(len(t) * BITRATE / fs)
    samples_per_bit = int(fs / BITRATE)
    
    # 生成不同波形类型的基带信号
    if signal_type == 'sine':
        # 10Hz正弦波（便于观察）
        return 0.5 * np.sin(2 * np.pi * 10 * t), t
    elif signal_type == 'square':
        # 5Hz方波
        return 0.5 * signal.square(2 * np.pi * 5 * t), t
    elif signal_type == 'triangle':
        # 2Hz三角波
        return 0.5 * signal.sawtooth(2 * np.pi * 2 * t, 0.5), t
    elif signal_type == 'noise':
        # 高斯白噪声
        return 0.5 * np.random.randn(len(t)), t
    else:  # 默认生成比特流调制信号
        bits = np.random.randint(0, 2, total_bits)
        baseband = np.zeros(len(t))
        for i in range(total_bits):
            start = i * samples_per_bit
            end = start + samples_per_bit
            phase = 0 if bits[i] else np.pi
            baseband[start:end] = 0.5 * np.sin(2 * np.pi * BITRATE * (t[start:end]-t[start]) + phase)
        return baseband, t

# BPSK调制器
def bpsk_modulate(baseband, fc=CARRIER_FREQ, fs=FS):
    t = np.arange(len(baseband))/fs
    phase_shift = np.pi * (baseband < 0)  # 负值对应π相位偏移
    return np.cos(2 * np.pi * fc * t + phase_shift)

# BPSK解调器
def bpsk_demodulate(modulated, fc=CARRIER_FREQ, fs=FS):
    # 带通滤波
    nyq = 0.5 * fs
    low, high = (fc-1000)/nyq, (fc+1000)/nyq
    b, a = signal.ellip(5, 0.5, 60, [low, high], 'bandpass')
    filtered = signal.filtfilt(b, a, modulated)
    
    # 相干解调
    t = np.arange(len(filtered))/fs
    demod = filtered * np.cos(2 * np.pi * fc * t)
    
    # 低通滤波
    b_lp, a_lp = signal.ellip(5, 0.5, 60, 2000/nyq, 'lowpass')
    lp_out = signal.filtfilt(b_lp, a_lp, demod)
    
    # 抽样判决
    samples = int(len(lp_out)/(fs/BITRATE))
    rx_bits = np.zeros(samples)
    for i in range(samples):
        start = i * int(fs/BITRATE)
        end = start + int(fs/BITRATE)
        segment = lp_out[start:end]
        energy = np.sum(segment**2)
        rx_bits[i] = 1 if energy > 0.1 else 0  # 阈值可根据需要调整
    
    return rx_bits, lp_out

# 完整处理流程
def process_signal(signal_type='sine', show_plots=True):
    # 生成基带信号
    baseband, t = generate_baseband(signal_type)
    
    # 调制
    modulated = bpsk_modulate(baseband)
    
    # 添加噪声
    noisy = awgn(modulated, NOISE_SNR)
    
    # 解调
    rx_bits, demod_signal = bpsk_demodulate(noisy)
    
    # 可视化
    if show_plots:
        plt.figure(figsize=(15, 12))
        
        # 基带信号
        plt.subplot(4,1,1)
        plt.plot(t[:2*FS], baseband[:2*FS])  # 显示前2秒
        plt.title(f'{signal_type.capitalize()} Baseband Signal')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.grid(True)
        
        # 调制信号
        plt.subplot(4,1,2)
        plt.plot(t[:2*FS], modulated[:2*FS])
        plt.title('BPSK Modulated Signal (Carrier Frequency: 5kHz)')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.grid(True)
        
        # 解调后信号（低通输出）
        plt.subplot(4,1,3)
        plt.plot(t[:2*FS], demod_signal[:2*FS])
        plt.title('Demodulated Signal (After Low-Pass Filter)')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.grid(True)
        
        # 抽样判决结果
        plt.subplot(4,1,4)
        plt.stem(rx_bits[:50], linefmt='C3-', markerfmt='C3o', basefmt=' ', 
                label='Received Bits')
        plt.title('Sampled and Decided Bits (First 50 Samples)')
        plt.xlabel('Bit Index')
        plt.ylabel('Value')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        plt.show()
    
    return rx_bits

# 测试不同信号类型
if __name__ == "__main__":
    signal_types = ['sine', 'square', 'triangle', 'noise']
    
    for st in signal_types:
        print(f"\nProcessing {st.capitalize()} signal...")
        try:
            process_signal(st)
            print(f"Completed processing {st.capitalize()} signal")
        except Exception as e:
            print(f"Error processing {st}: {str(e)}")