sudo apt install matchbox-keyboard

import subprocess

def open_keyboard():
    subprocess.Popen(['matchbox-keyboard'])

def close_keyboard():
    subprocess.call(['pkill', 'matchbox-keyboard'])