"""Genera el sitio estático completo de Casa Orus en ./dist"""
import os, json, shutil, html, datetime, re
from urllib.parse import quote
from catalogo import build as build_catalog, CATS, CAT

DOM = 'https://orusjoyeria.com'
WA_NUM = '573142720023'
IG = 'https://www.instagram.com/casa.orus/'
EMAIL = 'orusjoyeria1@gmail.com'
OUT = os.path.join(os.path.dirname(__file__), 'dist')
KIT = '/home/claude/kit/casa-orus-kit'
HOY = datetime.date.today().isoformat()
E = html.escape

def cop(v):
    return '$' + f'{v:,}'.replace(',', '.') if v else ''

def wa(msg):
    return f'https://wa.me/{WA_NUM}?text=' + quote(msg)

ICON = {
 'wa': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.2a9.7 9.7 0 0 0-8.3 14.8L2.4 21.8l4.9-1.3A9.7 9.7 0 1 0 12 2.2zm0 17.7c-1.5 0-3-.4-4.2-1.2l-.3-.2-2.9.8.8-2.8-.2-.3A8 8 0 1 1 12 19.9zm4.4-6c-.2-.1-1.4-.7-1.7-.8s-.4-.1-.5.1-.6.8-.8.9-.3.2-.5 0a6.6 6.6 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.1 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.5-.4h-.5a.9.9 0 0 0-.6.3 2.7 2.7 0 0 0-.9 2c0 1.2.9 2.4 1 2.5s1.7 2.6 4.2 3.7c1.6.7 2.2.7 3 .6.5-.1 1.4-.6 1.6-1.1s.2-1 .1-1.1-.2-.2-.4-.3z"/></svg>',
 'menu': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
 'buscar': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/></svg>',
 'ig': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="4" y="4" width="16" height="16" rx="4.5"/><circle cx="12" cy="12" r="3.6"/><circle cx="17" cy="7" r=".8" fill="currentColor"/></svg>',
}
L = 'fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
PICT = {
 'mano': f'<svg viewBox="0 0 24 24" {L}><path d="M7 12V6.5a1.5 1.5 0 0 1 3 0V11"/><path d="M10 10.5V5a1.5 1.5 0 0 1 3 0v5.5"/><path d="M13 10.5V6a1.5 1.5 0 0 1 3 0v6"/><path d="M16 9.5a1.5 1.5 0 0 1 3 0V14a7 7 0 0 1-7 7h-.6a6 6 0 0 1-4.6-2.2L4.2 15.6a1.6 1.6 0 0 1 2.5-2L8 15"/></svg>',
 'oro': f'<svg viewBox="0 0 24 24" {L}><path d="M3 18h8l-1.6-5H4.6z"/><path d="M13 18h8l-1.6-5h-4.8z"/><path d="M8 12h8l-1.6-5H9.6z"/></svg>',
 'escudo': f'<svg viewBox="0 0 24 24" {L}><path d="M12 3l7 3v5.5c0 4.6-3 8-7 9.5-4-1.5-7-4.9-7-9.5V6z"/><path d="M8.8 12.2l2.2 2.2 4.4-4.6"/></svg>',
 'envio': f'<svg viewBox="0 0 24 24" {L}><path d="M2.5 6.5h11v9h-11z"/><path d="M13.5 9.5h4l3 3.2v2.8h-7"/><circle cx="6.5" cy="17" r="1.8"/><circle cx="17" cy="17" r="1.8"/></svg>',
 'gema': f'<svg viewBox="0 0 24 24" {L}><path d="M7 4h10l4 5-9 11L3 9z"/><path d="M3 9h18"/><path d="M9.5 4L8 9l4 11 4-11-1.5-5"/></svg>',
 'destello': f'<svg viewBox="0 0 24 24" {L}><path d="M12,3 Q13.3,10.7 18,12 Q13.3,13.3 12,21 Q10.7,13.3 6,12 Q10.7,10.7 12,3 Z"/></svg>',
 'hoja': f'<svg viewBox="0 0 24 24" {L}><path d="M5 19c0-8 5-13 14-14 0 9-5 14-13 14z"/><path d="M5 19c3-4 6-6.5 9-8"/></svg>',
 'agua': f'<svg viewBox="0 0 24 24" {L}><path d="M12 3.5s-5.5 6.2-5.5 10a5.5 5.5 0 0 0 11 0c0-3.8-5.5-10-5.5-10z"/><path d="M4 20L20 4"/></svg>',
 'regalo': f'<svg viewBox="0 0 24 24" {L}><path d="M4 10h16v10H4z"/><path d="M3 7h18v3H3z"/><path d="M12 7v13"/><path d="M12 7C10.5 4 7.5 3.5 7.5 5.5S10 7 12 7zM12 7c1.5-3 4.5-3.5 4.5-1.5S14 7 12 7z"/></svg>',
 'frasco': f'<svg viewBox="0 0 24 24" {L}><path d="M9 3h6v3H9z"/><path d="M8 6h8l1 3v11H7V9z"/></svg>',
}

CAT_IMG = {}
DUP = {}  # se rellena con la primera pieza con foto de cada categoría

# ---------------------------------------------------------------- plantillas
NAV = [('Inicio', '/'), ('Colección', '/coleccion/'), ('Manillas', '/coleccion/manillas-y-pulseras/'), ('Cadenas', '/coleccion/cadenas-y-gargantillas/'),
       ('Aretes', '/coleccion/aretes/'), ('Dijes', '/coleccion/dijes/'),
       ('Casa Orus', '/creaciones/'), ('Historia', '/nuestra-historia/'), ('Guías', '/guias/')]

def head(title, desc, path, og_img='/assets/img/og-casa-orus.png', schema=None, noindex=False, typ='website', precio=None):
    can = DOM + path
    sch = ''.join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in (schema or []))
    return f'''<!DOCTYPE html>
<html lang="es-CO">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{can}">
{'<meta name="robots" content="noindex, follow">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'}
<meta property="og:type" content="{typ}"><meta property="og:site_name" content="Casa Orus">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{can}"><meta property="og:image" content="{og_img if og_img.startswith('http') else DOM + og_img}">
<meta property="og:locale" content="es_CO"><meta name="twitter:card" content="summary_large_image">{f'<meta property="product:price:amount" content="{precio}"><meta property="product:price:currency" content="COP">' if precio else ""}
<meta name="geo.region" content="CO-ANT"><meta name="geo.placename" content="Medellín">
<meta name="theme-color" content="#190420">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/pagella.woff" as="font" type="font/woff" crossorigin>
<link rel="preconnect" href="https://belatrizcolombia.com">
<link rel="stylesheet" href="/assets/css/estilos.css?v={HOY}">
<!-- Google Search Console: pega aquí la etiqueta de verificación -->
<!-- Google Analytics 4: pega aquí el fragmento gtag con tu ID G-XXXXXXX -->
{sch}
</head>
<body>
<a class="salto" href="#contenido">Saltar al contenido</a>
<div class="barra"><span>Envíos a toda Colombia</span><span>5 años de garantía en el color</span><span>Pedidos por WhatsApp</span></div>
<header class="cabecera"><div class="contenedor">
<a class="logo" href="/" aria-label="Casa Orus, inicio"><img src="/assets/img/logo-casa-orus.svg" alt="Casa Orus · Joyería que trasciende" width="180" height="52"></a>
<nav class="nav" id="nav" aria-label="Principal"><ul class="menu">{''.join(f'<li><a href="{u}"{" aria-current=\"page\"" if u == path else ""}>{n}</a></li>' for n, u in NAV)}</ul></nav>
<div class="acciones">
<a class="icono-btn" href="/coleccion/#buscar" aria-label="Buscar en la colección">{ICON['buscar']}</a>
<a class="icono-btn" href="{wa('Hola Casa Orus ✨ quiero información sobre sus joyas.')}" aria-label="Escribir por WhatsApp" rel="noopener">{ICON['wa']}</a>
<button class="icono-btn abrir-menu" aria-controls="nav" aria-expanded="false" aria-label="Abrir menú">{ICON['menu']}</button>
</div></div></header>
<main id="contenido">
'''

def foot():
    cats = ''.join(f'<li><a href="/coleccion/{c[0]}/">{c[1]}</a></li>' for c in CATS[:6])
    return f'''</main>
<footer class="pie"><div class="contenedor">
<div class="pie-grid">
<div><img src="/assets/img/logo-casa-orus.svg" alt="Casa Orus" width="190" height="55" style="height:55px;width:auto;margin-bottom:18px">
<p>Joyería en oro laminado 18k hecha con amor en Medellín. Más que joyas, creamos historias.</p>
<a class="icono-btn" href="{IG}" aria-label="Instagram de Casa Orus" rel="noopener">{ICON['ig']}</a></div>
<div><h4>Colección</h4><ul>{cats}<li><a href="/coleccion/fe-y-proteccion/">Fe y protección</a></li></ul></div>
<div><h4>Casa Orus</h4><ul><li><a href="/nuestra-historia/">Nuestra historia</a></li><li><a href="/creaciones/">Creaciones Casa Orus</a></li><li><a href="/regalos/">Regalos</a></li><li><a href="/guias/">Guías</a></li><li><a href="/aliados/">Aliados y mayoristas</a></li></ul></div>
<div><h4>Atención</h4><ul><li><a href="{wa('Hola Casa Orus ✨')}" rel="noopener">WhatsApp +57 314 272 0023</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="/garantia-y-cuidados/">Garantía y cuidados</a></li><li><a href="/preguntas-frecuentes/">Preguntas frecuentes</a></li><li><a href="/contacto/">Contacto</a></li></ul></div>
</div>
<div class="pie-base"><span>© {datetime.date.today().year} Casa Orus · Joyería que trasciende · Medellín, Colombia</span><span><a href="/privacidad/">Política de privacidad</a></span></div>
</div></footer>
<a class="wa-flotante" href="{wa('Hola Casa Orus ✨ quiero información sobre sus joyas.')}" aria-label="Escríbenos por WhatsApp" rel="noopener">{ICON['wa']}</a>
<script src="/assets/js/sitio.js?v={HOY}" defer></script>
</body></html>'''

