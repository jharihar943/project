"""
Lexical Analyzer (Lexer) for Multi-Language Compiler
Performs tokenization with AI-enhanced error detection
"""

import re
from enum import Enum, auto
from typing import List, Tuple, Optional
import difflib

class TokenType(Enum):
    # Keywords
    KEYWORD = auto()
    # Identifiers and literals
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    # Operators
    OPERATOR = auto()
    # Delimiters
    DELIMITER = auto()
    # Special
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()
    EOF = auto()
    # Error
    ERROR = auto()

class Token:
    def __init__(self, type: TokenType, value: str, line: int, column: int):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}', {self.line}:{self.column})"

class Lexer:
    """AI-Enhanced Lexical Analyzer"""
    
    # Language-specific keywords
    KEYWORDS = {
        'python': [
            'def', 'class', 'if', 'elif', 'else', 'while', 'for', 'in',
            'return', 'import', 'from', 'as', 'try', 'except', 'finally',
            'with', 'lambda', 'pass', 'break', 'continue', 'and', 'or', 'not',
            'True', 'False', 'None', 'print'
        ],
        'java': [
            'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch',
            'char', 'class', 'const', 'continue', 'default', 'do', 'double',
            'else', 'enum', 'extends', 'final', 'finally', 'float', 'for',
            'if', 'implements', 'import', 'instanceof', 'int', 'interface',
            'long', 'native', 'new', 'package', 'private', 'protected', 'public',
            'return', 'short', 'static', 'strictfp', 'super', 'switch',
            'synchronized', 'this', 'throw', 'throws', 'transient', 'try',
            'void', 'volatile', 'while', 'true', 'false', 'null'
        ]
    }
    
    # Built-in functions and types (should not be flagged as typos)
    BUILT_INS = {
        'python': [
            'int', 'str', 'float', 'bool', 'list', 'dict', 'tuple', 'set',
            'input', 'print', 'len', 'range', 'type', 'isinstance', 'abs',
            'sum', 'min', 'max', 'round', 'sorted', 'reversed', 'enumerate',
            'zip', 'map', 'filter', 'all', 'any', 'open', 'file'
        ],
        'java': [
            'String', 'System', 'Scanner', 'ArrayList', 'HashMap', 'Integer',
            'Double', 'Boolean', 'Math', 'Object', 'Exception', 'println',
            'print', 'length', 'size', 'add', 'remove', 'get', 'set', 'equals',
            'toString', 'indexOf', 'substring', 'charAt', 'split', 'trim'
        ],
        'javascript': [
            'function', 'var', 'let', 'const', 'if', 'else', 'while', 'for',
            'return', 'class', 'new', 'this', 'typeof', 'instanceof',
            'try', 'catch', 'finally', 'throw', 'async', 'await',
            'true', 'false', 'null', 'undefined', 'console'
        ],
        'cpp': [
            'int', 'float', 'double', 'char', 'bool', 'void', 'string',
            'if', 'else', 'while', 'for', 'return', 'class', 'struct',
            'public', 'private', 'protected', 'namespace', 'using',
            'include', 'cout', 'cin', 'endl', 'true', 'false'
        ]
    }
    
    def __init__(self, source_code: str, language: str = 'python'):
        self.source = source_code
        self.language = language.lower()
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        self.errors: List[dict] = []
        
    def tokenize(self) -> Tuple[List[Token], List[dict]]:
        """Tokenize source code with AI-enhanced error detection"""
        while self.position < len(self.source):
            self._skip_whitespace()
            
            if self.position >= len(self.source):
                break
                
            # Skip comments
            if self._check_comment():
                continue
            
            # Try to match tokens
            if not self._match_token():
                # AI-enhanced error handling
                error_char = self.source[self.position]
                suggestion = self._get_ai_suggestion(error_char)
                
                self.errors.append({
                    'line': self.line,
                    'column': self.column,
                    'message': f"Unexpected character: '{error_char}'",
                    'suggestion': suggestion,
                    'severity': 'error'
                })
                
                self.tokens.append(Token(TokenType.ERROR, error_char, self.line, self.column))
                self._advance()
        
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens, self.errors
    
    def _match_token(self) -> bool:
        """Try to match various token types"""
        # Numbers
        if self._current_char().isdigit():
            self._read_number()
            return True
        
        # Strings
        if self._current_char() in '"\'':
            self._read_string()
            return True
        
        # Identifiers and keywords
        if self._current_char().isalpha() or self._current_char() == '_':
            self._read_identifier()
            return True
        
        # Operators and delimiters
        if self._match_operator():
            return True
        
        return False
    
    def _read_number(self):
        """Read numeric literals"""
        start_pos = self.position
        start_col = self.column
        
        while self.position < len(self.source) and (
            self._current_char().isdigit() or self._current_char() == '.'
        ):
            self._advance()
        
        value = self.source[start_pos:self.position]
        self.tokens.append(Token(TokenType.NUMBER, value, self.line, start_col))
    
    def _read_string(self):
        """Read string literals"""
        quote = self._current_char()
        start_col = self.column
        self._advance()  # Skip opening quote
        
        start_pos = self.position
        while self.position < len(self.source) and self._current_char() != quote:
            if self._current_char() == '\\':
                self._advance()  # Skip escape character
            self._advance()
        
        value = self.source[start_pos:self.position]
        
        if self.position < len(self.source):
            self._advance()  # Skip closing quote
            self.tokens.append(Token(TokenType.STRING, value, self.line, start_col))
        else:
            self.errors.append({
                'line': self.line,
                'column': start_col,
                'message': 'Unterminated string literal',
                'suggestion': f'Add closing {quote} at the end of the string',
                'severity': 'error'
            })
    
    def _read_identifier(self):
        """Read identifiers and keywords"""
        start_pos = self.position
        start_col = self.column
        
        while self.position < len(self.source) and (
            self._current_char().isalnum() or self._current_char() == '_'
        ):
            self._advance()
        
        value = self.source[start_pos:self.position]
        
        # Check if it's a keyword with AI-enhanced typo detection
        keywords = self.KEYWORDS.get(self.language, [])
        built_ins = self.BUILT_INS.get(self.language, [])
        
        if value in keywords:
            token_type = TokenType.KEYWORD
        else:
            # Check for typos in keywords (but ignore built-in functions)
            if value not in built_ins:
                close_matches = difflib.get_close_matches(value, keywords, n=1, cutoff=0.8)
                if close_matches:
                    self.errors.append({
                        'line': self.line,
                        'column': start_col,
                        'message': f"Possible typo: '{value}'",
                        'suggestion': f"Did you mean '{close_matches[0]}'?",
                        'severity': 'warning'
                    })
            token_type = TokenType.IDENTIFIER
        
        self.tokens.append(Token(token_type, value, self.line, start_col))
    
    def _match_operator(self) -> bool:
        """Match operators and delimiters"""
        operators = ['==', '!=', '<=', '>=', '&&', '||', '++', '--', '+=', '-=', '*=', '/=',
                    '+', '-', '*', '/', '%', '=', '<', '>', '!', '&', '|', '^', '~']
        delimiters = ['(', ')', '{', '}', '[', ']', ';', ',', '.', ':']
        
        start_col = self.column
        
        # Try two-character operators first
        if self.position + 1 < len(self.source):
            two_char = self.source[self.position:self.position + 2]
            if two_char in operators:
                self.tokens.append(Token(TokenType.OPERATOR, two_char, self.line, start_col))
                self._advance()
                self._advance()
                return True
        
        # Single character operators and delimiters
        char = self._current_char()
        if char in operators:
            self.tokens.append(Token(TokenType.OPERATOR, char, self.line, start_col))
            self._advance()
            return True
        elif char in delimiters:
            self.tokens.append(Token(TokenType.DELIMITER, char, self.line, start_col))
            self._advance()
            return True
        
        return False
    
    def _check_comment(self) -> bool:
        """Skip comments based on language"""
        if self.language == 'python' and self._current_char() == '#':
            while self.position < len(self.source) and self._current_char() != '\n':
                self._advance()
            return True
        
        if self.language in ['javascript', 'cpp']:
            if self.position + 1 < len(self.source):
                if self.source[self.position:self.position + 2] == '//':
                    while self.position < len(self.source) and self._current_char() != '\n':
                        self._advance()
                    return True
        
        return False
    
    def _skip_whitespace(self):
        """Skip whitespace characters"""
        while self.position < len(self.source) and self._current_char() in ' \t\r\n':
            if self._current_char() == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1
    
    def _current_char(self) -> str:
        """Get current character"""
        if self.position >= len(self.source):
            return '\0'
        return self.source[self.position]
    
    def _advance(self):
        """Move to next character"""
        if self.position < len(self.source):
            if self.source[self.position] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1
    
    def _get_ai_suggestion(self, error_char: str) -> str:
        """AI-based suggestion for unexpected characters"""
        suggestions = {
            '@': 'Did you mean to use a decorator? Use @ at the start of a line',
            '$': 'Use variables without $. Try removing $',
            '%': 'Use % for modulo operation or string formatting',
            '`': 'Use single \' or double " quotes for strings',
        }
        return suggestions.get(error_char, 'Check for typos or invalid syntax')
