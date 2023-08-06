# Pip example package

[Tutorial about how to distribute pip packages](https://packaging.python.org/tutorials/packaging-projects/)

**Dependencies**

`pip install --upgrade setuptools wheel`

`pip install --upgrade twine`

**Build**

`python setup.py sdist bdist_wheel`

**Upload**

`twine upload  dist/*`
