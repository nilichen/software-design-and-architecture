from questions import ask_choice, ask_whole_number


def test_ask_whole_number_asks_again_until_it_gets_one_or_more():
    answers = iter(["half", "0", "4"])

    assert ask_whole_number("Days", lambda prompt: next(answers)) == 4


def test_ask_choice_asks_again_until_it_gets_an_option():
    answers = iter(["airprot", "airport"])

    branch = ask_choice(
        ["airport", "station", "city"], "Pick-up at", lambda _: next(answers)
    )

    assert branch == "airport"
