import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import time
from PIL import Image, ImageTk
from lib import *

def select_wav():
    """选择音频文件"""
    global wavInput_path
    file = filedialog.askopenfilename(
        title="选择WAV文件",
        filetypes=(("WAV文件", "*.wav"),)
    )
    if file:
        wavInput_path = file
        file_label.config(text=os.path.basename(file))
        info_label.config(text=f"已选择: {os.path.basename(file)}")

def play_audio():
    """播放音频"""
    if wavInput_path == "":
        messagebox.showwarning("提示", "请先选择WAV文件好吗")
        return
    os.startfile(wavInput_path)

def select_save_dir():
    """选择保存目录"""
    global saveDir_path
    dir = filedialog.askdirectory(title="选择保存路径")
    if dir:
        saveDir_path = dir
        save_label.config(text=f"保存到: {dir}")
        info_label.config(text=f"保存路径: {dir}")

def save_results():
    """保存结果"""
    if saveDir_path == "":
        messagebox.showwarning("提示", "请先选择保存路径好吗")
        return
    try:
        dir_copy("workspace", saveDir_path)
        messagebox.showinfo("成功", "文件已保存")
        info_label.config(text=f"保存完成!")
    except:
        messagebox.showerror("错误", "保存失败")

def execute_function():
    """执行功能"""
    info_label.config(text="处理中...")
    ###############################这里进行主要工作
    info_label.config(text="处理完成")
    messagebox.showinfo("完成", "功能执行完毕")

def update_display():
    """更新显示区域"""
    disp_type = display_type.get()
    if disp_type == "图片":
        try:
            ###########这里改图片
            img = Image.open(pngBpsk_path)
            img = img.resize((300, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            display_label.config(image=photo)
            display_label.image = photo
        except:
            display_label.config(image="", text="图片加载失败")
    else:
        display_label.config(image="", text="视频功能暂未实现")


# 创建主窗口
root = tk.Tk()
root.title("声波绘影——音频可视化链路系统")
root.geometry("700x450")

# 顶部栏
top_frame = tk.Frame(root)
top_frame.pack(fill=tk.X, padx=10, pady=5)

tk.Label(top_frame, text="欢迎使用声波绘影系统",
         font=("微软雅黑", 12, "bold")).pack(side=tk.LEFT)

time_label = tk.Label(top_frame, text=time.strftime("%Y-%m-%d %H:%M:%S"))
time_label.pack(side=tk.RIGHT)

# 主内容区域
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# 左侧控制面板
left_frame = tk.LabelFrame(main_frame, text="控制")
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)

# 文件操作区
tk.Label(left_frame, text="文件操作:").grid(row=0, column=0, sticky="w", pady=5)
file_label = tk.Label(left_frame, text="未选择文件", width=15, anchor="w")
file_label.grid(row=1, column=0, padx=5)

tk.Button(left_frame, text="选择WAV音频", command=select_wav, width=12
         ).grid(row=2, column=0, pady=5)
tk.Button(left_frame, text="播放音频", command=play_audio, width=12
         ).grid(row=3, column=0, pady=5)

# 保存操作区
tk.Label(left_frame, text="保存操作:").grid(row=4, column=0, sticky="w", pady=5)
save_label = tk.Label(left_frame, text="未设置路径", width=15, anchor="w")
save_label.grid(row=5, column=0, padx=5)

tk.Button(left_frame, text="选择保存路径", command=select_save_dir, width=12
         ).grid(row=6, column=0, pady=5)
tk.Button(left_frame, text="保存结果", command=save_results, width=12
         ).grid(row=7, column=0, pady=5)

# 右侧显示面板
right_frame = tk.LabelFrame(main_frame, text="显示与输出")
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

# 显示类型选择
disp_frame = tk.Frame(right_frame)
disp_frame.pack(fill=tk.X, pady=5)
tk.Label(disp_frame, text="显示:").pack(side=tk.LEFT)
display_type = tk.StringVar(value="图片")
ttk.Combobox(disp_frame, textvariable=display_type,
            values=["图片", "视频"], width=8, state="readonly"
            ).pack(side=tk.LEFT)
tk.Button(disp_frame, text="更新显示", command=update_display
         ).pack(side=tk.LEFT, padx=10)

# 显示区域
display_frame = tk.Frame(right_frame, bd=1, relief=tk.SUNKEN, bg="white")
display_frame.pack(fill=tk.BOTH, expand=True, pady=5)
display_label = tk.Label(display_frame)
display_label.pack()

# 功能按钮
tk.Button(right_frame, text="执行功能", command=execute_function,
          width=15).pack(pady=10)

# 信息标签
info_label = tk.Label(right_frame, text="就绪", bd=1, relief=tk.SUNKEN,
                     anchor="w", padx=5)
info_label.pack(fill=tk.X, pady=5)

# 时间更新
def update_time():
    time_label.config(text=time.strftime("%Y-%m-%d %H:%M:%S"))
    root.after(1000, update_time)

# 初始显示
update_time()
root.after(100, lambda: info_label.config(text="请选择音频文件开始"))
root.after(200, update_display)

root.mainloop()

#############这里清空初始化
# workspace_init()