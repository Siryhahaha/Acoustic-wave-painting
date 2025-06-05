# -*- coding: utf-8 -*-
# ָ���ļ�����ΪUTF-8��ȷ������·�����������

import numpy as np  # ������ѧ����⣬�����������
import matplotlib.pyplot as plt  # ͼ����ƿ⣬���ڴ���Ƶ��ͼ
from scipy.io import wavfile  # ��SciPy������Ƶ�ļ���ȡ����
from scipy.signal import stft  # ��ʱ����Ҷ�任������Ƶ�׷���
import warnings  # Python���þ���ģ�飬������ܳ��ֵľ�����Ϣ

# === Ĭ�ϲ������� ===
input_wav = r'D:\CUDA\ceshi.wav'  # Ĭ����Ƶ�ļ�·��
nperseg = 1024  # FFT���ڳ��ȣ�������������Ӱ��Ƶ�ʷֱ��ʺ�ʱ��ֱ���
noverlap = 512   # FFT�����ص����ȣ�����������������Ƶ�ױ߽�ЧӦ�����ʱ��������
dpi = 150         # ���ͼ��ֱ��ʣ�ÿӢ�����������ֵԽ��ͼ��Խ����

def generate_single_spectrum(input_wav, target_time, nperseg=1024, noverlap=512, dpi=150):
    
    #���Ĺ��ܣ�������Ƶ��ָ��ʱ����Ƶ������
    
    #����˵��:
    #    input_wav: ������Ƶ�ļ�·��(.wav��ʽ)
    #    target_time: Ŀ��ʱ��㣨��λ���룩  
    #    nperseg: FFT���ڳ��ȣ�Ĭ��1024�㣩
    #    noverlap: �����ص����ȣ�Ĭ��512�㣩
    #    dpi: ���ͼ��ֱ��ʣ�Ĭ��150��
    
    # ����:
    #    fig: ����Ƶ��ͼ��matplotlibͼ�ζ���
    #    freq: Ƶ�����飨��Ƶ�ʵ㣩
    #    spectrum: �������飨��Ƶ�ʶ�Ӧ������ǿ�ȣ�
    
    try:
        # === 1. ��Ƶ��ȡ��Ԥ���� ===
        # ����WAV�ļ���ȡʱ���ܳ��ֵ��޹ؾ���
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")  # �����ض�����
            
            # �Ӵ��̶�ȡ��Ƶ�ļ�
            sample_rate, data = wavfile.read(input_wav)  # ���ز����ʺ�ԭʼ����
            
            # �����������Ƶ��������ת��������
            if data.ndim > 1:  # ����Ƿ�Ϊ������
                data = data.mean(axis=1)  # ��������ȡƽ��ֵתΪ������
            
            # ��Ƶ���ݹ�һ����������ͬλ��ȵ���Ƶͳһ��[-1,1]��Χ
            # ����1: ת��Ϊfloat32���������������ͼ��㾫����ʧ
            # ����2: ��ȡ��Ƶ���ݵ�������ֵ����16λ��Ƶ��32768��
            # ����3: �������ֵ����һ����[-1,1]��Χ
            data = data.astype(np.float32) / np.iinfo(data.dtype).max

        # === 2. ��ʱ����Ҷ�任(STFT)���� ===
        # �ؼ����
        #   STFT����Ƶ�ָ�ɶ��СƬ��(����)����ν��и���Ҷ�任
        #   �����������飺Ƶ�ʵ�(f)��ʱ���(t)������Ƶ��(Zxx)
        f, t, Zxx = stft(
            data,               # Ԥ��������Ƶ����
            fs=sample_rate,     # ��Ƶ������(Hz)
            nperseg=nperseg,    # FFT���ڳ���(����)
            noverlap=noverlap,  # �����ص�����
            window='hann'       # ����������������Ƶ��й©
        )
        
        # === 3. ��λĿ��ʱ��� ===
        # ����ʱ���֮��������Ŀ��ʱ���(target_time)������ʱ���(t)�ľ��Բ�ֵ
        time_diffs = np.abs(t - target_time)  
        
        # �ҵ���ӽ���ʱ������������ز�ֵ��С������λ��
        closest_idx = np.argmin(time_diffs)  
        
        # ��ȡ��Ӧʱ����Ƶ�ף�
        #   Zxx��������ʱ����Ƶ����Ϣ(��״Ϊ[Ƶ�ʵ�����ʱ�����])
        #   Zxx[:, closest_idx]��ʾѡ���closest_idx��ʱ��������Ƶ��
        #   np.abs()ȡ����ֵ��������λ��Ϣ
        spectrum = np.abs(Zxx[:, closest_idx])
        
        # ����ʵ���ҵ���ʱ���(��Ϊʱ��㲻��������������ƫ��)
        actual_time = t[closest_idx]  

        # ��ӡʵ���ҵ���ʱ���
        print(f"target: {target_time}s , actual: {actual_time:.3f}s")
        
        # === 4. ����Ƶ��ͼ�� ===
        fig = plt.figure(figsize=(10, 6), dpi=dpi)  # ����10��6Ӣ��ͼ��
        ax = fig.add_subplot(111)  # ��ӵ�һ��ͼ(1��1�е�1��)
        
        # ����Ƶ�����ߣ�X��ΪƵ��(Hz)��Y��Ϊ����
        ax.plot(f, spectrum, color='blue', linewidth=2)
        
        # ���ö���Ƶ���᣺�������˶���Ƶ�ʵĸ�֪����
        #   �˶��Ե�Ƶ�仯�����У���Ƶ�仯������
        ax.set_xscale('log')  
        
        # ���������᷶Χ��
        #   X��: 20Hz(�˶����ŵ�Ƶ����)�������ʵ�һ��(NyquistƵ��)
        #   Y��: 0��Ƶ�����ֵ��1.1��������10%�Ŀռ�ʹͼ�������
        ax.set_xlim(20, sample_rate/2)  
        ax.set_ylim(0, np.max(spectrum)*1.1)  
        
        # ��ӱ�ǩ�ͱ��⣺�������ı�ʹͼ����׶�
        ax.set_title(f'{actual_time:.3f}s:')  # ��ʾʵ��ʱ���
        ax.set_xlabel('f (Hz)')  
        ax.set_ylabel('A')  
        
        # ��������ߣ�ʹ������׼ȷ��ָ������ͬʱ���������̶Ⱥ�С�̶�λ��
        ax.grid(True, which='both', linestyle='--', alpha=0.7)  
        
        # ���ʱ����ǣ�
        #   ��ͼ�����Ͻ�(98%λ��)��ʾʵ��ʱ���
        #   bbox����������ɫ��͸������������ı��ɶ���
        ax.text(
            0.98, 0.98,  # X��Yλ��(0-1��ʾ����λ��)
            f't = {actual_time:.3f}s',  # ��ʾ�ı�
            transform=ax.transAxes,  # ʹ������ϵ���λ��
            ha='right',  # ˮƽ���뷽ʽ(�Ҷ���)
            va='top',    # ��ֱ���뷽ʽ(��������)
            bbox=dict(   # �ı�����������
                boxstyle='round',  # Բ�Ǿ���
                facecolor='white', # ��ɫ���
                alpha=0.8          # 80%͸����
            )
        )
        
        plt.tight_layout()  # �Զ�����Ԫ�ؼ�࣬�����ص�
        print(f"{actual_time}s:successful")
        
        return fig, f, spectrum  # ����ͼ�����Ƶ�������Ƶ������
        
    except Exception as e:
        # ���񲢴����κ��쳣����߳���׳��
        print(f"error: {str(e)}")
        raise  # �����׳��쳣�����ڵ���

