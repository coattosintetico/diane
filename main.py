import datetime
import subprocess
import os
from pathlib import Path

REPOSITORY_PATH = Path("/data/data/com.termux/files/home/diane")
DATA_FOLDER_PATH = REPOSITORY_PATH / "data"

FILENAME = DATA_FOLDER_PATH / f"{datetime.datetime.now().strftime(r'%Y%m%d%H%M%S')}.m4a"

def record():
    subprocess.run(["termux-microphone-record", "-f", FILENAME], check=True, stdout=subprocess.DEVNULL)

def stop():
    subprocess.run(["termux-microphone-record", "-q"], check=True, stdout=subprocess.DEVNULL)
    os.remove(FILENAME)  # Remove the file after stopping the recording

if __name__ == "__main__":
    print("\n\tHEY... I'M DIANE\n")
    record()
    input("(👉👂 listening...)")
    stop()
    print("\n\tthx Cooper, noted\n")
