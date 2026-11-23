<?php
// ================================================================
// Casa Orus · Página de pago con Bold
// La llave secreta vive en /pagos/config.php (no accesible desde la web).
// ================================================================
declare(strict_types=1);
date_default_timezone_set('America/Bogota');
header('X-Robots-Tag: noindex, nofollow');
$RAIZ = dirname(__DIR__);
$cfgArchivo = file_exists($RAIZ . '/pagos/config.php') ? $RAIZ . '/pagos/config.php' : $RAIZ . '/pagos/config.ejemplo.php';
$cfg = require $cfgArchivo;
$productos = json_decode((string)file_get_contents($RAIZ . '/pagos/productos.json'), true) ?: [];
function h($s) { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }
function cop($n) { return '$' . number_format((int)$n, 0, ',', '.'); }

$slug = preg_replace('/[^a-z0-9\-]/', '', $_GET['p'] ?? $_POST['p'] ?? '');
$prod = $productos[$slug] ?? null;
$listo = trim($cfg['llave_identidad']) !== '' && trim($cfg['llave_secreta']) !== '' && strpos($cfg['llave_secreta'], 'PEGA') === false;
$errores = [];
$pedido = null;

if ($prod && $_SERVER['REQUEST_METHOD'] === 'POST' && ($_POST['empresa'] ?? '') === '') {
    $d = [];
    foreach (['nombre' => 80, 'celular' => 20, 'correo' => 120, 'cedula' => 20, 'direccion' => 160, 'barrio' => 80, 'ciudad' => 60, 'departamento' => 60, 'notas' => 300] as $k => $max) {
        $d[$k] = mb_substr(trim(strip_tags((string)($_POST[$k] ?? ''))), 0, $max);
    }
    $d['celular'] = preg_replace('/[^0-9]/', '', $d['celular']);
    if (mb_strlen($d['nombre']) < 3) $errores[] = 'Escribe tu nombre completo.';
    if (strlen($d['celular']) < 10) $errores[] = 'Escribe un celular válido de 10 dígitos.';
    if ($d['correo'] !== '' && !filter_var($d['correo'], FILTER_VALIDATE_EMAIL)) $errores[] = 'Revisa tu correo electrónico.';
    if (mb_strlen($d['direccion']) < 5) $errores[] = 'Escribe la dirección de entrega.';
    if (mb_strlen($d['ciudad']) < 3) $errores[] = 'Escribe la ciudad.';
    if (mb_strlen($d['departamento']) < 3) $errores[] = 'Escribe el departamento.';
    if (!$errores) {
        $orden = 'ORUS-' . date('ymdHis') . '-' . strtoupper(bin2hex(random_bytes(2)));
        $monto = (int)$prod['precio'];               // el precio sale del servidor, nunca del navegador
        $firma = hash('sha256', $orden . $monto . 'COP' . $cfg['llave_secreta']);
        $pedido = ['orden' => $orden, 'monto' => $monto, 'firma' => $firma, 'datos' => $d];
        // Registro del pedido (para saber a dónde enviar)
        $linea = [date('Y-m-d H:i:s'), $orden, $prod['nombre'], $prod['ref'], $monto, $d['nombre'], $d['celular'], $d['correo'], $d['cedula'],
                  $d['direccion'], $d['barrio'], $d['ciudad'], $d['departamento'], $d['notas'], $cfg['modo']];
        $f = @fopen($RAIZ . '/pagos/pedidos.csv', 'a');
        if ($f) { fputcsv($f, $linea, ';'); fclose($f); }
        if (!empty($cfg['correo_avisos'])) {
            $cuerpo = "Nuevo pedido iniciado en orusjoyeria.com (pago pendiente de confirmar en Bold)\n\n"
                . "Pedido: $orden\nProducto: {$prod['nombre']} (Ref. {$prod['ref']})\nValor: " . cop($monto) . " COP\n\n"
                . "Cliente: {$d['nombre']}\nCelular: {$d['celular']}\nCorreo: {$d['correo']}\nCédula: {$d['cedula']}\n"
                . "Dirección: {$d['direccion']} {$d['barrio']}\nCiudad: {$d['ciudad']}, {$d['departamento']}\nNotas: {$d['notas']}\n";
            @mail($cfg['correo_avisos'], "Pedido web $orden - {$prod['nombre']}", $cuerpo, "From: tienda@orusjoyeria.com\r\nContent-Type: text/plain; charset=UTF-8");
        }
    }
}
?>
<!DOCTYPE html>
<html lang="es-CO">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Finaliza tu compra | Casa Orus</title>
<meta name="description" content="Compra segura con Bold. Envío gratis a toda Colombia.">
<link rel="canonical" href="https://orusjoyeria.com/pagar/">
<meta name="robots" content="noindex, follow">
<meta property="og:type" content="website"><meta property="og:site_name" content="Casa Orus">
<meta property="og:title" content="Finaliza tu compra | Casa Orus"><meta property="og:description" content="Compra segura con Bold. Envío gratis a toda Colombia.">
<meta property="og:url" content="https://orusjoyeria.com/pagar/"><meta property="og:image" content="https://orusjoyeria.com/assets/img/og-casa-orus.png">
<meta property="og:locale" content="es_CO"><meta name="twitter:card" content="summary_large_image">
<meta name="geo.region" content="CO-ANT"><meta name="geo.placename" content="Medellín">
<meta name="theme-color" content="#190420">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/pagella.woff" as="font" type="font/woff" crossorigin>
<link rel="preconnect" href="https://belatrizcolombia.com">
<link rel="stylesheet" href="/assets/css/estilos.css?v=2026-11-23">
<!-- Google Search Console: pega aquí la etiqueta de verificación -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-S0NSFPG255"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-S0NSFPG255');
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href*="wa.me"]');if(a)gtag('event','contacto_whatsapp',{link_url:a.href,page_path:location.pathname});});</script>

