# Software Audit: Jobhunter

## Document control

| Field | Value |
| --- | --- |
| Assessment date | 2026-09-22 (America/Costa_Rica) |
| Application version | 0.1.0 |
| Assessment target | Local working tree after template corrections and SQLModel integration |
| Git baseline | `main`, commit `1ea59f5` (`Initial commit`) |
| Release status | Local development; no new commit, tag, push, or publication |
| Assessment type | Source, configuration, dependency, test, and packaging review |
| Scope classification | Minimal FastAPI template with a liveness module |

This report supersedes the earlier Spanish baseline report. Historical observations
are distinguished from the corrected working tree. It is a point-in-time technical
assessment, not a security certification or a guarantee about future dependency
releases.

## Executive assessment

The corrected template is operational within the tested Linux/CPython environment.
All 12 tests pass, all application statements and branches are covered, both import
contracts pass, and distribution builds succeed. The installed wheel also passes a
real Uvicorn HTTP smoke test in a clean environment containing only locked runtime
dependencies.

SQLModel 0.0.46 is integrated as the public response schema for FastAPI, using
Pydantic V2. SQLAlchemy 2.0.54 is installed once through SQLModel's dependency
graph. A separate in-memory SQLite round-trip confirmed basic ORM interoperability.
The application does not create an engine, sessions, tables, or database files.

The original architectural discovery and coverage defects are resolved. Remaining
limitations are an upstream deprecation warning, unexecuted hosted CI, and the
deliberately narrow platform and functional scope. Source files remain uncommitted
at the user's request.

## Scope and method

The review covered:

- All ten application Python files and four test/support Python files.
- Project and build metadata, Python selection, resolved dependency graph, and
  installed distributions.
- README, license, environment example, editor settings, ignore rules, CI, and
  Dependabot configuration.
- The previous baseline report, including its failing import contract, incomplete
  coverage discovery, placeholder CLI, and disconnected configuration.
- Runtime HTTP behavior, OpenAPI, configuration precedence, application isolation,
  source distribution, and wheel installation.

Evidence was collected through file inspection, PyPI release metadata, GitHub
release/tag metadata, uv resolution, automated tests, coverage, Ruff,
Import-linter, actionlint, and an isolated package/runtime smoke test. Stable
release selection excluded prereleases, development versions, and fully yanked
releases.

Not performed: penetration testing, advisory-database scanning, performance/load
testing, remote Git synchronization, deployment, production database validation,
or hosted GitHub Actions execution. Latest-version checks are not vulnerability
audits. Dependency metadata compatibility and passing tests provide evidence for
the exercised paths, not proof of every possible integration.

## Architecture and implementation

### Package inventory

| File or package | Responsibility |
| --- | --- |
| `src/jobhunter/__init__.py` | Package marker without startup or CLI behavior |
| `main.py` | `create_app(settings)` factory and exported ASGI `app` |
| `api/__init__.py`, `api/router.py` | Package marker and router composition |
| `core/__init__.py`, `core/config.py` | Shared, validated startup configuration |
| `modules/__init__.py` | Feature-module package |
| `modules/health/__init__.py` | Health-module package |
| `modules/health/router.py` | Asynchronous GET liveness handler |
| `modules/health/schemas.py` | SQLModel response schema, without `table=True` |

The dependency direction is `main → api → modules → core`. Higher layers may
depend directly on any lower layer; reverse imports are rejected. The layer
contract is exhaustive for top-level application modules. A wildcard independence
contract covers feature packages under `jobhunter.modules.*`, including future
siblings. With only one feature, the independence rule cannot yet demonstrate
separation between two real business modules.

Each package now has an explicit `__init__.py`, so imports, static discovery,
coverage, and packaging agree on the application layout. There are no database,
repository, service, authentication, frontend, or job-search layers.

### API contract

`GET /health` returns HTTP 200, content type `application/json`, and
`{"status": "ok"}`. `HealthResponse(SQLModel)` requires
`status: Literal["ok"]`; OpenAPI publishes the same constraint. Invalid status
values are rejected by Pydantic in the compatibility smoke test.

