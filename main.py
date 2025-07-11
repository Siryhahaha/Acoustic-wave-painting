from lib import *

def select_wav_bin():
    """选择wav或者bin文件"""
    global wavInput_path
    global binInput_path
    global iswav
    file = filedialog.askopenfilename(
        title="选择文件",
        filetypes=[
            ("WAV文件", "*.wav"),
            ("BIN文件", "*.bin"),
        ]
    )
    if file:
        ext = os.path.splitext(file)[1].lower()
        if ext==".wav":
            wavInput_path = file
            iswav = 1
        elif ext==".bin":
            binInput_path = file
            iswav = 0
        file_label.config(text=os.path.basename(file))

def play_audio():
    """播放音频"""
    if wavInput_path == "":
        messagebox.showwarning("提示", "请先选择WAV文件好吗")
        return
    os.startfile(wavInput_path)

def update_ylim_status():
    global isylim
    isylim = 1 if ylim_var.get() else 0

def update_GenMP4_status():
    global ismp4
    ismp4 = 1 if GenMP4_var.get() else 0

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

def save_wav():
    """保存wav"""
    if saveDir_path == "":
        messagebox.showwarning("提示", "请先选择保存路径好吗")
        return
    try:
        shutil.copy(wavOutput_path,saveDir_path)
        messagebox.showinfo("成功", "wav已保存")
    except:
        messagebox.showerror("错误", "保存失败")

def save_bin():
    """保存bin"""
    if saveDir_path == "":
        messagebox.showwarning("提示", "请先选择保存路径好吗")
        return
    try:
        shutil.copy(binOutput_path,saveDir_path)
        messagebox.showinfo("成功", "bin已保存")
    except:
        messagebox.showerror("错误", "保存失败")

def save_workspace():
    """保存工作区"""
    if saveDir_path == "":
        messagebox.showwarning("提示", "请先选择保存路径好吗")
        return
    try:
        dir_copy("workspace",saveDir_path)
        messagebox.showinfo("成功", "工作文件已保存")
    except:
        messagebox.showerror("错误", "保存失败")

def execute_function():
    """绘影"""
    global isInput,isylim,iswav,ismp4,fps_set,wavInput_path,binInput_path
    #判断输入情况
    if -isInput:
        messagebox.showinfo("错误", "请先选择输入一个好吗")
        return
    #判断输入格式
    if iswav:
        file_copy(wavInput_path, wavOutput_path)
        wav_read_bin(wavInput_path, binOutput_path)
    else:
        file_copy(binInput_path, binOutput_path)
        bin_read_wav(44100, binInput_path, wavOutput_path)
    #生成三维频谱图
    generate_spectrogram(wavOutput_path, pngTAF_path)
    #生成频谱视频
    if ismp4 == 1:
        fps_set = frame_rate_var.get()
        duration, num_spectra, interval, A_max =get_time_num_imterval(wavOutput_path, fps=fps_set)
        for i in range(num_spectra + 1):
            generate_png(wavOutput_path, duration, interval, i, fps=fps_set, A_max=A_max, isylim=isylim)
            print(f"{(i/num_spectra)*100:.1f}%")
        png_mp4(fps=fps_set)
        mp4_addWav(mp4Silent_path, wavOutput_path, mp4Output_path)
    messagebox.showinfo("完成", "声波绘影已完成！\n请选择上方显示")

