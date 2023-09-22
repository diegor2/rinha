FROM pypy:2.7-slim-bookworm

# Package dependencies
RUN apt update && apt install -y gcc make libffi-dev pkg-config \
    zlib1g-dev libbz2-dev libsqlite3-dev libncurses5-dev \
    libexpat1-dev libssl-dev libgdbm-dev tk-dev libgc-dev \
    liblzma-dev libncursesw5-dev

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app

# rpython toolchain
ADD https://downloads.python.org/pypy/pypy3.10-v7.3.12-src.tar.bz2 .
RUN mkdir pypy && tar -xvf pypy3.10-v7.3.12-src.tar.bz2 -C pypy --strip-components=1 && rm -f pypy3.10-v7.3.12-src.tar.bz2
ENV PYTHONPATH=/app/pypy

# Interpreter source
COPY . /app

# Compile the interpreter
RUN pypy pypy/rpython/bin/rpython --output rinha --verbose -O2 src/python/target.py

# Copy Rinha source
COPY src/rinha /var/rinha

# Interpret rinha code
ENTRYPOINT ["./rinha", "/var/rinha/fib.rinha"]
