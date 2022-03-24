from utils.constants import XPATH_AXES, STEP_STARTER, STEP_SEPERATOR
from utils.tokeniser import Tokeniser


print(XPATH_AXES)

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

    def next_token(self):
        self.tokeniser.next()

    def eat_string(self):
        return self.tokeniser.next()

    def eat_keyword(self, filter_func):
        token = self.eat_string()
        print(token)

        if token is None or not filter_func(token): 
            return None 
        else:
            return token

    def eat_axis(self):
        return self.eat_keyword(self.lexer.is_axis)

    def eat_backslash(self):
        return self.eat_keyword(self.lexer.is_backslash)   

    def eat_seperator(self):
        return self.eat_keyword(self.lexer.is_seperator)   

    def eat_path(self):
        self.eat_backslash()
        axis = self.eat_axis()
        self.eat_seperator()
        name = self.eat_string()
        print(axis, name)

    def run(self):
        while self.tokeniser.has_next():
            self.eat_path()
            print(1)
