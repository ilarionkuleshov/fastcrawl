#!/bin/bash
set -e

packages=("fastcrawl/" "examples/")

for package in "${packages[@]}"; do
    echo "Isort checking for $package package..."
    isort $package --check

    echo "Autoflake checking for $package package..."
    autoflake $package --check

    echo "Black checking for $package package..."
    black $package --check

    echo "Flake8 checking for $package package..."
    flake8 $package

    echo "Pylint checking for $package package..."
    pylint $package

    echo "Mypy checking for $package package..."
    mypy $package
done
