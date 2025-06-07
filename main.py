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

def play_audio():
    """播放音频"""
    if wavInput_path == "":
        messagebox.showwarning("提示", "请先选择WAV文件好吗")
        return
    os.startfile(wavInput_path)

def update_bpsk_status():
    global isBPSK
    isBPSK = 1 if bpsk_var.get() else 0

def select_save_dir():
    """选择保存目录"""
    global saveDir_path
    dir = filedialog.askdirectory(title="选择保存路径")
    if dir:
        saveDir_path = dir
        save_label.config(text=f"保存到: {dir}")

def save_mp4():
    """保存mp4"""
    if saveDir_path == "":
        messagebox.showwarning("提示", "请先选择保存路径好吗")
        return
    try:
        shutil.copy(mp4Output_path,saveDir_path)
        messagebox.showinfo("成功", "mp4已保存")
    except:
        messagebox.showerror("错误", "保存失败")

def save_workspace():
    """保存工作区"""
    if saveDir_path == "":
        messagebox.showwarning("提示", "请先选择保存路径好吗")
        return
    try:
        shutil.copy(mp4Output_path,saveDir_path)
        messagebox.showinfo("成功", "工作文件已保存")
    except:
        messagebox.showerror("错误", "保存失败")

def execute_function():
    """执行功能"""
    global fps_set
    fps_set = frame_rate_var.get()
    duration, num_spectra, interval, A_max =get_time_num_imterval(wavInput_path, fps=fps_set)
    for i in range(num_spectra + 1):
        generate_png(wavInput_path, duration, interval, i, fps=fps_set, A_max=A_max)
        print(f"{(i/num_spectra)*100:.1f}%")
    png_mp4(fps=fps_set)
    mp4_addWav(mp4Silent_path, wavInput_path, mp4Output_path)
    messagebox.showinfo("完成", "功能执行完毕")

