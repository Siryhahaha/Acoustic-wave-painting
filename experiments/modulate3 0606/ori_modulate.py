# -*- coding:utf-8 -*-
import numpy as np
from math import pi
import matplotlib.pyplot as plt
import matplotlib
import scipy.signal as signal
import math

#码元数
size = 10
sampling_t = 0.01
t = np.arange(0, size, sampling_t)

# 随机生成信号序列
a = np.random.randint(0, 2, size)
m = np.zeros(len(t), dtype=np.float32)
for i in range(len(t)):
    m[i] = a[math.floor(t[i])]
fig = plt.figure()
ax1 = fig.add_subplot(3, 1, 1)

# 解决set_title中文乱码
zhfont1 = matplotlib.font_manager.FontProperties(fname = 'C:\Windows\Fonts\simsun.ttc')
ax1.set_title('产生随机n位二进制信号', fontproperties = zhfont1, fontsize = 20)
plt.axis([0, size, -0.5, 1.5])
plt.plot(t, m, 'b')

fc = 4000
fs = 20 * fc # 采样频率
ts = np.arange(0, (100 * size) / fs, 1 / fs)
coherent_carrier = np.cos(np.dot(2 * pi * fc, ts))
bpsk = np.cos(np.dot(2 * pi * fc, ts) + pi * (m - 1) + pi / 4)

# BPSK调制信号波形
ax2 = fig.add_subplot(3, 1, 2)
ax2.set_title('BPSK调制信号', fontproperties=zhfont1, fontsize=20)
plt.axis([0,size,-1.5, 1.5])
plt.plot(t, bpsk, 'r')

# 定义加性高斯白噪声
def awgn(y, snr):
    snr = 10 ** (snr / 10.0)
    xpower = np.sum(y ** 2) / len(y)
    npower = xpower / snr
    return np.random.randn(len(y)) * np.sqrt(npower) + y

# 加AWGN噪声
noise_bpsk = awgn(bpsk, 5)

# BPSK调制信号叠加噪声波形
ax3 = fig.add_subplot(3, 1, 3)
ax3.set_title('BPSK调制信号叠加噪声波形', fontproperties = zhfont1, fontsize = 20) 
plt.axis([0, size, -1.5, 1.5])
plt.plot(t, noise_bpsk, 'r')

# 带通椭圆滤波器设计，通带为[2000，6000]
[b11,a11] = signal.ellip(5, 0.5, 60, [2000 * 2 / 80000, 6000 * 2 / 80000], btype = 'bandpass', analog = False, output = 'ba')
# 低通滤波器设计，通带截止频率为2000Hz
[b12,a12] = signal.ellip(5, 0.5, 60, (2000 * 2 / 80000), btype = 'lowpass', analog = False, output = 'ba')
# 通过带通滤波器滤除带外噪声
bandpass_out = signal.filtfilt(b11, a11, noise_bpsk)
# 相干解调,乘以同频同相的相干载波
coherent_demod = bandpass_out * (coherent_carrier * 2)
# 通过低通滤波器
lowpass_out = signal.filtfilt(b12, a12, coherent_demod)
fig2 = plt.figure()
bx1 = fig2.add_subplot(3, 1, 1)
bx1.set_title('本地载波下变频，经低通滤波器后', fontproperties = zhfont1, fontsize=20)
plt.axis([0, size, -1.5, 1.5])
plt.plot(t, lowpass_out, 'r')

#抽样判决
detection_bpsk = np.zeros(len(t), dtype=np.float32)
flag = np.zeros(size, dtype=np.float32)
for i in range(10):
    tempF = 0
    for j in range(100):
        tempF = tempF + lowpass_out[i * 100 + j]
    if tempF > 0:
        flag[i] = 1
    else:
        flag[i] = 0
for i in range(size):
    if flag[i] == 0:
        for j in range(100):
            detection_bpsk[i * 100 + j] = 0
    else:
        for j in range(100):
            detection_bpsk[i * 100 + j] = 1

bx2 = fig2.add_subplot(3, 1, 2)
bx2.set_title('BPSK信号抽样判决后的信号', fontproperties = zhfont1, fontsize=20)
plt.axis([0, size, -0.5, 1.5])
plt.plot(t, detection_bpsk, 'r')
plt.show()

def bin_to_bpsk(input_path, output_path, snr=5):
    # 1. 读取二进制文件 -> 比特流
    with open(input_path, 'rb') as f:
        data = np.frombuffer(f.read(), dtype=np.uint8)
    bits = np.unpackbits(data)
    
    # 2. 参数设置
    symbol_rate = 1000
    fs = 44100
    fc = 4000
    samples_per_symbol = int(fs / symbol_rate)
    
    # 3. 生成基带信号
    m_file = np.repeat(bits, samples_per_symbol)
    t_file = np.arange(len(m_file)) / fs
    
    # 4. BPSK调制
    carrier = np.cos(2 * np.pi * fc * t_file)
    bpsk_file = np.cos(2 * np.pi * fc * t_file + np.pi * (m_file - 1) + np.pi/4)
    
    # 5. 加噪解调 (复用原流程)
    noise_bpsk = awgn(bpsk_file, snr)
    bandpass_out = signal.filtfilt(b11, a11, noise_bpsk)
    coherent_demod = bandpass_out * (carrier * 2)
    lowpass_out = signal.filtfilt(b12, a12, coherent_demod)
    
    # 6. 抽样判决
    detected_bits = []
    for i in range(len(bits)):
        segment = lowpass_out[i*samples_per_symbol : (i+1)*samples_per_symbol]
        detected_bits.append(1 if np.sum(segment) > 0 else 0)
    
    # 7. 比特流 -> 字节流 -> 写入BIN
    output_bytes = np.packbits(detected_bits)
    with open(output_path, 'wb') as f:
        f.write(output_bytes.tobytes())

# 使用示例
bin_to_bpsk('input.bin', 'output.bin', snr=10)