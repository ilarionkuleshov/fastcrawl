#!/bin/bash
set -e

packages=("fastcrawl" "examples")

for package in "${packages[@]}"; do
    echo "Isort formatting for $package..."
    isort "$package/"

    echo "Autoflake formatting for $package..."
    autoflake "$package/"

    echo "Black formatting for $package..."
    black "$package/"

    echo "Flake8 checking for $package..."
    flake8 "$package/"

    echo "Pylint checking for $package..."
    pylint "$package/"

    echo "Mypy checking for $package..."
    mypy "$package/"
done
