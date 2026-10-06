# -*- coding: utf-8 -*-
"""Genera el sitio estático de Canary GPS (ES en la raíz, EN en en/).

Uso:  python3 _fuente/generar.py
"""
import os
import re
from html import escape
from urllib.parse import urlencode, quote

from datos import (EMPRESA, PAGO, IMG, PLANES, PRECIO_EN, PASOS, DISPOSITIVO,
                   FAQ_GENERAL, SOLUCIONES, VALORES, HISTORIA)
from config import GTM_ID, BISCOTTI_REABRIR
from datos_casos import (INDUSTRIAS, HISTORIAS_EXITO, AFI_PASOS, AFI_NIVELES,
                         AFI_FAQ, AFI_CANALES)

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANIO = 2026

# ---------------------------------------------------------------- Iconos
_P = {
    'tel': '<path d="M6.5 3.5h3l1.5 4-2 1.5a12 12 0 0 0 6 6l1.5-2 4 1.5v3a2 2 0 0 1-2.2 2A16.5 16.5 0 0 1 4.5 5.7 2 2 0 0 1 6.5 3.5Z"/>',
    'mail': '<path d="M3.5 6h17v12h-17z"/><path d="m3.5 7 8.5 6 8.5-6"/>',
    'pin': '<path d="M12 21s6.5-6 6.5-11a6.5 6.5 0 1 0-13 0C5.5 15 12 21 12 21Z"/><circle cx="12" cy="10" r="2.4"/>',
    'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
    'flecha': '<path d="M5 12h13"/><path d="m12.5 5.5 6.5 6.5-6.5 6.5"/>',
    'abajo': '<path d="m6.5 9.5 5.5 5 5.5-5"/>',
    'arriba': '<path d="M12 19V6"/><path d="m5.5 12.5 6.5-6.5 6.5 6.5"/>',
    'check': '<path d="m4.5 12.5 4.5 4.5 10.5-10.5"/>',
    'carrito': '<circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M2.5 3.5h3l2.4 11.5h11l2-8H6.8"/>',
    'coche': '<path d="M5 16.5h14v-4l-2-5.5H7l-2 5.5z"/><path d="M5 12.5h14"/><circle cx="8" cy="16.5" r="1.8"/><circle cx="16" cy="16.5" r="1.8"/>',
    'huella': '<circle cx="7" cy="9" r="1.8"/><circle cx="11" cy="5.8" r="1.8"/><circle cx="15.5" cy="6.5" r="1.8"/><circle cx="18.5" cy="10.5" r="1.8"/><path d="M8.5 17.5c0-3 2-5.5 4.5-5.5s4 2.5 4 4.5-1.5 3-3 3-2-.8-3-.8-1.5.8-2.5.8-0-.5 0-2Z"/>',
    'camion': '<path d="M2.5 6.5h11v10h-11z"/><path d="M13.5 10h4l3 3.5v3h-7"/><circle cx="6.5" cy="17.5" r="1.8"/><circle cx="16.5" cy="17.5" r="1.8"/>',
    'megafono': '<path d="M3.5 10v4h3l7 4.5v-13L6.5 10z"/><path d="M17 9a4 4 0 0 1 0 6"/><path d="M8 14.5 9.5 20"/>',
    'casa': '<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/><path d="M9.5 21v-6h5v6"/>',
    'bateria': '<rect x="2.5" y="7" width="17" height="10" rx="2"/><path d="M21.5 10.5v3"/><path d="M6 10v4M9.5 10v4M13 10v4"/>',
    'iman': '<path d="M6 3.5v8a6 6 0 0 0 12 0v-8h-4v8a2 2 0 0 1-4 0v-8z"/><path d="M6 7.5h4M14 7.5h4"/>',
    'agua': '<path d="M12 3.5s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11Z"/>',
    'aviso': '<path d="M6 16.5V11a6 6 0 0 1 12 0v5.5l1.5 2h-15z"/><path d="M10 20.5a2 2 0 0 0 4 0"/>',
    'corazon': '<path d="M12 20s-7.5-4.6-7.5-10A4.3 4.3 0 0 1 12 7.3 4.3 4.3 0 0 1 19.5 10c0 5.4-7.5 10-7.5 10Z"/>',
    'escudo': '<path d="M12 3.2 19 6v6c0 4.4-3 7.6-7 8.8-4-1.2-7-4.4-7-8.8V6Z"/><path d="m9 12 2 2 4-4"/>',
    'doc': '<path d="M6 3.5h8l4 4v13H6z"/><path d="M14 3.5v4h4"/><path d="M9 12h6M9 15.5h6"/>',
    'info': '<circle cx="12" cy="12" r="8.5"/><path d="M12 11v5"/><path d="M12 7.8v.1"/>',
    'mapa': '<path d="m3.5 6 5.5-2 6 2 5.5-2v14l-5.5 2-6-2-5.5 2z"/><path d="M9 4v14M15 6v14"/>',
    'pregunta': '<circle cx="12" cy="12" r="8.5"/><path d="M9.6 9.5a2.5 2.5 0 1 1 3.4 2.3c-.6.3-1 .8-1 1.5v.4"/><path d="M12 16.6v.1"/>',
    'personas': '<circle cx="9" cy="8" r="3"/><path d="M3.5 19a5.5 5.5 0 0 1 11 0"/><path d="M15.5 5.3a3 3 0 0 1 0 5.4M17.5 19a5.5 5.5 0 0 0-2.5-4.6"/>',
    'etiqueta': '<path d="M3.5 12.5V4h8.5l8.5 8.5-8.5 8.5z"/><circle cx="8" cy="8.5" r="1.3"/>',
    'casco': '<path d="M3.5 17.5h17"/><path d="M5 17.5a7 7 0 0 1 14 0"/><path d="M10 10.8V7h4v3.8"/>',
    'tienda': '<path d="M3.5 9.5 5 4.5h14l1.5 5"/><path d="M3.5 9.5a2.8 2.8 0 0 0 5.6 0 2.8 2.8 0 0 0 5.8 0 2.8 2.8 0 0 0 5.6 0"/><path d="M5 12v8.5h14V12"/><path d="M10 20.5v-5h4v5"/>',
    'llave': '<circle cx="8" cy="15" r="4"/><path d="m11 12 8.5-8.5"/><path d="m16.5 6.5 2.5 2.5M14 9l2 2"/>',
    'estrella': '<path d="m12 3.5 2.6 5.5 6 .8-4.4 4.2 1.1 6-5.3-2.9-5.3 2.9 1.1-6L3.4 9.8l6-.8z"/>',
    'euro': '<circle cx="12" cy="12" r="8.5"/><path d="M15.5 8.8a4 4 0 1 0 0 6.4"/><path d="M7.5 11h6M7.5 13.5h6"/>',
    'engranaje': '<circle cx="12" cy="12" r="3"/><path d="M12 3v2.5M12 18.5V21M3 12h2.5M18.5 12H21M5.6 5.6l1.8 1.8M16.6 16.6l1.8 1.8M5.6 18.4l1.8-1.8M16.6 7.4l1.8-1.8"/>',
}


def ico(nombre):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % _P[nombre])


# ---------------------------------------------------------------- Idioma
class L:
    """Contexto de idioma de la página que se está generando."""

    def __init__(self, lang):
        self.lang = lang
        self.en = lang == 'en'
        self.pre = '../' if self.en else ''   # ruta hasta la raíz del sitio

    def t(self, par):
        if isinstance(par, (tuple, list)):
            return par[1] if self.en else par[0]
        return par

    def precio(self, p):
        return PRECIO_EN.get(p, p) if self.en else p


def e(s):
    return escape(s, quote=True)


# ---------------------------------------------------------------- Partials
# Plantillas en _fuente/partials/*.html con tres marcas:
#   {{ variable }}        valor que pasa el generador (ya escapado si hace falta)
#   {{ ico:nombre }}      icono SVG
#   {{ t: español || english }}  texto según el idioma de la página
PARTIALS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'partials')
_cache = {}
_RE_T = re.compile(r'\{\{\s*t:\s*(.*?)\s*\|\|\s*(.*?)\s*\}\}', re.S)
_RE_ICO = re.compile(r'\{\{\s*ico:([a-z]+)\s*\}\}')
_RE_VAR = re.compile(r'\{\{\s*([a-z_]+)\s*\}\}')


def parcial(nombre, l, **ctx):
    if nombre not in _cache:
        with open(os.path.join(PARTIALS, nombre + '.html'), encoding='utf-8') as f:
            _cache[nombre] = f.read().rstrip('\n')
    html = _RE_T.sub(lambda m: m.group(2) if l.en else m.group(1), _cache[nombre])
    html = _RE_ICO.sub(lambda m: ico(m.group(1)), html)

    def var(m):
        if m.group(1) not in ctx:
            raise KeyError('Falta «%s» en el partial %s.html' % (m.group(1), nombre))
        return str(ctx[m.group(1)])
    html = _RE_VAR.sub(var, html)
    if '{{' in html:
        raise ValueError('Marca sin resolver en el partial %s.html' % nombre)
    return html


