# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

---

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## Introduction

> TODO: Write a few words about the package here

## Quick start

> TODO: Quick presentation of packkage usage

### Installing the package

> TODO: Explain installation procedure

This package is not (yet?) distributed on [pypi](https://pypi.org/). As such it cannot be installed directly using pip.

You can however install it from the git repository directly using SSH credentials:

- Using [pip](https://pip.pypa.io/en/stable/):

```bash
pip install git+{{ cookiecutter.repo_url }}
```

- Using [poetry](https://python-poetry.org/):

```bash
poetry add git+{{ cookiecutter.repo_url }}
```

### Using the package

> TODO: Show more advanced usages

## Contributing

> TODO: Tell fellow developpers how to contribute to the package.

1. First clone the repository

```bash
git clone {{ cookiecutter.repo_url }}
```

2. Install the package

This project relies on the dependency manager [poetry](https://python-poetry.org/). Make sure it is installed then go into the project directory and install the package:

```bash
poetry install
```

3. Serve the documentation and check the contribution guide :smile:

```bash
poetry shell
mkdocs serve
```
