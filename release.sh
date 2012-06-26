#!/bin/bash
set -e

pip install -q --upgrade pep8 autopep8
#pip install -q --upgrade autopep8

if ! python setup.py test; then
	echo "The test suite failed. Fix it!"
	exit 1
fi

autopep8 -i *.py

# commented some errors temporarly, TODO: remove them and fix the code
pep8 --max-line-length=180 --ignore=E502,E128,E123,E127,E125 src

echo "Please don't run this as a user. This generates a new release for PyPI. Press ^C to exit or Enter to continue."
read


# Clear old distutils stuff
rm -rf build dist MANIFEST &> /dev/null

# Build installers, etc. and upload to PyPI
# python setup.py register sdist bdist_wininst upload

#python setup.py register sdist build_sphinx upload upload_sphinx
python setup.py register sdist upload