# ---------------------------------------------------------------- Menú
NAV = [
    ('index', ('Inicio', 'Home')),
    ('casos-de-uso', ('Casos de uso', 'Use cases')),
    ('historias-de-exito', ('Historias de éxito', 'Success stories')),
    ('como-funciona', ('Cómo funciona', 'How it works')),
    ('planes', ('Planes', 'Plans')),
    ('afiliados', ('Afiliados', 'Affiliates')),
    ('quienes-somos', ('Quiénes somos', 'About us')),
    ('preguntas-frecuentes', ('Preguntas frecuentes', 'FAQ')),
    ('contacto', ('Contacto', 'Contact')),
]


def pago(l, producto, origen):
    """Enlace al abono personalizado con importe, concepto y página de origen."""
    importe, concepto = PAGO['productos'][producto]
    params = [('concepto', l.t(concepto)), ('origen', origen)]
    if importe:
        params.insert(0, ('importe', importe))
    return l.t(PAGO['url']) + '?' + urlencode(params, quote_via=quote)


# ---------------------------------------------------------------- Esqueleto
def pagina(l, slug, titulo, descripcion, cuerpo, activo=None, og_img=None, form=True):
    base = EMPRESA['base_url']
    url_es = base + slug + '.html'
    url_en = base + 'en/' + slug + '.html'
    zona = l.t(EMPRESA['zona'])
    nav_items = ''.join(
        '<li><a href="%s.html"%s>%s</a></li>' % (
            s, ' class="active" aria-current="%s"' % ('page' if s == slug else 'true') if s == activo else '', l.t(n))
        for s, n in NAV)
    destino = 'index' if slug == '404' else slug   # no existe en/404.html
    otro = ('<a href="../%s.html" hreflang="es" lang="es" title="Español">ES</a> · '
            '<a href="%s.html" hreflang="en" lang="en" aria-current="true">EN</a>' % (slug, slug)) if l.en else \
           ('<a href="%s.html" hreflang="es" lang="es" aria-current="true">ES</a> · '
            '<a href="en/%s.html" hreflang="en" lang="en" title="English">EN</a>' % (slug, destino))
    sol_links = ''.join(
        '<li><a href="%s.html">%s<span>%s</span></a></li>' % (s['slug'], ico(s['ico']), l.t(s['nombre']))
        for s in SOLUCIONES) + ''.join(
        '<li><a href="%s.html">%s<span>%s</span></a></li>' % (s, ico(i), l.t(n)) for s, i, n in [
            ('casos-de-uso', 'estrella', ('Casos de uso', 'Use cases')),
            ('industrias', 'tienda', ('Por industria', 'By industry')),
        ])
    if form:
        cuerpo += form_contacto(l)
    emp_links = ''.join(
        '<li><a href="%s.html">%s<span>%s</span></a></li>' % (s, ico(i), l.t(n)) for s, i, n in [
            ('como-funciona', 'engranaje', ('Cómo funciona', 'How it works')),
            ('planes', 'etiqueta', ('Planes', 'Plans')),
            ('historias-de-exito', 'corazon', ('Historias de éxito', 'Success stories')),
            ('afiliados', 'euro', ('Programa de afiliados', 'Affiliate programme')),
            ('quienes-somos', 'personas', ('Quiénes somos', 'About us')),
            ('preguntas-frecuentes', 'pregunta', ('Preguntas frecuentes', 'FAQ')),
            ('contacto', 'mail', ('Contacto', 'Contact')),
        ])
    if slug == '404':
        enlaces_seo = '<meta name="robots" content="noindex">'
    else:
        actual = url_en if l.en else url_es
        enlaces_seo = '\n'.join([
            '<link rel="canonical" href="%s">' % actual,
            '<meta property="og:url" content="%s">' % actual,
            '<link rel="alternate" hreflang="es" href="%s">' % url_es,
            '<link rel="alternate" hreflang="en" href="%s">' % url_en,
            '<link rel="alternate" hreflang="x-default" href="%s">' % url_es,
        ])
    comun = dict(pre=l.pre, zona=zona, email=EMPRESA['email'], gtm_id=GTM_ID)
    return '\n'.join([
        parcial('head', l, lang=l.lang, titulo=e(titulo), descripcion=e(descripcion),
                og_img=e(og_img or base + 'assets/og.png'), enlaces_seo=enlaces_seo, **comun),
        parcial('cabecera', l, idiomas=otro, nav_items=nav_items, **comun),
        '', '<main id="contenido" tabindex="-1">', cuerpo, '</main>',
        parcial('pie', l, sol_links=sol_links, emp_links=emp_links, anio=ANIO,
                biscotti_reabrir=BISCOTTI_REABRIR, **comun),
    ]) + '\n'


# ---------------------------------------------------------------- Bloques
def page_head(l, titulo, texto, migas, img=None, antetitulo=None):
    m = '<a href="index.html">%s</a>' % l.t(('Inicio', 'Home'))
    for href, txt in migas[:-1]:
        m += '<span>/</span><a href="%s">%s</a>' % (href, txt)
    m += '<span>/</span>' + migas[-1][1]
    estilo = ' con-foto" style="--foto:url(\'%s\')' % IMG[img] if img else ''
    ante = '<span class="eyebrow">%s</span>\n  ' % antetitulo if antetitulo else ''
    return f'''<div class="page-head{estilo}"><div class="wrap">
  <div class="crumbs">{m}</div>
  {ante}<h1>{titulo}</h1>
  <p>{texto}</p>
</div></div>'''


def pasos(l, lista, clase='g3'):
    items = ''.join(
        '<div class="paso"><span class="paso-n">%02d</span><h3>%s</h3><p>%s</p></div>' % (i + 1, l.t(t), l.t(d))
        for i, (t, d) in enumerate(lista))
    return '<div class="grid %s pasos">%s</div>' % (clase, items)


def faq(l, lista):
    return '<div class="faq">' + ''.join(
        '<details class="faq-item"><summary>%s%s</summary><div class="faq-r"><p>%s</p></div></details>'
        % (l.t(q), ico('abajo'), l.t(r)) for q, r in lista) + '</div>'


def tarjetas_planes(l, origen, destacar='anual'):
    out = []
    for clave, nombre, mes, total, dto in PLANES:
        badge = '<span class="plan-dto">%s</span>' % dto if dto else ''
        cls = ' plan-top' if clave == destacar else ''
        top = '<span class="plan-reco">%s</span>' % l.t(('Mejor precio', 'Best price')) if clave == destacar else ''
        out.append(f'''<div class="plan{cls}">{top}
  <div class="plan-cab"><h3>{l.t(nombre)}</h3>{badge}</div>
  <p class="plan-precio"><b>{l.precio(mes)}</b><span>{l.t(('/mes', '/month'))}</span></p>
  <p class="plan-total">{l.t(total)}</p>
  <a class="btn {'btn-primary' if clave == destacar else 'btn-ghost'}" href="{e(pago(l, clave, origen))}" rel="noopener">{ico('carrito')}{l.t(('Elegir', 'Choose'))} {l.t(nombre).lower()}</a>
</div>''')
    return '<div class="grid g4 planes">' + ''.join(out) + '</div>'


def tarjeta_solucion(l, s):
    return f'''<a class="card sol" href="{s['slug']}.html">
  <div class="sol-img"><img src="{IMG[s['img']]}" alt="" loading="lazy" width="800" height="533"></div>
  <div class="sol-txt">
    <span class="ico">{ico(s['ico'])}</span>
    <h3>{l.t(s['nombre'])}</h3><p>{l.t(s['resumen'])}</p>
    <span class="more">{l.t(('Saber más', 'Learn more'))} {ico('flecha')}</span>
  </div>
</a>'''


def panel(l, titulo, texto, botones):
    return f'''<section class="tight"><div class="wrap"><div class="panel">
  <h2>{titulo}</h2>
  <p>{texto}</p>
  <div class="actions">{botones}</div>
</div></div></section>'''


def btn(href, txt, clase='btn-primary', icono=None, externo=False):
    ext = ' rel="noopener"' if externo else ''
    return '<a class="btn %s" href="%s"%s>%s%s</a>' % (clase, e(href), ext, ico(icono) if icono else '', txt)