def sep():
    return '<div class="sep" aria-hidden="true"><i></i></div>'

def migas(items):
    li = ' <span>/</span> '.join(f'<a href="{u}">{E(n)}</a>' if u else E(n) for n, u in items)
    return f'<nav class="migas" aria-label="Ruta">{li}</nav>'

def bc_schema(items):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, **({'item': DOM + u} if u else {})} for i, (n, u) in enumerate(items)]}

ORG = {'@context': 'https://schema.org', '@type': 'JewelryStore', '@id': DOM + '/#tienda', 'name': 'Casa Orus', 'alternateName': 'Casa Orus · Joyería que trasciende',
       'url': DOM + '/', 'logo': DOM + '/assets/img/apple-touch-icon.png', 'image': DOM + '/assets/img/og-casa-orus.png',
       'description': 'Joyería en oro laminado 18k hecha en Medellín: manillas tejidas, cadenas, aretes, dijes y anillos con 5 años de garantía en el color.',
       'telephone': '+57 314 272 0023', 'email': EMAIL, 'priceRange': '$$',
       'address': {'@type': 'PostalAddress', 'addressLocality': 'Medellín', 'addressRegion': 'Antioquia', 'addressCountry': 'CO'},
       'areaServed': [{'@type': 'City', 'name': 'Medellín'}, {'@type': 'Country', 'name': 'Colombia'}], 'sameAs': [IG]}

def card(p, lazy=True):
    sinfoto = '<span class="sin-foto"><img src="/assets/img/isotipo.svg" alt=""></span>'
    alt_attr = f' data-alt="{p["img2"]}"' if p['img2'] else ''
    etq = '<span class="etq">Casa Orus</span>' if p['propio'] else ''
    buscar = E(f"{p['nombre']} {p['ref']} {CAT[p['cat']][1]} {' '.join(p['tags'])}")
    precio = f'<span class="precio">{cop(p["precio"])}</span>' if p['precio'] else '<span class="precio consultar">Consultar precio</span>'
    return (f'<a class="card" href="/joya/{p["slug"]}/" data-tags="{" ".join(p["tags"] + [p["cat"]])}" data-precio="{p["precio"] or 0}" data-buscar="{buscar}">'
            f'<div class="card-img">{etq}<img src="{p["img"]}"{alt_attr} alt="{E(p["nombre"])} en oro laminado 18k" width="400" height="400" loading="{"lazy" if lazy else "eager"}" decoding="async" referrerpolicy="no-referrer" onerror="orusImg(this)">{sinfoto}</div>'
            f'<div class="card-txt"><h3>{E(p["nombre"])}</h3>{precio}<span class="ref">{"Hecho a mano" if p["propio"] else "Ref. " + E(p["ref"])}</span></div></a>')

def write(path, content):
    full = os.path.join(OUT, path.strip('/'), 'index.html') if not path.endswith('.html') else os.path.join(OUT, path.strip('/'))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)
    return full

# ---------------------------------------------------------------- textos de categoría
CAT_TXT = {
 'manillas-y-pulseras': ('Manillas y pulseras en oro laminado 18k', '<p>En Casa Orus encuentras dos mundos: las <strong>manillas tejidas a mano</strong> en Medellín, con balines de oro laminado, hilo rojo y medallas de protección como San Benito, la Virgen de Guadalupe o el Divino Niño, y las <strong>pulseras de eslabón</strong> italianas: cubanas, singapur, marine, barril o militar.</p><p>Todas están hechas en oro laminado 18k, no contienen níquel y tienen 5 años de garantía en el color con uso adecuado. Las manillas tejidas son ajustables; las pulseras de eslabón vienen en 16 y 19,5 cm, varias con extensor.</p>',
   [('¿Las manillas son ajustables?', 'Sí. Las manillas tejidas a mano tienen nudo corredizo, así que se adaptan a cualquier muñeca.'), ('¿Qué largo de pulsera elijo?', 'La medida de 16 cm suele quedar bien en muñecas delgadas y la de 19,5 cm en muñecas medianas a gruesas. Si dudas, escríbenos y te ayudamos.'), ('¿Me puedo bañar con la manilla?', 'Te recomendamos quitártela para bañarte o nadar: así el oro laminado conserva su brillo por más tiempo.')]),
 'cadenas-y-gargantillas': ('Cadenas en oro laminado 18k para hombre y mujer', '<p>Cadenas de 40 a 65 cm en los eslabones que más se buscan: <strong>cubana, franco, singapur, militar, veneciana, marine, barril, escalera y tejido chino</strong>, muchas de ellas de línea italiana. Las de 40 a 45 cm se lucen a la altura de la clavícula, ideales con un dije; las de 60 a 65 cm caen sobre el pecho y son las preferidas para un look más marcado.</p><p>También tenemos gargantillas con extensor para un acabado delicado. Todas en oro laminado 18k, hipoalergénicas y con 5 años de garantía en el color.</p>',
   [('¿Qué largo de cadena me conviene?', '45 cm queda a la altura de la clavícula y 60 a 65 cm cae sobre el pecho. Para llevar un dije, la mayoría de clientes elige entre 45 y 50 cm.'), ('¿Las cadenas sirven para hombre?', 'Sí. Las cubanas, franco, militar y barril en grosores desde 3 mm son las más elegidas por hombres.'), ('¿El oro laminado se pone negro?', 'Con buen uso, no. Evita el agua, el perfume y las cremas sobre la pieza y guárdala seca.')]),
 'aretes': ('Aretes en oro laminado 18k: topos y candongas', '<p>Desde <strong>topos</strong> pequeños para el día a día hasta <strong>candongas</strong> con circonias para una ocasión especial, además de ear cuffs y aretes con motivos como el ojo turco, el trébol, la cruz o la mano de Fátima.</p><p>Son livianos, hipoalergénicos y libres de níquel, aptos para orejas sensibles. Todos tienen 5 años de garantía en el color.</p>',
   [('¿Sirven para orejas sensibles?', 'Sí. Nuestros aretes no contienen níquel, el metal que más alergias produce.'), ('¿Qué diferencia hay entre topos y candongas?', 'Los topos van pegados al lóbulo y son discretos; las candongas son aros, más visibles.')]),
 'dijes': ('Dijes en oro laminado 18k', '<p>Más de 200 dijes para contar tu historia: <strong>medallas de la Virgen de Guadalupe, San Benito, la Milagrosa y el Divino Niño</strong>, cruces, rostros de Cristo, iniciales, corazones y amuletos como el ojo turco o el trébol. Combínalos con cualquiera de nuestras cadenas.</p><p>Todos están hechos en oro laminado 18k y tienen 5 años de garantía en el color.</p>',
   [('¿El dije incluye cadena?', 'No, el dije se vende solo. Te ayudamos a elegir la cadena que mejor le queda.'), ('¿Tienen dijes con la inicial de mi nombre?', 'Sí, tenemos varios estilos de iniciales. Pregúntanos por la letra que buscas.')]),
 'anillos': ('Anillos en oro laminado 18k', '<p>Anillos <strong>tejidos a mano</strong> con balines, alianzas lisas y modelos ajustables que se adaptan a tu dedo. Son cómodos para llevar todos los días.</p>', [('¿Cómo sé mi talla?', 'Mide el contorno de tu dedo con un hilo y envíanos la medida en milímetros por WhatsApp. También tenemos modelos ajustables.')]),
 'rosarios-y-cruceros': ('Rosarios, cruceros y denarios en oro laminado', '<p>Cruceros de la Virgen de Guadalupe y San Benito, rosarios y denarios en oro laminado 18k para llevar tu fe contigo a diario.</p>', []),
 'tobilleras': ('Tobilleras en oro laminado 18k', '<p>Tobilleras finas de 22 a 25 cm, varias con extensor ajustable, en tejido chino, escalera, circonias y ojo turco.</p>', []),
 'conjuntos': ('Conjuntos en oro laminado 18k', '<p>Cadena y aretes a juego, listos para regalar o regalarte.</p>', []),
}
SUBF = {
 'manillas-y-pulseras': [('fe', 'Fe y protección'), ('italiana', 'Italianas'), ('brillo', 'Con brillo'), ('amor', 'Corazones')],
 'cadenas-y-gargantillas': [('corta', 'Cortas (hasta 45 cm)'), ('larga', 'Largas (50 a 65 cm)'), ('italiana', 'Italianas'), ('gargantilla', 'Gargantillas'), ('brillo', 'Con brillo')],
 'aretes': [('topos', 'Topos'), ('candongas', 'Candongas'), ('otros-aretes', 'Otros diseños'), ('fe', 'Fe y protección'), ('amor', 'Corazones')],
 'dijes': [('fe', 'Fe y protección'), ('iniciales', 'Iniciales'), ('amor', 'Amor'), ('brillo', 'Con circonias')],
 'anillos': [('casa-orus', 'Hechos por Casa Orus')],
}
TIPOS = {'manillas-y-pulseras': [('manillas', 'Manillas · balines y tejidas'), ('pulseras', 'Pulseras')]}

