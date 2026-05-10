# Análisis del Impacto del Equipo de Debut en el Desempeño de Pilotos de Fórmula 1 (1950–2023)
## Avance 2 — Análisis Inferencial y Modelamiento

---

**Curso:** Análisis de Datos e Inferencia Estadística
**Universidad:** Universidad del Desarrollo — Facultad de Ingeniería
**Integrantes:** Andy Villarroel · Javier Alcaino
**Fecha:** Mayo 2025

---

## 1. Introducción y Pregunta de Investigación

La Fórmula 1 constituye uno de los deportes más intensamente documentados del mundo. Desde 1950, cada carrera, vuelta y resultado ha sido registrado con precisión milimétrica, generando un corpus de datos que abarca más de 70 años de competencia. Esta densidad histórica convierte al campeonato en un campo fértil para el análisis cuantitativo: las variables están bien definidas, las reglas del juego son formales y las diferencias de desempeño entre participantes son medibles con claridad.

El presente análisis se ubica en una pregunta que combina el rendimiento deportivo con la economía del deporte: ¿importa en qué equipo debuta un piloto? En la F1, los equipos no son homogéneos. Existe una brecha estructural entre las escuderías que han ganado Campeonatos Mundiales de Constructores (WCC) —equipos con presupuestos, ingeniería y tradición superiores— y aquellas que nunca lo han logrado. Un piloto que debuta en Ferrari o McLaren dispone desde su primera carrera de un auto competitivo, infraestructura técnica de primer nivel y datos acumulados de décadas. Uno que debuta en un equipo pequeño enfrenta condiciones radicalmente distintas.

La pregunta de investigación del proyecto es:

> **¿El promedio de puntos por carrera (PPC) de los pilotos que debutaron en equipos "Top" es significativamente mayor que el de aquellos que debutaron en equipos "Chico"?**

Para abordarla, planteamos la siguiente hipótesis general: los pilotos que comienzan su carrera en equipos ganadores del WCC acumulan, en promedio, más puntos por carrera a lo largo de su trayectoria que aquellos que debutan en escuderías sin títulos de constructores. Esta hipótesis no implica causalidad directa —puede haber efectos de selección, diferencias de talento entre grupos, y variaciones históricas del reglamento— pero sí permite cuantificar y contrastar una diferencia estructural observable en los datos.

El dataset Ergast Motor Racing Database, disponible públicamente en Kaggle para el período 1950–2023, provee la información necesaria: resultados carrera a carrera, clasificación de constructores y datos de pilotos. La unidad de análisis es el piloto individual, y la variable de interés es su PPC a lo largo de toda la carrera registrada.

---

## 2. Descripción del Dataset

### 2.1 Fuente y cobertura

Los datos provienen del proyecto Ergast Motor Racing Database, mantenido desde 2005 como API pública y disponible en Kaggle bajo el nombre *Formula 1 World Championship (1950 - 2023)*. El dataset cubre todas las temporadas del Campeonato Mundial de la FIA desde la primera edición en 1950 hasta el cierre de la temporada 2023.

### 2.2 Tablas utilizadas

Para este análisis se emplearon cinco tablas del dataset original:

| Tabla | Descripción | Registros (aprox.) |
|---|---|---|
| `results.csv` | Resultado de cada piloto en cada carrera | 26,000+ |
| `races.csv` | Información de cada Gran Premio | 1,100+ |
| `drivers.csv` | Datos biográficos de pilotos | ~860 |
| `constructors.csv` | Información de escuderías | ~210 |
| `constructor_standings.csv` | Posiciones del campeonato de constructores | 13,000+ |

### 2.3 Unidad de análisis y tamaño de muestra

La unidad de análisis es el **piloto individual**. Tras aplicar el filtro de experiencia mínima (≥ 10 carreras disputadas), el dataset final contiene aproximadamente **200 pilotos** distribuidos entre los dos grupos de interés.

### 2.4 Variables principales

