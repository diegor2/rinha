.PHONY: docker build run clean rinha

build:
	docker build -t rinha .

run:
	docker run --rm rinha

docker: build run

clean:
	docker image ls -q | xargs docker image rm -f
	rm -rf bin/

rinha:
	python pypy/rpython/bin/rpython --output bin/rinha --verbose -O2 src/python/target.py
