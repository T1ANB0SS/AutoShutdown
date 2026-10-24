import os
import time
import tkinter as tk
from datetime import datetime, timedelta, timezone

timezone_delta = 7 # UTC+7

START_HOUR = 0
END_HOUR = 4

PASSWORD = "christianancelinoadji"

ASK_INTERVAL = 10 * 60 # Seconds before asking again
TIME_LIMIT = 30 # Seconds before shutdown
CANCEL_LIMIT = 5 # Ask amount before immediate shutdown

ENABLE_SHUTDOWN = True

root = tk.Tk()
root.withdraw()

time.sleep(10)

cancel_count = 0

def get_now():
    return datetime.now(timezone(timedelta(hours=timezone_delta)))

def is_restricted_time():
    hour = get_now().hour

    if START_HOUR < END_HOUR:
        return START_HOUR <= hour < END_HOUR

    return hour >= START_HOUR or hour < END_HOUR


def shutdown_pc(delay = 60):
    if ENABLE_SHUTDOWN:
        os.system(f"shutdown /a")
        os.system(f"shutdown /s /t {delay}")


def ask_password():
    result = {"answered": False}

    window = tk.Toplevel(root)
    window.title("Restricted Hours")
    window.geometry("320x150")
    window.attributes("-topmost", True)
    window.resizable(False, False)

    tk.Label(
        window,
        text=f"Enter password within {TIME_LIMIT} seconds:"
    ).pack(pady=10)

    entry = tk.Entry(window, show="*")
    entry.pack()
    entry.focus_set()

    status = tk.Label(window, text="")
    status.pack()

    def submit():
        if entry.get() == PASSWORD:
            result["answered"] = True
            window.destroy()
        else:
            entry.delete(0, tk.END)
            status.config(text="Incorrect password.")

    tk.Button(
        window,
        text="Submit",
        command=submit
    ).pack(pady=5)

    window.after(TIME_LIMIT * 1000, window.destroy)
    window.wait_window()

    return result["answered"]


now = get_now()
now = now.hour * 3600 + now.minute * 60 + now.second
force_shutdown_time = START_HOUR * 3600 + ASK_INTERVAL * CANCEL_LIMIT

if force_shutdown_time <= now:
    force_shutdown_time += 24 * 3600

shutdown_pc(int(force_shutdown_time - now))

while True:

    if is_restricted_time():

        ask_start = time.perf_counter()

        if cancel_count >= CANCEL_LIMIT or not ask_password():
            shutdown_pc()
            cancel_count = 0

        cancel_count += 1

        delta = time.perf_counter()-ask_start
        time.sleep(max(0, ASK_INTERVAL-delta))

    else:
        cancel_count = 0
        time.sleep(60)
