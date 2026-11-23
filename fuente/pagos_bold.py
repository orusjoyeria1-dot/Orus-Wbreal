# Módulo de pagos con Bold (botón de pagos, firma generada en el servidor con PHP)
import os, json

PAGAR_PHP = r'''<?php
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
'''

PAGAR_BODY = r'''<section class="cab-cat"><div class="contenedor"><span class="eyebrow">Compra segura con Bold</span><h1>Finaliza tu <span class="oro">compra</span></h1></div></section>
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
'''

CONFIG_PHP = r'''<?php
// ================================================================
// Casa Orus · Configuración de Bold
// 1) Entra a panel.bold.co → Integraciones → Botón de pagos.
// 2) Copia tus llaves y pégalas aquí ENTRE LAS COMILLAS.
//    Empieza con las llaves de PRUEBAS; cuando todo funcione, cámbialas por las de PRODUCCIÓN.
// 3) NUNCA compartas la llave secreta por chat, correo ni WhatsApp.
// ================================================================
return [
    'llave_identidad' => 'PEGA AQUÍ TU LLAVE DE IDENTIDAD',
    'llave_secreta'   => 'PEGA AQUÍ TU LLAVE SECRETA',
    'modo'            => 'pruebas',                    // cambia a 'produccion' cuando uses las llaves reales
    'correo_avisos'   => 'ventas@orusjoyeria.com',     // aquí te llega cada pedido con los datos de envío
];
'''

GRACIAS_BODY = r'''<section class="cab-cat"><div class="contenedor"><span class="eyebrow">Casa Orus</span><h1 id="g-titulo">Gracias por tu <span class="oro">compra</span></h1></div></section>
<section class="seccion"><div class="contenedor centro" style="max-width:640px">
<p class="lead" id="g-texto">Estamos confirmando tu pago.</p>
<p id="g-orden" class="nota"></p>
<div class="botones" style="justify-content:center"><a class="btn btn-oro" id="g-wa" href="https://wa.me/573142720023">Escríbenos por WhatsApp</a><a class="btn btn-linea" href="/coleccion/">Seguir viendo joyas</a></div>
<p class="nota" style="margin-top:24px">El envío es gratis a toda Colombia. Te confirmaremos por WhatsApp la guía de tu pedido.</p>
</div></section>
<script>(function(){var q=new URLSearchParams(location.search),o=q.get('bold-order-id')||'',s=(q.get('bold-tx-status')||'').toLowerCase();
var t=document.getElementById('g-titulo'),x=document.getElementById('g-texto');
if(s==='approved'){x.textContent='¡Tu pago fue aprobado! Ya estamos preparando tu joya con mucho cariño.';if(window.gtag)gtag('event','purchase',{transaction_id:o,currency:'COP'});}
else if(s==='rejected'||s==='failed'){t.innerHTML='Tu pago <span class="oro">no se completó</span>';x.textContent='No se realizó ningún cobro. Puedes intentarlo de nuevo o escribirnos y te ayudamos.';}
else if(s==='pending'||s==='processing'){x.textContent='Tu pago está en proceso. Te avisaremos apenas se confirme.';}
if(o){document.getElementById('g-orden').textContent='Número de pedido: '+o;document.getElementById('g-wa').href='https://wa.me/573142720023?text='+encodeURIComponent('Hola Casa Orus ✨ acabo de hacer el pedido '+o+' en la página.');}})();</script>
'''

CSS = '''
/* Pago Bold */
.pago{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:40px;align-items:start}
.pago-resumen{background:#fff;border:1px solid var(--linea, #e6d6c8);padding:24px;display:flex;flex-direction:column;gap:16px;position:sticky;top:110px}
.pago-resumen img{width:160px;height:160px;object-fit:cover;background:#f4ece6}
.pago-resumen h2{font-size:22px;margin:0}
.pago-total{list-style:none;margin:16px 0;padding:0}
.pago-total li{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(0,0,0,.08)}
.pago-total li.t{font-size:18px;border-bottom:0}
.pago-total .gratis{color:#2e7d32;text-transform:uppercase;letter-spacing:.08em}
.pago-caja{background:#fff;border:1px solid var(--linea, #e6d6c8);padding:28px}
.pago-caja h2{font-size:24px;margin-top:0}
.pago-form{display:grid;gap:14px}
.pago-form label{display:grid;gap:6px;font-size:14px;font-weight:500}
.pago-form input,.pago-form textarea{font:inherit;font-weight:400;padding:12px 14px;border:1px solid #cdbfb4;background:#fffdfb;border-radius:2px}
.pago-form input:focus,.pago-form textarea:focus{outline:2px solid var(--oro);border-color:var(--oro)}
.pago-dos{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.pago-error{background:#fdecea;border-left:3px solid #c62828;padding:10px 14px;margin-bottom:12px}
.pago-error p{margin:4px 0}
.pago-boton{margin:22px 0}
.btn-comprar{min-width:220px}
@media(max-width:820px){.pago{grid-template-columns:1fr}.pago-resumen{position:static;flex-direction:row}.pago-resumen img{width:110px;height:110px}.pago-dos{grid-template-columns:1fr}}
'''

def construir(OUT, P, head, foot):
    os.makedirs(os.path.join(OUT, 'pagar'), exist_ok=True)
    os.makedirs(os.path.join(OUT, 'pagos'), exist_ok=True)
    os.makedirs(os.path.join(OUT, 'gracias'), exist_ok=True)
    cab = head('Finaliza tu compra | Casa Orus', 'Compra segura con Bold. Envío gratis a toda Colombia.', '/pagar/', noindex=True)
    with open(os.path.join(OUT, 'pagar', 'index.php'), 'w', encoding='utf-8') as f:
        f.write(PAGAR_PHP + cab + PAGAR_BODY + foot())
    with open(os.path.join(OUT, 'gracias', 'index.html'), 'w', encoding='utf-8') as f:
        f.write(head('Gracias por tu compra | Casa Orus', 'Confirmación de tu pedido en Casa Orus.', '/gracias/', noindex=True) + GRACIAS_BODY + foot())
    prods = {p['slug']: {'nombre': p['nombre'], 'ref': '' if p['propio'] else p['ref'], 'precio': p['precio'], 'img': p['img']} for p in P if p['precio']}
    with open(os.path.join(OUT, 'pagos', 'productos.json'), 'w', encoding='utf-8') as f:
        json.dump(prods, f, ensure_ascii=False)
    with open(os.path.join(OUT, 'pagos', '.htaccess'), 'w') as f:
        f.write('# Carpeta privada: nadie puede abrir estos archivos desde el navegador\nRequire all denied\n')
    # config.php solo se crea en el paquete de "primera instalación" para no borrar las llaves ya pegadas
    with open(os.path.join(OUT, 'pagos', 'config.ejemplo.php'), 'w', encoding='utf-8') as f:
        f.write(CONFIG_PHP)
