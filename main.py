import subprocess

def record():
    subprocess.run(["termux-microphone-record", "-f", "./data/audio.m4a"], check=True, stdout=subprocess.DEVNULL)

def stop():
    subprocess.run(["termux-microphone-record", "-q"], check=True, stdout=subprocess.DEVNULL)

if __name__ == "__main__":
    record()
    input("🧏🏻 listening...")
    stop()
