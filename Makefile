.PHONY: test lint pretty plint run

CODE = russky
SRC = .
TEST = tests
OTEL_ENVS = ""
HTTP_PORT = 8080

test:
	PYTHONPATH=$(SRC) pytest --verbosity=2 --showlocals --strict-markers $(TEST)

lint:
	flake8 --jobs 4 --statistics --show-source $(CODE) $(TEST)
	mypy $(CODE)
	black --target-version py36 --skip-string-normalization --line-length=119 --check $(CODE) $(TEST)

pretty:
	isort $(CODE) $(TEST)
	black --target-version py36 --skip-string-normalization --line-length=119 $(CODE) $(TEST)
	unify --in-place --recursive $(CODE) $(TEST)

plint: pretty lint

run:
	uvicorn russky.app:app --host 0.0.0.0 --port $(HTTP_PORT)
