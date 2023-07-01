from typing import Optional, Literal, Tuple

from interpreter.lexer.ilexer import ILexer
from interpreter.error_handler.error_handler import ErrorHandler
from interpreter.reader.reader import Reader
from interpreter.token import Token, TokenType

INT_LEN = 39

SingleQuote = Literal["'"]
DoubleQuote = Literal['"']


class Lexer(ILexer):
    keywords = {
        "and": TokenType.AND_OPERATOR,
        "break": TokenType.BREAK,
        "case": TokenType.CASE,
        "continue": TokenType.CONTINUE,
        "default": TokenType.DEFAULT,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE_VAL,
        "fn": TokenType.FN,
        "is": TokenType.EQ_OPERATOR,
        "if": TokenType.IF,
        "let": TokenType.LET,
        "match": TokenType.MATCH,
        "mut": TokenType.MUT,
        "not": TokenType.NOT_OPERATOR,
        "null": TokenType.NULL_VAL,
        "or": TokenType.OR_OPERATOR,
        "true": TokenType.TRUE_VAL,
        "while": TokenType.WHILE,
        "return": TokenType.RETURN,
        "isEven": TokenType.IS_EVEN_OPERATOR,
        "isOdd": TokenType.IS_ODD_OPERATOR,
        "isQuarterO": TokenType.IS_QUARTERO_OPERATOR,
        "isQuarterTw": TokenType.IS_QUARTERTW_OPERATOR,
        "isQuarterTh": TokenType.IS_QUARTERTH_OPERATOR,
        "isQuarterF": TokenType.IS_QUARTERF_OPERATOR,
        "num": TokenType.NUM_TYPE,
        "str": TokenType.STR_TYPE,
        "bool": TokenType.BOOL_TYPE,
    }

    two_char_logical_operators = {
        "==": TokenType.EQ_OPERATOR,
        "!=": TokenType.NOT_EQ_OPERATOR,
        "<=": TokenType.LESS_OR_EQ_OPERATOR,
        ">=": TokenType.GREATER_OR_EQ_OPERATOR,
    }

    one_char_logical_operators = {
        "=": TokenType.ASSIGNMENT_OPERATOR,
        "!": TokenType.NOT_OPERATOR,
        "<": TokenType.LESS_OPERATOR,
        ">": TokenType.GREATER_OPERATOR,
    }

    one_char_arithmetic_operators = {
        "+": TokenType.ADDITION_OPERATOR,
        "-": TokenType.SUBTRACTION_OPERATOR,
        "*": TokenType.MULTIPLICATION_OPERATOR,
        "/": TokenType.DIVISION_OPERATOR,
        "%": TokenType.MODULO_OPERATOR,
        "{": TokenType.LEFT_CURLY_BRACKET,
        "}": TokenType.RIGHT_CURLY_BRACKET,
        "(": TokenType.LEFT_BRACKET,
        ")": TokenType.RIGHT_BRACKET,
        ":": TokenType.COLON,
        ";": TokenType.SEMICOLON,
        ",": TokenType.COMMA,
    }

    escape_chars = {
        "\\\\": "\\",
        "\\'": "'",
        '\\"': '"',
        "\\n": "\n",
        "\\r": "\r",
        "\\t": "\t",
        "\\b": "\b",
        "\\f": "\f",
    }

    def __init__(self, reader: Reader, error_handler: ErrorHandler):
        self._reader = reader
        self._error_handler = error_handler
        self._char = self._next_char()

    def _next_char(self) -> Optional[str]:
        self._char = self._reader.get_char()
        return self._char

    def next_token(self) -> Optional[Token]:
        self._skip_whitespaces()

        return (
            self._build_eof()
            or self._build_div_operator_or_comment()
            or self._build_num()
            or self._build_str()
            or self._build_operator()
            or self._build_keyword_or_identifier()
        )

    def _skip_whitespaces(self):
        while self._char is not None and self._char.isspace():
            self._next_char()

    def _build_num(self):
        if not self._char.isdigit():
            return None
        base = self._build_base()
        position = self._reader.position
        if base is None:
            return None
        value = float(base)
        if self._char == ".":
            self._next_char()
            if self._char.isdigit():
                fraction = self._build_fraction()
                value += fraction
                return Token(TokenType.NUM, position, value)
        return Token(TokenType.NUM, position, value)

    def _build_base(self) -> Optional[int]:
        if int(self._char) == 0:
            if self._next_char() is not None and self._char.isdigit():
                self._error_handler.leading_zero(self._reader.position)
                return None
            return 0

        res = self._build_digit_sequence()
        if res is not None:
            return res[0]
        return None

    def _build_fraction(self) -> float:
        value, radix = self._build_digit_sequence()
        return value / (10**radix)

    def _build_digit_sequence(self) -> Optional[Tuple[int, int]]:
        length = 0
        value = 0
        while self._char is not None and self._char.isdigit():
            value = value * 10 + int(self._char)
            length += 1
            if length > INT_LEN:
                self._error_handler.num_overflow_error(self._reader.position)
                while self._char is not None and self._char.isdigit():
                    self._next_char()
                return None
            self._next_char()
        return value, length

    def _build_div_operator_or_comment(self) -> Optional[Token]:
        if self._char != "/":
            return None
        position = self._reader.position
        self._next_char()
        if self._char != "/" and self._char != "*":
            return Token(TokenType.DIVISION_OPERATOR, position)
        if self._char == "/":
            comment = ""
            while self._next_char() != "\n" and self._char is not None:
                comment += self._char
            return Token(TokenType.ONE_LINE_COMMENT, position, comment)
        if self._char == "*":
            comment = ""
            while not (self._next_char() == "*" and self._reader.read_char() == "/"):
                if self._char is None:
                    self._error_handler.unexpected_end_of_text(position)
                    return None
                comment += self._char
            self._next_char()
            self._next_char()
            return Token(TokenType.MULTILINE_COMMENT, position, comment)

    def _build_str(self) -> Optional[Token]:
        return self._build_str_quote('"') or self._build_str_quote("'")

    def _build_str_quote(self, quote: SingleQuote | DoubleQuote) -> Optional[Token]:
        if self._char == quote:
            position = self._reader.position
            string = self._build_string_quote(quote)
            if string is not None:
                return Token(TokenType.STR, position, string)

    def _build_string_quote(self, quote: SingleQuote | DoubleQuote) -> Optional[str]:
        string = ""
        while self._next_char() != quote:
            if self._char is None:
                self._error_handler.unexpected_end_of_text(self._reader.position)
                return None
            if self._char == "\\":
                next_char = self._reader.read_char()
                if next_char is None:
                    self._error_handler.unexpected_end_of_text(self._reader.position)
                    return None
                escape_char = self.escape_chars.get(self._char + next_char)
                if escape_char is not None:
                    string += escape_char
                    self._next_char()
                else:
                    string += "\\"
            else:
                string += self._char
        self._next_char()
        return string

    def _build_operator(self) -> Optional[Token]:
        position = self._reader.position
        if self._char in self.one_char_logical_operators:
            next_char = self._reader.read_char()
            if next_char is not None:
                operator_type = self.two_char_logical_operators.get(
                    self._char + next_char
                )
                if operator_type is not None:
                    self._next_char()
                    self._next_char()
                    return Token(operator_type, position)
            operator_type = self.one_char_logical_operators[self._char]
            token = Token(operator_type, position)
            self._next_char()
            return token
        operator_type = self.one_char_arithmetic_operators.get(self._char)
        if operator_type is not None:
            token = Token(operator_type, position)
            self._next_char()
            return token

    def _build_keyword_or_identifier(self) -> Optional[Token]:
        if self._char is not None and (self._char.isalpha() or self._char == "_"):
            position = self._reader.position
            buffer = self._char
            while self._next_char() is not None and (
                self._char.isalpha() or self._char.isdigit() or self._char == "_"
            ):
                buffer += self._char
            if buffer in self.keywords:
                return Token(self.keywords[buffer], position)
            return Token(TokenType.IDENTIFIER, position, buffer)

    def _build_eof(self) -> Optional[Token]:
        if self._char is None:
            return Token(TokenType.EOF, self._reader.position)
