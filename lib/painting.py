from .constants import *

# input_wav = '..\\experiments\\频谱图01 0519\\频谱进阶\\yinpin\\ceshi.wav'
# input_wav = '..\\docs\\wav示例文件\\sample-3s.wav'  # 默认音频文件路径
# input_wav = wavInput_path
nperseg = 1024
noverlap = 512
dpi = 150

def get_audio_duration(input_wav):
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            sample_rate, data = wav.read(input_wav)
            if data.ndim > 1:
                data = data.mean(axis=1)
            return len(data) / float(sample_rate)
    except Exception as e:
        print(f"error: {str(e)}")
        return None


# 计算整个音频的最大幅值（增强兼容性）
def calculate_global_amplitude_max(input_wav, nperseg, noverlap):
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            sample_rate, data = wav.read(input_wav)
            # 处理多声道
            if data.ndim > 1:
                data = data.mean(axis=1)
                # 执行STFT
        f, t, Zxx = stft(
            data,
            fs=sample_rate,
            nperseg=nperseg,
            noverlap=noverlap,
            window='hann'
        )
        # 计算整个频谱的最大幅值
        global_max = np.max(np.abs(Zxx))
        print(f"音频最大幅值: {global_max:.4f}")
        return global_max
    except Exception as e:
        print(f"计算全局幅值时出错: {str(e)}")
        return 1.0  # 返回安全的默认值

def generate_single_spectrum(input_wav, target_time, nperseg=1024, noverlap=512, dpi=150, fps=fps_set):
    # 核心功能：分析音频在指定时间点的频谱特征
    #    fig: 包含频谱图的matplotlib图形对象
    #    freq: 频率数组（各频率点）
    #    spectrum: 幅度数组（各频率对应的声音强度）

    try:
        # === 1. 音频读取与预处理 ===
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            sample_rate, data = wav.read(input_wav)
            if data.ndim > 1:
                data = data.mean(axis=1)
            data = data.astype(np.float32)
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
        fig = plt.figure(figsize=(10, 7), dpi=dpi)  # 增加高度到7英寸
        fig.subplots_adjust(hspace=5)
        ax = fig.add_subplot(111)
        ax.plot(f, spectrum, color='blue', linewidth=2)
        ax.set_xscale('log')
        ax.set_xlim(20, sample_rate / 2)
        ax.set_ylim(0, calculate_global_amplitude_max(input_wav, nperseg, noverlap) * 1.1)
        ax.set_xlabel('f (Hz)')
        ax.set_ylabel('A')
        # ax.grid(True, which='both', linestyle='--', alpha=0.7)
        ax.text(
            0.98, 0.98,
            f't = {actual_time:.3f}s , fps = {fps}',
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
        return fig, f, spectrum
    except Exception as e:
        print(f"error: {str(e)}")
        raise

#这里写一个函数，得到总数和采样间隔
#这里写一个函数，输入数字得到对应时间的图片
def get_time_num_imterval(wav_path=wavOutput_path, fps=fps_set):
    duration = get_audio_duration(wav_path)
    if duration is None:
        print("error")
        exit(1)
    print(f"total length: {duration:.2f} s")
    # 设置采样间隔
    interval = 1/fps
    # 计算需要生成的频谱图数量
    num_spectra = int(duration / interval)
    return duration, num_spectra, interval

def generate_png(input_wav, duration, interval, i, fps=fps_set):
    # 循环生成频谱图
    # for i in range(num_spectra + 1):
    target_time = i * interval
    # 避免超出音频时长
    if target_time > duration:
        return
        # 生成频谱图
    fig, freq, spectrum = generate_single_spectrum(
        input_wav,
        target_time=target_time,
        nperseg=nperseg,
        noverlap=noverlap,
        dpi=dpi,
        fps=fps
    )
    # 设置图表标题
    fig.suptitle(Path(input_wav).stem, fontsize=20)
    fig.text(0.8, 0.01, "Acoustic-wave-painting  by SY MZH LHJ",
             ha='center', fontsize=10,
             bbox=dict(facecolor='white', alpha=0.7))
    file_name = f"{i + 1:05d}.png"
    full_path = pngTempDir_path + "\\" + file_name
    plt.savefig(full_path)
    plt.close('all')
        # print(f"已保存: {output_img}")
    # print(f"all {num_spectra} ")