PYTHON3_VERSION = $(shell seq 6 10)

.PHONY: lint
lint:
	docker pull alpine/flake8:6.0.0
	docker run -ti --rm -v :/apps alpine/flake8:6.0.0 --statistics --count .

.PHONY: unit
unit:
	for ver in ${PYTHON3_VERSION}; do docker pull cimg/python:3.$$ver; done
	