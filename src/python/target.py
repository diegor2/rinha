"""
    Run ./rinha <source.rinha>
"""

import sys
from rpython.rlib.streamio import open_file_as_stream
from rpython.jit.codewriter.policy import JitPolicy
from rinha.interpreter import interpret


def main(argv):
    if not len(argv) == 2:
        print(__doc__)
        return 1
    filename = argv[1]
    f = open_file_as_stream(filename)
    source = f.readall()
    f.close()

    interpret(filename, source)
    return 0


def target(driver, args):
    return main, None


def jitpolicy(driver):
    return JitPolicy()


if __name__ == '__main__':
    main(sys.argv)
