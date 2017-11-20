Data Portal APIs
================

# Scicence park data portal APIs

## Contents

- [Installation](#installation)
- [Development Workflow](#development-workflow)
- [Deployment](#deployment)

### Installation
Clone repo: 
```sh
git clone https://github.com/PharrellWANG/dataportalAPIs.git
cd dataportalAPIs
```

Make it your own:
```sh
rm -rf .git && git init
```
> :information_source: This re-initializes the repo and sets up your project.

Install the virtualenv:
```sh
virtualenv .venv -p `which python3`
```
Install the requirements
```sh
pip install -r requirements.txt
```

### Development Workflow
Activate the virtualenv
```sh
. ./venv.sh
```
> :information_source: This example is applicable for *zsh* shell.

Run scripts:
```sh
Python 1-*.py
```
### License
MIT