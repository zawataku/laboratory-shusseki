import tkinter as tk
from tkinter import messagebox
import csv
from os import makedirs, path
import nfc
import threading

# NFC の UID を格納する変数（グローバル）
idm_value = None

# UID を取得する関数
def read_uid():
    global idm_value
    # NFCリーダーと接続
    clf = nfc.ContactlessFrontend('usb')
    print("NFCリーダーを起動しました。カードをスキャンしてください...")
    clf.connect(rdwr={'on-connect': on_card})
    clf.close()

# NFC カードがスキャンされたときに呼び出される関数
def on_card(tag):
    global idm_value
    idm_value = str(tag.identifier.hex())  # UID を 16進数文字列に変換
    print(f"読み取ったUID: {idm_value}")
    return False  # 読み取り後に終了

# ユーザー登録画面を開く関数
def open_register_window():
    if idm_value is None:
        messagebox.showwarning("エラー", "カードをスキャンしてください！")
        return

    register_window = tk.Toplevel(root)
    register_window.title("ユーザー登録")

    # スキャン済みの UID を表示
    tk.Label(register_window, text="スキャンしたIDM:").grid(row=0, column=0, padx=10, pady=10)
    tk.Label(register_window, text=idm_value, fg="blue").grid(row=0, column=1, padx=10, pady=10)

    # 名前入力欄
    tk.Label(register_window, text="名前:").grid(row=1, column=0, padx=10, pady=10)
    name_entry = tk.Entry(register_window)
    name_entry.grid(row=1, column=1, padx=10, pady=10)

    # 登録処理
    def register_user():
        name = name_entry.get()
        if not name:
            messagebox.showwarning("エラー", "名前を入力してください！")
            return

        save_user(idm_value, name)
        messagebox.showinfo("成功", "ユーザーが登録されました！")
        register_window.destroy()

    # 登録ボタン
    tk.Button(register_window, text="登録", command=register_user).grid(row=2, column=0, columnspan=2, pady=20)

# ユーザー情報を保存する関数
def save_user(idm, name):
    log_directory = "data/student_data"
    if not path.exists(log_directory):
        makedirs(log_directory)

    filename = path.join(log_directory, "data.csv")
    try:
        with open(filename, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([idm, name])
    except Exception as e:
        messagebox.showerror("エラー", f"ユーザー情報の保存に失敗しました: {e}")

# NFC 読み取りスレッドを起動
def start_nfc_thread():
    thread = threading.Thread(target=read_uid)
    thread.daemon = True
    thread.start()

# メインウィンドウ
root = tk.Tk()
root.title("トップ画面")

# ボタン
tk.Label(root, text="トップ画面", font=("Arial", 16)).pack(pady=20)
tk.Button(root, text="NFC スキャンを開始", command=start_nfc_thread, width=20, height=2).pack(pady=10)
tk.Button(root, text="ユーザー登録", command=open_register_window, width=20, height=2).pack(pady=10)

# アプリのメインループ
root.mainloop()
