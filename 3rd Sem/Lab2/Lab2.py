import os
from enum import Enum
from typing import Tuple
import json

# Enum for colors
class Color(Enum):
    RED = '\033[31m'
    GREEN = '\033[32m'
    BLUE = '\033[34m'
    RESET = '\033[0m'

class Printer:
    def __init__(self, color: Color, position: Tuple[int, int], symbol: str = '*'):
        self.color = color
        self.position = position
        self.symbol = symbol

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(Color.RESET.value, end='') 

    def render(self, text: str):
        for i, line in enumerate(self._generate_text(text)):
            print(f"\033[{self.position[1] + i};{self.position[0]}H{self.color.value}{line}{Color.RESET.value}", end="\n")

    @staticmethod
    def load_font(file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"шрифт не найден: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def _generate_text(self, text: str):

        lines = []
        for char in text:
            if char in self.font:
                char_lines = self.font[char]
                if not lines:
                    lines = char_lines
                else:
                    lines = [line + " " + char_line for line, char_line in zip(lines, char_lines)]
            else:
                raise ValueError(f"символ '{char}' не найден в шрифте.")
        return lines

    @classmethod
    def print_static(cls, text: str, color: Color, position: Tuple[int, int], symbol: str = '*'):


        lines = []
        for char in text:
            if char in cls.font:
                char_lines = cls.font[char]
                if not lines:
                    lines = char_lines
                else:
                    lines = [line + " " + char_line for line, char_line in zip(lines, char_lines)]
            else:
                raise ValueError(f"символ '{char}' не найден в шрифте.")

        for i, line in enumerate(lines):
            print(f"\033[{position[1] + i};{position[0]}H{color.value}{line}{Color.RESET.value}", end="\n")

if __name__ == "__main__":
    Printer.font = Printer.load_font("font_5x7.json")

    Printer.print_static("ACCAC", Color.GREEN, (100, 20))
    Printer.print_static("ACCAC", Color.GREEN, (0, 100))
    Printer.print_static("ACC", Color.RED, (200, 22))
    Printer.print_static("ACC", Color.RED, (100, 35))


    Printer.font = Printer.load_font("font_7x7.json")
    with Printer(Color.BLUE, (200, 200)) as printer:
        printer.render("CC")
    printer.print_static("BACC", Color.RED, (20, 20))