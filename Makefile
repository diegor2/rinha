.PHONY: build run clean

build:
	docker build -t rinha .

run:
	docker run --rm rinha

clean:
	docker image ls -q | xargs docker image rm -f