</head>
<body>
<a class="salto" href="#contenido">Saltar al contenido</a>
<div class="barra envio-gratis" role="note" aria-label="Envío gratis a toda Colombia en todas tus compras"><div class="mq" aria-hidden="true"><div class="mq-pista"><span class="mq-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.5 6.5h11v9h-11z"/><path d="M13.5 9.5h4l3 3.2v2.8h-7"/><circle cx="6.5" cy="17" r="1.8"/><circle cx="17" cy="17" r="1.8"/></svg><b>ENVÍO GRATIS A TODA COLOMBIA</b><i>✦</i>En todas tus compras<i>✦</i></span><span class="mq-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.5 6.5h11v9h-11z"/><path d="M13.5 9.5h4l3 3.2v2.8h-7"/><circle cx="6.5" cy="17" r="1.8"/><circle cx="17" cy="17" r="1.8"/></svg><b>ENVÍO GRATIS A TODA COLOMBIA</b><i>✦</i>En todas tus compras<i>✦</i></span><span class="mq-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.5 6.5h11v9h-11z"/><path d="M13.5 9.5h4l3 3.2v2.8h-7"/><circle cx="6.5" cy="17" r="1.8"/><circle cx="17" cy="17" r="1.8"/></svg><b>ENVÍO GRATIS A TODA COLOMBIA</b><i>✦</i>En todas tus compras<i>✦</i></span><span class="mq-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.5 6.5h11v9h-11z"/><path d="M13.5 9.5h4l3 3.2v2.8h-7"/><circle cx="6.5" cy="17" r="1.8"/><circle cx="17" cy="17" r="1.8"/></svg><b>ENVÍO GRATIS A TODA COLOMBIA</b><i>✦</i>En todas tus compras<i>✦</i></span><span class="mq-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.5 6.5h11v9h-11z"/><path d="M13.5 9.5h4l3 3.2v2.8h-7"/><circle cx="6.5" cy="17" r="1.8"/><circle cx="17" cy="17" r="1.8"/></svg><b>ENVÍO GRATIS A TODA COLOMBIA</b><i>✦</i>En todas tus compras<i>✦</i></span><span class="mq-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.5 6.5h11v9h-11z"/><path d="M13.5 9.5h4l3 3.2v2.8h-7"/><circle cx="6.5" cy="17" r="1.8"/><circle cx="17" cy="17" r="1.8"/></svg><b>ENVÍO GRATIS A TODA COLOMBIA</b><i>✦</i>En todas tus compras<i>✦</i></span></div><div class="mq-pista"><span class="mq-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.5 6.5h11v9h-11z"/><path d="M13.5 9.5h4l3 3.2v2.8h-7"/><circle cx="6.5" cy="17" r="1.8"/><circle cx="17" cy="17" r="1.8"/></svg><b>ENVÍO GRATIS A TODA COLOMBIA</b><i>✦</i>En todas tus compras<i>✦</i></span><span class="mq-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.5 6.5h11v9h-11z"/><path d="M13.5 9.5h4l3 3.2v2.8h-7"/><circle cx="6.5" cy="17" r="1.8"/><circle cx="17" cy="17" r="1.8"/></svg><b>ENVÍO GRATIS A TODA COLOMBIA</b><i>✦</i>En todas tus compras<i>✦</i></span><span class="mq-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.5 6.5h11v9h-11z"/><path d="M13.5 9.5h4l3 3.2v2.8h-7"/><circle cx="6.5" cy="17" r="1.8"/><circle cx="17" cy="17" r="1.8"/></svg><b>ENVÍO GRATIS A TODA COLOMBIA</b><i>✦</i>En todas tus compras<i>✦</i></span><span class="mq-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.5 6.5h11v9h-11z"/><path d="M13.5 9.5h4l3 3.2v2.8h-7"/><circle cx="6.5" cy="17" r="1.8"/><circle cx="17" cy="17" r="1.8"/></svg><b>ENVÍO GRATIS A TODA COLOMBIA</b><i>✦</i>En todas tus compras<i>✦</i></span><span class="mq-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.5 6.5h11v9h-11z"/><path d="M13.5 9.5h4l3 3.2v2.8h-7"/><circle cx="6.5" cy="17" r="1.8"/><circle cx="17" cy="17" r="1.8"/></svg><b>ENVÍO GRATIS A TODA COLOMBIA</b><i>✦</i>En todas tus compras<i>✦</i></span><span class="mq-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.5 6.5h11v9h-11z"/><path d="M13.5 9.5h4l3 3.2v2.8h-7"/><circle cx="6.5" cy="17" r="1.8"/><circle cx="17" cy="17" r="1.8"/></svg><b>ENVÍO GRATIS A TODA COLOMBIA</b><i>✦</i>En todas tus compras<i>✦</i></span></div></div></div>
<header class="cabecera"><div class="contenedor">
<a class="logo" href="/" aria-label="Casa Orus, inicio"><img src="/assets/img/logo-casa-orus.svg" alt="Casa Orus · Joyería que trasciende" width="180" height="52"></a>
<nav class="nav" id="nav" aria-label="Principal"><ul class="menu"><li><a href="/">Inicio</a></li><li><a href="/coleccion/">Colección</a></li><li><a href="/coleccion/manillas-y-pulseras/">Manillas</a></li><li><a href="/coleccion/cadenas-y-gargantillas/">Cadenas</a></li><li><a href="/coleccion/aretes/">Aretes</a></li><li><a href="/coleccion/dijes/">Dijes</a></li><li><a href="/creaciones/">Casa Orus</a></li><li><a href="/nuestra-historia/">Historia</a></li><li><a href="/guias/">Guías</a></li></ul></nav>
<div class="acciones">
<a class="icono-btn" href="/coleccion/#buscar" aria-label="Buscar en la colección"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/></svg></a>
<a class="icono-btn" href="https://wa.me/573142720023?text=Hola%20Casa%20Orus%20%E2%9C%A8%20quiero%20informaci%C3%B3n%20sobre%20sus%20joyas." aria-label="Escribir por WhatsApp" rel="noopener"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.2a9.7 9.7 0 0 0-8.3 14.8L2.4 21.8l4.9-1.3A9.7 9.7 0 1 0 12 2.2zm0 17.7c-1.5 0-3-.4-4.2-1.2l-.3-.2-2.9.8.8-2.8-.2-.3A8 8 0 1 1 12 19.9zm4.4-6c-.2-.1-1.4-.7-1.7-.8s-.4-.1-.5.1-.6.8-.8.9-.3.2-.5 0a6.6 6.6 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.1 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.5-.4h-.5a.9.9 0 0 0-.6.3 2.7 2.7 0 0 0-.9 2c0 1.2.9 2.4 1 2.5s1.7 2.6 4.2 3.7c1.6.7 2.2.7 3 .6.5-.1 1.4-.6 1.6-1.1s.2-1 .1-1.1-.2-.2-.4-.3z"/></svg></a>
<button class="icono-btn abrir-menu" aria-controls="nav" aria-expanded="false" aria-label="Abrir menú"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
</div></div></header>
<main id="contenido">
<section class="cab-cat"><div class="contenedor"><span class="eyebrow">Compra segura con Bold</span><h1>Finaliza tu <span class="oro">compra</span></h1></div></section>
<section class="seccion" style="padding-top:8px"><div class="contenedor pago">
<?php if (!$prod): ?>
  <div class="pago-caja"><h2>No encontramos esta joya</h2><p>Vuelve a la colección y elige la pieza que quieres comprar.</p><p><a class="btn btn-oro" href="/coleccion/">Ver colección</a></p></div>
