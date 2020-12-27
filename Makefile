.PHONY: ship test


ship:
	python setup.py sdist bdist_wheel
	twine upload dist/* --skip-existing


test:
	pipenv run flake8 archiveis
	pipenv run coverage run test.py
	pipenv run coverage report -m
