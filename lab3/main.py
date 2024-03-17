from enum import Enum, auto

class TokenType(Enum):
    INTEGER = auto()
    FLOAT = auto()
    IDENTIFIER = auto()
    KEYWORD = auto()
    OPERATOR = auto()
    LPAREN = auto()
    RPAREN = auto()
    SEMICOLON = auto()
    EOF = auto()  # End of File/Stream token

# Keywords in our language
KEYWORDS = {'if', 'else', 'return'}
# Operators in our language
OPERATORS = {'+', '-', '*', '/', '>', '<'}

class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def next_token(self):
        if self.pos >= len(self.text):
            return Token(TokenType.EOF)

        current_char = self.text[self.pos]

        # Skip whitespace
        if current_char.isspace():
            self.skip_whitespace()
            return self.next_token()

        # Integer/Float Literals
        if current_char.isdigit():
            return self.number()

        # Identifiers and keywords
        if current_char.isalpha():
            return self.identifier()

        # Operators
        if current_char in OPERATORS:
            self.pos += 1
            return Token(TokenType.OPERATOR, current_char)

        # Parentheses and semicolons
        if current_char == '(':
            self.pos += 1
            return Token(TokenType.LPAREN, '(')
        if current_char == ')':
            self.pos += 1
            return Token(TokenType.RPAREN, ')')
        if current_char == ';':
            self.pos += 1
            return Token(TokenType.SEMICOLON, ';')

        self.error()

    def skip_whitespace(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

    def number(self):
        num_str = ''
        while self.pos < len(self.text) and self.text[self.pos].isdigit():
            num_str += self.text[self.pos]
            self.pos += 1

        if self.pos < len(self.text) and self.text[self.pos] == '.':
            num_str += self.text[self.pos]
            self.pos += 1
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                num_str += self.text[self.pos]
                self.pos += 1
            return Token(TokenType.FLOAT, float(num_str))
        else:
            return Token(TokenType.INTEGER, int(num_str))

    def identifier(self):
        result = ''
        while self.pos < len(self.text) and self.text[self.pos].isalnum():
            result += self.text[self.pos]
            self.pos += 1
        if result in KEYWORDS:
            return Token(TokenType.KEYWORD, result)
        else:
            return Token(TokenType.IDENTIFIER, result)

    def error(self):
        raise Exception(f'Invalid character: {self.text[self.pos]} at position {self.pos}')

    def get_all_tokens(self):
        tokens = []
        while True:
            token = self.next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens


text = "if (y < 50) return x * 10;"
lexer = Lexer(text)
tokens = lexer.get_all_tokens()
print(tokens)


