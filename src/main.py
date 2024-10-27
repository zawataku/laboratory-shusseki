import time
import threading
import tkinter as tk
from attendance import logger, student_data
from gui import gui_manager
from sound import sound_manager

def on_card(tag):
    idm = tag.identifier.hex()
    student_name = student_data.get_student_name(idm)  # student_dataから学生名を取得

    if student_name:
        if logger.is_already_logged(student_name):
            sound_manager.play_sound('data/sounds/error.mp3')
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
    # カードを読み取るための仮の関数（ここに実際のリーダー処理を実装）
    pass

if __name__ == "__main__":
    root = tk.Tk()
    root.title("出欠席管理システム")
    root.geometry("640x480")
    root.resizable(False, False)

    status_label = tk.Label(root, text="", font=("Helvetica", 18))
    status_label.pack(pady=20)

    welcome_message = tk.StringVar()
    welcome_message.set("Welcome to ○○研究室！")

    current_time = tk.StringVar()
    status_message = tk.StringVar()

    gui_manager.setup_gui(root, welcome_message, current_time, status_message)
    gui_manager.update_time(current_time)

    student_data.load_student_data()  # データをロード
    threading.Thread(target=read_card, daemon=True).start()

    root.mainloop()
