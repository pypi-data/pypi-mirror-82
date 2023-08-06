# dotsplit
> Transform dot-delimited strings to array of python strings.
```python
>>> import dotsplit
>>> dotsplit('group.0.section.a.seat.3')
['group', '0', 'section', 'a', 'seat', '3']
```

[![Downloads](https://pepy.tech/badge/dotsplit/month)](https://pepy.tech/project/dotsplit/month)
[![Supported Versions](https://img.shields.io/pypi/pyversions/dotsplit.svg)](https://pypi.org/project/dotsplit)
[![Contributors](https://img.shields.io/github/contributors/wilmoore/dotsplit.py.svg)](https://github.com/wilmoore/dotsplit.py/graphs/contributors)

## Installation
> dotsplit is available on PyPI:
###### poetry
```console
❯ poetry install dotsplit
```
###### pip
```console
❯ python -m pip install dotsplit
```

## Testing
> to run the unit test suite, cd to the root directory and run:
```
❯ poetry install
❯ poetry run pytest
```

## Licenses
[![GitHub license](https://img.shields.io/github/license/wilmoore/dotsplit.py.svg)](https://github.com/wilmoore/dotsplit.py/blob/master/license)
