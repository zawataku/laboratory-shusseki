import tkinter as tk
import time

def setup_gui(root, welcome_message, current_time, status_message):
    welcome_label = tk.Label(root, textvariable=welcome_message, font=("Helvetica", 24))
    welcome_label.pack(pady=10)

    time_label = tk.Label(root, textvariable=current_time, font=("Helvetica", 18))
    time_label.pack(pady=10)

    status_label = tk.Label(root, textvariable=status_message, font=("Helvetica", 18))
    status_label.pack(pady=20)

def update_time(root, current_time):
    def update():
        current_time.set(time.strftime("%Y-%m-%d %H:%M:%S"))
        root.after(1000, update)
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
