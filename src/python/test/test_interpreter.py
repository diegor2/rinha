import os

from rinha.interpreter import interpret

def interpret_file(filename):
    with open('src/rinha/%s' % filename) as f:
        return interpret(f.read())

def test_sample_file_hello_world(capfd):
    result = interpret_file('print.rinha')
    assert result.value == 'Hello world'
    
    out, err = capfd.readouterr()
    assert out == 'Hello world\n'
    assert err == ''

def test_sample_file_fibonacci(capfd):
    result = interpret_file('fib.rinha')
    assert result.value == '@!fibbo::55'
    
    out, err = capfd.readouterr()
    assert out == '@!compile::\n@!fibbo::55\n'
    assert err == ''

def test_sample_file_geometry(capfd):
    result = interpret_file('geom.rinha')
    assert result.value == 'scalene'

    out, err = capfd.readouterr()
    assert out == 'scalene\n'
    assert err == ''

# def test_sample_file_combination(capfd):
#     result = interpret_file('combination.rinha')
#     assert result.value == 55
    
#     out, err = capfd.readouterr()
#     assert out == '55\n'
#     assert err == ''

def test_sample_file_square(capfd):
    result = interpret_file('square.rinha')
    assert result.value == 16

    out, err = capfd.readouterr()
    assert out == '16\n'
    assert err == ''

def test_sample_file_recursive_sum(capfd):
    result = interpret_file('sum.rinha')
    assert result.value == 15

    out, err = capfd.readouterr()
    assert out == '15\n'
    assert err == ''

def test_print(capfd):
    result = interpret('let _ = print(1); print(2)')
    assert result.value == 2

    out, err = capfd.readouterr()
    assert out == '1\n2\n'
    assert err == ''
    
    result = interpret('let f = fn(x, y, z,) => { 0 }; f(print(1), print(2), print(3))')
    assert result.value == 0

    out, err = capfd.readouterr()
    assert out == '1\n2\n3\n'
    assert err == ''
    
    result = interpret('let tuple = (print(1), print(2)); print(tuple)')
    assert result.left.value == 1
    assert result.right.value == 2

    out, err = capfd.readouterr()
    assert out == '1\n2\n(1, 2)\n'
    assert err == ''

def test_add():
    result = interpret('3 + 5')
    assert result.value == 8
    
    result = interpret('"a" + 2')
    assert result.value == 'a2'
    
    result = interpret('2 + "a"')
    assert result.value == '2a'

    result = interpret('"a" + "b"')
    assert result.value == "ab"

def test_sub():
    result = interpret('0 - 1')
    assert result.value == -1

def test_mul():
    result = interpret('2 * 2')
    assert result.value == 4

def test_div():
    result = interpret('3 / 2')
    assert result.value == 1

def test_rem():
    result = interpret('4 % 2')
    assert result.value == 0

def test_eq():
    result = interpret('"a" == "a"')
    assert result.value == True

    result = interpret('2 == 1 + 1')
    assert result.value == True
    
    result = interpret('true == true')
    assert result.value == True

def test_neq():
    result = interpret('"a" != "b"')
    assert result.value == True

    result = interpret(' 3 != 1 + 1')
    assert result.value == True
    
    result = interpret('true != false')
    assert result.value == True

def test_comp():
    result = interpret('1 < 2')
    assert result.value == True

    result = interpret('2 > 3')
    assert result.value == False

    result = interpret('1 <= 2')
    assert result.value == True
    
    result = interpret('1 >= 2')
    assert result.value == False

def test_bool_algebra():
    result = interpret('true && false')
    assert result.value == False

    result = interpret('false || true')
    assert result.value == True

def test_let():
    result = interpret('let x = 1; x')
    assert result.value == 1
    
    result = interpret('let x = 1 + 2; x')
    assert result.value == 3
