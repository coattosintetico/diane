import os
import subprocess
import time
from pathlib import Path

from openai import OpenAI

from src.llm_call import extract_expense

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
        transcript = OPENAI_CLIENT.audio.transcriptions.create(
            model="whisper-1",
            file=audio,
            response_format="text",
            prompt="hola, son 3.50 euros",
        )
    os.remove(FILENAME)
    return transcript


def main():
    print()
    print()
    print("HEY... I'M DIANE")
    print()
    print()
    record()
    input("\t(👉👂 listening...)")
    stop()
    print("\t(🤔 mhh...)")
    transcript = transcribe()
    print(f"\t(🗣️ \"{transcript}\")")
    print("\t(🛠️...)")
    expense = extract_expense(transcript)
    print()
    print("\033[3mwell, I think I understood the following:\033[0m")
    print()
    print("┌───")
    print(f"│ description: {expense.description.lower()}")
    print(f"│ amount:      {expense.amount}")
    print(f"│ category:    {expense.category.value}")
    print("└───")
    print()
    confirmation = input("is that right? (Y/n)")
    if confirmation.lower() == "n":
        print("ooops sorry")
    else:
        print("nice then")


if __name__ == "__main__":
    main()
    # expense = extract_expense("cervezas en el pepe, 7.20, alcoholesto")
    # expense = extract_expense("compra mercadona helados, 12.50, sobrevivir es caro")
    # print(expense)
