from utils.constants import BinaryOperators


class Expression: 
    def __init__(self, path, op, value, value_type):
        self.path = path
        self.op = op 
        self.value = value
        self.value_type = value_type

    def is_unary_expr(self):
        return True 

    def is_or_expr(self):
        return False

    def is_and_expr(self):
        return False

    def __str__(self):
        if self.value_type == int:
            return "{} {} int({})".format(self.path, self.op, self.value)
        else:
            return "{} {} str({})".format(self.path, self.op, self.value)

class BinaryExpression:
    def __init__(self, expr_1, binary_op, expr_2):
        self.expr_1 = expr_1
        self.binary_op = binary_op
        self.expr_2 = expr_2

    def is_unary_expr(self):
        return False 

    def is_or_expr(self):
        return self.binary_op == BinaryOperators.OR.value 

    def is_and_expr(self):
        return self.binary_op == BinaryOperators.AND.value 

    def __str__(self):
        return "{} {} {}".format(self.expr_1, self.binary_op, self.expr_2)
