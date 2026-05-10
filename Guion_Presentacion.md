# Guion de Presentación Oral
## "Análisis de Puntos por Carrera según Equipo de Debut en Fórmula 1"
### Análisis de Datos e Inferencia Estadística — Universidad del Desarrollo
### Presentadores: Andy Villarroel | Javier Alcaino
### Duración estimada: ~12 minutos

---

> **INSTRUCCIONES DE USO**
> - `[ANDY]` y `[JAVIER]` indican quién habla en cada sección.
> - Los textos entre corchetes tipo `[Nota]` son instrucciones escénicas, no se leen.
> - El texto en prosa es lo que se dice en voz alta. Se puede leer directamente si hay nervios.
> - Tiempos estimados por slide están entre paréntesis.

---

## [Slide 1 — Portada] (0:40)

**[ANDY]**

Buenas tardes. Somos Andy Villarroel y Javier Alcaino, y hoy les presentamos nuestro análisis de datos sobre Fórmula 1. El título del proyecto es: *"¿Debutar en un equipo grande te hace mejor piloto... o simplemente te da más puntos?"*

En los próximos doce minutos les vamos a contar qué pregunta nos hicimos, cómo construimos el análisis, qué encontramos y por qué creemos que los resultados son interesantes aunque, como verán, tienen sus matices.

[Nota: Andy señala el título en la pantalla. Javier está de pie al lado, asiente. Pausa breve antes de pasar.]

---

## [Slide 2 — Agenda] (0:30)

**[ANDY]**

La presentación está dividida en cuatro bloques. Primero les explicamos la pregunta de investigación y el dataset. Luego mostramos el análisis exploratorio de datos. Después Javier les presenta las pruebas estadísticas formales: el test de hipótesis y la regresión. Y cerramos con la discusión, limitaciones y próximos pasos.

[Nota: Andy recorre visualmente los ítems de la agenda mientras los nombra. No leer cada ítem palabra por palabra, hablar fluidamente.]

---

## [Slide 3 — Pregunta de Investigación] (1:00)

**[ANDY]**

Todo buen análisis parte de una pregunta concreta. La nuestra es esta: **¿el promedio de puntos por carrera de pilotos que debutaron en equipos "Top" es significativamente mayor que el de pilotos que debutaron en equipos más chicos?**

Para ser precisos con los términos: definimos "equipo Top" como cualquier equipo que haya ganado al menos un Campeonato Mundial de Constructores. Eso incluye a Ferrari, McLaren, Mercedes, Red Bull, Williams, Renault, Lotus, entre otros. Equipos con título. Los que han levantado el trofeo al menos una vez.

Y nuestra métrica de rendimiento es el **Promedio de Puntos por Carrera**, que abreviamos PPC. Lo calculamos dividiendo el total de puntos acumulados por un piloto en toda su carrera entre el número de carreras que disputó.

La hipótesis nula es que no hay diferencia entre grupos. La hipótesis alternativa es que los pilotos de equipos Top tienen un PPC mayor. Es un test unilateral, y en un momento Javier les explica por qué tomamos esa dirección.

[Nota: Señalar la fórmula del PPC si está en la slide. Tomarse este slide con calma, es el marco conceptual y el profe prestará mucha atención aquí.]

---

## [Slide 4 — Dataset] (1:10)

**[ANDY]**

Para responder esa pregunta usamos el dataset de Ergast Motor Racing, que es una API pública con datos históricos de Fórmula 1 desde 1950 hasta la temporada más reciente disponible. Es el dataset de referencia para este tipo de análisis, hay varios papers académicos que lo usan.

El dataset incluye múltiples tablas: resultados por carrera, información de pilotos, datos de constructores, posiciones de campeonato, tiempos de vuelta, y más. Nosotros trabajamos principalmente con las tablas de resultados, constructores y clasificaciones de constructores.

En total, después de la limpieza que les muestro enseguida, trabajamos con **X pilotos** distribuidos entre ambos grupos. El dataset cubre más de setenta años de historia del deporte, lo que da una variabilidad enorme, y esa variabilidad es precisamente parte de lo que hace el análisis interesante y también lo que introduce algunas limitaciones importantes.

