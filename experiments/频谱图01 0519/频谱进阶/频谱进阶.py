# -*- coding: utf-8 -*-
# ָ���ļ�����ΪUTF-8��ȷ������·�����������

import numpy as np  # ������ѧ����⣬�����������
import matplotlib.pyplot as plt  # ͼ����ƿ⣬���ڴ���Ƶ��ͼ
from scipy.io import wavfile  # ��SciPy������Ƶ�ļ���ȡ����
from scipy.signal import stft  # ��ʱ����Ҷ�任������Ƶ�׷���
import warnings  # Python���þ���ģ�飬������ܳ��ֵľ�����Ϣ

# === Ĭ�ϲ������� ===
input_wav = 'yinpin\ceshi.wav'  # Ĭ����Ƶ�ļ�·��
nperseg = 1024  # FFT���ڳ��ȣ�������������Ӱ��Ƶ�ʷֱ��ʺ�ʱ��ֱ���
noverlap = 512   # FFT�����ص����ȣ�����������������Ƶ�ױ߽�ЧӦ�����ʱ��������
dpi = 150         # ���ͼ��ֱ��ʣ�ÿӢ�����������ֵԽ��ͼ��Խ����

# ��ӻ�ȡ��Ƶʱ���ĺ���
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
            nperseg=nperseg,    # STFT���ڳ���(����)
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
        # ax.set_title(f'{actual_time:.3f}s:')  # ��ʾʵ��ʱ���
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
    # ��ȡ��Ƶ��ʱ��
    duration = get_audio_duration(input_wav)
    if duration is None:
        print("error")
        exit(1) 
    print(f"total length: {duration:.2f} s")   
    # ���ò������
    interval = 0.5    
    # ������Ҫ���ɵ�Ƶ��ͼ����
    num_spectra = int(duration / interval)    
    # ѭ������Ƶ��ͼ
    for i in range(num_spectra + 1):
        target_time = i * interval        
        # ���ⳬ����Ƶʱ��
        if target_time > duration:
            break          
        # ����Ƶ��ͼ
        fig, freq, spectrum = generate_single_spectrum(
            input_wav,
            target_time=target_time,
            nperseg=nperseg,
            noverlap=noverlap,
            dpi=dpi
        )       
        # ����ͼ�����
        fig.suptitle(f"t: {target_time:.2f}s  (total_t: {duration:.2f}s)", fontsize=12)        
        # ��ʾͼƬ
        plt.show()      
        # �رյ�ǰͼƬ��ż���
        plt.close(fig)    
        
        # ��ѡ������Ƶ��ͼ
        # output_img = f'tupian/spectrum_{i:03d}_{target_time:.1f}s.png'
        # fig.savefig(output_img, bbox_inches='tight')
        # print(f"�ѱ���: {output_img}")   
    print(f"all {num_spectra} ")