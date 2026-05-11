# python exportar_graficos.py
# Genera fig_hist.png, fig_boxplot.png, fig_scatter.png

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

DARK  = '#0d0d0d'
CARD  = '#1c1c1c'
GRID  = '#2a2a2a'
TEXT  = '#cccccc'
MUTE  = '#888888'
RED   = '#E10600'
BLUE  = '#3A86FF'
colors = {'Top': RED, 'Chico': BLUE}

plt.rcParams.update({
    'figure.facecolor':  DARK,
    'axes.facecolor':    CARD,
    'axes.edgecolor':    '#333',
    'grid.color':        GRID,
    'grid.linewidth':    0.6,
    'text.color':        TEXT,
    'axes.labelcolor':   TEXT,
    'axes.titlecolor':   '#f0f0f0',
    'xtick.color':       MUTE,
    'ytick.color':       MUTE,
    'axes.spines.top':   False,
    'axes.spines.right': False,
    'axes.spines.left':  False,
    'axes.spines.bottom':False,
    'font.family':       'sans-serif',
    'axes.titlesize':    13,
    'axes.titleweight':  'bold',
    'axes.titlepad':     14,
    'axes.labelsize':    11,
    'legend.facecolor':  CARD,
    'legend.edgecolor':  '#333',
    'legend.labelcolor': TEXT,
})
sns.set_theme(style='darkgrid', font_scale=1.05)
sns.set_palette([RED, BLUE])

# ── Cargar y preparar datos (igual que el notebook) ──────────────────────────
races          = pd.read_csv('races.csv',                na_values='\\N')
drivers        = pd.read_csv('drivers.csv',              na_values='\\N')
constructors   = pd.read_csv('constructors.csv',         na_values='\\N')
results        = pd.read_csv('results.csv',              na_values='\\N')
constructor_std= pd.read_csv('constructor_standings.csv',na_values='\\N')

ultima = races.sort_values('date').groupby('year')['raceId'].last().reset_index(name='raceId')
ids_top = constructor_std.merge(ultima, on='raceId').query('position == 1')['constructorId'].unique()
constructors['tipo'] = np.where(constructors['constructorId'].isin(ids_top), 'Top', 'Chico')

debut = results.sort_values('raceId').groupby('driverId').first().reset_index()[['driverId','constructorId']]
debut = debut.rename(columns={'constructorId':'constructor_debut'})
debut = debut.merge(constructors[['constructorId','name','tipo']], left_on='constructor_debut', right_on='constructorId')
debut = debut.rename(columns={'name':'equipo_debut','tipo':'tipo_debut'})

ppc_df = results.groupby('driverId').agg(pts_totales=('points','sum'), n_carreras=('raceId','count')).reset_index()
ppc_df = ppc_df.query('n_carreras >= 10').copy()
ppc_df['ppc'] = ppc_df['pts_totales'] / ppc_df['n_carreras']

df = ppc_df.merge(debut[['driverId','equipo_debut','tipo_debut']], on='driverId')
df = df.merge(drivers[['driverId','forename','surname']], on='driverId')
print(f"Dataset: {len(df)} pilotos  |  Top: {(df.tipo_debut=='Top').sum()}  Chico: {(df.tipo_debut=='Chico').sum()}")

# ── FIG 1: Histograma ─────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 5.5), facecolor=DARK)
ax.set_facecolor(CARD)
sns.histplot(data=df, x='ppc', hue='tipo_debut', kde=True,
             palette=colors, alpha=0.45, ax=ax, linewidth=0.8)
ax.set_title('Distribución del PPC por Tipo de Equipo de Debut')
ax.set_xlabel('Puntos por Carrera (PPC)')
ax.set_ylabel('Cantidad de Pilotos')
ax.grid(True, axis='y', color=GRID, linewidth=0.6)
ax.grid(False, axis='x')
legend = ax.get_legend()
legend.set_title('Debut en')
plt.tight_layout(pad=1.5)
fig.savefig('fig_hist.png', dpi=150, bbox_inches='tight', facecolor=DARK)
plt.close(fig)
print('fig_hist.png  OK')

# ── FIG 2: Boxplot ────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 5), facecolor=DARK)
ax.set_facecolor(CARD)
sns.boxplot(data=df, x='tipo_debut', y='ppc', palette=colors,
            ax=ax, width=0.5, linewidth=1.2,
            order=['Top','Chico'],
            medianprops=dict(color='#fff', linewidth=2))
ax.set_title('Boxplot: Rango y Outliers del PPC')
ax.set_xlabel('Tipo de Equipo de Debut')
ax.set_ylabel('Puntos por Carrera (PPC)')
ax.grid(True, axis='y', color=GRID, linewidth=0.6)
ax.grid(False, axis='x')
plt.tight_layout(pad=1.5)
fig.savefig('fig_boxplot.png', dpi=150, bbox_inches='tight', facecolor=DARK)
plt.close(fig)
print('fig_boxplot.png  OK')

# ── FIG 3: Scatter ────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5), facecolor=DARK)
ax.set_facecolor(CARD)
for grupo, color in colors.items():
    sub = df[df['tipo_debut'] == grupo]
    ax.scatter(sub['n_carreras'], sub['ppc'], color=color,
               alpha=0.55, s=28, label=grupo, linewidths=0)
ax.set_title('Dispersión: Experiencia vs PPC')
ax.set_xlabel('Total de Carreras Disputadas')
ax.set_ylabel('Puntos por Carrera (PPC)')
ax.legend(title='Debut en', framealpha=0.3)
ax.grid(True, color=GRID, linewidth=0.6)
plt.tight_layout(pad=1.5)
fig.savefig('fig_scatter.png', dpi=150, bbox_inches='tight', facecolor=DARK)
plt.close(fig)
print('fig_scatter.png  OK')

print('\nListo. Ejecuta embed_graficos.py para incrustar en el HTML.')
