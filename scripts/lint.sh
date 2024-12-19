set -e

echo "Isort checking..."
isort fastcrawl/ --check

echo "Autoflake checking..."
autoflake fastcrawl/ --check

echo "Black checking..."
black fastcrawl/ --check

echo "Flake8 checking..."
flake8 fastcrawl/

echo "Pylint checking..."
pylint fastcrawl/

echo "Mypy checking..."
mypy fastcrawl/
