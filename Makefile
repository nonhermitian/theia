# This code is part of Qiskit.
#
# (C) Copyright IBM 2017.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

OS := $(shell uname -s)

ifeq ($(OS), Linux)
  NPROCS := $(shell grep -c ^processor /proc/cpuinfo)
else ifeq ($(OS), Darwin)
  NPROCS := 2
else
  NPROCS := 0
endif # $(OS)

ifeq ($(NPROCS), 2)
	CONCURRENCY := 2
else ifeq ($(NPROCS), 1)
	CONCURRENCY := 1
else ifeq ($(NPROCS), 3)
	CONCURRENCY := 3
else ifeq ($(NPROCS), 0)
	CONCURRENCY := 0
else
	CONCURRENCY := $(shell echo "$(NPROCS) 2" | awk '{printf "%.0f", $$1 / $$2}')
endif

.PHONY: lint test test_ci

# Ignoring generated ones with .py extension.
lint:
	pylint -rn theia

style:
	pycodestyle --max-line-length=100 theia

# Use the -s (starting directory) flag for "unittest discover" is necessary,
# otherwise the QuantumCircuit header will be modified during the discovery.
test:
	python3 -m unittest discover -s test -v
