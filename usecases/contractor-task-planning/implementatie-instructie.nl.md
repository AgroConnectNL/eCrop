# Implementatie-instructie: eCrop OpenAPI voor het Loonwerkportaal

*eCrop API v1.1.0 — use-case-scope voor een platform waarmee een loonwerker de percelen en bijbehorende geo-informatie van een boer kan raadplegen en de door hem uitgevoerde taken kan registreren.*

## 1. Use case en uitgangspunten

Een boer (akkerbouwer, melkveehouder) heeft in zijn bedrijfsmanagementsysteem (bms) percelen (plots, met geo-informatie) en (in geval akkerbouwers) teelten (crops) vastgelegd. Hij deelt deze gegevens met een loonwerker, die een taak (task + operation) voor hem moet uitvoeren. Voor de huidige implementatiefase is één use case geïdentificeerd, bestaande uit twee onderdelen:

**1. Percelen raadplegen (plannen). Een loonwerker moet als client (via zijn bms-loonwerker) de percelen van een teler (grower) kunnen ophalen. Bij deze percelen moet de client de bijbehorende geo-informatie (als Feature) kunnen ophalen — in willekeurige volgorde: eerst het Plot-object en van daaruit de Plot-geometrie, óf eerst de Plot-geometrie en van daaruit het Plot-object.**

**2. Uitgevoerde taken registreren. Nadat het werk is uitgevoerd, moet de loonwerker (via zijn bms-loonwerker) de taak (task, met operations) die hij op een perceel van de teler heeft uitgevoerd kunnen registreren, en deze achteraf kunnen corrigeren (via PUT; gedeeltelijk wijzigen via PATCH is optioneel) of verwijderen.**

Deze instructie beschrijft welke operaties uit de eCrop OpenAPI-specificatie voor deze use case gebouwd moeten worden, waarom de geo-operaties als geheel geïmplementeerd moeten worden, en welke zaken nog buiten de specificatie zelf geregeld moeten worden voordat dit in productie kan.

## 2. Te implementeren operaties

### 2.1 Kernoperaties voor deze use case

De volgende operaties zijn direct nodig om de use case te realiseren, in beide navigatierichtingen (Plot → Feature en Feature → Plot). De richtingen zijn niet gelijkwaardig: alleen Feature → Plot is als verwijzing opgeslagen, Plot → Feature is een zoekvraag (*backlink*, zie §3.11). Sinds de introductie van het /contractors-toegangsmodel verloopt de teler-/perceeltoegang voor een loonwerker expliciet via de contractor-gescopeerde operaties, niet meer via de directe /growers-operaties (die zijn voorbehouden aan de teler zelf, via zijn bms-teler):

**Contractor-operaties (business API, via /contractors)**

| Operatie                                                          | Doel                                                                                                 | Waarom nodig                                                                                         |
| ----------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `GET /contractors/{...}/{..}/growers`                             | Alle telers ophalen waarvoor de loonwerker (als contractor) toegang heeft gekregen                   | Nieuw discovery-startpunt: vervangt de eerdere aanname dat de loonwerker growerId al buiten de API om kende. De respons weerspiegelt direct welke telers voor deze loonwerker geautoriseerd zijn. |
| `GET /contractors/{...}/{..}/growers/{...}/{..}`                  | Basisgegevens van één specifieke teler ophalen                                                       | Optioneel: nuttig om bijv. de naam van de teler te tonen voordat de loonwerker diens percelen opvraagt |
| `GET /contractors/{...}/{..}/growers/{...}/{..}/plots`            | Volledige details van alle percelen van een teler ophalen (een lijst van Plot-objecten, elk met dezelfde details als de single-item-operatie), beperkt tot telers waarvoor de loonwerker toegang heeft | Startpunt van de flow wanneer de loonwerker nog geen specifiek plotId kent en wil zien welke percelen een teler heeft |
| `GET /contractors/{...}/{..}/growers/{...}/{..}/plots/{...}/{..}` | Volledige details van één specifiek perceel ophalen (zelfde detailniveau als een item uit de lijst hierboven) | Nodig zodra de loonwerker al een specifiek plotId kent (bijv. via een eerdere koppeling of via de link vanuit een Feature) en niet de volledige lijst wil ophalen |