The handler performs no blocking work or external I/O. Health is a liveness
signal, not a dependency readiness probe. It is safe to call without provisioning
a database. SQLModel integration does not make the response a persisted record.

FastAPI also exposes `/docs`, `/redoc`, and `/openapi.json`. The previous
baseline observed a 404 at `/` and a redirect from `/health/` to `/health`;
routing policy was not changed. These framework defaults are not new business
endpoints.

### Startup and configuration

`Settings` inherits from Pydantic Settings. It reads `JOBHUNTER_APP_NAME`,
optionally from the working directory's UTF-8 `.env` file. Explicit constructor
values take precedence over process environment, then dotenv values, then
defaults. Whitespace is stripped, empty titles are rejected, unrelated dotenv
keys are ignored, and the resulting settings object is frozen.

Settings are resolved when the application is created, rather than on each
request. No global settings cache is required. `create_app(settings)` supports
explicit test configuration and independent app state. The module-level `app`
is created on import, so invalid startup settings fail early.

OpenAPI's version comes from installed package metadata. Running `uv sync`
before startup is therefore required; manipulating `PYTHONPATH` alone is not a
supported installation procedure. The placeholder console entry point was removed.
The supported startup command is `uv run --locked uvicorn jobhunter.main:app`.

### Persistence boundary

SQLModel supplies Pydantic-compatible schemas and a SQLAlchemy integration point.
Only the schema side is used by application code today. There is no database URL,
driver selection, connection pool, request-session dependency, transaction policy,
or migration framework.

The isolated compatibility probe used a temporary table model, SQLite memory
storage, a session, an insert/commit, and a select. Those objects were confined to
the probe process and were not added to production code.

SQLModel 0.0.45 changed default database datetime handling to aware UTC values;
0.0.46 includes a related fix. There are no existing datetime fields or databases
to migrate in this project. Future persistence work must account for that behavior.

## Dependency and environment assessment

Observed environment: CPython 3.14.7, Linux x86_64, uv 0.12.18. Python 3.14.7
was the latest stable CPython offered by the installed uv catalog; 3.15.0rc2 was
excluded as a prerelease. The project requires `>=3.14` and selects the 3.14
series in `.python-version`. Later Python versions allowed by the metadata
have not been tested.

| Component | Resolved version | Assessment |
| --- | --- | --- |
| FastAPI | 0.141.1 | Latest stable checked on PyPI |
| Pydantic | 2.13.5 | Latest stable; project explicitly requires `>=2.13.5,<3` |
| Pydantic Settings | 2.15.0 | Latest stable |
| SQLModel | 0.0.46 | Latest stable; newly integrated |
| SQLAlchemy | 2.0.54 | Latest stable; satisfies SQLModel's `>=2.0.14,<2.1.0` |
| Uvicorn | 0.53.0 | Latest stable, standard extras enabled |
| HTTPX2 | 2.13.0 | Latest stable, test client dependency |
| Import-linter | 2.15 | Latest stable |
| pytest | 9.1.1 | Latest stable |
| pytest-cov | 7.1.0 | Latest stable |
| Ruff | 0.16.8 | Latest stable |
| uv / uv_build | 0.12.18 | Latest stable checked on PyPI |
| actions/checkout | 7.0.1 | Latest GitHub release; tag verified against pinned SHA |
| astral-sh/setup-uv | 10.2.0 | Latest GitHub release; tag verified against pinned SHA |
| actionlint | 1.7.12 | Local workflow validator; release checksum verified |

`uv lock --upgrade` resolved 42 entries including the project. The development
environment contains 40 compatible installed distributions. The lockfile's
Windows-only `colorama` and Emscripten-only `httpx2-jsfetch` are correctly
absent on Linux. The clean wheel environment contains 23 runtime dependencies
plus the application.

Every locked third-party package was compared against PyPI stable releases.
All match the latest stable version except **pydantic-core**:
Pydantic 2.13.5 requires **exactly 2.46.5**, while PyPI also offers 2.49.0.
Keeping 2.46.5 is required for compatibility; overriding that pin would violate
the installed Pydantic contract.

Pydantic remains a direct dependency because application configuration imports
`Field` directly. SQLAlchemy remains transitive because production code does
not import its API directly. These declarations do not install duplicate
Pydantic or SQLAlchemy distributions. HTTPX2 is intentional; no separate HTTPX
package was introduced.

