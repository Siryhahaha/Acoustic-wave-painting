import matplotlib.pyplot as plt
import numpy as np
import math
# from scipy.io import wavfile
# from scipy import signal

plt.figure(figsize=(10, 4))

plt.subplot(2,1,2)
k = np.arange(-20, 21)
x = np.zeros(len(k))
x[k] = (0.9 ** k) * (np.sin(0.25 * math.pi * k) + np.cos(0.25 * math.pi * k))
plt.stem(k, x)  # 画火柴棒图

x.astype(np.float32).tofile('S1.bin')
print("Save as S1.bin ,Size:", len(x)*4, "Byte")