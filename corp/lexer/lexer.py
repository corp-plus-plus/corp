"""
Corp++ Lexer / Tokenizer.
Tokenizes source code into high-bandwidth corporate tokens.
"""

from typing import List, Optional
from .tokens import Token, TokenType, KEYWORDS
from corp.telemetry.corporate_error import CorpSyntaxError


class Lexer:
    def __init__(self, source_code: str, file_path: Optional[str] = None):
        self.source_code = source_code
        self.file_path = file_path or "<corporate_memo.corp>"
        self.length = len(source_code)
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []

    def peek(self, offset: int = 0) -> str:
        idx = self.pos + offset
        if idx >= self.length:
            return '\0'
        return self.source_code[idx]

    def advance(self) -> str:
        if self.pos >= self.length:
            return '\0'
        char = self.source_code[self.pos]
        self.pos += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char

    def match(self, expected: str) -> bool:
        if self.pos >= self.length or self.source_code[self.pos] != expected:
            return False
        self.advance()
        return True

    def tokenize(self) -> List[Token]:
        while self.pos < self.length:
            char = self.peek()

            # Skip whitespace
            if char in ' \t\r\n':
                self.advance()
                continue

            # Corporate comments: //, FYI:, NOTE:
            if char == '/' and self.peek(1) == '/':
                while self.peek() not in ('\n', '\0'):
                    self.advance()
                continue

            # Block comments: /* ... */
            if char == '/' and self.peek(1) == '*':
                self.advance() # /
                self.advance() # *
                start_line = self.line
                start_col = self.column
                while not (self.peek() == '*' and self.peek(1) == '/') and self.peek() != '\0':
                    self.advance()
                if self.peek() == '\0':
                    raise CorpSyntaxError(
                        "Unclosed corporate confidential block comment. Expected '*/'.",
                        line=start_line,
                        column=start_col,
                        source_code=self.source_code,
                        file_path=self.file_path
                    )
                self.advance() # *
                self.advance() # /
                continue

            # Numbers (integers, floats, underscore separators)
            if char.isdigit():
                self.scan_number()
                continue

            # String literals
            if char in ('"', "'"):
                # Check if this might be let's_take_this_offline or just a string
                # If preceded by identifier chars it wouldn't reach here since scan_identifier handles it.
                self.scan_string(char)
                continue

            # Identifiers and keywords (including let's_take_this_offline)
            if char.isalpha() or char == '_':
                self.scan_identifier_or_keyword()
                continue

            # Single or multi-character symbols
            start_line = self.line
            start_col = self.column
            self.advance()

            if char == '+':
                self.tokens.append(Token(TokenType.PLUS, '+', start_line, start_col, '+'))
            elif char == '-':
                self.tokens.append(Token(TokenType.MINUS, '-', start_line, start_col, '-'))
            elif char == '*':
                self.tokens.append(Token(TokenType.MULTIPLY, '*', start_line, start_col, '*'))
            elif char == '/':
                self.tokens.append(Token(TokenType.DIVIDE, '/', start_line, start_col, '/'))
            elif char == '%':
                self.tokens.append(Token(TokenType.MODULO, '%', start_line, start_col, '%'))
            elif char == '=':
                if self.match('='):
                    self.tokens.append(Token(TokenType.EQUAL, '==', start_line, start_col, '=='))
                else:
                    self.tokens.append(Token(TokenType.ASSIGN, '=', start_line, start_col, '='))
            elif char == '!':
                if self.match('='):
                    self.tokens.append(Token(TokenType.NOT_EQUAL, '!=', start_line, start_col, '!='))
                else:
                    self.tokens.append(Token(TokenType.NOT, '!', start_line, start_col, '!'))
            elif char == '<':
                if self.match('='):
                    self.tokens.append(Token(TokenType.LESS_EQUAL, '<=', start_line, start_col, '<='))
                else:
                    self.tokens.append(Token(TokenType.LESS_THAN, '<', start_line, start_col, '<'))
            elif char == '>':
                if self.match('='):
                    self.tokens.append(Token(TokenType.GREATER_EQUAL, '>=', start_line, start_col, '>='))
                else:
                    self.tokens.append(Token(TokenType.GREATER_THAN, '>', start_line, start_col, '>'))
            elif char == '&':
                if self.match('&'):
                    self.tokens.append(Token(TokenType.AND, '&&', start_line, start_col, '&&'))
                else:
                    raise CorpSyntaxError(
                        f"Unexpected character '&'. Did you mean '&&' or 'synergizes_with'?",
                        line=start_line, column=start_col,
                        source_code=self.source_code, file_path=self.file_path
                    )
            elif char == '|':
                if self.match('|'):
                    self.tokens.append(Token(TokenType.OR, '||', start_line, start_col, '||'))
                else:
                    raise CorpSyntaxError(
                        f"Unexpected character '|'. Did you mean '||' or 'or'?",
                        line=start_line, column=start_col,
                        source_code=self.source_code, file_path=self.file_path
                    )
            elif char == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', start_line, start_col, '('))
            elif char == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', start_line, start_col, ')'))
            elif char == '{':
                self.tokens.append(Token(TokenType.LBRACE, '{', start_line, start_col, '{'))
            elif char == '}':
                self.tokens.append(Token(TokenType.RBRACE, '}', start_line, start_col, '}'))
            elif char == '[':
                self.tokens.append(Token(TokenType.LBRACKET, '[', start_line, start_col, '['))
            elif char == ']':
                self.tokens.append(Token(TokenType.RBRACKET, ']', start_line, start_col, ']'))
            elif char == ',':
                self.tokens.append(Token(TokenType.COMMA, ',', start_line, start_col, ','))
            elif char == '.':
                self.tokens.append(Token(TokenType.DOT, '.', start_line, start_col, '.'))
            elif char == ':':
                self.tokens.append(Token(TokenType.COLON, ':', start_line, start_col, ':'))
            elif char == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, ';', start_line, start_col, ';'))
            else:
                raise CorpSyntaxError(
                    f"Unrecognized corporate glyph '{char}'. Not aligned with company guidelines.",
                    line=start_line, column=start_col,
                    source_code=self.source_code, file_path=self.file_path
                )

        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column, ''))
        return self.tokens

    def scan_number(self):
        start_line = self.line
        start_col = self.column
        num_str = ""
        is_float = False

        while self.peek().isdigit() or self.peek() == '_':
            char = self.advance()
            if char != '_':
                num_str += char

        if self.peek() == '.' and self.peek(1).isdigit():
            is_float = True
            num_str += self.advance()  # consume '.'
            while self.peek().isdigit() or self.peek() == '_':
                char = self.advance()
                if char != '_':
                    num_str += char

        val = float(num_str) if is_float else int(num_str)
        self.tokens.append(Token(TokenType.NUMBER, val, start_line, start_col, num_str))

    def scan_string(self, quote: str):
        start_line = self.line
        start_col = self.column
        self.advance()  # opening quote
        result = []

        while self.peek() != quote and self.peek() != '\0':
            if self.peek() == '\\':
                self.advance()  # backslash
                esc = self.advance()
                if esc == 'n':
                    result.append('\n')
                elif esc == 't':
                    result.append('\t')
                elif esc == 'r':
                    result.append('\r')
                elif esc == '\\':
                    result.append('\\')
                elif esc == quote:
                    result.append(quote)
                else:
                    result.append(esc)
            else:
                result.append(self.advance())

        if self.peek() == '\0':
            raise CorpSyntaxError(
                "Unterminated string literal in corporate memo.",
                line=start_line, column=start_col,
                source_code=self.source_code, file_path=self.file_path
            )

        self.advance()  # closing quote
        str_val = "".join(result)
        self.tokens.append(Token(TokenType.STRING, str_val, start_line, start_col, str_val))

    def scan_identifier_or_keyword(self):
        start_line = self.line
        start_col = self.column
        chars = []

        while True:
            c = self.peek()
            # Allow letters, digits, underscores, and single quotes if part of let's_take_this_offline
            if c.isalnum() or c == '_':
                chars.append(self.advance())
            elif c == "'" and (self.peek(1).isalnum() or self.peek(1) == '_'):
                chars.append(self.advance())
            else:
                break

        ident = "".join(chars)

        # Check for corporate comment triggers like "FYI:" or "NOTE:"
        if ident in ("FYI", "NOTE") and self.peek() == ':':
            self.advance()  # consume ':'
            while self.peek() not in ('\n', '\0'):
                self.advance()
            return

        # Check keyword map
        token_type = KEYWORDS.get(ident)
        if token_type is not None:
            if token_type == TokenType.ALIGNED:
                self.tokens.append(Token(TokenType.ALIGNED, True, start_line, start_col, ident))
            elif token_type == TokenType.MISALIGNED:
                self.tokens.append(Token(TokenType.MISALIGNED, False, start_line, start_col, ident))
            elif token_type == TokenType.OUT_OF_OFFICE:
                self.tokens.append(Token(TokenType.OUT_OF_OFFICE, None, start_line, start_col, ident))
            elif token_type == TokenType.UNASSIGNED:
                self.tokens.append(Token(TokenType.UNASSIGNED, None, start_line, start_col, ident))
            else:
                self.tokens.append(Token(token_type, ident, start_line, start_col, ident))
        else:
            self.tokens.append(Token(TokenType.IDENTIFIER, ident, start_line, start_col, ident))
