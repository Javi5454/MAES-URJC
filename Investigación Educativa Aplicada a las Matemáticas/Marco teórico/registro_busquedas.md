# Registro de búsquedas bibliográficas

Sirve de base para el apartado de método de búsqueda y selección del marco teórico y para `bibliografia.bib`.

- **Fecha de las búsquedas:** 23 de noviembre de 2026.
- **Bases de datos:** Scopus, Web of Science Core Collection y Dialnet.
- **Verificación:** los datos de cada referencia (autores, revista, volumen, páginas y DOI) se han contrastado en Crossref.

## Cadenas y resultados

### Scopus (campo TITLE-ABS-KEY)

| # | Cadena | Resultados | Orden |
|---|---|---|---|
| S1 | `geogebra AND (trigonometr* OR vector* OR "analytic geometry") AND ("secondary" OR "high school")`, PUBYEAR > 2014 | 20 | Citas |
| S2 | `geogebra AND ("meta-analysis" OR "systematic review" OR "literature review")`, PUBYEAR > 2014 | 49 | Citas |
| S3 | `trigonometr* AND (understanding OR difficult* OR misconception*) AND (student* OR learner*)`, SUBJAREA(SOCI) | 168 | Citas |
| S4 | `("instrumental genesis" OR "instrumental approach") AND mathematic*` | 192 | Citas |
| S5 | `"dynamic geometry" AND (secondary OR "high school") AND (proof OR conjectur* OR dragging)` | 65 | Citas |
| S6 | `vector* AND (student* W/3 (understanding OR difficult* OR conception*)) AND (mathematic* OR physics)`, SUBJAREA(SOCI) | 134 | Citas |
| S7 | `(geogebra OR "dynamic geometry" OR "dynamic software") AND vector* AND (secondary OR "high school" OR "upper secondary" OR "grade 11" OR "grade 10" OR "pre-university")`, SUBJAREA(SOCI OR MATH) | 5 | Citas |
| S8 | `TITLE(geogebra AND vector*) OR TITLE-ABS-KEY(geogebra AND ("vector addition" OR "vector concept" OR "vectors") AND (learning OR teaching))` | 23 | Citas |

### Web of Science (campo TS, Core Collection)

| # | Cadena | Resultados |
|---|---|---|
| W1 | `TS=(GeoGebra AND (trigonometr* OR vector* OR "analytic geometry") AND (secondary OR "high school" OR "upper secondary")) AND PY=(2015-2026)` | 12 |
| W2 | `TS=(GeoGebra AND ("meta-analysis" OR "systematic review")) AND PY=(2015-2026)` | 19 |
| W3 | `TS=((trigonometr* OR vector* OR "analytic geometry") AND ("first-year" OR "first year" OR freshm* OR "introductory physics" OR entering OR "transition") AND (student* NEAR/3 (difficult* OR understanding OR misconception* OR error*)))`, áreas de educación (24-11-2026) | 58 |
| W4 | Como W3, ampliada a `"mathematical preparedness"`, `"prior mathematical knowledge"`, `"pre-university"`, `"secondary-tertiary"`, `underprepar*`, con PY=(2020-2026) (24-11-2026) | 20 |

### Dialnet (todos los campos)

| # | Cadena | Resultados |
|---|---|---|
| D1 | `geogebra trigonometría` | 21 |
| D2 | `geogebra vectores` | 26 |
| D3 | `geogebra bachillerato` | 102 |
| D4 | `geogebra "geometría analítica"` | 37 |
| D5 | `geometría dinámica bachillerato` | 29 |
| D6 | `geogebra secundaria rendimiento` | 11 |
| D7 | `trigonometría dificultades aprendizaje` | 10 |
| D8 | `génesis instrumental matemáticas` | 44 |
| D9 | `trigonometría primer curso universidad` (24-11-2026) | 11 |
| D10 | `conocimientos previos matemáticas primer curso ingeniería` (24-11-2026) | 33 |
| D11 | `vectores estudiantes universitarios dificultades` (24-11-2026) | 19 |
| D12 | `transición bachillerato universidad matemáticas dificultades` (24-11-2026) | 8 |
| D13 | `prueba diagnóstica matemáticas ingreso universidad` (24-11-2026) | 42 |

