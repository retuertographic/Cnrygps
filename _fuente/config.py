# -*- coding: utf-8 -*-
"""Configuración de etiquetado del sitio (único punto de edición).

El sitio es HTML estático generado con `python3 _fuente/generar.py`, sin
GitHub Actions: los valores se escriben en las páginas al regenerarlas.
"""

# Google Tag Manager. Toda la analítica y el seguimiento van dentro del contenedor.
GTM_ID = 'GTM-5GX49FMH'

# Función de Biscotti CMP que reabre el panel de preferencias de cookies
# (ruta desde window). El enlace «Preferencias de cookies» del pie la llama;
# si no existe, lleva a la política de cookies.
BISCOTTI_REABRIR = 'Biscotti.showPreferences'
