import tkinter as tk
import time

def setup_gui(root, welcome_message, current_time, status_message):
    # ラベルやウィジェットのセットアップ
    tk.Label(root, textvariable=welcome_message, font=("Arial", 24)).pack(pady=20)
    tk.Label(root, textvariable=current_time, font=("Arial", 16)).pack(pady=10)
    global status_label
    status_label = tk.Label(root, textvariable=status_message, font=("Arial", 16), width=40, height=5)

def update_time(current_time):
    def update():
        current_time.set(time.strftime("%Y-%m-%d %H:%M:%S"))
        status_label.after(1000, update)  # 毎秒更新
    update()


# GUIの初期化例
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sample GUI")

    welcome_message = tk.StringVar(value="Welcome to the GUI!")
    current_time = tk.StringVar()
    status_message = tk.StringVar(value="Status: Running")

    setup_gui(root, welcome_message, current_time, status_message)
    update_time(root, current_time)

    root.mainloop()
