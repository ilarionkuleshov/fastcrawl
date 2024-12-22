#!/bin/bash
set -e

packages=("fastcrawl" "examples")

for package in "${packages[@]}"; do
    echo "Isort checking for $package..."
    isort "$package/" --check

    echo "Autoflake checking for $package..."
    autoflake "$package/" --check

    echo "Black checking for $package..."
    black "$package/" --check

    echo "Flake8 checking for $package..."
    flake8 "$package/"

    echo "Pylint checking for $package..."
    pylint "$package/"

    echo "Mypy checking for $package..."
    mypy "$package/"
done
