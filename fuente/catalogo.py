"""Normaliza el catálogo del proveedor y las piezas propias en una lista de productos."""
import re, unicodedata, hashlib
import json, os
from data_raw import RAW, OWN, OWN_PRECIOS
PRECIOS = json.load(open(os.path.join(os.path.dirname(__file__), 'precios', 'detal.json')))

IMG_BASE = 'https://belatrizcolombia.com/app/public/template/shop/img/img_productos/'  # cambiar a '/assets/catalogo/' si se alojan localmente

CATS = [
 # slug, nombre, nombre corto, descripción corta, title SEO, meta
 ('manillas-y-pulseras', 'Manillas y pulseras', 'Manillas', 'Tejidas a mano y eslabones italianos',
  'Manillas y Pulseras en Oro Laminado 18k | Casa Orus Medellín',
  'Manillas tejidas a mano y pulseras en oro laminado 18k: hilo rojo, San Benito, cubanas, italianas y más. 5 años de garantía. Envíos a toda Colombia.'),
 ('cadenas-y-gargantillas', 'Cadenas y gargantillas', 'Cadenas', 'Cubanas, franco, singapur, militar',
  'Cadenas en Oro Laminado 18k para Hombre y Mujer | Casa Orus',
  'Cadenas y gargantillas en oro laminado 18k: cubana, franco, singapur, militar, veneciana y más, de 40 a 65 cm. Pide por WhatsApp. Envíos a Colombia.'),
 ('aretes', 'Aretes', 'Aretes', 'Topos, candongas y ear cuffs',
  'Aretes en Oro Laminado 18k | Topos y Candongas | Casa Orus',
  'Topos, candongas y aretes en oro laminado 18k con circonias y diseños exclusivos. Hipoalergénicos, sin níquel y con garantía. Envíos a toda Colombia.'),
 ('dijes', 'Dijes', 'Dijes', 'Medallas, cruces, iniciales y amuletos',
  'Dijes en Oro Laminado 18k | Medallas, Cruces e Iniciales | Casa Orus',
  'Dijes en oro laminado 18k: Virgen de Guadalupe, San Benito, Divino Niño, cruces, iniciales y amuletos. Combínalos con tu cadena. Envíos a Colombia.'),
 ('anillos', 'Anillos', 'Anillos', 'Tejidos, alianzas y ajustables',
  'Anillos en Oro Laminado 18k | Tejidos y Ajustables | Casa Orus',
  'Anillos tejidos a mano, alianzas y anillos ajustables en oro laminado 18k. Sin níquel y con 5 años de garantía en el color. Envíos a toda Colombia.'),
 ('rosarios-y-cruceros', 'Rosarios, cruceros y denarios', 'Rosarios', 'Para llevar tu fe contigo',
  'Rosarios, Cruceros y Denarios en Oro Laminado 18k | Casa Orus',
  'Cruceros de la Virgen de Guadalupe y San Benito, rosarios y denarios en oro laminado 18k. Piezas de fe para el día a día. Envíos a toda Colombia.'),
 ('tobilleras', 'Tobilleras', 'Tobilleras', 'Delicadas, para el verano',
  'Tobilleras en Oro Laminado 18k | Casa Orus Medellín',
  'Tobilleras en oro laminado 18k: tejido chino, escalera, circonias y ojo turco, con extensor. Resistentes y delicadas. Envíos a toda Colombia.'),
 ('conjuntos', 'Conjuntos', 'Conjuntos', 'Cadena y aretes a juego',
  'Conjuntos de Joyería en Oro Laminado 18k | Casa Orus',
  'Conjuntos de cadena y aretes en oro laminado 18k, listos para regalar. Hipoalergénicos y con garantía. Envíos a toda Colombia.'),
]
CAT = {c[0]: c for c in CATS}

FE = ['virgen', 'guadalupe', 'san benito', 'benito', 'milagrosa', 'cruz', 'cristo', 'divino', 'angel', 'ángel', 'san miguel', 'espiritu', 'espíritu',
      'fatima', 'fátima', 'carmen', 'rostro', 'inri', 'crucificado', 'madero', 'escapulario', 'ichtus', 'filipenses', 'buen pastor', 'jesus', 'jesús',
      'rosa mistica', 'crucero', 'rosario', 'denario', 'benedictus', 'redentor', 'guadalupana', 'gracias', 'dios', 'ankh', 'niño', 'paloma', 'blessed',
      'ojo turco', 'nazar', 'hamsa', 'fátima', 'mano de', 'virgen niña']
