import json

from math import fmod
from rply.token import BaseBox

## Term ABC

class Term(BaseBox):
    def eval(self, scope = None):
        raise NotImplementedError()

    def to_json(self):
        raise NotImplementedError()
    
## Primitive values

def boxed(value):
    if isinstance(value, int):
        return Int(value)
    elif isinstance(value, str):
        return Str(value)
    elif isinstance(value, bool):
        return Bool(value)
    else:
        return Str(str(value))

class Value(Term):
    def to_str(self):
        raise NotImplementedError()
    
    def is_truthy(self):
        raise NotImplementedError()

class Int(Value):
    def __init__(self, value):
        self.value = value

    def eval(self, scope = None):
        return self
    
    def to_json(self):
        return {'int': repr(self.value)}

    def to_str(self):
        return str(self.value)
    
    def is_truthy(self):
        return self.value == True
    
class Str(Value):
    def __init__(self, value):
        self.value = value

    def eval(self, scope = None):
        return self

    def to_json(self):
        return {'str': repr(self.value)}

    def to_str(self):
        return str(self.value)
    
    def is_truthy(self):
        return self.value == True
    
class Bool(Value):
    def __init__(self, value):
        self.value = value

    def eval(self, scope = None):
        return self
    
    def to_json(self):
        return {'bool': repr(self.value)}

    def to_str(self):
        return str(self.value)
    
    def is_truthy(self):
        return self.value
    
## Collections

class Tuple(Term):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, scope = None):
        return self

    def to_json(self):
        return {'tup': (self.left.to_json(), self.right.to_json())}

class First(Term):
    def __init__(self, ref):
        self.ref = ref

    def eval(self, scope = None):
        target = self.ref.eval(scope)
        assert isinstance(target, Tuple)
        return target.left

    def to_json(self):
        return {'first': self.ref.to_json()}

class Second(Term):
    def __init__(self, ref):
        self.ref = ref

    def eval(self, scope = None):
        target = self.ref.eval(scope)
        assert isinstance(target, Tuple)
        return target.right
    
    def to_json(self):
        return {'second': self.ref.to_json()}
    
## Intrinsic functions

class Print(Term):
    def __init__(self, expr):
        self.expr = expr

    def eval(self, scope = None):
        box = self.expr.eval(scope)

        assert isinstance(box, Value)
        print(box.to_str())
        # dump(box)
        return box

    def to_json(self):
        return {'print': self.expr.to_json()}
    
### Binary operators

class Binary(Term):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, scope = None):
        lhs, rhs = self.left.eval(scope), self.right.eval(scope)
        assert isinstance(lhs, Value) and isinstance(rhs, Value)

        # dump(self)
        # dump(lhs)
        # dump(rhs)

        result = self.compute(lhs, rhs)
        dump((self.__class__.__name__, lhs, rhs, result))

        return boxed(result)

    def compute(self, left, right):
        raise NotImplementedError()
    
class Add(Binary):
    def compute(self, left, right):
        # if isinstance(left, Int) and isinstance(right, Int):
            return left.value + right.value
        # else:
            # raise ValueError("Can't compute: %s + %s" % (type(left), type(right)))

    def to_json(self):
        return {'Add': (self.left.to_json(), self.right.to_json())}
    
class Sub(Binary):
    def compute(self, left, right):
        # if isinstance(left, Int) and isinstance(right, Int):
            return left.value - right.value
        # else:
        #     raise ValueError("Can't compute: %s - %s" % (type(left), type(right)))

    def to_json(self):
        return {'Sub': (self.left.to_json(), self.right.to_json())}
    
class Mul(Binary):
    def compute(self, left, right):
        # if isinstance(left, Int) and isinstance(right, Int):
            return left.value * right.value
        # else:
        #     raise ValueError("Can't compute: %s * %s" % (type(left), type(right)))

    def to_json(self):
        return {'Mul': (self.left.to_json(), self.right.to_json())}
    
class Div(Binary):
    def compute(self, left, right):
        # if isinstance(left, Int) and isinstance(right, Int):
            return left.value / right.value
        # else:
        #     raise ValueError("Can't compute: %s / %s" % (type(left), type(right)))

    def to_json(self):
        return {'Div': (self.left.to_json(), self.right.to_json())}
    
class Rem(Binary):
    def compute(self, left, right):
        # if isinstance(left, Int) and isinstance(right, Int):
            return fmod(left.value, right.value)
        # else:
        #     raise ValueError("Can't compute: %s %% %s" % (type(left), type(right)))

    def to_json(self):
        return {'Rem': (self.left.to_json(), self.right.to_json())}
    
class Eq(Binary):
    def compute(self, left, right):
        # dump(self)
        # if isinstance(left, Int) and isinstance(right, Int):
            return left.value == right.value
        # else:
        #     raise ValueError("Can't compare: %s == %s" % (type(left), type(right)))

    def to_json(self):
        return {'Eq': (self.left.to_json(), self.right.to_json())}
    
