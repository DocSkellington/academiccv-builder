build:
	pipenv run python example.py

dependencies:
	mkdir .venv
	pipenv install --dev

clean:
	rm -rf output
	rm -rf dist

nuke: clean
	rm -rf .venv
	rm -r Pipfile.lock