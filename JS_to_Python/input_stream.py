def input_stream(input):
    pos = 0
    line = 1
    col = 0
    return {
        next: next,
        peek: peek,
        eof: eof,
        croak: croak,
    }

    def next():
        ch = input[pos+1]
        if (ch == "\n"):
            line += 1
            col = 0
        else:
            col += 1
        return ch

    def peek():
        return input[pos]

    def eof():
        return peek() == ""

    def croak(msg):
        class Error(Exception):
            pass
        raise Error(msg + " (" + line + ":" + col + ")")
