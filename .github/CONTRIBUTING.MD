requirerments:
* Python >=3.8

steps:
1. Fork and clone this repository
2. pip install pipenv
3. pipenv install (in the root folder)
4. pipenv shell

### Run linter locally
inside pipenv shell, execute 
```
ruff check ./
```

### Run tests locally
```
pipenv run python -m pytest
```