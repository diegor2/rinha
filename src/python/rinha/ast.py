from math import fmod
from rply.token import BaseBox
from rply.token import Token

### ABC

class Term(BaseBox):
    def eval(self):
        raise NotImplementedError

## Literal values

class Int(Term):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        str(self.value)

    def eval(self):
        return self.value

class Str(Term):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def eval(self):
        return self.value

class Bool(Term):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def eval(self):
        return self.value

class Tuple(Term):
    def __init__(self, first, second):
        self.value = (first, second)

    def __str__(self):
        return str(self.value)

    def eval(self):
        return self.value

# User defined functions

class Function(Term):
    def __init__(self, params, expr):
        self.params = params
        self.expr = expr

    def __str__(self):
        return "fn ({}) => {}".format(_join(self.params), self.expr)

    def eval(self):
        return self.value

    def invoke(self, args):
        pass

class Call(Term):
    def __init__(self, callee, args):
        self.callee = callee
        self.args = args

    def __str__(self):
        return "Call {} with args: {}".format(self.callee, _join(self.args))

    def eval(self):
        return self.callee.invoke(self.args)

## Intrinsic functions

class Print(Term):
    def __init__(self, expr):
        self.expr = expr

    def eval(self):
        value = self.expr.eval()
        print(value)
        return value

class First(Term):
    def __init__(self, tuple):
        self.tuple = tuple

    def eval(self):
        return tuple[0]

class Second(Term):
    def __init__(self, tuple):
        self.tuple = tuple

    def eval(self):
        return tuple[1]

### Binary operators

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

class Rem(Binary):
    def eval(self):
        return fmod(self.left.eval(), self.right.eval())

class Eq(Binary):
    def eval(self):
        return self.left.eval() == self.right.eval()
    
class Neq(Binary):
    def eval(self):
        return self.left.eval() != self.right.eval()

class Lt(Binary):
    def eval(self):
        return self.left.eval() < self.right.eval()

class Gt(Binary):
    def eval(self):
        return self.left.eval() > self.right.eval()

class Lte(Binary):
    def eval(self):
        return self.left.eval() <= self.right.eval()

class Gte(Binary):
    def eval(self):
        return self.left.eval() >= self.right.eval()

class And(Binary):
    def eval(self):
        return self.left.eval() and self.right.eval()

class Or(Binary):
    def eval(self):
        return self.left.eval() or self.right.eval()

### Flow control

class Let(Term):
    def __init__(self, expr, args):
        self.callee = callee
        self.args = args

    def __str__(self):
        pass

    def eval():
        pass

class If(Term):
    def __init__(self, condition, then, otherwise):
        self.condition = condition
        self.then = then
        self.otherwise = otherwise

    def __str__(self):
        pass

    def eval():
        pass

### Helper functions

def _join(it):
    return ','.join(it)