**Contractor-operaties voor taakregistratie (business API, via /contractors)**

Alle taakoperaties zijn gescoped naar een perceel van een teler waarvoor de loonwerker toegang heeft: `/contractors/{...}/{..}/growers/{...}/{..}/plots/{plotSchemeId}/{plotId}/tasks`.

| Operatie                                  | Doel                                                                                                 | Waarom nodig                                                                                         |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `POST .../plots/{...}/{..}/tasks`         | Een (niet gewasspecifieke) taak, met bijbehorende operations, registreren die op het perceel is uitgevoerd | Hoofdoperatie om uitgevoerd werk te melden. De server kent het task-id toe; het eigen kenmerk van de loonwerker reist mee in `thirdPartyIds`. Opnieuw posten van een taak met hetzelfde externe id werkt de eerder geposte taak bij (geen duplicaten) |
| `PUT .../tasks/{taskSchemeId}/{taskId}`   | Een eerder geregistreerde taak bijwerken (als geheel vervangen); dekt alle wijzigingen van bestaande taken                                                  | Te verkiezen boven opnieuw posten wanneer de client de volledige, gecorrigeerde taak heeft           |
| `PATCH .../tasks/{taskSchemeId}/{taskId}` *(optioneel)* | Een eerder geregistreerde taak gedeeltelijk wijzigen met een JSON Patch-document (RFC 6902, mediatype `application/json-patch+json`, conform AASG-regel P012) | Optioneel, want PUT dekt alle wijzigingen van bestaande taken al af. Efficiënt voor kleine correcties, bijv. het gewijzigde oppervlak van een operation (`/operations/0/area/content`) van 25000 naar 24500 m2. Een `test`-operation in het patch-document beschermt tegen gelijktijdige wijzigingen |
| `DELETE .../tasks/{taskSchemeId}/{taskId}` | Een eerder geregistreerde taak verwijderen                                                          | Voor taken die per ongeluk zijn geregistreerd of waarvan het werk is geannuleerd                     |

De taakoperaties antwoorden met `202 Accepted` (POST, PUT, PATCH, met de geregistreerde taak in de respons) of `204 No Content` (DELETE). Zie ook het uitgewerkte voorbeeld in [README van deze use case](README.md).

**OGC API Features-operaties (plot-geometrie)**

| Operatie                                   | Doel                                                 | Waarom nodig                                                                                         |
| ------------------------------------------ | ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `GET /`                                    | Landing page van de Geo API                          | Verplicht startpunt van elke OGC API Features-conforme client                                        |
| `GET /conformance`                         | Conformance-declaratie                               | Verplicht: clients gebruiken dit om te bepalen welke profielen/functionaliteit de server ondersteunt |
| `GET /collections`                         | Lijst van beschikbare feature-collecties             | Verplicht discovery-stappunt, ook als er (nu) maar één collectie (plots) bestaat                     |
| `GET /collections/plots`                   | Metadata van de plots-collectie (extent, CRS-opties) | Nodig zodat een client weet in welke CRS'en en met welke profielen de collectie bevraagd kan worden  |
| `GET /collections/plots/items`             | FeatureCollection van percelen ophalen               | Nodig voor de "eerst Feature, dan Plot"-richting: de loonwerker kan features doorzoeken/filteren (bijv. op bbox) en van daaruit terugverwijzen naar het Plot-object. Met de queryparameters `plotSchemeId` en `plotId` (altijd samen) selecteert dezelfde operatie de Feature(s) van één perceel: dit is de zoekvraag achter de `plot-features`-link in een Plot-respons (de backlink, zie §3.11) |
| `GET /collections/plots/items/{featureId}` | Één Feature (geo-informatie van één perceel) ophalen | De geo-informatie van één Feature, bijv. als de featureId al bekend is uit een eerdere FeatureCollection-respons; de Feature verwijst terug naar het Plot-object via `properties.plotId` en de `plot`-link |

De twee operatiegroepen zijn in de specificatie voorzien van verschillende toegangspaden: de contractor-/business-operaties onder `https://standard-api.agroconnect.nl/ecrop/v1`, de plot-geometry-operaties onder `https://standard-api.agroconnect.nl/plot-features/v1`. Dit hoeft niet te betekenen dat deze twee ook daadwerkelijk op gescheiden (virtual) servers gebouwd moeten worden — beide toegangspaden kunnen prima door dezelfde onderliggende implementatie bediend worden, zolang ze beide putten uit dezelfde databron met perceelsgegevens. In dat geval is er tussen de twee toegangspaden ook geen aparte synchronisatie nodig: een wijziging die de teler doorvoert, is via beide paden meteen consistent zichtbaar.

