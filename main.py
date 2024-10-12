import csv
import nfc
import time
from datetime import datetime
from os import environ, path, makedirs
import threading
import tkinter as tk
from tkinter import Label
from tkinter import StringVar

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

# サウンドの初期化
pygame.mixer.init()

# サウンド再生関数
def play_sound(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

# 学生データの読み込み
def load_student_data():
    student_data = {}
    with open('data.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            student_data[row['idm']] = row['name']
    return student_data

# 既に出席記録があるか確認する関数
def is_already_logged(student_name):
    today = datetime.now().strftime('%Y%m%d')
    log_directory = "attendance_log"  # 保存先フォルダ
    filename = path.join(log_directory, f'{today}.csv')  # 当日のログファイル
    
    # ログファイルが存在しない場合はまだ出席記録がない
    if not path.exists(filename):
        return False

    # CSVファイルを読み込んで同じ学生名が既にあるか確認
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == student_name:
                return True
    return False

# 出席をログに記録
def log_attendance(student_name):
    today = datetime.now().strftime('%Y%m%d')
    log_directory = "attendance_log"  # 保存先フォルダ
    filename = path.join(log_directory, f'{today}.csv')  # フォルダ内にファイルを作成
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # フォルダが存在しない場合は作成
    if not path.exists(log_directory):
        makedirs(log_directory)
    
    # ログをCSVに追記
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([student_name, now])

# GUIの設定
def update_time():
    current_time.set(datetime.now().strftime('%Y-%m-%d\n%H:%M:%S'))
    root.after(1000, update_time)  # 1秒ごとに更新

# ステータスメッセージを5秒後に消す
def clear_status_message():
    status_message.set("")  # ステータスラベルのテキストを空にする
    status_label.config(bg=root['bg'])  # 背景色をウィンドウのデフォルトにリセット

# カード読み取り時の処理
def on_card(tag):
    # UIDの取得とコンソール出力
    idm = tag.identifier.hex()
    
    # 学生情報の確認
    student_name = student_data.get(idm)
    
    if student_name:
        # 既に同日のログに記録があるか確認
        if is_already_logged(student_name):
            play_sound('error.mp3')  # エラー音を鳴らす
            status_message.set(f"Error！\n{student_name} は既に出席済みです。")
            status_label.config(fg="white", bg="gray")
        else:
            now = datetime.now().strftime('%H:%M')
            log_attendance(student_name)
            play_sound('success.mp3')  # 成功音を鳴らす
            status_message.set(f"{student_name}\n\n{now}　出席しました。")
            status_label.config(fg="white", bg="green")
    else:
        play_sound('error.mp3')  # エラー音を鳴らす
        status_message.set("Error！\n不正なユーザーです。")
        status_label.config(fg="white", bg="red")

    root.after(5000, clear_status_message)
    return True

# カードリーダーの初期化と待機
def read_card():
    clf = nfc.ContactlessFrontend('usb')
    while True:
        clf.connect(rdwr={'on-connect': on_card})
        time.sleep(1)

# Tkinterウィンドウの設定
root = tk.Tk()
root.title("出欠席管理システム")
root.geometry("640x480")
root.resizable(False,False)

# ウェルカムメッセージを表示するラベル
welcome_message = StringVar()
welcome_message.set("Welcome to ○○研究室！")
welcome_label = Label(root, textvariable=welcome_message, font=("MS Gothic", 30),fg="blue")
welcome_label.pack(pady=(20, 0))  # 時刻の上に少し余裕を持たせて表示

# 現在時刻を表示するラベル
current_time = StringVar()
time_label = Label(root, textvariable=current_time, font=("MS Gothic", 50))
time_label.pack(pady=(30, 30))  # ウェルカムメッセージの後に表示

# ステータスメッセージを表示するラベル
status_message = StringVar()
status_label = Label(root, textvariable=status_message, font=("MS Gothic", 30), fg="white")  # 初期文字色は白
status_label.pack(pady=(20,50))

# 時刻の更新
update_time()

# カード読み取りを別スレッドで実行
student_data = load_student_data()
threading.Thread(target=read_card, daemon=True).start()

root.mainloop()
