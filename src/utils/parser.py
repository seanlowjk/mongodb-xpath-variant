from functools import reduce
from objects.expression import Expression

from objects.path import Path 
from utils.constants import STARTER_COMP_OPERATORS, XPATH_AXES, STEP_STARTER, STEP_SEPERATOR, Operators, Predicate
from utils.tokeniser import Tokeniser


class Lexer:
    def is_axis(self, keyword):
        return keyword in XPATH_AXES 

    def is_backslash(self, keyword):
        return keyword == STEP_STARTER

    def is_seperator(self, keyword):
        return keyword == STEP_SEPERATOR


class Parser:
    def __init__(self, input):
        self.tokeniser = Tokeniser(input)
        self.lexer = Lexer()

    def peek_token(self):
        self.tokeniser.peek_next()

    def eat_token(self):
        return self.tokeniser.next()

    def eat_keyword(self, filter_func):
        token = self.peek_token()

        if token is None or not filter_func(token): 
            return None 
        else:
            return self.eat_token()

    def eat_alnum(self):
        return self.eat_keyword(lambda a : a.isalnum())

    def eat_axis(self):
        return self.eat_keyword(self.lexer.is_axis)

    def eat_backslash(self):
        return self.eat_keyword(self.lexer.is_backslash)   

    def eat_seperator(self):
        return self.eat_keyword(self.lexer.is_seperator)   

    def eat_path(self):
        backslash = self.eat_backslash()
        axis = self.eat_axis()
        sepeator = self.eat_seperator()
        name = self.eat_token()
        
        is_syntax_correct = reduce(lambda a, b: a and b is not None, [backslash, axis, sepeator, name])
        if not is_syntax_correct:
            return None 

        return Path(axis, name)

    def eat_op(self):
        tok = self.eat_token()
        if not tok in STARTER_COMP_OPERATORS:
            return None 

        if tok == '<':
            tok2 = self.peek_token()
            if tok2 == '=':
                self.eat_token()
                return Operators.LE.value
            elif tok2.isalnum() or tok2 == '"' or tok2 == "'":
                self.eat_token()
                return Operators.LT.value 
            else:
                return None
        elif tok == '>':
            tok2 = self.peek_token()
            if tok2 == '=':
                self.eat_token()
                return Operators.GE.value
            elif tok2.isalnum() or tok2 == '"' or tok2 == "'":
                return Operators.GT.value 
            else:
                return None
        elif tok == '!':
            tok2 = self.peek_token()
            if tok2 == '=':
                self.eat_token()
                return Operators.NE.value
            else:
                return None
        elif tok == '=':
            return Operators.EQ.value 
        else:
            return None 

    def eat_value(self):
        tok = self.peek_token()
        if tok == '"':
            word = self.eat_alnum()
            end_tok = self.eat_keyword(lambda a: a == '"')
            if word is None or end_tok is None:
                return None 
            else: 
                return word 
        elif tok == "'":
            word = self.eat_alnum()
            end_tok = self.eat_keyword(lambda a: a == "'")
            if word is None or end_tok is None:
                return None 
            else: 
                return word 
        elif tok.isalnum():
            return self.eat_alnum()
        else:
            return None
            
    def eat_expression(self):
        path = self.eat_path()
        op = self.eat_op()
        val = self.eat_value()
        return Expression(path, op, val)

    def eat_predicate(self):
        left_brac = self.eat_keyword(lambda a : a == Predicate.LEFT_BRACKET)
        expr = self.eat_expression() 
        right_brac = self.eat_keyword(lambda a : a == Predicate.RIGHT_BRACKET)

        is_syntax_correct = reduce(lambda a, b: a and b is not None, [left_brac, expr, right_brac])
        if not is_syntax_correct:
            return None 

        return expr
        
    def run(self):
        while self.tokeniser.has_next():
            tok = self.eat_token()
            print(tok)
