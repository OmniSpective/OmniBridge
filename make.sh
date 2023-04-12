#!/bin/bash

function coverage() {
    echo "Running coverage..."
    pipenv run coverage run -m pytest && pipenv run coverage report -m
    echo "Coverage completed."
}

function lint() {
    echo "Running lint..."
    ruff check . && pipenv run mypy .
    echo "Lint completed."
}

function test() {
    echo "Running tests..."
    pipenv run python -m pytest tests
    echo "Tests completed."
}

function run_all() {
    coverage # tests are already executed in coverage
    lint
}

if [ "$1" == "coverage" ]; then
    coverage
elif [ "$1" == "lint" ]; then
    lint
elif [ "$1" == "test" ]; then
    test
elif [ "$1" == "all" ]; then
    run_all
else
    echo "Invalid command. Usage:"
    echo "./make.sh coverage"
    echo "./make.sh lint"
    echo "./make.sh test"
    echo "./make.sh all"
fi
