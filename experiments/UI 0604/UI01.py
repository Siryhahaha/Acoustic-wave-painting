import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import time
import threading
from PIL import Image, ImageTk

# 全局变量用于存储路径
wavInput_path = ""
save_path = ""  # 保存路径


def play_audio():
    """播放音频的线程函数"""
    if not wavInput_path:
        messagebox.showwarning("警告", "请先选择.wav文件")
        return

    try:
        # 使用系统默认播放器打开音频
        os.startfile(wavInput_path)
    except Exception as e:
        messagebox.showerror("错误", f"播放音频失败: {str(e)}")


def execute_function():
    """执行功能按钮的回调函数"""
    messagebox.showinfo("执行", "执行功能按钮被点击！")
    update_output(operation="功能执行")
    # 在这里可以执行你的具体函数


def save_file():
    """保存文件按钮的回调函数"""
    if not save_path:
        messagebox.showwarning("警告", "请先选择保存路径")
        return

    # 在这里添加实际保存文件的代码
    try:
        # 示例保存操作 - 替换为你的实际逻辑
        with open(os.path.join(save_path, "example.txt"), "w") as f:
            f.write(f"声波绘影系统保存操作于 {time.strftime('%Y-%m-%d %H:%M:%S')}")
        messagebox.showinfo("保存成功", f"文件已保存到:\n{save_path}")
        update_output(operation="保存完成")
    except Exception as e:
        messagebox.showerror("错误", f"保存文件失败: {str(e)}")


def select_save_path():
    """选择保存路径"""
    global save_path
    folder_path = filedialog.askdirectory(
        title="选择保存路径",
        initialdir=os.getcwd()
    )

    if folder_path:
        save_path = folder_path
        # 更新路径标签显示
        save_path_label.config(text=f"保存到: {folder_path}")
        messagebox.showinfo("路径已选择", f"已选择保存路径:\n{folder_path}")
        update_output(operation="设置保存路径")


def update_time():
    """更新时间显示"""
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    time_label.config(text=current_time)
    root.after(1000, update_time)  # 每秒更新一次


def update_output(operation="初始化"):
    """根据下拉菜单选项更新输出区域"""
    # 更新信息标签
    info_label.config(text=f"{operation}于: {time.strftime('%H:%M:%S')}")

    # 尝试加载图片或视频
    try:
        if display_type.get() == "图片":
            # 尝试加载图片
            img = Image.open("output.png")
            img = img.resize((300, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            output_label.config(image=photo)
            output_label.image = photo  # 保持引用
        else:
            # 视频功能尚未实现
            output_label.config(image="", text="视频功能未实现")
    except:
        # 如果图片加载失败，显示占位符
        output_label.config(image="", text="无输出内容")


def select_wav_file():
    """选择.wav文件"""
    global wavInput_path
    file_path = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title="选择音频文件",
        filetypes=(("WAV files", "*.wav"), ("All files", "*.*"))
    )

    if file_path:
        wavInput_path = file_path
        # 更新文件路径标签显示
        file_label.config(text=f"已选择: {os.path.basename(file_path)}")
        update_output(operation="文件选择")


# 创建主窗口
root = tk.Tk()
root.title("声波绘影系统")
root.geometry("800x500")

# 创建顶部框架（欢迎信息和时间）
top_frame = tk.Frame(root, height=40)
top_frame.pack(fill=tk.X, padx=10, pady=5)

# 欢迎标签
welcome_label = tk.Label(
    top_frame,
    text="欢迎使用声波绘影系统",
    font=("Arial", 14, "bold")
)
welcome_label.pack(side=tk.LEFT)

# 时间标签
time_label = tk.Label(top_frame, font=("Arial", 10))
time_label.pack(side=tk.RIGHT)

# 创建主内容框架
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# 左侧控制面板
left_frame = tk.LabelFrame(
    main_frame,
    text="控制区域",
    padx=10,
    pady=10,
    font=("Arial", 10)
)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

# 文件选择部分
file_frame = tk.LabelFrame(
    left_frame,
    text="文件操作",
    padx=5,
    pady=5
)
file_frame.pack(fill=tk.X, pady=5)

file_label = tk.Label(
    file_frame,
    text="请选择.wav音频文件",
    wraplength=180,
    justify=tk.LEFT
)
file_label.pack(pady=5)

tk.Button(
    file_frame,
    text="选择音频文件",
    command=select_wav_file,
    width=15
).pack(pady=5)

tk.Button(
    file_frame,
    text="播放音频",
    command=lambda: threading.Thread(target=play_audio).start(),
    width=15
).pack(pady=5)

# 保存操作部分
save_frame = tk.LabelFrame(
    left_frame,
    text="保存操作",
    padx=5,
    pady=5
)
save_frame.pack(fill=tk.X, pady=5)

save_path_label = tk.Label(
    save_frame,
    text="未设置保存路径",
    wraplength=180,
    justify=tk.LEFT
)
save_path_label.pack(pady=5)

tk.Button(
    save_frame,
    text="选择保存路径",
    command=select_save_path,
    width=15
).pack(pady=5)

tk.Button(
    save_frame,
    text="保存文件",
    command=save_file,
    width=15
).pack(pady=5)

# 右侧输出面板
right_frame = tk.LabelFrame(
    main_frame,
    text="输出区域",
    padx=10,
    pady=10,
    font=("Arial", 10)
)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# 输出类型选择（使用下拉菜单替换复选框）
display_frame = tk.Frame(right_frame)
display_frame.pack(fill=tk.X, pady=5)

tk.Label(display_frame, text="显示类型:").pack(side=tk.LEFT, padx=5)

display_type = tk.StringVar(value="图片")
display_menu = ttk.Combobox(
    display_frame,
    textvariable=display_type,
    values=["图片", "视频"],
    state="readonly",
    width=10
)
display_menu.pack(side=tk.LEFT, padx=5)
display_menu.bind("<<ComboboxSelected>>", lambda e: update_output(operation="显示类型变更"))

# 输出显示区域
output_label = tk.Label(
    right_frame,
    relief=tk.SUNKEN,
    borderwidth=1,
    bg="white"
)
output_label.pack(fill=tk.BOTH, expand=True, pady=5)

# 功能操作部分
button_frame = tk.Frame(right_frame)
button_frame.pack(fill=tk.X, pady=5)

tk.Button(
    button_frame,
    text="执行功能",
    command=execute_function,
    width=15
).pack(pady=10)

# 信息标签
info_label = tk.Label(
    right_frame,
    text="等待操作...",
    wraplength=300,
    justify=tk.LEFT,
    relief=tk.SUNKEN,
    padx=5,
    pady=5,
    anchor="w"
)
info_label.pack(fill=tk.X, pady=5)

# 底部状态栏
bottom_frame = tk.Frame(root, height=25, bg="#f0f0f0")
bottom_frame.pack(fill=tk.X, padx=10, pady=5)

status_label = tk.Label(
    bottom_frame,
    text="系统就绪 | 声波绘影系统 v1.0",
    bg="#f0f0f0",
    fg="#666"
)
status_label.pack(side=tk.LEFT)

# 初始化系统显示
update_time()  # 启动时间更新
update_output()  # 初始更新输出

# 运行主循环
root.mainloop()