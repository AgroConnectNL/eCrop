# eCrop

eCrop — the new REST API standard for crop-related data

## Licence summary

The eCrop standards, including the OpenAPI definitions, are published by AgroConnect under the [Creative Commons Attribution 4.0 International licence (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/legalcode.en).

This summary is for convenience only and is not legally binding. If there is any difference, the full licence text applies.

### What you may do
- **Use** the standards free of charge, including for commercial purposes.
- **Copy and adapt** the standards, including the OpenAPI definitions, for your own implementation.
- **Distribute** the standards or your adapted versions. You may license your own additions under any licence you choose.

No permission from AgroConnect is required.

### Conditions
- **Attribution.** When you share or publish the standards or an adapted version (for example in API documentation, a public specification or a repository), you must:
  - credit AgroConnect as the source;
  - name the licence and link to it;
  - indicate whether you have made changes.
- **Keep notices.** Do not remove existing attribution or licence notices from the files, such as the `x-source` field in the OpenAPI definitions.
- **No claim of ownership.** Do not present the standards as your own work.
- **No implied endorsement.** Do not suggest that AgroConnect endorses, certifies or approves your product or implementation.
- **No additional restrictions.** Do not impose terms or technical measures that prevent others from using the material under this licence.

Purely internal use, without sharing or publishing, does not require attribution.

**Suggested attribution:**
> Based on eCrop by AgroConnect, licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Changes have been made.

### Disclaimer and liability
- The standards are provided **"as is"**, without any warranty, including warranties of accuracy, completeness or fitness for a particular purpose.
- To the extent permitted by law, **AgroConnect is not liable** for any damage or loss arising from the use of the standards.
- You are responsible for verifying whether the standards are suitable for your implementation.

### Please note
- The licence does **not** grant any patent or trademark rights, including rights to the AgroConnect name or logo.
- Third-party material referenced in the standards, such as external code lists or standards, remains subject to its own licence.
- The standards may change. Always state which version you have implemented.

### Let us know
We would appreciate it if you let us know when you implement the standards. This is not a request for permission. It helps us keep an overview of implementations and inform you about upcoming changes. Contact: [email / link to issue form]

## Samenvatting licentievoorwaarden

De eCropstandaarden, inclusief de OpenAPI-definities, worden door AgroConnect gepubliceerd onder de [Creative Commons Naamsvermelding 4.0 Internationaal-licentie (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/deed.nl).

Deze samenvatting is alleen bedoeld als hulpmiddel en is juridisch niet bindend. Bij verschillen geldt de volledige licentietekst.

### Wat je mag
- **Gebruiken**: kosteloos, ook voor commerciële doeleinden.
- **Kopiëren en aanpassen**: de standaarden, inclusief de OpenAPI-definities, voor je eigen implementatie.
- **Verspreiden**: de standaarden of je aangepaste versies. Je eigen toevoegingen mag je onder een licentie naar keuze uitbrengen.

Je hebt hiervoor geen toestemming van AgroConnect nodig.

### Voorwaarden
- **Naamsvermelding.** Als je de standaarden of een aangepaste versie deelt of publiceert (bijvoorbeeld in API-documentatie, een openbare specificatie of een repository), moet je:
  - AgroConnect als bron vermelden;
  - de licentie noemen en ernaar linken;
  - aangeven of je wijzigingen hebt aangebracht.
- **Vermeldingen laten staan.** Verwijder bestaande bron- en licentievermeldingen niet uit de bestanden, zoals het `x-source`-veld in de OpenAPI-definities.
- **Geen eigendomsclaim.** Presenteer de standaarden niet als je eigen werk.
- **Geen gesuggereerde goedkeuring.** Wek niet de indruk dat AgroConnect je product of implementatie onderschrijft, certificeert of goedkeurt.
- **Geen extra beperkingen.** Leg geen voorwaarden of technische maatregelen op die anderen beletten het materiaal onder deze licentie te gebruiken.

Voor puur intern gebruik, zonder delen of publiceren, is naamsvermelding niet nodig.

**Voorbeeld van een naamsvermelding:**
> Gebaseerd op eCrop van AgroConnect, gelicentieerd onder CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Er zijn wijzigingen aangebracht.

### Garantie en aansprakelijkheid
- De standaarden worden geleverd **"zoals ze zijn"**, zonder enige garantie, ook niet op juistheid, volledigheid of geschiktheid voor een bepaald doel.
- Voor zover wettelijk toegestaan, is **AgroConnect niet aansprakelijk** voor schade of verlies door het gebruik van de standaarden.
- Je bent zelf verantwoordelijk voor het beoordelen of de standaarden geschikt zijn voor je implementatie.

### Let op
- De licentie geeft **geen** octrooi- of merkrechten, ook niet op de naam of het logo van AgroConnect.
- Materiaal van derden waarnaar de standaarden verwijzen, zoals externe codelijsten of standaarden, valt onder de eigen licentie van dat materiaal.
- De standaarden kunnen wijzigen. Vermeld altijd welke versie je hebt geïmplementeerd.

### Laat het ons weten
We stellen het op prijs als je meldt dat je de standaarden implementeert. Dit is geen verzoek om toestemming. Het helpt ons overzicht te houden van implementaties en je te informeren over komende wijzigingen. Contact: [e-mail / link naar issueformulier]

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
- [`usecases/`](usecases/) — one folder per business case, holding everything for that case: the description (actors, scope, operations used, an example flow with a sequence diagram, and open questions), the example overrides for its distribution of the specification (`examples.yaml`) and, where available, an implementation guide (e.g. [Loonwerkportaal](usecases/contractor-task-planning/implementatie-instructie.nl.md)); see [`usecases/README.md`](usecases/README.md) for the current list.
- [`scripts/`](scripts/) — repo tooling, e.g. [`build-distribution.py`](scripts/build-distribution.py), which builds a business-case specific distribution of the specification, and [`check-usecases-structure.js`](scripts/check-usecases-structure.js), which checks every business case in `usecases/` has the required sections.
- [`CHANGELOG.md`](CHANGELOG.md) — notable changes to the standard.

Pushes to `main` that touch `openapi/**` are linted (`.github/workflows/validate.yml`); every push to `main` rebuilds the business-case distributions and publishes them with the docs site on GitHub Pages, and tags `v*` attach them to a GitHub release (`.github/workflows/publish.yml`; see [`openapi/README.md`](openapi/README.md)); pushes touching `usecases/**` are checked for the required structure (`.github/workflows/check-usecases.yml`).
