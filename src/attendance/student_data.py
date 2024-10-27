import csv

def load_student_data():
    student_data = {}
    with open('data/student_data/data.csv', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            student_data[row['idm']] = row['name']
    return student_data

def get_student_name(idm):
    student_data = load_student_data()
    return student_data.get(idm)
