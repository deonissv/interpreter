from typing import IO, Optional, Literal, List, Tuple
from pathlib import Path

from interpreter.position import Position

NEWLINE_SYMBOLS = Literal[b"\n", b"\r", b"\r\n"]
DEFAULT_NEW_LINE_SYMBOL = "\n"
CODE_LINE_WIDTH = 79


class Reader:
    _file_handler: IO
    _position: int
    _column: int
    _row: int
    _valid_position: bool
    _newline_symbol: Optional[NEWLINE_SYMBOLS]
    _lines: List[int]

    def __init__(self, file_path: str):
        self.path = Path(file_path)
        self._position = 0
        self._column = 1
        self._row = 1
        self._valid_position = False
        self._newline_symbol = None
        self._lines = []

    def get_char(self) -> Optional[str]:
        if not self._valid_position:
            self._file_handler.seek(self._position, 0)
            self._valid_position = True
        char = self._file_handler.read(1)
        if char == b"":
            self._lines.append(self._position)
            return None
        if self._is_new_line(char):
            self._row += 1
            self._column = 1
            if self._newline_symbol == b"\r\n":
                self._position += 2
                self._file_handler.seek(self._position, 0)
            else:
                self._position += 1
            self._lines.append(self._position)
            return DEFAULT_NEW_LINE_SYMBOL
        else:
            self._column += 1
            self._position += 1
            return char.decode()

    def _is_new_line(self, char) -> bool:
        if self._newline_symbol is None:
            return self._find_new_line_symbol(char)
        if self._newline_symbol == b"\n" and char == b"\n":
            return True
        if self._newline_symbol == b"\r" and char == b"\r":
            return True
        if self._newline_symbol == b"\r\n" and char == b"\r":
            if self._file_handler.read(1) == b"\n":
                return True
            else:
                self._file_handler.seek(-1, 1)
                return False
        return False

    def _find_new_line_symbol(self, char) -> bool:
        if char == b"\n":
            self._newline_symbol = b"\n"
            return True
        if char == b"\r":
            if self._file_handler.read(1) == b"\n":
                self._newline_symbol = b"\r\n"
            else:
                self._newline_symbol = b"\r"
                self._file_handler.seek(-1, 1)
            return True
        return False

    def read_char(self) -> Optional[str]:
        self._valid_position = False
        char = self._file_handler.read(1)
        if char == b"":
            return None
        if self._is_new_line(char):
            return DEFAULT_NEW_LINE_SYMBOL
        else:
            return char.decode()

    def get_line_n_offset(self, position: Position) -> Tuple[str, int]:
        self._valid_position = False
        start = (
            self._lines[position.row - 2]
            if position.row > 1 and len(self._lines) > 1
            else 0
        )
        line = ""
        self._file_handler.seek(start)
        if position.row - 1 < len(self._lines):
            offset = self._lines[position.row - 1] - start
            line += self._file_handler.read(offset).decode().strip()
        else:
            char = self._file_handler.read(1)
            while not (char == b"" or self._is_new_line(char)):
                line += char.decode()
                char = self._file_handler.read(1)
        return line, position.position - start

    @property
    def newline_symbol(self) -> Optional[NEWLINE_SYMBOLS]:
        return self._newline_symbol

    @property
    def position(self) -> Position:
        return Position(self._position, self._row, self._column)

    def __iter__(self):
        return self

    def __next__(self):
        char = self.get_char()
        if char is None:
            raise StopIteration
        return char

    def __enter__(self):
        self._file_handler = open(self.path, "rb")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file_handler.close()
