# -*- coding:utf-8 -*-
import numpy as np
from math import pi
import matplotlib.pyplot as plt
import matplotlib
import scipy.signal as signal
import math
 
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