Scopus pidió volver a iniciar sesión el 24-11-2026, así que las búsquedas sobre la transición a la universidad se hicieron solo en WoS y Dialnet. Dialnet bloqueó temporalmente el acceso tras varias consultas seguidas. Conviene repetir D8 y revisar a mano la segunda página de D3.

## Criterios de selección

- **Inclusión:** estudios sobre Educación Secundaria o Bachillerato, o trabajos teóricos de referencia en el área. Deben ser estudios empíricos, revisiones sistemáticas o metaanálisis, o marcos teóricos muy citados. Tienen que relacionarse con GeoGebra o la geometría dinámica, la trigonometría, los vectores o la geometría analítica.
- **Periodo:** de 2015 a 2026 para la evidencia empírica. Se admiten clásicos anteriores (Artigue, Laborde, Duval, Weber…) cuando son la referencia teórica del concepto.
- **Exclusión:** trabajos de nivel universitario o de ingeniería, salvo que aporten algo transferible. También se excluyen las aplicaciones a la física sin componente matemático, los congresos de baja calidad sin revisión y los trabajos duplicados.
- **Idiomas:** inglés y español. Dialnet devuelve muchos trabajos en portugués, de Brasil, que se descartan por ahora.

## Selección final: núcleo de 25 fuentes

A petición del usuario, la bibliografía se reduce a unas 25 fuentes, una cantidad creíble de leer a fondo para un marco teórico de 10 a 15 páginas. Los criterios son tres:
1. Entre una y cinco fuentes por eje.
2. Prioridad a lo más reciente y a lo indexado en WoS o Scopus.
3. Se conservan todas las fuentes que se citan en la diapositiva y en el guion.

| Eje | Fuentes del núcleo (`bibliografia.bib`) |
|---|---|
| 1. Enfoque instrumental | `artigue2002`, `trouche2004`, `drijvers2015`, `clarkwilson2020` |
| 2. Representaciones | `duval2006` |
| 3. Geometría dinámica | `laborde2000`, `marrades2000`, `morales2021` |
| 4. Evidencia | `juandi2021`, `yohannes2023`, `zhang2025`, `alfonso2026`, `villalpando2022` (contraevidencia) |
| 5. Trigonometría | `weber2005`, `fiallo2017`, `carriazo2024`, `martinezsierra2025` |
| 6. Vectores | `barniol2014`, `heckler2015`, `quevedo2022`, `aliu2025` |
| 7. Llegada a la universidad | `mahadewsing2024`, `geewe2024`, `caballero2025`, `guerra2025` |

Las otras 22 fuentes localizadas y verificadas pasan a `bibliografia_reserva.bib`. La tabla siguiente recoge todas las localizadas, las del núcleo y las de reserva.

## Todas las fuentes localizadas por eje (núcleo y reserva)

