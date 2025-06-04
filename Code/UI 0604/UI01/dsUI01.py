#ui，以学习ds的代码为主哈，别喷我
#主要使用tkinter

import tkinter as tk
from tkinter import messagebox as box


def main():
    # 1. 创建主窗口 - Tk() 是 tkinter 的主窗口类
    root = tk.Tk()

    #标题大小
    root.title("声波绘影")
    root.geometry("300x200")

    # 2. 创建标签控件
    label = tk.Label(
        root,
        text="这是一个简单的GUI示例",
        font=("Arial", 12)
    )
    label.pack(pady=10)

    # 3. 创建按钮控件
    def on_button_click():
        user_input = entry.get()
        box.showinfo(
            "提示",
            f"你点击了按钮！\n输入内容是: {user_input}"
        )

    button = tk.Button(
        root,
        text="点击我",
        command=on_button_click,
        width=15,
        height=2
    )
    button.pack(pady=5)

    # 4. 创建输入框控件
    entry = tk.Entry(
        root,
        width=25
    )
    entry.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()