# ---------------------------------------------------------------- Páginas
def p_index(l):
    sols = ''.join(tarjeta_solucion(l, s) for s in SOLUCIONES)
    disp = ''.join('<li>%s<span><b>%s</b></span></li>' % (ico('check'), l.t(t)) for _, t in DISPOSITIVO)
    masc, publi = SOLUCIONES[1], SOLUCIONES[3]
    cuerpo = f'''
<div class="hero con-foto" style="--foto:url('{IMG['vehiculo']}')"><div class="wrap">
  <span class="respaldo">{l.t(('Canarias, en movimiento', 'The Canaries, on the move'))}</span>
  <h1>{l.t(('Que nunca pierdas de vista lo que te importa', 'Never lose sight of what matters to you'))}</h1>
  <p class="lead">{l.t(('Tu coche, tu negocio, tu mascota. Un solo dispositivo, sin instalación, sin depender de la luz ni del wifi.', 'Your car, your business, your pet. One device, no installation, no reliance on mains power or wifi.'))}</p>
  <div class="actions">
    {btn('planes.html', l.t(('Ver planes', 'See plans')), icono='etiqueta')}
    {btn('como-funciona.html', l.t(('Cómo funciona', 'How it works')), 'btn-line')}
  </div>
  <div class="hero-stats">
    <div><b>5</b><span>{l.t(('casos de uso', 'use cases'))}</span></div>
    <div><b>240</b><span>{l.t(('días de batería', 'days of battery'))}</span></div>
    <div><b>{l.precio('3,50 €')}</b><span>{l.t(('al mes, desde', 'a month, from'))}</span></div>
    <div><b>0</b><span>{l.t(('cables e instalación', 'cables or installation'))}</span></div>
  </div>
</div></div>

<section><div class="wrap">
  <div class="section-head">
    <span class="eyebrow-dark">{l.t(('Soluciones', 'Solutions'))}</span>
    <h2>{l.t(('Elige tu caso', 'Choose your case'))}</h2>
    <p>{l.t(('Un mismo dispositivo para cinco necesidades distintas. Entra en la tuya para ver cómo funciona.', 'One device for five different needs. Open yours to see how it works.'))}</p>
  </div>
  <div class="grid g3 sols">{sols}</div>
  <div class="pie-seccion">{btn('casos-de-uso.html', l.t(('Ver todos los casos de uso', 'See all use cases')), 'btn-ghost', 'flecha')}{btn('industrias.html', l.t(('Casos por industria', 'Use cases by industry')), 'btn-ghost', 'tienda')}</div>
</div></section>

<section class="alt"><div class="wrap">
  <div class="grid g2 destacado" style="align-items:center;gap:44px">
    <div class="foto-marco"><img src="{IMG['mascotas']}" alt="{l.t(('Perro con collar GPS', 'Dog wearing a GPS collar'))}" loading="lazy" width="800" height="533"></div>
    <div>
      <span class="eyebrow-dark">{l.t(masc['nombre'])}</span>
      <h2>{l.t(masc['titulo'])}</h2>
      <p class="entradilla">{l.t(('Localiza a tu mascota en minutos, sin depender de que alguien la vea pasar.', 'Locate your pet in minutes, without relying on someone seeing it go by.'))}</p>
      {btn(masc['slug'] + '.html', l.t(('Saber más', 'Learn more')), 'btn-ghost')}
    </div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="grid g2 destacado" style="align-items:center;gap:44px">
    <div>
      <span class="eyebrow-dark">{l.t(publi['antetitulo'])}</span>
      <h2>{l.t(publi['titulo'])}</h2>
      <p class="entradilla">{l.t(publi['problema'])}</p>
      <div class="btn-par">{btn(publi['slug'] + '.html', l.t(('Saber más', 'Learn more')), 'btn-ghost')}{btn('contacto.html', l.t(('Hablemos', 'Let’s talk')), 'btn-navy', 'mail')}</div>
    </div>
    <div class="foto-marco"><img src="{IMG['publicidad']}" alt="{l.t(('Vehículos de flota turística', 'Tourist fleet vehicles'))}" loading="lazy" width="800" height="533"></div>
  </div>
</div></section>

<section class="alt"><div class="wrap">
  <div class="section-head">
    <span class="eyebrow-dark">{l.t(('Cómo funciona', 'How it works'))}</span>
    <h2>{l.t(('Del paquete a la app, sin complicaciones', 'From the box to the app, hassle-free'))}</h2>
  </div>
  {pasos(l, PASOS[:3])}
  <div class="grid g2" style="margin-top:34px;align-items:center;gap:30px">
    <ul class="checks chips">{disp}</ul>
    <div>{btn('como-funciona.html', l.t(('Ver en detalle', 'See in detail')), 'btn-ghost', 'flecha')}</div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="section-head">
    <span class="eyebrow-dark">{l.t(('Planes', 'Plans'))}</span>
    <h2>{l.t(('Un precio claro, sin sorpresas', 'A clear price, no surprises'))}</h2>
    <p>{l.t(('Elige la duración que mejor te encaje. Cuanto más tiempo eliges, menos pagas al mes.', 'Choose the length that suits you best. The longer you choose, the less you pay per month.'))}</p>
  </div>
  {tarjetas_planes(l, 'index')}
  <p class="note-inline" style="margin-top:18px">{l.t(('Precios con IGIC incluido para clientes en Canarias. El dispositivo se compra aparte, con pago único.', 'Prices include IGIC for customers in the Canary Islands. The device is bought separately, with a one-off payment.'))} <a href="planes.html">{l.t(('Ver planes', 'See plans'))}</a></p>
</div></section>

<section class="alt"><div class="wrap">
  <div class="section-head">
    <span class="eyebrow-dark">{l.t(('Historias de éxito', 'Success stories'))}</span>
    <h2>{l.t(('Esto es lo que pasa cuando no pierdes de vista lo que te importa', 'This is what happens when you never lose sight of what matters to you'))}</h2>
  </div>
  {historias(l, [HISTORIAS_EXITO['solucion-vehiculo'][0], HISTORIAS_EXITO['solucion-mascotas'][0], HISTORIAS_EXITO['solucion-flotas'][0]])}
  <div class="pie-seccion">{btn('historias-de-exito.html', l.t(('Ver todas las historias', 'See all stories')), 'btn-ghost', 'flecha')}</div>
</div></section>

{panel(l, l.t(('¿Listo para no perderlo de vista?', 'Ready to never lose sight of it?')),
       l.t(('¿Tienes dudas sobre qué plan elegir, o quieres hablar de una campaña de publicidad en movimiento? Cuéntanos qué necesitas.', 'Not sure which plan to choose, or want to talk about an advertising-on-the-move campaign? Tell us what you need.')),
       btn('planes.html', l.t(('Ver planes', 'See plans')), icono='etiqueta') + btn('#escribenos', l.t(('Hablemos', 'Let’s talk')), 'btn-line', 'mail'))}
{relacionados(l, ['casos-de-uso', 'historias-de-exito', 'afiliados'])}
'''
    return pagina(l, 'index', l.t(('Canary GPS — Localización GPS para tu coche, mascota o negocio en Canarias',
                                   'Canary GPS — GPS tracking for your car, pet or business in the Canary Islands')),
                  l.t(('Tu coche, tu negocio, tu mascota. Un solo dispositivo GPS, sin instalación, sin depender de la luz ni del wifi. Planes desde 3,50 €/mes.',
                       'Your car, your business, your pet. One GPS device, no installation, no reliance on mains power or wifi. Plans from €3.50/month.')),
                  cuerpo, 'index')


def p_soluciones(l):
    """La antigua página «Soluciones» redirige a «Casos de uso»."""
    return f'''<!DOCTYPE html>
<html lang="{l.lang}">
<head>
<meta charset="utf-8">
<title>Canary GPS</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{EMPRESA['base_url']}{'en/' if l.en else ''}casos-de-uso.html">
<meta http-equiv="refresh" content="0; url=casos-de-uso.html">
</head>
<body><p><a href="casos-de-uso.html">{l.t(('Casos de uso', 'Use cases'))}</a></p></body>
</html>
'''