[Nota: Reemplazar "X pilotos" con el número real del análisis antes de presentar. Si no se tiene el número exacto, decir "varios cientos de pilotos" y no dar cifra incorrecta.]

---

## [Slide 5 — Limpieza de Datos] (1:00)

**[ANDY]**

Ahora bien, los datos crudos no llegaron listos para usar. Tuvimos que hacer varios pasos de limpieza.

El criterio más importante fue **filtrar pilotos con menos de 10 carreras disputadas**. La razón es estadística: si un piloto corrió solo dos o tres carreras, su PPC no es representativo de su rendimiento real. Podría ser alguien que ganó una carrera en su debut y no volvió, o alguien que no terminó ninguna. Con menos de 10 carreras hay demasiado ruido.

También identificamos el equipo de debut de cada piloto, que es el constructor con el que corrió su primera carrera en el campeonato, y lo clasificamos como Top o Chico según la definición que ya mencionamos.

Además manejamos valores nulos en el campo de puntos, que corresponden a carreras donde el piloto no clasificó o se retiró sin puntuar. Esos se tratan como cero puntos para la carrera, lo cual es lo más honesto.

[Nota: Si hay una tabla o diagrama de flujo de limpieza en la slide, señalarla aquí. Mantener el ritmo, este slide no requiere demasiado detalle técnico salvo que el profe pregunte.]

**Transición:** Con los datos limpios, pasamos a explorarlos.

---

## [Slide 6 — EDA: Estadística Descriptiva] (1:00)

**[ANDY]**

En el análisis exploratorio, lo primero que hacemos es describir los datos. Y los números ya cuentan una historia bastante clara.

El grupo de pilotos que debutaron en equipos Top tiene un **PPC promedio de aproximadamente 1.62 puntos por carrera**. El grupo que debutó en equipos chicos tiene un promedio de **0.63 puntos por carrera**. Eso es una diferencia de aproximadamente un punto por carrera, lo que en Fórmula 1 puede significar la diferencia entre terminar sexto o décimo en el campeonato al final de la temporada.

Las medianas cuentan una historia similar, y las desviaciones estándar nos dicen que ambos grupos tienen bastante dispersión interna, lo cual tiene sentido: dentro de los equipos Top también hay pilotos que no llegaron a nada, y en los equipos chicos también hay pilotos que se destacaron enormemente.

[Nota: Señalar los valores de la tabla descriptiva en la pantalla mientras los nombra.]

---

## [Slide 7 — Histograma de Distribución] (0:50)

**[ANDY]**

El histograma nos muestra la distribución completa del PPC para ambos grupos superpuestos.

Lo que vemos es que ambas distribuciones tienen asimetría positiva, es decir, la mayoría de los pilotos se acumula en valores bajos de PPC y hay una cola larga hacia la derecha. Eso es esperable: los pilotos de alto rendimiento son excepcionales por definición.

Lo interesante es que la distribución del grupo Top está claramente corrida hacia la derecha respecto al grupo Chico. La concentración del grupo Chico está muy cercana a cero, mientras que el grupo Top tiene una masa mayor de pilotos en rangos intermedios y altos.

Esta distribución sesgada, dicho sea de paso, es una de las razones por las que vamos a usar el t-test de Welch en lugar de un test paramétrico estándar, pero eso se los explica Javier en el siguiente bloque.

[Nota: Señalar en la pantalla la diferencia de centros entre ambas distribuciones. Esto es el cierre del bloque de Andy.]

**[ANDY — Transición a Javier]**

Con ese panorama descriptivo sobre la mesa, le paso la palabra a Javier para que nos cuente qué dicen las pruebas estadísticas formales.

---

---

## [Slide 8 — Boxplot y Scatter] (1:10)

**[JAVIER]**

Gracias, Andy. Antes de entrar al test de hipótesis, quiero mostrarles dos visualizaciones más que nos ayudan a ver la estructura de los datos.

El **boxplot** confirma visualmente lo que Andy describió: la mediana del grupo Top es notablemente más alta que la del grupo Chico, y la caja del grupo Top está completamente por encima de la del grupo Chico. También podemos ver que hay más outliers en el grupo Top, lo que corresponde a esos pilotos excepcionalmente buenos, las leyendas del deporte, que traccionan la media hacia arriba.

