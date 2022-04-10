.PHONY: test lint pretty plint run

BIN = venv/bin/
CODE = russky
SRC = .
TEST = tests
OTEL_ENVS = ""

add_local_env_file:
    # https://www.elastic.co/guide/en/apm/get-started/current/open-telemetry-elastic.html
	echo EOF > .env
	export OTEL_RESOURCE_ATTRIBUTES=service.name=russky-app-2022,service.version=1.0,deployment.environment=dev
	export OTEL_EXPORTER_OTLP_ENDPOINT=https://localhost:8200
	#export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer an_apm_secret_token"
	EOF

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