def p_solucion(l, s):
    cta = {
        'planes': btn('planes.html', l.t(('Ver planes', 'See plans')), icono='etiqueta'),
        'contacto': btn('contacto.html', l.t(('Habla con nosotros', 'Talk to us')), icono='mail'),
        'campana': btn('contacto.html', l.t(('Hablemos de tu campaña', 'Let’s talk about your campaign')), icono='mail'),
    }[s['cta_btn']]
    extra = ''
    if 'para' in s:
        tit, items = s['para']
        cards = ''.join('<div class="card cob"><h3>%s</h3><p>%s</p></div>' % (l.t(a), l.t(b)) for a, b in items)
        extra += f'''<section><div class="wrap">
  <div class="section-head"><span class="eyebrow-dark">{l.t(tit)}</span></div>
  <div class="grid g3">{cards}</div>
</div></section>'''
    if 'nota' in s:
        nt, nx = s['nota']
        extra += f'''<section class="tight"><div class="wrap"><div class="note nota-grande">{ico('info')}<div><b>{l.t(nt)}</b><p>{l.t(nx)}</p></div></div></div></section>'''
    if 'faq' in s:
        extra += f'''<section class="alt"><div class="wrap">
  <div class="section-head"><h2>{l.t(('Preguntas frecuentes', 'Frequently asked questions'))}</h2></div>
  {faq(l, s['faq'])}
</div></section>'''
    otras = ''.join(tarjeta_solucion(l, o) for o in SOLUCIONES if o is not s)
    cuerpo = page_head(l, l.t(s['titulo']), l.t(s['resumen']),
                       [('casos-de-uso.html', l.t(('Casos de uso', 'Use cases'))), ('', l.t(s['nombre']))],
                       img=s['img'], antetitulo=l.t(s['antetitulo'])) + f'''
<section><div class="wrap"><div class="grid g2" style="gap:44px;align-items:center">
  <div>
    <span class="eyebrow-dark">{l.t(s['nombre'])}</span>
    <p class="entradilla">{l.t(s['problema'])}</p>
    <div class="btn-par">{cta}{btn('como-funciona.html', l.t(('Cómo funciona', 'How it works')), 'btn-ghost')}</div>
  </div>
  <div class="foto-marco"><img src="{IMG[s['img']]}" alt="{e(l.t(s['nombre']))}" loading="lazy" width="800" height="533"></div>
</div></div></section>

<section class="alt"><div class="wrap">
  <div class="section-head"><span class="eyebrow-dark">{l.t(('Cómo funciona', 'How it works'))}</span><h2>{l.t(('Tres pasos y listo', 'Three steps and you’re set'))}</h2></div>
  {pasos(l, s['pasos'])}
</div></section>
{extra}
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow-dark">{l.t(('Historias de éxito', 'Success stories'))}</span><h2>{l.t(('Ya les ha pasado', 'It’s already happened to them'))}</h2></div>
  {historias(l, HISTORIAS_EXITO[s['slug']][:3])}
  <div class="pie-seccion">{btn('historias-de-exito.html#' + s['slug'], l.t(('Ver más historias', 'See more stories')), 'btn-ghost', 'flecha')}</div>
</div></section>
{panel(l, l.t(s['cta']), l.t(('Planes desde 3,50 €/mes con IGIC incluido. Sin instalación y sin cables.', 'Plans from €3.50/month including IGIC. No installation and no cables.')), cta + btn('contacto.html', l.t(('Contacto', 'Contact')), 'btn-line'))}

<section><div class="wrap">
  <div class="section-head"><h2>{l.t(('Otras soluciones', 'Other solutions'))}</h2></div>
  <div class="grid g4 sols mini">{otras}</div>
  <div class="pie-seccion">{btn('casos-de-uso.html', l.t(('Ver todos los casos de uso', 'See all use cases')), 'btn-ghost', 'flecha')}</div>
</div></section>
'''
    return pagina(l, s['slug'], '%s | Canary GPS' % l.t(s['nombre']), l.t(s['resumen']), cuerpo, 'casos-de-uso')


def p_como(l):
    disp = ''.join('<div class="card disp"><span class="ico">%s</span><h3>%s</h3></div>' % (ico(i), l.t(t)) for i, t in DISPOSITIVO)
    cuerpo = page_head(l, l.t(('Del paquete a la app, en cuatro pasos', 'From the box to the app, in four steps')),
                       l.t(('Sin instalador, sin cables, sin conocimientos técnicos.', 'No installer, no cables, no technical knowledge needed.')),
                       [('', l.t(('Cómo funciona', 'How it works')))]) + f'''
<section><div class="wrap">
  <h2 class="sr-only">{l.t(('Los cuatro pasos', 'The four steps'))}</h2>
  {pasos(l, PASOS, 'g4')}
</div></section>
<section class="alt"><div class="wrap">
  <div class="section-head"><span class="eyebrow-dark">{l.t(('El dispositivo', 'The device'))}</span><h2>{l.t(('Pensado para colocarse y olvidarse', 'Designed to fit and forget'))}</h2></div>
  <div class="grid g4">{disp}</div>
</div></section>
<section><div class="wrap">
  <div class="section-head"><h2>{l.t(('Preguntas frecuentes', 'Frequently asked questions'))}</h2></div>
  {faq(l, FAQ_GENERAL)}
</div></section>
''' + panel(l, l.t(('¿Listo para no perderlo de vista?', 'Ready to never lose sight of it?')),
            l.t(('Elige la duración que mejor te encaje. Cuanto más tiempo eliges, menos pagas al mes.', 'Choose the length that suits you best. The longer you choose, the less you pay per month.')),
            btn('planes.html', l.t(('Ver planes', 'See plans')), icono='etiqueta'))
    return pagina(l, 'como-funciona', l.t(('Cómo funciona Canary GPS — sin instalación, sin cables', 'How Canary GPS works — no installation, no cables')),
                  l.t(('Del paquete a la app, en cuatro pasos. Sin instalador, sin cables, sin conocimientos técnicos.', 'From the box to the app, in four steps. No installer, no cables, no technical knowledge needed.')),
                  cuerpo, 'como-funciona')


def p_planes(l):
    cuerpo = page_head(l, l.t(('Un precio claro, sin sorpresas', 'A clear price, no surprises')),
                       l.t(('Elige la duración que mejor te encaje. Cuanto más tiempo eliges, menos pagas al mes.', 'Choose the length that suits you best. The longer you choose, the less you pay per month.')),
                       [('', l.t(('Planes', 'Plans')))]) + f'''
<section><div class="wrap">
  <h2 class="sr-only">{l.t(('Elige tu plan', 'Choose your plan'))}</h2>
  {tarjetas_planes(l, 'planes')}
  <p class="note-inline" style="margin-top:18px">{l.t(('Precios con IGIC incluido para clientes en Canarias.', 'Prices include IGIC for customers in the Canary Islands.'))}</p>
</div></section>
<section class="alt"><div class="wrap"><div class="grid g2" style="gap:44px;align-items:center">
  <div>
    <span class="eyebrow-dark">{l.t(('El dispositivo', 'The device'))}</span>
    <h2>{l.t(('El dispositivo se compra aparte, con pago único', 'The device is bought separately, with a one-off payment'))}</h2>
    <p class="entradilla">{l.t(('La suscripción da acceso a la plataforma, la app y el historial de rutas. El dispositivo se coloca en minutos y no requiere instalación.', 'The subscription gives you access to the platform, the app and route history. The device is fitted in minutes and needs no installation.'))}</p>
    <div class="btn-par">{btn(pago(l, 'dispositivo', 'planes'), l.t(('Comprar dispositivo', 'Buy the device')), icono='carrito', externo=True)}{btn('como-funciona.html', l.t(('Ver cómo funciona', 'See how it works')), 'btn-ghost', 'flecha')}</div>
  </div>
  <ul class="checks">{''.join('<li>%s<span><b>%s</b></span></li>' % (ico('check'), l.t(t)) for _, t in DISPOSITIVO)}</ul>
</div></div></section>
<section><div class="wrap">
  <div class="section-head"><h2>{l.t(('Dudas sobre los planes', 'Questions about the plans'))}</h2></div>
  {faq(l, FAQ_GENERAL[1:3])}
</div></section>
'''
    return pagina(l, 'planes', l.t(('Planes y precios — Canary GPS', 'Plans and prices — Canary GPS')),
                  l.t(('Un precio claro, sin sorpresas. Elige la duración que mejor te encaje: mensual, trimestral, semestral o anual.', 'A clear price, no surprises. Choose the length that suits you best: monthly, quarterly, six-monthly or annual.')),
                  cuerpo, 'planes')


def p_quienes(l):
    hist = ''.join('<p>%s</p>' % l.t(p) for p in HISTORIA)
    val = ''.join('<div class="card"><span class="ico">%s</span><h3>%s</h3><p>%s</p></div>' % (ico(i), l.t(t), l.t(d))
                  for i, (t, d) in zip(['corazon', 'doc', 'escudo'], VALORES))
    cuerpo = page_head(l, l.t(('Somos de aquí, y se nota', 'We’re from here, and it shows')),
                       l.t(('Un proyecto canario para que nadie en las islas pierda de vista lo que le importa.', 'A Canary Islands project so that nobody on the islands loses sight of what matters to them.')),
                       [('', l.t(('Quiénes somos', 'About us')))]) + f'''
<section><div class="wrap"><div class="grid g2" style="gap:44px;align-items:start">
  <div class="texto-largo">
    <span class="eyebrow-dark">{l.t(('Nuestra historia', 'Our story'))}</span>
    <h2>{l.t(('Nace de una necesidad, no de un plan de negocio', 'Born of a need, not a business plan'))}</h2>
    {hist}
  </div>
  <div>
    <div class="foto-marco"><img src="{IMG['vehiculo']}" alt="{l.t(('Furgoneta camperizada aparcada', 'Parked campervan'))}" loading="lazy" width="800" height="533"></div>
    <div class="hero-stats claro">
      <div><b>5</b><span>{l.t(('Casos de uso', 'Use cases'))}</span></div>
      <div><b>240</b><span>{l.t(('Días de batería', 'Days of battery'))}</span></div>
    </div>
  </div>
</div></div></section>
<section class="alt"><div class="wrap">
  <div class="section-head"><span class="eyebrow-dark">{l.t(('Cómo trabajamos', 'How we work'))}</span><h2>{l.t(('Lo que nos mueve', 'What drives us'))}</h2></div>
  <div class="grid g3">{val}</div>
</div></section>
''' + panel(l, l.t(('¿Hablamos?', 'Shall we talk?')),
            l.t(('Si tienes un problema, hablas con alguien que lo entiende.', 'If you have a problem, you talk to someone who understands it.')),
            btn('contacto.html', l.t(('Contacto', 'Contact')), icono='mail') + btn('planes.html', l.t(('Ver planes', 'See plans')), 'btn-line'))
    return pagina(l, 'quienes-somos', l.t(('Quiénes somos — Canary GPS', 'About us — Canary GPS')),
                  l.t(('Un proyecto canario para que nadie en las islas pierda de vista lo que le importa.', 'A Canary Islands project so that nobody on the islands loses sight of what matters to them.')),
                  cuerpo, 'quienes-somos')


