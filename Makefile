flake:
	flake8 kurier tests

develop:
	python setup.py develop

test:
	py.test -q -s --cov kurier --cov-report term-missing --tb=native