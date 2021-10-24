
dist:
	source venv/bin/activate; \
	pip install --upgrade setuptools wheel twine; \
	python setup.py sdist bdist_wheel; \
	python -m twine upload dist/*

clean:
	rm -rf vertex2tex.egg-info build dist

