# Canary GPS — Localización GPS en Canarias

Sitio web estático y bilingüe de Canary GPS (20 páginas en español y 20 en inglés), con la estructura y la maquetación del sitio de Retuerto y Asociados y la identidad corporativa de Canary GPS: inicio, casos de uso (vehículo, mascotas, flotas, publicidad en movimiento, hogar y negocio), casos por industria, historias de éxito, programa de afiliados, cómo funciona, planes y precios, quiénes somos, preguntas frecuentes, contacto y páginas legales. Todas las páginas terminan con elementos relacionados y un formulario de contacto antes del pie (en Afiliados, el de solicitud de código). `soluciones.html` redirige a `casos-de-uso.html`.

- `*.html` — versión en español (raíz del sitio).
- `en/*.html` — versión en inglés, con los mismos nombres de archivo.
- `assets/` — estilos, script, logotipos (horizontal, en blanco e isotipo), favicon e imagen para redes. `site.js` adapta sus textos al idioma de la página (`<html lang>`).
- Cada página enlaza a su equivalente con el selector ES · EN de la barra superior y con `hreflang`. Incluye `sitemap.xml`, `robots.txt` y `404.html`.
- Los botones «Elegir plan» y «Comprar dispositivo» llevan a la plataforma de pagos (`pagos.canarygps.com`).
- Publicado con GitHub Pages (Deploy from a branch) con dominio propio: https://canarygps.com/ y https://canarygps.com/en/ (archivo `CNAME`).

## Identidad

| Color | Hex | Uso |
|---|---|---|
| Ocean Blue | `#0D223A` | Marca, titulares, cabeceras y pie |
| Slate Grey | `#4B5B72` | Texto secundario |
| Cyan Teal | `#009FA1` | Acentos (en botones se usa `#007A7C` para que el texto blanco sea legible) |
| Pure White | `#FFFFFF` | Fondos |

Tipografías: Montserrat (texto y titulares) y Yellowtail (acento manuscrito, como «Canary» en el logotipo).

## Cómo editar

Las páginas se generan; no se editan a mano.

- `_fuente/datos.py` — datos de la empresa (correo, teléfono, zona, URL de pagos), planes y precios, pasos, soluciones, preguntas frecuentes e historia, en ES/EN.
- `_fuente/datos_casos.py` — industrias, historias de éxito y programa de afiliados (niveles, pasos y preguntas), en ES/EN.
- `_fuente/config.py` — ID de Google Tag Manager (`GTM_ID`) y función de Biscotti CMP que reabre las preferencias de cookies (`BISCOTTI_REABRIR`).
- `_fuente/partials/` — piezas comunes de todas las páginas:
  - `head.html` — `<head>` completo, con Biscotti CMP y Google Tag Manager.
  - `cabecera.html` — `<noscript>` de GTM, barra superior y menú.
  - `pie.html` — pie de página, botón «volver arriba» y `site.js`.
  - `formulario.html`, `campos-contacto.html`, `campos-afiliado.html` — formulario que va antes del pie.

  Marcas: `{{ variable }}` (valor del generador), `{{ ico:nombre }}` (icono) y `{{ t: español || english }}` (texto según idioma).
- `_fuente/generar.py` — compone cada página: rellena los partials y genera el contenido propio de cada una.

```
python3 _fuente/generar.py    # regenera todas las páginas
```

## Consentimiento y etiquetado

Cada página carga primero el banner de Biscotti CMP y justo después Google Tag Manager (script en `<head>` y `<noscript>` tras `<body>`). No hay ningún otro script de seguimiento: todo se configura dentro del contenedor de GTM. El enlace «Preferencias de cookies» del pie reabre el panel de Biscotti.

## Pendiente

- Teléfono definitivo (la web original muestra `+34 000 000 000`).
- Titular, NIF y domicilio en el aviso legal y la política de privacidad (marcados como «pendiente de completar»).
