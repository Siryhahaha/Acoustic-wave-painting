# -*- coding:utf-8 -*-
import numpy as np
from math import pi
import matplotlib.pyplot as plt
import matplotlib
import scipy.signal as signal

# 参数配置
fc = 44100          # 载波频率44.1kHz
fs = 20 * fc        # 采样率882kHz
symbol_rate = 44100 # 码元率44.1kHz
size = 10           # 码元数量
snr = 5             # 信噪比(dB)

# 时间参数计算
t_symbol = 1 / symbol_rate  # 单个码元持续时间
t_total = size * t_symbol    # 总持续时间
ts = np.arange(0, t_total, 1/fs)  # 时间向量

# 生成随机二进制信号
a = np.random.randint(0, 2, size)

# 构建基带信号（每个码元重复采样）
samples_per_symbol = int(fs * t_symbol)
m = np.repeat(a, samples_per_symbol).astype(float)

# 生成相干载波
t_carrier = np.arange(len(ts)) / fs
coherent_carrier = np.cos(2 * pi * fc * t_carrier)

# BPSK调制
bpsk = np.cos(2 * pi * fc * t_carrier + pi * (m - 1) + pi/4)

# 添加高斯白噪声
def awgn(signal, snr):
    snr = 10 ** (snr / 10.0)
    signal_power = np.mean(signal ** 2)
    noise_power = signal_power / snr
    noise = np.random.randn(len(signal)) * np.sqrt(noise_power)
    return signal + noise

noise_bpsk = awgn(bpsk, snr=10)

# 带通滤波器设计（通带44.1kHz±2kHz）
bandwidth = 2000 
nyq = 0.5 * fs
low = (fc - bandwidth/2) / nyq
high = (fc + bandwidth/2) / nyq
[b_bandpass, a_bandpass] = signal.ellip(
    5, 0.5, 60, [low, high],
    btype='bandpass', analog=False, output='ba'
)

# 低通滤波器设计（截止频率2kHz）
cutoff = 2000 / nyq
[b_lowpass, a_lowpass] = signal.ellip(
    5, 0.5, 60, cutoff,
    btype='lowpass', analog=False, output='ba'
)

# 解调流程
bandpass_out = signal.filtfilt(b_bandpass, a_bandpass, noise_bpsk)
# 添加载波相位同步（示例）：
phase_offset = np.angle(np.sum(bandpass_out * coherent_carrier))
corrected_carrier = np.cos(2 * np.pi * fc * t_carrier + phase_offset)
coherent_demod = bandpass_out * corrected_carrier
lowpass_out = signal.filtfilt(b_lowpass, a_lowpass, coherent_demod)

# 抽样判决
flag = np.zeros(size)
for i in range(size):
    start = i * samples_per_symbol
    end = start + samples_per_symbol
    avg = np.mean(lowpass_out[start:end]) - 0.5
    flag[i] = 1 if avg > 0 else 0

# 计算误码率
error_count = np.sum(a != flag)
ber = error_count / size
print(f"误码率（失真率）: {ber*100:.2f}%")

# 可视化设置
plt.figure(figsize=(12, 8))
zhfont = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')

# 原始信号
plt.subplot(4, 1, 1)
plt.title('原始二进制信号 (44.1kHz码元率)', fontproperties=zhfont, fontsize=12)
plt.plot(ts, m, 'b')
plt.ylim(-0.5, 1.5)

# 调制信号
plt.subplot(4, 1, 2)
plt.title('BPSK调制信号 (44.1kHz载波)', fontproperties=zhfont, fontsize=12)
plt.plot(ts, bpsk, 'r')
plt.ylim(-1.5, 1.5)

# 噪声信号
plt.subplot(4, 1, 3)
plt.title('叠加高斯白噪声后的信号 (SNR=5dB)', fontproperties=zhfont, fontsize=12)
plt.plot(ts, noise_bpsk, 'g')
plt.ylim(-1.5, 1.5)

# 解调信号
plt.subplot(4, 1, 4)
plt.title('解调恢复信号', fontproperties=zhfont, fontsize=12)
plt.plot(ts, np.repeat(flag, samples_per_symbol), 'm')
plt.ylim(-0.5, 1.5)

plt.tight_layout()
plt.show()