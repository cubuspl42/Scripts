import os
import subprocess

def get_last_screenshot_path():
    command = "adb shell ls -t /sdcard/Pictures/Screenshots/ | head -n 1"
    result = subprocess.check_output(command, shell=True).decode('utf-8').strip()
    return f"/sdcard/Pictures/Screenshots/{result}"

def copy_screenshot_to_computer(screenshot_path):
    command = f"adb pull {screenshot_path}"
    os.system(command)

if __name__ == "__main__":
    last_screenshot_path = get_last_screenshot_path()
    copy_screenshot_to_computer(last_screenshot_path)
