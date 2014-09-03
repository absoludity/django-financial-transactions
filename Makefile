DJANGO_SETTINGS_MODULE=test_settings
VENV=.virtualenv
PYTHON=${VENV}/bin/python
PIP=${VENV}/bin/pip
NOSETESTS=${VENV}/bin/nosetests
DJANGO_ADMIN=./manage.py
DATABASE=/tmp/test_financial_transactions.db

install-deps: .virtualenv/lib/python2.7/site-packages/categories

install-test-deps: .virtualenv/lib/python2.7/site-packages/nose

setup-database: ${DATABASE}

test: setup-database
	DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE} ${NOSETESTS} financial_transactions

${DATABASE}:
	DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE} ${DJANGO_ADMIN} syncdb
	DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE} ${DJANGO_ADMIN} migrate

.virtualenv/lib/python2.7/site-packages/nose:
	${PIP} install -r test_requirements.txt

.virtualenv/lib/python2.7/site-packages/categories:
	${PYTHON} setup.py develop

.PHONY: install-test-deps test clean
