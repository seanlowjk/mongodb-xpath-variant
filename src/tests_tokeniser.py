from utils.tokeniser import Tokeniser

tok = Tokeniser("/child::bookstore/descendant::book[position()<3]")
token = tok.peek_next()

while token is not None:
    print(token)
    token = tok.next()
    token = tok.peek_next()

print(tok.buffer)
print()

tok = Tokeniser("/child")
token = tok.peek_next()

while token is not None:
    print(token)
    token = tok.next()
    token = tok.peek_next()

print(tok.buffer)
print()
