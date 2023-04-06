# Install

requirerments:
* Python 3.11

steps:
1. git clone https://github.com/tmpOrgName/tmp.git
2. pip install pipenv
3. pipenv install (in the root folder)
4. pipenv shell

# Run linter locally

inside pipenv shell, execute `ruff check ./`

# Usage

Available in CLI with the following arguments:

* -m / --model
* -p / --prompt

single model example:
`python main.py -m chatgpt -p hello`

multi model example:
`python main.py -m chatgpt -p hello -m dalle -p goodbye`

Note that the order of specification matters, meaning that in the above example, chatgpt will get the prompt `hello` and dalle will get the prompt `goodbye`
