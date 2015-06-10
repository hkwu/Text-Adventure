import os
import string
import textwrap

SCREEN_WIDTH = 75

# Utility functions
def wrapStr(string):
    """
    Textwraps a string using SCREEN_WIDTH 
    and joins them with newlines, then prints
    """
    split_str = string.splitlines()

    if len(split_str) == 1:
        print("\n".join(textwrap.wrap(split_str[0], SCREEN_WIDTH)))
    else:
        index = 0

        for paragraph in split_str:
            print("\n".join(textwrap.wrap(paragraph, SCREEN_WIDTH)))

            # We don't print extra line at end of entire dialogue
            if index < len(split_str) - 1:
                print("")

            index += 1


def cls():
    """Clears the screen"""
    os.system("cls" if os.name == "nt" else "clear")


def dialoguePrompt():
    """Special prompt for dialogue sequences that allows quitting"""
    choice = input("> ")
    if choice.lower() == "q" or choice.lower() == "quit":
        cls()
        print("Game Over!")
        raise SystemExit
    else:
        return