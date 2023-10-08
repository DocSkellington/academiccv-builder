build:
	pipenv run python example.py

dependencies:
	mkdir .venv
	pipenv install --dev

release: build
	pipenv run python -m build
	zip release -r \
		dist/academiccv_builder-1.0.0-py3-none-any.whl \
		dist/academiccv_builder-1.0.0.tar.gz \
		example.py example.json output/ resources/ \
		README.md License

clean:
	rm -rf output
	rm -rf dist

nuke: clean
	rm -rf .venv
	rm -r Pipfile.lock