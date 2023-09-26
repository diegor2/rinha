from math import fmod
from rply.token import BaseBox

 
## Term ABC
class Term(BaseBox):
    def eval(self, scope = None):
        raise NotImplementedError()

## Literal values
class Int(Term):
    def __init__(self, value):
        self.value = value

    def eval(self, scope = None):
        return self

class Str(Term):
    def __init__(self, value):
        self.value = value

    def eval(self, scope = None):
        return self

class Bool(Term):
    def __init__(self, value):
        self.value = value

    def eval(self, scope = None):
        return self
    
class Reference(Term):
    def __init__(self, identif):
        self.identif = identif

    def eval(self, scope = None):
        return scope[self.identif]

## Collections

class Tuple(Term):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, scope = None):
        return self

class First(Term):
    def __init__(self, ref):
        self.ref = ref

    def eval(self, scope = None):
        target = self.ref.eval(scope)
        assert isinstance(target, Tuple)
        return target.left

class Second(Term):
    def __init__(self, ref):
        self.ref = ref

    def eval(self, scope = None):
        target = self.ref.eval(scope)
        assert isinstance(target, Tuple)
        return target.right
    
## Intrinsic functions

class Print(Term):
    def __init__(self, expr):
        self.expr = expr

    def eval(self, scope = None):
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

    def eval(self, scope = None):
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

class ParamList(BaseBox):
    def __init__(self, identif = None):
        self.ids = [identif] if identif else []
    
    def merge(self, pl):
        assert isinstance(pl, ParamList)
        self.ids = self.ids + pl.ids
        return self

class Function(Term):
    def __init__(self, params, body):
        assert isinstance(params, ParamList)
        assert isinstance(body, Term)
        self.params = params
        self.body = body

    def eval(self, scope = None):
        return self

    def apply(self, scope):
        return self.body.eval(scope)

class ArgList(BaseBox):
    def __init__(self, expr = None):
        self.exprs = [expr] if expr else []

    def merge(self, al):
        assert isinstance(al, ArgList)
        self.exprs = self.exprs + al.exprs
        return self

class Call(Term):
    def __init__(self, callee, args):
        # assert isinstance(callee, Reference)
        # assert isinstance(args, ArgList)
        self.ref = callee
        self.args = args

    def eval(self, scope = None):
        fn = self.ref.eval(scope)
        assert isinstance(fn, Function)
        assert len(fn.params.ids) == len(self.args.exprs)
        
        cloj = scope or dict()
        cloj.update(zip(fn.params.ids, self.args.exprs))
        return fn.apply(cloj)

## Naming things

class Reference(Term):
    def __init__(self, identif):
        self.identif = identif

    def eval(self, scope = None):
        return scope[self.identif]

class Let(Term):
    def __init__(self, identif, expr, next):
        self.identif = identif
        self.expr = expr
        self.next = next

    def eval(self, scope = None):
        cloj = scope or dict()
        cloj[self.identif] = self.expr
        return self.next.eval(cloj)

## Flow control

class If(Term):
    def __init__(self, condition, then, otherwise):
        self.condition = condition
        self.then = then
        self.otherwise = otherwise

    def eval(self, scope = None):
        pass

### Helper functions

def _join(it):
    return ','.join(it)
