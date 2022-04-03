def evaluate(value, op, value2):
    if op == "=":
        op = "=="

    eval_string = "x {} y".format(op)
    eval_locals = { "x": value, "y": value2 }
    return eval(eval_string, eval_locals)
