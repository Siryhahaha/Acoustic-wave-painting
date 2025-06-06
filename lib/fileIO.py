import numpy as np
import cv2
import os
import shutil
import scipy.io.wavfile as wav
from tkinter import filedialog, messagebox, ttk
from .constants import *
import natsort

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
    img = cv2.imread(png_path, cv2.IMREAD_UNCHANGED)
    return img

def png_write(png, png_path="pngTempDir_path\\0.png"):
    png.tofile(png_path)

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


def png_mp4(image_folder=pngTempDir_path, output_mp4=mp4Output_path, fps=2):
    """"""
    # 验证文件夹存在
    if not os.path.exists(image_folder):
        raise FileNotFoundError(f"图片文件夹不存在: {image_folder}")

    # 获取文件夹中所有PNG文件（自然排序）
    png_files = [f for f in os.listdir(image_folder) if f.lower().endswith('.png')]
    if not png_files:
        raise ValueError(f"文件夹中没有PNG图片: {image_folder}")

    # 按自然顺序排序（考虑数字顺序）
    png_files = natsort.natsorted(png_files)

    # 获取第一张图片的尺寸
    first_frame = cv2.imread(os.path.join(image_folder, png_files[0]))
    if first_frame is None:
        raise ValueError(f"无法读取第一帧图片: {png_files[0]}")

    height, width, _ = first_frame.shape
    size = (width, height)

    # 创建视频写入对象
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4编码器
    out = cv2.VideoWriter(output_mp4, fourcc, fps, size)

    # 处理并写入每帧图片
    for png_file in png_files:
        file_path = os.path.join(image_folder, png_file)
        frame = cv2.imread(file_path)

        if frame is None:
            print(f"警告: 跳过无法读取的图片: {png_file}")
            continue

        # 如果尺寸不匹配，调整大小
        if frame.shape[1] != width or frame.shape[0] != height:
            frame = cv2.resize(frame, size)

        out.write(frame)

    # 释放资源
    out.release()
    print(f"视频已保存至: {output_mp4}")
    print(f"共处理 {len(png_files)} 张图片, 帧率: {fps}fps")