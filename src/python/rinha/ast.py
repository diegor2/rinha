from math import fmod
from rply.token import BaseBox
from rply.token import Token

### Term ABC
class Term(BaseBox):
    def eval(self):
        raise NotImplementedError

    def to_string(self):
        raise NotImplementedError

    def to_debug_string(self):
        raise NotImplementedError

## Literal values
class Int(Term):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self

    def to_string(self):
        return "%d" % self.value
    
    def to_debug_string(self):
        return 'rinha.ast.Int(%s)'% str(self)

class Str(Term):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self

    def to_string(self):
        return self.value

    def to_debug_string(self):
        return 'rinha.ast.Str(%s)'% self.value
    
class Bool(Term):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self

    def to_string(self):
        return 'true' if self.value else 'false'

    def to_debug_string(self):
        return 'rinha.ast.Bool(%s)'% str(self)
    
class Tuple(Term):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self

    def to_string(self):
        return '(%s, %s)' % (
            self.value[0].eval(), 
            self.value[1].eval()
        )

    def to_debug_string(self):
        return 'rinha.ast.Tuple(%s)'% str(self)
    
# User defined functions

class Function(Term):
    def __init__(self, params, expr):
        self.params = params
        self.expr = expr

    def to_string(self):
        return "fn ({}) => {}".format(_join(self.params), self.expr)

    def eval(self):
        return self.value

    def invoke(self, args):
        pass

class Call(Term):
    def __init__(self, callee, args):
        self.callee = callee
        self.args = args

    def to_string(self):
        return "Call {} with args: {}".format(self.callee, _join(self.args))

    def eval(self):
        return self.callee.invoke(self.args)

## Intrinsic functions

class Print(Term):
    def __init__(self, expr):
        self.expr = expr

    def eval(self):
        box = self.expr.eval()
        print(box.to_string())
        return Int(0)

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

class Binary(Term):
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

    def to_string(self):
        pass

    def eval():
        pass

class If(Term):
    def __init__(self, condition, then, otherwise):
        self.condition = condition
        self.then = then
        self.otherwise = otherwise

    def to_string(self):
        pass

    def eval():
        pass

### Helper functions

def _join(it):
    return ','.join(it)