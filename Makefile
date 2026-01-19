lint:
	@echo "Running linters..."
	@uv run ruff check . --fix

isort:
	@echo "Sorting imports..."
	@uv run isort apps cv_worker

black:
	@echo "Formatting code..."
	@uv run black apps cv_worker

ty:
	@echo "Running type checker..."
	@uv run ty check

# Run all quality checks
check: isort black lint ty
	@echo "All checks passed"
