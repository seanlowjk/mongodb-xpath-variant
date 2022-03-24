from utils.tokeniser import Tokeniser


class Parser:
    def __init__(self, input):
        self.tokeniser = Tokeniser(input)

    def run(self):
        while self.tokeniser.has_next():
            print(self.tokeniser.next())

