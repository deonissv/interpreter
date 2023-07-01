from interpreter.error_handler import Error
from interpreter.reader.reader import Reader


class ErrorFormatter:
    def __init__(self, reader: Reader):
        self._reader = reader

    def get_error_msg(self, error: Error):
        line, offset = self._reader.get_line_n_offset(error.position)
        msg_offset = len(str(error.position.row)) + 2
        error_msg = f"{error.msg}\n"
        error_msg += f'{" " * msg_offset}|\n'
        error_msg += f" {error.position.row} | {line}\n"
        error_msg += f'{" " * msg_offset}|{" " * offset}^^^\n'
        return error_msg
