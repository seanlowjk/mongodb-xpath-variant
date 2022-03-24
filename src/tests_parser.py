from utils.parser import Parser

p = Parser('/child::bookstore[child::name = "Sean"]')
p.run() 
