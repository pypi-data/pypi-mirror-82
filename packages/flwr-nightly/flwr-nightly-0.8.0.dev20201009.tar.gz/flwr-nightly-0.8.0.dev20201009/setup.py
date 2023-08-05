# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src/py'}

packages = \
['flwr',
 'flwr.client',
 'flwr.client.grpc_client',
 'flwr.common',
 'flwr.proto',
 'flwr.server',
 'flwr.server.grpc_server',
 'flwr.server.strategy',
 'flwr_example',
 'flwr_example.pytorch',
 'flwr_example.pytorch_imagenet',
 'flwr_example.quickstart',
 'flwr_example.quickstart_pytorch',
 'flwr_example.tensorflow',
 'flwr_experimental',
 'flwr_experimental.baseline',
 'flwr_experimental.baseline.common',
 'flwr_experimental.baseline.config',
 'flwr_experimental.baseline.dataset',
 'flwr_experimental.baseline.model',
 'flwr_experimental.baseline.plot',
 'flwr_experimental.baseline.tf_cifar',
 'flwr_experimental.baseline.tf_fashion_mnist',
 'flwr_experimental.baseline.tf_hotkey',
 'flwr_experimental.logserver',
 'flwr_experimental.ops',
 'flwr_experimental.ops.compute']

package_data = \
{'': ['*']}

install_requires = \
['google>=2.0.3,<3.0.0',
 'grpcio>=1.27.2,<2.0.0',
 'numpy>=1.18.1,<2.0.0',
 'protobuf>=3.12.1,<4.0.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses==0.6'],
 'baseline': ['tensorflow-cpu==2.3.0',
              'boto3>=1.12.36,<2.0.0',
              'boto3_type_annotations>=0.3.1,<0.4.0',
              'paramiko>=2.7.1,<3.0.0',
              'docker>=4.2.0,<5.0.0',
              'matplotlib>=3.2.1,<4.0.0'],
 'examples-pytorch': ['torch==1.6.0',
                      'torchvision==0.7.0',
                      'tqdm>=4.48.2,<5.0.0'],
 'examples-tensorflow': ['tensorflow-cpu==2.3.0'],
 'http-logger': ['tensorflow-cpu==2.3.0',
                 'boto3>=1.12.36,<2.0.0',
                 'boto3>=1.12.36,<2.0.0',
                 'boto3_type_annotations>=0.3.1,<0.4.0',
                 'boto3_type_annotations>=0.3.1,<0.4.0',
                 'paramiko>=2.7.1,<3.0.0',
                 'docker>=4.2.0,<5.0.0',
                 'matplotlib>=3.2.1,<4.0.0'],
 'ops': ['boto3>=1.12.36,<2.0.0',
         'boto3_type_annotations>=0.3.1,<0.4.0',
         'paramiko>=2.7.1,<3.0.0',
         'docker>=4.2.0,<5.0.0']}

setup_kwargs = {
    'name': 'flwr-nightly',
    'version': '0.8.0.dev20201009',
    'description': 'Flower - A Friendly Federated Learning Research Framework',
    'long_description': '# Flower (`flwr`) - A Friendly Federated Learning Research Framework\n\n[![GitHub license](https://img.shields.io/github/license/adap/flower)](https://github.com/adap/flower/blob/main/LICENSE)\n[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/adap/flower/blob/main/CONTRIBUTING.md)\n![Build](https://github.com/adap/flower/workflows/Build/badge.svg)\n\nFlower (`flwr`) is a research framework for building federated learning systems. The\ndesign of Flower is based on a few guiding principles:\n\n* **Customizable**: Federated learning systems vary wildly from one use case to\n  another. Flower allows for a wide range of different configurations depending\n  on the needs of each individual use case.\n\n* **Extendable**: Flower originated from a research project at the Univerity of\n  Oxford, so it was build with AI research in mind. Many components can be\n  extended and overridden to build new state-of-the-art systems.\n\n* **Framework-agnostic**: Different machine learning frameworks have different\n  strengths. Flower can be used with any machine learning framework, for\n  example, [PyTorch](https://pytorch.org),\n  [TensorFlow](https://tensorflow.org), or even raw [NumPy](https://numpy.org/)\n  for users who enjoy computing gradients by hand.\n\n* **Understandable**: Flower is written with maintainability in mind. The\n  community is encouraged to both read and contribute to the codebase.\n\n## Documentation\n\n* [Documentation](https://flower.dev)\n  * [Quickstart](https://flower.dev/quickstart.html)\n  * [Installation](https://flower.dev/installation.html)\n\n## Flower Usage Examples\n\nA number of examples show different usage scenarios of Flower (in combination\nwith popular machine learning frameworks such as PyTorch or TensorFlow). To run\nan example, first install the necessary extras:\n\n[Usage Examples Documentation](https://flower.dev/examples.html)\n\nAvailable [examples](src/py/flwr_example):\n\n* [Quickstart: Keras & MNIST](src/py/flwr_example/quickstart)\n* [PyTorch & CIFAR-10](src/py/flwr_example/pytorch)\n* [PyTorch & ImageNet](src/py/flwr_example/pytorch_imagenet)\n* [TensorFlow & Fashion-MNIST](src/py/flwr_example/tensorflow)\n\n## Flower Baselines\n\n*Coming soon* - curious minds can take a peek at [src/py/flwr_experimental/baseline](src/py/flwr_experimental/baseline).\n\n## Flower Datasets\n\n*Coming soon* - curious minds can take a peek at [src/py/flwr_experimental/baseline/dataset](src/py/flwr_experimental/baseline/dataset).\n\n## Citation\n\nIf you publish work that uses Flower, please cite Flower as follows: \n\n```bibtex\n@article{beutel2020flower,\n  title={Flower: A Friendly Federated Learning Research Framework},\n  author={Beutel, Daniel J and Topal, Taner and Mathur, Akhil and Qiu, Xinchi and Parcollet, Titouan and Lane, Nicholas D},\n  journal={arXiv preprint arXiv:2007.14390},\n  year={2020}\n}\n```\n\nPlease also consider adding your publication to the list of Flower-based publications in the docs, just open a Pull Request.\n\n## Contributing to Flower\n\nWe welcome contributions. Please see [CONTRIBUTING.md](CONTRIBUTING.md) to get\nstarted!\n',
    'author': 'The Flower Authors',
    'author_email': 'enquiries@flower.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://flower.dev',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)
