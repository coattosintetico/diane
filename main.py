import os
import subprocess
from pathlib import Path
import time
from openai import OpenAI

REPOSITORY_PATH = Path("/data/data/com.termux/files/home/diane")
DATA_FOLDER_PATH = REPOSITORY_PATH / "data"

FILENAME = DATA_FOLDER_PATH / f"audiorecording.m4a"

with open(Path("/data/data/com.termux/files/home/.secrets/openai_api_key.txt"), "r") as file:
    OPENAI_API_KEY = file.read().strip()


def record():
    subprocess.run(["termux-microphone-record", "-f", FILENAME], check=True, stdout=subprocess.DEVNULL)


def stop():
    subprocess.run(["termux-microphone-record", "-q"], check=True, stdout=subprocess.DEVNULL)
    # Give some time to the file to be created
    time.sleep(1)


def transcribe():
    client = OpenAI(api_key=OPENAI_API_KEY)
    with open(FILENAME, "rb") as audio:
        return client.audio.transcriptions.create(
            model="whisper-1",
            file=audio,
            response_format="text",
            prompt="hola, hablo en español",
        )

def cleanup():
    os.remove(FILENAME)


if __name__ == "__main__":
    print("\nHEY... I'M DIANE\n")
    record()
    input("\n\t(👉👂 listening...)")
    stop()
    print("\t🤔 mhh...")
    transcript = transcribe()
    print("\nthx Cooper, noted:\n")
    print(f"\t{transcript}\n")
    cleanup()