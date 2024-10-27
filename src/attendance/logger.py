import os
from datetime import datetime

log_file = 'attendance_log.txt'

def log_attendance(student_name):
    with open(log_file, 'a', encoding='utf-8') as file:
        file.write(f"{datetime.now()}, {student_name}\n")

def is_already_logged(student_name):
    if not os.path.exists(log_file):
        return False
    with open(log_file, 'r', encoding='utf-8') as file:
        for line in file:
            if student_name in line:
                return True
    return False
