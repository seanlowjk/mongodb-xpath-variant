from utils.parser import Parser

p = Parser('/child::bookstore[child::name = "Sean Low"]')
p.run() 
