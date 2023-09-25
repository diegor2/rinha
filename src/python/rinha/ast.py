from math import fmod
from rply.token import BaseBox

 
## Term ABC
class Term(BaseBox):
    def eval(self, scope):
        raise NotImplementedError()

## Literal values
class Int(Term):
    def __init__(self, value):
        self.value = value

    def eval(self, scope):
        return self

class Str(Term):
    def __init__(self, value):
        self.value = value

    def eval(self, scope):
        return self

class Bool(Term):
    def __init__(self, value):
        self.value = value

    def eval(self, scope):
        return self
    
class Identifier(Term):
    def __init__(self, value):
        self.value = value

    def eval(self, scope):
        return scope[self.value]
    
class Nil(Term):
    def eval(self, scope):
        raise ValueError('nil reference')

## Collections

class Tuple(Term):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, scope):
        return self

class First(Term):
    def __init__(self, value):
        self.value = value

    def eval(self, scope):
        target = self.value.eval(scope)
        assert isinstance(target, Tuple)
        return target.left

class Second(Term):
    def __init__(self, value):
        self.value = value

    def eval(self, scope):
        target = self.value.eval(scope)
        assert isinstance(target, Tuple)
        return target.right
    
## Intrinsic functions

class Print(Term):
    def __init__(self, expr):
        self.expr = expr

    def eval(self, scope):
        box = self.expr.eval(scope)

        if isinstance(box, Str):
            print(box.value)
        elif isinstance(box, Int):
            print(box.value)
        elif isinstance(box, Bool):
            print('true' if box.value else 'false')
        else:
            raise ValueError("Can't print this! %s" % type(box))
        return box

### Binary operators

class Binary(Term):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, scope):
        return self.compute(self.left.eval(scope), self.right.eval(scope))
    
    def compute(self, left, right):
        raise NotImplementedError()

class Add(Binary):
    def compute(self, left, right):
        if isinstance(left, Int) and isinstance(right, Int):
            return Int(left.value + right.value)
        else:
            raise ValueError("Can't compute: %s + %s" % (type(left), type(right)))

class Sub(Binary):
    def compute(self, left, right):
        if isinstance(left, Int) and isinstance(right, Int):
            return Int(left.value - right.value)
        else:
            raise ValueError("Can't compute: %s - %s" % (type(left), type(right)))

class Mul(Binary):
    def compute(self, left, right):
        if isinstance(left, Int) and isinstance(right, Int):
            return Int(left.value * right.value)
        else:
            raise ValueError("Can't compute: %s * %s" % (type(left), type(right)))

class Div(Binary):
    def compute(self, left, right):
        if isinstance(left, Int) and isinstance(right, Int):
            return Int(left.value / right.value)
        else:
            raise ValueError("Can't compute: %s / %s" % (type(left), type(right)))

class Rem(Binary):
    def compute(self, left, right):
        if isinstance(left, Int) and isinstance(right, Int):
            return Int(fmod(left.value, right.value))
        else:
            raise ValueError("Can't compute: %s %% %s" % (type(left), type(right)))

class Eq(Binary):
    def compute(self, left, right):
        if isinstance(left, Int) and isinstance(right, Int):
            return Bool(left.value == right.value)
        else:
            raise ValueError("Can't compare: %s == %s" % (type(left), type(right)))

class Neq(Binary):
    def compute(self, left, right):
        if isinstance(left, Int) and isinstance(right, Int):
            return Bool(left.value != right.value)
        else:
            raise ValueError("Can't compare: %s == %s" % (type(left), type(right)))

class Lt(Binary):
    def compute(self, left, right):
        if isinstance(left, Int) and isinstance(right, Int):
            return Bool(left.value < right.value)
        else:
            raise ValueError("Can't compare: %s , %s" % (type(left), type(right)))

class Gt(Binary):
    def compute(self, left, right):
        if isinstance(left, Int) and isinstance(right, Int):
            return Bool(left.value > right.value)
        else:
            raise ValueError("Can't compare: %s > %s" % (type(left), type(right)))

class Lte(Binary):
    def compute(self, left, right):
        if isinstance(left, Int) and isinstance(right, Int):
            return Bool(left.value <= right.value)
        else:
            raise ValueError("Can't compare: %s <= %s" % (type(left), type(right)))

class Gte(Binary):
    def compute(self, left, right):
        if isinstance(left, Int) and isinstance(right, Int):
            return Bool(left.value >= right.value)
        else:
            raise ValueError("Can't compare: %s >= %s" % (type(left), type(right)))

class And(Binary):
    def compute(self, left, right):
        if isinstance(left, Int) and isinstance(right, Int):
            return Bool(left.value and right.value)
        else:
            raise ValueError("Can't compare: %s && %s" % (type(left), type(right)))

class Or(Binary):
    def compute(self, left, right):
        if isinstance(left, Int) and isinstance(right, Int):
            return Bool(left.value or right.value)
        else:
            raise ValueError("Can't compare: %s || %s" % (type(left), type(right)))

# User defined functions

class Function(Term):
    def __init__(self, params, body):
        self.params = params
        self.body = body

    def eval(self, scope):
        return self

    def apply(self, args):
        return self

class Call(Term):
    def __init__(self, callee, args):
        self.callee = callee
        self.args = args

    def eval(self, scope):
        return self.callee.apply(self.args)

## Flow control

class Let(Term):
    def __init__(self, expr, args):
        self.callee = callee
        self.args = args

    def to_string(self):
        pass

    def eval(self, scope):
        pass

class If(Term):
    def __init__(self, condition, then, otherwise):
        self.condition = condition
        self.then = then
        self.otherwise = otherwise

    def eval(self, scope):
        pass

### Helper functions

def _join(it):
    return ','.join(it)
