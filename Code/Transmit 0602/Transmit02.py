import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt

"""
可以导入wav文件了，依旧是写入bin文件中
"""

wavPath="music02.wav"
binPath="S2.bin"

def save_audio(wav_path=wavPath, bin_path=binPath):
    #读取WAV文件并保存为二进制
    rate, data = wav.read(wav_path)#采样率和数据
    if data.ndim > 1:
        data = data[:, 0]
    data.astype(np.float32).tofile(bin_path)
    return rate, data

def load_and_plot(bin_path=binPath, show_samples=1000):
    #加载二进制文件并绘制波形
    audio = np.fromfile(bin_path, dtype=np.float32)
    plt.figure(figsize=(10, 4))
    time = np.arange(show_samples) / sample_rate  # 转换为秒
    plt.plot(time, audio[:show_samples])
    plt.title("S2")
    plt.xlabel("Time(s)")
    plt.ylabel("A")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    sample_rate, audio_data = save_audio()
    load_and_plot(binPath,len(audio_data))
    print("Rate:", sample_rate, "Hz")
    print("Total:", len(audio_data))
    print("Time:", len(audio_data) / sample_rate, "s")