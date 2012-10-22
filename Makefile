clean:
	rm *.pyc

setup-dev:
	pip install -r requirements/development.txt

test:
	clear
	nosetests -dsvx --with-yanc --with-coverage --cover-package=mail_reply_cleaner test_*.py

@PHONY: clean setup-dev test
