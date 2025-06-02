import numpy as np
import matplotlib.pyplot as plt

#从.bin文件读取信号
recovered_x2 = np.fromfile('S1.bin', dtype=np.float32)

#重新生成位置坐标
recovered_k2 = np.arange(-20,21)

# 3. 绘图验证
plt.stem(recovered_k2, recovered_x2)
plt.title("S1.bin")
plt.xlabel("k")
plt.ylabel("x")
plt.show()