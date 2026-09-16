# Implementatie-instructie: eCrop OpenAPI voor het Loonwerkportaal

*eCrop API v1.1.0 — use-case-scope voor een platform waarmee een loonwerker de percelen en bijbehorende geo-informatie van een teler kan raadplegen.*

## 1. Use case en uitgangspunten

Een teler heeft in zijn bms-teler percelen (plots, met geo-informatie) en teelten (crops) vastgelegd. Hij deelt deze gegevens met een loonwerker, die een taak (task + operation) voor de teler moet uitvoeren. Voor de huidige implementatiefase is precies één use case geïdentificeerd:

**Een loonwerker moet als client (via zijn bms-loonwerker) de percelen van een teler (grower) kunnen ophalen. Bij deze percelen moet de client de bijbehorende geo-informatie (als Feature) kunnen ophalen — in beide richtingen: eerst het Plot-object en van daaruit de Feature, óf eerst de Feature en van daaruit het Plot-object.**

Deze instructie beschrijft welke operaties uit de eCrop OpenAPI-specificatie voor deze use case gebouwd moeten worden, waarom de geo-operaties als geheel geïmplementeerd moeten worden, en welke zaken nog buiten de specificatie zelf geregeld moeten worden voordat dit in productie kan.

## 2. Te implementeren operaties

### 2.1 Kernoperaties voor deze use case

De volgende operaties zijn direct nodig om de use case te realiseren, in beide navigatierichtingen (Plot → Feature en Feature → Plot). Sinds de introductie van het /contractors-toegangsmodel verloopt de teler-/perceeltoegang voor een loonwerker expliciet via de contractor-gescopeerde operaties, niet meer via de directe /growers-operaties (die zijn voorbehouden aan de teler zelf, via zijn bms-teler):

**Contractor-operaties (business API, via /contractors)**

| Operatie | Doel | Waarom nodig |
| --- | --- | --- |
| `GET /contractors/{...}/{..}/growers` | Alle telers ophalen waarvoor de loonwerker (als contractor) toegang heeft gekregen | Nieuw discovery-startpunt: vervangt de eerdere aanname dat de loonwerker growerId al buiten de API om kende. De respons weerspiegelt direct welke telers voor deze loonwerker geautoriseerd zijn. |
| `GET /contractors/{...}/{..}/growers/{...}/{..}` | Basisgegevens van één specifieke teler ophalen | Optioneel: nuttig om bijv. de naam van de teler te tonen voordat de loonwerker diens percelen opvraagt |
| `GET /contractors/{...}/{..}/growers/{...}/{..}/plots` | Volledige details van alle percelen van een teler ophalen (een lijst van Plot-objecten, elk met dezelfde details als de single-item-operatie), beperkt tot telers waarvoor de loonwerker toegang heeft | Startpunt van de flow wanneer de loonwerker nog geen specifiek plotId kent en wil zien welke percelen een teler heeft |
| `GET /contractors/{...}/{..}/growers/{...}/{..}/plots/{...}/{..}` | Volledige details van één specifiek perceel ophalen (zelfde detailniveau als een item uit de lijst hierboven) | Nodig zodra de loonwerker al een specifiek plotId kent (bijv. via een eerdere koppeling of via de link vanuit een Feature) en niet de volledige lijst wil ophalen |

**OGC API Features-operaties (plot-geometrie)**

| Operatie | Doel | Waarom nodig |
| --- | --- | --- |
| `GET /` | Landing page van de Geo API | Verplicht startpunt van elke OGC API Features-conforme client |
| `GET /conformance` | Conformance-declaratie | Verplicht: clients gebruiken dit om te bepalen welke profielen/functionaliteit de server ondersteunt |
| `GET /collections` | Lijst van beschikbare feature-collecties | Verplicht discovery-stappunt, ook als er (nu) maar één collectie (plots) bestaat |
| `GET /collections/plots` | Metadata van de plots-collectie (extent, CRS-opties) | Nodig zodat een client weet in welke CRS'en en met welke profielen de collectie bevraagd kan worden |
| `GET /collections/plots/items` | FeatureCollection van percelen ophalen | Nodig voor de "eerst Feature, dan Plot"-richting: de loonwerker kan features doorzoeken/filteren (bijv. op bbox) en van daaruit terugverwijzen naar het Plot-object |
| `GET /collections/plots/items/{featureId}` | Één Feature (geo-informatie van één perceel) ophalen | De kern van de use case: de geo-informatie behorend bij een specifiek perceel, met de terugverwijzing naar het Plot-object via links |

