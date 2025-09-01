# commands_map.py
import re

COMMANDS = {
    r"take off(?: (\d+))?": ("takeoff", None),
    r"land": ("land", None),
    r"return home|rtl": ("return_home", None),
    r"move forward(?: (\d+))?": ("forward", None),
    r"move backward(?: (\d+))?": ("backward", None),
    r"move left(?: (\d+))?": ("left", None),
    r"move right(?: (\d+))?": ("right", None),
    r"move up(?: (\d+))?": ("up", None),
    r"move down(?: (\d+))?": ("down", None),
    r"set speed (\d+)": ("speed", None),
}

