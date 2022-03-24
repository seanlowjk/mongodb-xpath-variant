class Expression: 
    def __init__(self, path, op, value):
        self.path = path
        self.op = op 
        self.value = value

class BinaryExpression:
    def __init__(self, expr_1, binary_op, expr_2):
        self.expr_1 = expr_1
        self.binary_op = binary_op
        self.expr_2 = expr_2
