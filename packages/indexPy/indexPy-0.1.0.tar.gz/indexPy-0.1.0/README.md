# indexPy

indexPy is a Python3 module designed for working with PyPI API; an API for viewing Python package data.

## Installation

The easiest way to install `indexPy` is through PIP.

`pip install indexPy` or `pip3 install indexPy`

**Before installing**, ensure your Python version is 3.6 or above.

## Usage

With `indexPy`, you can access data from a package like it's package name, author,
contact information, URLs, releases, etc.

The following example demonstrates the standard use of `indexPy`.

```py
# Example 1
from indexPy.api import PackageInfo # Import the module
pkg = PackageInfo("requests") # Save the information
pkg.author
>>> 'Kenneth Reitz'
pkg.name
>>> 'requests'

# Example 2
from indexPy.api import PackageInfo # Import the module
pkg = PackageInfo("indexPy") # Save the information
pkg.author
>>> 'Angel Carias'
pkg.name
>>> 'indexPy'
```