def p_faq(l):
    bloques = '<h2>%s</h2>%s' % (l.t(('General', 'General')), faq(l, FAQ_GENERAL))
    for s in SOLUCIONES:
        if 'faq' in s:
            bloques += '<h2 style="margin-top:40px">%s</h2>%s' % (l.t(s['nombre']), faq(l, s['faq']))
    cuerpo = page_head(l, l.t(('Preguntas frecuentes', 'Frequently asked questions')),
                       l.t(('Lo que más nos preguntan sobre el dispositivo, los planes y la app.', 'What people ask us most about the device, the plans and the app.')),
                       [('', l.t(('Preguntas frecuentes', 'FAQ')))]) + f'''
<section><div class="wrap">{bloques}</div></section>
''' + panel(l, l.t(('¿No encuentras tu respuesta?', 'Can’t find your answer?')),
            l.t(('Cuéntanos qué necesitas y te respondemos.', 'Tell us what you need and we’ll get back to you.')),
            btn('contacto.html', l.t(('Contacto', 'Contact')), icono='mail'))
    return pagina(l, 'preguntas-frecuentes', l.t(('Preguntas frecuentes — Canary GPS', 'FAQ — Canary GPS')),
                  l.t(('Respuestas sobre el dispositivo GPS, la batería, los planes y la cancelación.', 'Answers about the GPS device, battery, plans and cancellation.')),
                  cuerpo, 'preguntas-frecuentes')


def p_contacto(l):
    cuerpo = page_head(l, l.t(('Habla con nosotros', 'Talk to us')),
                       l.t(('¿Tienes dudas sobre qué plan elegir, o quieres hablar de una campaña de publicidad en movimiento? Cuéntanos qué necesitas.',
                            'Not sure which plan to choose, or want to talk about an advertising-on-the-move campaign? Tell us what you need.')),
                       [('', l.t(('Contacto', 'Contact')))], img='hogar', antetitulo=l.t(('Contacto', 'Contact')))
    cuerpo += form_contacto(l, titulo=l.t(('Escríbenos', 'Write to us')),
                            texto=l.t(('Te respondemos por correo o por teléfono, como prefieras.', 'We’ll reply by email or phone, whichever you prefer.')))
    cuerpo += f'''
<section class="tight"><div class="wrap"><div class="note"><p>{l.t(('¿Ya sabes lo que quieres? Puedes', 'Already know what you want? You can'))} <a href="planes.html">{l.t(('elegir tu plan', 'choose your plan'))}</a> {l.t(('o', 'or'))} <a href="{e(pago(l, 'dispositivo', 'contacto'))}" rel="noopener">{l.t(('comprar el dispositivo', 'buy the device'))}</a> {l.t(('directamente. ¿Quieres recomendar Canary GPS?', 'directly. Want to recommend Canary GPS?'))} <a href="afiliados.html">{l.t(('Hazte afiliado', 'Become an affiliate'))}</a>.</p></div></div></section>
''' + relacionados(l, ['casos-de-uso', 'historias-de-exito', 'afiliados'])
    return pagina(l, 'contacto', l.t(('Contacto — Canary GPS', 'Contact — Canary GPS')),
                  l.t(('¿Tienes dudas sobre qué plan elegir, o quieres hablar de una campaña de publicidad en movimiento? Cuéntanos qué necesitas.',
                       'Not sure which plan to choose, or want to talk about an advertising-on-the-move campaign? Tell us what you need.')),
                  cuerpo, 'contacto', form=False)


# ---------------------------------------------------------------- Bloques nuevos
def historias(l, lista):
    return '<div class="grid g3 historias">' + ''.join(
        '<figure class="historia"><figcaption>%s%s</figcaption><blockquote>%s</blockquote></figure>'
        % (ico('pin'), l.t((le, len_)), l.t((te, ten))) for le, len_, te, ten in lista) + '</div>'


def solucion(slug):
    return next(x for x in SOLUCIONES if x['slug'] == slug)


def tarjeta_rel(l, href, img, icono, titulo, texto):
    return f'''<a class="card sol" href="{href}">
  <div class="sol-img"><img src="{IMG[img]}" alt="" loading="lazy" width="800" height="533"></div>
  <div class="sol-txt">
    <span class="ico">{ico(icono)}</span>
    <h3>{titulo}</h3><p>{texto}</p>
    <span class="more">{l.t(('Saber más', 'Learn more'))} {ico('flecha')}</span>
  </div>
</a>'''


REL = {
    'casos-de-uso': ('casos-de-uso.html', 'vehiculo', 'estrella', ('Casos de uso', 'Use cases'),
                     ('Un mismo dispositivo, cinco maneras de protegerte.', 'One device, five ways to protect yourself.')),
    'industrias': ('industrias.html', 'flotas', 'tienda', ('Casos por industria', 'Use cases by industry'),
                   ('Esto es lo que Canary GPS resuelve según tu sector.', 'This is what Canary GPS solves in your sector.')),
    'historias-de-exito': ('historias-de-exito.html', 'mascotas', 'corazon', ('Historias de éxito', 'Success stories'),
                           ('Gente real de las siete islas que no perdió de vista lo que le importa.', 'Real people from all seven islands who never lost sight of what matters to them.')),
    'afiliados': ('afiliados.html', 'publicidad', 'euro', ('Programa de afiliados', 'Affiliate programme'),
                  ('Gana una comisión recurrente por cada cliente que traigas.', 'Earn recurring commission for every customer you bring in.')),
    'planes': ('planes.html', 'hogar', 'etiqueta', ('Planes y precios', 'Plans and prices'),
               ('Desde 3,50 € al mes, IGIC incluido. Sin sorpresas.', 'From €3.50 a month, IGIC included. No surprises.')),
}


def relacionados(l, claves, titulo=('También te puede interesar', 'You may also be interested in')):
    cards = ''.join(tarjeta_rel(l, h, i, ic, l.t(t), l.t(x)) for h, i, ic, t, x in (REL[c] for c in claves))
    return f'''<section><div class="wrap">
  <div class="section-head"><h2>{l.t(titulo)}</h2></div>
  <div class="grid g3 sols mini">{cards}</div>
</div></section>'''


def form_contacto(l, titulo=None, texto=None, afiliado=False):
    """Formulario de contacto que va siempre antes del pie (partials/formulario.html)."""
    if afiliado:
        titulo = titulo or l.t(('Solicita tu código de afiliado', 'Apply for your affiliate code'))
        texto = texto or l.t(('Cuéntanos un poco sobre ti y te damos de alta.', 'Tell us a bit about yourself and we’ll sign you up.'))
        campos = parcial('campos-afiliado', l, opciones=''.join('<option>%s</option>' % l.t(c) for c in AFI_CANALES))
        asunto = l.t(('Solicitud de código de afiliado', 'Affiliate code application'))
        boton = l.t(('Enviar solicitud', 'Send application'))
        ancla = 'solicitud'
    else:
        titulo = titulo or l.t(('Habla con nosotros', 'Talk to us'))
        texto = texto or l.t(('¿Tienes dudas sobre qué plan elegir, o quieres hablar de una campaña de publicidad en movimiento? Cuéntanos qué necesitas.',
                              'Not sure which plan to choose, or want to talk about an advertising-on-the-move campaign? Tell us what you need.'))
        campos = parcial('campos-contacto', l, opciones=''.join('<option>%s</option>' % l.t(x['nombre']) for x in SOLUCIONES))
        asunto = l.t(('Consulta', 'Enquiry'))
        boton = l.t(('Enviar mensaje', 'Send message'))
        ancla = 'escribenos'
    return parcial('formulario', l, ancla=ancla, titulo=titulo, texto=texto, campos=campos,
                   asunto=e(asunto), boton=boton, zona=l.t(EMPRESA['zona']), email=EMPRESA['email'],
                   telefono=EMPRESA['telefono'], telefono_href=EMPRESA['telefono_href'])


def tabla_industrias(l, enlazar_historias=True):
    filas = ''
    for ind in INDUSTRIAS:
        sols = ' · '.join('<a href="%s.html">%s</a>' % (x, l.t(solucion(x)['nombre'])) for x in ind['soluciones'])
        nombre = '<a href="industrias.html#%s">%s</a>' % (ind['id'], l.t(ind['nombre'])) if enlazar_historias else l.t(ind['nombre'])
        filas += '<tr><td data-col="%s">%s</td><td data-col="%s">%s</td><td data-col="%s">%s</td></tr>' % (
            l.t(('Sector', 'Sector')), nombre, l.t(('Necesidad típica', 'Typical need')), l.t(ind['necesidad']),
            l.t(('Solución que aplica', 'Solution')), sols)
    return f'''<div class="tabla-scroll"><table class="datos pares">
  <thead><tr><th>{l.t(('Sector', 'Sector'))}</th><th>{l.t(('Necesidad típica', 'Typical need'))}</th><th>{l.t(('Solución que aplica', 'Solution'))}</th></tr></thead>
  <tbody>{filas}</tbody>
</table></div>'''