The complete third-party lock snapshot follows. Versions are observational
evidence, not a separate dependency manifest; `uv.lock` remains authoritative.

| Distribution | Locked version |
| --- | --- |
| annotated-doc | 0.0.5 |
| annotated-types | 0.8.0 |
| anyio | 4.15.1 |
| click | 8.5.0 |
| colorama | 0.4.6 |
| coverage | 7.16.1 |
| fastapi | 0.141.1 |
| greenlet | 3.5.6 |
| grimp | 3.17 |
| h11 | 0.16.0 |
| httpcore2 | 2.13.0 |
| httptools | 0.8.0 |
| httpx2 | 2.13.0 |
| httpx2-jsfetch | 1.0 |
| idna | 3.20 |
| import-linter | 2.15 |
| iniconfig | 2.3.0 |
| markdown-it-py | 4.2.0 |
| mdurl | 0.1.2 |
| packaging | 26.3 |
| pluggy | 1.6.0 |
| pydantic | 2.13.5 |
| pydantic-core | 2.46.5 |
| pydantic-settings | 2.15.0 |
| pygments | 2.21.0 |
| pytest | 9.1.1 |
| pytest-cov | 7.1.0 |
| python-dotenv | 1.2.3 |
| pyyaml | 6.0.3 |
| rich | 15.0.0 |
| ruff | 0.16.8 |
| sqlalchemy | 2.0.54 |
| sqlmodel | 0.0.46 |
| starlette | 1.6.0 |
| truststore | 0.10.4 |
| typing-extensions | 4.16.0 |
| typing-inspection | 0.4.4 |
| uvicorn | 0.53.0 |
| uvloop | 0.22.1 |
| watchfiles | 1.3.0 |
| websockets | 17.1 |

## Quality controls and evidence

| Check | Observed result |
| --- | --- |
| `uv sync --locked` | Succeeded without dependency drift |
| `uv run --locked ruff check .` | Passed |
| `uv run --locked ruff format --check .` | Passed; all discovered files already formatted |
| `uv run --locked lint-imports --no-cache` | 2 contracts kept, 0 broken |
| `uv run --locked pytest --cov --cov-report=term-missing` | 12 tests passed |
| Application statement coverage | 29/29 statements covered |
| Application branch coverage | 2/2 branch destinations covered |
| Combined coverage | 100%; configured minimum is 90% |
| `uv pip check` | All 40 installed distributions compatible |
| `uv build --no-sources` | Source distribution and wheel built successfully |
| Wheel install with locked runtime dependencies | Passed in a clean temporary virtual environment |
| Actual Uvicorn HTTP smoke test | Health, environment title, and OpenAPI passed |
| SQLModel/Pydantic/SQLAlchemy probe | Validation and SQLite round-trip passed |
| actionlint 1.7.12 | Workflow accepted without diagnostics |

The test suite covers default settings, environment integration, dotenv loading,
environment-over-dotenv precedence, two invalid-title cases, three HTTP health
assertions, explicit application settings, app-state isolation, and the public
OpenAPI response/version contract. TestClient is context-managed, allowing
startup/shutdown handling, and each HTTP test gets a fresh application instance.

Coverage discovery now includes all application packages, including unimported
namespace packages if any are added later. The original 93% report omitted
`core/config.py`; measuring the complete old tree produced 67%. Current 100%
coverage reflects a very small application and does not establish production
readiness or coverage of third-party code.

## Findings register

Severity describes project impact within this template, not a CVSS score.

