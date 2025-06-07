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
wavOutput_path = "workspace\\wavOutput.wav"
binOri_path = "workspace\\binOri.bin"
binBpsk_path = "workspace\\binBpsk_path.bin"
binDebpsk_path = "workspace\\binDebpsk.bin"
pngTempDir_path = "workspace\\pngTemp"
pngOI_path = "使用说明.png"
pngBpsk_path = "workspace\\pngBpsk.png"
mp4Silent_path = "workspace\\mp4Silent.mp4"
mp4Output_path = "workspace\\mp4Output.mp4"
#
isSave = 0
isInputWav = 0
isOriBin = 0
isBPSK = 0
#
fps_set = 30
def nothing():
    no = 1
    no += 1