De twee operatiegroepen zijn in de specificatie voorzien van verschillende toegangspaden: de contractor-/business-operaties onder `https://standard-api.agroconnect.nl/ecrop/v1`, de plot-geometry-operaties onder `https://standard-api.agroconnect.nl/plot-features/v1`. Dit hoeft niet te betekenen dat deze twee ook daadwerkelijk op gescheiden (virtual) servers gebouwd moeten worden — beide toegangspaden kunnen prima door dezelfde onderliggende implementatie bediend worden, zolang ze beide putten uit dezelfde databron met perceelsgegevens. In dat geval is er tussen de twee toegangspaden ook geen aparte synchronisatie nodig: een wijziging die de teler doorvoert, is via beide paden meteen consistent zichtbaar.

### 2.2 Advies: GET /health

Hoewel `GET /health` geen onderdeel is van de functionele use case, adviseren wij deze operatie standaard te implementeren:

- Load balancers en orchestration-platforms (bijv. Kubernetes readiness/liveness probes) hebben een lichte, ongeauthenticeerde endpoint nodig om te bepalen of een API-instantie verkeer mag ontvangen.
- Monitoring en alerting (uptime-bewaking, SLA-rapportage richting de teler/loonwerker-organisaties) hebben een stabiel, voorspelbaar endpoint nodig dat niet afhankelijk is van business-logica of achterliggende databronnen.
- Het is een vaste bouwsteen in vrijwel elk productie-API-platform en kost nauwelijks implementatie-inspanning, terwijl het ontbreken ervan operationele bewaking sterk bemoeilijkt.

### 2.3 Expliciet buiten scope voor deze implementatiefase

De volgende operaties uit de specificatie zijn voor de huidige use case niet nodig en hoeven in deze fase niet gebouwd te worden:

| Domein | Operaties | Waarom buiten scope |
| --- | --- | --- |
| Schrijfoperaties op plots | `POST`/`PUT`/`DELETE .../plots(/{plotId})` | De use case is uitsluitend lezend; het vastleggen en wijzigen van percelen blijft de verantwoordelijkheid van de teler via zijn bms-teler |
| Directe, niet-contractor-gescopeerde plot-toegang | `GET /growers/{...}/{..}/plots(/{plotId})` | Dit is de toegangsroute voor de teler zelf (bms-teler); de loonwerker gebruikt uitsluitend de contractor-gescopeerde variant onder `/contractors/.../growers/.../plots`, zodat de toegang beperkt blijft tot telers waarvoor hij is geautoriseerd |
| Generieke contractor-lookup | `GET /contractors`, `/contractors/{id}` | Niet nodig voor deze use case: de loonwerker kent zijn eigen contractorSchemeId/contractorId al via zijn eigen configuratie/credentials en hoeft zichzelf of andere contractors niet op te zoeken |
| Parties (growers/suppliers lookup) | `GET /growers`, `/growers/{id}`, `/suppliers`, `/suppliers/{id}`, `/suppliers/.../growers(/{id})` | Generieke, niet-gescopeerde partij-lookup blijft buiten scope; het ontdekken van "welke telers mag ik als loonwerker zien" verloopt voortaan via `GET /contractors/.../growers` (zie §2.1), niet via deze generieke endpoints |
| Delivery | Alle `/inbound-deliveries`-operaties | Andere procesdomein (leveringen van/naar suppliers), niet gerelateerd aan percelen of geo-informatie |
| Production locations | `GET .../production-locations`, tasks op dit niveau | Niet nodig voor het ophalen van percelen en geo-informatie |
| Crops | `GET`/`POST`/`PUT`/`DELETE .../crops(/{cropId})` | Teeltgegevens zijn in de huidige use case niet vereist; kan in een latere fase relevant worden zodra taken crop-specifieke context nodig hebben |
| Tasks/operations | Alle `.../tasks`-operaties (grower/plot/crop-niveau) | De daadwerkelijke taakuitvoering door de loonwerker is context voor het geheel, maar geen onderdeel van de nu geïdentificeerde use case; te scopen zodra taakuitvoering zelf als use case wordt uitgewerkt |

*Dit is een bewuste, expliciete scope-afbakening: deze operaties bestaan in de specificatie en kunnen in een volgende fase alsnog nodig zijn, maar horen niet bij de nu vastgestelde use case.*

