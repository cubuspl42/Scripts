import subprocess
import time

def run_adb_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    
    if result.returncode != 0:
        print("Error:", result.stderr)
    
    return result.stdout

def run_adb_input_char(char):
    run_adb_command(f'adb shell input text {char}')

def run_adb_input_tap(pos):
    (x, y) = pos
    run_adb_command(f'adb shell input tap {x} {y}')

delay = 1.0
# delay = 0.01

position = (970, 1240)
# position = (550, 470)

for i in range(5):
    message = f"Hello{i}"

    for char in message:
        run_adb_input_char(char)
        time.sleep(delay) 

    run_adb_input_tap(position)
    time.sleep(delay) 