| ID | Severity | Finding and evidence | Disposition |
| --- | --- | --- | --- |
| JH-001 | Medium | Original Import-linter run failed to discover health; package markers were absent. | Resolved: explicit packages and two passing contracts. |
| JH-002 | Medium | Original coverage omitted unimported configuration and overstated coverage. | Resolved: complete discovery, branch coverage, and a 90% gate. |
| JH-003 | Low | Settings did not affect the application and accepted no environment configuration. | Resolved: validated settings wired into the app factory. |
| JH-004 | Low | CLI entry point only printed a greeting. | Resolved: removed stub and documented the actual ASGI command. |
| JH-005 | Low | Health schema allowed an arbitrary string-valued object. | Resolved: required literal status in SQLModel and OpenAPI contract tests. |
| JH-006 | Low | No root ignore rules; local coverage and bytecode appeared in Git status. | Resolved: cache, build, virtualenv, and dotenv exclusions; example retained. |
| JH-007 | Low | Missing development instructions and automated quality workflow. | Resolved locally: English README and validated CI configuration. Hosted execution pending. |
| JH-008 | Low | Starlette TestClient emits a deprecation warning for `anyio.abc.BlockingPortal`. | Open upstream limitation; tests pass and warning is not suppressed. |
| JH-009 | Informational | Most project files are still untracked; only README/LICENSE exist in the original commit. | Intentionally deferred: user prohibited committing. |
| JH-010 | Informational | Latest pydantic-core is newer than Pydantic's exact compatible requirement. | Accepted constraint: preserve 2.46.5 and update through Pydantic. |
| JH-011 | Informational | Only Linux/CPython 3.14.7 was exercised; no production persistence exists. | Scope limitation; validate target platforms and database when selected. |

No unresolved defect in the tested health/configuration paths was observed.
This statement does not imply that there are no vulnerabilities or undiscovered
defects outside the executed checks.

## CI and repository hygiene

The CI workflow runs on pull requests, pushes to `main`, and manual dispatch.
One Ubuntu job installs Python from the project selection, installs locked
dependencies, checks format/lint/architecture, runs coverage-gated tests, and
builds distributions. A ten-minute timeout and concurrency cancellation limit
stale work.

Actions are pinned to verified full commit SHAs. Repository contents permission
is read-only, checkout credentials are not persisted, and the workflow performs
no deployment or publication. No project secrets or third-party reporting
accounts are required. uv caching is enabled.

Dependabot is configured for weekly `uv` and `github-actions` updates with a
five-PR limit per ecosystem. This configuration is local until the repository is
pushed and the hosting service processes it. Branch protection and required
status checks are hosting settings and were not changed.

The local actionlint check validates workflow structure and expressions, not
GitHub runner execution. The clean-wheel HTTP and ORM probes were local audit
checks; they are not part of the project pytest suite or CI workflow.

## Remaining decisions and maintenance actions

1. When authorized, review and version the source, tests, lockfile, configuration,
   and documentation. No staging, commit, tag, or push was performed here.
2. After pushing, confirm the first hosted CI run and choose required branch
   protection checks.
3. Track the Starlette/AnyIO deprecation warning through compatible upstream
   updates; do not monkey-patch dependencies or globally suppress warnings.
4. When adding persistence, choose a database/driver, define transaction and
   session lifetimes, add migrations, and test against that database.
5. Expand integration and platform coverage only as the supported scope grows.
6. Re-run the documented checks for dependency updates; do not bypass the
   Pydantic core constraint to obtain a numerically newer release.

## Traceability and sources

- [Current setup and commands](../README.md)
- [Project metadata and quality configuration](../pyproject.toml)
- [Resolved dependency graph](../uv.lock)
- [CI workflow](../.github/workflows/ci.yml)
- [Dependabot configuration](../.github/dependabot.yml)
- [SQLModel release notes](https://sqlmodel.tiangolo.com/release-notes/)
- [SQLModel response models with FastAPI](https://sqlmodel.tiangolo.com/tutorial/fastapi/response-model/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [uv locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/)
- [uv Dependabot integration](https://docs.astral.sh/uv/guides/integration/dependabot/)
- [Import-linter contract types](https://import-linter.readthedocs.io/en/stable/contract_types/)
- [PyPI package metadata](https://pypi.org/project/sqlmodel/)
- [checkout 7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1)
- [setup-uv 10.2.0](https://github.com/astral-sh/setup-uv/releases/tag/v10.2.0)
- [actionlint 1.7.12](https://github.com/rhysd/actionlint/releases/tag/v1.7.12)

The former baseline was read before this assessment. Its observations remain
represented in the historical coverage comparison and findings register.
The initial local project history and current unreleased work are recorded
separately in the changelog.
