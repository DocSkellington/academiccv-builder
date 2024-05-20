build:
	pipenv run python example.py

dependencies:
	mkdir .venv
	pipenv install --dev
	
documentation: dependencies
	pipenv run python -m mkdocs build

release: documentation
	pipenv run python -m build
	zip release -r \
		dist/academiccv_builder-2.0.0-py3-none-any.whl \
		dist/academiccv_builder-2.0.0.tar.gz \
		example.pyjson_example/ output/ resources/ \
		site/ \
		README.md License

clean:
	rm -rf output
	rm -rf dist

nuke: clean
	rm -rf .venv
	rm -r Pipfile.lock