| Eje | Clave bib | Base donde aparece | Para qué sirve |
|---|---|---|---|
| 1. Enfoque instrumental | `artigue2002` | Scopus S4 | Génesis instrumental: el artefacto se convierte en instrumento; dialéctica entre trabajo técnico y conceptual |
| | `trouche2004` | Scopus S4 | Orquestación instrumental: el papel del docente al organizar el uso de la herramienta |
| | `drijvers2010` | Scopus S4 | Perspectivas teóricas sobre la integración de la tecnología (estudio ICMI 17) |
| | `drijvers2015` | Crossref | Factores que hacen que la tecnología funcione o no: diseño de tareas, papel del docente y contexto |
| | `clarkwilson2020` | Scopus S4 | Estado de la cuestión reciente sobre la enseñanza con tecnología digital |
| 2. Representaciones | `duval2006` | Scopus | Registros de representación semiótica: comprender exige coordinar registros (algebraico y gráfico en GeoGebra) |
| 3. Geometría dinámica | `hohenwarter2004` | Web | Origen de GeoGebra como unión de geometría dinámica y álgebra (literatura gris) |
| | `laborde2000` | Scopus S5 | Los entornos dinámicos como contexto para conjeturar y demostrar |
| | `marrades2000` | Scopus S5 | Demostraciones de alumnado de Secundaria en geometría dinámica (autores españoles) |
| | `morales2021` | Dialnet D3 | Argumentación de alumnado de Bachillerato con GeoGebra |
| | `richard2010` | Dialnet D5 | Geometría dinámica y competencia de modelización en Bachillerato |
| | `aranda2021` | Dialnet D5 | Experimentos de enseñanza en Bachillerato con geometría dinámica |
| | `orts2016` | Dialnet D5 | Software de geometría dinámica como mediador del aprendizaje en Bachillerato |
| | `ortizmay2025` | Dialnet D5 | Resolución de problemas y tecnologías digitales en Bachillerato |
| | `mora2019` | Dialnet D3 | Investigaciones matemáticas en clase con GeoGebra (contexto español) |
| 4. Evidencia | `juandi2021` | Scopus S2 y WoS W2 | Metaanálisis sobre una década de aprendizaje con GeoGebra |
| | `yohannes2023` | Scopus S2 y WoS W2 | Revisión sistemática de artículos sobre GeoGebra (2010–2020) |
| | `zhang2025` | Scopus S2 | Metaanálisis de 20 años de visualización dinámica con GeoGebra |
| | `ji2024` | WoS W2 | Metaanálisis de tres niveles sobre software matemático dinámico |
| | `alfonso2026` | WoS W1 y W2 | Metaanálisis sobre geometría sintética y analítica con GeoGebra en Secundaria (autores españoles). **Muy alineado con el TFM** |
| | `hoyes2026` | WoS W2 | Revisión sistemática de 30 años de geometría dinámica |
| | `cevikbas2021` | Scopus S2 y WoS W2 | Diseño de tareas en entornos dinámicos e interactivos |
| 5. Trigonometría | `weber2005` | Scopus S3 | Comprensión de las funciones trigonométricas; ventaja de construirlas en el círculo unidad |
| | `moore2013` | Scopus S3 | Medida de ángulos y comprensión del radián |
| | `fiallo2017` | Scopus S3 | Conjetura y demostración en trigonometría de grado 10 (Colombia); Gutiérrez es de la Universitat de València |
| | `martinezsierra2025` | Scopus S1 y WoS W1 | Razonamiento covariacional en seno y coseno con applets de GeoGebra |
| | `carriazo2024` | Scopus S1 | Estudio cuasiexperimental: competencia trigonométrica con GeoGebra en Secundaria |
| | `nordlander2022` | Scopus S1 y WoS W1 | De lo procedimental a lo conceptual en trigonometría con GeoGebra |
| 6. Vectores | `barniol2014` | Scopus S6 | Test de comprensión de vectores; dificultades típicas |
| | `heckler2015` | Scopus S6 | Dificultades al sumar y restar vectores con la representación de flechas |
| | `aliu2025` | Scopus S8 | **El estudio más cercano:** cuasiexperimental en 9.º curso; con GeoGebra mejora la comprensión conceptual y procedimental de los vectores frente al método clásico |
| | `guntur2021` | Scopus S8 | Bachillerato (Indonesia): realidad aumentada frente a módulo convencional con GeoGebra (GeoGebra es el control). Sirve de contraste |
| | `quevedo2022` | Dialnet D2 | 1.º de Bachillerato (Ecuador): dificultades con el concepto, la representación y las propiedades de los vectores. Fundamenta una estrategia con GeoGebra y aprendizaje cooperativo, sin datos de aplicación |
| | `villalpando2022` | Dialnet D2 | **Contraevidencia:** objeto de aprendizaje en GeoGebra sobre vectores en R²; sin diferencias significativas con el grupo de control. Nivel por confirmar |
| 7. Las dificultades persisten en la universidad | `geewe2024` | WoS W4 | 1.º de Ingeniería: no conectan el álgebra de vectores con su representación gráfica |
| | `mahadewsing2024` | WoS W4 | 1.º de Ingeniería: muchos errores de cálculo vienen de álgebra y trigonometría básicas |
| | `hodds2023` | WoS W4 | Competencias matemáticas de entrada a la universidad (Reino Unido, tras la COVID-19) |
| | `mayerhofer2025` | WoS W4 | Transición Secundaria-universidad: cursos puente para reducir las carencias previas |
| | `guerra2025` | Dialnet D9 | Chile: dificultades con las ecuaciones trigonométricas en 1.º de Ingeniería |
| | `vecino2025` | Dialnet D9 | Argentina: trigonometría desaprovechada en Secundaria y su efecto en el primer año universitario |
| | `caballero2025` | Dialnet D12 | España: brecha entre Bachillerato y universidad; enseñanza memorística y con poca tecnología |
| | `garciasalmeron2021` | Dialnet D11 | México: entendimiento endeble del vector en 111 universitarios (test TUV) |
| | `aray2020` | Dialnet (búsqueda inicial D7) | Ecuador: la trigonometría superficial en Bachillerato dificulta el cálculo |
| | `castro2018` | Dialnet D10 | España (Universidad de Alicante): carencias matemáticas al acceder a Ingeniería |
| | `kamber2018` | WoS W3 | Aspectos problemáticos de la trigonometría en Secundaria |
| | `nieto2017` | Dialnet D10 | España: nivel matemático de 402 estudiantes de nuevo ingreso según la vía de acceso y la PAU |
| | `nguyen2003` | WoS W3 | **Clásico, se mantiene por la contundencia del dato:** de 2031 universitarios, más de 1/4 (física con cálculo) y más de 1/2 (física algebraica) no sabían sumar vectores en 2D |

