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
ENV PYPY_TARBALL=pypy2.7-v7.3.12-src.tar.bz2
ADD https://downloads.python.org/pypy/$PYPY_TARBALL .
RUN mkdir pypy && tar -xvf $PYPY_TARBALL -C pypy --strip-components=1 && rm -f $PYPY_TARBALL
ENV PYTHONPATH=/app/pypy

# Interpreter source
COPY . /app

# Compile the interpreter
RUN make rinha

# Copy Rinha source
COPY src/rinha /var/rinha

# Interpret rinha code
ENTRYPOINT ["./rinha", "/var/rinha/source.rinha"]