def p_casos(l):
    cards = ''.join(f'''<a class="card sol" href="{x['slug']}.html">
  <div class="sol-img"><img src="{IMG[x['img']]}" alt="" loading="lazy" width="800" height="533"></div>
  <div class="sol-txt">
    <span class="ico">{ico(x['ico'])}</span>
    <h3>{l.t(x['nombre'])}</h3><p>{l.t(x['titulo'])}</p>
    <span class="more">{l.t(('Ver más', 'See more'))} {ico('flecha')}</span>
  </div>
</a>''' for x in SOLUCIONES)
    cuerpo = page_head(l, l.t(('Un mismo dispositivo, cinco maneras de protegerte', 'One device, five ways to protect yourself')),
                       l.t(('Elige el que se ajusta a lo que quieres cuidar. Todos comparten el mismo aparato y la misma suscripción.',
                            'Choose the one that fits what you want to look after. They all share the same device and the same subscription.')),
                       [('', l.t(('Casos de uso', 'Use cases')))], img='vehiculo', antetitulo=l.t(('Casos de uso', 'Use cases'))) + f'''
<section><div class="wrap">
  <h2 class="sr-only">{l.t(('Soluciones', 'Solutions'))}</h2>
  <div class="grid g3 sols">{cards}</div>
</div></section>
<section class="alt"><div class="wrap">
  <div class="section-head">
    <span class="eyebrow-dark">{l.t(('Por industria', 'By industry'))}</span>
    <h2>{l.t(('¿A qué te dedicas?', 'What do you do?'))}</h2>
    <p>{l.t(('Esto es lo que Canary GPS resuelve según tu sector.', 'This is what Canary GPS solves in your sector.'))}</p>
  </div>
  {tabla_industrias(l)}
  <div class="pie-seccion">{btn('industrias.html', l.t(('Ver casos por industria', 'See use cases by industry')), 'btn-ghost', 'flecha')}</div>
</div></section>
''' + panel(l, l.t(('¿No sabes cuál encaja contigo?', 'Not sure which one fits you?')),
            l.t(('Cuéntanos qué quieres cuidar y te ayudamos a elegir.', 'Tell us what you want to look after and we’ll help you choose.')),
            btn('contacto.html', l.t(('Escríbenos y te ayudamos a elegir', 'Write to us and we’ll help you choose')), icono='mail') +
            btn('planes.html', l.t(('Ver planes', 'See plans')), 'btn-line')) + \
        relacionados(l, ['industrias', 'historias-de-exito', 'afiliados'])
    return pagina(l, 'casos-de-uso', l.t(('Casos de uso — Canary GPS', 'Use cases — Canary GPS')),
                  l.t(('Un mismo dispositivo, cinco maneras de protegerte. Descubre cómo usar Canary GPS según lo que quieras cuidar.',
                       'One device, five ways to protect yourself. Find out how to use Canary GPS for whatever you want to look after.')),
                  cuerpo, 'casos-de-uso')


def chips(items):
    return '<nav class="chips-nav">' + ''.join('<a href="#%s">%s%s</a>' % (a, ico(i), t) for a, i, t in items) + '</nav>'


def p_industrias(l):
    bloques = ''
    for n, ind in enumerate(INDUSTRIAS):
        sols = ''.join(btn(x + '.html', l.t(solucion(x)['nombre']), 'btn-ghost', solucion(x)['ico']) for x in ind['soluciones'])
        bloques += f'''<section class="{'alt' if n % 2 == 0 else ''} bloque-ind" id="{ind['id']}"><div class="wrap">
  <div class="section-head ind-head">
    <span class="ico-grande">{ico(ind['ico'])}</span>
    <div><h2>{l.t(ind['nombre'])}</h2><p>{l.t(ind['necesidad'])}</p></div>
  </div>
  {historias(l, ind['historias'])}
  <div class="pie-seccion"><div class="btn-par">{sols}</div></div>
</div></section>'''
    cuerpo = page_head(l, l.t(('¿A qué te dedicas?', 'What do you do?')),
                       l.t(('Esto es lo que Canary GPS resuelve según tu sector, con casos de las siete islas.',
                            'This is what Canary GPS solves in your sector, with examples from all seven islands.')),
                       [('casos-de-uso.html', l.t(('Casos de uso', 'Use cases'))), ('', l.t(('Por industria', 'By industry')))],
                       img='flotas', antetitulo=l.t(('Casos de uso por industria', 'Use cases by industry'))) + f'''
<section><div class="wrap">
  <div class="section-head"><h2>{l.t(('Tabla resumen', 'Summary'))}</h2></div>
  {tabla_industrias(l)}
  {chips([(i['id'], i['ico'], l.t(i['nombre'])) for i in INDUSTRIAS])}
</div></section>
{bloques}
''' + panel(l, l.t(('¿Tu sector no aparece?', 'Is your sector missing?')),
            l.t(('Cuéntanos a qué te dedicas y te decimos cómo te puede ayudar Canary GPS.', 'Tell us what you do and we’ll tell you how Canary GPS can help.')),
            btn('#escribenos', l.t(('Escríbenos', 'Write to us')), icono='mail') + btn('planes.html', l.t(('Ver planes', 'See plans')), 'btn-line')) + \
        relacionados(l, ['casos-de-uso', 'historias-de-exito', 'afiliados'])
    return pagina(l, 'industrias', l.t(('Casos de uso por industria — Canary GPS', 'Use cases by industry — Canary GPS')),
                  l.t(('Alquiler de vehículos, tours, reparto, obra, hostelería, segundas residencias, publicidad, particulares y mascotas: qué resuelve Canary GPS en cada sector.',
                       'Vehicle rental, tours, delivery, construction, hospitality, second homes, advertising, private owners and pets: what Canary GPS solves in each sector.')),
                  cuerpo, 'casos-de-uso')


def p_historias(l):
    bloques = ''
    for n, x in enumerate(SOLUCIONES):
        bloques += f'''<section class="{'alt' if n % 2 == 0 else ''} bloque-ind" id="{x['slug']}"><div class="wrap">
  <div class="section-head ind-head">
    <span class="ico-grande">{ico(x['ico'])}</span>
    <div><h2>{l.t(x['nombre'])}</h2><p>{l.t(x['titulo'])}</p></div>
  </div>
  {historias(l, HISTORIAS_EXITO[x['slug']])}
  <div class="pie-seccion">{btn(x['slug'] + '.html', l.t(('Ver la solución', 'See the solution')), 'btn-ghost', 'flecha')}</div>
</div></section>'''
    cuerpo = page_head(l, l.t(('Esto es lo que pasa cuando no pierdes de vista lo que te importa', 'This is what happens when you never lose sight of what matters to you')),
                       l.t(('Así es como Canary GPS ayuda a gente real a no perder de vista lo que le importa, en las siete islas.',
                            'This is how Canary GPS helps real people keep sight of what matters to them, across all seven islands.')),
                       [('', l.t(('Historias de éxito', 'Success stories')))], img='mascotas', antetitulo=l.t(('Historias de éxito', 'Success stories'))) + f'''
<section class="tight"><div class="wrap">
  {chips([(x['slug'], x['ico'], l.t(x['nombre'])) for x in SOLUCIONES])}
</div></section>
{bloques}
''' + panel(l, l.t(('¿Quieres ser la próxima historia?', 'Want to be the next story?')),
            l.t(('Planes desde 3,50 €/mes con IGIC incluido. Sin instalación y sin cables.', 'Plans from €3.50/month including IGIC. No installation and no cables.')),
            btn('planes.html', l.t(('Ver planes', 'See plans')), icono='etiqueta') + btn('#escribenos', l.t(('Contacto', 'Contact')), 'btn-line')) + \
        relacionados(l, ['casos-de-uso', 'industrias', 'afiliados'])
    return pagina(l, 'historias-de-exito', l.t(('Historias de éxito — Canary GPS', 'Success stories — Canary GPS')),
                  l.t(('Así es como Canary GPS ayuda a gente real a no perder de vista lo que le importa.',
                       'This is how Canary GPS helps real people keep sight of what matters to them.')),
                  cuerpo, 'historias-de-exito')


