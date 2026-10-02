# openapi

- [`ecrop.yaml`](ecrop.yaml) — the AgroConnect eCrop OpenAPI 3.0 specification, source of truth for the standard.

The eCrop OpenAPI spec can also be viewed online on SwaggerHub: [app.swaggerhub.com/apis-docs/vanraaijadvies/eCropAPI/1.1.0](https://app.swaggerhub.com/apis-docs/vanraaijadvies/eCropAPI/1.1.0?view=uiDocs)

## Business-case distributions

`ecrop.yaml` serves several business cases (see [`examples/`](../examples/)). Every operation carries an
`x-usecases` list (`all` = in every distribution, `unassigned` = in no distribution yet), and
[`redocly.yaml`](../redocly.yaml) has one `apis:` entry per business case. A distribution contains only the
operations of its business case, and only the request bodies, responses, parameters, schemas and examples
those operations need.

Build one (or more) into `dist/` (requires Node.js and Python with PyYAML):

```bash
python scripts/build-distribution.py contractor-task-planning
```

Examples that must differ per business case (e.g. identifier schemes) are overridden in
[`usecases/<name>.examples.yaml`](usecases/): whole entries of `components/examples`, plus the `example` of
named `components/schemas` and `components/parameters`.
