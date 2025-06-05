import tkinter as tk
from tkinter import messagebox as box
from tkinter import filedialog, ttk
from PIL import Image, ImageTk  # 需要安装Pillow库: pip install Pillow
import time
import threading


def main():
    # 1. 创建主窗口
    root = tk.Tk()
    root.title("声波绘影 - Tkinter学习")
    root.geometry("600x500")  # 扩大窗口尺寸

    # ==================== 布局管理器 ====================
    # 创建主框架 - 使用grid布局
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # 左侧面板 - 使用pack布局
    left_panel = tk.Frame(main_frame, bd=2, relief=tk.GROOVE)
    left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

    # 右侧面板 - 使用grid布局
    right_panel = tk.Frame(main_frame)
    right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # ==================== 基础控件 ====================
    # 标签控件
    label = tk.Label(
        left_panel,
        text="Tkinter控件演示",
        font=("Arial", 12, "bold"),
        fg="blue"
    )
    label.pack(pady=10)

    # 输入框控件
    entry = tk.Entry(
        left_panel,
        width=25
    )
    entry.pack(pady=5)

    # 按钮控件
    def on_button_click():
        user_input = entry.get()
        box.showinfo(
            "提示",
            f"输入内容: {user_input}\n"
            f"复选框状态: {check_var.get()}\n"
            f"单选按钮选择: {radio_var.get()}"
        )

    button = tk.Button(
        left_panel,
        text="显示输入内容",
        command=on_button_click,
        width=15,
        height=2
    )
    button.pack(pady=5)

    # ==================== 复选框 ====================
    check_var = tk.BooleanVar()
    check_button = tk.Checkbutton(
        left_panel,
        text="同意条款",
        variable=check_var,
        onvalue=True,
        offvalue=False
    )
    check_button.pack(pady=5)

    # ==================== 单选按钮 ====================
    radio_var = tk.StringVar(value="选项1")

    tk.Label(left_panel, text="选择一项:").pack(anchor=tk.W)

    for i, text in enumerate(["选项1", "选项2", "选项3"], 1):
        rb = tk.Radiobutton(
            left_panel,
            text=text,
            variable=radio_var,
            value=f"选项{i}"
        )
        rb.pack(anchor=tk.W)

    # ==================== 下拉菜单 ====================
    options = ["Python", "Java", "C++", "JavaScript"]
    combo_var = tk.StringVar()
    combo = ttk.Combobox(
        left_panel,
        textvariable=combo_var,
        values=options,
        state="readonly"
    )
    combo.set("选择语言")  # 默认显示文本
    combo.pack(pady=5)

    # ==================== 图片显示 ====================
    try:
        # 尝试加载图片 (需要准备一张test.jpg放在同目录)
        img = Image.open("test.jpg")
        img = img.resize((200, 150), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)

        img_label = tk.Label(right_panel, image=photo)
        img_label.image = photo  # 保持引用
        img_label.grid(row=0, column=0, padx=5, pady=5)
    except FileNotFoundError:
        no_img_label = tk.Label(right_panel, text="图片未找到\n(请准备test.jpg)", fg="red")
        no_img_label.grid(row=0, column=0)

    # ==================== 文件对话框 ====================
    def open_file():
        file_path = filedialog.askopenfilename(
            title="选择文件",
            filetypes=[("图片文件", "*.jpg *.png"), ("所有文件", "*.*")]
        )
        if file_path:
            box.showinfo("文件选择", f"已选择文件:\n{file_path}")

    file_button = tk.Button(
        right_panel,
        text="打开文件",
        command=open_file,
        width=15
    )
    file_button.grid(row=1, column=0, pady=5)

    # ==================== 新窗口 ====================
    def open_new_window():
        new_win = tk.Toplevel(root)
        new_win.title("新窗口")
        new_win.geometry("300x200")

        tk.Label(new_win, text="这是一个独立的新窗口").pack(pady=20)

        def close_new():
            new_win.destroy()
            box.showinfo("提示", "新窗口已关闭")

        tk.Button(new_win, text="关闭", command=close_new).pack()

    new_win_button = tk.Button(
        right_panel,
        text="打开新窗口",
        command=open_new_window,
        width=15
    )
    new_win_button.grid(row=2, column=0, pady=5)

    # ==================== 实时时钟 ====================
    def update_clock():
        current_time = time.strftime("%H:%M:%S")
        clock_label.config(text=current_time)
        root.after(1000, update_clock)  # 每秒更新一次

    clock_label = tk.Label(
        right_panel,
        text="",
        font=("Arial", 14),
        fg="green"
    )
    clock_label.grid(row=3, column=0, pady=10)
    update_clock()  # 启动时钟

    # ==================== 进度条 ====================
    progress = ttk.Progressbar(
        right_panel,
        orient=tk.HORIZONTAL,
        length=200,
        mode='determinate'
    )
    progress.grid(row=4, column=0, pady=10)

    def start_progress():
        def run():
            for i in range(101):
                progress['value'] = i
                root.update_idletasks()
                time.sleep(0.05)

        threading.Thread(target=run).start()

    progress_button = tk.Button(
        right_panel,
        text="开始进度条",
        command=start_progress,
        width=15
    )
    progress_button.grid(row=5, column=0, pady=5)

    # ==================== 文本框 ====================
    text_frame = tk.Frame(right_panel)
    text_frame.grid(row=0, column=1, rowspan=6, padx=10, sticky=tk.N + tk.S)

    text = tk.Text(
        text_frame,
        width=30,
        height=20,
        wrap=tk.WORD
    )
    text.pack(side=tk.LEFT, fill=tk.BOTH)

    scroll = tk.Scrollbar(text_frame)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)

    text.config(yscrollcommand=scroll.set)
    scroll.config(command=text.yview)

    # 默认添加一些文本
    text.insert(tk.END, "这是一个文本框示例\n\n")
    text.insert(tk.END, "你可以在这里输入多行文本\n")
    text.insert(tk.END, "也可以显示程序输出内容\n")

    root.mainloop()


if __name__ == "__main__":
    main()