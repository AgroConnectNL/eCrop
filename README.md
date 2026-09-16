# eCrop
eCrops standard

Licensed under [CC BY 4.0](LICENSE).

## Repository layout

- [`openapi/ecrop.yaml`](openapi/ecrop.yaml) — the OpenAPI specification, source of truth for the standard.
- [`docs/`](docs/) — Swagger UI docs site, published via GitHub Pages ([getting started](docs/getting-started.md), [enabling Pages](docs/enabling-pages.md)).
- [`docs/guides/`](docs/guides/) — use-case-specific implementation guides for particular integrations (e.g. [Loonwerkportaal](docs/guides/implementatie-instructie-loonwerkportaal.md)).
- [`examples/`](examples/) — sample requests and responses.
- [`CHANGELOG.md`](CHANGELOG.md) — notable changes to the standard.

Pushes to `main` that touch `openapi/**` are linted (`.github/workflows/validate.yml`); pushes touching `docs/**` or `openapi/**` rebuild and publish the docs site (`.github/workflows/publish.yml`).
