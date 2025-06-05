import numpy as np
import cv2
import os
import shutil
import scipy.io.wavfile as wav
from tkinter import filedialog, messagebox, ttk
from .constants import *

#这里读写文件，包括读wav、读bin、bin-wav转换、读写png、png转mp4
#文件的复制清除，工作区的初始化
#文件的选择、文件夹的选择
#wav的播放

def wav_read_bin(wav_path=wavInput_path, bin_path=binOri_path):
    """读wav，wav-bin，返回rate和data"""
    rate, data = wav.read(wav_path)
    if data.ndim > 1:
        data = data[:, 0]
    data = data.astype(np.float32) / np.max(np.abs(data))
    data.tofile(bin_path)
    return rate, data

def bin_read_wav(rate=44100, bin_path=binDebpsk_path, wav_path=wavOutput_path):
    """读bin，bin-wav"""
    audio = np.fromfile(bin_path, dtype=np.float32)
    audio_int = (audio * 32767).astype(np.int16)
    wav.write(wav_path, rate, audio_int)

def bin_write(data, bin_path=binBpsk_path):
    data.tofile(bin_path)

def png_read(png_path):
    img = cv2.imread(png_path, cv2.IMREAD_UNCHANGED)  # 支持透明度
    return img

def png_write(png, png_path="pngTempDir_path\\0.png"):
    png.tofile(png_path)

def png_mp4(pngDir=pngTempDir_path, mp4_path=mp4Output_path, fps=20):
    """读png，png-mp4,by ds"""
    images = [img for img in os.listdir(pngDir) if img.endswith(".png")]
    images.sort()
    frame = cv2.imread(os.path.join(pngDir, images[0]))
    height, width, _ = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 编码格式（MP4）
    video = cv2.VideoWriter(mp4_path, fourcc, fps, (width, height))

    #逐帧写入
    for image in images:
        img_path = os.path.join(pngDir, image)
        frame = cv2.imread(img_path)
        video.write(frame)

def dir_copy(DirInput_path, DirOutput_path):
    shutil.copytree(DirInput_path, DirOutput_path)

def file_clear(file_path):
    """直接清空文件"""
    with open(file_path, 'w') as f:
        f.truncate(0)

def dir_clear(dir_path):
    """清空文件夹"""
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        else:
            shutil.rmtree(file_path)

def workspace_init():
    """清空所有本层文件，删除暂存过程png"""
    file_clear(binOri_path)
    file_clear(binBpsk_path)
    file_clear(binDebpsk_path)
    file_clear(pngBpsk_path)
    file_clear(mp4Output_path)
    file_clear(wavOutput_path)
    dir_clear(pngTempDir_path)

