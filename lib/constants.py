import os
import shutil
import subprocess
import sys
import time
import warnings
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import cv2
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("Agg")
import natsort
import numpy as np
from moviepy import AudioFileClip, VideoFileClip
from PIL import Image, ImageTk
from scipy.io import wavfile as wav
from scipy.signal import stft

#路径
saveDir_path = ""
wavInput_path = ""
binInput_path = ""
wavOutput_path = "workspace\\wavOutput.wav"
binOutput_path = "workspace\\binOutput_path.bin"
pngTempDir_path = "workspace\\pngTemp"
pngOI_path = "使用说明.png"
pngTAF_path = "workspace\\pngTAF.png"
mp4Silent_path = "workspace\\mp4Silent.mp4"
mp4Output_path = "workspace\\mp4Output.mp4"

#标志位
isSave = 0
isInput = 0
iswav = 1   #0为bin1为wav
isylim = 0  #0为不变1为变
ismp4 = 1

#帧率
fps_set = 30

def nothing():
    return 0