def update_display():
    """更新显示区域"""
    disp_type = display_type.get()

    # 清除之前的显示内容
    display_label.config(image="", text="")

    if disp_type == "说明":
        try:
            img_path = pngOI_path  # 确保此路径有效
            if not os.path.exists(img_path):
                raise FileNotFoundError

            img = Image.open(img_path)
            img = img.resize((450, 300), Image.LANCZOS)
            photo0 = ImageTk.PhotoImage(img)
            display_label.config(image=photo0)
            display_label.image = photo0  # 保持引用
        except:
            display_label.config(text="说明图片加载失败")

    elif disp_type == "全时长频谱图":
        try:
            img_path = pngBpsk_path  # 确保此路径有效
            if not os.path.exists(img_path):
                raise FileNotFoundError

            img = Image.open(img_path)
            img = img.resize((450, 300), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            display_label.config(image=photo)
            display_label.image = photo  # 保持引用
        except:
            display_label.config(text="BPSK图片加载失败")

    elif disp_type == "解调后音频":
        try:
            ########
            a = 1
        except:
            display_label.config(text="音频播放失败")

    elif disp_type == "视频":
        try:
            os.startfile(mp4Output_path)
        except:
            display_label.config(text="视频播放失败")


# 主程序部分保持不变...

if __name__ == "__main__":
    workspace_init()
    # 创建主窗口
    root = tk.Tk()
    root.title("声波绘影——音频可视化链路系统")
    root.geometry("800x550")

    # 顶部栏
    top_frame = tk.Frame(root)
    top_frame.pack(fill=tk.X, padx=10, pady=5)
    tk.Label(top_frame, text="欢迎使用声波绘影系统",
             font=("微软雅黑", 12, "bold")).pack(side=tk.LEFT)

    # 主内容区域
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # 左侧控制面板
    left_frame = tk.LabelFrame(main_frame, text="控制")
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
    # 文件操作区 (保持不变)
    tk.Label(left_frame, text="文件操作:").grid(row=0, column=0, sticky="w", pady=5)
    file_label = tk.Label(left_frame, text="未选择文件", width=15, anchor="w")
    file_label.grid(row=1, column=0, padx=5)
    tk.Button(left_frame, text="选择WAV音频", command=select_wav, width=12
              ).grid(row=2, column=0, pady=5)
    tk.Button(left_frame, text="播放音频", command=play_audio, width=12
              ).grid(row=3, column=0, pady=5)
    # 生成规则区
    tk.Label(left_frame, text="生成规则:", pady=5, anchor="w").grid(row=4, column=0, sticky="w", pady=(15, 0))
    rule_frame = tk.Frame(left_frame)
    rule_frame.grid(row=5, column=0, sticky="we", padx=5)
    tk.Label(rule_frame, text="帧率选择:").grid(row=0, column=0, sticky="w", padx=(0, 5))
    frame_rate_var = tk.IntVar(value=30)
    ttk.Combobox(rule_frame, textvariable=frame_rate_var,
                 values=[1, 5, 10, 20, 24, 30], width=4, state="readonly").grid(row=0, column=1, sticky="w")
    bpsk_var = tk.BooleanVar(value=False)
    bpsk_cb = ttk.Checkbutton(rule_frame, text="BPSK调制", variable=bpsk_var, command=update_bpsk_status
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(5, 0))
    # 保存操作区
    tk.Label(left_frame, text="保存操作:", pady=5).grid(row=6, column=0, sticky="w", pady=(15, 5))
    save_label = tk.Label(left_frame, text="未设置路径", width=15, anchor="w")
    save_label.grid(row=7, column=0, padx=5)
    tk.Button(left_frame, text="选择保存路径", command=select_save_dir, width=12
              ).grid(row=8, column=0, pady=5)
    tk.Button(left_frame, text="保存MP4", command=save_mp4, width=12
              ).grid(row=9, column=0, pady=5)
    tk.Button(left_frame, text="保存工作文件", command=save_workspace, width=12
              ).grid(row=10, column=0, pady=5)

    # 右侧显示面板
    right_frame = tk.LabelFrame(main_frame, text="显示与输出")
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
    # 显示类型选择
    disp_frame = tk.Frame(right_frame)
    disp_frame.pack(fill=tk.X, pady=5)
    tk.Label(disp_frame, text="显示:").pack(side=tk.LEFT)
    display_type = tk.StringVar(value="说明")
    ttk.Combobox(disp_frame, textvariable=display_type,
                values=["说明", "全时长频谱图", "解调后音频", "视频"], width=8, state="readonly"
                ).pack(side=tk.LEFT)
    tk.Button(disp_frame, text="更新显示", command=update_display
             ).pack(side=tk.LEFT, padx=10)
    # 显示区域
    display_frame = tk.Frame(right_frame, bd=1, relief=tk.SUNKEN, bg="white")
    display_frame.pack(fill=tk.BOTH, expand=True, pady=5)
    display_label = tk.Label(display_frame)
    display_label.pack()
    # 功能按钮
    tk.Button(right_frame, text="绘影", command=execute_function,
              width=15).pack(pady=10)
    # 信息标签
    info_frame = tk.Frame(right_frame, bd=1, relief=tk.SUNKEN)
    info_frame.pack(fill=tk.X, pady=5)
    left_text = tk.Label(info_frame, text="by 踹开那扇门 —— 孙艺 马梓豪 李昊峻", anchor="w")
    left_text.grid(row=0, column=0, sticky="w", padx=5)
    right_text = tk.Label(info_frame, text="当前时间："+time.strftime("%Y-%m-%d"), anchor="e")
    right_text.grid(row=0, column=1, sticky="e", padx=5)
    info_frame.columnconfigure(0, weight=1)
    info_frame.columnconfigure(1, weight=1)

    root.after(200, update_display)
    root.mainloop()
    dir_clear(pngTempDir_path)