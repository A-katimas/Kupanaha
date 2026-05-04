PYTHON = python3
UV = uv
SRC = a_maze_ing.py
VENV = .venv
CONFIG ?= config.txt

run:
	@if [ -f "$(CONFIG)" ]; then \
		uv run $(SRC) $(CONFIG); \
	else \
		echo "⚠️  Fichier $(CONFIG) introuvable, lancement sans config..."; \
		uv run $(SRC); \
	fi

install:
	@if [ ! -d $(VENV) ]; then \
		@echo "Création de l'environnement..."; \
		@uv sync --extra dev; \
	fi

build:
	@tar -czvf mazetar.tar mazetar/

debug:
	@uv run python -m pdb $(SRC)

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -name "*.pyc" -delete
	@rm -rf $(VENV)
	@rm -rf uv.lock
	@rm -rf maze.txt
	@echo "all is clear"

lint:
	@uv run $(PYTHON) -m flake8 . --extend-exclude .venv
	@uv run $(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs


lint-strict:
	@uv run $(PYTHON) -m flake8 . --extend-exclude .venv
	@uv run $(PYTHON) -m mypy . --strict

.PHONY: run install debug clean lint lint-strict build