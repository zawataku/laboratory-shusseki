import time
import threading
import tkinter as tk
from attendance import logger, student_data
from gui import gui_manager
from sound import sound_manager
import nfc
import os

# 現在のスクリプトがあるディレクトリを取得
current_dir = os.path.dirname(os.path.abspath(__file__))

# 正しいパスを構築
error_sound_path = os.path.abspath(os.path.join(current_dir, "../data/sounds/error.mp3"))
success_sound_path = os.path.abspath(os.path.join(current_dir, "../data/sounds/success.mp3"))

def on_card(tag):
    idm = tag.identifier.hex()
    # student_dataは辞書として扱う
    student_name = student_data.get(idm)  # student_dataから学生名を取得

    if student_name:
        if logger.is_already_logged(student_name):
            sound_manager.play_sound(error_sound_path)
            status_message.set(f"Error！\n{student_name} は既に出席済みです。")
            status_label.config(fg="white", bg="gray")
        else:
            logger.log_attendance(student_name)
            sound_manager.play_sound('data/sounds/success.mp3')
            status_message.set(f"{student_name}\n出席しました。")
            status_label.config(fg="white", bg="green")
    else:
        sound_manager.play_sound('data/sounds/error.mp3')
        status_message.set("Error！\n不正なユーザーです。")
        status_label.config(fg="white", bg="red")
    root.after(5000, clear_status_message)
    return True

def clear_status_message():
    status_message.set("")

def read_card():
    clf = nfc.ContactlessFrontend('usb')
    while True:
        clf.connect(rdwr={'on-connect': on_card})
        time.sleep(1)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("出欠席管理システム")
    root.geometry("640x480")
    root.resizable(False, False)

    welcome_message = tk.StringVar()
    welcome_message.set("Welcome to ○○研究室！")

    current_time = tk.StringVar()
    status_message = tk.StringVar()

    # GUIセットアップ
    gui_manager.setup_gui(root, welcome_message, current_time, status_message)

    # `status_label` を初期化
    status_label = tk.Label(
        root,
        textvariable=status_message,  # メッセージを表示
        font=("Arial", 16),
        fg="white",
        bg="gray",
        width=40,
        height=5,
    )
    # status_label.pack(pady=20)  # GUI内に配置

    gui_manager.update_time(current_time)  # 修正: current_timeのみを渡す

    # 学生データの読み込み
    student_data = student_data.load_student_data()

    # カード読み取り処理をバックグラウンドで実行
    threading.Thread(target=read_card, daemon=True).start()

    root.mainloop()