## 3. Nog te regelen zaken

De specificatie beschrijft de vorm van de API; een aantal zaken moet nog buiten de OpenAPI-definitie zelf worden ingevuld voordat een implementatie hierop productiewaardig is.

### 3.1 Security

De huidige specificatie bevat geen enkele security-definitie (geen securitySchemes, geen security-vereiste op operaties). Dit moet nog volledig worden ingevuld:

- Authenticatiemechanisme: OAuth 2.0 / OIDC heeft de voorkeur boven alternatieven zoals API-sleutels of mTLS, omdat dit voldoet aan de AASG (rule S-categorie); te kiezen client credentials of authorization code flow voor het bms-loonwerker-platform, en vast te leggen als securityScheme in de OpenAPI-definitie.
- Autorisatiemodel: het datamodel voor het mandaat is inmiddels aanwezig — de `/contractors/{...}/{..}/growers`-operaties laten expliciet zien voor welke telers een contractor (loonwerker) is geautoriseerd, en die scoping wordt consequent doorgevoerd naar de onderliggende percelen. Wat nog wel open staat, is de daadwerkelijke verificatie: hoe wordt gegarandeerd dat de authenticatie van de aanroepende client (zie hierboven) daadwerkelijk overeenkomt met de contractorId waarvoor autorisatie wordt geclaimd, en hoe en door wie het onderliggende mandaat (welke teler welke loonwerker toegang geeft, voor welke periode) wordt vastgelegd en beheerd.
- CORS-beleid, indien het bms-loonwerker-platform (deels) browser-based is.
- Rate limiting/throttling, mede ter bescherming tegen misbruik van de ongeauthenticeerde `/health`-endpoint en tegen zware bbox/FeatureCollection-bevragingen.
- Logging en auditing van welke loonwerker welke telergegevens heeft opgevraagd, gezien de gevoeligheid van perceelslocaties.

### 3.2 Identifier-schemes (schemeId-waarden)

Alle idType-achtige properties (top-level id, thirdPartyIds) gebruiken momenteel placeholder-schemeId-waarden uit de voorbeelden (bijv. `com.my-mps.codelist.guid`, `nl.kvk.codelist.kvknummer`, `com.gs1.codelist.gln`). Voor productie moet per identifier-soort een definitief, beheerd schemeId worden vastgesteld en gepubliceerd:

| Resource | Huidige voorbeeld-schemeId | Te besluiten |
| --- | --- | --- |
| Plot / Grower / Supplier / ProductionLocation (eigen id) | `com.my-mps.codelist.guid` | Welk eCrop-eigen ID-schema wordt de bron van waarheid: een GUID uitgegeven door het platform zelf, of een ander scheme? |
| thirdPartyIds (KVK-nummer) | `nl.kvk.codelist.kvknummer` | Bevestigen als definitief scheme, inclusief validatieregels (lengte/formaat) |
| thirdPartyIds (GLN) | `com.gs1.codelist.gln` | Bevestigen als definitief scheme; vaststellen of GLN verplicht of optioneel is per resource |
| thirdPartyIds (kasnummer/teeltnummer) | `com.my-mps.codelist.kasnummer` / `teeltnummer` | Vaststellen of dit een eCrop-breed erkend scheme wordt, of een deelnemer-specifiek scheme blijft |

### 3.3 Querymogelijkheden voor GET .../plots

Aan `GET /contractors/{...}/{..}/growers/{...}/{..}/plots` (de lijst-operatie, zonder plotId) moeten nog queryparameters toegevoegd worden waarmee de client de selectie van percelen kan inperken — zonder filtering zou dit endpoint bij telers met veel percelen onbruikbaar groot worden. Minimaal noodzakelijk is een filter op jaar/peildatum (bijv. op basis van startDate/endDate van het perceel), zodat de loonwerker gericht de percelen kan opvragen die in het relevante teeltjaar actief zijn. Welke aanvullende filters (bijv. op type of regularOrOrganic) nodig zijn, moet nog worden bepaald.

### 3.4 Beslissen hoe Crop-informatie van een Plot gedeeld wordt

De huidige responsedefinities van Plot bevatten geen crop-sectie: teeltinformatie (Crop) wordt op dit moment niet aan de client teruggegeven bij het ophalen van een perceel. Dit moet nog expliciet ingevuld worden, en kan op verschillende manieren:

