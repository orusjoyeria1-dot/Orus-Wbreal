/* Casa Orus · interacción mínima del sitio */
(function () {
  'use strict';
  // Menú móvil
  var btn = document.querySelector('.abrir-menu'), nav = document.getElementById('nav');
  if (btn && nav) btn.addEventListener('click', function () {
    var a = nav.classList.toggle('abierto'); btn.setAttribute('aria-expanded', a ? 'true' : 'false');
  });

  // Respaldo de imágenes del catálogo: PERFIL.webp -> _1.webp -> marca
  window.orusImg = function (img) {
    var alt = img.getAttribute('data-alt');
    if (alt && img.src.indexOf(alt) === -1) { img.src = alt; return; }
    img.style.display = 'none';
    var f = img.parentNode.querySelector('.sin-foto'); if (f) f.style.display = 'flex';
  };
  document.querySelectorAll('img[data-alt]').forEach(function (img) {
    if (img.complete && img.naturalWidth === 0) window.orusImg(img);
  });

  // Galería de ficha
  var principal = document.querySelector('.galeria-principal img');
  document.querySelectorAll('.miniaturas button').forEach(function (b) {
    var im = b.querySelector('img');
    im.addEventListener('error', function () { b.remove(); });
    b.addEventListener('click', function () {
      principal.src = im.src;
      document.querySelectorAll('.miniaturas button').forEach(function (x) { x.setAttribute('aria-current', 'false'); });
      b.setAttribute('aria-current', 'true');
    });
  });

  // Filtros de listado (por subtipo) y buscador del catálogo
  var lista = document.getElementById('lista');
  if (lista) {
    var cards = Array.prototype.slice.call(lista.querySelectorAll('.card'));
    var contador = document.getElementById('contador');
    var input = document.getElementById('q');
    var activo = 'todo';
    function norm(s) { return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }
    function aplicar() {
      var q = norm(input ? input.value : '');
      var n = 0;
      cards.forEach(function (c) {
        var ok = (activo === 'todo' || (' ' + c.getAttribute('data-tags') + ' ').indexOf(' ' + activo + ' ') > -1)
          && (!q || norm(c.getAttribute('data-buscar')).indexOf(q) > -1);
        c.hidden = !ok; if (ok) n++;
      });
      if (contador) contador.textContent = n + (n === 1 ? ' pieza' : ' piezas');
    }
    document.querySelectorAll('.filtros .chip[data-f]').forEach(function (ch) {
      ch.addEventListener('click', function () {
        activo = ch.getAttribute('data-f');
        document.querySelectorAll('.filtros .chip[data-f]').forEach(function (x) { x.setAttribute('aria-pressed', x === ch ? 'true' : 'false'); });
        aplicar();
      });
    });
    if (input) {
      var p = new URLSearchParams(location.search).get('q'); if (p) input.value = p;
      input.addEventListener('input', aplicar);
      var form = input.closest('form'); if (form) form.addEventListener('submit', function (e) { e.preventDefault(); aplicar(); });
    }
    aplicar();
  }
})();
