# eCrop

eCrop — the new REST API standard for crop-related data

## Licence

The eCrop standard, including its OpenAPI definitions, may be used free of charge and at your own responsibility. It is published under the Creative Commons Attribution 4.0 International licence (CC BY 4.0). For more information, see the [licence summary](LICENSE-SUMMARY.md) (in English and Dutch) and the [complete licence text](LICENSE).

## About eCrop

### AgroConnect: the background

AgroConnect is the Dutch non-profit consultation platform that promotes eBusiness in agriculture. The association brings together parties in the agrifood sector — suppliers, agricultural cooperatives, the food industry, service providers, advisory organisations and government bodies — to agree on data sharing. Through working groups and product groups, members steer the standards for electronic data interchange in the supply chain, including the standards for the crop sector managed by the Crop product group.

### From EDI-Crop to eCrop

Since 2017, crop data in the sector has been exchanged using the EDI-Crop message set: three XML messages — the cropping scheme message (CroppingScheme), the crop recording message (CropRecording) and the advice message (CroppingAdvice) — each strictly defined in an XSD schema and structured around the hierarchy Farm → Field → CropField → Task → Operation → TreatmentZone. This XML/EDI-based model has served for years as the basis for exchanging cropping schemes, crop registrations, and fertilisation and crop protection advice between growers, advisers and buyers.

eCrop is the modern successor to the XML EDI-Crop standard. Based on the eCrop data model, eCrop leaves the XML/EDI paradigm behind in favour of a contemporary, RESTful JSON API. This aligns with the broader movement within AgroConnect to reformulate sector standards as modern, developer-friendly web interfaces rather than message formats.

This transition is more than a technical choice: functionally, a REST API offers substantial advantages over exchanging EDI and SOAP/XML messages. Whereas EDI messages copy data periodically and in batches from one party to another, a REST API retrieves data directly from the source — current, at the moment it is requested, rather than an outdated snapshot file. This aligns with the FAIR principle (Findable, Accessible, Interoperable, Reusable): data remains unambiguously findable and retrievable at the source holder, is directly reusable by multiple parties in the chain, and no longer needs to be redundantly stored and synchronised in everyone's own copy. For growers, advisers and buyers, this means less re-keying and fewer synchronisation errors, faster insight into the current situation in the field, and a lower threshold for connecting new systems and parties to the chain.

### Set-up as a REST API and conformance to standards

eCrop is fully specified as an OpenAPI 3.0 document (current draft version 1.1.0) and published as a ready-to-use specification that platforms can start working with directly. The API conforms to AgroConnect's AGRI API Style Guide (AASG), which prescribes unambiguous rules for, among other things, version management, security, URL and resource naming, RESTful principles, payload conventions and HTTP status codes — with the aim that all APIs in the agri and food sector feel as though they were designed by a single team.

The AASG itself is deliberately not detached from national standards: it builds on the NL API Strategy and the REST API Design Rules (ADR) of the Knowledge Platform APIs / Forum Standaardisatie (the Dutch Standardisation Forum). This means eCrop aligns not only with the agrifood sector but also with the broader Dutch government standard for APIs.

Both the AASG and eCrop itself also conform to established international standards, including the specifications of the IETF (HTTP semantics, RFCs for, among others, Problem Details, JSON Patch and date/time notations), the W3C (web standards on which HTTP and JSON-related technology are built), and ISO (such as ISO 8601 for date and time formats). For exchanging geographic field information, eCrop also aligns with the standards of the Open Geospatial Consortium (OGC). By building on these widely supported international standards rather than sector-specific agreements of its own, eCrop remains interoperable with systems and applications far beyond the Dutch agrifood sector.

### Overview of supported operations

The eCrop API is structured around a number of functional categories (tags), each focused on part of the crop production process:

| Category | Description | Example operations |
| --- | --- | --- |
| general | General operations, incl. API health check and publication of the OpenAPI document | `GET /health`, `GET /openapi.json` |
| parties | Retrieving parties (growers, suppliers, contractors) and the growers a supplier or contractor is authorized for | `GET /growers`, `GET /suppliers`, `GET /contractors`, `GET /contractors/{...}/{...}/growers` |
| plots | Retrieving and maintaining basic (non-geo) plot information; contractors can retrieve the plots of the growers they are authorized for | `GET`/`POST`/`PUT`/`DELETE .../plots`, `GET /contractors/.../growers/.../plots` |
| plot-geometry | Retrieving the geo-information of plots (boundary, entry point, AB line) via an OGC API Features / JSON-FG-compliant API; the features of one plot are selected with the `plotSchemeId` and `plotId` query parameters | `GET /collections/plots`, `GET /collections/plots/items`, `GET /collections/plots/items/{featureId}` |
| crops | Retrieving and maintaining crop information | `GET`/`POST`/`PUT`/`DELETE .../crops` |
| delivery | Registering inbound deliveries (products delivered by suppliers to growers), by the grower or by an authorized supplier | `POST`/`PUT`/`DELETE .../inbound-deliveries`, `GET /suppliers/{...}/{...}/growers` |
| farm level registration | Retrieving production locations and registration of (non-crop-related) tasks and operations at farm level | `GET .../production-locations`, `POST`/`PUT`/`DELETE .../production-locations/.../tasks` |
| plot level registration | Registration of (non-crop-related) tasks and operations at plot level, by the grower or by an authorized contractor | `POST`/`PUT`/`DELETE .../plots/.../tasks` (for contractors also `PATCH`, with a JSON Patch document) |
| crop level registration | Registration of crop-related tasks and operations | `POST`/`PUT`/`DELETE .../crops/.../tasks` |
| footprint | Retrieving yearly footprint declarations (PEFCR) of growers, for use by an external footprint calculation tool | `GET /footprint-declarations` |