def p_afiliados(l):
    niveles = ''.join(f'''<div class="plan{' plan-top' if i == 2 else ''}">
  <div class="plan-cab"><h3>{l.t(n)}</h3><span class="plan-dto">{l.t(('Nivel', 'Tier'))} {i + 1}</span></div>
  <p class="plan-precio"><b>{c}</b><span>{l.t(('comisión', 'commission'))}</span></p>
  <p class="plan-total">{r} {l.t(('suscripciones activas', 'active subscriptions'))}</p>
</div>''' for i, (n, r, c) in enumerate(AFI_NIVELES))
    cuerpo = page_head(l, l.t(('Gana cada mes, no solo una vez', 'Earn every month, not just once')),
                       l.t(('Trae clientes con tu código y gana una comisión recurrente mientras sigan activos. Sin comprar dispositivos por adelantado.',
                            'Bring in customers with your code and earn recurring commission while they stay active. No need to buy devices up front.')),
                       [('', l.t(('Afiliados', 'Affiliates')))], img='publicidad', antetitulo=l.t(('Programa de afiliados', 'Affiliate programme'))) + f'''
<section><div class="wrap"><div class="grid g2" style="gap:44px;align-items:center">
  <div>
    <span class="eyebrow-dark">{l.t(('Programa de afiliados', 'Affiliate programme'))}</span>
    <p class="entradilla">{l.t(('Sin stock, sin mínimos de compra. Tu cliente paga menos con tu código y tú cobras cada mes que siga activo.', 'No stock, no minimum purchase. Your customer pays less with your code and you get paid every month they stay active.'))}</p>
    <div class="btn-par">{btn('#solicitud', l.t(('Solicita tu código', 'Apply for your code')), icono='euro')}{btn('planes.html', l.t(('Ver planes', 'See plans')), 'btn-ghost')}</div>
  </div>
  <div class="foto-marco"><img src="{IMG['publicidad']}" alt="" loading="lazy" width="800" height="533"></div>
</div></div></section>
<section class="alt"><div class="wrap">
  <div class="section-head"><span class="eyebrow-dark">{l.t(('Cómo funciona', 'How it works'))}</span><h2>{l.t(('Tres pasos y listo', 'Three steps and you’re set'))}</h2></div>
  {pasos(l, AFI_PASOS)}
</div></section>
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow-dark">{l.t(('Niveles', 'Tiers'))}</span><h2>{l.t(('Según cuántas suscripciones activas gestiones', 'Based on how many active subscriptions you manage'))}</h2></div>
  <div class="grid g3 planes">{niveles}</div>
</div></section>
<section class="tight"><div class="wrap"><div class="note nota-grande">{ico('info')}<div><b>{l.t(('Cómo se calcula', 'How it is calculated'))}</b><p>{l.t(('La comisión se calcula sobre el precio ya rebajado que paga tu cliente, no sobre el precio público — cuanto más volumen traigas, más subes de nivel automáticamente.', 'Commission is calculated on the discounted price your customer pays, not the public price. The more volume you bring in, the higher you climb, automatically.'))}</p></div></div></div></section>
<section class="alt"><div class="wrap">
  <div class="section-head"><h2>{l.t(('Preguntas frecuentes', 'Frequently asked questions'))}</h2></div>
  {faq(l, AFI_FAQ)}
</div></section>
''' + panel(l, l.t(('¿Ya tienes cartera de clientes que podrían necesitar esto?', 'Already have customers who could need this?')),
            l.t(('Solicita tu código y empieza a ganar comisión recurrente.', 'Apply for your code and start earning recurring commission.')),
            btn('#solicitud', l.t(('Solicita tu código', 'Apply for your code')), icono='flecha')) + \
        relacionados(l, ['casos-de-uso', 'historias-de-exito', 'planes'])
    return pagina(l, 'afiliados', l.t(('Hazte afiliado — Canary GPS', 'Become an affiliate — Canary GPS')),
                  l.t(('Gana comisión recurrente por cada cliente que traigas a Canary GPS. Sin stock, sin mínimos de compra.',
                       'Earn recurring commission for every customer you bring to Canary GPS. No stock, no minimum purchase.')),
                  cuerpo + form_contacto(l, afiliado=True), 'afiliados', form=False)



# ---------------------------------------------------------------- Legales
PENDIENTE = ('[pendiente de completar]', '[to be completed]')


def legal(l, slug, titulo, intro, secciones):
    nav = ''.join('<li><a href="#s%d">%s</a></li>' % (i, t) for i, (t, _) in enumerate(secciones, 1))
    body = ''.join('<div class="legal-sec" id="s%d"><h2>%s</h2>%s</div>' % (i, t, h) for i, (t, h) in enumerate(secciones, 1))
    cuerpo = page_head(l, titulo, intro, [('', titulo)]) + f'''
<section><div class="wrap"><div class="legal-layout">
  <nav class="legal-nav" aria-label="{titulo}"><h2 class="legal-nav-t">{l.t(('Contenido', 'Contents'))}</h2><ul class="foot-links dark">{nav}</ul></nav>
  <div class="legal-body">{body}<p class="legal-version">{l.t(('Última actualización:', 'Last updated:'))} {ANIO}.</p></div>
</div></div></section>'''
    return pagina(l, slug, '%s — Canary GPS' % titulo, intro, cuerpo)


def p_aviso(l):
    pend = l.t(PENDIENTE)
    mail = '<a href="mailto:%s">%s</a>' % (EMPRESA['email'], EMPRESA['email'])
    s = [
        (l.t(('Titular del sitio', 'Website owner')), l.t((
            f'<p>En cumplimiento de la Ley 34/2002, de Servicios de la Sociedad de la Información y de Comercio Electrónico (LSSI-CE), se informa de los datos del titular de este sitio web:</p><ul><li>Denominación: Canary GPS</li><li>Titular y NIF: {pend}</li><li>Domicilio: {pend}, Tenerife, Canarias</li><li>Correo electrónico: {mail}</li></ul>',
            f'<p>In accordance with Spanish Law 34/2002 on Information Society Services and Electronic Commerce (LSSI-CE), the details of the owner of this website are:</p><ul><li>Trading name: Canary GPS</li><li>Owner and tax ID: {pend}</li><li>Address: {pend}, Tenerife, Canary Islands</li><li>Email: {mail}</li></ul>'))),
        (l.t(('Objeto', 'Purpose')), l.t((
            '<p>Este sitio informa sobre los dispositivos de localización GPS y los planes de suscripción de Canary GPS. El pago se realiza en la tienda de Retuerto Graphic Design (retuertographicdesign.com), que informa de sus propias condiciones antes de cada compra.</p>',
            '<p>This website provides information about Canary GPS tracking devices and subscription plans. Payment is made in the Retuerto Graphic Design shop (retuertographicdesign.com), which sets out its own terms before each purchase.</p>'))),
        (l.t(('Precios', 'Prices')), l.t((
            '<p>Los precios mostrados incluyen el IGIC aplicable a clientes en Canarias. El dispositivo se adquiere con un pago único y la suscripción se abona según la duración elegida (mensual, trimestral, semestral o anual).</p>',
            '<p>The prices shown include the IGIC applicable to customers in the Canary Islands. The device is bought with a one-off payment and the subscription is paid according to the chosen length (monthly, quarterly, six-monthly or annual).</p>'))),
        (l.t(('Propiedad intelectual', 'Intellectual property')), l.t((
            '<p>La marca, el logotipo y los contenidos de este sitio pertenecen a su titular. Las fotografías proceden de Unsplash y se usan conforme a su licencia. No se permite su reproducción sin autorización.</p>',
            '<p>The brand, logo and content of this website belong to its owner. Photographs come from Unsplash and are used under its licence. Reproduction without permission is not allowed.</p>'))),
        (l.t(('Responsabilidad', 'Liability')), l.t((
            '<p>El titular procura que la información sea exacta y esté actualizada, pero no garantiza la ausencia de errores ni la disponibilidad continua del sitio. Los enlaces a sitios de terceros se ofrecen solo como referencia.</p>',
            '<p>The owner strives to keep the information accurate and up to date but does not guarantee the absence of errors or the continuous availability of the website. Links to third-party sites are provided for reference only.</p>'))),
        (l.t(('Legislación aplicable', 'Applicable law')), l.t((
            '<p>Estas condiciones se rigen por la legislación española.</p>', '<p>These terms are governed by Spanish law.</p>'))),
    ]
    return legal(l, 'aviso-legal', l.t(('Aviso legal', 'Legal notice')),
                 l.t(('Datos del titular y condiciones de uso de este sitio web.', 'Owner details and terms of use of this website.')), s)


