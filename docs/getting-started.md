# Getting started

This page introduces the eCrop standard and how to work with the OpenAPI specification in this repository.

## Where things live

- [`openapi/ecrop.yaml`](../openapi/ecrop.yaml) — the OpenAPI specification, the source of truth for the standard.
- [`docs/index.html`](index.html) — a Swagger UI page that renders the specification.
- [`usecases/`](../usecases/) — business cases: descriptions, sample requests and responses, example overrides and implementation guides.

## Viewing the docs locally

Open `docs/index.html` in a browser. It loads the spec from `../openapi/ecrop.yaml` directly, so no build step is required.