## Pendiente de revisar

- **Eje 7, prioridad a lo reciente:** a petición del usuario se han descartado `knight1995`, `mikula2014` y `gomezchacon2009` por antiguos. Solo `nguyen2003` se mantiene como clásico. `kamber2018`, `nieto2017` y `castro2018` se conservan por ser de Secundaria o del contexto español. Cuando Scopus vuelva a estar accesible, repetir W4 allí para buscar más trabajos de 2020–2026.
- **`castro2018` y `caballero2025`:** falta confirmar la editorial.

- **Leer cada fuente antes de citarla.** Las descripciones de la tabla vienen del título y del resumen, no de la lectura completa.
- **`ji2024`:** las páginas no coinciden entre Crossref (815–840) y WoS (1035–1060). Hay que comprobarlas en la revista.
- **`hohenwarter2004`:** es literatura gris. Si se prefiere una fuente indexada, se puede citar GeoGebra a través de las revisiones del eje 4.
- **`richard2010`, `aranda2021` y `orts2016`:** falta confirmar la editorial.
- **Alcance de la búsqueda (vectores):** S7 confirma que en Scopus no hay ningún estudio sobre vectores con GeoGebra en la clase de matemáticas de Bachillerato. Lo más cercano es `aliu2025` (9.º curso) y `quevedo2022` (1.º de Bachillerato, sin datos). Las dificultades con vectores están descritas sobre todo en física universitaria (`barniol2014`, `heckler2015`). Esto se justifica como **vacío en la literatura**. Hay que recoger también la contraevidencia (`villalpando2022`): GeoGebra no funciona por sí solo, lo que conecta con el enfoque instrumental del eje 1.
- **`villalpando2022`:** confirmar el nivel educativo leyendo el texto completo.
- **`quevedo2022`:** faltan las páginas.
- **Dialnet en español:** domina la literatura latinoamericana en revistas de impacto bajo (Ecuador, México, Perú). Conviene seleccionar con criterio y priorizar trabajos de la SEIEM, de revistas españolas indexadas (*Enseñanza de las Ciencias*, *PNA*, *Números*, *Suma*) y de autores españoles.