El **scatter plot**, por su parte, muestra el PPC versus el número de carreras disputadas. Aquí hay algo interesante: hay una leve tendencia positiva. Los pilotos con más carreras disputadas tienden a tener PPC más altos. Eso tiene sentido: los pilotos que duran más en la grilla son los que más puntúan. Y eso ya nos da un indicio de que el número de carreras podría ser una covariable relevante, algo que vamos a incorporar en la regresión.

[Nota: Señalar primero el boxplot, luego moverse al scatter. Si están en slides separadas, pasar rápido de una a otra describiendo cada una brevemente.]

---

## [Slide 9 — Test de Hipótesis] (1:30)

**[JAVIER]**

Ahora sí, el test formal. Nuestras hipótesis son:

- H0: El PPC promedio de ambos grupos es igual. No hay diferencia.
- H1: El PPC promedio del grupo Top es mayor que el del grupo Chico. Test unilateral hacia la derecha.

Usamos el **t-test de Welch**, también conocido como t-test con varianzas desiguales. ¿Por qué Welch y no el t-test estándar? Porque el t-test de Student asume que las varianzas de ambos grupos son iguales. Nosotros no tenemos razón para asumir eso, los dos grupos tienen tamaños distintos y dispersiones distintas, como vimos en los boxplots. El test de Welch es más robusto en esa situación y es el estándar recomendado en la literatura actual. Por eso en la implementación usamos `equal_var=False`.

El resultado fue contundente: el **p-valor es muchísimo menor que 0.05**. Esto significa que rechazamos la hipótesis nula con un nivel de confianza muy alto. Hay evidencia estadística de que los pilotos que debutaron en equipos Top tienen un PPC promedio significativamente mayor.

Ahora, rechazar H0 no nos dice nada sobre cuánto mayor es la diferencia ni si hay otras variables involucradas. Para eso necesitamos el modelo de regresión.

[Nota: Mostrar el output del test en la slide si está incluido. Señalar el p-valor explícitamente.]

---

## [Slide 10 — Modelo de Regresión OLS] (1:10)

**[JAVIER]**

Para profundizar en la relación, construimos un modelo de regresión lineal por mínimos cuadrados ordinarios, OLS. La variable dependiente es el PPC de cada piloto. Las variables independientes son dos: `es_top`, que es una variable binaria que vale 1 si el piloto debutó en un equipo Top y 0 si no, y `n_carreras`, que es el total de carreras disputadas por el piloto.

Incluimos `n_carreras` porque el scatter que vimos antes sugería que hay una relación, y porque intuitivamente tiene sentido: no queremos que la diferencia entre grupos se explique únicamente por el hecho de que los pilotos de equipos Top tienden a tener carreras más largas.

El modelo resultante tiene un **R² de aproximadamente 21.7%**. Ambos coeficientes son estadísticamente significativos. Vamos slide siguiente para la interpretación.

[Nota: Señalar la tabla de resultados del modelo en la pantalla. Mencionar los valores p de los coeficientes si están visibles.]

---

## [Slide 11 — Interpretación de Coeficientes] (1:10)

**[JAVIER]**

Interpretemos los coeficientes uno por uno.

El coeficiente de `es_top` nos dice que, **manteniendo constante el número de carreras disputadas**, un piloto que debutó en un equipo Top tiene en promedio aproximadamente 1 punto más por carrera que uno que no lo hizo. Ese coeficiente es estadísticamente significativo, lo que refuerza el resultado del t-test.

El coeficiente de `n_carreras` es positivo y también significativo. Cada carrera adicional en la trayectoria de un piloto se asocia con un PPC marginalmente más alto. La interpretación es que los pilotos más longevos en la grilla tienden a ser mejores, o al menos más consistentes, lo que tiene lógica deportiva.

Ahora bien, el R² de 21.7% significa que nuestras dos variables explican algo más de un quinto de la varianza total en el PPC. El resto, casi el 80%, lo explican factores que no están en el modelo: el talento individual del piloto, el año en que corrió, el auto específico que tuvo, la suerte en carrera, y muchos otros factores. Eso no invalida el modelo, simplemente indica que el fenómeno es complejo y que hemos capturado una parte relevante pero no toda la historia.

[Nota: Señalar los coeficientes en la tabla mientras los interpreta. Si hay una ecuación del modelo en la slide, señalarla también.]

