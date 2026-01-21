lint:
	@echo "Running linters..."
	@uv run ruff check . --fix

isort:
	@echo "Sorting imports..."
	@uv run isort apps cv_worker

black:
	@echo "Formatting code..."
	@uv run black apps cv_worker

mypy:
	@echo "Running type checker..."
	@uv run mypy

# Run all quality checks
check: isort black lint mypy
	@echo "All checks passed"
