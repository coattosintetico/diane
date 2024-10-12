import datetime
import subprocess
import os

now = datetime.datetime.now().strftime(r"%Y%m%d%H%M%S")
FILENAME = f"./data/{now}.m4a"

def record():
    subprocess.run(["termux-microphone-record", "-f", FILENAME], check=True, stdout=subprocess.DEVNULL)

def stop():
    subprocess.run(["termux-microphone-record", "-q"], check=True, stdout=subprocess.DEVNULL)
    os.remove(FILENAME)  # Remove the file after stopping the recording

if __name__ == "__main__":
    record()
    input("🧏🏻 listening...")
    stop()
