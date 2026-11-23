"""The questions the app asks. `read` defaults to the keyboard."""

from collections.abc import Callable

Read = Callable[[str], str]


def ask_choice(options: list[str], prompt: str, read: Read = input) -> str:
    while True:
        answer = read(f"{prompt} ({'/'.join(options)}): ")
        if answer in options:
            return answer
        print(f"Please choose one of: {', '.join(options)}")


def ask_whole_number(prompt: str, read: Read = input) -> int:
    while True:
        answer = read(f"{prompt}: ")
        if answer.isdigit() and int(answer) > 0:
            return int(answer)
        print("Please enter a whole number, 1 or more")