### 2.2 Advies: GET /health

Hoewel `GET /health` geen onderdeel is van de functionele use case, adviseren wij deze operatie standaard te implementeren:

- Load balancers en orchestration-platforms (bijv. Kubernetes readiness/liveness probes) hebben een lichte, ongeauthenticeerde endpoint nodig om te bepalen of een API-instantie verkeer mag ontvangen.
- Monitoring en alerting (uptime-bewaking, SLA-rapportage richting de teler/loonwerker-organisaties) hebben een stabiel, voorspelbaar endpoint nodig dat niet afhankelijk is van business-logica of achterliggende databronnen.
- Het is een vaste bouwsteen in vrijwel elk productie-API-platform en kost nauwelijks implementatie-inspanning, terwijl het ontbreken ervan operationele bewaking sterk bemoeilijkt.

### 2.3 Expliciet buiten scope voor deze implementatiefase

De volgende operaties uit de specificatie zijn voor de huidige use case niet nodig en hoeven in deze fase niet gebouwd te worden:

| Domein                                            | Operaties                                                                                         | Waarom buiten scope                                                                                  |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Schrijfoperaties op plots                         | `POST`/`PUT`/`DELETE .../plots(/{plotId})`                                                        | Ten aanzien van percelen is de use case uitsluitend lezend; het vastleggen en wijzigen van percelen blijft de verantwoordelijkheid van de teler via zijn bms-teler |
| Directe, niet-contractor-gescopeerde plot-toegang | `GET /growers/{...}/{..}/plots(/{plotId})`                                                        | Dit is de toegangsroute voor de teler zelf (bms-teler); de loonwerker gebruikt uitsluitend de contractor-gescopeerde variant onder `/contractors/.../growers/.../plots`, zodat de toegang beperkt blijft tot telers waarvoor hij is geautoriseerd |
| Generieke contractor-lookup                       | `GET /contractors`, `/contractors/{id}`                                                           | Niet nodig voor deze use case: de loonwerker kent zijn eigen contractorSchemeId/contractorId al via zijn eigen configuratie/credentials en hoeft zichzelf of andere contractors niet op te zoeken |
| Parties (growers/suppliers lookup)                | `GET /growers`, `/growers/{id}`, `/suppliers`, `/suppliers/{id}`, `/suppliers/.../growers(/{id})` | Generieke, niet-gescopeerde partij-lookup blijft buiten scope; het ontdekken van "welke telers mag ik als loonwerker zien" verloopt voortaan via `GET /contractors/.../growers` (zie §2.1), niet via deze generieke endpoints |
| Delivery                                          | Alle `/inbound-deliveries`-operaties                                                              | Andere procesdomein (leveringen van/naar suppliers), niet gerelateerd aan percelen of geo-informatie |
| Production locations                              | `GET .../production-locations`, tasks op dit niveau                                               | Niet nodig voor het ophalen van percelen en geo-informatie                                           |
| Crops                                             | `GET`/`POST`/`PUT`/`DELETE .../crops(/{cropId})`                                                  | Teeltgegevens zijn in de huidige use case niet vereist; kan in een latere fase relevant worden zodra taken crop-specifieke context nodig hebben |
| Directe, niet-contractor-gescopeerde taakregistratie | `POST`/`PUT`/`PATCH`/`DELETE /growers/{...}/{..}/plots/{...}/{..}/tasks(...)`                  | Dit is de route voor de teler zelf (bms-teler); de loonwerker gebruikt uitsluitend de contractor-gescopeerde taakoperaties (zie §2.1) |
| Taken op andere niveaus                           | `.../production-locations/.../tasks`, `.../growers/{...}/{..}/tasks`, taken op crop-niveau        | De contractor-gescopeerde taakoperaties bestaan alleen op perceelniveau; taken op andere niveaus zijn niet nodig voor deze use case |