AMOR = ['corazon', 'corazón', 'love', 'heart', 'amour', 'amore', 'coeur', 'amare', 'pasion', 'pasión', 'romantic']
BRILLO = ['circon', 'crystal', 'cristal', 'brightness', 'destello', 'sparkle', 'shine', 'ice', 'emerald', 'esmerald', 'halo', 'pave', 'charm crystal', 'eclat', 'helix', 'dynasty', 'swarovski']

def slugify(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return re.sub(r'-+', '-', s)

TYPE = {'C': 'Cadena', 'G': 'Gargantilla', 'A': 'Aretes', 'P': 'Pulsera', 'T': 'Tobillera', 'D': 'Dije', 'H': 'Dije'}

REPL = [
    (r'\bIT\b', ''), (r'\bItaly\b', 'italiana'), (r'\bitaly\b', 'italiana'), (r'\bCms?\b', 'cm'), (r'\bCMS\b', 'cm'), (r'\bcms\b', 'cm'),
    (r'(\d)\s*Mm\b', r'\1 mm'), (r'(\d)mm\b', r'\1 mm'), (r'(\d)cm\b', r'\1 cm'), (r'(\d)Cm\b', r'\1 cm'), (r'\bMm\b', 'mm'),
    (r'\+\s*Extensor\b', 'con extensor'), (r'\+\s*Ext\b', 'con extensor'), (r'(?<!con )\bExtensor\b', 'con extensor'), (r'-?\s*extensor\b', ' con extensor'),
    (r'\bPrismc\b', 'prismática'), (r'\bDelg\.?', 'delgada'), (r'\bT\. Chino\b', 'tejido chino'), (r'\bB\. Frances\b', 'balín francés'),
    (r'\bV\. Guadalupe\b', 'Virgen de Guadalupe'), (r'\bCirconias\b', 'circonias'), (r'\bcirconias-', 'circonias '),
    (r'\bGucci\b', 'eslabón G'), (r'(\d),(\d)', r'\1.\2'), (r'\s+', ' '),
]
COLORES = {'ROJO': 'rojo', 'NEGRO': 'negro', 'NEGRA': 'negra', 'VERDE': 'verde', 'CRISTAL': 'cristal', 'AZUL': 'azul', 'COLORES': 'colores', 'COLORS': 'colores', 'NACAR': 'nácar', 'AZULTOMMY': 'azul'}

def clean_title(raw, src):
    t = raw.strip()
    m = re.match(r'^([CGAPTDH])\.?\s+(.*)$', t)
    prefix = None
    if m and src not in ('conjuntos',) and not t.startswith('Conjunto'):
        prefix, t = m.group(1), m.group(2)
    elif m and src == 'conjuntos':
        t = m.group(2)
    if src == 'religiosos' and t.startswith('C Crucero'):
        t = t[2:]
    for a, b in REPL:
        t = re.sub(a, b, t)
    for k, v in COLORES.items():
        t = re.sub(r'\b' + k + r'\b', v, t)
    t = t.strip(' -')
    # tipo de pieza
    low = t.lower()
    if src == 'anillos':
        name = t
    elif src == 'conjuntos':
        name = t if low.startswith('conjunto') else 'Conjunto ' + t
    elif src == 'religiosos':
        name = t
    elif src == 'tobilleras' and low.startswith('tobillera'):
        name = t
    else:
        typ = TYPE.get(prefix) or {'cadenas': 'Cadena', 'pulseras': 'Pulsera', 'gargantillas': 'Gargantilla', 'aretes': 'Aretes', 'tobilleras': 'Tobillera', 'dijes': 'Dije'}.get(src, '')
        if typ == 'Aretes':
            if low.startswith('topo'):
                typ, t = 'Topos', t[4:].strip()
            elif low.startswith('candongas'):
                typ, t = 'Candongas', t[9:].strip()
            elif low.startswith('candonga'):
                typ, t = 'Candongas', t[8:].strip()
            elif low.startswith('ear cuff'):
                typ, t = 'Ear cuff', t[8:].strip()
        name = (typ + ' ' + t).strip()
    name = re.sub(r'\s+', ' ', name).strip()
    name = re.sub(r'(con )+con extensor', 'con extensor', name)
    name = re.sub(r'\bBalin\b', 'balín', name).replace('Balón', 'balón').replace('Balon', 'balón')
    w = name.split(' ')
    small = {'Con','De','Del','La','El','Y','Para','En','Los','Las'}
    w = [x.lower() if (i > 0 and x in small) else x for i, x in enumerate(w)]
    name = ' '.join(w)
    return name[0].upper() + name[1:]

def site_cat(src, prefix_letter):
    return {'cadenas': 'cadenas-y-gargantillas', 'gargantillas': 'cadenas-y-gargantillas', 'pulseras': 'manillas-y-pulseras',
            'aretes': 'aretes', 'dijes': 'dijes', 'anillos': 'anillos', 'tobilleras': 'tobilleras', 'conjuntos': 'conjuntos',
            'religiosos': 'rosarios-y-cruceros'}.get(src) or ('aretes' if prefix_letter == 'A' else 'dijes')

FE_ESTRICTO = ['san benito', 'benito', 'benedictus', 'virgen', 'guadalupe', 'guadalupana', 'milagrosa', 'immaculata', 'carmen', 'fatima', 'fátima', 'rosa mistica', 'señora', 'maría']

def tags_for(name, cat):
    low = name.lower(); tags = []
    if any(k in low for k in FE_ESTRICTO) and 'mano de' not in low: tags.append('fe')
    if any(k in low for k in AMOR): tags.append('amor')
    if any(k in low for k in BRILLO): tags.append('brillo')
    if 'italiana' in low: tags.append('italiana')
    if cat == 'aretes':
        tags.append('topos' if low.startswith('topos') else 'candongas' if low.startswith('candongas') else 'otros-aretes')
    if cat == 'cadenas-y-gargantillas':
        m = re.search(r'(\d{2})(?:\.\d)? cm', low)
        if m:
            L = int(m.group(1)); tags.append('corta' if L <= 45 else 'larga')
        if low.startswith('gargantilla'): tags.append('gargantilla')
    if cat == 'dijes' and low.startswith('dije inicial'): tags.append('iniciales')
    return tags

def medidas(name):
    out = {}
    m = re.search(r'(\d+(?:\.\d+)?) cm', name)
    if m: out['Largo'] = m.group(1).replace('.', ',') + ' cm'
    m = re.search(r'(\d+(?:\.\d+)?) mm', name)
    if m: out['Grosor / tamaño'] = m.group(1).replace('.', ',') + ' mm'
    if 'extensor' in name.lower(): out['Cierre'] = 'Con extensor ajustable'
    if 'ajustable' in name.lower(): out['Talla'] = 'Ajustable'
    m = re.search(r'\bT(\d+(?:\.\d+)?)\b', name)
    if m: out['Talla'] = m.group(1).replace('.', ',')
    return out

INTRO = {
 'cadenas-y-gargantillas': ['Una cadena pensada para llevarse todos los días, sola o con tu dije favorito.', 'Eslabones bien definidos y un brillo que no pasa desapercibido.', 'Ligera, firme y fácil de combinar con el resto de tus piezas.'],
 'manillas-y-pulseras': ['Una pulsera cómoda para el día a día, que combina con todo.', 'Brillo discreto en la muñeca, para llevar sola o en conjunto.', 'Pensada para acompañarte desde la mañana hasta la noche.'],
 'aretes': ['Aretes livianos que iluminan el rostro sin pesar.', 'Un detalle que eleva cualquier look, del diario a la ocasión especial.', 'Cómodos para todo el día y fáciles de combinar.'],
 'dijes': ['Un dije con significado, para llevar cerca del corazón.', 'Combínalo con tu cadena favorita y haz que cuente tu historia.', 'Pequeño en tamaño, grande en lo que representa.'],
 'anillos': ['Un anillo para llevar todos los días, solo o combinado.', 'Cómodo, ligero y con el brillo del oro laminado.'],
 'rosarios-y-cruceros': ['Una pieza de fe para llevar contigo a donde vayas.', 'Para quienes encuentran protección y calma en sus creencias.'],
 'tobilleras': ['Una tobillera delicada para lucir con sandalias y en vacaciones.', 'Fina, ajustable y pensada para el uso diario.'],
 'conjuntos': ['Un conjunto a juego, listo para regalar o regalarte.', 'Piezas que se complementan para un look completo.'],
}

def describe(name, cat, ref):
    h = int(hashlib.md5(ref.encode()).hexdigest(), 16)
    opts = INTRO[cat]
    s1 = opts[h % len(opts)]
    extra = ''
    low = name.lower()
    if 'fe' in tags_for(name, cat):
        extra = ' Un símbolo de fe y protección, ideal también para regalar.'
    elif 'amor' in tags_for(name, cat):
        extra = ' Un regalo con significado para alguien especial.'
    elif 'circon' in low or 'cristal' in low:
        extra = ' Sus circonias aportan un destello elegante.'
    return f'{name} en oro laminado 18k. {s1}{extra}'

def build():
    prods, seen = [], set()
    for src, block in RAW.items():
        if src == 'letras':
            continue
        for line in block.strip().splitlines():
            title, ref = [x.strip() for x in line.rsplit('|', 1)]
            if ref in seen:
                continue
            seen.add(ref)
            m = re.match(r'^([CGAPTDH])\.?\s', title)
            pl = m.group(1) if m else None
            cat = site_cat(src, pl)
            name = clean_title(title, src)
            folder = ref
            prods.append(dict(ref=ref, nombre=name, cat=cat, origen=src, propio=False, it=bool(re.search(r'\bIT\b|italy', title, re.I)),
                              img=IMG_BASE + folder + '/PERFIL.webp', img2=IMG_BASE + folder + '/' + folder + '_1.webp',
                              galeria=[IMG_BASE + folder + '/PERFIL.webp'] + [IMG_BASE + folder + f'/{folder}_{i}.webp' for i in (1, 2, 3)]))
    # Iniciales agrupadas por familia
    estilos = {'23360': 'clásica', '23370': 'con circonias', '24360': 'script', '25360': 'mayúscula', '26360': 'minimal'}
    for fam, letras in RAW['letras'].items():
        L = letras.split()
        ref = f'{fam}-{L[0]}'
        prods.append(dict(ref=fam, nombre=f'Dije inicial {estilos[fam]}', cat='dijes', origen='dijes', propio=False, variantes=L,
                          img=IMG_BASE + ref + '/PERFIL.webp', img2=IMG_BASE + ref + '/' + ref + '_1.webp',
                          galeria=[IMG_BASE + f'{fam}-{x}/PERFIL.webp' for x in L[:4]]))
    # Piezas propias
    for slug, name, kind, img, desc in OWN:
        cat = 'anillos' if kind == 'anillos' else 'manillas-y-pulseras'
        prods.append(dict(ref='CO-' + slug.upper()[:18], nombre=name, cat=cat, origen='propio', propio=True, slug=slug,
                          img=img, img2='', galeria=[img], desc_propia=desc))
    for p in prods:
        p.setdefault('slug', slugify(p['nombre']) + ('' if p['propio'] else '-' + slugify(p['ref'])))
        p['tags'] = tags_for(p['nombre'], p['cat']) + (['casa-orus'] if p['propio'] else [])
        if p.get('it') and 'italiana' not in p['tags']: p['tags'].append('italiana')
        if p['propio']:
            p['tags'] += ['hecho-a-mano']
            if any(k in p['nombre'].lower() for k in ['benito', 'guadalupe']): p['tags'].append('fe')
        p['medidas'] = medidas(p['nombre'])
        p['desc'] = (p['nombre'] + ' en oro laminado 18k, hecha a mano por Casa Orus en Medellín. ' + p['desc_propia']) if p['propio'] else describe(p['nombre'], p['cat'], p['ref'])
    fam = {'23360': '23360-P', '23370': '23370-C', '24360': '24360-E', '25360': '25360-E', '26360': '26360-B'}
    for p in prods:
        p['precio'] = OWN_PRECIOS.get(p.get('slug')) if p['propio'] else PRECIOS.get(fam.get(p['ref'], p['ref']))
        # tipo dentro de manillas y pulseras
        if p['cat'] == 'manillas-y-pulseras':
            p['tags'].append('manillas' if (p['propio'] or 'hilo' in p['nombre'].lower()) else 'pulseras')
    # piezas descontinuadas: el proveedor ya no las tiene en su catálogo detal
    prods = [p for p in prods if p['propio'] or p['precio']]
    slugs = [p['slug'] for p in prods]
    assert len(slugs) == len(set(slugs)), 'slugs duplicados'
    return prods

if __name__ == '__main__':
    P = build()
    from collections import Counter
    print(len(P), Counter(p['cat'] for p in P))
    for p in P[::37]: print(p['ref'], '|', p['nombre'], '|', p['tags'], p['medidas'])