# === ��������� ===
if __name__ == "__main__":
    # �������Ȥ��ʱ��㣨��λ���룩
    target_time = 2.3  # ���磺������2.3���Ƶ��
    
    # ����Ƶ��ͼ�����ú��ĺ���
    fig, freq, spectrum = generate_single_spectrum(
        r'D:\CUDA\ceshi.wav',  # ��Ƶ�ļ�·��
        target_time=target_time,  # Ŀ��ʱ���
        nperseg=512,       # FFT���ڳ���
        noverlap=256,      # FFT�����ص�����
        dpi=150            # ͼ��ֱ���
    )
    
    # ����Ƶ��ͼ����ͼ�����Ϊͼ���ļ�
    output_img = r'D:\CUDA\spectrum_at_time.png'  # ���·��
    fig.savefig(output_img, bbox_inches='tight')  # ���ղ��ֱ���
    plt.close(fig)  # �ر�ͼ���ͷ��ڴ�
    print(f"saved to: {output_img}")
    
    # === ��ѡƵ�׷���ʾ�� ===
    
    # 1. ������Ƶ�ʣ���߷��ȶ�Ӧ��Ƶ�ʣ�
    peak_freq_idx = np.argmax(spectrum)  # �ҵ������ȶ�Ӧ������
    peak_freq = freq[peak_freq_idx]  # ��Ƶ�������ȡ��ӦƵ��
    print(f"f: {peak_freq:.1f} Hz")
    
    # 2. �����ض�Ƶ�ʷ�Χ��Ƶ������������������Χ��
    vocal_range = (85, 255)  # ������ҪƵ�ʷ�Χ(������Ƶ)
    # ɸѡ��ָ��Ƶ�ʷ�Χ�ڵ�Ƶ�׵�
    in_range = spectrum[(freq >= vocal_range[0]) & (freq <= vocal_range[1])]
    vocal_energy = np.mean(in_range)  # ����ƽ��ֵ��Ϊ����ָ��
    print(f"pingjunenergy: {vocal_energy:.4f}")
    
    # 3. �����������㣨�����������ռ������������
    total_energy = np.sum(spectrum)  # ������
    high_freq_range = (2000, sample_rate/2)  # ����Ƶ�ʷ�Χ(2kHz����)
    # ɸѡ������Ƶ�׵�
    high_freq_energy = np.sum(spectrum[(freq >= high_freq_range[0])])
    high_freq_ratio = high_freq_energy / total_energy * 100  # �ٷֱ�
    print(f"gaoyinzhanbi: {high_freq_ratio:.1f}%")