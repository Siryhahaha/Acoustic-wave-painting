import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, filtfilt

def am_demodulate(input_bin, output_wav):
    """
    AM解调器（带同步检测和去加重处理）
    参数：
        input_bin: 输入二进制文件路径
        output_wav: 输出WAV文件路径
    """
    # 读取二进制文件
    with open(input_bin, 'rb') as f:
        fs = np.frombuffer(f.read(4), dtype='<i4')[0]  # 读取采样率
        fc = np.frombuffer(f.read(4), dtype='<i4')[0]  # 读取载波频率
        modulated = np.fromfile(f, dtype=np.float32)   # 读取调制信号
    
    # 生成同步载波
    t = np.arange(len(modulated)) / fs
    carrier = np.sin(2 * np.pi * fc * t)
    
    # 同步解调
    mixed = modulated * carrier
    
    # 设计10阶切比雪夫低通滤波器
    def cheby_lowpass(cutoff, fs, order=10, ripple=1):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low')
        return b, a
    
    # 自动选择安全截止频率
    cutoff = min(8000, fs//2 - 1000)
    b, a = cheby_lowpass(cutoff, fs)
    
    # 零相位滤波
    demodulated = filtfilt(b, a, mixed)
    
    # 去加重处理
    de_emphasis = 0.97
    processed = np.append(demodulated[0], demodulated[1:] - de_emphasis * demodulated[:-1])
    
    # 统计归一化
    processed = (processed - np.mean(processed)) / np.std(processed)
    processed = np.clip(processed, -1.0, 1.0)
    
    # 保存结果
    wavfile.write(output_wav, fs, (processed * 32767).astype(np.int16))

if __name__ == "__main__":
    # 使用示例
    am_demodulate('modulated.bin', 'output.wav')