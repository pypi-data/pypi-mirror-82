# Python-LFU

Pure Python library implementing LFU cache system with O(1) cache eviction
scheme. The algorithm is based on the following [research paper](http://dhruvbird.com/lfu.pdf).

Along, with cache it also provides a generic Double Linked List implementation
for your use.

## Installation

Install the library with pip:

```sh
$ pip install python-lfu
```

## Usage

Python-LFU, has a very easy to use API. Primarily, you will initialize an
object with maximum limit and use standard get/put to cache and fetch data.

Example:

```python
>>> from lfu_cache import LFUCache
>>> cache = LFUCache(2)
>>> cache.put(1, 1)
>>> cache.put(2, 2)
>>> cache.get(1)
1
>>> cache.put(3, 3) # will evict 2
>>> cache.get(2) # Raises KeyError
>>>
```

Key, value can be of `Any` type.

Complete documentation for Python-LFU is available on [ReadTheDocs](https://python-lfu.readthedocs.io/en/latest/)

## Development

Python-LFU supports Python 3.6, 3.7, 3.8 and possibly later (not tested yet) so
its best to setup multiple Python environment using
[pyenv](https://github.com/pyenv/pyenv). We extensively use typing and use mypy
to validate it. You can quickly set it up like so:

```sh
pyenv virtualenv 3.6.12 python_lfu
pyenv local python_lfu  3.7.9 3.8.6
pip install -r requirements.dev.txt
```

Run tests using `tox` or `make test`.

## Contributing

We welcome contributions! If you would like to hack on Python-LFU, please
follow these steps:

1. Fork this repository
2. Make your changes
3. Install the requirements in `requirements.dev.txt`
4. Submit a pull request after running `make check` (ensure it does not error!)

Please give us adequate time to review your submission. Thanks!
