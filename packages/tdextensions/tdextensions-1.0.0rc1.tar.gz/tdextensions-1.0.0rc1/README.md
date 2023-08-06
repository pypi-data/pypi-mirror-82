
# Teradata ML Extensions

Extensions to the core teradataml library by Teradata Consulting to aid in field development work around BYOM, STO, RTO and AnalyticOps solutions.

## Requirements

Python 3.6+


## Usage

See the pypi [guide](./docs/pypi.md) for some usage notes. 


## Installation

To install the latest release, just do

```
pip install tdextensions
```

To build from source, it is advisable to create a Python venv or a Conda environment 

Python venv:
```
python -m venv tdextension
source tdextension/bin/activate
```

Install library from local folder using pip:

```
pip install --upgrade .
```

Install library from package file

```
# first create the package
python setup.py sdist bdist_wheel

# install using pip
pip install dist/*.whl
```

## Testing

```
pytest --junitxml=test-results/junit.xml -v
```


    /var/opt/teradata/tdtemp/uiflib/scriptlog

## Building 

```
python -m pip install --user --upgrade setuptools wheel

python setup.py sdist bdist_wheel

twine upload -u td-aoa -p <user@pass> dist/*

```

