# python embed_graficos.py
# Lee los PNG y los incrusta como base64 en presentacion.html

import base64, re

def b64(path):
    with open(path, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode()

with open('presentacion.html', encoding='utf-8') as f:
    html = f.read()

# ── Slide 7: reemplazar placeholder del histograma ───────────────────────────
OLD_HIST = '''    <div class="img-placeholder">
      <div style="font-size:2em">📊</div>
      <span>fig_hist.png</span>
      <span style="font-size:.65em;color:#444">Exportar desde el notebook y reemplazar aquí</span>
    </div>'''

NEW_HIST = f'    <img src="{b64("fig_hist.png")}" style="width:100%;border-radius:6px;object-fit:contain;max-height:300px;">'

# ── Slide 8: reemplazar placeholders del boxplot y scatter ───────────────────
OLD_BOX = '''    <div class="img-placeholder" style="height:200px">
      <div style="font-size:1.6em">📦</div>
      <span>fig_boxplot.png</span>
    </div>'''

NEW_BOX = f'    <img src="{b64("fig_boxplot.png")}" style="width:100%;border-radius:6px;object-fit:contain;height:200px;">'

OLD_SCA = '''    <div class="img-placeholder" style="height:200px">
      <div style="font-size:1.6em">🔵</div>
      <span>fig_scatter.png</span>
    </div>'''

NEW_SCA = f'    <img src="{b64("fig_scatter.png")}" style="width:100%;border-radius:6px;object-fit:contain;height:200px;">'

html = html.replace(OLD_HIST, NEW_HIST)
html = html.replace(OLD_BOX,  NEW_BOX)
html = html.replace(OLD_SCA,  NEW_SCA)

with open('presentacion.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('presentacion.html actualizado con los 3 graficos incrustados.')
