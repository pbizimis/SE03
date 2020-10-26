import re
def token_stream(input):
    current = null
    keywords = " if then else lambda λ True False "
    return {
        next  : next,
        peek  : peek,
        eof   : eof,
        croak : input.croak
    }
    def is_keyword(x):
        return keywords.index(" " + x + " ") >= 0
    def is_digit(ch):
        return re.match("[0-9]", ch)
    def is_id_start(ch):
        return re.match("[a-zλ_]", ch, re.IGNORECASE)
    def is_id(ch):
        return is_id_start(ch) or "?!-<>=0123456789".index(ch) >= 0
    def is_op_char(ch):
        return "+-*/%=&|<>!".index(ch) >= 0
    def is_punc(ch):
        return ",[]".index(ch) >= 0
    def is_whitespace(ch):
        return " \t\n".index(ch) >= 0
    def read_while(predicate):
        stri = ""
        while (notinput.eof() and predicate(input.peek())):
            stri += input.next()
        return stri
    def read_number():
        has_dot = False

        def read_number_helper(ch):
            if (ch == "."):
                if (has_dot):
                    return False
                has_dot = True
                return True
            return is_digit(ch)
        number = read_while(read_number_helper)
        return{"type": "num", "value": float(number)}
    def read_ident():
        id = read_while(is_id)
        return {
            "type": "kw" if is_keyword(id) else "var",
            "value": id
        }
    def read_escaped(end):
        escaped = False
        stri = ""
        input.next()
        while (not input.eof()):
            ch = input.next()
            if (escaped):
                stri += ch
                escaped = False
            elif (ch == "\\"):
                escaped = True
            elif (ch == end):
                break
            else:
                stri += ch
        return stri
    def read_string():
        return{"type": "str", "value": read_escaped('"')}
    def skip_comment():
        def skip_comment_helper(ch):
            return ch != "\n"
        read_while(skip_comment_helper)
        input.next()
    def read_next():
        read_while(is_whitespace)
        if (input.eof()):
            return None
        ch = input.peek()
        if (ch == "#"):
            skip_comment()
            return read_next()

        if (ch == '"'):
            return read_string()
        if (is_digit(ch)):
            return read_number()
        if (is_id_start(ch)):
            return read_ident()
        if (is_punc(ch)):
            return {
                "type": "punc",
                "value": input.next()
            }
        if (is_op_char(ch)):
            return {
                "type"  : "op",
                "value" : read_while(is_op_char)
            }
        input.croak("Can't handle character: " + ch)
    def peek():
        if (current):
            return current
        else:
            current = read_next()
            return current
    def next():
        tok = current
        current = None
        return tok or read_next()
    def eof():
        return peek() == None