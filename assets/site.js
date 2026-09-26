// Textos de la interfaz según el idioma de la página (<html lang>).
var EN = (document.documentElement.lang || '').slice(0, 2) === 'en';
var T = EN ? {
  abrir: 'Open menu', cerrar: 'Close menu',
  correo: 'Email', alta: 'Subscribe me to Canary GPS news', altaAsunto: 'News subscription',
  altaOk: 'Your email program will open to confirm the subscription.'
} : {
  abrir: 'Abrir menú', cerrar: 'Cerrar menú',
  correo: 'Correo', alta: 'Quiero recibir las novedades de Canary GPS', altaAsunto: 'Alta en novedades',
  altaOk: 'Se abrirá tu programa de correo para confirmar la suscripción.'
};

// Menú responsive
(function () {
  var btn = document.getElementById('navToggle');
  var nav = document.getElementById('mainNav');
  if (!btn || !nav) return;
  btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', String(open));
    btn.setAttribute('aria-label', open ? T.cerrar : T.abrir);
  });
  nav.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') nav.classList.remove('open');
  });
})();

// Menú principal con desbordamiento: los elementos que no caben se recogen
// en «Más», y vuelven al menú al ensanchar la ventana.
(function () {
  var nav = document.getElementById('mainNav');
  if (!nav) return;
  var lista = nav.querySelector('ul');
  var mas = lista.querySelector('.nav-mas');
  var drop = mas && mas.querySelector('.nav-drop');
  var cta = lista.querySelector('.cta');
  var wrap = document.querySelector('.site-header .wrap');
  if (!mas || !drop || !wrap) return;
  var movil = window.matchMedia('(max-width:1080px)');

  function restaurar() {
    while (drop.firstElementChild) lista.insertBefore(drop.firstElementChild, mas);
    mas.hidden = true;
    cerrar();
  }
  function cerrar() {
    mas.classList.remove('abierto');
    mas.querySelector('button').setAttribute('aria-expanded', 'false');
  }
  function ajustar() {
    restaurar();
    if (movil.matches) return;
    var items = Array.prototype.filter.call(
      lista.children, function (li) { return li !== mas && li !== cta; }
    );
    // Se recogen desde el final; «Inicio» no se mueve nunca.
    var i = items.length - 1;
    while (wrap.scrollWidth > wrap.clientWidth + 1 && i >= 1) {
      mas.hidden = false;
      drop.insertBefore(items[i], drop.firstChild);
      i--;
    }
    if (!drop.children.length) { mas.hidden = true; return; }
    // Si la página actual ha quedado recogida, se marca «Más».
    mas.classList.toggle('tiene-activo', !!drop.querySelector('a.active'));
  }

  mas.querySelector('button').addEventListener('click', function (e) {
    e.stopPropagation();
    var abierto = mas.classList.toggle('abierto');
    this.setAttribute('aria-expanded', String(abierto));
  });
  document.addEventListener('click', function (e) {
    if (!mas.contains(e.target)) cerrar();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') cerrar();
  });

  var pendiente;
  window.addEventListener('resize', function () {
    clearTimeout(pendiente);
    pendiente = setTimeout(ajustar, 120);
  });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(ajustar);
  ajustar();
})();

// Botón de volver arriba.
(function () {
  var boton = document.getElementById('irArriba');
  if (!boton) return;
  var visible = false;
  function revisar() {
    var debe = window.scrollY > 600;
    if (debe !== visible) { visible = debe; boton.hidden = !debe; }
  }
  boton.addEventListener('click', function () {
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
  });
  window.addEventListener('scroll', revisar, { passive: true });
  revisar();
})();

// Formularios de contacto y de afiliados: el sitio es estático, así que componen
// un correo con cada campo rellenado (etiqueta: valor).
(function () {
  document.querySelectorAll('form.js-correo').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var lineas = [];
      var nombre = '';
      Array.prototype.forEach.call(form.elements, function (el) {
        if (!el.name || el.type === 'checkbox' || el.type === 'submit') return;
        var valor = el.value.trim();
        if (!valor) return;
        var etiqueta = form.querySelector('label[for="' + el.id + '"]');
        lineas.push((etiqueta ? etiqueta.textContent.trim() : el.name) + ': ' + valor);
        if (el.name === 'f-nombre') nombre = valor;
      });
      var url = 'mailto:' + form.dataset.to +
        '?subject=' + encodeURIComponent(form.dataset.asunto + ' — ' + (nombre || 'web')) +
        '&body=' + encodeURIComponent(lineas.join('\n'));
      var msg = form.querySelector('.form-msg');
      if (msg) msg.classList.add('show');
      window.location.href = url;
    });
  });
})();

(function () {
  var form = document.getElementById('newsForm');
  if (!form) return;
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var correo = form.elements.email.value.trim();
    var url = 'mailto:' + form.dataset.to +
      '?subject=' + encodeURIComponent(T.altaAsunto) +
      '&body=' + encodeURIComponent(T.alta + '\n' + T.correo + ': ' + correo);
    var ok = form.querySelector('.news-ok');
    if (!ok) {
      ok = document.createElement('p');
      ok.className = 'news-ok';
      ok.setAttribute('role', 'status');
      form.appendChild(ok);
    }
    ok.textContent = T.altaOk;
    ok.classList.add('show');
    window.location.href = url;
  });
})();
