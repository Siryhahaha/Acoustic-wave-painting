from .constants import *

# input_wav = '..\\experiments\\频谱图01 0519\\频谱进阶\\yinpin\\ceshi.wav'
# input_wav = '..\\docs\\wav示例文件\\sample-3s.wav'
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
    except:
        return None

#计算整个音频的最大幅值
def calculate_global_amplitude_max(input_wav, nperseg, noverlap):
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            sample_rate, data = wav.read(input_wav)
            ##########这里改用自己的函数
            if data.ndim > 1:
                data = data.mean(axis=1)
        f, t, Zxx = stft(
            data,
            fs=sample_rate,
            nperseg=nperseg,
            noverlap=noverlap,
            window='hann'
        )
        global_max = np.max(np.abs(Zxx))
        return global_max
    except Exception as e:
        return 5000 #5000一般也够了

def generate_single_spectrum(input_wav, target_time, fps=fps_set, A_max=5000, isylim=isylim):
    #    fig: 包含频谱图的matplotlib图形对象
    #    freq: 频率数组（各频率点）
    #    spectrum: 幅度数组（各频率对应的声音强度）
    try:
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
        time_diffs = np.abs(t - target_time)
        closest_idx = np.argmin(time_diffs)
        spectrum = np.abs(Zxx[:, closest_idx])
        actual_time = t[closest_idx]
        peak_idx = np.argmax(spectrum)
        peak_freq = f[peak_idx]
        peak_amp = spectrum[peak_idx]
        fig = plt.figure(figsize=(10, 7), dpi=dpi)
        fig.subplots_adjust(hspace=5)
        ax = fig.add_subplot(111)
        ax.plot(f, spectrum, color='blue', linewidth=2)
        ax.set_xscale('log')
        ax.set_xlim(20, sample_rate / 2)
        if isylim==0:
            ax.set_ylim(0, A_max * 1.01)
        elif isylim==1 :
            ax.set_ylim(0, np.max(spectrum)*1.1)
        ax.set_xlabel('f (Hz)')
        ax.set_ylabel('A')
        ax.axvline(x=peak_freq, color='red', linestyle='--', alpha=0.7)
        ax.axhline(y=peak_amp, color='red', linestyle='--', alpha=0.7)
        ax.plot(peak_freq, peak_amp, 'ro', markersize=6)
        ax.text(
            0.98, 0.98,
            f't = {actual_time:.3f}s , fps = {fps}, \nmain = {peak_freq:.1f} Hz',
            transform=ax.transAxes,
            ha='right',
            va='top',
            fontsize=10,
            bbox=dict(
                boxstyle='round',
                facecolor='white',
                alpha=0.8
            )
        )

        plt.tight_layout()
        return fig, f, spectrum
    except:
        raise

def generate_spectrogram(input_wav=wavOutput_path, output_png=pngTAF_path):
    nperseg = 1024
    noverlap = 512
    cmap = 'plasma'
    dpi = 150

    sample_rate, data = wav.read(input_wav)
    if data.ndim > 1:  # 转为单声道
        data = data.mean(axis=1)
    data = data.astype(np.float32) / np.max(np.abs(data))
    f, t, Zxx = stft(data,
                     fs=sample_rate,
                     nperseg=nperseg,
                     noverlap=noverlap,
                     window='hann')
    spectrogram = 20 * np.log10(np.abs(Zxx) + 1e-9)
    plt.figure(figsize=(10, 4))
    plt.pcolormesh(t, f, spectrogram, shading='gouraud', cmap=cmap)
    plt.yscale('symlog')  # 对数频率轴
    plt.ylim(20, sample_rate / 2)  # 忽略直流和超高频
    plt.colorbar(label='Intensity (dB)')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.tight_layout()
    plt.savefig(output_png, dpi=dpi, bbox_inches='tight', format='png')
    plt.close()

def get_time_num_imterval(wav_path=wavOutput_path, fps=fps_set):
    duration = get_audio_duration(wav_path)
    if duration is None:
        exit(1)
    #采样间隔
    interval = 1/fps
    #生成的频谱图数量
    num_spectra = int(duration / interval)
    A_max=calculate_global_amplitude_max(wav_path, nperseg, noverlap)
    return duration, num_spectra, interval, A_max

def generate_png(input_wav, duration, interval, i, fps=fps_set, A_max=5000, isylim=isylim):
    target_time = i * interval
    if target_time > duration:
        return
    fig, freq, spectrum = generate_single_spectrum(
        input_wav,
        target_time=target_time,
        fps=fps,
        A_max=A_max,
        isylim=isylim
    )
    fig.suptitle(Path(input_wav).stem, fontsize=20)
    fig.text(0.1, 0.01, "Acoustic-wave-painting  by SY MZH LHJ",
             fontsize=10,
             bbox=dict(facecolor='white', alpha=0.7))
    file_name = f"{i + 1:05d}.png"
    full_path = pngTempDir_path + "\\" + file_name
    plt.savefig(full_path)
    plt.close('all')