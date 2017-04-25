[![Build Status](https://travis-ci.org/kota7/kgschart.svg?branch=master)](https://travis-ci.org/kota7/kgschart)

kgschart
==========
Parse KGS Rank Graph into Data


## Installation

The installation is easiest with [anaconda](https://anaconda.org/)/[miniconda](https://conda.io/miniconda.html) python distribution, since it automatically resolves
dependencies on scientific computation libraries such as `numpy`, `scipy`, and `scikit-learn`.

The package has been tested on miniconda on Linux for python versions `2.7`, `3.4`, `3.5`, and `3.6`.


### anaconda/miniconda users

If you use python distribution based on anaconda or miniconda based environment, first, install required packages by `conda` command:

```bash
conda install numpy pillow scipy pandas scikit-learn matplotlib pip
```

Then, install `kgschart` package by:

```bash
git clone --depth 1 https://github.com/kota7/kgschart.git
pip install --no-deps kgschart
```
Note that we should use `--no-deps` flag since required packages are already installed by `conda`.


Alternatively, download the package directly from GitHub

```bash
pip install --no-deps git+https://github.com/kota7/kgschart
```


### Official Python (non-conda) users

The `kgschart` package works also on official (non-conda) Python.

The following command tries to install the package along with the dependencies.

```bash
git clone --depth 1 https://github.com/kota7/kgschart.git
pip install kgschart
```

Alternatively, download the package directly from GitHub

```bash
pip install git+https://github.com/kota7/kgschart
```

Depending on the environment and Python versions, the package may not work as expeted.  You would need to set up required packages on your own.
The required packages are
`numpy` `pillow` `scipy` `pandas` `scikit-learn` and `matplotlib`.


## Quick Installation Check

If the installation is successful, following commands should run with no error.
```python
from kgschart import KgsChart
from pkg_resources import resource_stream
with resource_stream('kgschart', 'example/leela-ja_JP.png') as f:
    k = KgsChart(f)
k.parse()
print(k.data.head())
#                        time      rate
#0 2016-03-21 22:19:01.165048  1.762470
#1 2016-03-22 13:51:03.495146  1.762470
#2 2016-03-23 05:23:05.825242  1.776722
#3 2016-03-23 20:55:08.155340  2.040380
#4 2016-03-24 12:27:10.485436  2.232779
```

