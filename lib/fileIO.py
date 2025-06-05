import numpy as np
import cv2
import os
import scipy.io.wavfile as wav
from lib.constants import *
#这里读写文件，包括读wav、读bin、bin-wav转换、读写png、png转mp4

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
    """读png，png-mp4"""
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
