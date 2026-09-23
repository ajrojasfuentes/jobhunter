# Changelog

Notable project changes are recorded here using
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) categories and
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Version 0.1.0 identifies the initial local project baseline. It has not been
tagged or published. Subsequent working-tree improvements remain under
Unreleased until a release is explicitly prepared.

## [Unreleased]

### Added

- SQLModel 0.0.46 integration for the FastAPI health response, with compatible
  SQLAlchemy 2.0.54 available for future persistence.
- Validated Pydantic Settings configuration with an optional dotenv file and
  a `JOBHUNTER_` environment prefix.
- An application factory for explicit configuration and isolated test instances.
- Layered import contracts and automatic independence checks for feature modules.
- Configuration, app-isolation, and OpenAPI contract tests.
- GitHub Actions checks for formatting, lint, architecture, coverage, and builds.
- Weekly Dependabot updates for uv dependencies and GitHub Actions.
- Root ignore rules, EditorConfig, and a documented environment example.
- English setup instructions and a detailed software audit in `docs/AUDIT.md`.

### Changed

- Health responses now use a required literal `status` field in a SQLModel
  schema; the HTTP 200 response and `{"status": "ok"}` body remain unchanged.
- Health handling is asynchronous and remains independent of external services.
- OpenAPI reads the application version from installed package metadata.
- Test clients now manage application lifespan and use fresh application instances.
- Coverage includes all application packages and branches, with a 90% minimum.
- Technical documentation, comments, and configuration labels are standardized
  in English.
- Dependency resolution has been refreshed against stable releases, with an
  explicit Pydantic V2 constraint and compatible transitive versions preserved.

### Fixed

- Package discovery failures in Import-linter caused by missing package markers.
- Incomplete coverage reports that omitted the configuration module.
- Application settings that previously had no effect on startup configuration.

### Removed

- The placeholder `jobhunter` console command that only printed a greeting;
  use `uv run --locked uvicorn jobhunter.main:app` to start the API.
- The obsolete Spanish baseline report, superseded by the verified audit and
  this project history.

## [0.1.0] - 2026-09-22

Initial local project baseline; this entry records project creation, not a
published release.

### Added

- A Python 3.14 project using the `src` layout, uv dependency locking, and the
  uv_build backend.
- A FastAPI application with central router composition and a health module.
- A `GET /health` endpoint returning HTTP 200 and `{"status": "ok"}`.
- Five pytest checks for application loading, health-route registration,
  response status, response body, and JSON content type.
- Initial Ruff, Import-linter, and branch-coverage configuration.
- A shared configuration placeholder, project README, and MIT license.
