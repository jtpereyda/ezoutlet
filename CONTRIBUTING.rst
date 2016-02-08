Issues and Bugs
===============
If you have a bug report or idea for improvement, please create an issue on GitHub, or a pull request with the fix.

Contributors
============

Pull Request Checklist
----------------------

1. Verify tests pass:

        tox

2. If you have PyCharm, use it to see if your changes introduce any new static analysis warnings.

3. Modify CHANGELOG.rst to say what you changed.

Maintainers
===========

Release Checklist
-----------------

1. Verify tests pass.

2. Build distributions:

        python setup.py sdist bdist_wheel

3. Upload to testpypi if changes impact PyPI (e.g., if README changed):

        twine upload -r test  dist\ezoutlet-x.y.z-py2-none-any.whl dist\ezoutlet-0.0.1-dev3.zip

3. Upload to pypi:

        twine upload dist\ezoutlet-x.y.z-py2-none-any.whl dist\ezoutlet-0.0.1-dev3.zip