*Dit is een bewuste, expliciete scope-afbakening: deze operaties bestaan in de specificatie en kunnen in een volgende fase alsnog nodig zijn, maar horen niet bij de nu vastgestelde use case.*

## 3. Nog te regelen zaken

De specificatie beschrijft de vorm van de API; een aantal zaken moet nog buiten de OpenAPI-definitie zelf worden ingevuld voordat een implementatie hierop productiewaardig is.

### 3.1 Security

De huidige specificatie bevat geen enkele security-definitie (geen securitySchemes, geen security-vereiste op operaties). Dit moet nog volledig worden ingevuld:

- Authenticatiemechanisme: OAuth 2.0 / OIDC heeft de voorkeur boven alternatieven zoals API-sleutels of mTLS, omdat dit voldoet aan de AASG (rule S-categorie); te kiezen client credentials of authorization code flow voor het bms-loonwerker-platform, en vast te leggen als securityScheme in de OpenAPI-definitie.
- Autorisatiemodel: het datamodel voor het mandaat is inmiddels aanwezig — de `/contractors/{...}/{..}/growers`-operaties laten expliciet zien voor welke telers een contractor (loonwerker) is geautoriseerd, en die scoping wordt consequent doorgevoerd naar de onderliggende percelen. Wat nog wel open staat, is de daadwerkelijke verificatie: hoe wordt gegarandeerd dat de authenticatie van de aanroepende client (zie hierboven) daadwerkelijk overeenkomt met de contractorId waarvoor autorisatie wordt geclaimd, en hoe en door wie het onderliggende mandaat (welke teler welke loonwerker toegang geeft, voor welke periode) wordt vastgelegd en beheerd.
- CORS-beleid, indien het bms-loonwerker-platform (deels) browser-based is.
- Rate limiting/throttling, mede ter bescherming tegen misbruik van de ongeauthenticeerde `/health`-endpoint en tegen zware bbox/FeatureCollection-bevragingen.
- Logging en auditing van welke loonwerker welke telergegevens heeft opgevraagd, gezien de gevoeligheid van perceelslocaties, en van welke loonwerker welke taken heeft geregistreerd, gewijzigd of verwijderd.

### 3.2 Identifier-schemes (schemeId-waarden)

Alle idType-achtige properties (top-level id, thirdPartyIds) hebben een `schemeId` die aangeeft door wie en binnen welk register de identifier is uitgegeven. De voorbeelden in de distributie voor deze use case (`ecrop-contractor-task-planning.yaml`, zie `examples.yaml` in deze map) gebruiken de volgende schemes. Voor productie moet per identifier-soort een definitief, beheerd schemeId worden vastgesteld en gepubliceerd:

| Identifier-soort                                  | Voorbeeld-schemeId                                 | Uitgegeven door                          | Te besluiten                                                                                         |
| ------------------------------------------------- | -------------------------------------------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Primaire id's (`id` van grower, plot, task, ...)  | `nl.loonwerkportaal.codelist.guid`                 | Het Loonwerkportaal                      | Bevestigen als definitief scheme (GUID-formaat); ook gebruikt als `*SchemeId` in de URI's (`growerSchemeId`, `plotSchemeId`, `taskSchemeId`, ...) |
| Taak (`thirdPartyIds`)                            | `nl.my-cps.codelist.registratienummer`, `nl.my-cps.codelist.werkbonnummer` | Planningssysteem van de loonwerker (CPS) | Welke taak-identifiers de loonwerker minimaal meestuurt (bijv. verplicht werkbonnummer) |
| Operation (`thirdPartyIds`)                       | `nl.my-cps.codelist.operatienummer`                | Planningssysteem van de loonwerker       | Idem                                                                                                 |
| Behandelzone en invoerallocatie (`thirdPartyIds`) | `nl.my-cps.codelist.padnummers`, `nl.my-cps.codelist.registratienummer` | Planningssysteem van de loonwerker | Idem                                                                                          |
| Materieel (equipment)                             | `nl.my-cps.codelist.materieelnummer`               | Planningssysteem van de loonwerker       | Idem                                                                                                 |
| Medewerker (worker)                               | `nl.my-cps.codelist.medewerkernummer`              | Planningssysteem van de loonwerker       | Idem                                                                                                 |
| Perceelsnummer (plot, `thirdPartyIds`)            | `nl.rvo.codelist.perceelsnummer`                   | RVO                                      | Bevestigen als definitief scheme, inclusief validatieregels (formaat, bijv. `APD03-AD-4094`)         |
| thirdPartyIds van de teler (KVK-nummer)           | `nl.kvk.codelist.kvknummer`                        | Kamer van Koophandel                     | Bevestigen als definitief scheme, inclusief validatieregels (lengte/formaat)                         |
| thirdPartyIds van de teler (GLN)                  | `com.gs1.codelist.gln`                             | GS1                                      | Bevestigen als definitief scheme; vaststellen of GLN verplicht of optioneel is per resource          |

