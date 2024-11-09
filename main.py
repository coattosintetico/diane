import os
import subprocess
import time
from pathlib import Path

from openai import OpenAI

REPOSITORY_PATH = Path("/data/data/com.termux/files/home/diane")
FILENAME = REPOSITORY_PATH / "audiorecording.m4a"  # this is how Termux saves the audio file by default

OPENAI_CLIENT = OpenAI()


def record():
    subprocess.run(["termux-microphone-record", "-f", FILENAME], check=True, stdout=subprocess.DEVNULL)


def stop():
    subprocess.run(["termux-microphone-record", "-q"], check=True, stdout=subprocess.DEVNULL)
    # Give some time to the file to be created, otherwise there's a weird race condition
    time.sleep(1)


def transcribe():
    with open(FILENAME, "rb") as audio:
        return OPENAI_CLIENT.audio.transcriptions.create(
            model="whisper-1",
            file=audio,
            response_format="text",
            prompt="hola, son 3.50 euros",
        )


def cleanup():
    os.remove(FILENAME)


if __name__ == "__main__":
    print()
    print("HEY... I'M DIANE")
    print()
    print()
    record()
    input("\t(👉👂 listening...)")
    stop()
    print("\t(🤔 mhh...)")
    transcript = transcribe()
    print()
    print("thx Cooper, noted:")
    print()
    print(f"\t{transcript}")
    cleanup()
