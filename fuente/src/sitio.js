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

  // Filtros de listado (tipo + subfiltro), orden por precio y buscador
  var lista = document.getElementById('lista');
  if (lista) {
    var cards = Array.prototype.slice.call(lista.querySelectorAll('.card'));
    cards.forEach(function (c, i) { c.setAttribute('data-i', i); });
    var contador = document.getElementById('contador');
    var input = document.getElementById('q');
    var orden = document.getElementById('orden');
    var tipo = 'todo', activo = 'todo';
    function norm(s) { return (s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, ''); }
    function tiene(c, t) { return t === 'todo' || (' ' + c.getAttribute('data-tags') + ' ').indexOf(' ' + t + ' ') > -1; }
    function aplicar() {
      var q = norm(input ? input.value : ''), n = 0;
      cards.forEach(function (c) {
        var ok = tiene(c, tipo) && tiene(c, activo) && (!q || norm(c.getAttribute('data-buscar')).indexOf(q) > -1);
        c.hidden = !ok; if (ok) n++;
      });
      // subfiltros sin piezas dentro del tipo elegido se ocultan
      document.querySelectorAll('.filtros .chip[data-f]').forEach(function (ch) {
        var f = ch.getAttribute('data-f');
        if (f === 'todo') return;
        ch.hidden = !cards.some(function (c) { return tiene(c, tipo) && tiene(c, f); });
      });
      if (contador) contador.textContent = n + (n === 1 ? ' pieza' : ' piezas');
    }
    function ordenar() {
      var v = orden ? orden.value : 'rel';
      var arr = cards.slice().sort(function (a, b) {
        if (v === 'rel') return a.getAttribute('data-i') - b.getAttribute('data-i');
        var pa = +a.getAttribute('data-precio') || (v === 'asc' ? 1e12 : -1), pb = +b.getAttribute('data-precio') || (v === 'asc' ? 1e12 : -1);
        return v === 'asc' ? pa - pb : pb - pa;
      });
      arr.forEach(function (c) { lista.appendChild(c); });
    }
    function grupo(sel, set) {
      document.querySelectorAll(sel).forEach(function (ch) {
        ch.addEventListener('click', function () {
          set(ch);
          document.querySelectorAll(sel).forEach(function (x) { x.setAttribute('aria-pressed', x === ch ? 'true' : 'false'); });
          aplicar();
        });
      });
    }
    grupo('.filtros .chip[data-t]', function (ch) {
      tipo = ch.getAttribute('data-t'); activo = 'todo';
      document.querySelectorAll('.filtros .chip[data-f]').forEach(function (x) { x.setAttribute('aria-pressed', x.getAttribute('data-f') === 'todo' ? 'true' : 'false'); });
    });
    grupo('.filtros .chip[data-f]', function (ch) { activo = ch.getAttribute('data-f'); });
    if (orden) orden.addEventListener('change', ordenar);
    if (input) {
      var p = new URLSearchParams(location.search).get('q'); if (p) input.value = p;
      input.addEventListener('input', aplicar);
      var form = input.closest('form'); if (form) form.addEventListener('submit', function (e) { e.preventDefault(); aplicar(); });
    }
    aplicar();
  }
})();