def orden():
    return ('<div class="orden"><label for="orden">Ordenar:</label><select id="orden"><option value="rel">Destacados</option>'
            '<option value="asc">Precio: menor a mayor</option><option value="desc">Precio: mayor a menor</option></select></div>')

def rango(prods):
    v = sorted(p['precio'] for p in prods if p['precio'])
    return (v[0], v[-1]) if v else (None, None)

def faq_html(faqs):
    return ''.join(f'<details class="acord"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faqs)

def faq_schema(faqs):
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faqs]}

# ---------------------------------------------------------------- páginas
def page_cat(slug, prods):
    c = CAT[slug]; h2, txt, faqs = CAT_TXT[slug]
    items = [('Inicio', '/'), ('Colección', '/coleccion/'), (c[1], None)]
    chips = ''.join(f'<button class="chip" type="button" data-f="{k}" aria-pressed="false">{n}</button>' for k, n in SUBF.get(slug, []) if any(k in p['tags'] for p in prods))
    tipos = ''.join(f'<button class="chip tipo" type="button" data-t="{k}" aria-pressed="false">{n}</button>' for k, n in TIPOS.get(slug, []))
    filtros = ''
    if tipos:
        filtros += f'<div class="filtros tipos" role="group" aria-label="Tipo"><button class="chip tipo" type="button" data-t="todo" aria-pressed="true">Todas</button>{tipos}</div>'
    if chips:
        filtros += f'<div class="filtros" role="group" aria-label="Filtrar"><button class="chip" type="button" data-f="todo" aria-pressed="true">{"Todo" if tipos else "Todas"}</button>{chips}</div>'
    filtros += orden()
    lo, hi = rango(prods)
    grid = ''.join(card(p, i > 7) for i, p in enumerate(sorted(prods, key=lambda p: (not p['propio'], p['nombre']))))
    sch = [bc_schema(items), {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': c[1], 'url': DOM + f'/coleccion/{slug}/',
           'mainEntity': {'@type': 'ItemList', 'numberOfItems': len(prods), 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': DOM + f'/joya/{p["slug"]}/'} for i, p in enumerate(prods[:50])]}}]
    if faqs: sch.append(faq_schema(faqs))
    body = f'''<section class="cab-cat"><div class="contenedor">{migas(items)}
<span class="eyebrow">Colección · {len(prods)} piezas</span><h1>{E(c[1])} <span class="oro">en oro laminado 18k</span></h1>
<p class="lead">{E(c[3])}{f", desde {cop(lo)}" if lo else ""}. Pide cualquier pieza por WhatsApp citando su referencia.</p></div></section>
<section class="contenedor" style="padding-bottom:90px">{filtros}<p class="contador" id="contador" aria-live="polite"></p><div class="grid" id="lista">{grid}</div>
<div class="texto-cat"><h2>{E(h2)}</h2>{txt}{('<h2 style="margin-top:40px">Preguntas frecuentes</h2>' + faq_html(faqs)) if faqs else ''}</div></section>'''
    desc = c[5].replace('Envíos a toda Colombia.', f'Desde {cop(lo)}. Envíos a Colombia.') if lo else c[5]
    write(f'/coleccion/{slug}/', head(c[4], desc[:160], f'/coleccion/{slug}/', schema=sch) + body + foot())

def page_coleccion(P):
    items = [('Inicio', '/'), ('Colección', None)]
    chips = ''.join(f'<button class="chip" type="button" data-f="{c[0]}" aria-pressed="false">{c[2]}</button>' for c in CATS)
    cats = ''.join(cat_tile(c) for c in CATS)
    grid = ''.join(card(p, i > 7) for i, p in enumerate(sorted(P, key=lambda p: (not p['propio'], [c[0] for c in CATS].index(p['cat']), p['nombre']))))
    body = f'''<section class="cab-cat"><div class="contenedor">{migas(items)}<span class="eyebrow">{len(P)} piezas en oro laminado 18k</span>
<h1>La colección <span class="oro">Casa Orus</span></h1><p class="lead">Manillas, cadenas, aretes, dijes y más. Explora por categoría o busca por nombre o referencia, y pide tu pieza por WhatsApp.</p>
<div class="cats">{cats}</div></div></section>
<section class="contenedor" style="padding:30px 24px 90px" id="buscar"><h2>Todas las piezas</h2>
<form class="buscador" role="search" action="/coleccion/"><label class="salto" for="q">Buscar joyas</label><input id="q" name="q" type="search" placeholder="Busca: cubana, San Benito, topos, 45413…" autocomplete="off"><button class="btn btn-oro" type="submit">Buscar</button></form>
<div class="filtros" role="group" aria-label="Filtrar por categoría"><button class="chip" type="button" data-f="todo" aria-pressed="true">Todas</button>{chips}<button class="chip" type="button" data-f="fe" aria-pressed="false">Fe y protección</button></div>
{orden()}<p class="contador" id="contador" aria-live="polite"></p><div class="grid" id="lista">{grid}</div></section>'''
    write('/coleccion/', head('Colección de Joyería en Oro Laminado 18k | Casa Orus Medellín', 'Más de 500 piezas en oro laminado 18k: manillas, cadenas, aretes, dijes, anillos y tobilleras. Pide por WhatsApp con envío a toda Colombia.', '/coleccion/', schema=[bc_schema(items)]) + body + foot())

def cat_tile(c):
    img = CAT_IMG.get(c[0])
    return (f'<a class="cat" href="/coleccion/{c[0]}/"><div class="cat-img" style="background:#fff">'
            f'<img src="{img["img"]}" data-alt="{img["img2"]}" alt="{E(c[1])} en oro laminado" loading="lazy" style="object-fit:contain;padding:12%" referrerpolicy="no-referrer" onerror="orusImg(this)"><span class="sin-foto"><img src="/assets/img/isotipo.svg" alt=""></span></div>'
            f'<h3>{E(c[2] if len(c[1]) > 18 else c[1])}</h3><span>{E(c[3])}</span></a>')

def page_fe(P):
    fe = [p for p in P if 'fe' in p['tags']]
    items = [('Inicio', '/'), ('Colección', '/coleccion/'), ('Fe y protección', None)]
    chips = ''.join(f'<button class="chip" type="button" data-f="{c[0]}" aria-pressed="false">{c[2]}</button>' for c in CATS if any(p['cat'] == c[0] for p in fe))
    grid = ''.join(card(p, i > 7) for i, p in enumerate(sorted(fe, key=lambda p: (not p['propio'], p['cat'], p['nombre']))))
    faqs = [('¿Qué significa la medalla de San Benito?', 'Es una de las medallas de protección más antiguas de la tradición católica; quienes la llevan la asocian con la protección frente al mal.'),
            ('¿Qué representa la Virgen de Guadalupe?', 'Es una de las advocaciones marianas más queridas en Latinoamérica; su medalla se lleva como símbolo de fe, amor y protección.'),
            ('¿Son buen regalo de primera comunión o bautizo?', 'Sí. Las medallas de la Virgen y las manillas de San Benito son de los regalos más elegidos para estas fechas.')]
    body = f'''<section class="cab-cat noche" style="padding-bottom:56px"><div class="contenedor">{migas(items)}<span class="eyebrow">Colección especial</span>
<h1>Fe y protección <span class="oro">en oro laminado</span></h1><p class="lead">Solo piezas de San Benito y de la Virgen: Guadalupe, Milagrosa, del Carmen, de Fátima y Rosa Mística, en manillas, medallas, cruceros y aretes. Para llevar tu fe contigo, todos los días.</p></div></section>
<section class="contenedor" style="padding:46px 24px 90px"><div class="filtros" role="group" aria-label="Filtrar"><button class="chip" type="button" data-f="todo" aria-pressed="true">Todas</button>{chips}</div>{orden()}
<p class="contador" id="contador" aria-live="polite"></p><div class="grid" id="lista">{grid}</div>
<div class="texto-cat"><h2>Joyería de fe hecha para el día a día</h2><p>Las piezas de protección son las que más acompañan a nuestros clientes: una manilla de San Benito que no se quitan, una medalla de la Virgen de Guadalupe o de la Milagrosa que acompaña cada paso. Por eso las hacemos en oro laminado 18k, resistente al uso diario y con 5 años de garantía en el color.</p><h2 style="margin-top:40px">Preguntas frecuentes</h2>{faq_html(faqs)}</div></section>'''
    write('/coleccion/fe-y-proteccion/', head('Manillas y Medallas San Benito y Virgen en Oro Laminado | Casa Orus', ('Manillas y medallas de San Benito y de la Virgen de Guadalupe, la Milagrosa y del Carmen en oro laminado 18k, hechas en Medellín. 5 años de garantía.')[:160], '/coleccion/fe-y-proteccion/', schema=[bc_schema(items), faq_schema(faqs)]) + body + foot())

def page_producto(p, P):
    c = CAT[p['cat']]
    items = [('Inicio', '/'), ('Colección', '/coleccion/'), (c[1], f'/coleccion/{p["cat"]}/'), (p['nombre'], None)]
    titulo = f'{p["nombre"]} en oro laminado 18k'
    msg = f'Hola Casa Orus ✨ me interesa la pieza "{p["nombre"]}"' + ('' if p['propio'] else f' (Ref. {p["ref"]})') + (f' de {cop(p["precio"])}' if p['precio'] else '') + f'. {DOM}/joya/{p["slug"]}/'
    gal = p['galeria']
    thumbs = ''.join(f'<button type="button" aria-label="Ver foto {i+1}" aria-current="{"true" if i == 0 else "false"}"><img src="{u}" alt="" loading="lazy" referrerpolicy="no-referrer"></button>' for i, u in enumerate(gal)) if len(gal) > 1 else ''
    datos = [('Material', 'Oro laminado 18k sobre plata ley 925'), ('Categoría', c[1])] + list(p['medidas'].items()) + [('Elaboración', 'Hecha a mano en Medellín' if p['propio'] else 'Selección Casa Orus'), ('Garantía', '5 años en el color')]
    if not p['propio']: datos.insert(0, ('Referencia', p['ref']))
    var = f'<p style="margin:14px 0 4px;font-size:14px"><b style="font-weight:500">Letras disponibles:</b></p><div class="variantes">{"".join(f"<span>{v}</span>" for v in p["variantes"])}</div>' if p.get('variantes') else ''
    rel = [x for x in P if x['cat'] == p['cat'] and x['slug'] != p['slug'] and (set(x['tags']) & set(p['tags']) or not p['tags'])][:8] or [x for x in P if x['cat'] == p['cat'] and x['slug'] != p['slug']][:8]
    sch = [bc_schema(items), {'@context': 'https://schema.org', '@type': 'Product', 'name': titulo, 'image': gal[:1], 'description': p['desc'],
           'sku': p['ref'], 'mpn': p['ref'], 'brand': {'@type': 'Brand', 'name': 'Casa Orus'}, 'material': 'Oro laminado 18k', 'category': c[1], 'url': DOM + f'/joya/{p["slug"]}/'}]
    if p['precio']:
        sch[1]['offers'] = {'@type': 'Offer', 'url': DOM + f'/joya/{p["slug"]}/', 'priceCurrency': 'COP', 'price': p['precio'], 'priceValidUntil': f'{datetime.date.today().year + 1}-12-31',
            'availability': 'https://schema.org/InStock', 'itemCondition': 'https://schema.org/NewCondition', 'seller': {'@id': DOM + '/#tienda'}}
    alt1 = f' data-alt="{p["img2"]}"' if p['img2'] else ''
    body = f'''<div class="contenedor"><div style="padding-top:28px">{migas(items)}</div>
<article class="ficha">
<div><div class="galeria-principal" style="position:relative"><img src="{gal[0]}"{alt1} alt="{E(titulo)}" width="800" height="800" fetchpriority="high" referrerpolicy="no-referrer" onerror="orusImg(this)"><span class="sin-foto"><img src="/assets/img/isotipo.svg" alt=""></span></div>
<div class="miniaturas">{thumbs}</div></div>
<div><span class="eyebrow">{"Creación Casa Orus" if p["propio"] else c[1]}</span><h1>{E(p["nombre"])} <span class="oro">en oro laminado 18k</span></h1>
<p class="precio-ficha">{cop(p["precio"]) if p["precio"] else "Consultar precio"}{' <span>COP</span>' if p["precio"] else ""}</p>
<p class="lead" style="font-size:17px">{E(p["desc"])}</p>{var}
<div class="botones" style="margin-top:20px"><a class="btn btn-oro" href="{wa(msg)}" rel="noopener">{ICON["wa"]} Pedir por WhatsApp</a><a class="btn btn-linea" href="/coleccion/{p["cat"]}/">Ver más {E(c[2].lower())}</a></div>
<p class="nota" style="margin-top:12px">Te confirmamos disponibilidad y envío por WhatsApp.</p>
<ul class="datos">{"".join(f"<li><b>{E(k)}</b><span>{E(v)}</span></li>" for k, v in datos)}</ul>
<details class="acord" open><summary>Garantía de 5 años</summary><p>Tu pieza está hecha en plata ley 925 con tres capas de oro 18k, libre de níquel e hipoalergénica. Cubrimos el cambio de color durante 5 años con uso adecuado. <a href="/garantia-y-cuidados/">Ver condiciones</a>.</p></details>
<details class="acord"><summary>Cuidados</summary><ul><li>Quítatela para bañarte, nadar o hacer ejercicio.</li><li>Aplica perfume y cremas antes de ponértela.</li><li>Guárdala seca, en su bolsita o estuche.</li></ul></details>
<details class="acord"><summary>Envíos</summary><p>Enviamos a toda Colombia. Coordina tu pedido por WhatsApp y te damos el valor y el tiempo de entrega según tu ciudad.</p></details>
</div></article></div>
<section class="seccion alt" style="padding:70px 0"><div class="contenedor"><h2 class="centro">También te puede gustar</h2>{sep().replace('class="sep"', 'class="sep" style="margin:14px auto 34px"')}<div class="grid">{"".join(card(x) for x in rel)}</div></div></section>'''
    desc = f'{titulo}' + (f' por {cop(p["precio"])}. ' if p['precio'] else '. ') + ('Hecha a mano en Medellín. ' if p['propio'] else f'Ref. {p["ref"]}. ') + 'Sin níquel, 5 años de garantía. Envíos a toda Colombia.'
    og = gal[0] if gal[0].startswith('http') else '/assets/img/og-casa-orus.png'
    t = f'{titulo} | Casa Orus'
    if DUP.get(p['nombre'], 0) > 1 and not p['propio']: t = f'{p["nombre"]} Ref. {p["ref"]} · Oro Laminado 18k | Casa Orus'
    if len(t) > 68: t = f'{p["nombre"]}' + (f' Ref. {p["ref"]}' if DUP.get(p['nombre'], 0) > 1 else '') + ' | Casa Orus'
    write(f'/joya/{p["slug"]}/', head(t, desc[:158], f'/joya/{p["slug"]}/', og_img=og, schema=sch, typ='product', precio=p['precio']) + body + foot())

def pilares(oscuro=False):
    data = [('oro', 'Oro laminado', 'Belleza que perdura, brillo que hace historia.'), ('gema', 'Piedras naturales', 'Energía real, directamente de la naturaleza.'),
            ('destello', 'Diseños únicos', 'Cada pieza, una expresión de autenticidad.'), ('mano', 'Hechos a mano', 'Con amor y dedicación, en Medellín.')]
    return '<div class="pilares">' + ''.join(f'<div class="pilar"><div class="medallon">{PICT[i]}</div><h3>{t}</h3><p>{d}</p></div>' for i, t, d in data) + '</div>'

def pasos_garantia():
    data = [('Uso diario y cuidado especial', 'Nuestras joyas están hechas para usarse a diario sin cambiar de color. Evita el contacto con agua, perfumes, cremas y químicos, y guárdalas en un lugar seco.'),
            ('Hipoalergénicas y libres de níquel', 'Base de plata ley 925 con tres capas de oro 18k, sin níquel. Aptas para todo tipo de piel.'),
            ('Cobertura total del color', 'Cubrimos al 100 % el cambio de color con uso adecuado durante 5 años. No cubre roturas, pérdidas ni daños por mal uso.')]
    return '<ol class="pasos">' + ''.join(f'<li><span class="num">{i+1}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for i, (t, d) in enumerate(data)) + '</ol>'

FAQ_GEN = [
 ('¿Qué es el oro laminado?', 'Es una capa de oro real adherida a un metal base. En Casa Orus esa base es plata ley 925 cubierta con tres capas de oro 18k: el brillo del oro a un precio accesible y mucho más durable que un simple baño.'),
 ('¿El oro laminado se pone negro?', 'Con buen uso, no. Lo que lo opaca es el contacto frecuente con agua, perfume, cremas o químicos. Por eso damos 5 años de garantía en el color.'),
 ('¿Son hipoalergénicas?', 'Sí. No contienen níquel y su base es plata ley 925.'),
 ('¿Cómo hago un pedido?', 'Escríbenos por WhatsApp al +57 314 272 0023 con el nombre o la referencia de la pieza. Te confirmamos disponibilidad, precio y envío.'),
 ('¿Hacen envíos?', 'Sí, a toda Colombia. En Medellín coordinamos la entrega contigo.'),
 ('¿Hacen piezas personalizadas?', 'Sí: placas con nombre, combinaciones de piedras y manillas a pedido. Cuéntanos tu idea por WhatsApp.'),
]

def page_home(P):
    destacados = [p for p in P if p['propio']][:4] + [p for p in P if p['ref'] in ('41413', '45036', '23325', '23319', '30014', '55162', '23939', '34003')][:8]
    destacados = destacados[:8]
    fe = [p for p in P if 'fe' in p['tags'] and not p['propio']][:4]
    fe = [p for p in P if p['propio'] and 'fe' in p['tags']][:2] + fe[:2]
    cats = ''.join(cat_tile(c) for c in CATS[:4])
    guias = ''.join(f'<a class="guia" href="/guias/{s}/"><span class="eyebrow">Guía</span><h3>{E(t)}</h3><p>{E(d)}</p><span>Leer guía →</span></a>' for s, t, d, _ in GUIAS)
    sch = [ORG, {'@context': 'https://schema.org', '@type': 'WebSite', 'name': 'Casa Orus', 'url': DOM + '/', 'inLanguage': 'es-CO',
            'potentialAction': {'@type': 'SearchAction', 'target': DOM + '/coleccion/?q={q}', 'query-input': 'required name=q'}}, faq_schema(FAQ_GEN)]
    body = f'''<section class="hero noche"><div class="contenedor">
<div><span class="eyebrow">Joyería en oro laminado 18k · Medellín</span>
<h1>Joyería en oro laminado <span>que trasciende</span></h1>{sep()}
<p class="lead">Manillas tejidas a mano, cadenas, aretes y dijes en oro laminado 18k, sin níquel y con 5 años de garantía en el color. Más que joyas, creamos historias.</p>
<div class="botones"><a class="btn btn-oro" href="/coleccion/">Ver colección</a><a class="btn btn-linea" href="{wa('Hola Casa Orus ✨ quiero asesoría para elegir una joya.')}" rel="noopener">{ICON['wa']} Escríbenos</a></div></div>
<img class="hero-arte" src="/assets/img/logo-vertical-metal.svg" alt="" width="420" height="434" fetchpriority="high">
</div></section>
<section class="confianza" aria-label="Por qué Casa Orus"><div class="contenedor"><ul>
<li>{PICT['mano']}Hecho a mano en Medellín</li><li>{PICT['oro']}Oro laminado 18k</li><li>{PICT['hoja']}Sin níquel, hipoalergénico</li><li>{PICT['escudo']}5 años de garantía</li></ul></div></section>
<section class="seccion"><div class="contenedor centro"><span class="eyebrow">Explora</span><h2>Encuentra tu <span class="oro">pieza</span></h2>{sep()}
<p class="lead">Más de {len(P) // 100 * 100} piezas en oro laminado 18k para cada estilo y cada historia.</p><div class="cats">{cats}</div>
<div class="botones"><a class="btn btn-linea" href="/coleccion/">Ver toda la colección</a></div></div></section>
<section class="seccion alt"><div class="contenedor"><div class="centro"><span class="eyebrow">Lo más pedido</span><h2>Favoritas de <span class="oro">nuestros clientes</span></h2>{sep()}</div>
<div class="grid" style="margin-top:34px">{''.join(card(p) for p in destacados)}</div></div></section>
<section class="seccion noche"><div class="contenedor dos">
<div><span class="eyebrow">Colección especial</span><h2>Fe y <span class="oro">protección</span></h2>{sep()}
<p class="lead">Manillas y medallas de San Benito, la Virgen de Guadalupe, la Milagrosa y la Virgen del Carmen en oro laminado 18k. Para llevar tu fe contigo, todos los días.</p>
<div class="botones"><a class="btn btn-oro" href="/coleccion/fe-y-proteccion/">Ver fe y protección</a></div></div>
<div class="grid" style="grid-template-columns:repeat(2,1fr)">{''.join(card(p) for p in fe)}</div></div></section>
<section class="seccion"><div class="contenedor dos">
<div class="arco-foto"><img src="/assets/img/maria-jose.jpg" alt="María José, creadora de Casa Orus" loading="lazy" width="440" height="550" onerror="this.style.display='none'"><span class="respaldo" aria-hidden="true"><img src="/assets/img/logo-vertical-metal.svg" alt=""></span></div>
<div><span class="eyebrow">Detrás de cada pieza</span><h2>Nacida de un <span class="oro">talento temprano</span></h2>{sep()}
<p class="lead">Casa Orus es la visión de María José, una creadora con una mirada fresca, intuitiva y genuina. Desde muy temprano la fascinaron el brillo y la precisión, y hoy esa sensibilidad se convierte en joyas con alma.</p>
<p>Cada diseño nace de una idea sencilla: que una joya acompañe lo que importa. Una fe, un amor, un nuevo comienzo. Demostrando que el arte de la distinción no tiene edad.</p>
<div class="botones"><a class="btn btn-linea" href="/nuestra-historia/">Conoce nuestra historia</a><a class="btn btn-linea" href="/creaciones/">Creaciones Casa Orus</a></div></div></div></section>
<section class="seccion alt"><div class="contenedor centro"><span class="eyebrow">Nuestra esencia</span><h2>La esencia de <span class="oro">Casa Orus</span></h2>{sep()}{pilares()}</div></section>
<section class="seccion noche"><div class="contenedor centro"><span class="eyebrow">Garantía Casa Orus</span><h2>Tu joya, brillante <span class="oro">por 5 años</span></h2>{sep()}
<p class="lead">Plata ley 925 con tres capas de oro 18k. Libre de níquel e hipoalergénica.</p>
<div style="text-align:left">{pasos_garantia().replace('class="pasos"', 'class="pasos" style="color:var(--marfil)"').replace('<p>', '<p class="suave">')}</div>
<div class="botones"><a class="btn btn-linea" href="/garantia-y-cuidados/">Ver garantía y cuidados</a></div></div></section>
<section class="seccion"><div class="contenedor centro"><span class="eyebrow">Aprende</span><h2>Guías de <span class="oro">oro laminado</span></h2>{sep()}<div class="guias" style="text-align:left">{guias}</div></div></section>
<section class="seccion alt"><div class="contenedor"><div class="centro"><span class="eyebrow">Resolvemos tus dudas</span><h2>Preguntas <span class="oro">frecuentes</span></h2>{sep()}</div><div class="faq">{faq_html(FAQ_GEN)}</div></div></section>
<section class="seccion" style="padding-top:0;background:var(--pergamino)"><div class="contenedor"><div class="banda-aliados">
<div><span class="eyebrow">Aliados comerciales</span><h2 style="margin:0">¿Tienes un negocio?</h2><p class="lead" style="margin:10px 0 0">Vende oro laminado en tu tienda con consignación o compra mayorista.</p></div>
<a class="btn btn-oro" href="/aliados/">Conocer la alianza</a></div></div></section>
<section class="seccion noche"><div class="contenedor centro"><p class="cita">“Más que joyas, creamos historias.”</p>
<div class="botones"><a class="btn btn-linea" href="{IG}" rel="noopener">{ICON['ig']} Síguenos en Instagram @casa.orus</a></div></div></section>'''
    write('/', head('Casa Orus · Joyería en Oro Laminado 18k en Medellín', 'Joyería en oro laminado 18k hecha en Medellín: manillas tejidas a mano, cadenas, aretes y dijes. Sin níquel, 5 años de garantía. Pedidos por WhatsApp y envíos a Colombia.', '/', schema=sch) + body + foot())

def simple(path, title, desc, eyebrow, h1, content, schema=None, oscuro=False, noindex=False):
    items = [('Inicio', '/'), (re.sub('<.*?>', '', h1), None)]
    body = f'''<section class="cab-cat{' noche' if oscuro else ''}"><div class="contenedor">{migas(items)}<span class="eyebrow">{eyebrow}</span><h1>{h1}</h1></div></section>{content}'''
    write(path, head(title, desc[:160], path, schema=[bc_schema(items)] + (schema or []), noindex=noindex) + body + foot())

GUIAS = [
 ('como-saber-si-el-oro-laminado-es-bueno', 'Cómo saber si el oro laminado es bueno', 'Las 6 señales para reconocer una pieza de calidad antes de comprarla.',
  '''<p>No todo lo que brilla es igual. Cuando compras una joya en oro laminado, la diferencia entre una pieza que dura años y una que se pone oscura en semanas está en detalles que puedes revisar tú misma.</p>
<h2>1. Pregunta por el metal base</h2><p>El oro laminado es una capa de oro real unida a otro metal. Si ese metal base es de buena calidad, la pieza resiste mejor. En Casa Orus la base es <strong>plata ley 925</strong>, cubierta con tres capas de oro 18k.</p>
<h2>2. Que diga 18k</h2><p>El quilataje indica la pureza del oro de la capa. El 18k tiene un tono cálido y profundo, el que asociamos con la joyería fina.</p>
<h2>3. Sin níquel</h2><p>El níquel es la causa más común de alergias y manchas verdes en la piel. Una buena pieza de oro laminado lo dice claramente: libre de níquel, hipoalergénica.</p>
<h2>4. Peso y acabado</h2><p>Revisa que los eslabones estén bien cerrados, que el broche abra y cierre con firmeza y que no haya zonas opacas, rayas o bordes ásperos.</p>
<h2>5. Garantía por escrito</h2><p>Quien confía en su producto lo respalda. Nosotros damos <strong>5 años de garantía en el color</strong>; desconfía de quien no ofrece ninguna.</p>
<h2>6. Quién la vende</h2><p>Compra a joyerías que muestren su referencia, sus materiales y una forma clara de contacto y posventa.</p>
<blockquote>Una buena joya de oro laminado no es la más barata: es la que sigue brillando años después.</blockquote>'''),
 ('oro-laminado-se-pone-negro-como-limpiarlo', '¿El oro laminado se pone negro? Cómo limpiarlo y cuidarlo', 'Por qué se opaca, cómo limpiarlo en casa y los hábitos que alargan su brillo.',
  '''<p>Es la pregunta que más nos hacen. La respuesta corta: un oro laminado de calidad, bien cuidado, <strong>no se pone negro</strong>. Lo que sí puede pasar es que pierda brillo si lo exponemos a ciertos productos a diario.</p>
<h2>¿Por qué se opaca?</h2><ul><li>El cloro de piscinas y el agua de mar.</li><li>Perfumes, cremas y protector solar aplicados sobre la pieza.</li><li>El sudor intenso y los productos de limpieza.</li><li>Guardarla húmeda o junto a otras joyas que la rayen.</li></ul>
<h2>Cómo limpiarlo en casa</h2><ol><li>Prepara agua tibia con una gota de jabón neutro.</li><li>Sumerge la pieza unos segundos y frota suavemente con un paño de microfibra o un cepillo de dientes de cerdas suaves.</li><li>Enjuaga con agua limpia y <strong>seca muy bien</strong> con un paño suave.</li></ol>
<p>Evita bicarbonato, vinagre, crema dental o limpiadores abrasivos: rayan la capa de oro.</p>
<h2>Tres hábitos que cambian todo</h2><p><strong>Quítatela para bañarte. Perfume primero, joya después. Guárdala seca.</strong> Con eso, tu pieza conserva su color y tu garantía de 5 años queda protegida.</p>'''),
 ('diferencia-entre-oro-laminado-y-enchapado', 'Diferencia entre oro laminado, enchapado y bañado', 'Qué cambia entre cada técnica y cuál conviene según el uso que le darás.',
  '''<p>En las vitrinas verás tres palabras que parecen lo mismo pero no lo son. Entenderlas te ayuda a saber qué estás pagando.</p>
<table class="tabla"><thead><tr><th>Técnica</th><th>Cómo se hace</th><th>Durabilidad</th></tr></thead><tbody>
<tr><td>Bañado en oro</td><td>Una película muy fina de oro sobre el metal, normalmente por electrólisis.</td><td>Baja: puede desgastarse en semanas o meses.</td></tr>
<tr><td>Enchapado</td><td>Capa de oro algo más gruesa que el baño.</td><td>Media, depende del grosor y del metal base.</td></tr>
<tr><td>Oro laminado</td><td>Capas de oro unidas al metal base con calor y presión.</td><td>Alta: pensado para el uso diario durante años.</td></tr></tbody></table>
<h2>¿Y el metal de abajo?</h2><p>Importa tanto como la capa de oro. Un metal base de baja calidad puede oxidarse y causar alergias. Por eso en Casa Orus usamos <strong>plata ley 925 con tres capas de oro 18k</strong>, sin níquel.</p>
<h2>¿Cuál me conviene?</h2><p>Si quieres una pieza para llevar todos los días, el oro laminado es la opción con mejor relación entre precio, brillo y duración.</p>'''),
]

def build_pages(P):
    # Creaciones
    own = [p for p in P if p['propio']]
    simple('/creaciones/', 'Creaciones Casa Orus · Manillas y Anillos Tejidos a Mano en Medellín', 'Manillas tejidas, de protección y anillos hechos a mano por Casa Orus en Medellín, en oro laminado 18k. Piezas únicas y personalizadas.',
           'Hecho a mano en Medellín', 'Creaciones <span class="oro">Casa Orus</span>',
           f'<section class="contenedor" style="padding-bottom:90px"><p class="lead" style="margin-bottom:36px">Estas piezas nacen en nuestro taller: manillas y anillos tejidos uno a uno, con balines de oro laminado, hilo de protección y medallas. También las hacemos personalizadas.</p><div class="grid" id="lista">{"".join(card(p) for p in own)}</div>'
           f'<div class="botones centro" style="justify-content:center"><a class="btn btn-oro" href="{wa("Hola Casa Orus ✨ quiero una pieza personalizada.")}" rel="noopener">{ICON["wa"]} Pide una pieza personalizada</a></div></section>')
    # Historia
    simple('/nuestra-historia/', 'Nuestra Historia · Casa Orus, Joyería que Trasciende', 'Conoce la historia de Casa Orus: joyería en oro laminado 18k nacida en Medellín de un talento temprano y una mirada fresca.',
           'Nuestra historia', 'Joyería que <span class="oro">trasciende</span>',
           f'''<section class="seccion" style="padding-top:20px"><div class="contenedor dos">
<div class="arco-foto"><img src="/assets/img/maria-jose.jpg" alt="María José, creadora de Casa Orus" width="440" height="550" onerror="this.style.display='none'"><span class="respaldo" aria-hidden="true"><img src="/assets/img/logo-vertical-metal.svg" alt=""></span></div>
<div><span class="eyebrow">La creadora</span><h2>María José</h2>{sep()}
<p class="lead">Nacida de un talento innato y una fascinación temprana por el brillo y la precisión, Casa Orus es el reflejo de una visión audaz liderada por nuestra joven fundadora, María José.</p>
<p>Con una perspectiva fresca, intuitiva y genuina, ha sabido capturar la esencia de la elegancia contemporánea, demostrando que el arte de la distinción no tiene edad. Cada pieza refleja su sensibilidad por los detalles y el lujo sutil.</p>
<p>Lo que empezó tejiendo manillas para las personas cercanas hoy es una casa de joyería con identidad propia, que acompaña historias de fe, de amor y de nuevos comienzos.</p></div></div></section>
<section class="seccion alt"><div class="contenedor centro"><span class="eyebrow">Lo que nos mueve</span><h2>Nuestra <span class="oro">visión</span></h2>{sep()}
<p class="lead">Aspiramos a redefinir el lujo silencioso: joyas que no solo adornen, sino que cuenten historias y trasciendan generaciones.</p>{pilares()}</div></section>
<section class="seccion noche"><div class="contenedor centro"><p class="cita">“Más que joyas, creamos historias.”</p><div class="botones"><a class="btn btn-oro" href="/coleccion/">Ver la colección</a></div></div></section>''')
    # Garantía
    simple('/garantia-y-cuidados/', 'Garantía de 5 Años y Cuidados del Oro Laminado | Casa Orus', 'Garantía Casa Orus: 5 años por cambio de color en oro laminado 18k sobre plata ley 925. Aprende a cuidar tus joyas para que brillen siempre.',
           'Garantía Casa Orus', 'Garantía y <span class="oro">cuidados</span>',
           f'''<section class="contenedor" style="padding-bottom:30px"><p class="lead">Todas nuestras joyas están hechas en plata ley 925 con tres capas de oro 18k, libres de níquel e hipoalergénicas. Por eso las respaldamos con <strong>5 años de garantía en el color</strong>.</p>{pasos_garantia()}</section>
<section class="seccion alt"><div class="contenedor centro"><h2>Cuida tu <span class="oro">oro laminado</span></h2>{sep()}
<div class="pilares"><div class="pilar"><div class="medallon">{PICT['agua']}</div><h3>Sin agua</h3><p>Quítatela para bañarte, nadar o hacer ejercicio.</p></div><div class="pilar"><div class="medallon">{PICT['frasco']}</div><h3>Perfume primero</h3><p>Aplica perfume y cremas antes de ponerte la joya.</p></div><div class="pilar"><div class="medallon">{PICT['regalo']}</div><h3>Guárdala seca</h3><p>En su bolsita o estuche, lejos de la humedad.</p></div><div class="pilar"><div class="medallon">{PICT['destello']}</div><h3>Limpieza suave</h3><p>Agua tibia, jabón neutro y un paño suave.</p></div></div>
<div class="botones"><a class="btn btn-linea" href="/guias/oro-laminado-se-pone-negro-como-limpiarlo/">Guía completa de limpieza</a></div></div></section>
<section class="seccion"><div class="contenedor"><h2 class="centro">Condiciones</h2>{sep().replace('class="sep"','class="sep" style="margin:14px auto 26px"')}<div class="faq">
<details class="acord" open><summary>Qué cubre</summary><p>El cambio de color de la pieza con uso adecuado, durante 5 años desde la fecha de compra.</p></details>
<details class="acord"><summary>Qué no cubre</summary><p>Roturas, pérdidas, deformaciones y daños por mal uso, golpes o contacto con químicos.</p></details>
<details class="acord"><summary>Cómo hacerla efectiva</summary><p>Escríbenos por WhatsApp con tu certificado de garantía o el soporte de compra y fotos de la pieza. Te indicamos los siguientes pasos.</p></details></div></div></section>''')
    # FAQ
    simple('/preguntas-frecuentes/', 'Preguntas Frecuentes sobre Oro Laminado | Casa Orus', 'Resolvemos tus dudas sobre el oro laminado 18k, la garantía, los envíos, los pedidos y las piezas personalizadas de Casa Orus.',
           'Ayuda', 'Preguntas <span class="oro">frecuentes</span>', f'<section class="contenedor" style="padding-bottom:90px"><div class="faq" style="margin-top:0">{faq_html(FAQ_GEN)}</div></section>', schema=[faq_schema(FAQ_GEN)])
    # Regalos
    occ = [('Para el amor', 'amor', 'Corazones, iniciales y piezas para regalar a tu pareja.'), ('Fe y protección', 'fe', 'San Benito y la Virgen, para primera comunión, bautizo o confirmación.'), ('Con brillo', 'brillo', 'Piezas con circonias para una ocasión especial.'), ('Hechas a mano', 'casa-orus', 'Creaciones únicas tejidas en nuestro taller.')]
    blocks = ''
    for t, tag, d in occ:
        ps = [p for p in P if tag in p['tags']][:8]
        blocks += f'<section class="seccion" style="padding:50px 0"><div class="contenedor"><h2>{t}</h2><p class="lead">{d}</p><div class="grid" style="margin-top:26px">{"".join(card(p) for p in ps)}</div></div></section>'
    simple('/regalos/', 'Ideas de Regalo en Oro Laminado 18k | Casa Orus Medellín', 'Ideas de regalo en oro laminado 18k: para el amor, primera comunión, bautizo, amistad y ocasiones especiales. Te asesoramos por WhatsApp.',
           'Ideas de regalo', 'El regalo que <span class="oro">se queda</span>', f'<section class="contenedor"><p class="lead">Un regalo que no se guarda en un cajón: se lleva puesto. Te ayudamos a elegir por WhatsApp.</p></section>' + blocks)
    # Guías
    simple('/guias/', 'Guías de Oro Laminado: Cuidados, Calidad y Diferencias | Casa Orus', 'Aprende a elegir y cuidar tus joyas de oro laminado: cómo saber si es bueno, cómo limpiarlo y en qué se diferencia del enchapado.',
           'Aprende', 'Guías de <span class="oro">oro laminado</span>', f'<section class="contenedor" style="padding-bottom:90px"><div class="guias" style="margin-top:0">{"".join(f"<a class=\"guia\" href=\"/guias/{s}/\"><span class=\"eyebrow\">Guía</span><h3>{E(t)}</h3><p>{E(d)}</p><span>Leer guía →</span></a>" for s, t, d, _ in GUIAS)}</div></section>')
    for s, t, d, c in GUIAS:
        items = [('Inicio', '/'), ('Guías', '/guias/'), (t, None)]
        art = {'@context': 'https://schema.org', '@type': 'Article', 'headline': t, 'description': d, 'inLanguage': 'es-CO', 'datePublished': HOY, 'dateModified': HOY,
               'author': {'@type': 'Organization', 'name': 'Casa Orus'}, 'publisher': {'@id': DOM + '/#tienda'}, 'mainEntityOfPage': DOM + f'/guias/{s}/'}
        body = f'''<div class="contenedor" style="padding-top:28px">{migas(items)}</div><article class="articulo"><span class="eyebrow">Guía Casa Orus</span><h1 style="font-size:clamp(30px,4vw,44px)">{E(t)}</h1>{sep()}{c}
<div class="banda-aliados" style="margin-top:50px;padding:32px"><div><h3 style="margin:0 0 6px">¿Buscas una pieza que dure?</h3><p style="margin:0">Oro laminado 18k sobre plata 925, con 5 años de garantía.</p></div><a class="btn btn-oro" href="/coleccion/">Ver colección</a></div></article>'''
        write(f'/guias/{s}/', head(f'{t} | Casa Orus', d + ' Guía de Casa Orus, joyería en Medellín.', f'/guias/{s}/', schema=[bc_schema(items), art], typ='article') + body + foot())
    # Aliados
    simple('/aliados/', 'Vende Oro Laminado en tu Negocio | Aliados y Mayoristas Casa Orus', 'Incorpora joyería en oro laminado 18k a tu negocio con Casa Orus: consignación sin inversión inicial o compra mayorista, rotación de inventario y material publicitario.',
           'Alianza comercial', 'Incorpora oro laminado <span class="oro">a tu negocio</span>',
           f'''<section class="contenedor" style="padding-bottom:20px"><p class="lead">Amplía el portafolio de tu tienda con una línea de joyería en oro laminado que atrae nuevos clientes. Diseñamos un modelo flexible que se adapta a tu capacidad de inversión.</p></section>
<section class="seccion" style="padding-top:30px"><div class="contenedor"><div class="pilares" style="grid-template-columns:repeat(auto-fit,minmax(240px,1fr))">
<div class="pilar"><div class="medallon">{PICT['escudo']}</div><h3>Consignación</h3><p>Comienza sin inversión inicial: exhibe y vende, y recibe una comisión sobre el precio de venta al público.</p></div>
<div class="pilar"><div class="medallon">{PICT['oro']}</div><h3>Compra mayorista</h3><p>Inventario propio con mayor margen de utilidad y acceso a nuevas referencias y colecciones.</p></div>
<div class="pilar"><div class="medallon">{PICT['destello']}</div><h3>Rotación de inventario</h3><p>Aproximadamente cada dos meses cambias las referencias de menor salida por otras de igual valor.</p></div>
<div class="pilar"><div class="medallon">{PICT['regalo']}</div><h3>Material publicitario</h3><p>Fotos, videos e imágenes para WhatsApp y redes para vender también en línea.</p></div></div>
<div class="botones" style="justify-content:center"><a class="btn btn-oro" href="{wa('Hola Casa Orus ✨ quiero recibir la propuesta de alianza comercial para mi negocio.')}" rel="noopener">{ICON['wa']} Solicitar la propuesta completa</a></div></div></section>''')
    # Contacto
    simple('/contacto/', 'Contacto · Casa Orus Joyería en Medellín', 'Escríbenos por WhatsApp al +57 314 272 0023, por Instagram @casa.orus o al correo orusjoyeria1@gmail.com. Atendemos pedidos en Medellín y toda Colombia.',
           'Hablemos', 'Estamos para <span class="oro">ayudarte</span>',
           f'''<section class="contenedor" style="padding-bottom:90px"><p class="lead">Atendemos pedidos, asesoría para regalos y piezas personalizadas. Somos una joyería online con base en Medellín y enviamos a toda Colombia.</p>
<div class="pilares" style="grid-template-columns:repeat(auto-fit,minmax(240px,1fr))">
<div class="pilar"><div class="medallon">{ICON['wa']}</div><h3>WhatsApp</h3><p><a href="{wa('Hola Casa Orus ✨')}" rel="noopener">+57 314 272 0023</a></p></div>
<div class="pilar"><div class="medallon">{ICON['ig']}</div><h3>Instagram</h3><p><a href="{IG}" rel="noopener">@casa.orus</a></p></div>
<div class="pilar"><div class="medallon">{PICT['envio']}</div><h3>Correo</h3><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div></div></section>''', schema=[ORG])
    # Privacidad
    simple('/privacidad/', 'Política de Privacidad | Casa Orus', 'Política de tratamiento de datos personales de Casa Orus conforme a la Ley 1581 de 2012.', 'Legal', 'Política de <span class="oro">privacidad</span>',
           '''<section class="articulo" style="padding-top:0"><p>Casa Orus trata los datos personales que nos compartes (nombre, teléfono, correo y dirección de envío) únicamente para atender tus pedidos, consultas y garantías, de acuerdo con la Ley 1581 de 2012 y sus decretos reglamentarios.</p>
<p>Este sitio no tiene formularios ni cuentas de usuario: el contacto se realiza por WhatsApp, Instagram o correo electrónico. No vendemos ni cedemos tus datos a terceros.</p>
<p>Puedes conocer, actualizar, rectificar o solicitar la eliminación de tus datos escribiendo a orusjoyeria1@gmail.com.</p>
<p>Este sitio puede usar herramientas de analítica (como Google Analytics) para conocer de forma agregada cómo se usa la web.</p></section>''')
    # 404
    write('404.html', head('Página no encontrada | Casa Orus', 'La página que buscas no existe.', '/404.html', noindex=True) +
          f'<section class="seccion noche centro"><div class="contenedor"><span class="eyebrow">Error 404</span><h1>Esta página <span class="oro">no existe</span></h1>{sep()}<p class="lead">Pero tu próxima joya sí.</p><div class="botones"><a class="btn btn-oro" href="/coleccion/">Ver la colección</a><a class="btn btn-linea" href="/">Ir al inicio</a></div></div></section>' + foot())

# ---------------------------------------------------------------- recursos y SEO técnico
def assets():
    a = os.path.join(OUT, 'assets'); os.makedirs(a + '/img', exist_ok=True); os.makedirs(a + '/css', exist_ok=True); os.makedirs(a + '/js', exist_ok=True); os.makedirs(a + '/fonts', exist_ok=True)
    shutil.copy('src/estilos.css', a + '/css/estilos.css'); shutil.copy('src/sitio.js', a + '/js/sitio.js')
    cp = lambda s, d: shutil.copy(os.path.join(KIT, s), os.path.join(a, 'img', d))
    cp('01-logos/horizontal/svg/casa-orus-horizontal-oro-transparente.svg', 'logo-casa-orus.svg')
    cp('01-logos/vertical/svg/casa-orus-vertical-oro-metalico-transparente.svg', 'logo-vertical-metal.svg')
    cp('01-logos/isotipo/svg/casa-orus-isotipo-oro-transparente.svg', 'isotipo.svg')
    cp('01-logos/favicon/favicon.svg', 'favicon.svg'); cp('01-logos/favicon/apple-touch-icon-180.png', 'apple-touch-icon.png')
    cp('01-logos/favicon/favicon-192.png', 'icon-192.png'); cp('01-logos/favicon/favicon-512.png', 'icon-512.png')
    cp('07-banners-web/og-image-redes-1200x630.png', 'og-casa-orus.png')
    shutil.copy('src/img/maria-jose.jpg', a + '/img/maria-jose.jpg')
    shutil.copytree('src/img/creaciones', a + '/img/creaciones')
    shutil.copy(os.path.join(KIT, '01-logos/favicon/favicon.ico'), os.path.join(OUT, 'favicon.ico'))
    # fuentes en woff, recortadas a latín
    from fontTools import subset
    FS = [('/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyrepagella-regular.otf', 'pagella.woff'),
          ('/usr/share/fonts/truetype/google-fonts/Poppins-Light.ttf', 'poppins-300.woff'), ('/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf', 'poppins-400.woff'),
          ('/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf', 'poppins-500.woff'), ('/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf', 'poppins-700.woff'),
          ('/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf', 'lora-italic.woff')]
    for src, dst in FS:
        opts = subset.Options(); opts.flavor = 'woff'; opts.layout_features = ['kern', 'liga']; opts.name_IDs = ['*']
        f = subset.load_font(src, opts); s = subset.Subsetter(opts)
        s.populate(unicodes=list(range(0x20, 0x7F)) + list(range(0xA0, 0x180)) + [0x2013, 0x2014, 0x2018, 0x2019, 0x201C, 0x201D, 0x2022, 0x2026, 0x2192, 0x2726, 0x20AC])
        s.subset(f); subset.save_font(f, os.path.join(a, 'fonts', dst), opts)
    with open(os.path.join(OUT, 'site.webmanifest'), 'w') as f:
        json.dump({'name': 'Casa Orus', 'short_name': 'Casa Orus', 'start_url': '/', 'display': 'browser', 'background_color': '#190420', 'theme_color': '#190420',
                   'icons': [{'src': '/assets/img/icon-192.png', 'sizes': '192x192', 'type': 'image/png'}, {'src': '/assets/img/icon-512.png', 'sizes': '512x512', 'type': 'image/png'}]}, f)

def seo_files(P):
    urls = ['/', '/coleccion/', '/coleccion/fe-y-proteccion/'] + [f'/coleccion/{c[0]}/' for c in CATS] + ['/creaciones/', '/nuestra-historia/', '/garantia-y-cuidados/', '/preguntas-frecuentes/', '/regalos/', '/guias/', '/aliados/', '/contacto/', '/privacidad/'] + [f'/guias/{g[0]}/' for g in GUIAS]
    pri = lambda u: '1.0' if u == '/' else '0.9' if u.startswith('/coleccion') else '0.7'
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for u in urls: xml.append(f'<url><loc>{DOM}{u}</loc><lastmod>{HOY}</lastmod><priority>{pri(u)}</priority></url>')
    for p in P:
        xml.append(f'<url><loc>{DOM}/joya/{p["slug"]}/</loc><lastmod>{HOY}</lastmod><priority>0.6</priority><image:image><image:loc>{E(p["img"])}</image:loc></image:image></url>')
    xml.append('</urlset>')
    with open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8') as f: f.write('\n'.join(xml))
    with open(os.path.join(OUT, 'robots.txt'), 'w') as f: f.write(f'User-agent: *\nAllow: /\nDisallow: /404.html\n\nSitemap: {DOM}/sitemap.xml\n')
    # redirecciones desde la web anterior
    old = {'/shop': '/coleccion/', '/collection': '/coleccion/', '/gallery': '/creaciones/', '/about': '/nuestra-historia/', '/contact': '/contacto/',
           '/shop/manillas': '/coleccion/manillas-y-pulseras/', '/shop/cadenas': '/coleccion/cadenas-y-gargantillas/', '/shop/aretes': '/coleccion/aretes/', '/shop/anillos': '/coleccion/anillos/', '/shop/otros': '/coleccion/',
           '/category/Anillos': '/coleccion/anillos/', '/category/Cadenas': '/coleccion/cadenas-y-gargantillas/', '/category/Aretes': '/coleccion/aretes/', '/category/Manillas%20Tejidas': '/coleccion/manillas-y-pulseras/'}
    own_map = {'anillo-tejido-balin-liso1': 'anillo-tejido-balin-liso-4mm', 'anillo-tejido-balin-liso': 'anillo-tejido-balines-4mm', 'anillo-tejido-balines-italy': 'anillo-tejido-balines-italianos',
               'manilla-oso-t-balines-': 'manilla-oso-balines', 'manilla-verde-herraje-bola-de-fuego': 'manilla-verde-bola-de-fuego', 'manilla-roja-tejida-balines': 'manilla-roja-tejida-balines',
               'manilla-tejida-chakras-trebol': 'manilla-chakras-trebol', 'manilla-virgen-de-guadalupe': 'manilla-virgen-de-guadalupe', 'manilla-placa-personalizada': 'manilla-placa-personalizada',
               'face-serum-gxrcld': 'manilla-divino-nino', 'handmade-vase-slowpy': 'manilla-balin-liso-4mm', 'set-of-plates-cxlzwx': 'manilla-lotus', 'sunglasses-iubjnq': 'manilla-san-benito'}
    by_ref = {p['ref']: p['slug'] for p in P}
    resold = {'anillo-alianza-t55': '13009-T5.5', 'anillo-flicker-ajustable': '13102'}
    lines = ['# Casa Orus · configuración Apache (Hostinger)', 'Options -Indexes', 'DirectoryIndex index.html', 'ErrorDocument 404 /404.html', '',
             'RewriteEngine On', '# Forzar HTTPS y dominio sin www', 'RewriteCond %{HTTPS} off [OR]', 'RewriteCond %{HTTP_HOST} ^www\\. [NC]',
             'RewriteRule ^(.*)$ https://orusjoyeria.com/$1 [L,R=301]', '', '# Redirecciones de la web anterior']
    for a, b in old.items(): lines.append(f'Redirect 301 {a} {DOM}{b}')
    for a, b in own_map.items(): lines.append(f'Redirect 301 /product/{a} {DOM}/joya/{b}/')
    for a, r in resold.items():
        if r in by_ref: lines.append(f'Redirect 301 /product/{a} {DOM}/joya/{by_ref[r]}/')
    lines += ['RedirectMatch 301 ^/product/.*$ https://orusjoyeria.com/coleccion/', '', '# Caché y compresión',
              '<IfModule mod_expires.c>', 'ExpiresActive On', 'ExpiresByType text/css "access plus 1 year"', 'ExpiresByType application/javascript "access plus 1 year"',
              'ExpiresByType font/woff "access plus 1 year"', 'ExpiresByType image/svg+xml "access plus 1 year"', 'ExpiresByType image/png "access plus 1 year"',
              'ExpiresByType image/jpeg "access plus 1 year"', 'ExpiresByType image/webp "access plus 1 year"', 'ExpiresByType text/html "access plus 1 hour"', '</IfModule>',
              '<IfModule mod_deflate.c>', 'AddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml application/xml text/plain application/json', '</IfModule>',
              '', '# Cabeceras de seguridad', '<IfModule mod_headers.c>', 'Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"',
              'Header always set X-Content-Type-Options "nosniff"', 'Header always set X-Frame-Options "SAMEORIGIN"', 'Header always set Referrer-Policy "strict-origin-when-cross-origin"',
              'Header always set Permissions-Policy "geolocation=(), camera=(), microphone=()"', '</IfModule>', 'AddType font/woff .woff', 'AddType application/manifest+json .webmanifest']
    with open(os.path.join(OUT, '.htaccess'), 'w') as f: f.write('\n'.join(lines) + '\n')

def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    P = build_catalog()
    for c in CATS:
        first = next(p for p in P if p['cat'] == c[0] and not p['propio'])
        pref = {'manillas-y-pulseras': '55162', 'cadenas-y-gargantillas': '45036', 'aretes': '30014', 'dijes': '23319', 'anillos': '13102'}
        CAT_IMG[c[0]] = next((p for p in P if p['ref'] == pref.get(c[0])), first)
    assets()
    page_home(P); page_coleccion(P); page_fe(P)
    for c in CATS: page_cat(c[0], [p for p in P if p['cat'] == c[0]])
    import collections
    DUP.update(collections.Counter(p['nombre'] for p in P))
    for p in P: page_producto(p, P)
    build_pages(P); seo_files(P)
    with open(os.path.join(OUT, 'assets', 'catalogo.json'), 'w', encoding='utf-8') as f:
        json.dump([{k: p[k] for k in ('ref', 'nombre', 'cat', 'slug', 'img', 'tags', 'propio')} for p in P], f, ensure_ascii=False)
    n = sum(len(fs) for _, _, fs in os.walk(OUT))
    print('productos', len(P), '· archivos', n)

if __name__ == '__main__':
    main()
