import numpy as np
from scipy.io import wavfile

def am_modulate(input_wav, output_wav, fc=18000.0):
    """
    适配44.1kHz采样率的AM调制器
    参数：
        input_wav: 输入WAV文件路径
        output_wav: 输出WAV文件路径
        fc: 载波频率（默认18kHz）
    """
    # 读取音频
    fs, data = wavfile.read(input_wav)
    
    # 参数校验
    if fs != 44100:
        raise ValueError("本版本仅支持44.1kHz采样率")
    if fc >= fs/2:
        raise ValueError(f"载波频率需< {fs/2/1000}kHz")
    
    # 转换为单声道并预加重
    if data.ndim > 1:
        data = data.mean(axis=1)
    pre_emphasis = 0.95  # 调整预加重系数
    data = np.append(data[0], data[1:] - pre_emphasis * data[:-1])
    
    # 归一化到[-1,1]
    data = data.astype(np.float32)
    data /= np.max(np.abs(data))
    
    # DSB调制
    t = np.arange(len(data)) / fs
    carrier = np.sin(2 * np.pi * fc * t)
    modulated = data * carrier  # 直接调制不添加直流偏置
    
    # 保存为32位WAV文件
    wavfile.write(output_wav, fs, modulated.astype(np.float32))
    
    # 保存元数据
    with open(f"{output_wav}.meta", 'w') as f:
        f.write(f"fs={fs}\nfc={fc}")

if __name__ == "__main__":
    am_modulate('input_44k.wav', 'modulated_44k.wav')