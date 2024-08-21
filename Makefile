SHELL := /bin/bash
.ONESHELL:

env:
	python3 -m venv venv
	. venv/bin/activate
	pip install -r requirements.txt


dev:
	. venv/bin/activate
	python3 src/main.py


release:
	. venv/bin/activate
	pyinstaller src/main.py --onefile --noconfirm --name psd-atlas


install:
	make release
	sudo cp dist/psd-atlas /usr/local/bin/


clean:
	rm build/ dist/ -r