In addition to these functional operations, the API provides generic, consistent support for pagination, major versioning via HTTP headers, and standardised error handling in accordance with the AASG — so that platforms built on eCrop behave seamlessly like other AgroConnect-compliant APIs.

#### Business-case distributions

Not every platform needs every operation. The complete specification therefore serves several business cases, and for each business case a distribution is published that contains only the operations (and the request bodies, responses, parameters, schemas and examples) of that business case:

| Business case | Distribution |
| --- | --- |
| [Contractor planning: retrieving a grower's plots and geometry, and registering the performed tasks](usecases/contractor-task-planning/README.md) | [`ecrop-contractor-task-planning.yaml`](https://agroconnectnl.github.io/eCrop/openapi/ecrop-contractor-task-planning.yaml) |
| [Farm Management System sync of executed field operations](usecases/fms-crop-operations-sync/README.md) | [`ecrop-fms-crop-operations-sync.yaml`](https://agroconnectnl.github.io/eCrop/openapi/ecrop-fms-crop-operations-sync.yaml) |
| [Supplier inbound delivery registration](usecases/supplier-inbound-delivery-registration/README.md) | [`ecrop-supplier-inbound-delivery-registration.yaml`](https://agroconnectnl.github.io/eCrop/openapi/ecrop-supplier-inbound-delivery-registration.yaml) |
| [Footprint calculation: providing crop data to an external footprint calculation tool](usecases/footprint-calculation/README.md) | [`ecrop-footprint-calculation.yaml`](https://agroconnectnl.github.io/eCrop/openapi/ecrop-footprint-calculation.yaml) |

The complete specification and the documentation (with a selector per business case) are published at [agroconnectnl.github.io/eCrop](https://agroconnectnl.github.io/eCrop/); see [`openapi/README.md`](openapi/README.md) for how the distributions are built.

### Planned extensions

eCrop is deliberately not a final destination: the standard is being actively developed further. The draft version 1.1.0 of the eCrop OpenAPI spec has already been extended with geographic information on plots (boundary, entry point, AB line) based on the OGC JSON-FG standard (the `plot-geometry` category), with operations for contractors and for the exchange of executed tasks between growers' farm management systems, contractors' systems and the crop registration platform, and with the retrieval of footprint declarations (the `footprint` category). The roadmap includes, among other things:

- **Returning calculated footprint data**: the operation with which an external footprint calculation tool returns the calculated footprint to the platform (an asynchronous process), as the follow-up of the retrieval of footprint declarations.
- **Footprint and sustainability data**: extending eCrop to exchange Footprint scores, as a basis for a broader set of sustainability calculations to be added in later versions.
- **Additional business cases**: further business cases with their own distribution of the specification, see [`usecases/`](usecases/).
- **OGC API**: possible additional support for the OGC API standard for the plot geo-information.

### Acknowledgements

eCrop was developed through the collaboration of the following organisations in the AgroConnect eCrop working group:

- AgroVision ([www.agrovision.com](https://www.agrovision.com))
- Dacom ([www.cropx.nl](https://www.cropx.nl))
- Farmmaps ([www.farmmaps.net](https://www.farmmaps.net))
- GreenlinQdata ([www.greenlinqdata.nl](https://www.greenlinqdata.nl))
- MPS ([www.my-mps.com](https://www.my-mps.com))

More information: [www.agroconnect.nl](https://www.agroconnect.nl) | [github.com/AgroConnectNL](https://github.com/AgroConnectNL)

## Repository layout

- [`openapi/ecrop.yaml`](openapi/ecrop.yaml) — the OpenAPI specification, source of truth for the standard.
- [`docs/`](docs/) — Swagger UI docs site, published via GitHub Pages ([getting started](docs/getting-started.md), [enabling Pages](docs/enabling-pages.md)).
- [`usecases/`](usecases/) — one folder per business case, holding everything for that case: the description (actors, scope, operations used, an example flow with a sequence diagram, and open questions), the example overrides for its distribution of the specification (`examples.yaml`) and, where available, an implementation guide (e.g. [Loonwerkportaal](usecases/contractor-task-planning/implementatie-instructie.nl.md)); see [`usecases/README.md`](usecases/README.md) for the current list.
- [`scripts/`](scripts/) — repo tooling, e.g. [`build-distribution.py`](scripts/build-distribution.py), which builds a business-case specific distribution of the specification, and [`check-usecases-structure.js`](scripts/check-usecases-structure.js), which checks every business case in `usecases/` has the required sections.
- [`CHANGELOG.md`](CHANGELOG.md) — notable changes to the standard.

Pushes to `main` that touch `openapi/**` are linted (`.github/workflows/validate.yml`); every push to `main` rebuilds the business-case distributions and publishes them with the docs site on GitHub Pages, and tags `v*` attach them to a GitHub release (`.github/workflows/publish.yml`; see [`openapi/README.md`](openapi/README.md)); pushes touching `usecases/**` are checked for the required structure (`.github/workflows/check-usecases.yml`).
