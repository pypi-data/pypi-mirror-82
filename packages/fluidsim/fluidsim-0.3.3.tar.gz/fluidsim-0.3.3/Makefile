# Second tag after tip is usually the latest release
RELEASE=$(shell hg tags -T "{node|short}\n" | sed -n 2p)

develop:
	pip install -v -e .[dev] | grep -v link

develop_user:
	pip install -v -e .[dev] --user | grep -v link

clean_so:
	find fluidsim -name "*.so" -delete

clean_pyc:
	find fluidsim -name "*.pyc" -delete
	find fluidsim -name "__pycache__" -type d | xargs rm -rf

cleantransonic:
	find fluidsim -type d -name __pythran__ | xargs rm -rf
	find fluidsim -type d -name __python__ | xargs rm -rf
	find fluidsim -type d -name __numba__ | xargs rm -rf
	find fluidsim -type d -name __cython__ | xargs rm -rf

clean:
	rm -rf build

cleanall: clean clean_so cleantransonic

shortlog:
	@hg log -M -r$(RELEASE): --template '- {desc|firstline} (:rev:`{node|short}`)\n'

black:
	black -l 82 fluidsim scripts bench doc

tests:
	fluidsim-test -v

tests_mpi:
	mpirun -np 2 --oversubscribe fluidsim-test -v

_tests_coverage:
	mkdir -p .coverage
	coverage run -p -m fluidsim.util.testing -v
	TRANSONIC_NO_REPLACE=1 coverage run -p -m fluidsim.util.testing -v
	TRANSONIC_NO_REPLACE=1 mpirun -np 2 --oversubscribe coverage run -p -m fluidsim.util.testing -v

_report_coverage:
	coverage combine
	coverage report
	coverage html
	coverage xml
	@echo "Code coverage analysis complete. View detailed report:"
	@echo "file://${PWD}/.coverage/index.html"

coverage: _tests_coverage _report_coverage

coverage_short:
	mkdir -p .coverage
	TRANSONIC_NO_REPLACE=1 coverage run -p -m fluidsim.util.testing -v
	make _report_coverage

lint:
	pylint -rn --rcfile=pylintrc --jobs=$(shell nproc) fluidsim --exit-zero
