#!/usr/bin/env python3
"""Generador estático del sitio de la Dirección de Planeación / Portal SIE (UAdeC).

Uso:  python3 build.py        (desde la carpeta fuente/)
Produce los archivos .html en ../sitio/. No requiere dependencias.
Edita SITE_URL antes de publicar.
"""
import json, os, html, datetime

OUT = os.environ.get('OUT', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sitio'))
SITE_URL = os.environ.get('SITE_URL', 'https://planeacion.uadec.mx')  # <-- CAMBIAR al dominio real
VER = '20261107'
SIZES = json.load(open(os.path.join(os.path.dirname(__file__), 'sizes.json')))
TODAY = '7 de noviembre de 2026'

CONTACT = {
    'email': 'planeacion@uadec.edu.mx',
    'tels': ['844 438 1766', '844 438 1626', '844 438 1627'],
    'addr': ['M. Hidalgo y José Cárdenas Valdés', 'Col. República Oriente, C.P. 25280', 'Saltillo, Coahuila'],
    'hours': 'Lunes a viernes, 8:00 a 15:00 h',
    'facebook': 'https://www.facebook.com/profile.php?id=100064146907208',
    'maps': 'https://www.google.com/maps/search/?api=1&query=Direcci%C3%B3n+de+Planeaci%C3%B3n+UAdeC+Saltillo',
}

CSP = ("default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; "
       "connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self' mailto:; manifest-src 'self'")

e = html.escape


def ic(name, cls='icon', B=''):
    return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="{B}assets/img/icons.svg#i-{name}"></use></svg>'


def img(name, alt, B='', cls='', lazy=True, ext='webp', sizes_attr=None, srcset=None, priority=False):
    w, h = SIZES[name]
    attrs = [f'src="{B}assets/img/{name}.{ext}"', f'width="{w}"', f'height="{h}"', f'alt="{e(alt)}"']
    if srcset: attrs.append(f'srcset="{srcset}"')
    if sizes_attr: attrs.append(f'sizes="{sizes_attr}"')
    if cls: attrs.append(f'class="{cls}"')
    if priority: attrs.append('fetchpriority="high"')
    elif lazy: attrs.append('loading="lazy"')
    attrs.append('decoding="async"')
    return '<img ' + ' '.join(attrs) + '>'


SIE_MENU = [
    ('sie.html', '¿Qué es el SIE?', 'database'),
    ('numeralia.html', 'Numeralia', 'list-ordered'),
    ('indicadores.html', 'Indicadores básicos', 'chart-no-axes-combined'),
    ('documentos.html', 'Documentos e informes', 'file-text'),
    ('auditorias.html', 'Auditorías de matrícula 911', 'clipboard-check'),
    ('cubos.html', 'Modelos (cubos OLAP)', 'box'),
]


def header(active, B=''):
    def cur(slug):
        return ' aria-current="page"' if slug == active else ''
    sie_active = active in [m[0] for m in SIE_MENU]
    sub = ''.join(f'<li><a href="{B}{u}"{cur(u)}>{ic(i, B=B)}<span>{t}</span></a></li>' for u, t, i in SIE_MENU)
    return f'''<a class="skip-link" href="#contenido">Saltar al contenido</a>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="{B}index.html">
      <img src="{B}assets/img/escudo-uadec.webp" width="{SIZES['escudo-uadec'][0]}" height="{SIZES['escudo-uadec'][1]}" alt="">
      <span class="brand-uni">Universidad<br>Autónoma<br>de Coahuila</span>
      <span class="brand-dep">Dirección de<strong>Planeación</strong></span>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="main-nav" aria-label="Abrir menú de navegación">
      {ic('menu', 'i-open', B)}{ic('x', 'i-close', B)}
    </button>
    <nav id="main-nav" class="main-nav" aria-label="Principal">
      <ul class="nav-list">
        <li><a class="nav-link" href="{B}index.html"{cur('index.html')}>Inicio</a></li>
        <li><a class="nav-link" href="{B}somos-uadec.html"{cur('somos-uadec.html')}>Somos UAdeC</a></li>
        <li class="has-sub"><button class="nav-link{' is-active' if sie_active else ''}" type="button" aria-expanded="false" aria-controls="sub-sie">Portal SIE{ic('chevron-down', B=B)}</button>
          <ul class="subnav" id="sub-sie">{sub}</ul>
        </li>
        <li><a class="nav-link" href="{B}contacto.html"{cur('contacto.html')}>Contacto</a></li>
      </ul>
      <div class="nav-cta"><a class="btn btn--primary" href="{B}numeralia.html">Consultar cifras {ic('arrow-right', B=B)}</a></div>
    </nav>
  </div>
</header>'''


def footer(B=''):
    tels = '<br>'.join(f'<a href="tel:+52{t.replace(" ", "")}">{t}</a>' for t in CONTACT['tels'])
    sie = ''.join(f'<li><a href="{B}{u}">{t}</a></li>' for u, t, _ in SIE_MENU[1:])
    return f'''<footer class="site-footer">
  <div class="container footer-top">
    <div>
      <div class="footer-brand">
        <img src="{B}assets/img/escudo-uadec-blanco.webp" width="{SIZES['escudo-uadec-blanco'][0]}" height="{SIZES['escudo-uadec-blanco'][1]}" alt="" loading="lazy">
        <span>Dirección de Planeación<small>Universidad Autónoma de Coahuila</small></span>
      </div>
      <p>Área responsable de dirigir y coordinar los procesos de planeación estratégica, evaluación y seguimiento que fortalecen el desarrollo institucional.</p>
      <div class="social">
        <a href="{CONTACT['facebook']}" target="_blank" rel="noopener noreferrer" aria-label="Facebook de la Dirección de Planeación (se abre en otra pestaña)">{ic('facebook', B=B)}</a>
        <a href="mailto:{CONTACT['email']}" aria-label="Enviar correo a la Dirección de Planeación">{ic('mail', B=B)}</a>
      </div>
    </div>
    <div>
      <h2>Enlaces rápidos</h2>
      <ul>
        <li><a href="{B}index.html">Inicio</a></li>
        <li><a href="{B}somos-uadec.html">Somos UAdeC</a></li>
        <li><a href="{B}sie.html">Portal SIE</a></li>
        <li><a href="{B}contacto.html">Contacto</a></li>
        <li><a href="{B}aviso-de-privacidad.html">Aviso de privacidad</a></li>
      </ul>
    </div>
    <div>
      <h2>Información estadística</h2>
      <ul>{sie}</ul>
    </div>
    <div>
      <h2>Contacto</h2>
      <ul class="footer-contact">
        <li>{ic('map-pin', B=B)}<span>{'<br>'.join(CONTACT['addr'])}<br><a href="{CONTACT['maps']}" target="_blank" rel="noopener noreferrer">Cómo llegar</a></span></li>
        <li>{ic('phone', B=B)}<span>{tels}</span></li>
        <li>{ic('mail', B=B)}<a href="mailto:{CONTACT['email']}">{CONTACT['email']}</a></li>
        <li>{ic('clock', B=B)}<span>{CONTACT['hours']}</span></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="container">
      <span>© <span data-year>2026</span> Universidad Autónoma de Coahuila. Todos los derechos reservados.</span>
      <div class="footer-links">
        <a href="{B}aviso-de-privacidad.html">Aviso de privacidad</a>
        <button type="button" data-open-cookies>Preferencias de cookies</button>
        <a href="{B}sitemap.xml">Mapa del sitio</a>
      </div>
    </div>
  </div>
</footer>
<div class="cookie-banner" id="cookie-banner" role="region" aria-label="Aviso de cookies" hidden>
  <h2>{ic('cookie', B=B)}Tu privacidad importa</h2>
  <p>Este sitio <strong>no usa cookies de rastreo ni publicidad</strong>. Solo guardamos en tu navegador tu elección sobre este aviso. Si en el futuro activamos estadísticas de visitas, solo se cargarán con tu permiso. Consulta nuestra <a href="{B}aviso-de-privacidad.html#cookies">política de cookies</a>.</p>
  <div class="cookie-prefs" id="cookie-prefs" hidden>
    <div class="pref"><div><strong>Necesarias</strong><span>Recuerdan tu elección de privacidad. Siempre activas.</span></div><label class="switch"><input type="checkbox" checked disabled aria-label="Almacenamiento necesario (siempre activo)"><i></i></label></div>
    <div class="pref"><div><strong>Estadísticas</strong><span>Medición anónima de visitas para mejorar el sitio. Actualmente no hay ningún servicio activo.</span></div><label class="switch"><input type="checkbox" id="pref-analytics" aria-label="Permitir estadísticas anónimas"><i></i></label></div>
  </div>
  <div class="cookie-actions">
    <button class="btn btn--primary" type="button" data-cookie="accept">Aceptar</button>
    <button class="btn btn--ghost" type="button" data-cookie="reject">Solo necesarias</button>
    <button class="btn btn--ghost" type="button" data-cookie="config">Configurar</button>
    <button class="btn btn--primary" type="button" data-cookie="save" hidden>Guardar preferencias</button>
  </div>
</div>
<button class="to-top" type="button" aria-label="Volver arriba">{ic('arrow-up', B=B)}</button>'''


def page(slug, title, desc, body, active=None, B='', noindex=False, jsonld=None, preload_img=None):
    full_title = title if 'UAdeC' in title else f'{title} | Dirección de Planeación UAdeC'
    url = SITE_URL + '/' + ('' if slug == 'index.html' else slug)
    pre = ''
    if preload_img:
        pre = f'\n<link rel="preload" as="image" href="{B}{preload_img[0]}" imagesrcset="{preload_img[1]}" imagesizes="{preload_img[2]}" fetchpriority="high">'
    ld = f'\n<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ''
    robots = 'noindex, follow' if noindex else 'index, follow, max-image-preview:large'
    canon = '' if noindex else f'\n<link rel="canonical" href="{url}">'
    return f'''<!DOCTYPE html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{CSP}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{e(full_title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">{canon}
<meta name="theme-color" content="#062a7a">
<meta name="author" content="Dirección de Planeación, Universidad Autónoma de Coahuila">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_MX">
<meta property="og:site_name" content="Dirección de Planeación UAdeC">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/assets/img/og-planeacion.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Edificio de la Dirección de Planeación de la UAdeC">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{B}favicon.ico" sizes="32x32">
<link rel="icon" type="image/png" sizes="192x192" href="{B}assets/img/icon-192.png">
<link rel="apple-touch-icon" href="{B}assets/img/icon-180.png">
<link rel="manifest" href="{B}site.webmanifest">
<link rel="preload" href="{B}assets/fonts/poppins-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{B}assets/fonts/poppins-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>{pre}
<link rel="stylesheet" href="{B}assets/css/main.css?v={VER}">
<script src="{B}assets/js/boot.js?v={VER}"></script>
<script src="{B}assets/js/main.js?v={VER}" defer></script>{ld}
</head>
<body data-icons="{B}assets/img/icons.svg">
{header(active, B)}
<main id="contenido" tabindex="-1">
{body}
</main>
{footer(B)}
</body>
</html>
'''


def page_hero(eyebrow, title, lead, crumbs, B=''):
    items = [f'<li><a href="{B}index.html">Inicio</a></li>'] + [
        (f'<li><a href="{B}{u}">{t}</a></li>' if u else f'<li aria-current="page">{t}</li>') for t, u in crumbs]
    return f'''<section class="page-hero">
  <div class="container hero-anim">
    <nav aria-label="Ruta de navegación"><ol class="breadcrumb">{''.join(items)}</ol></nav>
    <h1>{title}</h1>
    <p>{lead}</p>
  </div>
</section>'''


def figure(name, caption, B='', wide=False):
    return f'''<figure class="figure{' figure--wide' if wide else ''} reveal">
  <button type="button" data-lightbox="{B}assets/img/{name}.webp" data-caption="{e(caption)}">{img(name, caption, B)}<span class="sr-only"> (ampliar imagen)</span></button>
  <figcaption>{caption}</figcaption>
</figure>'''


def card(icon, title, text, href=None, foot=None, delay=0):
    d = f' reveal-d{delay}' if delay else ''
    inner = f'<span class="card-icon">{ic(icon)}</span><h3>{title}</h3><p>{text}</p>'
    if href:
        inner += f'<span class="card-foot">{foot or "Ver más"} {ic("arrow-right")}</span>'
        return f'<a class="card reveal{d}" href="{href}">{inner}</a>'
    return f'<div class="card card--hover reveal{d}">{inner}</div>'


def n(x):
    return f'{x:,}'


def kpi(value, label, gold=False, count=True):
    v = f'<strong data-count="{value}">{n(value)}</strong>' if count and isinstance(value, int) else f'<strong>{value}</strong>'
    return f'<div class="kpi{" kpi--gold" if gold else ""}">{v}<span>{label}</span></div>'


# ======================================================================
# INICIO
# ======================================================================
def build_index():
    B = ''
    hero_srcset = 'assets/img/edificio-planeacion-800.webp 800w, assets/img/edificio-planeacion-1400.webp 1400w'
    hero_sizes = '(min-width: 960px) 50vw, 100vw'
    areas = [
        ('landmark', 'Subdirección de Fortalecimiento Institucional', 'Impulsamos estrategias y proyectos para fortalecer la capacidad institucional.'),
        ('file-chart-column', 'Subdirección de Planeación Financiera', 'Administramos y planificamos los recursos financieros de manera eficiente.'),
        ('award', 'Subdirección de Evaluación, Acreditación y Certificación', 'Promovemos la evaluación institucional y la mejora continua.'),
    ]
    cards = ''.join(card(i, t, d, delay=k) for k, (i, t, d) in enumerate(areas))
    cards += card('monitor-cog', 'Sistema de Información Estadística (SIE)', 'Información estadística para el análisis y la toma de decisiones.', 'sie.html', 'Ir al Portal SIE', 3)

    quick = [
        ('list-ordered', 'Numeralia', 'Cifras clave por ciclo escolar: estudiantes, programas y personal académico.', 'numeralia.html'),
        ('chart-no-axes-combined', 'Indicadores básicos', 'Aspirantes, demanda por carrera y evolución de la planta docente.', 'indicadores.html'),
        ('file-text', 'Documentos e informes', 'Cuadernillos de indicadores e informes de actividades.', 'documentos.html'),
        ('clipboard-check', 'Auditorías 911', 'Resultados de la auditoría de matrícula por ciclo escolar.', 'auditorias.html'),
        ('box', 'Modelos (cubos)', 'Consultas dinámicas para áreas autorizadas.', 'cubos.html'),
        ('map', 'Somos UAdeC', 'Coahuila y la presencia regional de la Universidad.', 'somos-uadec.html'),
    ]
    qcards = ''.join(card(i, t, d, u, 'Consultar', k % 3) for k, (i, t, d, u) in enumerate(quick))

    body = f'''<section class="hero">
  <div class="container hero-grid">
    <div class="hero-anim">
      <span class="eyebrow">Dirección de Planeación</span>
      <h1>Planeamos el presente, <span>construimos el futuro</span></h1>
      <p>Impulsamos el desarrollo institucional mediante la planeación estratégica, la evaluación y el seguimiento de los proyectos que fortalecen a nuestra universidad.</p>
      <div class="hero-actions">
        <a class="btn btn--primary" href="#areas">Conoce nuestras áreas {ic('arrow-right')}</a>
        <a class="link-arrow" href="sie.html">Explora el Portal SIE {ic('arrow-up-right')}</a>
      </div>
    </div>
    <div class="hero-media">
      <picture>{img('edificio-planeacion-1400', 'Edificio de la Dirección de Planeación de la Universidad Autónoma de Coahuila', srcset=hero_srcset, sizes_attr=hero_sizes, priority=True)}</picture>
      <div class="hero-badge">{ic('target')}<span><strong>Planeación estratégica</strong>evaluación y seguimiento</span></div>
    </div>
  </div>
</section>

<section class="section" id="areas">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">¿Qué hacemos?</span>
      <h2>Nuestras áreas de trabajo</h2>
      <p>Coordinamos los procesos que permiten a la Universidad planear, medir y mejorar.</p>
    </div>
    <div class="grid-4">{cards}</div>
  </div>
</section>

<section class="section stats" aria-labelledby="stats-title">
  <div class="container stats-grid">
    <div class="reveal">
      <span class="eyebrow">La UAdeC en cifras</span>
      <h2 id="stats-title">Trabajamos por una universidad en constante <span>crecimiento</span></h2>
      <p>A través de la planeación y el trabajo colaborativo fortalecemos el presente para asegurar un mejor futuro para nuestra comunidad universitaria.</p>
      <a class="btn btn--gold" href="numeralia.html">Ver numeralia {ic('arrow-right')}</a>
    </div>
    <div class="stat-list">
      <div class="stat reveal reveal-d1">{ic('building-2')}<span class="stat-num" data-count="3">3</span><span class="stat-label">Unidades regionales</span></div>
      <div class="stat reveal reveal-d2">{ic('graduation-cap')}<span class="stat-num" data-count="60" data-suffix="+">60+</span><span class="stat-label">Escuelas, facultades e institutos</span></div>
      <div class="stat reveal reveal-d3">{ic('users')}<span class="stat-num" data-count="41534">41,534</span><span class="stat-label">Estudiantes</span><span class="stat-note">Ciclo 2025-2 (enero–junio 2026)</span></div>
      <div class="stat reveal reveal-d4">{ic('book-open-text')}<span class="stat-num" data-count="65" data-suffix="+">65+</span><span class="stat-label">Años de historia y compromiso</span></div>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Portal SIE</span>
      <h2>Información estadística a un clic</h2>
      <p>Consulta la información institucional que publica el Sistema de Información Estadística.</p>
    </div>
    <div class="grid-3">{qcards}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="cta reveal">
      <div class="cta-body">
        <span class="eyebrow">¿Necesitas información?</span>
        <h2>Solicita datos estadísticos o asesoría</h2>
        <p>Escuelas, facultades y dependencias pueden solicitar información sobre matrícula, indicadores y modelos estadísticos.</p>
        <div class="hero-actions">
          <a class="btn btn--gold" href="contacto.html">Contáctanos {ic('arrow-right')}</a>
          <a class="btn btn--light" href="tel:+528444381766">{ic('phone')} 844 438 1766</a>
        </div>
      </div>
      <div class="cta-media"><picture>{img('letrero-planeacion-900', 'Letrero de la Dirección de Planeación en la fachada del edificio', srcset='assets/img/letrero-planeacion-600.webp 600w, assets/img/letrero-planeacion-900.webp 900w', sizes_attr='(min-width: 900px) 45vw, 100vw')}</picture></div>
    </div>
  </div>
</section>'''
    ld = {
        '@context': 'https://schema.org', '@type': 'Organization',
        'name': 'Dirección de Planeación, Universidad Autónoma de Coahuila',
        'url': SITE_URL + '/', 'logo': SITE_URL + '/assets/img/escudo-uadec.png', 'email': CONTACT['email'],
        'telephone': '+52 844 438 1766',
        'address': {'@type': 'PostalAddress', 'streetAddress': CONTACT['addr'][0], 'addressLocality': 'Saltillo',
                    'addressRegion': 'Coahuila', 'postalCode': '25280', 'addressCountry': 'MX'},
        'parentOrganization': {'@type': 'CollegeOrUniversity', 'name': 'Universidad Autónoma de Coahuila'},
        'sameAs': [CONTACT['facebook']]}
    return page('index.html', 'Dirección de Planeación | Universidad Autónoma de Coahuila (UAdeC)',
                'Dirección de Planeación de la UAdeC: planeación estratégica, evaluación institucional y el Sistema de Información Estadística (SIE) con numeralia, indicadores y documentos.',
                body, 'index.html', jsonld=ld,
                preload_img=('assets/img/edificio-planeacion-1400.webp', hero_srcset, hero_sizes))


# ======================================================================
# ¿QUÉ ES EL SIE?
# ======================================================================
def build_sie():
    body = page_hero('Portal SIE', '¿Qué es el SIE?', 'El Sistema de Información Estadística reúne los datos de los sistemas administrativos de la Universidad y los convierte en información clara para la planeación y la toma de decisiones.', [('Portal SIE', None)]) + f'''
<section class="section">
  <div class="container split">
    <div class="prose reveal">
      <span class="eyebrow">Portal de Estadística Universitaria</span>
      <h2>Información útil, al instante</h2>
      <p>El SIE es un sistema informático de apoyo cuya finalidad principal es que las personas usuarias cuenten de forma inmediata con información relevante, con la posibilidad de analizarla a detalle para apoyar la toma de decisiones.</p>
      <p>Su propósito es acceder a los datos de los sistemas institucionales, crear información útil y presentar los resultados de forma clara. Ofrece información estadística en línea orientada a:</p>
      <ul class="check-list">
        <li>{ic('check')}<span>Numeralia universitaria por ciclo escolar.</span></li>
        <li>{ic('check')}<span>Series históricas de estadística básica.</span></li>
        <li>{ic('check')}<span>Indicadores institucionales.</span></li>
        <li>{ic('check')}<span>Consultas dinámicas a los acervos de datos estadísticos (modelos o cubos).</span></li>
      </ul>
    </div>
    <div class="reveal reveal-d2">
      <div class="callout callout--gold">{ic('info')}<p>La estadística recopila e interpreta los datos que se manejan en los sistemas administrativos de la Universidad y aporta instrumentos de apoyo para la toma de decisiones de escuelas, facultades y dependencias.</p></div>
      <div class="kpis" style-free>
        {kpi(15, 'Documentos de auditoría 911 publicados')}
        {kpi(5, 'Ciclos con numeralia')}
        {kpi(3, 'Cuadernillos de indicadores')}
      </div>
    </div>
  </div>
</section>
<section class="section section--tint">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">Secciones</span><h2>¿Qué puedes consultar?</h2></div>
    <div class="grid-3">
      {card('list-ordered', 'Numeralia', 'Resúmenes con cifras significativas de la UAdeC por ciclo escolar.', 'numeralia.html', 'Ver numeralia')}
      {card('chart-no-axes-combined', 'Indicadores básicos', 'Competitividad académica (aspirantes y demanda) y capacidad académica (planta docente).', 'indicadores.html', 'Ver indicadores', 1)}
      {card('file-text', 'Documentos', 'Cuadernillos de indicadores e informes de actividades del Rector.', 'documentos.html', 'Ver documentos', 2)}
      {card('clipboard-check', 'Auditorías 911', 'Documentos de la auditoría de matrícula del Cuestionario Estadístico 911.', 'auditorias.html', 'Ver auditorías')}
      {card('box', 'Modelos (cubos)', 'Análisis multidimensional de aspirantes, matrícula, títulos y eficiencia terminal.', 'cubos.html', 'Conocer los modelos', 1)}
      {card('mail', 'Contacto SIE', 'Solicita información, acceso a modelos o reporta un problema.', 'contacto.html', 'Escribirnos', 2)}
    </div>
  </div>
</section>'''
    body = body.replace(' style-free', '')
    return page('sie.html', 'Portal SIE: Sistema de Información Estadística', 'Qué es el Sistema de Información Estadística (SIE) de la UAdeC: numeralia, indicadores, documentos, auditorías de matrícula 911 y modelos de consulta.', body, 'sie.html')


# ======================================================================
# SOMOS UADEC
# ======================================================================
def build_somos():
    secs = [
        ('coahuila', 'Mapa de México con el estado de Coahuila resaltado', 'El estado', 'Coahuila de Zaragoza',
         '<p>Se localiza en el noreste de México y colinda al norte con Texas (Estados Unidos), al sur con Zacatecas y San Luis Potosí, al este con Nuevo León y al oeste con Durango y Chihuahua.</p><p>Ocupa el <strong>3.er lugar nacional en extensión territorial</strong> (151,571 km²), el 7.7&nbsp;% de la superficie del país.</p>'),
        ('regiones', 'Mapa de Coahuila dividido en sus cinco regiones', 'Territorio', 'Regiones del estado',
         '<ul><li><strong>Fronteriza:</strong> Acuña, Allende, Guerrero, Jiménez, Morelos, Nava, Piedras Negras, Zaragoza y Villa Unión.</li><li><strong>Centro:</strong> Abasolo, Candela, Castaños, Cuatro Ciénegas, Escobedo, Frontera, Lamadrid, Monclova, Nadadores, Ocampo, Sacramento, San Buenaventura y Sierra Mojada.</li><li><strong>Carbonífera:</strong> Juárez, Múzquiz, Progreso, Sabinas y San Juan de Sabinas.</li><li><strong>Laguna:</strong> Francisco I. Madero, Matamoros, San Pedro, Torreón y Viesca.</li><li><strong>Sureste:</strong> Arteaga, General Cepeda, Parras, Ramos Arizpe y Saltillo.</li></ul>'),
        ('poblacion', 'Collage de sitios representativos de Coahuila', 'Población y economía', 'Un estado urbano e industrial',
         '<p>La población del estado representa el 2.4&nbsp;% de la nacional, con 2.75 millones de habitantes; la fuerza de trabajo equivale a poco menos de la mitad de la población total. Coahuila participa con el 3.1&nbsp;% del producto interno bruto del país y el 90&nbsp;% de su población vive en zonas urbanas.</p><p>El sector industrial pesa más que el promedio nacional, con una participación del 44&nbsp;%. El ingreso per cápita es de 126 mil pesos al año, 20&nbsp;% mayor que el nacional: la séptima entidad con el valor más alto.</p>'),
        ('industria', 'Collage de actividades industriales en Coahuila', 'Industria', 'Agrupamientos industriales',
         '<p>En la región Laguna se ubican las principales industrias textiles, agropecuarias y ligeras; en el sureste se concentra la industria automotriz, así como empresas químicas, textiles y metalúrgicas; en el centro se encuentra una de las siderúrgicas más grandes del país, y en el norte, con posición estratégica hacia Estados Unidos, se ubican empresas maquiladoras.</p>'),
        ('competitividad', 'Investigadora trabajando en un laboratorio', 'Competitividad', 'Entre los estados mejor calificados',
         '<p>Coahuila ocupa el cuarto lugar en competitividad global entre las entidades federativas y se encuentra entre los cinco estados con mejor calificación en desempeño económico.</p>'),
        ('educacion', 'Collage de estudiantes y docentes en actividades académicas', 'Educación', 'Cobertura y crecimiento',
         '<p>La cobertura de educación básica es prácticamente del 100&nbsp;%. La matrícula de educación media superior creció a un ritmo anual de 3.5&nbsp;% en los últimos cuatro periodos escolares, y la de educación superior, 4.9&nbsp;%.</p><p>De la educación superior egresan 13,300 personas por año; el 37.7&nbsp;% corresponde a ingeniería y tecnología, áreas clave para la vocación industrial del estado.</p>'),
        ('regiones-uadec', 'Organigrama de la Rectoría y las coordinaciones de unidad', 'La Universidad', 'Una institución de calidad internacional',
         '<p>La UAdeC es una institución de calidad internacional, socialmente responsable y comprometida con la sustentabilidad, cuyos estudiantes se distinguen por su formación académica, ética, cultural y deportiva; sus egresados conservan el sentido de pertenencia, son altamente competitivos y capaces de integrarse con éxito al entorno global.</p>'),
        ('unidades-uadec', 'Mapa de Coahuila con las unidades Saltillo, Torreón y Norte', 'Presencia regional', 'Presencia en 13 municipios',
         '<p>La Universidad Autónoma de Coahuila tiene presencia en <strong>13 municipios</strong>, con un impacto en el 86&nbsp;% de la población total del estado.</p>'),
        ('necesidad', 'Collage de estudiantes en actividades de vinculación', 'Pertinencia', 'Oferta educativa que responde',
         '<p>Responde a las necesidades cambiantes de los sectores productivo y social mediante una oferta educativa pertinente, innovadora y flexible, respaldada por docentes e investigadores con perfil idóneo, organizados en cuerpos académicos vinculados al desarrollo de la ciencia, la tecnología y las humanidades mediante redes nacionales e internacionales.</p>'),
        ('infraestructura', 'Collage de edificios e instalaciones universitarias', 'Gestión', 'Infraestructura y procesos',
         '<p>Su normativa, infraestructura y procesos de gestión respaldan de manera efectiva, eficiente y transparente las actividades sustantivas.</p>'),
    ]
    blocks = ''
    for k, (im, alt, eb, h, txt) in enumerate(secs):
        tint = ' section--tint' if k % 2 else ''
        rev = ' split--rev' if k % 2 else ''
        blocks += f'''<section class="section section--tight{tint}">
  <div class="container split{rev}">
    <div class="media-frame reveal"><button type="button" class="figure-btn" data-lightbox="assets/img/{im}.webp" data-caption="{e(alt)}">{img(im, alt, lazy=k > 0)}<span class="sr-only"> (ampliar imagen)</span></button></div>
    <div class="prose reveal reveal-d1"><span class="eyebrow">{eb}</span><h2>{h}</h2>{txt}</div>
  </div>
</section>'''
    body = page_hero('Somos UAdeC', 'Somos UAdeC', 'Conoce el contexto de Coahuila y la presencia de la Universidad Autónoma de Coahuila en el estado.', [('Somos UAdeC', None)]) + f'''
<div class="container"><div class="callout" role="note" style-free>{ic('info')}<p>Los datos de esta sección provienen de la información de referencia publicada por el Portal SIE (2015–2017).</p></div></div>
''' + blocks
    body = body.replace(' style-free', '').replace('<div class="container"><div class="callout"', '<div class="container section--tight"><div class="callout"')
    return page('somos-uadec.html', 'Somos UAdeC: Coahuila y la Universidad', 'Contexto geográfico, económico y educativo de Coahuila y la presencia regional de la Universidad Autónoma de Coahuila.', body, 'somos-uadec.html')


# ======================================================================
# NUMERALIA
# ======================================================================
CYCLES = [
    dict(id='ciclo-2017-1', tab='Ene–Jun 2017', ciclo='2016-2017', fac=44, planteles=14,
         centros=('4', '2 unidades académicas independientes y 2 centros dependientes de unidades académicas'),
         bach_detalle='12 escolarizados, 2 abiertos · 11 en el Sistema Nacional de Bachillerato',
         lic=85, lic_detalle=[('PE a distancia', 2), ('PE presenciales', 83), ('PE evaluables', 70), ('PE de calidad', 40)],
         pos=53, pos_detalle=[('Especialidades', 5), ('Maestrías', 41), ('Doctorados', 7)], pnpc=(21, 16, 5),
         units=[('Saltillo', 5705, 9457, 889), ('Torreón', 2667, 8897, 599), ('Norte', 2410, 3793, 165)],
         doc=(3097, 1025, 2072), ptc='De los <strong>829</strong> profesores de tiempo completo del nivel superior, el <strong>93.2&nbsp;%</strong> cuenta con estudios de posgrado.',
         prodep=326, sni=139, ca=(367, 54), map='distribucion-2017',
         charts=[('alumnos-2017-1', 'Estudiantes por nivel educativo'), ('docentes-2017-1', 'Profesores de tiempo completo y de tiempo parcial por nivel'),
                 ('grado-2017-1', 'Profesores de tiempo completo por grado académico'), ('ca-2017-1', 'Cuerpos académicos por grado de consolidación'),
                 ('pnpc-2017', 'Programas de posgrado en el PNPC por nivel')]),
    dict(id='ciclo-2016-2', tab='Ago–Dic 2016', ciclo='2016-2017', fac=44, planteles=14,
         centros=('4', '2 unidades académicas independientes y 2 centros dependientes de unidades académicas'),
         bach_detalle='12 escolarizados, 2 abiertos · 11 en el Sistema Nacional de Bachillerato',
         lic=84, lic_detalle=[('PE a distancia', 2), ('PE presenciales', 82), ('PE evaluables', 71), ('PE de calidad', 36)],
         pos=55, pos_detalle=[('Especialidades', 5), ('Maestrías', 43), ('Doctorados', 7)], pnpc=(22, 17, 5),
         units=[('Saltillo', 6093, 9600, 940), ('Torreón', 2854, 9161, 722), ('Norte', 2471, 4064, 179)],
         doc=(3126, 1032, 2094), ptc='De los <strong>829</strong> profesores de tiempo completo del nivel superior, el <strong>91.6&nbsp;%</strong> cuenta con estudios de posgrado.',
         prodep=333, sni=114, ca=(369, 54), map='distribucion-2017',
         charts=[('alumnos-2016-2', 'Estudiantes por nivel educativo'), ('docentes-2016-2', 'Profesores de tiempo completo y de tiempo parcial por nivel'),
                 ('ca-2016-2', 'Cuerpos académicos por grado de consolidación'), ('pnpc-2016-2', 'Programas de posgrado en el PNPC por nivel')]),
    dict(id='ciclo-2016-1', tab='Ene–Jun 2016', ciclo='2015-2016', fac=43, planteles=14,
         centros=('4', '2 unidades académicas independientes y 2 centros dependientes de unidades académicas'),
         bach_detalle='12 escolarizados, 2 abiertos · 10 en el Sistema Nacional de Bachillerato',
         lic=81, lic_detalle=[('PE a distancia', 3), ('PE presenciales', 78), ('PE evaluables', 67), ('PE de calidad', 60)],
         pos=56, pos_detalle=[('Especialidades', 5), ('Maestrías', 43), ('Doctorados', 8)], pnpc=(22, 17, 5),
         units=[('Saltillo', 5802, 9348, 958), ('Torreón', 2858, 8673, 851), ('Norte', 2591, 3721, 188)],
         doc=(3005, 1038, 1967), ptc='En el nivel medio superior, el <strong>66&nbsp;%</strong> de los <strong>211</strong> profesores de tiempo completo cuenta con posgrado. En licenciatura, de los <strong>827</strong> profesores de tiempo completo el <strong>90.2&nbsp;%</strong> cuenta con estudios de posgrado.',
         prodep=317, sni=115, ca=(288, 54), map='distribucion-2016',
         charts=[('alumnos-2016-1', 'Estudiantes por nivel educativo'), ('docentes-2016-1', 'Profesores de tiempo completo y de tiempo parcial por nivel'),
                 ('grado-ms-2016-1', 'Profesores de tiempo completo de nivel medio superior por grado académico'), ('grado-2016-1', 'Profesores de tiempo completo de nivel superior por grado académico'),
                 ('ca-2016-1', 'Cuerpos académicos por grado de consolidación'), ('pnpc-2016-1', 'Programas de posgrado en el PNPC por nivel')]),
    dict(id='ciclo-2015-2', tab='Ago–Dic 2015', ciclo='2015-2016', fac=43, planteles=14,
         centros=('2', 'Centro de Investigaciones Socioeconómicas y Centro de Estudios e Investigaciones Interdisciplinarias'),
         bach_detalle='Sistemas escolarizado y abierto',
         lic=81, lic_detalle=[('PE presenciales', 78), ('PE evaluables', 67), ('PE de calidad', 60)],
         pos=53, pos_detalle=[('Especialidades', 5), ('Maestrías', 40), ('Doctorados', 8)], pnpc=(23, 18, 5),
         units=[('Saltillo', 5860, 9526, 1040), ('Torreón', 2827, 9052, 967), ('Norte', 2543, 4067, 181)],
         doc=(3064, 996, 2068), ptc='De los <strong>791</strong> profesores de tiempo completo de licenciatura, el <strong>89.5&nbsp;%</strong> cuenta con estudios de posgrado.',
         prodep=320, sni=105, ca=(288, 54), map='distribucion-2015',
         charts=[('alumnos-2015-2', 'Estudiantes por nivel educativo'), ('docentes-2015-2', 'Profesores de tiempo completo y de tiempo parcial por nivel'),
                 ('grado-2015-2', 'Profesores de tiempo completo por grado académico'), ('ca-2015-2', 'Cuerpos académicos por grado de consolidación'),
                 ('pnpc-2015', 'Programas de posgrado en el PNPC por nivel'), ('proyeccion-competitividad-2016', 'Competitividad académica: junio 2015 y proyección a enero 2016')]),
    dict(id='ciclo-2015-1', tab='Ene–Jun 2015', ciclo='2014-2015', fac=43, planteles=14,
         centros=('2', 'Centro de Investigaciones Socioeconómicas y Centro de Estudios e Investigaciones Interdisciplinarias'),
         bach_detalle='Sistemas escolarizado y abierto',
         lic=81, lic_detalle=[('PE presenciales', 78), ('PE evaluables', 67), ('PE de calidad', 60)],
         pos=53, pos_detalle=[('Especialidades', 5), ('Maestrías', 40), ('Doctorados', 8)], pnpc=(23, 18, 5),
         units=[('Saltillo', 5347, 9279, 1149), ('Torreón', 2821, 8652, 972), ('Norte', 2416, 3877, 177)],
         doc=(3077, 1009, 2068), ptc='De los <strong>804</strong> profesores de tiempo completo de licenciatura, el <strong>88.8&nbsp;%</strong> cuenta con estudios de posgrado.',
         prodep=293, sni=108, ca=(282, 54), map='distribucion-2015',
         becas=dict(total=2243, items=[('Excelencia académica', 838), ('Apoyo académico', 960), ('Deportivas', 343), ('Artísticas', 60), ('Cívicas', 16)]),
         movilidad=(248, 189),
         charts=[('alumnos-2015-1', 'Estudiantes por nivel educativo'), ('docentes-2015-1', 'Profesores de tiempo completo y de tiempo parcial por nivel'),
                 ('grado-2015-1', 'Profesores de tiempo completo por grado académico'), ('pnpc-2015', 'Programas de posgrado en el PNPC por nivel'),
                 ('movilidad-2015', 'Distribución por área del conocimiento')]),
]


def cycle_panel(c, first):
    bach = sum(u[1] for u in c['units']); lic = sum(u[2] for u in c['units']); pos = sum(u[3] for u in c['units'])
    tot = bach + lic + pos
    rows = ''.join(f'<tr><th scope="row">{u[0]}</th><td>{n(u[1])}</td><td>{n(u[2])}</td><td>{n(u[3])}</td><td>{n(sum(u[1:]))}</td><td>{sum(u[1:]) / tot * 100:.1f}&nbsp;%</td></tr>' for u in c['units'])
    lvl = [('Bachillerato', bach, ''), ('Licenciatura', lic, ' bar-fill--gold'), ('Posgrado', pos, ' bar-fill--soft')]
    bars = ''.join(f'<div class="bar-row"><span>{l}</span><span class="bar-track"><span class="bar-fill{cl}" data-value="{v}" data-max="{tot}"></span></span><strong>{v / tot * 100:.1f}&nbsp;%</strong></div>' for l, v, cl in lvl)
    unit_bars = ''.join(f'<div class="bar-row"><span>{u[0]}</span><span class="bar-track"><span class="bar-fill" data-value="{sum(u[1:])}" data-max="{tot}"></span></span><strong>{n(sum(u[1:]))}</strong></div>' for u in c['units'])
    doc_t, tc, tp = c['doc']
    lic_d = ''.join(kpi(v, l) for l, v in c['lic_detalle'])
    pos_d = ''.join(kpi(v, l) for l, v in c['pos_detalle'])
    gallery = ''.join(figure(nm, cap) for nm, cap in c['charts'])
    extra = ''
    if c.get('becas'):
        b = c['becas']
        bb = ''.join(f'<div class="bar-row"><span>{l}</span><span class="bar-track"><span class="bar-fill bar-fill--gold" data-value="{v}" data-max="{max(x[1] for x in b["items"])}"></span></span><strong>{n(v)}</strong></div>' for l, v in b['items'])
        extra = f'''<div class="panel-block">
  <h3 class="panel-title">{ic('award')}Becas y movilidad</h3>
  <div class="grid-2">
    <div><div class="kpis">{kpi(b['total'], 'Becas a estudiantes', True)}</div><div class="bars" style-free>{bb}</div></div>
    <div class="kpis">{kpi(c['movilidad'][0], 'Becas de movilidad estudiantil nacional (2014-2015)')}{kpi(c['movilidad'][1], 'Becas de movilidad estudiantil internacional')}</div>
  </div>
</div>'''
    note = ''
    if c['id'] == 'ciclo-2015-2':
        note = '<p class="table-note">El total de bachillerato (11,230) corresponde a la suma por unidad y a la cifra publicada en el resumen del ciclo.</p>'
    if c['id'] == 'ciclo-2016-2':
        note = '<p class="table-note">Posgrado: 1,841 estudiantes según la suma por unidad regional publicada en la tabla del ciclo.</p>'
    hidden = '' if first else ' hidden'
    return f'''<div class="tab-panel" role="tabpanel" id="{c['id']}" aria-labelledby="tab-{c['id']}" tabindex="0"{hidden}>
  <h2 class="sr-only">Numeralia del ciclo {c['tab']} ({c['ciclo']})</h2>
  <div class="kpis">
    {kpi(tot, 'Estudiantes', True)}{kpi(doc_t, 'Docentes')}{kpi(c['lic'], 'Programas de licenciatura')}{kpi(c['pos'], 'Programas de posgrado')}{kpi(c['fac'], 'Facultades y escuelas de educación superior')}
  </div>

  <div class="panel-block">
    <h3 class="panel-title">{ic('users')}Estudiantes por unidad regional</h3>
    <div class="table-wrap">
      <table>
        <caption>Matrícula por unidad y nivel educativo, ciclo {c['tab']}</caption>
        <thead><tr><th scope="col">Unidad</th><th scope="col">Bachillerato</th><th scope="col">Licenciatura</th><th scope="col">Posgrado</th><th scope="col">Total</th><th scope="col">%</th></tr></thead>
        <tbody>{rows}</tbody>
        <tfoot><tr><th scope="row">UAdeC</th><td>{n(bach)}</td><td>{n(lic)}</td><td>{n(pos)}</td><td>{n(tot)}</td><td>100&nbsp;%</td></tr></tfoot>
      </table>
    </div>{note}
    <div class="grid-2 panel-block">
      <div><h4>Por nivel educativo</h4><div class="bars">{bars}</div></div>
      <div><h4>Por unidad regional</h4><div class="bars">{unit_bars}</div></div>
    </div>
  </div>

  <div class="panel-block">
    <h3 class="panel-title">{ic('school')}Unidades académicas</h3>
    <div class="kpis">
      {kpi(c['fac'], 'Facultades y/o escuelas de educación superior')}
      {kpi(c['planteles'], 'Planteles de bachillerato (' + c['bach_detalle'] + ')')}
      {kpi(c['centros'][0], 'Centros de investigación: ' + c['centros'][1], count=False)}
    </div>
  </div>

  <div class="panel-block">
    <h3 class="panel-title">{ic('graduation-cap')}Programas educativos</h3>
    <h4>Licenciatura: {c['lic']} programas</h4>
    <div class="kpis">{lic_d}</div>
    <h4 class="panel-block">Posgrado: {c['pos']} programas</h4>
    <div class="kpis">{pos_d}{kpi(c['pnpc'][0], f"Posgrados en el PNPC ({c['pnpc'][1]} maestrías y {c['pnpc'][2]} doctorados)", True)}</div>
  </div>

  <div class="panel-block">
    <h3 class="panel-title">{ic('users-round')}Personal académico</h3>
    <div class="grid-2">
      <div>
        <div class="bars">
          <div class="bar-row"><span>Tiempo completo</span><span class="bar-track"><span class="bar-fill" data-value="{tc}" data-max="{doc_t}"></span></span><strong>{n(tc)}</strong></div>
          <div class="bar-row"><span>Tiempo parcial</span><span class="bar-track"><span class="bar-fill bar-fill--gold" data-value="{tp}" data-max="{doc_t}"></span></span><strong>{n(tp)}</strong></div>
        </div>
        <div class="callout panel-block">{ic('graduation-cap')}<p>{c['ptc']}</p></div>
      </div>
      <div class="kpis">
        {kpi(c['prodep'], 'Profesores con perfil deseable PRODEP')}
        {kpi(c['sni'], 'Profesores en el Sistema Nacional de Investigadores')}
        {kpi(c['ca'][0], f"Profesores en {c['ca'][1]} cuerpos académicos reconocidos ante PRODEP")}
      </div>
    </div>
  </div>
  {extra}
  <div class="panel-block">
    <h3 class="panel-title">{ic('map')}Distribución geográfica</h3>
    {figure(c['map'], 'Distribución de las unidades académicas de la UAdeC en Coahuila', wide=True)}
  </div>

  <div class="panel-block">
    <h3 class="panel-title">{ic('chart-pie')}Gráficas del ciclo</h3>
    <div class="gallery">{gallery}</div>
  </div>
</div>'''


def build_numeralia():
    tabs = ''.join(f'<button class="tab" role="tab" id="tab-{c["id"]}" aria-controls="{c["id"]}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}" type="button">{c["tab"]}<small>Ciclo {c["ciclo"]}</small></button>' for i, c in enumerate(CYCLES))
    panels = ''.join(cycle_panel(c, i == 0) for i, c in enumerate(CYCLES))
    body = page_hero('Portal SIE', 'Numeralia', 'Resúmenes con información estadística y cifras significativas de la UAdeC por ciclo escolar.', [('Portal SIE', 'sie.html'), ('Numeralia', None)]) + f'''
<section class="section">
  <div class="container">
    <div class="callout callout--gold reveal">{ic('info')}<p>La actualización de los datos de la numeralia, de acuerdo con el ciclo, está sujeta a la revisión y aprobación de la Dirección de Planeación. Selecciona un ciclo para ver sus cifras.</p></div>
    <div class="panel-block">
      <div class="tabs" role="tablist" aria-label="Ciclos escolares">{tabs}</div>
      {panels}
    </div>
  </div>
</section>'''
    body = body.replace(' style-free', '')
    return page('numeralia.html', 'Numeralia: la UAdeC en números', 'Cifras de la Universidad Autónoma de Coahuila por ciclo escolar: estudiantes por unidad, programas educativos, personal académico, becas y cuerpos académicos.', body, 'numeralia.html')


# ======================================================================
# INDICADORES
# ======================================================================
def build_indicadores():
    asp = [('Bachillerato', 4583, 3249, 4406, 3143), ('Licenciatura', 7720, 5445, 7931, 5750)]
    rows = ''.join(f'<tr><th scope="row">{a[0]}</th><td>{n(a[1])}</td><td>{n(a[2])}</td><td>{n(a[1] + a[2])}</td><td>{n(a[3])}</td><td>{n(a[4])}</td><td>{n(a[3] + a[4])}</td></tr>' for a in asp)
    t = [sum(a[i] for a in asp) for i in range(1, 5)]
    body = page_hero('Portal SIE', 'Indicadores básicos', 'Indicadores de competitividad académica (aspirantes y demanda) y de capacidad académica (planta docente).', [('Portal SIE', 'sie.html'), ('Indicadores básicos', None)]) + f'''
<section class="section">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">Competitividad académica</span><h2>Aspirantes a la UAdeC</h2><p>Aspirantes por nivel educativo y sexo en los periodos de admisión 2014-1 y 2015-1.</p></div>
    <div class="kpis reveal">
      {kpi(t[0] + t[1], 'Aspirantes en el periodo 2014-1')}{kpi(t[2] + t[3], 'Aspirantes en el periodo 2015-1', True)}{kpi(t[2], 'Mujeres aspirantes 2015-1')}{kpi(t[3], 'Hombres aspirantes 2015-1')}
    </div>
    <div class="table-wrap panel-block reveal">
      <table>
        <caption>Aspirantes por nivel educativo y sexo</caption>
        <thead><tr><th scope="col" rowspan="2">Nivel</th><th scope="colgroup" colspan="3">2014-1</th><th scope="colgroup" colspan="3">2015-1</th></tr>
        <tr><th scope="col">Mujeres</th><th scope="col">Hombres</th><th scope="col">Total</th><th scope="col">Mujeres</th><th scope="col">Hombres</th><th scope="col">Total</th></tr></thead>
        <tbody>{rows}</tbody>
        <tfoot><tr><th scope="row">Total</th><td>{n(t[0])}</td><td>{n(t[1])}</td><td>{n(t[0] + t[1])}</td><td>{n(t[2])}</td><td>{n(t[3])}</td><td>{n(t[2] + t[3])}</td></tr></tfoot>
      </table>
    </div>
    <div class="gallery panel-block">
      {figure('aspirantes-grafica', 'Aspirantes a la UAdeC por sexo y nivel, 2014-1 y 2015-1')}
      {figure('aspirantes-demanda-unidad', 'Carreras con mayor demanda de aspirantes')}
      {figure('aspirantes-demanda-general', 'Carreras con mayor demanda: comparativo general')}
    </div>
  </div>
</section>
<section class="section section--tint">
  <div class="container split">
    <div class="prose reveal"><span class="eyebrow">Capacidad académica</span><h2>Distribución de la planta docente</h2><p>Profesores de tiempo completo y de tiempo parcial por nivel educativo. La información detallada por ciclo se encuentra en la <a href="numeralia.html">numeralia</a>.</p><a class="link-arrow" href="numeralia.html">Ver personal académico por ciclo {ic('arrow-up-right')}</a></div>
    {figure('planta-docente', 'Distribución de la planta docente por nivel y tipo de contratación', wide=True)}
  </div>
</section>'''
    return page('indicadores.html', 'Indicadores básicos: aspirantes y planta docente', 'Indicadores de la UAdeC: aspirantes por nivel y sexo, carreras con mayor demanda y distribución de la planta docente.', body, 'indicadores.html')


# ======================================================================
# DOCUMENTOS
# ======================================================================
def fsize(fn):
    s = os.path.getsize(os.path.join(OUT, 'docs', fn))
    return f'{s / 1048576:.1f} MB' if s > 1048576 else f'{round(s / 1024)} KB'


def doc_item(title, sub, files):
    acts = ''.join(f'<a href="docs/{fn}" target="_blank" rel="noopener">{ic("file-down")}{lbl}<span class="sr-only"> {e(title)} en PDF, se abre en otra pestaña</span> <span class="muted small">· {fsize(fn)}</span></a>' if fn else f'<span class="muted small">{lbl}: no disponible</span>' for lbl, fn in files)
    return f'<div class="doc reveal"><span class="doc-icon">{ic("file-text")}</span><div class="doc-body"><h3>{title}</h3><p>{sub}</p></div><div class="doc-actions">{acts}</div></div>'


def build_documentos():
    cuad = [('Cuadernillo de Indicadores 2016', 'Edición de enero de 2016', 'cuadernillo_indicene16.pdf'),
            ('Cuadernillo de Indicadores 2015', 'Edición de mayo de 2015', 'cuadernillo_indicmay15.pdf'),
            ('Cuadernillo de Indicadores 2014', 'Edición de mayo de 2014', 'cuadernillo_indicmay14.pdf')]
    inf = [('Segundo Informe del Rector 2014-2015', 'Informe de actividades', 'segundoinformerector2014-2015.pdf'),
           ('Primer Informe del Rector 2013-2014', 'Informe de actividades', 'primerinformerector2013-2014.pdf')]
    body = page_hero('Portal SIE', 'Documentos e informes', 'Publicaciones con información cuantitativa sobre el quehacer institucional.', [('Portal SIE', 'sie.html'), ('Documentos', None)]) + f'''
<section class="section">
  <div class="container">
    <div class="split">
      <div class="prose reveal"><span class="eyebrow">Cuadernillo de indicadores</span><h2>Publicación anual de indicadores</h2><p>El cuadernillo de indicadores reúne información cuantitativa sobre el quehacer institucional para apoyar la planeación, la evaluación y la toma de decisiones en las actividades institucionales, el personal académico, la docencia, la investigación y la difusión cultural.</p></div>
      <div class="doc-list">{''.join(doc_item(t, s, [('Descargar', f)]) for t, s, f in cuad)}</div>
    </div>
  </div>
</section>
<section class="section section--tint">
  <div class="container">
    <div class="split">
      <div class="prose reveal"><span class="eyebrow">Informes</span><h2>Informes de actividades del Rector</h2><p>Documentos que presentan los resultados anuales de la gestión universitaria.</p></div>
      <div class="doc-list">{''.join(doc_item(t, s, [('Descargar', f)]) for t, s, f in inf)}</div>
    </div>
  </div>
</section>'''
    return page('documentos.html', 'Documentos: cuadernillos de indicadores e informes', 'Descarga los cuadernillos de indicadores 2014, 2015 y 2016 y los informes de actividades del Rector de la UAdeC en PDF.', body, 'documentos.html')


# ======================================================================
# AUDITORÍAS
# ======================================================================
def build_auditorias():
    aud = [('Auditoría 2016-2', 'Enero–junio 2017', 'aud_20162_gral.pdf', 'aud_20162_res.pdf'),
           ('Auditoría 2016-1', 'Agosto–diciembre 2016', 'aud_20161_gral.pdf', 'aud_20161_res.pdf'),
           ('Auditoría 2015-2', 'Enero–junio 2016', 'aud_20152_gral.pdf', None),
           ('Auditoría 2015-1', 'Agosto–diciembre 2015', 'aud_20151_gral.pdf', 'aud_20151_res.pdf'),
           ('Auditoría 2014-2', 'Enero–junio 2015', 'aud_20142_gral.pdf', 'aud_20142_res.pdf'),
           ('Auditoría 2014-1', 'Agosto–diciembre 2014', None, 'aud_20141_res.pdf')]
    items = ''.join(f'<li>{doc_item(t, s, [x for x in [("General", g), ("Resumen", r)]])}</li>' for t, s, g, r in aud)
    body = page_hero('Portal SIE', 'Auditorías de matrícula 911', 'Documentos de la auditoría de la matrícula reportada en el Cuestionario Estadístico 911, por ciclo escolar.', [('Portal SIE', 'sie.html'), ('Auditorías 911', None)]) + f'''
<section class="section">
  <div class="container split split--aud">
    <div class="prose reveal">
      <span class="eyebrow">Cuestionario Estadístico 911</span>
      <h2>¿Qué es el formato 911?</h2>
      <p>Es el instrumento de la Secretaría de Educación Pública (SEP) para recabar información educativa de los niveles básico, medio superior y superior. Se elabora en conjunto con la Asociación Nacional de Universidades e Instituciones de Educación Superior (ANUIES) y la Secretaría de Hacienda y Crédito Público (SHCP).</p>
      <p>Recopila información como:</p>
      <ul class="chips">
        <li>Alumnos por área académica</li><li>Género y grado escolar</li><li>Egresados y titulados</li><li>Escuelas, facultades y posgrados</li><li>Institutos y centros de investigación</li><li>Personal académico y administrativo</li><li>Inmuebles</li><li>Carreras y modalidades</li>
      </ul>
      <p class="panel-block">En cumplimiento del requisito de la SEP, la UAdeC entrega y publica esta información desde el periodo 2011-2.</p>
    </div>
    <div>
      <h2 class="h3 reveal">Documentos por ciclo</h2>
      <ol class="timeline">{items}</ol>
    </div>
  </div>
</section>'''
    return page('auditorias.html', 'Auditorías de matrícula 911', 'Documentos generales y resúmenes de la auditoría de matrícula del Cuestionario Estadístico 911 de la UAdeC, de 2014 a 2017.', body, 'auditorias.html')


# ======================================================================
# CUBOS
# ======================================================================
def build_cubos():
    ind = ['Aspirantes por unidad, nivel educativo, aceptados y sexo', 'Carreras con mayor demanda, aspirantes y aceptados', 'Gráficos de alumnos demandantes por carrera',
           'Aspirantes por ciclo', 'Carreras más demandadas a través de los años', 'Aspirantes por estado de procedencia',
           'Primeros lugares del examen de admisión (College Board)', 'Calificaciones de aceptados', 'Puntuaciones mayores a 80 en el examen de admisión',
           'Aspirantes de bachilleratos de la UAdeC a licenciaturas de la UAdeC']
    lis = ''.join(f'<li>{ic("check")}<span>{x}</span></li>' for x in ind)
    body = page_hero('Portal SIE', 'Modelos (cubos OLAP)', 'Consultas dinámicas que permiten analizar grandes cantidades de datos desde distintas perspectivas.', [('Portal SIE', 'sie.html'), ('Modelos (cubos)', None)]) + f'''
<section class="section">
  <div class="container split">
    <div class="prose reveal">
      <span class="eyebrow">¿Qué es un cubo?</span>
      <h2>Datos organizados en jerarquías</h2>
      <p>Una de las formas de analizar la información es mediante cubos. Un cubo es una estructura de datos organizada en jerarquías: cada indicador puede evaluarse en cualquiera de sus niveles.</p>
      <p>Por ejemplo, es posible obtener los <em>aspirantes</em> por sexo, por periodo escolar, aceptados en una escuela determinada, por unidad o en toda la Universidad. Su objetivo es agilizar la consulta de grandes volúmenes de datos.</p>
      <div class="callout callout--gold">{ic('shield-check')}<p><strong>Acceso restringido.</strong> Para utilizar los modelos se requiere un usuario y contraseña institucionales. Para solicitar acceso, <a href="contacto.html">escríbenos</a>.</p></div>
      <div class="hero-actions"><a class="btn btn--primary" href="http://dwhouse.uadec.mx/cognos" target="_blank" rel="noopener noreferrer">Acceder a los modelos SIE {ic('external-link')}</a></div>
    </div>
    <div class="media-frame reveal reveal-d2">{img('cubo-olap', 'Ilustración de un cubo de datos con gráficas')}</div>
  </div>
</section>
<section class="section section--tint">
  <div class="container split split--rev">
    <div class="prose reveal">
      <span class="eyebrow">Ejemplo</span>
      <h2>Modelo de Admisiones</h2>
      <p>Aspirantes por unidad y periodo. Algunos indicadores que maneja el modelo:</p>
      <ul class="check-list">{lis}</ul>
      <h3>Otros cubos disponibles</h3>
      <ul class="chips"><li>Matrícula auditada 911</li><li>Títulos</li><li>Eficiencia terminal</li></ul>
    </div>
    {figure('modelo-admisiones', 'Vista del modelo de Admisiones: aspirantes por unidad y periodo', wide=True)}
  </div>
</section>'''
    return page('cubos.html', 'Modelos (cubos OLAP) del SIE', 'Modelos multidimensionales (cubos) del SIE de la UAdeC para consultar aspirantes, matrícula auditada 911, títulos y eficiencia terminal.', body, 'cubos.html')


# ======================================================================
# CONTACTO
# ======================================================================
def build_contacto():
    tels = '<br>'.join(f'<a href="tel:+52{t.replace(" ", "")}">{t}</a>' for t in CONTACT['tels'])
    body = page_hero('Contacto', 'Contacto', 'Escríbenos para solicitar información estadística, acceso a modelos o para cualquier duda sobre la Dirección de Planeación.', [('Contacto', None)]) + f'''
<section class="section">
  <div class="container split split--aud">
    <div class="reveal">
      <h2>Envíanos un mensaje</h2>
      <p class="muted">Al enviar, se abrirá tu aplicación de correo con el mensaje listo. Tus datos no se guardan en este sitio.</p>
      <form id="contact-form" class="form" novalidate autocomplete="on" action="mailto:{CONTACT['email']}" method="post" enctype="text/plain">
        <div class="form-row">
          <div class="field"><label for="nombre">Nombre completo <span class="req" aria-hidden="true">*</span></label><input class="input" id="nombre" name="nombre" type="text" required maxlength="80" autocomplete="name"><p class="field-error" aria-live="polite"></p></div>
          <div class="field"><label for="correo">Correo electrónico <span class="req" aria-hidden="true">*</span></label><input class="input" id="correo" name="correo" type="email" required maxlength="120" autocomplete="email" inputmode="email"><p class="field-error" aria-live="polite"></p></div>
        </div>
        <div class="form-row">
          <div class="field"><label for="telefono">Teléfono <span class="muted small">(opcional)</span></label><input class="input" id="telefono" name="telefono" type="tel" maxlength="20" autocomplete="tel" inputmode="tel"><p class="field-error" aria-live="polite"></p></div>
          <div class="field"><label for="escuela">Escuela, facultad o dependencia</label><input class="input" id="escuela" name="escuela" type="text" maxlength="120" autocomplete="organization"><p class="field-error" aria-live="polite"></p></div>
        </div>
        <div class="form-row">
          <div class="field"><label for="asunto">Asunto <span class="req" aria-hidden="true">*</span></label>
            <select class="select" id="asunto" name="asunto" required>
              <option value="">Selecciona una opción</option>
              <option>Modelos (cubos) e intranet</option><option>Indicadores</option><option>Matrícula 911</option><option>Numeralia</option><option>Otro</option>
            </select><p class="field-error" aria-live="polite"></p></div>
          <fieldset class="field"><legend>Prioridad</legend>
            <div class="radio-group">
              <label class="radio-pill"><input type="radio" name="prioridad" value="Baja"><span>Baja</span></label>
              <label class="radio-pill"><input type="radio" name="prioridad" value="Media" checked><span>Media</span></label>
              <label class="radio-pill"><input type="radio" name="prioridad" value="Alta"><span>Alta</span></label>
            </div>
          </fieldset>
        </div>
        <div class="field"><label for="mensaje">Mensaje <span class="req" aria-hidden="true">*</span></label><textarea class="textarea" id="mensaje" name="mensaje" required minlength="10" maxlength="2000"></textarea><p class="field-hint">Máximo 2,000 caracteres.</p><p class="field-error" aria-live="polite"></p></div>
        <div class="hp" aria-hidden="true"><label for="website">No llenar este campo</label><input id="website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
        <div class="check"><input id="privacidad" name="privacidad" type="checkbox" required><label for="privacidad">He leído y acepto el <a href="aviso-de-privacidad.html" target="_blank" rel="noopener">aviso de privacidad</a>. <span class="req" aria-hidden="true">*</span></label><p class="field-error" aria-live="polite"></p></div>
        <p id="form-status" class="form-status" role="status" hidden></p>
        <button class="btn btn--primary" type="submit">{ic('send')} Preparar mensaje</button>
      </form>
    </div>
    <aside class="reveal reveal-d2" aria-label="Datos de contacto">
      <div class="card">
        <h2>Datos de contacto</h2>
        <div class="contact-card">
          <div class="contact-item">{ic('map-pin')}<div><strong>Dirección</strong>{'<br>'.join(CONTACT['addr'])}<br><a href="{CONTACT['maps']}" target="_blank" rel="noopener noreferrer">Ver en el mapa</a></div></div>
          <div class="contact-item">{ic('phone')}<div><strong>Teléfonos</strong>{tels}</div></div>
          <div class="contact-item">{ic('mail')}<div><strong>Correo</strong><a href="mailto:{CONTACT['email']}">{CONTACT['email']}</a></div></div>
          <div class="contact-item">{ic('clock')}<div><strong>Horario de atención</strong>{CONTACT['hours']}</div></div>
          <div class="contact-item">{ic('facebook')}<div><strong>Redes sociales</strong><a href="{CONTACT['facebook']}" target="_blank" rel="noopener noreferrer">Facebook de la Dirección de Planeación</a></div></div>
        </div>
      </div>
    </aside>
  </div>
</section>'''
    body = body.replace(' style-free', '')
    return page('contacto.html', 'Contacto', 'Contacta a la Dirección de Planeación de la UAdeC: dirección, teléfonos, correo, horario y formulario para solicitudes del SIE.', body, 'contacto.html')


# ======================================================================
# AVISO DE PRIVACIDAD
# ======================================================================
def build_privacidad():
    body = page_hero('Legal', 'Aviso de privacidad', 'Cómo tratamos tus datos personales cuando visitas este sitio o te comunicas con nosotros.', [('Aviso de privacidad', None)]) + f'''
<section class="section">
  <div class="container prose">
    <p class="muted small">Última actualización: {TODAY}</p>
    <h2>1. Responsable</h2>
    <p>La <strong>Universidad Autónoma de Coahuila</strong>, a través de la <strong>Dirección de Planeación</strong>, con domicilio en {', '.join(CONTACT['addr'])}, es responsable del tratamiento de los datos personales que se recaben por medio de este sitio, conforme a la Ley General de Protección de Datos Personales en Posesión de Sujetos Obligados y a la Ley de Protección de Datos Personales en Posesión de Sujetos Obligados del Estado de Coahuila de Zaragoza.</p>
    <h2>2. Datos personales que se recaban</h2>
    <p>Solo si decides escribirnos mediante el formulario de contacto o por correo: nombre, correo electrónico, teléfono (opcional), escuela, facultad o dependencia, y el contenido de tu mensaje. <strong>No se recaban datos personales sensibles.</strong></p>
    <p>El formulario de este sitio <strong>no almacena información en ningún servidor</strong>: prepara un mensaje en tu propia aplicación de correo y tú decides si lo envías.</p>
    <h2>3. Finalidades</h2>
    <ul><li>Atender y dar seguimiento a tu solicitud de información, asesoría o acceso a los modelos del SIE.</li><li>Comunicarnos contigo para responder tu solicitud.</li></ul>
    <p>Tus datos no se utilizan con fines publicitarios ni de mercadotecnia.</p>
    <h2>4. Transferencias</h2>
    <p>No se realizan transferencias de datos personales, salvo aquellas necesarias para atender requerimientos de información de una autoridad competente, debidamente fundados y motivados.</p>
    <h2>5. Derechos ARCO</h2>
    <p>Puedes ejercer tus derechos de acceso, rectificación, cancelación y oposición (ARCO), así como la portabilidad de tus datos, ante la Unidad de Transparencia de la Universidad Autónoma de Coahuila, o escribiendo a <a href="mailto:{CONTACT['email']}">{CONTACT['email']}</a>, indicando tu nombre, el derecho que deseas ejercer y un medio para recibir respuesta.</p>
    <h2 id="cookies">6. Cookies y almacenamiento local</h2>
    <p>Este sitio <strong>no utiliza cookies propias ni de terceros</strong> para rastreo, publicidad o perfiles. No carga recursos de redes sociales, mapas ni servicios externos que puedan instalar cookies.</p>
    <div class="table-wrap">
      <table>
        <caption>Información almacenada en tu navegador</caption>
        <thead><tr><th scope="col">Nombre</th><th scope="col">Tipo</th><th scope="col">Finalidad</th><th scope="col">Duración</th></tr></thead>
        <tbody><tr><th scope="row">dp_consent</th><td>Almacenamiento local (necesario)</td><td>Recordar tu elección en el aviso de cookies</td><td>Hasta que lo borres</td></tr></tbody>
      </table>
    </div>
    <p class="panel-block">Si en el futuro se incorporan estadísticas de visitas, solo se activarán con tu consentimiento previo y este aviso se actualizará. Puedes cambiar tu elección en cualquier momento:</p>
    <p><button class="btn btn--ghost" type="button" data-open-cookies>{ic('cookie')} Preferencias de cookies</button></p>
    <h2>7. Registros del servidor</h2>
    <p>Como cualquier sitio web, el servidor puede registrar de forma automática datos técnicos (dirección IP, fecha y hora, página solicitada y navegador) con fines exclusivos de seguridad y funcionamiento. Estos registros no se usan para identificarte.</p>
    <h2>8. Cambios al aviso</h2>
    <p>Cualquier modificación a este aviso de privacidad se publicará en esta misma página.</p>
  </div>
</section>'''
    return page('aviso-de-privacidad.html', 'Aviso de privacidad y política de cookies', 'Aviso de privacidad y política de cookies del sitio de la Dirección de Planeación de la Universidad Autónoma de Coahuila.', body, 'aviso-de-privacidad.html')


# ======================================================================
# 404
# ======================================================================
def build_404():
    B = '/'  # rutas absolutas: la 404 se muestra en cualquier URL
    body = f'''<section class="error-page">
  <div class="container hero-anim">
    <img src="{B}assets/img/escudo-uadec.webp" width="{SIZES['escudo-uadec'][0]}" height="{SIZES['escudo-uadec'][1]}" alt="">
    <p class="error-code" aria-hidden="true">404</p>
    <h1>No encontramos esta página</h1>
    <p class="lead muted">Es posible que la dirección haya cambiado con el nuevo diseño del sitio o que el enlace esté incompleto.</p>
    <div class="hero-actions">
      <a class="btn btn--primary" href="{B}index.html">{ic('house', B=B)} Ir al inicio</a>
      <a class="btn btn--ghost" href="{B}numeralia.html">Ver numeralia</a>
      <a class="btn btn--ghost" href="{B}contacto.html">Reportar un problema</a>
    </div>
  </div>
</section>'''
    return page('404.html', 'Página no encontrada', 'La página que buscas no existe o cambió de dirección.', body, None, B=B, noindex=True)


PAGES = {
    'index.html': (build_index, '1.0', 'monthly'),
    'sie.html': (build_sie, '0.9', 'yearly'),
    'numeralia.html': (build_numeralia, '0.9', 'monthly'),
    'indicadores.html': (build_indicadores, '0.8', 'yearly'),
    'documentos.html': (build_documentos, '0.8', 'yearly'),
    'auditorias.html': (build_auditorias, '0.7', 'yearly'),
    'cubos.html': (build_cubos, '0.6', 'yearly'),
    'somos-uadec.html': (build_somos, '0.7', 'yearly'),
    'contacto.html': (build_contacto, '0.7', 'yearly'),
    'aviso-de-privacidad.html': (build_privacidad, '0.3', 'yearly'),
    '404.html': (build_404, None, None),
}

if __name__ == '__main__':
    today = datetime.date(2026, 11, 7).isoformat()
    urls = []
    for slug, (fn, prio, freq) in PAGES.items():
        out = fn()
        assert 'style=' not in out, f'estilo inline en {slug}'
        open(os.path.join(OUT, slug), 'w', encoding='utf-8').write(out)
        if prio:
            loc = SITE_URL + '/' + ('' if slug == 'index.html' else slug)
            urls.append(f'  <url><loc>{loc}</loc><lastmod>{today}</lastmod><changefreq>{freq}</changefreq><priority>{prio}</priority></url>')
    open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(urls) + '\n</urlset>\n')
    open(os.path.join(OUT, 'robots.txt'), 'w', encoding='utf-8').write(
        f'User-agent: *\nAllow: /\nDisallow: /404.html\n\nSitemap: {SITE_URL}/sitemap.xml\n')
    print('OK', len(PAGES), 'páginas')
