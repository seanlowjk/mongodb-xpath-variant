from tokenize import String


class Tokeniser:
    def __init__(self, input) -> None:
        self.input = input
        self.ptr = 0
        self.buffer = list()

    # consumes the token
    def next(self):
        if self.ptr >= len(self.input):
            return None

        if len(self.buffer) > 0:
            token = self.buffer.pop(0)
            return token

        if self.input[self.ptr].isspace():
            self.cleanSpace()

        if self.input[self.ptr].isalnum():
            return self.nextAlNum()
        else:
            return self.nextSymbol()

    def has_next(self):
        return not self.peek_next() is None

    # peeks what is the next string, doesnt consume
    def peek_next(self) -> String:
        if self.ptr >= len(self.input):
            return None

        if len(self.buffer) != 0:
            return self.buffer[0]

        if self.input[self.ptr].isspace():
            self.cleanSpace()

        if self.input[self.ptr].isalnum():
            token = self.nextAlNum()
            self.buffer.append(token)

            return token
        else:
            token = self.nextSymbol()
            self.buffer.append(token)

            return token

    def cleanSpace(self) -> None:
        while self.ptr < len(self.input) and self.input[self.ptr].isspace():
            self.ptr += 1

    def nextAlNum(self) -> String:
        tokens = list()
        while self.ptr < len(self.input) and self.input[self.ptr].isalnum():
            tokens.append(self.input[self.ptr])
            self.ptr += 1

        return "".join(tokens)

    def nextSymbol(self) -> String:
        tokens = list()
        tokens.append(self.input[self.ptr])
        self.ptr += 1

        if tokens[0] == "/" or tokens[0] == ":":
            next_tok = self.input[self.ptr]
            if tokens[0] == next_tok:
                tokens.append(next_tok)
                self.ptr += 1

        return "".join(tokens)
