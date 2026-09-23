# Jobhunter

A minimal, modular FastAPI starter with a system liveness endpoint. The project
uses Python 3.14, Pydantic V2, SQLModel, and uv. It does not implement job-search
features or connect to a database yet.

## Local setup

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run
these commands from the repository root:

```bash
uv python install
uv sync --locked
uv run --locked uvicorn jobhunter.main:app --reload
```

Python is selected from `.python-version`. Keep the dependency lockfile alongside
`pyproject.toml`; `--locked` rejects stale dependency metadata.
The development toolchain uses uv 0.12.18.

The server listens at http://127.0.0.1:8000. Use `--reload` only for local
development. Stop it with Ctrl+C. For a non-reloading local process:

```bash
uv run --locked uvicorn jobhunter.main:app
```

There is no custom `jobhunter` console command. Run the ASGI application with
Uvicorn as shown above.

## HTTP interface

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/health` | Returns HTTP 200 and `{"status": "ok"}` |
| GET | `/docs` | Interactive Swagger UI |
| GET | `/redoc` | ReDoc documentation |
| GET | `/openapi.json` | OpenAPI schema |

`/health` is a liveness check: it confirms that the API can respond. It does
not verify database readiness or external services. It remains independent of
future persistence infrastructure. The response is a SQLModel schema with a
required `status: Literal["ok"]` field and is not a database table.

## Configuration

The default application title is `jobhunter`. Optionally copy
`.env.example` to `.env` and set `JOBHUNTER_APP_NAME`.

Settings are validated once when an application instance is created. Precedence
is explicit `Settings(...)` values, environment variables, the `.env` file in
the current working directory, then defaults. Blank titles are rejected.
Unrelated dotenv entries are ignored. Settings are immutable after creation.

Use `create_app(settings)` to supply explicit configuration in tests or another
ASGI entry point. The exported `jobhunter.main:app` uses startup configuration
and gets its API version from installed package metadata. Restart the process
after changing settings.

## Structure and architecture

```text
src/jobhunter/
├── main.py                  # Application factory and ASGI entry point
├── api/router.py            # Router composition
├── core/config.py           # Shared startup settings
└── modules/health/
    ├── router.py            # Liveness endpoint
    └── schemas.py           # SQLModel response schema
tests/
├── conftest.py              # Isolated app and lifespan-aware client fixtures
├── core/test_config.py
├── modules/health/test_router.py
└── test_app.py
```

Every application package has an `__init__.py`. Import-linter enforces the
dependency direction `main → api → modules → core`; higher layers may also
use lower layers directly. Feature packages under `modules/*` must be
independent. Add new top-level packages to the layer contract deliberately.

SQLModel provides the schema integration with FastAPI and brings a compatible
SQLAlchemy dependency. Pydantic is declared directly because configuration code
imports it. There is one resolved distribution per dependency in `uv.lock`.
Add table models, an engine, request-scoped sessions, and migrations only when
the database requirements are defined; do not add database probes to liveness.

## Development checks

```bash
uv run --locked ruff format --check .
uv run --locked ruff check .
uv run --locked lint-imports
uv run --locked pytest --cov --cov-report=term-missing
uv pip check
uv build --no-sources
```

To apply formatting, run `uv run --locked ruff format .`.
Tests use fresh application instances and a context-managed TestClient.
Coverage includes all application packages and branches, with a 90% minimum.
The initial corrected template achieves 100%; that does not replace meaningful
tests for future behavior.

A known upstream Starlette/AnyIO deprecation warning remains visible in tests.
See [the audit](docs/AUDIT.md) for evidence and limitations.

## Dependency updates and CI

`uv.lock` records exact versions. To refresh compatible stable dependencies:

```bash
uv lock --upgrade
uv sync --locked
```

Run all development checks after an update. Respect transitive constraints:
Pydantic currently requires a specific `pydantic-core` version. Do not upgrade
that component independently. SQLModel 0.0.45 introduced UTC-aware database
datetime handling; account for it when adding persistence.

GitHub Actions runs on pull requests, pushes to `main`, and manual dispatch.
It checks formatting, lint, import contracts, tests with coverage, and package
builds. Actions are pinned to verified commit SHAs, the token has read-only
contents permission, and superseded runs are cancelled. Dependabot checks uv
dependencies and action versions weekly. Deployment and publishing are not
configured. No external service credentials are needed for CI.

## Documentation

- [Software audit](docs/AUDIT.md): inspected state, dependencies, findings,
  validation evidence, and remaining limitations.
- [Changelog](docs/CHANGELOG.md): initial baseline and unreleased improvements.
- [License](LICENSE): MIT.

Technical references:
[SQLModel with FastAPI](https://sqlmodel.tiangolo.com/tutorial/fastapi/response-model/),
[Pydantic settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/),
[uv on GitHub Actions](https://docs.astral.sh/uv/guides/integration/github/),
and [SQLModel release notes](https://sqlmodel.tiangolo.com/release-notes/).
