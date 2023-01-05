PYTHON3_VERSION		= $(shell seq 6 10)
PWD					= $(shell pwd)
USER            	= $(shell whoami)

GIT_SHORT_COMMIT 	= $(shell git log --pretty="%h" -n1)
GIT_BRANCH			= $(shell git branch --show-current)

APP_NAME			= pyRegistryStore
APP_VERSION 		= $(shell ./pyRegistryStore.py version)
SETUP_VERSION 		= $(shell python3 setup.py --version)

DEV_ARTIFACT		= $(APP_NAME)-$(APP_VERSION).dev$(GIT_SHORT_COMMIT).tar.gz
RELEASE_ARTIFACT	= $(APP_NAME)-$(APP_VERSION).tar.gz

CI_ARTIFACT_PATH	= /opt/pip/pyRegistryStore

DOCKER_BUILD		= PYTHON_VERSION=3.$(1) docker build -t pytest:3.$(1) --no-cache .ci/
DOCKER_PYTEST 		= docker run --rm \
					-u $(shell id -u $(USER)):$(shell id -g $(USER)) \
					-v /etc/passwd:/etc/passwd:ro \
					-v $(PWD):/apps -t pytest:3.$(1) run -m pytest -v --junitxml=tests/output/units_3.$(1).xml

DOCKER_COVER 		= docker run --rm \
					-u $(shell id -u $(USER)):$(shell id -g $(USER)) \
					-v /etc/passwd:/etc/passwd:ro \
					-v $(PWD):/apps -t pytest:3.10 $(1)

.PHONY: test version lint unit build

ifneq ($(GIT_BRANCH), 'release')
all: version lint unit build
else
all: build
endif

version:
	@echo "Run test version: $(APP_VERSION)"
	@echo
	@test -z `git tag -l $(APP_VERSION)` || (echo "Check version ($(APP_VERSION)) - failed"; false)
	@test $(APP_VERSION) = $(SETUP_VERSION) || (echo "Setup version ($(SETUP_VERSION)) - failed"; false)

lint:
	@docker pull alpine/flake8:6.0.0
	@docker run --rm -v $(PWD):/apps alpine/flake8:6.0.0 --statistics --count .

unit:
	@for ver in $(PYTHON3_VERSION); do \
		echo "Python version: 3.$$ver" ; \
		docker build -q -t pytest:3.$$ver --build-arg PYTHON_VERSION=3.$$ver .ci/ ; \
		$(call DOCKER_PYTEST,$$ver) ; \
	done
	@$(call DOCKER_COVER,report)
	@$(call DOCKER_COVER,html)

clean:
	@rm -rf dist *.egg-info

ifneq ($(GIT_BRANCH), 'release')
build: clean
	@python3 setup.py egg_info --tag-build=.dev$(GIT_SHORT_COMMIT) sdist
	@scp dist/$(DEV_ARTIFACT) ci@su-blog.ru:$(CI_ARTIFACT_PATH)/dev
	@mkdir /tmp/pip_download; cd /tmp/pip_download; pip download http://pip.su-blog.ru/pyRegistryStore/dev/$(DEV_ARTIFACT)
	@rm -rf /tmp/pip_download
endif