- Als geneste detail-lijst binnen de Plot-response (vergelijkbaar met hoe plots nu genest voorkomen in een Crop-response).
- Als aparte detail-operaties onder plots, bijvoorbeeld `GET /growers/{...}/{..}/plots/{...}/{..}/crops`.

De juiste keuze hangt af van de business case en hangt mede samen met de vraag of (en hoe) historie gedeeld moet worden: een geneste lijst past beter bij een klein, overzichtelijk aantal actuele teelten, terwijl aparte detail-operaties zich beter lenen voor het doorzoeken/filteren van een langere teelthistorie zonder de Plot-response onnodig te belasten.

### 3.5 Codelijsten (listId-waarden voor CodeType-velden)

Alle CodeType-velden (content + listId) verwijzen naar codelijsten die als NSID (bijv. `nl.agroconnect.codelist.clXXX`) benoemd zijn, maar nog niet daadwerkelijk gepubliceerd en beheerd hoeven te zijn. Dit moet voor productie geregeld worden:

| Veld | listId (huidig) | Actie |
| --- | --- | --- |
| Plot.regularOrOrganic | `nl.agroconnect.codelist.cl015` | Codelijst publiceren en beheerproces vaststellen |
| Plot.localSoilType / regulatorySoilType | `nl.agroconnect.codelist.cl405` | Idem; vaststellen of lokale en regulatoire bodemtype-lijst dezelfde codes gebruiken |
| Plot/Crop.area.unitCode | `nl.agroconnect.codelist.cl020` | Idem |
| Crop.useTitle | `nl.agroconnect.codelist.cl412` | Idem |
| Crop.productionType | `nl.agroconnect.codelist.cl255` | Idem |
| Crop.productionPurpose | `nl.agroconnect.codelist.cl251` | Idem |
| Crop.growEnvironment | `nl.agroconnect.codelist.cl299` | Idem |
| Crop.growMedium | `nl.agroconnect.codelist.cl300` | Idem |
| AddressType.country / Crop.country | `iso.3166-1.alpha2` | Vaststellen of de ISO 3166-1-lijst rechtstreeks gebruikt wordt, of via een eigen AgroConnect-NSID ontsloten wordt |

*Voor elke lijst moet worden vastgesteld: waar deze gepubliceerd wordt (bijv. een AgroConnect-codelijstenregister), wie beheerder is, en hoe wijzigingen/nieuwe codes worden gecommuniceerd naar implementerende partijen.*

### 3.6 featureType-vocabulaire

De waarde `agroconnect:ecrop:plot` voor featureType is een voorbeeldwaarde. Een definitief namespace- en registratiebeleid voor featureType-waarden binnen eCrop/AASG staat nog open, zoals ook in het architectuuradvies benoemd.

### 3.7 Custom link relations

De custom rel-URI's (`https://ecrop.agroconnect.nl/rel/plot` en `.../rel/plot-features`) moeten daadwerkelijk dereferentieerbaar gemaakt worden: een pagina die de betekenis van de relatie documenteert, conform de aanbevolen praktijk voor eigen link relation types.

### 3.8 CRS en mod-geo-compliance

Voor de loonwerkportaal-praktijk is het aan te bevelen om `profile=jsonfg` met `crs=EPSG:28992` (RD New) als praktisch relevante default te communiceren richting bms-loonwerker-implementaties, aangezien agrarische GPS-/besturingssystemen doorgaans in RD New werken.

Daarnaast moet nog worden bepaald welke geo-profielen de API daadwerkelijk gaat ondersteunen — en daarmee welke CRS'en: alleen `rfc7946` (kale GeoJSON, altijd WGS84), alleen `jsonfg` (met RD New als native CRS), of beide naast elkaar. Deze keuze bepaalt mede hoeveel van de in §2 beschreven contentnegotiatie daadwerkelijk relevant is voor de loonwerkportaal-doelgroep.

### 3.9 Synchronisatie tussen Plot en Feature

Deze instructie gaat ervan uit dat de Plot API en de Plot Features API beide uit dezelfde onderliggende datastore putten. Daardoor is er geen aparte synchronisatie tussen twee gescheiden databronnen nodig: een wijziging die de teler in zijn bms-teler doorvoert, is voor beide API's onmiddellijk en consistent zichtbaar, zonder replicatie- of cache-vertraging. Mocht in een latere fase alsnog voor gescheiden datastores gekozen worden, dan moet dit punt opnieuw expliciet uitgewerkt worden.