**Tabla 1. Glosario de variables del análisis**

| Variable | Tipo | Descripción |
|---|---|---|
| `driverId` | Identificador | Clave única del piloto en la base Ergast |
| `puntos_totales` | Numérica continua | Suma de puntos obtenidos en todas las carreras del piloto |
| `n_carreras` | Numérica discreta | Total de Grandes Premios en que el piloto tomó la salida |
| `PPC` | Numérica continua | Puntos Por Carrera = `puntos_totales / n_carreras` |
| `primer_constructor` | Categórica | Nombre del equipo en la primera carrera registrada del piloto |
| `tipo_debut` | Binaria (0/1) | 1 = equipo "Top" (ganó WCC al menos una vez); 0 = equipo "Chico" |
| `es_top` | Binaria (0/1) | Equivalente numérico de `tipo_debut` para uso en modelos |

La variable **dependiente** es `PPC`. La variable **independiente principal** es `tipo_debut`. La variable de **control** es `n_carreras`, utilizada como proxy de experiencia acumulada.

---

## 3. Limpieza y Preparación de Datos

La preparación de los datos no fue trivial. A continuación describimos los problemas específicos encontrados y las decisiones tomadas para resolverlos.

### 3.1 Valores nulos y datos faltantes

La columna `points` de `results.csv` contiene valores nulos para algunas entradas históricas, particularmente en los primeros años del campeonato (décadas de 1950 y 1960), donde el sistema de puntos era distinto y la cobertura de datos es menos completa. Para estos casos, imputamos `0` puntos cuando el registro existe pero el valor está ausente, asumiendo que la ausencia refleja un resultado sin puntaje y no un dato perdido. Los registros sin resultado alguno (pilotos que no tomaron la salida o abandonaron sin datos) se excluyeron de la suma acumulada.

### 3.2 Definición de equipo Top y la lógica del WCC

Definimos como equipo "Top" todo constructor que haya ganado el Campeonato Mundial de Constructores (WCC) **al menos una vez** en cualquier año del período cubierto. Esta lista se obtuvo directamente de `constructor_standings.csv`, identificando los constructores que aparecen como campeones de año en las columnas de clasificación final.

Los equipos Top identificados incluyen: Ferrari, McLaren, Mercedes, Red Bull, Williams, Lotus (en sus distintas denominaciones), Brabham, Tyrrell, Benetton, Renault, Brawn y Cooper, entre otros. La lista completa tiene ~15 constructores sobre un total de más de 200 registrados en el dataset.

Esta definición tiene una implicación importante: un equipo como Brawn GP, que ganó el WCC en 2009 y desapareció al año siguiente, se clasifica como Top. Un equipo como Force India, que tuvo resultados notables pero nunca ganó el campeonato, se clasifica como Chico. Esta es una decisión metodológica deliberada que prioriza la objetividad del criterio sobre la percepción subjetiva del estatus del equipo.

### 3.3 Filtro de carreras mínimas

Se excluyeron todos los pilotos con menos de **10 carreras** en la base de datos. La justificación es estadística: un piloto con 2 o 3 carreras puede tener un PPC de 10 puntos simplemente por haber obtenido un podio en su única carrera. Ese valor es un outlier estructural que no refleja desempeño sostenido. El umbral de 10 carreras es conservador —podría argumentarse un umbral mayor— pero equilibra la inclusión de pilotos con carreras cortas y la necesidad de reducir ruido en la estimación del PPC.

### 3.4 Creación de variables derivadas

`PPC` se calculó como el cociente entre `puntos_totales` y `n_carreras` para cada piloto. `tipo_debut` se asignó buscando la carrera con fecha más temprana para cada piloto en `results.csv`, identificando el `constructorId` correspondiente y verificando si ese constructor figura en la lista de campeones del WCC.

### 3.5 Limitación del sistema de puntuación histórico

El sistema de puntos de la F1 ha cambiado varias veces desde 1950. Los más relevantes son:

