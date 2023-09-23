.PHONY: image container clean rinha test reqs freeze publish

clean:
	rm -rf bin/
	find -name '*.pyc' -exec rm -f {} +
	find -name '__pycache__' -exec rm -rf {} +
	find -name '.pytest_cache' -exec rm -rf {} +

image: clean freeze
	docker build -t diegor2/rinha .

container: image
	docker run --rm diegor2/rinha

publish: image
	docker push diegor2/rinha:latest

toolchain:
	PYPY_TARBALL := pypy2.7-v7.3.12-src.tar.bz2
	wget https://downloads.python.org/pypy/${PYPY_TARBALL} .
	ifneq ("$(wildcard $(PATH_TO_FILE))","")
		@echo "Already downloaded. Remove pypy directory before getting it again."
	else
		mkdir pypy
		tar -xvf ${PYPY_TARBALL} -C pypy --strip-components=1
		rm -f ${PYPY_TARBALL}
		export PYTHONPATH=/app/pypy
	endif

freeze:
	pip freeze > requirements.txt

reqs:
	pip install -r requirements.txt

rinha:
	python pypy/rpython/bin/rpython --output bin/rinha --verbose -O2 src/python/target.py

test:
	pytest -s src/python/

docker-test: image
	docker run --rm diegor2/rinha pytest src/python/