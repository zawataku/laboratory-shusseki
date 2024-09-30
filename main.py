import csv
import nfc
import time
from datetime import datetime

from os import environ
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

# 出席をログに記録
def log_attendance(student_name):
    today = datetime.now().strftime('%Y%m%d')
    filename = f'{today}.csv'
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([student_name, now])

# カード読み取り時の処理
def on_card(tag):
    # UIDの取得とコンソール出力
    idm = tag.identifier.hex()
    print(f"Scanned Card UID: {idm}")  # UIDをデバッグ用に出力
    
    # 学生情報の確認
    student_name = student_data.get(idm)
    
    if student_name:
        print(f'Attendance recorded for: {student_name}')
        log_attendance(student_name)
        play_sound('success.mp3')  # 成功音を鳴らす
    else:
        print('Error: Student not found!')
        play_sound('error.mp3')  # エラー音を鳴らす
    return True

# カードリーダーの初期化と待機
def read_card():
    clf = nfc.ContactlessFrontend('usb')
    while True:
        clf.connect(rdwr={'on-connect': on_card})
        time.sleep(1)

if __name__ == '__main__':
    student_data = load_student_data()
    read_card()