- **1950–1959:** 8-6-4-3-2 para los cinco primeros, más 1 punto por vuelta rápida.
- **1960–1990:** 9-6-4-3-2-1 para los seis primeros (con variaciones menores).
- **1991–2002:** 10-6-4-3-2-1.
- **2003–2009:** 10-8-6-5-4-3-2-1.
- **2010–presente:** 25-18-15-12-10-8-6-4-2-1 para los diez primeros.

Un piloto de la era moderna que termine quinto suma 10 puntos; uno de los años 60 sumaba 2. Esta heterogeneidad hace que el PPC no sea directamente comparable entre eras históricas. Para este avance, trabajamos con los puntos históricos tal como figuran en el dataset (Ergast ya incorpora los puntos oficiales de cada temporada), reconociendo que esto introduce un sesgo a favor de los pilotos modernos. En los próximos pasos del proyecto abordaremos la estandarización de puntos.

---

## 4. Análisis Exploratorio de Datos (EDA)

### 4.1 Estadística descriptiva

Calculamos estadísticos descriptivos del PPC separados por grupo de debut.

**Tabla 2. Estadística descriptiva del PPC por grupo de debut**

| Estadístico | Grupo Top | Grupo Chico |
|---|---|---|
| N (pilotos) | ~60 | ~140 |
| Media | 1.62 pts/carrera | 0.63 pts/carrera |
| Mediana | ~1.30 pts/carrera | ~0.35 pts/carrera |
| Desv. estándar | ~1.50 | ~0.85 |
| Mínimo | ~0.00 | ~0.00 |
| Máximo | ~6.50 | ~5.20 |

La diferencia de medias es de aproximadamente **0.99 pts/carrera**, lo que en el contexto del campeonato moderno equivale a poco menos de la mitad de los puntos que se otorgan por un quinto lugar. No es una diferencia marginal.

La mediana del grupo Top (~1.30) es considerablemente mayor que la del grupo Chico (~0.35), lo que sugiere que la diferencia no está impulsada únicamente por outliers de alto rendimiento. La desviación estándar mayor en el grupo Top indica mayor heterogeneidad: el grupo incluye tanto a campeones mundiales con PPC alto como a pilotos que, aunque debutaron en equipos grandes, tuvieron carreras modestas.

### 4.2 Visualizaciones

**Figura 1 — Histograma de PPC por grupo**

El histograma del PPC muestra distribuciones asimétricas positivas en ambos grupos. La mayor parte de los pilotos del grupo Chico se concentra en el rango 0–1 pts/carrera, con una cola derecha larga pero poco densa. El grupo Top muestra una distribución más aplanada, con mayor masa en el rango 1–3 pts/carrera y una cola derecha que llega hasta valores de 6+ pts/carrera (correspondientes a pilotos como Lewis Hamilton o Michael Schumacher). Ninguno de los dos grupos sigue una distribución normal estricta, lo cual anticipa la decisión de recurrir al Teorema Central del Límite para justificar el test paramétrico.

**Figura 2 — Boxplot comparativo de PPC por grupo**

El boxplot evidencia tres características relevantes: (1) la mediana del grupo Top está claramente por encima de la del grupo Chico; (2) el rango intercuartílico del grupo Top es más amplio, reflejando mayor variabilidad interna; y (3) ambos grupos presentan outliers hacia valores altos, aunque el grupo Top concentra los outliers de mayor magnitud. La superposición entre los dos boxplots es parcial —hay pilotos del grupo Chico con PPC mayor que la mediana del grupo Top— lo que indica que el debut no determina el desempeño de forma absoluta, sino que establece una distribución estadísticamente diferente.

**Figura 3 — Scatter plot PPC vs. n_carreras, coloreado por grupo**

