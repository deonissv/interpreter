import argparse
import sys
from pathlib import Path

from interpreter.comments_filter import CommentsFilter
from interpreter.error_formatter import ErrorFormatter
from interpreter.error_handler import ErrorHandler, CriticalError
from interpreter.interpreter.interpreter import Interpreter
from interpreter.lexer import Lexer
from interpreter.parser import Parser
from interpreter.reader import Reader

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    if len(sys.argv) == 1:
        print("Usage: python -m interpreter <source>")
        sys.exit(1)
    args = parser.parse_args()

    path = Path(args.filename)
    if not path.is_file():
        print(f"Unable to resolve the path: {args.filename}")
        exit(0)

    with Reader(f"{path}") as reader:
        error_handler = ErrorHandler()
        error_formatter = ErrorFormatter(reader)

        lexer = Lexer(reader, error_handler)
        parser = Parser(CommentsFilter(lexer), error_handler)
        program = parser.parse()

        if len(error_handler.errors) > 0:
            for error in error_handler.errors:
                msg = error_formatter.get_error_msg(error)
                print(msg)
                exit(0)

        interpreter = Interpreter(error_handler)
        try:
            program.accept(interpreter)
        except CriticalError as error:
            msg = error_formatter.get_error_msg(error)
            print(msg)
            exit(0)
