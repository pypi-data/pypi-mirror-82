[![GitHub top language](https://img.shields.io/github/languages/top/FHPythonUtils/FHDoc.svg?style=for-the-badge)](../../)
[![Codacy grade](https://img.shields.io/codacy/grade/[codacy-proj-id].svg?style=for-the-badge)](https://www.codacy.com/manual|gh/FHPythonUtils/FHDoc)
[![Repository size](https://img.shields.io/github/repo-size/FHPythonUtils/FHDoc.svg?style=for-the-badge)](../../)
[![Issues](https://img.shields.io/github/issues/FHPythonUtils/FHDoc.svg?style=for-the-badge)](../../issues)
[![License](https://img.shields.io/github/license/FHPythonUtils/FHDoc.svg?style=for-the-badge)](/LICENSE.md)
[![Commit activity](https://img.shields.io/github/commit-activity/m/FHPythonUtils/FHDoc.svg?style=for-the-badge)](../../commits/master)
[![Last commit](https://img.shields.io/github/last-commit/FHPythonUtils/FHDoc.svg?style=for-the-badge)](../../commits/master)
[![PyPI Downloads](https://img.shields.io/pypi/dm/fhdoc.svg?style=for-the-badge)](https://pypi.org/project/fhdoc/)
[![PyPI Version](https://img.shields.io/pypi/v/fhdoc.svg?style=for-the-badge)](https://pypi.org/project/fhdoc/)



# 🙌 FHDoc - Python documentation generator



Python docstring-based documentation generator for lazy perfectionists.

- [🙌 FHDoc - Python documentation generator](#-fhdoc---python-documentation-generator)
	- [Features](#features)
	- [Do you need fhdoc?](#do-you-need-fhdoc)
	- [Examples](#examples)
	- [Usage](#usage)
		- [💻 From command line](#-from-command-line)
		- [📦 As a Docker image](#-as-a-docker-image)
		- [📝 As a GitHub Pages manager](#-as-a-github-pages-manager)
		- [🐏 Deploy on Read the Docs](#-deploy-on-read-the-docs)
		- [📋 Build static HTML](#-build-static-html)
		- [🧩 As a module](#-as-a-module)
	- [Installation](#installation)
	- [Development](#development)
	- [Changelog](#changelog)

## Features

- [PEP 257](https://www.python.org/dev/peps/pep-0257/),
  [Google](http://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings),
  [Sphinx](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html)
  and [reStructuredText](https://www.python.org/dev/peps/pep-0287/)
  docstrings support. All of them are converted to a valid Markdown.
- Works with [Django](https://www.djangoproject.com/) and [Flask](https://palletsprojects.com/p/flask/) apps
- Can be used locally, or
  [right on GitHub](https://github.com/vemel/fhdoc/blob/master/docs/README.md) or even deployed on
  [GitHub Pages](https://vemel.github.io/fhdoc/) and [Read the Docs](https://fhdoc.readthedocs.io/)!
- Signatures for every class, function, property and method.
- Support for type annotations. Even for the ones from the `__future__`!
- Nice list of all modules in [Modules](https://github.com/vemel/fhdoc/blob/master/docs/MODULES.md)
- Gather all scattered `README.md` in submodules to one place
- Find related source code from every doc section.
- Make links by just adding `module.import.String` to docs.
- Do you use type annotations? Well, you get auto-discovery of related modules for free!

## Do you need fhdoc?

You definitely *do* if you:

- prefer to automate documentation builds
- work with a team and plan to simplify knowledge sharing
- want to show your project without navigating through a source code
- build `Django` or `Flask` applications, and even if you do not
- are proud of your project and not afraid to show it
- love Open Source

And probably *do not* if you:

- not very into docstrings and type annotations
- like to abstract a documentation away from the way things really are
- use [Pandas docstrings](https://pandas.pydata.org/pandas-docs/stable/development/contributing_docstring.html)
  as they are not supported yet

## Examples

- [All documentation](https://vemel.github.io/fhdoc/) in this project
- [Main](https://github.com/vemel/fhdoc/blob/master/examples/main_example.py) with [generated output](https://github.com/vemel/fhdoc/tree/master/docs/examples/main_example.md)
- [RST docstrings](https://github.com/vemel/fhdoc/blob/master/examples/rst_docstrings.py) with [generated output](https://github.com/vemel/fhdoc/tree/master/docs/examples/rst_docstrings.md)
- [Google docstrings](https://github.com/vemel/fhdoc/blob/master/examples/google_docstrings.py) with [generated output](https://github.com/vemel/fhdoc/tree/master/docs/examples/google_docstrings.md)
- [PEP 257 docstrings](https://github.com/vemel/fhdoc/blob/master/examples/pep257_docstrings.py) with [generated output](https://github.com/vemel/fhdoc/tree/master/docs/examples/pep257_docstrings.md)
- [Sphinx docstrings](https://github.com/vemel/fhdoc/blob/master/examples/sphinx_docstrings.py) with [generated output](https://github.com/vemel/fhdoc/tree/master/docs/examples/sphinx_docstrings.md)
- [Type annotations](https://github.com/vemel/fhdoc/blob/master/examples/typed.py) with [generated output](https://github.com/vemel/fhdoc/tree/master/docs/examples/typed.md)
- [Comment-style type annotations](https://github.com/vemel/fhdoc/blob/master/examples/comment_typed.py) with [generated output](https://github.com/vemel/fhdoc/tree/master/docs/examples/comment_typed.md)

## Usage

### 💻 From command line

Just go to your favorite project that has lots of docstrings but missing
auto-generated docs and let `fhdoc` do the thing.

```bash
cd ~/my/project

# build documentation *.md* files in docs/* directory
fhdoc

# or provide custom output directory: output_dir/*
fhdoc -o output_dir

# generate docs only for my_module, but exclude migrations
fhdoc my_module --exclude my_module/migrations

# generate documentation for deployment
fhdoc --external `git config --get remote.origin.url` -n ProjectName
```

Navigate to `docs/README.md` to check your new documentation!

### 📦 As a Docker image

- Install [Docker](https://docs.docker.com/install/)
- Pull latest `fhdoc` version and tag it

```bash
docker pull docker.pkg.github.com/vemel/fhdoc/fhdoc:latest
docker tag docker.pkg.github.com/vemel/fhdoc/fhdoc:latest fhdoc
```

- Generate docs for `ProjectName` in current directory

```bash
# for Python 3 project
docker run -v `pwd`:/app fhdoc -n ProjectName

# for Python 2 project
PYTHON_VER=2 docker run -v `pwd`:/app fhdoc -n ProjectName

# generate documentation for deployment
docker run -v `pwd`:/app fhdoc --external `git config --get remote.origin.url` -n ProjectName
```

### 📝 As a GitHub Pages manager

With `--external` CLI flag, `fhdoc` generates all required configuration
for [GitHub Pages](https://pages.github.com/), so you just need to setup your
GitHub repository.

```bash
# Generate documentation that points to master branch
# do not use custom output location, as `GitHub Pages`
# works only with `docs` directory
fhdoc --external `git config --get remote.origin.url`

# or specify GitHub url directly
fhdoc --external https://github.com/<user>/<project>/blob/master/
```

- Generate documentation with `--external` flag as shown above, do not use `--output`
  flag, only `docs` folder is supported by `GitHub Pages`
- Commit and push all changes a to `master` branch.
- Set your GitHub project `Settings` > `GitHub Pages` > `Source` to `master branch /docs folder`

All set! You can change `docs/_config.yml` to add your own touch.

With `--external` flag links to your source are absolute and point to your GitHub repo. If you
still want to have relative links to source, e.g. for using docs locally,
generate docs to another folder

```bash
# `docs_local` folder will be created in your project root
# you probably want to add it to .gitignore
fhdoc -o docs_local
```

### 🐏 Deploy on Read the Docs

With `--external` CLI flag, `fhdoc` generates all required configuration
for [Read the Docs](https://readthedocs.org/), so you just need to to add your
GitHub repository to `Read the Docs`.

```bash
# Generate documentation that points to master branch
# do not use custom output location, as `GitHub Pages`
# works only with `docs` directory
fhdoc --external `git config --get remote.origin.url`

# or specify GitHub url directly
fhdoc --external https://github.com/<user>/<project>/blob/master/
```

- Generate documentation with `--external` flag as shown above, do not use `--output`
  flag, only `docs` folder is supported by `Read the Docs`
- Commit and push all changes a to `master` branch.
- Add your repository on [Read the Docs](https://readthedocs.org/)

All set! You can change `.readthedocs.yml` and `mkdocs.yml` to add your own touch.

### 📋 Build static HTML

```bash
# Generate documentation that points to master branch
# with source links pointing to your repository
# this command also creates `mkdocs.yml`
fhdoc --external `git config --get remote.origin.url`

# Run mkdocs to build HTML
mkdocs build
```

### 🧩 As a module

```python
from fhdoc.generator import Generator
from fhdoc.utils.path_finder import PathFinder

# this is our project root directory
repo_path = Path.cwd()

# this little tool works like `pathlib.Path.glob` with some extra magic
# but in this case `repo_path.glob("**/*.py")` would do as well
path_finder = PathFinder(repo_path, "**/*.py")

# no docs for tests and build
path_finder.exclude("tests/*", "build/*")

# initialize generator
fhdoc = Generator(
	input_path=repo_path,
	output_path=repo_path / 'output',
	source_paths=path_finder.glob("**/*.py")
)

# generate all docs at once
fhdoc.generate_docs()

# or generate just for one doc
fhdoc.generate_doc(repo_path / 'my_module' / 'source.py')

# and generate index.md file
fhdoc.generate_index()

# navigate to `output` dir and check results
```

## Installation

Install using `pip` from PyPI

```bash
pip install fhdoc
```

or directly from GitHub if you cannot wait to test new features

```bash
pip install git+https://github.com/vemel/fhdoc.git
```

## Development

- Install [pipenv](https://pypi.org/project/pipenv/)
- Run `pipenv install -d`
- Use `black` formatter in your IDE

## Changelog

Changelog can be found in [Releases](https://github.com/vemel/fhdoc/releases)
