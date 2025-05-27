# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import stft
import warnings

# Ĭ�ϲ�������
input_wav = r'D:\Study\大二下\信号系统课设\Acoustic-wave-painting\Code\频谱图01\input_44k.wav'
output_img = r'D:\Study\大二下\信号系统课设\Acoustic-wave-painting\Code\频谱图01\haha.png'  # ��ΪPNG��ʽ
nperseg = 1024   # ���Ƶ�ʷֱ���
noverlap = 512   # 50%�ص�
cmap = 'plasma'  # ��ɫ����
dpi = 150        # �ϸ߷ֱ���

def generate_spectrogram(input_wav, output_img, nperseg=1024, noverlap=512, cmap='plasma', dpi=150):
    #
    #���ɲ�����Ƶ��ͼ
    #
    #������
   #     input_wav: ������Ƶ·�� (.wav)
    #    output_img: ���ͼ��·�� (֧��png/jpg��)
    #    nperseg: FFT���ڳ��� (Ĭ��1024)
    #    noverlap: �����ص����� (Ĭ��512)
    #    cmap: ��ɫӳ�� (Ĭ��'plasma')
    #    dpi: ����ֱ��� (Ĭ��150)
    #
    try:
        # ����WAV�ļ���С����
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            
            # 1. ��ȡ��Ƶ
            sample_rate, data = wavfile.read(input_wav)
            if data.ndim > 1:  # תΪ������
                data = data.mean(axis=1)
            data = data.astype(np.float32) / np.iinfo(data.dtype).max  # ��һ����[-1,1]

        # 2. ����STFT
        f, t, Zxx = stft(data, 
                         fs=sample_rate, 
                         nperseg=nperseg, 
                         noverlap=noverlap,
                         window='hann')
        spectrogram = 20 * np.log10(np.abs(Zxx) + 1e-9)  # ת�ֱ�

        # 3. ���Ʋ�����
        plt.figure(figsize=(10, 6))
        plt.pcolormesh(t, f, spectrogram, shading='gouraud', cmap=cmap)
        plt.yscale('symlog')  # ����Ƶ����
        plt.ylim(20, sample_rate/2)  # ����ֱ���ͳ���Ƶ
        plt.colorbar(label='Intensity (dB)')
        plt.title('Spectrogram')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.tight_layout()

        # 4. ����ΪPNG��������֧�ֵĸ�ʽ��
        plt.savefig(output_img, dpi=dpi, bbox_inches='tight')
        plt.close()
        print(f"Spectrogram successfully saved to {output_img}")
        
    except Exception as e:
        print(f"Error generating spectrogram: {str(e)}")
        raise

# ���ú���
if __name__ == "__main__":
    generate_spectrogram(input_wav, output_img, nperseg, noverlap, cmap, dpi)