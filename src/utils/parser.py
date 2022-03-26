from functools import reduce

from objects.expression import BinaryExpression, Expression
from objects.path import Path

from utils.constants import (
    STARTER_COMP_OPERATORS, BINARY_OPERATORS, 
    XPATH_AXES, STEP_STARTER, STEP_SEPERATOR, 
    Operators, Predicate
)
from utils.tokeniser import Tokeniser


class Lexer:
    def is_axis(self, keyword):
        return keyword in XPATH_AXES 

    def is_backslash(self, keyword):
        return keyword == STEP_STARTER

    def is_seperator(self, keyword):
        return keyword == STEP_SEPERATOR

    def is_binary_op(self, keyword):
        return keyword in BINARY_OPERATORS


class Parser:
    def __init__(self, input):
        self.tokeniser = Tokeniser(input)
        self.lexer = Lexer()
        self.curr_path = ""

    def peek_token(self):
        """
        Peeks the next token from the tokeniser.

        Returns the token as a string. 
        """
        return self.tokeniser.peek_next()

    def eat_token(self):
        """
        Eats the next token from the tokeniser. 

        Returns the token as a string. 
        """
        return self.tokeniser.next()

    def eat_keyword(self, filter_func):
        """
        Eats a keyword based on a filter function. 

        If the filter function evaluations to true, the 
        keyword will be returned as a string. 
        """
        token = self.peek_token()

        if token is None or not filter_func(token): 
            return None 
        else:
            return self.eat_token()

    def eat_alnum(self):
        """
        Eats a keyword as long as it is alphanumeric. 

        Returns the token as a string. 
        """
        return self.eat_keyword(lambda a : a.isalnum())

    def eat_axis(self):
        """
        Eats a keyword as long as it is in the form 
        of an XPath axes. 

        Returns the token as a string. 
        """
        return self.eat_keyword(self.lexer.is_axis)

    def eat_backslash(self):
        """
        Eats a keyword as long as it is a backslash. 

        Returns the token as a string. 
        """
        return self.eat_keyword(self.lexer.is_backslash)   

    def eat_seperator(self):
        """
        Eats a keyword as long as it is a double colon (::). 

        Returns the token as a string. 
        """
        return self.eat_keyword(self.lexer.is_seperator)   

    def eat_path(self, has_backslash=True):
        """
        Eats a path as long as it is in the correct long-form format. 

        Returns the path as an object.
        Refer to objects/path.py
        """
        if has_backslash:
            backslash = self.eat_backslash()
        else: 
            backslash = "/"
            
        axis = self.eat_axis()
        sepeator = self.eat_seperator()
        name = self.eat_token()
        
        is_syntax_correct = reduce(lambda a, b: a and b is not None, [backslash, axis, sepeator, name])
        if not is_syntax_correct:
            return None 

        output_path = axis + "::" + name
        if has_backslash:
            self.curr_path = self.curr_path + "/" + output_path

        return Path(output_path)

    def eat_op(self):
        """
        Eats a keyword so long as it is a binary operator 
        for example: <=, <, !=, =, >, >=

        Returns the operation as a string. 
        """
        tok = self.eat_token()
        if not tok in STARTER_COMP_OPERATORS:
            return None 

        if tok == '<':
            tok2 = self.peek_token()
            if tok2 == '=':
                self.eat_token()
                return Operators.LE.value
            elif tok2.isalnum() or tok2 == '"' or tok2 == "'":
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
        """
        Eats a keyword so long as it is a value 

        Returns the value as a tuple:
            the first element contains the value 
            the second element contains the type of the value 
                (str or int)
        """
        tok = self.peek_token()
        if tok == '"':
            self.eat_token()
            val = ""
            while True: 
                word = self.peek_token()
                if word == '"':
                    break 
                val = val + self.eat_token() + " "
            end_tok = self.eat_keyword(lambda a: a == '"')
            if end_tok is None:
                return None, None
            else: 
                return val.strip(), str
        elif tok == "'":
            val = ""
            self.eat_token()
            while True: 
                word = self.peek_token()
                if word == "'":
                    break 
                val = val + self.eat_token() + " "
            end_tok = self.eat_keyword(lambda a: a == "'")
            if end_tok is None:
                return  None, None 
            else: 
                return val.strip(), str
        elif tok.isnumeric():
            return self.eat_alnum(), int
        else:
            return  None, None
            
    def eat_expression(self):
        """
        Eats an expression in the form of (path op value)

        Returns the expression as an object 
        Refer to objects/expression.py
        """
        path = self.eat_path(False)
        op = self.eat_op()
        val, val_type = self.eat_value() 
        return Expression(path, op, val, val_type)

    def eat_binary_expression(self, prev_expr=None, prev_bin_op=None):
        """
        Eats an expression in the form of (path op value) and (path op value)
            OR (path op value) or (path op value)

        Returns the expression as an object 
        Refer to objects/expression.py
        """
        expr = self.eat_expression()
        next = self.peek_token()
        if next == Predicate.RIGHT_BRACKET.value:
            self.eat_keyword(lambda a : a == Predicate.RIGHT_BRACKET.value)
            if prev_expr is None:
                return expr 
            else:
                return BinaryExpression(prev_expr, prev_bin_op, expr)
        elif self.lexer.is_binary_op(next):
            if not prev_expr is None:
                binary_expr = BinaryExpression(prev_expr, prev_bin_op, expr)
            else:
                binary_expr = expr
            return self.eat_binary_expression(binary_expr, self.eat_token())
        else:
            return None

    def eat_predicate(self):
        """
        Eats a predicate in the form of [ expr* ]

        Returns the predicate in the form of an expression
        """
        left_brac = self.eat_keyword(lambda a : a == Predicate.LEFT_BRACKET.value)

        if left_brac is None:
            return None 

        return self.eat_binary_expression()
        
    def run(self):
        """
        Returns the paths and expressions in the form of two lists:
            1. List of Levels 
            2. List of Expressions 
        """
        paths = []
        expressions = []
        while self.tokeniser.has_next():
            tok = self.peek_token()
            if tok == STEP_STARTER:
                path = self.eat_path()
                paths.append(path)
            elif tok == Predicate.LEFT_BRACKET.value:
                expr = self.eat_predicate()
                expressions.append(expr)
            else:
                print(tok)

        return paths, expressions

            

