# GitHub Pages

GitHub Pages is enabled for this repository, with **GitHub Actions** as source (Settings → Pages). The site is
published at <https://agroconnectnl.github.io/eCrop/>: a Swagger UI page over `openapi/ecrop.yaml` and over the
business-case distributions, plus the specification files themselves under `/openapi/`.

## How it is published

[`.github/workflows/publish.yml`](../.github/workflows/publish.yml):

1. builds and lints the business-case distributions (`scripts/build-distribution.py`);
2. assembles the site (`scripts/assemble-site.py`): `docs/`, `openapi/` and the distributions;
3. on pushes to `main` (and manual runs from `main`), deploys the site with `actions/deploy-pages`;
4. on tags `v*`, attaches `ecrop.yaml` and the distributions to the GitHub release.

Pull requests only run steps 1 and 2, so a broken override or distribution is caught before it reaches `main`.

`validate.yml` (OpenAPI linting of the complete specification) is independent of this and runs on every push/PR
touching `openapi/**`.

## If Pages needs to be set up again

Repo **Settings → Pages → Source: GitHub Actions**, then run the workflow once from the Actions tab
(`workflow_dispatch`).