<?php elseif (!$listo): ?>
  <div class="pago-caja"><h2>El pago en línea estará disponible muy pronto</h2><p>Mientras tanto, haz tu pedido por WhatsApp y te enviamos un link de pago seguro.</p>
  <p><a class="btn btn-oro" href="https://wa.me/573142720023?text=<?= rawurlencode('Hola Casa Orus ✨ quiero comprar "' . $prod['nombre'] . '" de ' . cop($prod['precio'])) ?>">Pedir por WhatsApp</a></p></div>
<?php else: ?>
  <aside class="pago-resumen">
    <img src="<?= h($prod['img']) ?>" alt="<?= h($prod['nombre']) ?>" referrerpolicy="no-referrer" width="160" height="160">
    <div><h2><?= h($prod['nombre']) ?></h2><?php if ($prod['ref']): ?><p class="nota">Ref. <?= h($prod['ref']) ?></p><?php endif; ?>
    <ul class="pago-total"><li><span>Joya</span><b><?= cop($prod['precio']) ?></b></li><li><span>Envío</span><b class="gratis">Gratis</b></li><li class="t"><span>Total</span><b><?= cop($prod['precio']) ?> COP</b></li></ul>
    <p class="nota">Oro laminado 18k sobre plata ley 925 · 5 años de garantía en el color.</p></div>
  </aside>
  <div class="pago-caja">
  <?php if ($pedido): $d = $pedido['datos']; ?>
    <h2>Paso 2 de 2 · Pago seguro</h2>
    <p>Pedido <b><?= h($pedido['orden']) ?></b>. Enviaremos tu joya a <b><?= h($d['direccion']) ?>, <?= h($d['ciudad']) ?></b>.</p>
    <p>Haz clic en el botón para pagar con tarjeta, PSE, Nequi, Daviplata o QR. El pago lo procesa <b>Bold</b>, una plataforma vigilada por la Superintendencia Financiera.</p>
    <div class="pago-boton">
    <script
      data-bold-button="dark-L"
      data-api-key="<?= h($cfg['llave_identidad']) ?>"
      data-order-id="<?= h($pedido['orden']) ?>"
      data-currency="COP"
      data-amount="<?= (int)$pedido['monto'] ?>"
      data-integrity-signature="<?= h($pedido['firma']) ?>"
      data-description="<?= h(mb_substr($prod['nombre'] . ' · Casa Orus', 0, 100)) ?>"
      data-redirection-url="https://orusjoyeria.com/gracias/"
      data-customer-data='<?= h(json_encode(array_filter(['email' => $d['correo'], 'fullName' => $d['nombre'], 'phone' => $d['celular'], 'dialCode' => '+57', 'documentNumber' => $d['cedula'], 'documentType' => $d['cedula'] ? 'CC' : '']), JSON_UNESCAPED_UNICODE)) ?>'
      data-billing-address='<?= h(json_encode(['address' => trim($d['direccion'] . ' ' . $d['barrio']), 'city' => $d['ciudad'], 'state' => $d['departamento'], 'country' => 'CO'], JSON_UNESCAPED_UNICODE)) ?>'
      data-extra-data-1="<?= h($prod['ref']) ?>"
    ></script>
    </div>
    <p class="nota"><a href="?p=<?= h($slug) ?>">← Corregir mis datos de envío</a></p>
  <?php else: ?>
    <h2>Paso 1 de 2 · Datos de envío</h2>
    <?php if ($errores): ?><div class="pago-error"><?php foreach ($errores as $e): ?><p><?= h($e) ?></p><?php endforeach; ?></div><?php endif; ?>
    <form method="post" class="pago-form" novalidate>
      <input type="hidden" name="p" value="<?= h($slug) ?>">
      <label class="salto">Empresa<input name="empresa" tabindex="-1" autocomplete="off"></label>
      <label>Nombre completo*<input name="nombre" required autocomplete="name" value="<?= h($_POST['nombre'] ?? '') ?>"></label>
      <div class="pago-dos"><label>Celular*<input name="celular" required inputmode="tel" autocomplete="tel" placeholder="300 123 4567" value="<?= h($_POST['celular'] ?? '') ?>"></label>
      <label>Cédula<input name="cedula" inputmode="numeric" value="<?= h($_POST['cedula'] ?? '') ?>"></label></div>
      <label>Correo (para enviarte el comprobante)<input name="correo" type="email" autocomplete="email" value="<?= h($_POST['correo'] ?? '') ?>"></label>
      <label>Dirección de entrega*<input name="direccion" required autocomplete="street-address" placeholder="Calle, número, apto / casa" value="<?= h($_POST['direccion'] ?? '') ?>"></label>
      <label>Barrio o conjunto<input name="barrio" value="<?= h($_POST['barrio'] ?? '') ?>"></label>
      <div class="pago-dos"><label>Ciudad*<input name="ciudad" required autocomplete="address-level2" value="<?= h($_POST['ciudad'] ?? '') ?>"></label>
      <label>Departamento*<input name="departamento" required autocomplete="address-level1" value="<?= h($_POST['departamento'] ?? '') ?>"></label></div>
      <label>Notas para tu pedido<textarea name="notas" rows="2" placeholder="Talla, letra, mensaje de regalo…"><?= h($_POST['notas'] ?? '') ?></textarea></label>
      <button class="btn btn-oro" type="submit">Continuar al pago</button>
      <p class="nota">Al continuar aceptas nuestra <a href="/politica-de-devoluciones/">política de devoluciones</a> y el tratamiento de tus datos según la <a href="/privacidad/">política de privacidad</a>.</p>
    </form>
  <?php endif; ?>
  </div>
