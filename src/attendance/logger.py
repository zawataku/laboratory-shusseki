import csv
from datetime import datetime
from os import path, makedirs

def log_attendance(student_name):
    today = datetime.now().strftime('%Y%m%d')
    log_directory = path.join(path.dirname(path.abspath(__file__)), "../../data/attendance_log")
    filename = path.join(log_directory, f'{today}.csv')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # フォルダが存在しない場合は作成
    if not path.exists(log_directory):
        makedirs(log_directory)
    
    # ログ保存処理
    try:
        is_new_file = not path.exists(filename)
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if is_new_file:
                writer.writerow(["Student Name", "Timestamp"])
            writer.writerow([student_name, now])
        print(f"Attendance logged for {student_name}")
    except Exception as e:
        print(f"Error logging attendance: {e}")

import csv

def is_already_logged(student_name):
    today = datetime.now().strftime('%Y%m%d')
    log_directory = path.join(path.dirname(path.abspath(__file__)), "../../data/attendance_log")
    filename = path.join(log_directory, f'{today}.csv')

    if not path.exists(filename):
        return False  # ファイルが存在しなければ未ログとして扱う

    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) > 0 and row[0] == student_name:
                    return True  # 学生名が既にログに存在
        return False
    except Exception as e:
        print(f"Error checking log: {e}")
        return False
