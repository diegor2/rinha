#!/usr/bin/env sh

PYPY_TARBALL="pypy2.7-v7.3.12-src.tar.bz2"

if [ -d "$PWD/pypy" ]; then
    echo "Already there! Remove pypy directory before getting it again."
else
    wget "https://downloads.python.org/pypy/$PYPY_TARBALL" .
    mkdir pypy
    tar -xvf $PYPY_TARBALL -C pypy --strip-components=1
    rm -f $PYPY_TARBALL
fi

export PYTHONPATH=$PWD/pypy
