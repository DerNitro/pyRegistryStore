PYTHON3_VERSION	= $(shell seq 6 10)
PWD				= $(shell pwd)
USER            = $(shell whoami)

APP_VERSION = $(shell ./pyRegistryStore.py version)

DOCKER_BUILD	= PYTHON_VERSION=3.$(1) docker build -t pytest:3.$(1) --no-cache .ci/
DOCKER_PYTEST 	= docker run --rm \
				-u $(shell id -u $(USER)):$(shell id -g $(USER)) \
				-v /etc/passwd:/etc/passwd:ro \
				-v $(PWD):/apps -t pytest:3.$(1) run -m pytest --junitxml=tests/output/units_3.$(1).xml

DOCKER_COVER 	= docker run --rm \
				-u $(shell id -u $(USER)):$(shell id -g $(USER)) \
				-v /etc/passwd:/etc/passwd:ro \
				-v $(PWD):/apps -t pytest:3.10 $(1)

.PHONY: test
test: version lint unit

.PHONY: version
version:
	@echo "Run test version: $(APP_VERSION)"
	@echo
	@test -z `git tag -l $(APP_VERSION)` || (echo "Check version ($(APP_VERSION)) - failed"; false)

.PHONY: lint
lint:
	@docker pull alpine/flake8:6.0.0
	@docker run --rm -v $(PWD):/apps alpine/flake8:6.0.0 --statistics --count .

.PHONY: unit
unit:
	@for ver in $(PYTHON3_VERSION); do \
		echo "Python version: 3.$$ver" ; \
		docker build -q -t pytest:3.$$ver --build-arg PYTHON_VERSION=3.$$ver .ci/ ; \
		$(call DOCKER_PYTEST,$$ver) ; \
	done
	@$(call DOCKER_COVER,report)
	@$(call DOCKER_COVER,html)
