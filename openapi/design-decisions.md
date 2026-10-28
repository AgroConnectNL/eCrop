# Design decisions

These design decisions describe how the [eCrop class model](https://www.agroconnect.nl/Portals/10/EnterpriseArchitect/eCrop_json/eCrop_v1.1.1/index.html) is transferred to the OpenAPI definition [`ecrop.yaml`](ecrop.yaml). They apply to the complete specification and to all business-case distributions of it (see [`README.md`](README.md)).

General rules for the design of the API (versioning and headers, security, URLs and resource names, naming of schemas and properties, date and time formats, HTTP methods and status codes, error handling, links, `PATCH`) are given by the [AgroConnect AGRI API Style Guide](https://github.com/AgroConnectNL/API-Style-Guide/blob/main/API%20Style%20Guide%20Documentation/AGRI%20API%20Style%20Guide.md) (AASG), to which this specification conforms. They are not repeated here.

## 1. From class model to schemas

1. **Specialisations (UML generalisations).** A subtype is an `allOf` with a `$ref` to the supertype and an object with the attributes of the subtype.
2. **Compositions (UML compositions).** A composition is expressed either as a hierarchy in the URI (for instance `/growers/{...}/plots/{...}/tasks`) or as an array in the master object. In the eCrop class model these relations should be aggregations.
3. **Resource schema and details schema.** The attributes of a resource are defined in a `...Details` schema (for instance `PlotDetails`). The schema of the resource itself (`Plot`) is the server-assigned `id` combined with the `...Details` schema (`allOf`). Request bodies use the `...Details` schema, because the server assigns the id; responses use the resource schema.
4. **Multiplicity.** An attribute with multiplicity 1 in the class model is `required`, an attribute with multiplicity 0..1 is optional and an attribute with multiplicity 0..n is an array. Deviations from the class model are deliberate and documented in the description of the schema (for instance the optional street name and street number of an address, so that a PO box address can be expressed) and in the [changelog](../CHANGELOG.md).
5. **Names.** Names follow the class model. Reusable data types have the suffix `Type` (`IdType`, `CodeType`, `MeasureType`). Obvious spelling errors in the class model are corrected in the specification.
6. **Primitive types.** The primitive types of the class model are mapped as follows: `string` to `string`, `int` to `integer`, `float` to `number` (format `float`), `boolean` to `boolean`, `date` to `DateType` and `dateTime` to `DateTimeType`.
7. **Enumerations and code lists.** A closed value set that is part of the standard is an `enum` (for instance the plot type and the process status). A coded value from a code list that is maintained outside this specification is a `CodeType`: the code (`content`) and the identification of the code list (`listId`, an NSID such as `nl.agroconnect.codelist.cl271`). The description of the property names the code list.
8. **Characteristics.** The class `characteristicType` becomes the `CharacteristicType`: a code that says what the characteristic is, and exactly one value (`stringValue`, `booleanValue`, `dateValue`, `dateTimeValue`, `codeValue` or `measureValue`).
9. **Quantities.** A quantity (`measureType`) is a `MeasureType`: the value (`content`) and the unit (`unitCode`, a `CodeType`).
10. **OpenAPI 3.0.** The definition is an OpenAPI 3.0 document (3.0.4). Constructs of later versions (`const`, type arrays) are therefore not used; where a property that is a `$ref` needs its own description or `nullable`, it is combined with `allOf`.

## 2. Identification

1. **Server-assigned identification.** Each resource that has operations defined on it has a server-assigned identification named `id`, of type `IdType` in the class model: the value (`content`) and the scheme it comes from (`schemeId`).
2. **Client-assigned identifications.** Each schema has a list of client-assigned identifications named `thirdPartyIds` (an array of `IdType`: `content` and `schemeId`). A client can use these to find back its own identification and to prevent duplicates: posting a resource again with the same `thirdPartyIds` updates the earlier posted resource instead of creating a duplicate. In the class model this list is optional; in this specification it is required for most `...Details` schemas.
3. **Identification in the URI.** The `id` of a resource appears in the URI as two path segments, `{xSchemeId}/{xId}` (for instance `/growers/{growerSchemeId}/{growerId}`). Because path parameters in the same URI must have different names, each resource has its own pair of path parameters.

## 3. Roles and routes

The class model has several roles that act on the same data: the grower (`Farm`), the supplier and the contractor. The URI states on whose behalf a client acts. A grower uses `/growers/...`, a supplier uses `/suppliers/{...}/growers/{...}/...` and a contractor uses `/contractors/{...}/growers/{...}/...`, so that a supplier or contractor can only reach the growers that granted access. Authorisation itself is outside the specification.

## 4. Pagination

Pagination of collection (list) `GET` operations follows the [Logius API pagination standard](https://logius-standaarden.github.io/API-mod-pagination/). It defines two methods, of which an operation must use exactly one: page number (`page` / `pageSize`) or cursor (`cursor` / `limit`). Both are available as reusable parameters in `components/parameters`, so that an implementer who extends the API can pick whichever method fits a given (future) collection.

- The business list operations (`growers`, `suppliers`, `contractors`, `production-locations`, `plots`, `crops`, footprint declarations) use page-number pagination, because these are bounded, relatively static master-data collections.
- Business list responses convey the adjacent pages in the `Link` response header (RFC 8288), for instance `<.../growers?page=1&pageSize=20>; rel="first", <.../growers?page=3&pageSize=20>; rel="next", <.../growers?page=1&pageSize=20>; rel="prev"`.
- The plot-geometry operations (OGC API Features) use cursor-style pagination: the `limit` query parameter with an opaque continuation via the `next` relation, as in the OGC API Features convention. Their (FeatureCollection) responses convey the adjacent pages in the `links` array of the response body (`rel` = `next` / `prev`), per OGC API - Features - Part 1: Core. On those responses the `Link` header is reserved for the JSON-FG profile relation, for instance `<http://www.opengis.net/def/profile/OGC/0/jsonfg>; rel="profile"`.

## 5. Geographic information

1. **OGC API Features and JSON-FG.** The geometry classes of the class model (the plot geometry with boundary, entry point and AB line) are published through operations that conform to OGC API - Features - Part 1 and JSON-FG, on a separate server (`.../plot-features/v1`). A client selects the encoding with the `profile` query parameter: plain GeoJSON (`rfc7946`, default, always WGS84) or JSON-FG (`jsonfg`, with the CRS of the `crs` parameter).
2. **One-way reference between plot and feature.** In the class model a plot and its feature are associated. In the specification only the Feature refers to its Plot (`properties.plotId` and a link with `rel` `https://ecrop.agroconnect.nl/rel/plot`). A Plot stores no Feature id. The link with `rel` `https://ecrop.agroconnect.nl/rel/plot-features` in a Plot response is a query for the features that refer to the plot (the "backlink": `GET /collections/plots/items?plotSchemeId=...&plotId=...`). In this way the two representations contain no identifier of each other, which is a precondition for content-based identifiers.