def p_privacidad(l):
    pend = l.t(PENDIENTE)
    mail = '<a href="mailto:%s">%s</a>' % (EMPRESA['email'], EMPRESA['email'])
    s = [
        (l.t(('Responsable', 'Data controller')), l.t((
            f'<p>Canary GPS (titular y NIF: {pend}). Contacto: {mail}.</p>', f'<p>Canary GPS (owner and tax ID: {pend}). Contact: {mail}.</p>'))),
        (l.t(('Qué datos tratamos', 'What data we process')), l.t((
            '<p>Los que nos facilitas al escribirnos o suscribirte a las novedades: nombre, apellidos, correo electrónico, teléfono (opcional) y el contenido de tu mensaje. Este sitio no tiene formularios que envíen datos a un servidor: al enviar, se abre tu programa de correo con el mensaje redactado.</p>',
            '<p>The data you give us when you write to us or subscribe to our news: first name, surname, email address, phone (optional) and the content of your message. This website has no forms that send data to a server: when you submit, your email program opens with the message ready to send.</p>'))),
        (l.t(('Finalidad y legitimación', 'Purpose and legal basis')), l.t((
            '<p>Responder a tu consulta y, si te suscribes, enviarte novedades de Canary GPS. La base legal es tu consentimiento, que puedes retirar en cualquier momento.</p>',
            '<p>To reply to your enquiry and, if you subscribe, to send you news from Canary GPS. The legal basis is your consent, which you can withdraw at any time.</p>'))),
        (l.t(('Datos de localización', 'Location data')), l.t((
            '<p>Los datos de ubicación de los dispositivos se tratan en la plataforma de Canary GPS solo para prestar el servicio contratado. En la solución de publicidad en movimiento solo se comparten informes agregados de recorrido, con la autorización expresa del operador de la flota.</p>',
            '<p>Device location data is processed on the Canary GPS platform solely to provide the contracted service. In the advertising-on-the-move solution only aggregated route reports are shared, with the express authorisation of the fleet operator.</p>'))),
        (l.t(('Conservación', 'Retention')), l.t((
            '<p>Conservamos los datos mientras sean necesarios para la finalidad indicada y durante los plazos legales aplicables. El historial de rutas se guarda hasta 6 meses por dispositivo.</p>',
            '<p>We keep data for as long as it is needed for the stated purpose and for the applicable legal periods. Route history is kept for up to 6 months per device.</p>'))),
        (l.t(('Tus derechos', 'Your rights')), l.t((
            f'<p>Puedes ejercer tus derechos de acceso, rectificación, supresión, oposición, limitación y portabilidad escribiendo a {mail}. También puedes reclamar ante la Agencia Española de Protección de Datos (aepd.es).</p>',
            f'<p>You can exercise your rights of access, rectification, erasure, objection, restriction and portability by writing to {mail}. You can also lodge a complaint with the Spanish Data Protection Agency (aepd.es).</p>'))),
    ]
    return legal(l, 'politica-de-privacidad', l.t(('Política de privacidad', 'Privacy policy')),
                 l.t(('Cómo tratamos los datos personales que nos facilitas.', 'How we process the personal data you give us.')), s)


def p_cookies(l):
    s = [
        (l.t(('Gestión del consentimiento', 'Consent management')), l.t((
            '<p>Al entrar en el sitio se muestra el banner de Biscotti CMP, donde decides qué categorías de cookies aceptas. Las cookies que no son técnicas solo se activan con tu consentimiento. Puedes cambiar tu elección en cualquier momento desde el enlace «Preferencias de cookies» del pie de página.</p>',
            '<p>When you visit the site, the Biscotti CMP banner lets you choose which cookie categories you accept. Non-essential cookies are only activated with your consent. You can change your choice at any time from the “Cookie preferences” link in the footer.</p>'))),
        (l.t(('Analítica y etiquetas', 'Analytics and tags')), l.t((
            '<p>Las herramientas de medición y marketing se cargan a través de Google Tag Manager, y solo las que hayas aceptado en el banner.</p>',
            '<p>Measurement and marketing tools are loaded through Google Tag Manager, and only those you have accepted in the banner.</p>'))),
        (l.t(('Servicios de terceros', 'Third-party services')), l.t((
            '<p>Para mostrar las tipografías y las fotografías, tu navegador descarga recursos de Google Fonts (fonts.googleapis.com, fonts.gstatic.com) y de Unsplash (images.unsplash.com). Estos servicios pueden registrar tu dirección IP conforme a sus propias políticas de privacidad. La tienda donde se realiza el pago (retuertographicdesign.com) puede usar cookies técnicas necesarias para completar la compra.</p>',
            '<p>To display fonts and photographs, your browser downloads resources from Google Fonts (fonts.googleapis.com, fonts.gstatic.com) and Unsplash (images.unsplash.com). These services may log your IP address under their own privacy policies. The shop where payment is made (retuertographicdesign.com) may use technical cookies needed to complete a purchase.</p>'))),
        (l.t(('Cómo gestionarlas', 'How to manage them')), l.t((
            '<p>Cambia tu consentimiento desde el enlace «Preferencias de cookies» del pie. También puedes bloquear o eliminar las cookies desde la configuración de tu navegador.</p>',
            '<p>Change your consent from the “Cookie preferences” link in the footer. You can also block or delete cookies from your browser settings.</p>'))),
    ]
    return legal(l, 'cookies', l.t(('Política de cookies', 'Cookie policy')),
                 l.t(('Qué cookies y recursos de terceros utiliza este sitio.', 'Which cookies and third-party resources this website uses.')), s)


def lista_paginas(l):
    return [
        ('index', l.t(('Inicio', 'Home'))),
        ('casos-de-uso', l.t(('Casos de uso', 'Use cases'))),
    ] + [(s['slug'], '— ' + l.t(s['nombre'])) for s in SOLUCIONES] + [
        ('industrias', '— ' + l.t(('Casos por industria', 'Use cases by industry'))),
        ('historias-de-exito', l.t(('Historias de éxito', 'Success stories'))),
        ('afiliados', l.t(('Programa de afiliados', 'Affiliate programme'))),
        ('como-funciona', l.t(('Cómo funciona', 'How it works'))),
        ('planes', l.t(('Planes', 'Plans'))),
        ('quienes-somos', l.t(('Quiénes somos', 'About us'))),
        ('preguntas-frecuentes', l.t(('Preguntas frecuentes', 'FAQ'))),
        ('contacto', l.t(('Contacto', 'Contact'))),
        ('aviso-legal', l.t(('Aviso legal', 'Legal notice'))),
        ('politica-de-privacidad', l.t(('Política de privacidad', 'Privacy policy'))),
        ('cookies', l.t(('Política de cookies', 'Cookie policy'))),
    ]


def p_mapa(l):
    items = ''.join('<li><a href="%s.html">%s<span>%s</span></a></li>' % (s, ico('flecha'), t) for s, t in lista_paginas(l))
    cuerpo = page_head(l, l.t(('Mapa web', 'Site map')), l.t(('Todas las páginas del sitio.', 'Every page on the site.')),
                       [('', l.t(('Mapa web', 'Site map')))]) + \
        '<section><div class="wrap"><ul class="foot-links dark mapa">%s</ul></div></section>' % items
    return pagina(l, 'mapa-web', l.t(('Mapa web — Canary GPS', 'Site map — Canary GPS')),
                  l.t(('Todas las páginas del sitio de Canary GPS.', 'Every page on the Canary GPS website.')), cuerpo)


def p_404(l):
    cuerpo = page_head(l, l.t(('Esta página se ha perdido', 'This page has gone missing')),
                       l.t(('Y no llevaba GPS. Vuelve al inicio o elige una sección.', 'And it wasn’t wearing a GPS. Go back home or pick a section.')),
                       [('', '404')]) + panel(l, l.t(('¿Qué buscabas?', 'What were you looking for?')), '',
                                              btn('index.html', l.t(('Inicio', 'Home'))) + btn('casos-de-uso.html', l.t(('Casos de uso', 'Use cases')), 'btn-line') + btn('planes.html', l.t(('Planes', 'Plans')), 'btn-line'))
    return pagina(l, '404', 'Canary GPS — 404', l.t(('Página no encontrada.', 'Page not found.')), cuerpo)


# ---------------------------------------------------------------- Salida
def escribir(ruta, html):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(html)


def main():
    total = 0
    for lang in ('es', 'en'):
        l = L(lang)
        dest = os.path.join(RAIZ, 'en') if l.en else RAIZ
        paginas = {
            'index': p_index(l), 'soluciones': p_soluciones(l), 'casos-de-uso': p_casos(l),
            'industrias': p_industrias(l), 'historias-de-exito': p_historias(l), 'afiliados': p_afiliados(l),
            'como-funciona': p_como(l),
            'planes': p_planes(l), 'quienes-somos': p_quienes(l), 'preguntas-frecuentes': p_faq(l),
            'contacto': p_contacto(l), 'aviso-legal': p_aviso(l), 'politica-de-privacidad': p_privacidad(l),
            'cookies': p_cookies(l), 'mapa-web': p_mapa(l),
        }
        for s in SOLUCIONES:
            paginas[s['slug']] = p_solucion(l, s)
        for slug, html in paginas.items():
            escribir(os.path.join(dest, slug + '.html'), html)
            total += 1
        if not l.en:
            # GitHub Pages sirve 404.html en cualquier ruta: <base> fija los enlaces relativos.
            escribir(os.path.join(RAIZ, '404.html'),
                     p_404(l).replace('<head>\n', '<head>\n<base href="%s">\n' % EMPRESA['base_url'], 1))

    base = EMPRESA['base_url']
    urls = ''.join(
        '<url><loc>%s%s.html</loc><xhtml:link rel="alternate" hreflang="es" href="%s%s.html"/>'
        '<xhtml:link rel="alternate" hreflang="en" href="%sen/%s.html"/></url>\n' % (base, pre + s, base, s, base, s)
        for s, _ in lista_paginas(L('es')) for pre in ('', 'en/'))
    escribir(os.path.join(RAIZ, 'sitemap.xml'),
             '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
             'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + urls + '</urlset>\n')
    escribir(os.path.join(RAIZ, 'robots.txt'), 'User-agent: *\nAllow: /\nSitemap: %ssitemap.xml\n' % base)
    print('%d páginas generadas (+404, sitemap.xml, robots.txt)' % total)


if __name__ == '__main__':
    main()