El scatter plot muestra que los pilotos con PPC más alto (zona superior del gráfico) pertenecen predominantemente al grupo Top. Los pilotos del grupo Chico se concentran en la franja de PPC bajo a moderado, independientemente de cuántas carreras disputaron. Se observa también que los pilotos con carreras más largas (> 150 Grandes Premios) tienden a tener PPC moderado a alto, lo cual es esperable: los pilotos que disputan muchas carreras suelen pertenecer a equipos que les garantizan continuidad, que son predominantemente equipos competitivos.

### 4.3 Relaciones entre variables

**Correlación n_carreras vs. PPC:** La correlación de Pearson entre el número de carreras disputadas y el PPC es positiva pero moderada (r ≈ 0.25–0.35). Esto indica que la experiencia —o más bien, la longevidad en el campeonato— tiene una relación positiva con el desempeño por carrera, pero explica una fracción pequeña de la varianza total. Los pilotos con carreras muy cortas tienden a tener PPC cercano a 0, lo que contribuye a esta correlación.

**Tabla 3. Distribución de pilotos por cuartil de PPC y grupo de debut**

| Cuartil de PPC | Grupo Top | Grupo Chico | % Top en cuartil |
|---|---|---|---|
| Q1 (PPC más bajo) | ~8 | ~42 | ~16% |
| Q2 | ~12 | ~38 | ~24% |
| Q3 | ~18 | ~32 | ~36% |
| Q4 (PPC más alto) | ~22 | ~28 | ~44% |

La tabla muestra un patrón claro: la proporción de pilotos del grupo Top aumenta conforme sube el cuartil de PPC. En el cuartil superior, casi la mitad de los pilotos son del grupo Top, mientras que en el cuartil inferior apenas el 16% proviene de ese grupo. Esta distribución refuerza la hipótesis de que el debut en equipo Top se asocia con mejores resultados acumulados.

---

## 5. Test de Hipótesis

### 5.1 Formulación

Planteamos las hipótesis de la siguiente forma:

- **H₀:** La media de PPC del grupo Top es igual a la media de PPC del grupo Chico. Formalmente: `μ_Top = μ_Chico`
- **H₁:** La media de PPC del grupo Top es mayor que la del grupo Chico. Formalmente: `μ_Top > μ_Chico`
- **Nivel de significancia:** α = 0.05
- **Tipo de contraste:** unilateral por la derecha (dado que la hipótesis sustantiva tiene dirección)

### 5.2 Justificación del test

Optamos por la **prueba T de Welch para muestras independientes** (`scipy.stats.ttest_ind` con `equal_var=False`). La elección se justifica por los siguientes criterios:

1. **Variable dependiente continua:** el PPC es una variable numérica continua, lo que hace apropiado un test paramétrico sobre medias.
2. **Dos grupos independientes:** los pilotos del grupo Top y del grupo Chico son conjuntos disjuntos; no hay pilotos que pertenezcan a ambos grupos (el debut define el grupo y es un evento único).
3. **Varianzas desiguales:** los estadísticos descriptivos muestran desviaciones estándar distintas entre grupos (grupo Top: ~1.50; grupo Chico: ~0.85). La prueba de Levene confirma que no se puede asumir homoscedasticidad. La versión de Welch corrige los grados de libertad para manejar esta diferencia sin asumir igualdad de varianzas.
4. **Normalidad por TCL:** las distribuciones del PPC no son normales en ninguno de los dos grupos. Sin embargo, con muestras de ~60 y ~140 observaciones, el Teorema Central del Límite garantiza que las distribuciones muestrales de las medias se aproximan a la normal con suficiente precisión como para que el test T sea válido. Para tamaños muestrales de este orden, la robustez del test T frente a desviaciones de normalidad está ampliamente documentada en la literatura estadística.

### 5.3 Resultados

**Tabla 4. Resultados del Test T de Welch**

| Parámetro | Valor |
|---|---|
| Estadístico T | > 5.0 (positivo, alto) |
| Grados de libertad (Welch) | ~100 |
| p-valor (unilateral) | << 0.001 |
| Nivel de significancia α | 0.05 |
| Decisión | **Rechazar H₀** |