*Het voorvoegsel `nl.my-cps.*` is een voorbeeld voor het eigen planningssysteem van een loonwerker. Elke leverancier van loonwerksoftware gebruikt in de praktijk zijn eigen, unieke scheme-namespace.* Daarom moet nog worden vastgesteld hoe schemes van verschillende CPS-leveranciers worden geregistreerd en herkend door het Loonwerkportaal, en of een onbekend `schemeId` wordt geweigerd of alleen als vrije herkomstaanduiding wordt opgeslagen.

### 3.3 Querymogelijkheden voor GET .../plots

Aan `GET /contractors/{...}/{..}/growers/{...}/{..}/plots` (de lijst-operatie, zonder plotId) moeten nog queryparameters toegevoegd worden waarmee de client de selectie van percelen kan inperken — zonder filtering zou dit endpoint bij telers met veel percelen onbruikbaar groot worden. Minimaal noodzakelijk is een filter op jaar/peildatum (bijv. op basis van startDate/endDate van het perceel), zodat de loonwerker gericht de percelen kan opvragen die in het relevante teeltjaar actief zijn. Welke aanvullende filters (bijv. op type of regularOrOrganic) nodig zijn, moet nog worden bepaald.

### 3.4 Beslissen hoe Crop-informatie van een Plot gedeeld wordt

De huidige responsedefinities van Plot bevatten geen crop-sectie: teeltinformatie (Crop) wordt op dit moment niet aan de client teruggegeven bij het ophalen van een perceel. Dit moet nog expliciet ingevuld worden, en kan op verschillende manieren:

- Als geneste detail-lijst binnen de Plot-response (vergelijkbaar met hoe plots nu genest voorkomen in een Crop-response).
- Als aparte detail-operaties onder plots, bijvoorbeeld `GET /growers/{...}/{..}/plots/{...}/{..}/crops`.

De juiste keuze hangt af van de business case en hangt mede samen met de vraag of (en hoe) historie gedeeld moet worden: een geneste lijst past beter bij een klein, overzichtelijk aantal actuele teelten, terwijl aparte detail-operaties zich beter lenen voor het doorzoeken/filteren van een langere teelthistorie zonder de Plot-response onnodig te belasten.

### 3.5 Codelijsten (listId-waarden voor CodeType-velden)

Alle CodeType-velden (content + listId) verwijzen naar codelijsten die als NSID (bijv. `nl.agroconnect.codelist.clXXX`) benoemd zijn, maar nog niet daadwerkelijk gepubliceerd en beheerd hoeven te zijn. Dit moet voor productie geregeld worden:

| Veld                                    | listId (huidig)                 | Actie                                                                                                |
| --------------------------------------- | ------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Plot.regularOrOrganic                   | `nl.agroconnect.codelist.cl015` | Codelijst publiceren en beheerproces vaststellen                                                     |
| Plot.localSoilType / regulatorySoilType | `nl.agroconnect.codelist.cl405` | Idem; vaststellen of lokale en regulatoire bodemtype-lijst dezelfde codes gebruiken                  |
| Plot/Crop.area.unitCode                 | `nl.agroconnect.codelist.cl020` | Idem                                                                                                 |
| Crop.useTitle                           | `nl.agroconnect.codelist.cl412` | Idem                                                                                                 |
| Crop.productionType                     | `nl.agroconnect.codelist.cl255` | Idem                                                                                                 |
| Crop.productionPurpose                  | `nl.agroconnect.codelist.cl251` | Idem                                                                                                 |
| Crop.growEnvironment                    | `nl.agroconnect.codelist.cl299` | Idem                                                                                                 |
| Crop.growMedium                         | `nl.agroconnect.codelist.cl300` | Idem                                                                                                 |
| AddressType.country / Crop.country      | `iso.3166-1.alpha2`             | Vaststellen of de ISO 3166-1-lijst rechtstreeks gebruikt wordt, of via een eigen AgroConnect-NSID ontsloten wordt |

