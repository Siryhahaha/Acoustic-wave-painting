# -*- coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import soundfile as sf

# 音频参数配置（自动适配输入文件）
def process_audio_file(input_path, output_path):
    # 读取输入文件
    input_data, fs = sf.read(input_path, dtype='float32')
    if input_data.ndim > 1:
        input_data = input_data[:, 0]  # 转换为单声道
    
    # 参数适配
    FS = fs
    CARRIER_FREQ = 1000  # 载波频率（可根据需要调整）
    BITRATE = 100        # 码元速率（可根据需要调整）
    
    # 生成测试比特流（实际使用时应替换为真实数据）
    tx_bits = np.random.randint(0, 2, int(len(input_data)/FS * BITRATE))
    
    # 初始化变量
    rx_bits = []
    prev_phase = 0
    
    # 带通滤波器设计（保留载波频带）
    def design_bandpass_filter():
        nyq = 0.5 * FS
        low = (CARRIER_FREQ - 500) / nyq
        high = (CARRIER_FREQ + 500) / nyq
        return signal.ellip(4, 0.5, 40, [low, high], 
                           btype='bandpass', analog=False)
    
    # 低通滤波器设计
    def design_lowpass_filter():
        nyq = 0.5 * FS
        cutoff = 1000 / nyq  # 截止频率1kHz
        return signal.ellip(4, 0.5, 40, cutoff, 
                           btype='lowpass', analog=False)
    
    # BPSK调制器（文件版）
    def bpsk_modulate(bit, t):
        phase_shift = np.pi if bit == 0 else 0
        return np.cos(2*np.pi*CARRIER_FREQ*t + phase_shift) * 0.5
    
    # BPSK解调器（文件版）
    def bpsk_demodulate(input_signal):
        nonlocal prev_phase
        # 带通滤波
        filtered = signal.filtfilt(*design_bandpass_filter(),input_signal)
        # 相干解调
        t = np.arange(len(filtered))/FS
        demod = filtered * np.cos(2*np.pi*CARRIER_FREQ*t + prev_phase)
        # 低通滤波
        demod = signal.filtfilt(*design_lowpass_filter(), demod)
        # 积分判决
        energy = np.sum(demod**2)
        bit = 1 if energy > 0.1 else 0
        prev_phase = np.angle(np.mean(np.exp(1j*(2*np.pi*CARRIER_FREQ*t + 
                              np.angle(demod))))) % (2*np.pi)
        return bit
    
    # 调制过程
    modulated = np.zeros_like(input_data)
    t_total = np.arange(len(input_data))/FS
    bit_index = 0
    
    for i in range(len(tx_bits)):
        start = int(i * FS/BITRATE)
        end = int((i+1) * FS/BITRATE)
        if start >= len(t_total):
            break
        t = t_total[start:end]
        modulated[start:end] = bpsk_modulate(tx_bits[i], t)
    
    # 添加噪声（可选）
    # modulated += np.random.normal(0, 0.1, len(modulated))
    
    # 解调过程
    for i in range(0, len(modulated), int(FS/BITRATE)):
        chunk = modulated[i:i+int(FS/BITRATE)]
        if len(chunk) < int(FS/BITRATE):
            continue
        rx_bit = bpsk_demodulate(chunk)
        rx_bits.append(rx_bit)
    
    # 计算误码率
    errors = np.sum(tx_bits[:len(rx_bits)] != rx_bits)
    print(f"处理完成，误码率: {errors/len(tx_bits):.2%} (处理了{len(rx_bits)}/{len(tx_bits)}比特)")
    
    # 保存输出文件
    sf.write(output_path, modulated, FS)
    print(f"输出文件已保存至：{output_path}")

# 主程序
if __name__ == "__main__":
    # 使用示例
    input_file = "input_audio.wav"  # 输入文件路径
    output_file = "output_audio.wav" # 输出文件路径
    
    # 生成测试音频（可选）
    # generate_test_audio()
    
    process_audio_file(input_file, output_file)
    
    # 可视化结果（可选）
    plt.figure(figsize=(12, 8))
    
    # 绘制原始信号
    plt.subplot(3, 1, 1)
    data, fs = sf.read(input_file)
    plt.plot(data[:int(fs*0.1)])  # 显示前0.1秒
    plt.title("原始音频信号")
    
    # 绘制调制后信号
    plt.subplot(3, 1, 2)
    mod_data, _ = sf.read(output_file)
    plt.plot(mod_data[:int(fs*0.1)])
    plt.title("BPSK调制后信号")
    
    # 绘制频谱对比
    plt.subplot(3, 1, 3)
    f, t, Sxx = plt.specgram(data[:int(fs*1)], Fs=fs, NFFT=1024, noverlap=512)
    plt.title("原始信号频谱")
    
    plt.tight_layout()
    plt.show()