VENV=.virtualenv
PIP=${VENV}/bin/pip
DJANGO_ADMIN=./manage.py
DATABASE=/tmp/test_financial_transactions.db

test: ${VENV} ${DATABASE}
	${DJANGO_ADMIN} test financial_transactions

${VENV}:
	virtualenv ${VENV}
	${PIP} install -r test_requirements.txt
	

${DATABASE}:
	${DJANGO_ADMIN} syncdb
	${DJANGO_ADMIN} migrate

.PHONY: test