*Voor elke lijst moet worden vastgesteld: waar deze gepubliceerd wordt (bijv. een AgroConnect-codelijstenregister), wie beheerder is, en hoe wijzigingen/nieuwe codes worden gecommuniceerd naar implementerende partijen.*

### 3.6 featureType-vocabulaire

De waarde `agroconnect:ecrop:plot` voor featureType is een voorbeeldwaarde. Een definitief namespace- en registratiebeleid voor featureType-waarden binnen eCrop/AASG staat nog open, zoals ook in het architectuuradvies benoemd.

### 3.7 Custom link relations

De custom rel-URI's (`https://ecrop.agroconnect.nl/rel/plot` en `.../rel/plot-features`) moeten daadwerkelijk dereferentieerbaar gemaakt worden: een pagina die de betekenis van de relatie documenteert, conform de aanbevolen praktijk voor eigen link relation types. Let op: `.../rel/plot` is de opgeslagen verwijzing van een Feature naar zijn Plot, `.../rel/plot-features` is een zoekvraag (backlink) in de Plot-respons naar de Feature(s) van dat perceel (zie §3.11).

### 3.8 CRS en mod-geo-compliance

Voor de loonwerkportaal-praktijk is het aan te bevelen om `profile=jsonfg` met `crs=EPSG:28992` (RD New) als praktisch relevante default te communiceren richting bms-loonwerker-implementaties, aangezien agrarische GPS-/besturingssystemen doorgaans in RD New werken.

Daarnaast moet nog worden bepaald welke geo-profielen de API daadwerkelijk gaat ondersteunen — en daarmee welke CRS'en: alleen `rfc7946` (kale GeoJSON, altijd WGS84), alleen `jsonfg` (met RD New als native CRS), of beide naast elkaar. Deze keuze bepaalt mede hoeveel van de in §2 beschreven contentnegotiatie daadwerkelijk relevant is voor de loonwerkportaal-doelgroep.

### 3.9 Taakregistratie: verwerking en eigenaarschap

De taakoperaties (POST, PUT, PATCH) antwoorden met `202 Accepted`: de server heeft de taak aangenomen, maar de specificatie definieert geen statusresource of callback waarmee de loonwerker kan nagaan of de (eventueel asynchrone) verwerking is geslaagd of dat het systeem van de teler de taak later heeft afgewezen. Daarnaast moet nog worden vastgesteld:

- Hoe de teler de door een loonwerker op zijn percelen geregistreerde taken kan inzien, accepteren of betwisten.
- Of een loonwerker uitsluitend zijn eigen taken mag wijzigen of verwijderen. De contractor-gescopeerde URI suggereert dit, maar de specificatie dwingt het niet af; de implementatie moet dit expliciet controleren.
- Hoe met gelijktijdige wijzigingen wordt omgegaan. Bij PATCH kan de client een `test`-operation in het patch-document opnemen; voor PUT en POST is nog geen optimistic-concurrency-mechanisme (bijv. ETag) gedefinieerd. Een JSON Patch-document wordt als geheel toegepast of als geheel afgewezen (RFC 6902, §5): als één operation faalt, mag geen enkele wijziging doorgevoerd worden.

### 3.10 Synchronisatie tussen Plot en Feature

Deze instructie gaat ervan uit dat de Plot API en de Plot Features API beide uit dezelfde onderliggende datastore putten. Daardoor is er geen aparte synchronisatie tussen twee gescheiden databronnen nodig: een wijziging die de teler in zijn bms-teler doorvoert, is voor beide API's onmiddellijk en consistent zichtbaar, zonder replicatie- of cache-vertraging. Mocht in een latere fase alsnog voor gescheiden datastores gekozen worden, dan moet dit punt opnieuw expliciet uitgewerkt worden.

### 3.11 Verwijzing tussen Plot en Feature: backlinks