def update_display():
    """更新显示区域"""
    disp_type = display_type.get()

    # 清除之前的显示内容
    display_label.config(image="", text="")

    if disp_type == "操作说明":
        try:
            img_path = pngOI_path
            img = Image.open(img_path)
            img = img.resize((600, 400), Image.LANCZOS)
            photo0 = ImageTk.PhotoImage(img)
            display_label.config(image=photo0)
            display_label.image = photo0
        except:
            display_label.config(text="还没做呢（）")

    elif disp_type == "全时长频谱图":
        try:
            img_path = pngTAF_path  # 确保此路径有效
            if not os.path.exists(img_path):
                raise FileNotFoundError

            img = Image.open(img_path)
            img = img.resize((600, 350), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            display_label.config(image=photo)
            display_label.image = photo
        except:
            display_label.config(text="请点击下方“绘影”")

    elif disp_type == "音频":
        try:
            os.startfile(wavOutput_path)
        except:
            display_label.config(text="请点击下方“绘影”")

    elif disp_type == "视频":
        try:
            os.startfile(mp4Output_path)
        except:
            display_label.config(text="请点击下方“绘影”")


# 主程序部分保持不变...

if __name__ == "__main__":

    workspace_init()

    root = tk.Tk()
    root.title("声波绘影——音频可视化链路系统")
    root.geometry("800x620")

    top_frame = tk.Frame(root)
    top_frame.pack(fill=tk.X, padx=10, pady=5)
    tk.Label(top_frame, text="欢迎使用声波绘影系统",
             font=("微软雅黑", 12, "bold")).pack(side=tk.LEFT)

    #主内容
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    #左侧
    left_frame = tk.LabelFrame(main_frame, text="控制")
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
    #文件操作
    tk.Label(left_frame, text="文件操作:").grid(row=0, column=0, sticky="w", pady=5)
    file_label = tk.Label(left_frame, text="未选择文件", width=15, anchor="w")
    file_label.grid(row=1, column=0, padx=5)
    tk.Button(left_frame, text="选择输入文件", command=select_wav_bin, width=12
              ).grid(row=2, column=0, pady=5)
    tk.Button(left_frame, text="播放音频", command=play_audio, width=12
              ).grid(row=3, column=0, pady=5)
    #生成规则
    tk.Label(left_frame, text="生成规则:", pady=5, anchor="w").grid(row=4, column=0, sticky="w", pady=(15, 0))
    rule_frame = tk.Frame(left_frame)
    rule_frame.grid(row=5, column=0, sticky="we", padx=5)
    tk.Label(rule_frame, text="帧率选择:").grid(row=0, column=0, sticky="w", padx=(0, 5))
    frame_rate_var = tk.IntVar(value=30)
    ttk.Combobox(rule_frame, textvariable=frame_rate_var,
                 values=[1, 5, 10, 20, 24, 30], width=4, state="readonly").grid(row=0, column=1, sticky="w")
    ylim_var = tk.BooleanVar(value=False)
    ylim_cb = ttk.Checkbutton(rule_frame, text="纵轴变化", variable=ylim_var, command=update_ylim_status
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(5, 0))
    GenMP4_var = tk.BooleanVar(value=True)
    ylim_cb = ttk.Checkbutton(rule_frame, text="生成MP4", variable=GenMP4_var, command=update_GenMP4_status
        ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(5, 0))
    #保存操作
    tk.Label(left_frame, text="保存操作:", pady=5).grid(row=6, column=0, sticky="w", pady=(15, 5))
    save_label = tk.Label(left_frame, text="未设置路径", width=15, anchor="w")
    save_label.grid(row=7, column=0, padx=5)
    tk.Button(left_frame, text="选择保存路径", command=select_save_dir, width=12
              ).grid(row=8, column=0, pady=5)
    tk.Button(left_frame, text="保存MP4", command=save_mp4, width=12
              ).grid(row=9, column=0, pady=5)
    tk.Button(left_frame, text="保存WAV", command=save_wav, width=12
              ).grid(row=10, column=0, pady=5)
    tk.Button(left_frame, text="保存BIN", command=save_bin, width=12
              ).grid(row=11, column=0, pady=5)
    tk.Button(left_frame, text="保存工作文件", command=save_workspace, width=12
              ).grid(row=12, column=0, pady=5)

    #右侧
    right_frame = tk.LabelFrame(main_frame, text="显示与输出")
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
    # 显示类型选择
    disp_frame = tk.Frame(right_frame)
    disp_frame.pack(fill=tk.X, pady=5)
    tk.Label(disp_frame, text="显示:").pack(side=tk.LEFT)
    display_type = tk.StringVar(value="操作说明")
    ttk.Combobox(disp_frame, textvariable=display_type,
                values=["操作说明",  "视频", "音频", "全时长频谱图"], width=15, state="readonly"
                ).pack(side=tk.LEFT)
    tk.Button(disp_frame, text="更新显示", command=update_display
             ).pack(side=tk.LEFT, padx=10)
    #显示
    display_frame = tk.Frame(right_frame, bd=1, relief=tk.SUNKEN, bg="white")
    display_frame.pack(fill=tk.BOTH, expand=True, pady=5)
    display_label = tk.Label(display_frame)
    display_label.pack()
    #绘影
    tk.Button(right_frame, text="绘影", command=execute_function,
              width=15).pack(pady=10)
    #tag
    info_frame = tk.Frame(right_frame, bd=1, relief=tk.SUNKEN)
    info_frame.pack(fill=tk.X, pady=5)
    left_text = tk.Label(info_frame, text="by 踹开那扇门 —— 孙艺 马梓豪 李昊峻", anchor="w")
    left_text.grid(row=0, column=0, sticky="w", padx=5)
    right_text = tk.Label(info_frame, text="今日："+time.strftime("%Y-%m-%d"), anchor="e")
    right_text.grid(row=0, column=1, sticky="e", padx=5)
    info_frame.columnconfigure(0, weight=1)
    info_frame.columnconfigure(1, weight=1)

    root.after(200, update_display)
    root.mainloop()
    dir_clear(pngTempDir_path)