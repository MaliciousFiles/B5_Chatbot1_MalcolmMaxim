# Main file/interface
from time import sleep
import sys

from src.response_parser import ResponseParser

__author__ = "Maxim Rebguns and Malcolm Roalson"
__copyright__ = "Copyright 2020, the creators of Ogekron"
__credits__ = ["Gunnar Z."]

__license__ = ""  # To be determined
__version__ = "0.0.1"
__status__ = "Development"

ART = """
-----------------------------------------------------------------------------
|                         ###                                 /\            |
|                        ######                              /  \           |
|                         #######                           |    |          |
|                            ####                         --:'''':--        |
|                             ###                           :'_' :          |
|                              #                            _:"":\___       |
|                __        _    #            ' '      ____.' :::     '._    |
|              _/  \    _(\(o                . *=====<<=)           \    :  |
|             /     \  /  _  ^^^o             .  '      '-'-'\_      /'._.' |
|            /   !   \/  ! '!!!v'                              \====:_ ""   |
|           !  !  \ _' ( \____                                .'     \\\\     |
|            ! . \ _!\   \===^\)                              :       :     |
| Art by      \ \_!  / __!                                   /   :    \     |
|  Gunnar Z.   \!   /    \                                  :   .      '.   |
|        (\_      _/   _\ )                                 :  : :      :   |
|         \ ^^--^^ __-^ /(__                                :__:-:__.;--'   |   
|          ^^----^^    "^--v'                               '-'   '-'       |
-----------------------------------------------------------------------------
"""
WELCOME_MESSAGE = """\nHello, my name is Ogrekron. I have traveled far and wide, all across Aquara. I've fought monsters and dragons, and concocted potions of great power! What are you interested in, commoner?"""


def slow_print(text, skip_whitespace=False, end="\n"):
    for c in text:
        print(c, end="")
        sys.stdout.flush()
        if skip_whitespace and (c == " " or c == "\t"):
            sleep(0.01)
            continue
        sleep(0.05)
    print(end=end)


def main(skip_intro=False):
    if not skip_intro:
        slow_print(ART, True, "")
        slow_print(f"Version {__version__} by {__author__}.")

        if __status__ == "Development":
            print(
                "Ogekron is still in development. Please be aware that the bot is unfinished."
            )

        slow_print(WELCOME_MESSAGE)

    response_parser = ResponseParser("src/responses.json")
    # Main loop
    while True:
        # The user input is first, as the original prompt
        # is printed above.
        user_input = input("\033[94m(type q to quit)\033[0m ").strip()

        if user_input.lower() == "q":
            break

        response = response_parser.get_response(user_input)
        slow_print(response)


if __name__ == "__main__":
    main()
