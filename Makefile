ifneq ($(strip $(MAKEFILES)),)
$(error MAKEFILES must be empty; repository verification requires this Makefile to be loaded alone)
endif
ifneq ($(origin MAKEFILE_LIST),file)
$(error MAKEFILE_LIST must not be overridden)
endif
ifneq ($(filter command line override,$(origin SHELL)),)
$(error SHELL must not be overridden for repository verification)
endif
ifneq ($(filter command line override,$(origin .SHELLFLAGS)),)
$(error .SHELLFLAGS must not be overridden for repository verification)
endif
override ROOT := $(shell path='$(subst ','"'"',$(MAKEFILE_LIST))'; path=$$(printf '%s\n' "$$path" | sed 's/^ //'); dirname -- "$$path")

.PHONY: build check lint test

lint test build: check

check:
	python3 "$(ROOT)/scripts/check-baseline.py"
