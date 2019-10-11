#!/bin/bash
rm -R _build
virtualenv ../venv
source ../venv/bin/activate
pip install sphinx
pip install sphinx-autodoc-typehints
pip install sphinx-rtd-theme
pip install pymongo
pip install pandas
sphinx-build ./ _build/
make html
deactivate
rm -R ../venv
