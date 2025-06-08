set -e

echo "Ruff checking..."
ruff check fastcrawl/ --select I
ruff check fastcrawl/

echo "Mypy checking..."
mypy fastcrawl/
