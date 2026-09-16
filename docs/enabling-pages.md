# Enabling GitHub Pages

GitHub Pages is not enabled for this repository yet. The docs site (Swagger UI over `openapi/ecrop.yaml`) can be published once it is.

## Steps

1. Repo **Settings → Pages → Source: GitHub Actions**.
2. In [`.github/workflows/publish.yml`](../.github/workflows/publish.yml), uncomment the `push` trigger block so it fires automatically on changes to `docs/**` or `openapi/**`:

   ```yaml
   on:
     push:
       branches: [main]
       paths:
         - "docs/**"
         - "openapi/**"
     workflow_dispatch:
   ```

Until then, the workflow only runs manually (`workflow_dispatch`, via the Actions tab) — this avoids failing CI runs on every push, since `actions/deploy-pages` errors if no Pages site exists yet.

`validate.yml` (OpenAPI linting) is unaffected by any of this and runs on every push/PR touching `openapi/**` regardless of Pages status.
