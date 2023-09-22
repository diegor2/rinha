FROM pypy:3.10-slim

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Rinha source
COPY src/rinha /var/rinha

WORKDIR /app
COPY . /app

ENTRYPOINT ["python", "src/python/main.py", "/var/rinha/fib.rinha"]
