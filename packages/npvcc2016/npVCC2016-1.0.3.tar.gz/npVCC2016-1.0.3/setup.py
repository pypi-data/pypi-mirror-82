# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['npvcc2016',
 'npvcc2016.PyTorch',
 'npvcc2016.PyTorch.Lightning',
 'npvcc2016.PyTorch.Lightning.datamodule',
 'npvcc2016.PyTorch.dataset']

package_data = \
{'': ['*']}

install_requires = \
['pytorch-lightning>=0.10.0,<0.11.0',
 'torch>=1.6.0,<2.0.0',
 'torchaudio>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'npvcc2016',
    'version': '1.0.3',
    'description': 'npVCC2016: Python loader of npVCC2016 speech corpus',
    'long_description': '# `npVCC2016` - Python loader of npVCC2016Corpus\n[![PyPI version](https://badge.fury.io/py/npVCC2016.svg)](https://badge.fury.io/py/npVCC2016)\n![Python Versions](https://img.shields.io/pypi/pyversions/npVCC2016.svg)  \n\n`npVCC2016` is a Python loader set for [npVCC2016 non-parallel speech corpus](https://github.com/tarepan/npVCC2016Corpus).  \nFor machine learning, corpus/dataset is indispensable - but troublesome - part.  \nWe need portable & flexible loader for streamline development.  \n`npVCC2016` is the one!!  \n\n## Demo\n\nPython/PyTorch  \n\n```bash\npip install npVCC2016\n```\n\n```python\nfrom npVCC2016.PyTorch.dataset.waveform import NpVCC2016\n\ndataset = NpVCC2016(".", train=True, download=True)\n\nfor datum in dataset:\n    print("Yeah, data is acquired with only two line of code!!")\n    print(datum) # (datum, label) tuple provided\n``` \n\n`npVCC2016` transparently downloads corpus, structures the data and provides standarized datasets.  \nWhat you have to do is only instantiating the class!  \n\n## APIs\nCurrent `npVCC2016` support PyTorch.  \nAs interface, PyTorch\'s `Dataset` and PyTorch-Lightning\'s `DataModule` are provided.  \nnpVCC2016 corpus is speech corpus, so we provide `waveform` dataset and `spectrogram` dataset for both interfaces.  \n\n- PyTorch\n  - (pure PyTorch) dataset\n    - waveform: `NpVCC2016`\n    - spectrogram: `NpVCC2016_spec`\n  - PyTorch-Lightning\n    - waveform: `NpVCC2016DataModule`\n    - spectrogram: `NpVCC2016_spec_DataModule`\n\n### Extendibility\n`waveform` dataset has easy-to-extend structure.  \nBy overiding hook functions, you can customize preprocessing for your machine-learning tasks.  \nPlease check `dataset`-`waveform` file.  \n',
    'author': 'Tarepan',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tarepan/npVCC2016',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
