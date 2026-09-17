# eCrop

eCrop — the new REST API standard for crop-related data

Licensed under [CC BY 4.0](LICENSE).

## About eCrop

### AgroConnect: the background

AgroConnect is the Dutch non-profit consultation platform that promotes eBusiness in agriculture. The association brings together parties in the agrifood sector — suppliers, agricultural cooperatives, the food industry, service providers, advisory organisations and government bodies — to agree on data sharing. Through working groups and product groups, members steer the standards for electronic data interchange in the supply chain, including the standards for the crop sector managed by the Crop product group.

### From EDI-Crop to eCrop

Since 2017, crop data in the sector has been exchanged using the EDI-Crop message set: three XML messages — the cropping scheme message (CroppingScheme), the crop recording message (CropRecording) and the advice message (CroppingAdvice) — each strictly defined in an XSD schema and structured around the hierarchy Farm → Field → CropField → Task → Operation → TreatmentZone. This XML/EDI-based model has served for years as the basis for exchanging cropping schemes, crop registrations, and fertilisation and crop protection advice between growers, advisers and buyers.

eCrop is the modern successor to the XML EDI-Crop standard. Based on the eCrop data model, eCrop leaves the XML/EDI paradigm behind in favour of a contemporary, RESTful JSON API. This aligns with the broader movement within AgroConnect to reformulate sector standards as modern, developer-friendly web interfaces rather than message formats.

This transition is more than a technical choice: functionally, a REST API offers substantial advantages over exchanging EDI and SOAP/XML messages. Whereas EDI messages copy data periodically and in batches from one party to another, a REST API retrieves data directly from the source — current, at the moment it is requested, rather than an outdated snapshot file. This aligns with the FAIR principle (Findable, Accessible, Interoperable, Reusable): data remains unambiguously findable and retrievable at the source holder, is directly reusable by multiple parties in the chain, and no longer needs to be redundantly stored and synchronised in everyone's own copy. For growers, advisers and buyers, this means less re-keying and fewer synchronisation errors, faster insight into the current situation in the field, and a lower threshold for connecting new systems and parties to the chain.

### Set-up as a REST API and conformance to standards

eCrop is fully specified as an OpenAPI 3.0 document (current version 1.0.3) and published as a ready-to-use specification that platforms can start working with directly. The API conforms to AgroConnect's AGRI API Style Guide (AASG), which prescribes unambiguous rules for, among other things, version management, security, URL and resource naming, RESTful principles, payload conventions and HTTP status codes — with the aim that all APIs in the agri and food sector feel as though they were designed by a single team.

The AASG itself is deliberately not detached from national standards: it builds on the NL API Strategy and the REST API Design Rules (ADR) of the Knowledge Platform APIs / Forum Standaardisatie (the Dutch Standardisation Forum). This means eCrop aligns not only with the agrifood sector but also with the broader Dutch government standard for APIs.

Both the AASG and eCrop itself also conform to established international standards, including the specifications of the IETF (HTTP semantics, RFCs for, among others, Problem Details, JSON Patch and date/time notations), the W3C (web standards on which HTTP and JSON-related technology are built), and ISO (such as ISO 8601 for date and time formats). For exchanging geographic field information, eCrop also aligns with the standards of the Open Geospatial Consortium (OGC). By building on these widely supported international standards rather than sector-specific agreements of its own, eCrop remains interoperable with systems and applications far beyond the Dutch agrifood sector.

### Overview of supported operations

The eCrop API is structured around a number of functional categories (tags), each focused on part of the crop production process:

| Category | Description | Example operations |
| --- | --- | --- |
| general | General operations, incl. API health check | `GET /health` |
| parties | Retrieving parties (growers, suppliers, contractors) | `GET /growers`, `GET /suppliers`, `GET /contractors` |
| plots | Retrieving and maintaining basic (non-geo) plot information | `GET`/`POST`/`PUT`/`DELETE .../plots` |
| plot-geometry | Retrieving the geo-information of plots (boundary, entry point, AB line) via an OGC API Features / JSON-FG-compliant API | `GET /collections/plots`, `GET /collections/plots/items` |
| crops | Retrieving and maintaining crop information | `GET`/`POST`/`PUT`/`DELETE .../crops` |
| delivery | Registering inbound deliveries (products delivered by suppliers to growers) | `POST`/`GET .../inbound-deliveries` |
| farm level registration | Registration of (non-crop-related) tasks and operations at farm level | Tasks/Operations at Farm level |
| plot level registration | Registration of (non-crop-related) tasks and operations at plot level | Tasks/Operations at Plot level |
| crop level registration | Registration of crop-related tasks and operations | Tasks/Operations at Crop level |

In addition to these functional operations, the API provides generic, consistent support for pagination, major versioning via HTTP headers, and standardised error handling in accordance with the AASG — so that platforms built on eCrop behave seamlessly like other AgroConnect-compliant APIs.

### Planned extensions

eCrop is deliberately not a final destination: the standard is being actively developed further. Geographic information on plots (boundary, entry point, AB line), based on the OGC JSON-FG standard, has already been added to the draft version 1.1.0 of the eCrop OpenAPI spec, exposed via the `plot-geometry` category above, with possible additional support for the OGC API standard to follow. The roadmap also includes, among other things:

- **Footprint and sustainability data**: extending eCrop to exchange Footprint data (PEFCR) and Footprint scores, as a basis for a broader set of sustainability calculations to be added in later versions.
- **Exchange of crop-related data** between growers' farm management systems and contractors' management systems.

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
- [`docs/guides/`](docs/guides/) — use-case-specific implementation guides for particular integrations (e.g. [Loonwerkportaal](docs/guides/implementatie-instructie-loonwerkportaal.md)).
- [`examples/`](examples/) — sample requests and responses.
- [`CHANGELOG.md`](CHANGELOG.md) — notable changes to the standard.

Pushes to `main` that touch `openapi/**` are linted (`.github/workflows/validate.yml`); pushes touching `docs/**` or `openapi/**` rebuild and publish the docs site (`.github/workflows/publish.yml`).