<?php endif; ?>
</div></section>
<?php if ($pedido): ?><script src="https://checkout.bold.co/library/boldPaymentButton.js"></script><?php endif; ?>
</main>
<footer class="pie"><div class="contenedor">
<div class="pie-grid">
<div><img src="/assets/img/logo-casa-orus.svg" alt="Casa Orus" width="190" height="55" style="height:55px;width:auto;margin-bottom:18px">
<p>Joyería en oro laminado 18k hecha con amor en Medellín. Más que joyas, creamos historias.</p>
<a class="icono-btn" href="https://www.instagram.com/casa.orus/" aria-label="Instagram de Casa Orus" rel="noopener"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="4" y="4" width="16" height="16" rx="4.5"/><circle cx="12" cy="12" r="3.6"/><circle cx="17" cy="7" r=".8" fill="currentColor"/></svg></a></div>
<div><h4>Colección</h4><ul><li><a href="/coleccion/manillas-y-pulseras/">Manillas y pulseras</a></li><li><a href="/coleccion/cadenas-y-gargantillas/">Cadenas y gargantillas</a></li><li><a href="/coleccion/aretes/">Aretes</a></li><li><a href="/coleccion/dijes/">Dijes</a></li><li><a href="/coleccion/anillos/">Anillos</a></li><li><a href="/coleccion/rosarios-y-cruceros/">Rosarios, cruceros y denarios</a></li><li><a href="/coleccion/fe-y-proteccion/">Fe y protección</a></li></ul></div>
<div><h4>Casa Orus</h4><ul><li><a href="/nuestra-historia/">Nuestra historia</a></li><li><a href="/creaciones/">Creaciones Casa Orus</a></li><li><a href="/regalos/">Regalos</a></li><li><a href="/guias/">Guías</a></li><li><a href="/aliados/">Aliados y mayoristas</a></li></ul></div>
<div><h4>Atención</h4><ul><li><a href="https://wa.me/573142720023?text=Hola%20Casa%20Orus%20%E2%9C%A8" rel="noopener">WhatsApp +57 314 272 0023</a></li><li><a href="mailto:orusjoyeria1@gmail.com">orusjoyeria1@gmail.com</a></li><li><a href="/garantia-y-cuidados/">Garantía y cuidados</a></li><li><a href="/preguntas-frecuentes/">Preguntas frecuentes</a></li><li><a href="/contacto/">Contacto</a></li></ul></div>
</div>
<div class="pie-base"><span>© 2026 Casa Orus · Joyería que trasciende · Medellín, Colombia</span><span><a href="/politica-de-devoluciones/">Devoluciones y cambios</a> · <a href="/privacidad/">Política de privacidad</a></span></div>
</div></footer>
<a class="wa-flotante" href="https://wa.me/573142720023?text=Hola%20Casa%20Orus%20%E2%9C%A8%20quiero%20informaci%C3%B3n%20sobre%20sus%20joyas." aria-label="Escríbenos por WhatsApp" rel="noopener"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.2a9.7 9.7 0 0 0-8.3 14.8L2.4 21.8l4.9-1.3A9.7 9.7 0 1 0 12 2.2zm0 17.7c-1.5 0-3-.4-4.2-1.2l-.3-.2-2.9.8.8-2.8-.2-.3A8 8 0 1 1 12 19.9zm4.4-6c-.2-.1-1.4-.7-1.7-.8s-.4-.1-.5.1-.6.8-.8.9-.3.2-.5 0a6.6 6.6 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.1 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.5-.4h-.5a.9.9 0 0 0-.6.3 2.7 2.7 0 0 0-.9 2c0 1.2.9 2.4 1 2.5s1.7 2.6 4.2 3.7c1.6.7 2.2.7 3 .6.5-.1 1.4-.6 1.6-1.1s.2-1 .1-1.1-.2-.2-.4-.3z"/></svg></a>
<script src="/assets/js/sitio.js?v=2026-11-23" defer></script>
</body></html>