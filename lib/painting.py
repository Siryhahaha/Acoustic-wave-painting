
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import stft
import warnings
import os
from .constants import *

input_wav = '..\\experiments\\频谱图01 0519\\频谱进阶\\yinpin\\ceshi.wav'
# input_wav = '..\\docs\\wav示例文件\\sample-3s.wav'  # 默认音频文件路径
nperseg = 1024
noverlap = 512
dpi = 150

def get_audio_duration(input_wav):
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            sample_rate, data = wavfile.read(input_wav)
            if data.ndim > 1:
                data = data.mean(axis=1)
            return len(data) / float(sample_rate)
    except Exception as e:
        print(f"error: {str(e)}")
        return None


def generate_single_spectrum(input_wav, target_time, nperseg=1024, noverlap=512, dpi=150):
    # 核心功能：分析音频在指定时间点的频谱特征
    #    fig: 包含频谱图的matplotlib图形对象
    #    freq: 频率数组（各频率点）
    #    spectrum: 幅度数组（各频率对应的声音强度）

    try:
        # === 1. 音频读取与预处理 ===
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            sample_rate, data = wavfile.read(input_wav)
            if data.ndim > 1:
                data = data.mean(axis=1)
        f, t, Zxx = stft(
            data,
            fs=sample_rate,
            nperseg=nperseg,
            noverlap=noverlap,
            window='hann'
        )
        # === 3. 定位目标时间点 ===
        time_diffs = np.abs(t - target_time)
        closest_idx = np.argmin(time_diffs)
        spectrum = np.abs(Zxx[:, closest_idx])
        actual_time = t[closest_idx]
        print(f"target: {target_time}s , actual: {actual_time:.3f}s")
        # === 4. 创建频谱图表 ===
        fig = plt.figure(figsize=(10, 6), dpi=dpi)
        ax = fig.add_subplot(111)
        ax.plot(f, spectrum, color='blue', linewidth=2)
        ax.set_xscale('log')
        ax.set_xlim(20, sample_rate / 2)
        # ax.set_ylim(0, np.max(spectrum) * 1.1)
        ax.set_ylim(0, 5000)
        ax.set_xlabel('f (Hz)')
        ax.set_ylabel('A')
        # ax.grid(True, which='both', linestyle='--', alpha=0.7)
        ax.text(
            0.98, 0.98,
            f't = {actual_time:.3f}s',
            transform=ax.transAxes,
            ha='right',
            va='top',
            bbox=dict(
                boxstyle='round',
                facecolor='white',
                alpha=0.8
            )
        )

        plt.tight_layout()
        print(f"{actual_time}s:successful")
        return fig, f, spectrum
    except Exception as e:
        print(f"error: {str(e)}")
        raise


# # 获取音频总时长
# duration = get_audio_duration(input_wav)
# if duration is None:
#     print("error")
#     exit(1)
# print(f"total length: {duration:.2f} s")
# # 设置采样间隔
# interval = 0.033333
# # 计算需要生成的频谱图数量
# num_spectra = int(duration / interval)
# # 循环生成频谱图
# for i in range(num_spectra + 1):
#     target_time = i * interval
#     # 避免超出音频时长
#     if target_time > duration:
#         break
#         # 生成频谱图
#     fig, freq, spectrum = generate_single_spectrum(
#         input_wav,
#         target_time=target_time,
#         nperseg=nperseg,
#         noverlap=noverlap,
#         dpi=dpi
#     )
#     # 设置图表标题
#     fig.suptitle(f"t: {target_time:.2f}s  (total_t: {duration:.2f}s)", fontsize=12)
#     # plt.show()
#     # plt.close(fig)
#     # output_img = f'tupian/spectrum_{i:03d}_{target_time:.1f}s.png'
#     file_name = f"{i + 1:05d}.png"  # 格式化为5位数字，不足前面补零
#     full_path = pngTempDir_path + "\\" + file_name
#     plt.savefig(full_path)
#     # print(f"已保存: {output_img}")
# print(f"all {num_spectra} ")