---

## [Slide 12 — Discusión y Limitaciones] (1:20)

**[JAVIER]**

Ahora lo más importante: ¿qué significa todo esto y cuáles son las limitaciones?

Los resultados son claros en términos estadísticos. Hay una diferencia real y significativa en el PPC entre grupos. Pero la interpretación causal es delicada.

La limitación más grande de nuestro análisis es el **cambio histórico en el sistema de puntuación**. En los años 50, el ganador se llevaba 9 puntos. Hoy se llevan 25, más un punto por la vuelta rápida, más puntos de sprint. Si un piloto corrió en los años 50 y otro corrió en 2020, sus PPC simplemente no son comparables en escala. Nosotros no estandarizamos los puntos porque eso requería una metodología adicional que dejamos como trabajo futuro, pero es una limitación que hay que tener presente al interpretar los resultados.

Una segunda limitación es la **causalidad invertida** o la confusión de variables. ¿Debutar en un equipo Top hace que el piloto sea mejor, o los equipos Top contratan a los pilotos que ya muestran ser mejores desde las categorías menores? No lo podemos determinar con este diseño observacional. Es una correlación, no una relación causal establecida.

Dicho esto, el análisis cumple su objetivo: describe una diferencia real en los datos y la cuantifica con rigor estadístico.

[Nota: Hablar con seguridad sobre las limitaciones. Mencionarlas no debilita el trabajo, al contrario, muestra pensamiento crítico. El profe valora esto.]

---

## [Slide 13 — Próximos Pasos] (0:40)

**[JAVIER]**

Con estas limitaciones en mente, los próximos pasos naturales del análisis serían tres.

Primero, estandarizar los puntos según la época. Se puede usar el porcentaje del máximo posible de puntos por temporada como métrica normalizada.

Segundo, incorporar más variables de control: el año de debut, la posición de partida promedio, los abandonos mecánicos. Un modelo más rico daría un R² más alto y una historia más completa.

Y tercero, si quisiéramos acercarnos más a la causalidad, se podría explorar un diseño de diferencias en diferencias o algún análisis de emparejamiento por propensión, aunque eso ya excede el alcance de este curso.

[Nota: Este slide puede ir rápido, no necesita detalles. Es para mostrar que pensamos en el futuro del análisis.]

---

## [Slide 14 — Cierre] (0:30)

**[JAVIER]**

Para cerrar: encontramos evidencia estadística sólida de que los pilotos que debutan en equipos que han ganado el Campeonato de Constructores acumulan en promedio significativamente más puntos por carrera que quienes debutan en equipos más chicos. La diferencia es de aproximadamente un punto por carrera, y es robusta tanto en el t-test como en la regresión controlando por el número de carreras.

Si Hamilton hubiera debutado en un Minardi, ¿dónde estaría hoy? Probablemente la respuesta estadística sería: con un PPC bastante más bajo. Pero eso es especulación, y nosotros somos gente de datos.

Muchas gracias. Quedamos disponibles para preguntas.

[Nota: Ambos presentadores al frente. Javier termina el discurso, Andy puede asentir o agregar "gracias" final. Dejar un silencio breve y natural después del cierre antes de abrir preguntas.]

---

---

# SECCIÓN DE PREGUNTAS ANTICIPADAS

> Esta sección NO se lee en la presentación. Es para preparar las respuestas durante la sesión de preguntas.

---

## Pregunta 1: "¿Por qué no estandarizaron los puntos según la época?"

**Respuesta recomendada:**

"Es una observación muy válida y es la principal limitación que reconocemos. No estandarizamos los puntos porque hacerlo requería definir un denominador de normalización, que podría ser el máximo posible de puntos en la temporada, la posición en campeonato relativa, o algún índice percentil. Todas esas opciones introducen supuestos propios. Optamos por reportar la limitación explícitamente en lugar de introducir una estandarización que podría no ser la más correcta sin un análisis adicional. Si tuviéramos que extender el trabajo, usaríamos el porcentaje de puntos obtenidos sobre el máximo posible en cada temporada como métrica normalizada."

---

## Pregunta 2: "¿Cómo saben que el equipo causó el éxito y no el talento del piloto?"

**Respuesta recomendada:**

