from rply.token import BaseBox
from rply.token import Token

### ABC

class Term(BaseBox):
    def eval(self):
        raise NotImplementedError

## Primitive values

class Str(Term):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def eval(self):
        return self.value

class Int(Term):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        "%d" % self.value

# User defined functions

class Call(Term):
    def __init__(self, callee, args):
        self.callee = callee
        self.args = args

    def __str__(self):
        pass
    
    def eval():
        pass

## Intrinsic functions

class Print(Term):
    def __init__(self, expr):
        self.expr = expr

    def eval(self):
        value = self.expr.eval()
        print(value)
        return value
    
### Binary operations

class Binary(Token):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Add(Binary):
    def eval(self):
        return self.left.eval() + self.right.eval()

class Sub(Binary):
    def eval(self):
        return self.left.eval() - self.right.eval()

class Mul(Binary):
    def eval(self):
        return self.left.eval() * self.right.eval()

class Div(Binary):
    def eval(self):
        return self.left.eval() / self.right.eval()
    