# Análisis de Datos F1 — Avance 2

**Curso:** Análisis de Datos e Inferencia Estadística  
**Integrantes:** Andy Villarroel, Javier Alcaino  
**Universidad del Desarrollo — Facultad de Ingeniería**

## Descripción del proyecto

Este repositorio contiene dos análisis estadísticos sobre la Fórmula 1 (1950–2023):

| Notebook | Pregunta de investigación |
|---|---|
| `Opcion 1 Avance 2.ipynb` | ¿Se ha estrechado o ampliado la brecha de rendimiento entre el auto más rápido y el más lento a lo largo de las décadas? |
| `Opcion 2 Avance 2.ipynb` | ¿El PPC de pilotos que debutaron en equipos Top es significativamente mayor que el de quienes debutaron en equipos chicos? |

## Fuente de datos

**Ergast Motor Racing Database** — Formula 1 World Championship (1950–2023)  
Disponible en: https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020

## Archivos de datos

| Archivo | Descripción |
|---|---|
| `results.csv` | Resultados por piloto por carrera |
| `races.csv` | Información de cada Gran Premio |
| `drivers.csv` | Datos de pilotos |
| `constructors.csv` | Datos de escuderías |
| `constructor_standings.csv` | Clasificación de constructores |
| `constructor_results.csv` | Resultados por constructor |
| `driver_standings.csv` | Clasificación de pilotos |
| `lap_times.csv` | Tiempos por vuelta |
| `pit_stops.csv` | Datos de pit stops |
| `qualifying.csv` | Resultados de clasificación |
| `circuits.csv` | Información de circuitos |
| `seasons.csv` | Datos de temporadas |
| `sprint_results.csv` | Resultados de sprints |
| `status.csv` | Códigos de estado de resultado |

## Cómo reproducir el análisis

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/boxs21/analisis-datos.git
   cd analisis-datos
   ```

2. Instalar dependencias:
   ```bash
   pip install pandas numpy matplotlib seaborn scipy statsmodels
   ```

3. Abrir Jupyter y ejecutar cualquiera de los notebooks:
   ```bash
   jupyter notebook
   ```

Los notebooks deben ejecutarse con todos los archivos CSV en el mismo directorio.
