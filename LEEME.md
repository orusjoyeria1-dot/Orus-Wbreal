# Casa Orus · Sitio web nuevo

Sitio estático (HTML, CSS y JS sin dependencias) generado a partir del catálogo del proveedor y de las piezas propias. 520 piezas, 8 categorías, colección "Fe y protección", 3 guías, páginas de marca y SEO técnico listo.

## Cómo publicarlo en Hostinger

1. Entra a hPanel → **Administrador de archivos** → carpeta `public_html` de orusjoyeria.com.
2. Haz una copia de seguridad de lo que haya y vacía la carpeta.
3. Sube el contenido de la carpeta **`publicar/`** (no la carpeta en sí), incluido el archivo oculto `.htaccess`. Lo más rápido: sube `publicar.zip` y usa "Extraer".
4. Abre https://orusjoyeria.com y revisa.
5. En Google Search Console envía `https://orusjoyeria.com/sitemap.xml`.

## Antes o justo después de publicar

- **Foto de María José:** ya incluida (`assets/img/maria-jose.jpg`).
- **Fotos de las creaciones propias:** ya incluidas en `assets/img/creaciones/` (WebP optimizado). Ya puedes cancelar Horizons cuando la web nueva esté publicada.
- **Analítica:** pega tu etiqueta de Google Analytics 4 y la verificación de Search Console donde lo indican los comentarios en `<head>` (archivo `build.py`, función `head`, y regenera; o pídemelo).
- **Fotos del catálogo:** se muestran enlazadas desde belatrizcolombia.com. Si el proveedor bloquea el enlazado externo, las tarjetas mostrarán el isotipo de Casa Orus en lugar de la foto. Para alojarlas en tu dominio basta con cambiar `IMG_BASE` en `fuente/catalogo.py`.

## Qué incluye

- **Inicio** por secciones: portada, banda de confianza, categorías, favoritas, fe y protección, historia, esencia, garantía, guías, preguntas frecuentes, aliados e Instagram.
- **Colección** completa con buscador (nombre o referencia) y filtros; 8 páginas de categoría con texto SEO y preguntas frecuentes; landing **Fe y protección**.
- **520 fichas de producto** con foto, título reescrito, referencia, medidas, botón **Pedir por WhatsApp** con la referencia ya escrita, garantía, cuidados y piezas relacionadas. Sin precios.
- **Páginas:** Creaciones Casa Orus, Nuestra historia, Garantía y cuidados, Preguntas frecuentes, Regalos, Guías (3 artículos), Aliados y mayoristas, Contacto, Privacidad, 404.
- **SEO:** title y meta únicos por página, URLs limpias, canonical, Open Graph, datos estructurados (JewelryStore, Product, BreadcrumbList, FAQPage, Article, WebSite con buscador), sitemap con imágenes, robots.txt, redirecciones 301 desde todas las URLs de la web anterior, HTTPS forzado, caché, compresión y cabeceras de seguridad (`.htaccess`).

## Para actualizar el catálogo

En `fuente/` está todo el generador. Con Python 3 y `fonttools` instalados: edita `data_raw.py` (añadir o quitar piezas) y ejecuta `python3 build.py`; el sitio nuevo queda en `dist/`. También puedes pedírmelo y lo regenero.

Piezas excluidas a propósito por marcas registradas o licencias: Atlético Nacional, Tío Rico, Krabs/Paul y la categoría Herrajes. Nombres de marcas de lujo en títulos (Gucci, Swarovski, Van Cleef, Cartier) se reemplazaron por descripciones genéricas.