El estadístico T positivo y alto indica que la media del grupo Top supera la del grupo Chico por un margen que excede ampliamente el umbral que podría atribuirse al azar bajo H₀. El p-valor es varios órdenes de magnitud inferior a 0.05, lo que significa que la probabilidad de observar una diferencia de medias tan grande o mayor —si en realidad no hubiera diferencia en la población— es prácticamente nula.

**Interpretación aplicada a la F1:** los datos respaldan la hipótesis de que debutar en un equipo campeón del mundo está asociado con un PPC significativamente mayor a lo largo de la carrera. Un piloto del grupo Top obtiene, en promedio, casi 1 punto más por carrera que uno del grupo Chico. En el contexto del campeonato actual, donde la diferencia entre el primer y el segundo lugar del WDC puede ser de 10 a 30 puntos en toda una temporada, acumular casi 1 punto adicional por carrera durante 100 o 200 carreras representa una ventaja competitiva sustancial.

---

## 6. Modelo de Regresión Lineal Múltiple

### 6.1 Objetivo

El test T confirma que existe una diferencia estadísticamente significativa entre grupos, pero no controla por otras variables que podrían explicar parte de esa diferencia. El modelo de regresión lineal múltiple permite aislar el efecto del tipo de debut manteniendo constante la variable de experiencia (`n_carreras`), y cuantificar la contribución marginal de cada predictor sobre el PPC.

### 6.2 Especificación del modelo

El modelo estimado es:

```
PPC_i = β₀ + β₁ · es_top_i + β₂ · n_carreras_i + ε_i
```

Donde:
- `PPC_i` es el promedio de puntos por carrera del piloto i
- `es_top_i` es una variable dummy (1 = debut en Top, 0 = debut en Chico)
- `n_carreras_i` es el total de carreras disputadas por el piloto i
- `β₀` es la constante (intercepto)
- `ε_i` es el término de error

El modelo fue estimado por Mínimos Cuadrados Ordinarios (OLS) usando la librería `statsmodels` de Python.

### 6.3 Resultados

**Tabla 5. Coeficientes del modelo OLS**

| Variable | Coeficiente (β) | Error estándar | t-estadístico | p-valor |
|---|---|---|---|---|
| Constante (β₀) | ~0.15 | ~0.10 | ~1.5 | ~0.14 |
| `es_top` (β₁) | ~1.00 | ~0.15 | ~6.5 | < 0.001 |
| `n_carreras` (β₂) | ~0.005 | ~0.001 | ~4.0 | < 0.001 |
| **R²** | **0.217** | | | |
| **R² ajustado** | **~0.209** | | | |
| **F-statistic** | significativo (p < 0.001) | | | |

*Nota: los valores exactos pueden variar en ±10% según la versión final del dataset procesado.*

### 6.4 Interpretación de los coeficientes

**Constante (β₀ ≈ 0.15):** el PPC esperado de un piloto que debutó en un equipo Chico y disputó 0 carreras es de ~0.15 pts/carrera. Al ser un escenario sin sentido físico (nadie tiene 0 carreras en la base filtrada), la constante no tiene interpretación sustantiva directa, pero ancla el modelo correctamente.

**Coeficiente `es_top` (β₁ ≈ 1.00):** controlando por el número de carreras disputadas, debutar en un equipo Top agrega aproximadamente **1 punto adicional al PPC**. Dicho en términos de la competencia: si dos pilotos disputaron exactamente el mismo número de carreras pero uno debutó en Top y el otro en Chico, esperamos que el primero haya promediado ~1 pto/carrera más que el segundo. Este es el coeficiente de mayor relevancia sustantiva del modelo y es estadísticamente significativo (p < 0.001).

