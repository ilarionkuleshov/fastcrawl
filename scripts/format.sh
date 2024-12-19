set -e

echo "Isort formatting..."
isort fastcrawl/

echo "Autoflake formatting..."
autoflake fastcrawl/

echo "Black formatting..."
black fastcrawl/

echo "Flake8 checking..."
flake8 fastcrawl/

echo "Pylint checking..."
pylint fastcrawl/

echo "Mypy checking..."
mypy fastcrawl/
