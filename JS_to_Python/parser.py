import json

FALSE = {"type": "bool", "value": False}
def parse(input):
    PRECEDENCE = {
        "=": 1,
        "||": 2,
        "&&": 3,
        "<": 7, ">": 7, "<=": 7, ">=": 7, "==": 7, "!=": 7,
        "+": 10, "-": 10,
        "*": 20, "/": 20, "%": 20,
    }
    return parse_toplevel()
    def is_punc(ch):
        tok = input.peek()
        return tok and tok.type == "punc" and (not ch or tok.value == ch) and tok
    def is_kw(kw):
        tok = input.peek()
        return tok and tok.type == "kw" and (not kw or tok.value == kw) and tok
    def is_op(op):
        tok = input.peek()
        return tok and tok.type == "op" and (not op or tok.value == op) and tok
    def skip_punc(ch):
        if (is_punc(ch)):
            input.next()
        else:
            input.croak("Expecting punctuation: \"" + ch + "\"")
    def skip_kw(kw):
        if (is_kw(kw)):
            input.next()
        else:
            input.croak("Expecting keyword: \"" + kw + "\"")
    def skip_op(op):
        if (is_op(op)):
            input.next()
        else:
            input.croak("Expecting operator: \"" + op + "\"")
    def unexpected():
        input.croak("Unexpected token: " + json.dumbs(input.peek()))
    def maybe_binary(left, my_prec):
        tok = is_op()
        if (tok):
            his_prec = PRECEDENCE[tok.value]
            if (his_prec > my_prec):
                input.next()
                return maybe_binary({
                    "type": "assign" if tok.value == "=" else "binary",
                    "operator": tok.value,
                    "left": left,
                    "right": maybe_binary(parse_atom(), his_prec)
                }, my_prec)
        return left
    def delimited(start, stop, separator, parser):
        a = []
        first = True
        skip_punc(start)
        while (not input.eof()):
            if (is_punc(stop)):
                break
            if (first):
                first = False
            else:
                skip_punc(separator)
            if (is_punc(stop)):
                break
            a.push(parser())
        skip_punc(stop)
        return a
    def parse_call(func):
        return {
            "type": "call",
            "func": func,
            "args": delimited("(", ")", ",", parse_expression),
        }
    def parse_varname():
        name = input.next()
        if (name.type != "var"):
            input.croak("Expecting variable name")
        return name.value
    def parse_if():
        skip_kw("if")
        cond = parse_expression()
        if (not is_punc(":")):
            skip_kw("then")
        then = parse_expression()
        ret = {
            "type": "if",
            "cond": cond,
            "then": then,
        }
        if (is_kw("else")):
            input.next()
            ret["else"] = parse_expression()
        return ret
    def parse_lambda():
        return {
            "type": "lambda",
           "vars": delimited("(", ")", ",", parse_ame),
            "body": parse_expression()
        }
    def parse_bool():
        return {
            "type": "bool",
            "value": input.next().value == "true"
        }
    def maybe_call(expr):
        expr = expr()
        return parse_call(expr) if is_punc("(") else expr
    def parse_atom():
        def parse_atom_helper():
            if (is_punc("(")):
                input.next()
                exp = parse_expression()
                skip_punc(")")
                return exp
    
            if (is_punc(":")):
                return parse_prog()
            if (is_kw("if")):
                return parse_if()
            if (is_kw("true") or is_kw("false")):
                return parse_bool()
            if (is_kw("lambda") or is_kw("λ")):
                input.next()
                return parse_lambda()
    
            tok = input.next()
            if (tok.type == "var" or tok.type == "num" or tok.type == "str"):
                return tok
            unexpected()

        return maybe_call(parse_atom_helper)
            
    def parse_toplevel():
        prog = []
        while (not input.eof()):
            prog.push(parse_expression())
            if (not input.eof()):
                skip_punc(";")

        return {"type": "prog", "prog": prog}
    def parse_prog():
        prog = delimited("{","}", ";", parse_expression)
        if (prog.length == 0):
            return False
        if (prog.length == 1):
            return prog[0]
        return {"type": "prog", "prog": prog}
    def parse_expression():
        def parse_expression_helper():
            return maybe_binary(parse_atom(), 0)
        return maybe_call(parse_expression_helper)