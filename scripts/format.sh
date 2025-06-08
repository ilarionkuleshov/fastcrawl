set -e

echo "Ruff formatting..."
ruff format fastcrawl/
ruff check fastcrawl/ --select I --fix
ruff check fastcrawl/
ruff format tests/
ruff check tests/ --select I --fix

echo "Mypy checking..."
mypy fastcrawl/
