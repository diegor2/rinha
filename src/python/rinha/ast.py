from math import fmod
from rply.token import BaseBox

 
## Term ABC
class Term(BaseBox):
    def eval(self):
        raise NotImplementedError()

## Literal values
class Int(Term):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self

class Str(Term):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self

class Bool(Term):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self

## Collections

class Tuple(Term):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self

# User defined functions

# class Function(Term):
#     def __init__(self, params, expr):
#         self.params = params
#         self.expr = expr

#     def to_string(self):
#         return "fn ({}) => {}".format(_join(self.params), self.expr)

#     def eval(self):
#         return self.value

#     def invoke(self, args):
#         pass

# class Call(Term):
#     def __init__(self, callee, args):
#         self.callee = callee
#         self.args = args

#     def to_string(self):
#         return "Call {} with args: {}".format(self.callee, _join(self.args))

#     def eval(self):
#         return self.callee.invoke(self.args)

## Intrinsic functions

class Print(Term):
    def __init__(self, expr):
        self.expr = expr

    def eval(self):
        box = self.expr.eval()

        if isinstance(box, Str):
            print(box.value)
        elif isinstance(box, Int):
            print(box.value)
        elif isinstance(box, Bool):
            print('true' if box.value else 'false')
        else:
            raise ValueError("Can't print this! %s" % type(box))
        return box

# class First(Term):
#     def __init__(self, tuple):
#         self.tuple = tuple

#     def eval(self):
#         return tuple[0]

# class Second(Term):
#     def __init__(self, tuple):
#         self.tuple = tuple

#     def eval(self):
#         return tuple[1]

### Binary operators

class Binary(Term):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self):
        return self.compute(self.left.eval(), self.right.eval())
    
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
            raise ValueError("Can't compute: %s \% %s" % (type(left), type(right)))

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

### Flow control

# class Let(Term):
#     def __init__(self, expr, args):
#         self.callee = callee
#         self.args = args

#     def to_string(self):
#         pass

#     def eval():
#         pass

# class If(Term):
#     def __init__(self, condition, then, otherwise):
#         self.condition = condition
#         self.then = then
#         self.otherwise = otherwise

#     def to_string(self):
#         pass

#     def eval():
#         pass

### Helper functions

def _join(it):
    return ','.join(it)
