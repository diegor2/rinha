from math import fmod
from rply.token import BaseBox
from rply.token import Token

## Literal values
class Int(BaseBox):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self

    def __str__(self):
        return str(self.value)

class Str(BaseBox):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self

    def __str__(self):
        return str(self.value)

class Bool(BaseBox):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self

    def __str__(self):
        return str(self.value)

class Tuple(BaseBox):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self

    def __str__(self):
        return str(self.value)

# User defined functions

class Function(BaseBox):
    def __init__(self, params, expr):
        self.params = params
        self.expr = expr

    def __str__(self):
        return "fn ({}) => {}".format(_join(self.params), self.expr)

    def eval(self):
        return self.value

    def invoke(self, args):
        pass

class Call(BaseBox):
    def __init__(self, callee, args):
        self.callee = callee
        self.args = args

    def __str__(self):
        return "Call {} with args: {}".format(self.callee, _join(self.args))

    def eval(self):
        return self.callee.invoke(self.args)

## Intrinsic functions

class Print(BaseBox):
    def __init__(self, expr):
        self.expr = expr

    def eval(self):
        box = self.expr.eval()
        print(str(box))
        return box

class First(BaseBox):
    def __init__(self, tuple):
        self.tuple = tuple

    def eval(self):
        return tuple[0]

class Second(BaseBox):
    def __init__(self, tuple):
        self.tuple = tuple

    def eval(self):
        return tuple[1]

### Binary operators

class Binary(BaseBox):
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

class Let(BaseBox):
    def __init__(self, expr, args):
        self.callee = callee
        self.args = args

    def __str__(self):
        pass

    def eval():
        pass

class If(BaseBox):
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