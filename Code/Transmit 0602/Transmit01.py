import matplotlib.pyplot as plt
import numpy as np
import math

"""
将生成的np数组保存到S1.bin中，并绘图呈现
在main后分别注释语句1和2，即可分别查看代码功能
"""

def generate_and_save_data():
    #生成信号，保存到bin文件
    k = np.arange(-20, 21)
    x = np.zeros(len(k))
    x[k] = (0.9 ** k) * (np.sin(0.25 * math.pi * k) + np.cos(0.25 * math.pi * k))
    x.astype(np.float32).tofile('S1.bin')   #写入
    print("Save as S1.bin ,Size:", len(x) * 4, "Byte")
    return k, x


def load_and_plot():
    #读取与载入范围
    recovered_x = np.fromfile('S1.bin', dtype=np.float32)   #读取
    recovered_k = np.arange(len(recovered_x))
    # 绘图
    plt.stem(recovered_k, recovered_x)
    plt.title("S1")
    plt.xlabel("k")
    plt.ylabel("x")
    plt.grid(True)
    plt.show()
    return recovered_k, recovered_x

if __name__ == "__main__":
    _, _ = generate_and_save_data()  # 生成并保存
    _, _ = load_and_plot()  # 加载并绘图