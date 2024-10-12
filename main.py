import datetime
import os
import subprocess
from pathlib import Path

from openai import OpenAI

REPOSITORY_PATH = Path("/data/data/com.termux/files/home/diane")
DATA_FOLDER_PATH = REPOSITORY_PATH / "data"

FILENAME = DATA_FOLDER_PATH / f"{datetime.datetime.now().strftime(r'%Y%m%d%H%M%S')}.m4a"

with open(Path("/data/data/com.termux/files/home/.secrets/openai_api_key.txt"), "r") as file:
    OPENAI_API_KEY = file.read().strip()


def record():
    subprocess.run(["termux-microphone-record", "-f", FILENAME], check=True, stdout=subprocess.DEVNULL)


def stop():
    subprocess.run(["termux-microphone-record", "-q"], check=True, stdout=subprocess.DEVNULL)


def transcribe():
    client = OpenAI(api_key=OPENAI_API_KEY)
    with open(FILENAME, "rb") as audio:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio,
            response_format="text",
            prompt="Hola! ¿Qué tal?",
        )
    return transcript.text

def cleanup():
    os.remove(FILENAME)


if __name__ == "__main__":
    print("\nHEY... I'M DIANE\n")
    record()
    input("\n\t(👉👂 listening...)")
    print("\t🤔 mhh...")
    transcript = transcribe()
    stop()
    print("\nthx Cooper, noted:\n")
    print(f"\t{transcript}\n")
    cleanup()