"No lo sabemos, y somos explícitos en eso. Nuestro diseño es observacional, no experimental. No podemos afirmar causalidad en ninguna dirección. Lo que encontramos es una correlación estadísticamente significativa. La confusión entre talento y equipo es un problema clásico en el análisis de deportes: los equipos buenos contratan pilotos buenos, y los pilotos buenos terminan en equipos buenos. Para intentar separar esas variables necesitaríamos un diseño cuasi-experimental, por ejemplo comparando pilotos que cambiaron de un equipo Top a uno chico o viceversa a lo largo de su carrera. Eso está fuera del alcance de este trabajo, pero es el siguiente paso natural."

---

## Pregunta 3: "¿Por qué el R² es tan bajo, 21.7%? ¿No indica que el modelo no sirve?"

**Respuesta recomendada:**

"El R² de 21.7% no significa que el modelo no sirva, significa que el fenómeno es complejo. En ciencias sociales y en análisis deportivos, un R² en ese rango con solo dos variables predictoras es completamente razonable. Estamos modelando el rendimiento humano en un deporte que depende de cientos de factores: el auto, el motor, la estrategia de carrera, las condiciones climáticas, los accidentes, la salud del piloto. Que dos variables de nivel de estructura, el tipo de equipo de debut y la longevidad en el deporte, expliquen más de un quinto de la varianza ya es informativo. Los coeficientes son significativos, la dirección es la esperada, y el modelo cumple su propósito descriptivo."

---

## Pregunta 4: "¿Por qué usaron `equal_var=False` en el t-test? ¿Verificaron el supuesto de varianzas?"

**Respuesta recomendada:**

"Sí, lo consideramos. El t-test de Welch con `equal_var=False` es hoy el estándar recomendado por defecto en la mayoría de los textos de estadística aplicada, precisamente porque es más robusto cuando las varianzas son desiguales y no pierde mucha potencia cuando sí lo son. Para verificar formalmente la igualdad de varianzas podríamos usar el test de Levene o el test de Bartlett. En los boxplots que mostramos se observa que las dispersiones de ambos grupos son distintas, lo que sugiere que `equal_var=False` es la elección correcta. Si hubiéramos usado `equal_var=True` y las varianzas fueran realmente distintas, el test estaría mal especificado y los valores p serían incorrectos."

---

## Pregunta 5: "¿Verificaron los supuestos del t-test? ¿Normalidad, independencia?"

**Respuesta recomendada:**

"El supuesto de normalidad es menos crítico en este caso porque ambos grupos tienen tamaños de muestra suficientemente grandes para invocar el teorema central del límite, que garantiza que la distribución de las medias muestrales se aproxima a la normal independientemente de la distribución original. Para muestras grandes, el t-test es robusto a desviaciones de normalidad. El supuesto de independencia entre observaciones se cumple razonablemente: cada piloto es una observación independiente, no hay medidas repetidas sobre el mismo individuo. Lo que podría discutirse es si pilotos de la misma era o del mismo equipo son verdaderamente independientes, pero para el nivel de este análisis ese es un supuesto aceptable."

---

---

# RESUMEN DE TIEMPOS

| Slide | Presentador | Tiempo estimado |
|-------|-------------|-----------------|
| 1 — Portada | Andy | 0:40 |
| 2 — Agenda | Andy | 0:30 |
| 3 — Pregunta de Investigación | Andy | 1:00 |
| 4 — Dataset | Andy | 1:10 |
| 5 — Limpieza de Datos | Andy | 1:00 |
| 6 — EDA Descriptiva | Andy | 1:00 |
| 7 — Histograma | Andy | 0:50 |
| **[Cambio de presentador]** | | |
| 8 — Boxplot y Scatter | Javier | 1:10 |
| 9 — Test de Hipótesis | Javier | 1:30 |
| 10 — Regresión OLS | Javier | 1:10 |
| 11 — Interpretación | Javier | 1:10 |
| 12 — Discusión y Limitaciones | Javier | 1:20 |
| 13 — Próximos Pasos | Javier | 0:40 |
| 14 — Cierre | Javier | 0:30 |
| **TOTAL** | | **~12:50** |

---

*Guion preparado para la presentación final del proyecto — Análisis de Datos e Inferencia Estadística, Universidad del Desarrollo.*