**Het probleem.** Een Plot en zijn Feature verwezen oorspronkelijk naar elkaar: de Plot bevatte een link naar één specifieke Feature (`/collections/plots/items/384912567`), en de Feature bevatte het id van de Plot (`properties.plotId`) en een link terug naar de Plot. Elke kant bewaart dus een identifier van de andere kant. Zodra identifiers van de inhoud worden afgeleid (content identifiers, bijv. een hash die verandert als de inhoud verandert), ontstaat daardoor een kringverwijzing: het id van de Plot hangt af van zijn inhoud en dus van het Feature-id, en het id van de Feature hangt af van zijn inhoud en dus van het Plot-id. Geen van beide kan als eerste worden berekend, en een wijziging aan de ene kant verandert het id van de andere kant, waardoor de eerste weer verandert. Wederzijdse verwijzingen met id's blokkeren het gebruik van content identifiers dus.

**De oplossing: backlinks vanaf de Feature-kant.** Er wordt maar één richting opgeslagen; de andere richting wordt afgeleid op het moment dat ze nodig is.

1. **De Feature bewaart de verwijzing naar de Plot** (`properties.plotId` en de link met `rel=https://ecrop.agroconnect.nl/rel/plot`). Een Feature bestaat alleen voor een Plot, dus deze afhankelijkheid is natuurlijk.
2. **De Plot bewaart geen Feature-id.** Zijn inhoud hangt daardoor niet van een Feature af, en zijn id is stabiel.
3. **De link van de Plot naar zijn geometrie wordt bij het lezen berekend.** De server beantwoordt de vraag "welke Features verwijzen naar dit Plot?" en geeft het antwoord als link terug. Die zoekvraag is de backlink.

De afhankelijkheid loopt nu in één richting (Feature hangt af van Plot), zodat er geen kringverwijzing meer is en id's op beide kanten van hun inhoud afgeleid kunnen worden.

**Hoe dit in de API werkt.** De `plot-features`-link in een Plot-respons wijst niet meer naar één Feature, maar is een zoekopdracht op de Features-collectie:

```json
{
  "rel": "https://ecrop.agroconnect.nl/rel/plot-features",
  "href": "https://standard-api.agroconnect.nl/plot-features/v1/collections/plots/items?plotSchemeId=nl.loonwerkportaal.codelist.guid&plotId=e7f8a9b0-1c2d-3e4f-5a6b-7c8d9e0f1a2b",
  "type": "application/geo+json"
}
```

`GET /collections/plots/items` heeft hiervoor de queryparameters `plotSchemeId` en `plotId` (altijd samen te gebruiken, samen vormen ze het id van de Plot). De respons is een FeatureCollection met de Features waarvan `properties.plotId` gelijk is aan dat id.

**Gevolgen en aandachtspunten voor de implementatie.**

- **Een Plot kan meerdere Features hebben.** Bijvoorbeeld een in de tijd gewijzigde geometrie, of meerdere varianten. Omdat de backlink een zoekvraag is, is dit zonder extra voorzieningen mogelijk. De respons is daarom altijd een FeatureCollection, ook als er normaal gesproken één Feature in zit; de client kiest de actuele.
- **De server heeft een index op `properties.plotId` nodig,** zodat de omgekeerde zoekactie snel blijft. In de specificatie is `plotId` nu alleen een eenvoudige queryparameter; een formele definitie als OGC API Features *queryable* (Part 3) is niet opgenomen.
- **Eén stap meer voor de client.** De client haalt eerst de Plot op en volgt daarna de backlink, en krijgt een lijst terug in plaats van één Feature. De "2 acties per perceel" blijven bestaan.
- **Verwijderen van een Plot.** Features die naar een verwijderde Plot verwijzen, blijven achter zonder doel. De implementatie moet bepalen of die Features dan mee worden verwijderd of als vervallen worden gemarkeerd.
- **Beide kanten blijven consistent doordat ze uit dezelfde datastore putten** (zie §3.10); er is geen apart bijhouden van een tweede verwijzing nodig.
- **Compatibiliteit.** Clients die de link uit een eerdere versie als verwijzing naar één Feature gebruikten (`.../items/{featureId}`), moeten de nieuwe link als zoekvraag behandelen. De href kan altijd gewoon gevolgd worden, zoals in de voorbeelden, zodat clients die de link niet zelf opbouwen niet hoeven te veranderen, behalve in het verwerken van de FeatureCollection-respons.
