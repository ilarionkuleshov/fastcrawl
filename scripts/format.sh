#!/bin/bash
set -e

packages=("fastcrawl/" "examples/")

for package in "${packages[@]}"; do
    echo "Isort formatting for $package package..."
    isort $package

    echo "Autoflake formatting for $package package..."
    autoflake $package

    echo "Black formatting for $package package..."
    black $package

    echo "Flake8 checking for $package package..."
    flake8 $package

    echo "Pylint checking for $package package..."
    pylint $package

    echo "Mypy checking for $package package..."
    mypy $package
done