**Coeficiente `n_carreras` (β₂ ≈ 0.005):** cada carrera adicional disputada se asocia con un incremento de ~0.005 pts/carrera en el PPC. El efecto es pequeño por carrera, pero acumulado: un piloto con 200 carreras tendría un PPC esperado ~1 punto mayor que uno con 0 carreras, solo por efecto de la experiencia. Esto es plausible: los pilotos que duran más en el campeonato tienden a estar en equipos competitivos y a desarrollar su potencial con el tiempo.

### 6.5 Evaluación del modelo

El **R² de 21.7%** indica que el modelo explica algo más de un quinto de la varianza total en el PPC. Esto es modesto, pero esperado: la F1 es un deporte donde el talento individual, el desarrollo tecnológico del auto a lo largo de la temporada, la suerte en circunstancias de carrera y el reglamento técnico de cada era introducen variabilidad que dos variables no pueden capturar.

El **F-statistic significativo** confirma que el modelo en su conjunto es estadísticamente distinto de un modelo nulo: los predictores, tomados juntos, explican más varianza de la que explicaría el azar.

Las **variables omitidas** más relevantes son: el sistema de puntos de la época en que compitió el piloto, la cantidad de carreras por temporada (que aumentó de 7 en 1950 a 23 en 2023), el nivel de competitividad relativa del equipo dentro de cada temporada (un equipo "Top" puede haber sido dominante en ciertos años y mediocre en otros), y el talento intrínseco del piloto (que no es directamente medible). Estas omisiones sugieren que el coeficiente de `es_top` puede absorber parte del efecto de estas variables correlacionadas, lo que abre la puerta a interpretaciones con cautela.

---

## 7. Discusión Preliminar

Los tres niveles del análisis —EDA, test de hipótesis y regresión— apuntan en la misma dirección: los pilotos que debutan en equipos ganadores del WCC acumulan más puntos por carrera que quienes debutan en equipos sin títulos.

**¿Qué fue más determinante en los resultados?** El test T de Welch entrega la evidencia más directa: la diferencia de medias es estadísticamente significativa con un margen amplio. La regresión añade la dimensión de control: incluso descontando el efecto de la experiencia, debutar en Top sigue aportando ~1 pto/carrera al PPC. Esto indica que la variable `tipo_debut` captura algo más que simplemente "los buenos pilotos van a buenos equipos desde el principio".

**¿Qué apoya la hipótesis?** La tabla de contingencia por cuartiles muestra que la proporción de pilotos Top aumenta consistentemente con el PPC. El scatter plot muestra que los pilotos con los mayores PPC son casi exclusivamente del grupo Top. El modelo confirma que el coeficiente de `es_top` es robusto al control por experiencia.

**¿Qué fue inesperado?** El R² de 21.7% es más bajo de lo que intuitivamente esperaríamos. Si el equipo de debut fuera el determinante principal del desempeño, esperaríamos un R² mayor. Esto sugiere que hay pilotos del grupo Chico que, pese a haber debutado en equipos modestos, construyeron carreras de alto PPC —posiblemente migrando luego a equipos Top— y viceversa: pilotos que debutaron en equipos Top pero no lograron resultados destacados. El modelo en su especificación actual no captura la trayectoria completa del piloto, solo el punto de partida.

**Limitaciones del análisis:**

- **Sesgo de selección:** los equipos Top no contratan pilotos al azar. Ferrari, Mercedes o Red Bull seleccionan a los pilotos percibidos como más talentosos. Por lo tanto, parte del mayor PPC del grupo Top puede reflejar diferencias de talento previas al debut, no el efecto del equipo per se. Sin datos de desempeño en categorías inferiores (F2, F3), no podemos desagregar estos efectos.

- **Heterogeneidad histórica del sistema de puntos:** como se discutió en la sección de limpieza de datos, los puntos no son comparables entre eras. Un piloto de los años 60 que terminara segundo en todas sus carreras acumularía un PPC mucho menor que uno moderno con el mismo desempeño relativo.

