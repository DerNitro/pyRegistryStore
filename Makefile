PYTHON3_VERSION	= $(shell seq 6 10)
PWD				= $(shell pwd)

DOCKER_IMAGE	= docker images -q pytest:3.$(1)
DOCKER_BUILD	= PYTHON_VERSION=3.$(1) docker build -t pytest:3.$(1) --no-cache .ci/
DOCKER_PYTEST 	= docker run --rm -t pytest:3.$(1) run -m pytest --junitxml=units_3.$(1).xml

.PHONY: lint
lint:
	docker pull alpine/flake8:6.0.0
	docker run --rm -v $(PWD):/apps alpine/flake8:6.0.0 --statistics --count .

.PHONY: unit
unit:
	for ver in ${PYTHON3_VERSION}; do
		@if [[ $(call DOCKER_IMAGE,$$ver) == "" ]]; then
			$(call DOCKER_BUILD,$$ver) ;
		fi
		$(call DOCKER_PYTEST,$$ver) ;
	done
	
