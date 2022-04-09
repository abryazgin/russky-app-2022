.PHONY: test lint pretty plint run

BIN = venv/bin/
CODE = russky
SRC = .
TEST = tests

test:
	PYTHONPATH=$(SRC) $(BIN)pytest --verbosity=2 --showlocals --strict-markers $(TEST)

lint:
	$(BIN)flake8 --jobs 4 --statistics --show-source $(CODE) $(TEST)
	$(BIN)mypy $(CODE)
	$(BIN)black --target-version py36 --skip-string-normalization --line-length=119 --check $(CODE) $(TEST)

pretty:
	$(BIN)isort $(CODE) $(TEST)
	$(BIN)black --target-version py36 --skip-string-normalization --line-length=119 $(CODE) $(TEST)
	$(BIN)unify --in-place --recursive $(CODE) $(TEST)

plint: pretty lint

run:
	$(BIN)uvicorn russky.app:app --reload