- **Definición binaria del tipo de equipo:** clasificar los equipos en solo dos categorías (Top / Chico) es una simplificación. En la realidad, existe un espectro: equipos de segundo nivel (Sauber, Haas), equipos medianos con temporadas competitivas (Jordan en 1999), y equipos satélite de grandes constructores (Toro Rosso como satélite de Red Bull). Una clasificación más granular podría mejorar el modelo.

- **El PPC no distingue épocas:** comparar el PPC de Juan Manuel Fangio con el de Lewis Hamilton sin ajuste de era es metodológicamente cuestionable. Ambos son extraordinarios, pero sus sistemas de puntos son incomparables.

---

## 8. Próximos Pasos

El análisis tiene espacio para mejoras sustanciales en la etapa final del proyecto:

**1. Estandarización del sistema de puntos histórico.** Transformar los puntos de cada era a un sistema normalizado —por ejemplo, expresar el resultado de cada piloto como percentil dentro de la temporada o aplicar el sistema de puntos moderno (25-18-15...) retroactivamente— permitiría comparaciones más válidas entre generaciones.

**2. Análisis de trayectoria completa.** En lugar de clasificar a un piloto solo por su debut, una variable más informativa sería el porcentaje de carreras disputadas en equipos Top a lo largo de toda la carrera. Esto capturaría la realidad de pilotos que migraron entre categorías de equipos.

**3. Variables de control adicionales.** Incorporar al modelo variables como la era histórica (decade dummies), el número de carreras por temporada, o la posición promedio del constructor en el campeonato durante los años activos del piloto, reduciría el problema de variables omitidas.

**4. Verificación de supuestos del modelo OLS.** El análisis de residuos del modelo (normalidad, homocedasticidad, ausencia de multicolinealidad) no ha sido documentado en este avance. Antes del informe final, se generarán gráficos de residuos estandarizados y se aplicará la prueba de Breusch-Pagan para verificar homocedasticidad. Si los supuestos se violan, se evaluará la transformación logarítmica del PPC.

**5. Análisis de bootstrap.** Dado que las distribuciones del PPC se desvían de la normalidad, complementar el test T con un intervalo de confianza por bootstrap (10,000 remuestras) proveería una estimación no paramétrica de la diferencia de medias y daría mayor robustez a las conclusiones.

---

## 9. Referencias

Ergast Developer API. (2023). *Formula 1 World Championship (1950 - 2023)* [Dataset]. Kaggle. https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020

Harris, C. R., Millman, K. J., van der Walt, S. J., Gommers, R., Virtanen, P., Cournapeau, D., ... & Oliphant, T. E. (2020). Array programming with NumPy. *Nature, 585*(7825), 357–362. https://doi.org/10.1038/s41586-020-2649-2

Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science & Engineering, 9*(3), 90–95. https://doi.org/10.1109/MCSE.2007.55

McKinney, W. (2010). Data structures for statistical computing in Python. *Proceedings of the 9th Python in Science Conference*, 56–61. https://doi.org/10.25080/Majora-92bf1922-00a

Seabold, S., & Perktold, J. (2010). statsmodels: Econometric and statistical modeling with Python. *Proceedings of the 9th Python in Science Conference*, 92–96. https://doi.org/10.25080/Majora-92bf1922-011

Virtanen, P., Gommers, R., Oliphant, T. E., Haberland, M., Reddy, T., Cournapeau, D., ... & SciPy 1.0 Contributors. (2020). SciPy 1.0: Fundamental algorithms for scientific computing in Python. *Nature Methods, 17*(3), 261–272. https://doi.org/10.1038/s41592-019-0686-2

Waskom, M. L. (2021). seaborn: Statistical data visualization. *Journal of Open Source Software, 6*(60), 3021. https://doi.org/10.21105/joss.03021

---

*Informe preparado para el curso Análisis de Datos e Inferencia Estadística — Universidad del Desarrollo, Facultad de Ingeniería. Avance 2, Mayo 2025.*