class Neq(Binary):
    def compute(self, left, right):
        # if isinstance(left, Int) and isinstance(right, Int):
            return left.value != right.value
        # else:
        #     raise ValueError("Can't compare: %s != %s" % (type(left), type(right)))

    def to_json(self):
        return {'Neq': (self.left.to_json(), self.right.to_json())}
    
class Lt(Binary):
    def compute(self, left, right):
        # if isinstance(left, Int) and isinstance(right, Int):
            return left.value < right.value
        # else:
        #     raise ValueError("Can't compare: %s < %s" % (type(left), type(right)))

    def to_json(self):
        return {'Lt': (self.left.to_json(), self.right.to_json())}
    
class Gt(Binary):
    def compute(self, left, right):
        # if isinstance(left, Int) and isinstance(right, Int):
            return left.value > right.value
        # else:
        #     raise ValueError("Can't compare: %s > %s" % (type(left), type(right)))

    def to_json(self):
        return {'Gt': (self.left.to_json(), self.right.to_json())}
    
class Lte(Binary):
    def compute(self, left, right):
        # if isinstance(left, Int) and isinstance(right, Int):
            return left.value <= right.value
        # else:
        #     raise ValueError("Can't compare: %s <= %s" % (type(left), type(right)))

    def to_json(self):
        return {'Lte': (self.left.to_json(), self.right.to_json())}
    
class Gte(Binary):
    def compute(self, left, right):
        # if isinstance(left, Int) and isinstance(right, Int):
            return left.value >= right.value
        # else:
        #     raise ValueError("Can't compare: %s >= %s" % (type(left), type(right)))

    def to_json(self):
        return {'Gte': (self.left.to_json(), self.right.to_json())}
    
class And(Binary):
    def compute(self, left, right):
        # if isinstance(left, Value) and isinstance(right, Value):
            return left.value and right.value
        # else:
        #     raise ValueError("Can't compare: %s && %s" % (type(left), type(right)))

    def to_json(self):
        return {'And': (self.left.to_json(), self.right.to_json())}
    
class Or(Binary):
    def compute(self, left, right):
        # if isinstance(left, Int) and isinstance(right, Int):
            return left.value or right.value
        # else:
        #     raise ValueError("Can't compare: %s || %s" % (type(left), type(right)))

    def to_json(self):
        return {'Or': (self.left.to_json(), self.right.to_json())}
    
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

    def to_json(self):
        return {'fun': {'param': self.params.ids, 'body': self.body.to_json()} }
    
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
        self.callee = callee
        self.args = args

    def eval(self, scope = None):
        fn = self.callee.eval(scope)

        assert isinstance(fn, Function)
        assert len(fn.params.ids) == len(self.args.exprs)
        
        cloj = dict(scope) or dict()

        args = [e.eval(scope) for e in self.args.exprs]
        locals = zip(fn.params.ids, args)
        cloj.update(locals)

        result = fn.apply(cloj)

        dump({
            # 'body': fn.body,
            'args': locals,
            'result': result,
        })
        # dump((self.callee, scope['n'], result))
        print('-' * 10)

        return result
        
    def to_json(self):
        return "Cal(%s) <= (%s)" % (self.callee.to_json(), self.args.to_json())
        
    def to_json(self):
        return {'call': {'callee': self.callee.to_json(), 'args': [e.to_json() for e in self.args.exprs] } }
    
## Naming things

class Reference(Term):
    def __init__(self, identif):
        self.identif = identif

    def eval(self, scope = None):
        expr = scope[self.identif]
        # dump(expr)
        # if(isinstance(expr, Value) or isinstance(expr, Function)):
            # return expr
        # else:
        #     return expr.eval(scope)
        return expr.eval(scope)
    
    def to_json(self):
        return {'ref': self.identif }
        
class Let(Term):
    def __init__(self, identif, expr, next):
        self.identif = identif
        self.expr = expr
        self.next = next

    def eval(self, scope = None):
        cloj = scope or dict()
        cloj[self.identif] = self.expr # late eval

        # dump(('let', cloj))

        return self.next.eval(cloj)

    def to_json(self):
        return {'let': {'id': self.identif, 'exp': self.expr.to_json() , 'nxt': self.next.to_json() }}

## Flow control

class If(Term):
    def __init__(self, condition, then, otherwise):
        self.condition = condition
        self.then = then
        self.otherwise = otherwise

    def eval(self, scope = None):
        box = self.condition.eval(scope)

        # dump((self.condition, scope['n']))

        if(box.is_truthy()):
            # print('then')
            return self.then.eval(scope)
        else:
            # print('else')
            return self.otherwise.eval(scope)

    def to_json(self):
        return {'if': {'cond': self.condition, 'then': self.then.to_json() , 'else': self.otherwise.to_json()}}

## debug

def dump(ast, indent=None):
    print(json.dumps(ast, default=lambda o: o.to_json(), indent=indent))
