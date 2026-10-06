# Changelog

All notable changes to the eCrop standard are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

The section of a version is used as the body of the GitHub release for its tag (`v<version>`; a pre-release tag such as
`v1.1.0-rc.1` uses the section of `1.1.0`). Add changes to the section of the version in preparation, or to *Unreleased*.

## [Unreleased]

## [1.1.0] - in preparation (pre-release v1.1.0-rc.1)

- Added business-case specific distributions of the specification: every operation has an *x-usecases* marker, and request/response examples moved to *components/examples* so that they can be overridden per business case (see *usecases/* and *openapi/README.md*)
- Replaced the bilateral reference between a Plot and its Feature by a one-way reference: a Feature refers to its Plot (*properties.plotId*), while the *plot-features* link of a Plot response is now a query (*GET /collections/plots/items?plotSchemeId=...&plotId=...*, a "backlink") instead of a link to one specific Feature. Added the *plotSchemeId* and *plotId* query parameters to *GET /collections/plots/items* for this. This enables content-based identifiers, which a bilateral reference would block
- Added reusable *JsonPatch* schema (RFC 6902 JSON Patch document, media type *application/json-patch+json*) to be used as request payload of PATCH operations, per AASG rule P012
- Added *PATCH /contractors/{contractorSchemeId}/{contractorId}/growers/{growerSchemeId}/{growerId}/plots/{plotSchemeId}/{plotId}/tasks/{taskSchemeId}/{taskId}* (JSON Patch request payload) for partially updating a plot-level task, e.g. changing the area of an operation from 25000 to 24500
- Added *POST /contractors/{contractorSchemeId}/{contractorId}/growers/{growerSchemeId}/{growerId}/plots/{plotSchemeId}/{plotId}/tasks* and *PUT*/*DELETE .../tasks/{taskSchemeId}/{taskId}*, letting a contractor register, update and delete non crop-specific plot-level tasks (with operations) on behalf of a grower he is granted access to, comparable to how a supplier manages inbound-deliveries for a grower
- Added *page*/*pageSize* query parameters and a *Link* response header (RFC 8288, rel=first/prev/next/last) to all business list GET operations, replacing the non-standard *offset*/*limit* parameters, to comply with the Logius API pagination standard; also removed *page*/*pageSize* erroneously present on the single-item *GET .../plots/{plotSchemeId}/{plotId}* operation
- Added reusable *cursor*/*limit* query parameters (the Logius API pagination standard's cursor-pagination method) to *components/parameters*, as an alternative to *page*/*pageSize* for implementors adding cursor-paginated operations
- Added *GET /openapi.json*, self-publishing this OpenAPI Specification document with CORS enabled, per the NLGov API Design Rules */core/publish-openapi* requirement
- Changed *license* in info section from *Agroconnect* to *CC BY 4.0* (https://creativecommons.org/licenses/by/4.0/)
- Fixed phrasing of tag descriptions for *farm level registration*, *plot level registration* and *crop level registration* ("Growers can use these operations" -> "These operations can be used")
- Corrected description of tag *plots*: plot geo-information is not part of these operations, it is published via the *plot-geometry* operations
- Added *GET /contractors/{contractorSchemeId}/{contractorId}/growers/{growerSchemeId}/{growerId}*, to retrieve a specific grower for a contractor, comparable to the existing supplier operation
- Added *GET /contractors/{contractorSchemeId}/{contractorId}*, to retrieve a specific contractor, comparable to the existing supplier operation
- Added *GET /contractors/{contractorSchemeId}/{contractorId}/growers/{growerSchemeId}/{growerId}/plots* and *GET .../plots/{plotSchemeId}/{plotId}*, giving a contractor read-only access to the plots (and a specific plot) of a grower he is granted access to
- Added *Contractor* as a new *Party* subtype (schemas *Contractor*/*ContractorDetails*), with basic *GET /contractors* and *GET /contractors/{contractorSchemeId}/{contractorId}/growers* operations, comparable to the existing supplier operations
- Extended *OperationDetails* schema with new optional properties *equipmentAssignments* (list of *EquipmentAssignment*) and *workerAssignments* (list of *WorkAssignment*); added missing descriptions to its *inputAllocations* and *outputAllocations* properties
- Added new schemas *EquipmentDetail*, *EquipmentAssignment*, *Worker* and *WorkAssignment*, to register equipment and workers used in an operation
- Added a dedicated *servers* override (*https://standard-api.agroconnect.nl/plot-features/v1*) to the *plot-geometry* operations, separating the OGC API Features/JSON-FG geo endpoints from the main eCrop business API server
- Added OGC API Features (Part 1: Core) and JSON-FG 1.0 support for plot geo-information: geometry schemas (Point/LineString/Polygon/MultiPolygon), PlotFeature/PlotFeatureCollection schemas with shared reusable properties, and the landing page/conformance/collections/items operations with profile (rfc7946/jsonfg), crs, bbox and datetime query parameters
- Replaced *Hallink* and *Hallinks* schemas with RFC 8288 compliant *Link* and *Links* schemas
- Fixed type *agroconnectcodelists* in examples (must be *agroconnect.codelist*)
- Fixed typo *thirdPartydIds* in examples (must be *thirdPartyIds*)
- Added tags *plots* and *crops* and added plots and crop operations to these sections 
- Changed description of *Date* and *DateTime* schemas (format, RFC compliancy)
- Changed description of *dateOfDelivery* in *InboundDeliveryDetails* schema (format, RFC compliancy)
- Changed content of unit-examples to Agroconnect cl020 codes
- Changed *unitcode* into *unitCode* in schema *MeasureType*
- Changed example of *inboundDeliveryId* parameter to be compliant with uuid format
- Changed *measuredValue* into *measureValue* in examples
- Added *codeValue* property to *CharacteristicsType*
- Fixed typos in descriptions of tags
- Removed conformance references info section and added reference to AGRI API Style Guide
- Removed Standard responses from info section (now part of the AGRI API Style Guide)
- Fixed typo in plot example (*conent* -> *content*)
- Fixed *ProblemDetails* schema and example to include an *errors* array (field/message) for reporting multiple validation errors, per AASG rule H007
- Fixed missing H004-required response codes (400/401/404) on several OGC and business operations
- Aligned *country* and *thirdPartyIds* examples with their schemas (object instead of plain string, content/schemeId instead of id/type) across Grower, Supplier and ProductionLocation examples
- Fixed required-but-nullable inconsistencies in address examples (removed invalid nulls, corrected streetNumber/postalBoxId to string type)
- Filled in placeholder *listId* values in the CropDetails example with actual AgroConnect codelist NSIDs (cl412/cl255/cl251/cl015/cl299/cl300)
- Added missing *id* to the nested *plots* in the CropDetails example, reusing the same identifiers as used in the GET /.../plots examples
- Changed *regularOrOrganic*, *localSoilType* and *regulatorySoilType* in the *Plot* schema from plain string to *CodeType* (content+listId), consistent with the same properties in *Crop*; updated all affected examples accordingly
- Renamed tag *geo* to *plot-geometry* for clarity
- Made *streetName*, *streetNumber* and *countryName* optional in *AddressType* (only *postalCode*, *cityName* and *country* remain required); added new property *streetNumberExtension* (string)
- Changed the *postalAddress* example in Grower to a PO box address (street properties omitted, *postalBoxId* populated), illustrating the now-optional street properties
- Removed the schema-level *example* from *ProblemDetails* (it caused the same 400-style example to appear on every error response); added a status-specific *example* to *default_error* instead, so each reusable error response (400/401/403/404/500/default) now shows its own matching example
- Replaced all occurrences of the en dash (U+2013, “–”) in examples with a regular hyphen-minus (U+002D, “-”), per OpenAPI validator recommendation

## [1.0.2]

- Added HalLinks and HalLink schemas.
- Added NsidType schema.
- Changed codeList schema to use NsidType for listId
- Removed erroneous '//' from paths from operations post-growers-plot-tasks and put-growers-plot-tasks

## [1.0.1]

- Changed reference to eCrop class model in the *externalDocs* section to version 1.0.0
- Renamed schema *MeasurementType* to *MeasureType*
- MeasureType Schema: Added unitCode to required section
- Added reusable type-schemas *Year* and *Time*
- Changed format of DateTime**Type type from *datetime* to *date-time* (OpenAPI 3.0 standard)
- Changed titles of Type schemas to correct English (separate words)
- Party Schema: typo: renamed property name *visitorsAdress* to *visitorsAddress*
- Party Schema: typo: renamed property name *emailAdress* scheme to *emailAddress*
- Grower Schema: fixed typo *visitorsAdress* and *emailAdress* in example
- Supplier Schema: fixed typo *visitorsAdress* and *emailAdress* in example
- ProductionLocationDetails Schema: fixed typos *visitorsAdress* and *emailAdress* in example
- PlantSpecies Schema: typo: renamed property name *plantSpecies* to *species*
- Tasks Schema: removed property *referenceId* (also in examples where applicable)
- Operations Schema: removed property *referenceId* (also in examples where applicable)
- Operations Schema: removed property *culturalPractice* (also in examples where applicable)
- Operations Schema: added missing property *type* 
- Operations Schema: renamed property *operationTechnique* to *technique* (q: which codelist?)
- AllocationDetails Schema: replaced *quantityAbsolute*  and *quantityRate* with *quantity* 
- AllocationDetails Schema: removed property *resourceId* (redundant with product-relation)
- CharacteristicsType Schema: modified definition of *characteristicsType* (separate value properties per type)
- Changed description of all *thirdPartyids* properties
- Added *additionalProperties: false* to pdt and udt schematypes
- Added reusable examples in the *components* section and checked them all with openapi-exmaples-validator

## [1.0.0]

Released for implementation of inbound-deliveries
