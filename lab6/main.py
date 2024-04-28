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
        return f"Token({self.type}, {repr(self.value)})"

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

# AST Node Classes
class ASTNode:
    pass

class BinaryOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op  # Token (operator type and value)
        self.right = right

    def __repr__(self):
        return f"BinaryOpNode({self.left}, {self.op.value}, {self.right})"

class NumNode(ASTNode):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"NumNode({self.value})"

class VarNode(ASTNode):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"VarNode({self.value})"

class IfNode(ASTNode):
    def __init__(self, condition, true_block, false_block=None):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block

    def __repr__(self):
        return f"IfNode({self.condition}, {self.true_block}, {self.false_block})"

class BlockNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"BlockNode({self.statements})"

class ReturnNode(ASTNode):
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"ReturnNode({self.expression})"

# Parser Class
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]

    def error(self):
        raise Exception("Invalid syntax")

    def advance(self):
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None  # No more tokens

    def eat(self, token_type):
        if self.current_token.type == token_type:
            print(f"Consuming: {self.current_token}")  # Debug output
            self.advance()
        else:
            print(f"Error: Expected {token_type}, but got {self.current_token}")  # Debug output
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == TokenType.INTEGER or token.type == TokenType.FLOAT:
            self.eat(token.type)
            return NumNode(token)
        elif token.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            return VarNode(token)
        else:
            self.error()

    def term(self):
        node = self.factor()
        while self.current_token and self.current_token.type == TokenType.OPERATOR and self.current_token.value in ('*', '/'):
            token = self.current_token
            self.eat(TokenType.OPERATOR)
            node = BinaryOpNode(node, token, self.factor())
        return node

    def expr(self):
        node = self.term()
        while self.current_token and (
                self.current_token.type == TokenType.OPERATOR and self.current_token.value in ('+', '-', '>', '<')):
            token = self.current_token
            self.eat(TokenType.OPERATOR)
            node = BinaryOpNode(node, token, self.term())
        return node

    def statement(self):
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'return':
            self.eat(TokenType.KEYWORD)
            expr = self.expr()
            self.eat(TokenType.SEMICOLON)
            return ReturnNode(expr)
        elif self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'if':
            self.eat(TokenType.KEYWORD)
            self.eat(TokenType.LPAREN)
            condition = self.expr()  # Parse condition which might include operators like '>'
            self.eat(TokenType.RPAREN)
            if self.current_token and self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'return':
                true_block = self.statement()
                false_block = None
                if self.current_token and self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'else':
                    self.eat(TokenType.KEYWORD)
                    false_block = self.statement()
                return IfNode(condition, true_block, false_block)
            else:
                self.error()  # Debug here to find what token is causing the issue
        else:
            self.error()

    def parse(self):
        ast = self.statement()
        if self.current_token.type != TokenType.EOF:
            self.error()
        return ast

    def parse_block_or_single_statement(self):
        # Simple version: assuming next non-block statement is a single return statement.
        return self.statement()

# Example usage
text = "if (x > 50) return x * 10;"
lexer = Lexer(text)
tokens = lexer.get_all_tokens()
parser = Parser(tokens)
ast = parser.parse()
print(ast)
