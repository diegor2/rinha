.PHONY: image container clean rinha test reqs freeze publish

clean:
	rm -f ${PWD}/rinha
	find -name '*.pyc' -exec rm -f {} +
	find -name '__pycache__' -exec rm -rf {} +
	find -name '.pytest_cache' -exec rm -rf {} +

image: clean
	docker build -t diegor2/rinha .

container: image
	docker run --rm -v ${PWD}/src/rinha:/var/rinha diegor2/rinha

publish: image
	docker push diegor2/rinha:latest

toolchain:
	./get-toolchain.sh

freeze:
	pip freeze > requirements.txt

reqs:
	pip install -r requirements.txt

rinha: toolchain reqs
	python pypy/rpython/bin/rpython --output rinha --verbose -O2 src/python/target.py

test:
	pytest -sxW ignore src/python/
