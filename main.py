import os
import readline
import subprocess
import time
from pathlib import Path

from openai import OpenAI

from src.add_expense import add_expense
from src.llm_call import extract_expense

REPOSITORY_PATH = Path("/data/data/com.termux/files/home/diane")
FILENAME = REPOSITORY_PATH / "audiorecording.m4a"  # this is how Termux saves the audio file by default

OPENAI_CLIENT = OpenAI()


def greetings():
    print()
    print()
    print("HEY COOPER... I'M DIANE")
    print()
    print()


def record():
    subprocess.run(["termux-microphone-record", "-f", FILENAME], check=True, stdout=subprocess.DEVNULL)


def stop():
    subprocess.run(["termux-microphone-record", "-q"], check=True, stdout=subprocess.DEVNULL)
    # Give some time to the file to be created, otherwise there's a weird race condition
    time.sleep(0.5)


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


def get_input_with_default(prompt: str, default: str) -> str:
    def hook():
        readline.insert_text(default)
        readline.redisplay()

    readline.set_pre_input_hook(hook)
    try:
        return input(prompt)
    finally:
        readline.set_pre_input_hook()


def main():
    expense_not_saved_yet = True

    while expense_not_saved_yet:
        record()
        input("\t(👉👂 listening...)")
        stop()
        print("\t(🤔 mhh...)")
        transcript = transcribe()
        print(f'\t(🗣️ "{transcript}")')
        print("\t(🛠️...)")
        expense = extract_expense(transcript)
        print()
        print("\033[3mwell, I think I understood the following:\033[0m")
        print()
        print("┌───")
        print(f"│ description: {expense.description}")
        print(f"│ amount:      {expense.amount}")
        print(f"│ category:    {expense.category.value}")
        print("└───")
        print()
        confirmation = input("is that right or correct description? (Y/n/r)")
        if confirmation.lower() == "r":
            print("sorry, retrying...")
            print()
            continue
        elif confirmation.lower() == "n":
            corrected_description = get_input_with_default(
                "ooops sorry, try correcting the description:\n\n> ", expense.description
            )
            expense.description = corrected_description
        print()
        print("\t(📝 saving...)")
        add_expense(expense)
        print("\t(✅ done)")
        print()
        expense_not_saved_yet = False
    return


if __name__ == "__main__":
    greetings()
    main()
