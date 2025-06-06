import os
import hashlib
from pathlib import Path

BASE_PATH = Path(os.getenv('LOCALAPPDATA') or Path.home() / ".local" / "share") / 'Void Runner'
SECRET_KEY = "nicoleismygirlfriend"

def load_data(file ,list=False):
    path = BASE_PATH / f"{secret_letter(file)}.{get_hash(secret_letter(file))}.txt"
    try:
        f = open(path, 'r')
        data = f.read()
        f.close()
        if not list:
            return decode(data)
        else:
            return data
    except:
        return "0"

def save_data(file, data, list=False):
    path = BASE_PATH / f"{secret_letter(file)}.{get_hash(secret_letter(file))}.txt"
    f = open(path, 'w')
    if not list:
        f.write(f"{data}:{get_hash(data)}")
    else: 
        f.write(data)
    f.close()


def load_numbers(file, list=False):
    data = load_data(file, True)
    if list and data == "0":
        return [1, 0, 0, 0]
    lines = data.strip().split('\n')
    return [int(decode(line)) for line in lines ]


def save_numbers(file, numbers):
    data = "" 
    for num in numbers:
        data += f"{str(num)}:{get_hash(str(num))}\n" 
    save_data(file, data, False)

def get_hash(data):
    return hashlib.sha256((data + SECRET_KEY).encode()).hexdigest()

def decode(data):
    try:
        value, hash = data.split(":")
        expected_hash = get_hash(value)

        if hash == expected_hash:
            return value
        else:
            return "0"
    
    except Exception:
        return "0"    

def secret_letter(word):
    return word[1:4]

def reset_files():
    save_data('coins.txt', str(0))
    save_data('highScore.txt', str(0))
    save_data('music.txt', str(1))
    save_data('sfx.txt', str(1))
    save_data('player.txt', str(1))
    save_numbers('store.txt', [1, 0, 0, 0])

