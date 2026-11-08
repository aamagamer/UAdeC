/* =========================================================
   Dirección de Planeación · UAdeC — Interacciones del sitio
   JavaScript puro, sin dependencias. Compatible con CSP estricta
   (sin eval, sin innerHTML con datos del usuario, sin handlers inline).
   ========================================================= */
(function () {
  'use strict';

  /* ---- Configuración editable ---- */
  var CONFIG = {
    // Correo que recibe los mensajes del formulario de contacto
    contactEmail: 'planeacion@uadec.edu.mx',
    // Versión de la política de cookies: si cambia, se vuelve a pedir el consentimiento
    consentVersion: 1,
    consentKey: 'dp_consent'
  };

  var $ = function (sel, ctx) { return (ctx || document).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fmt = new Intl.NumberFormat('es-MX');

  /* ---- Año en el pie ---- */
  $$('[data-year]').forEach(function (el) { el.textContent = String(new Date().getFullYear()); });

  /* ---- Header al hacer scroll + botón subir ---- */
  var header = $('.site-header');
  var toTop = $('.to-top');
  var ticking = false;
  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (header) header.classList.toggle('is-scrolled', y > 8);
    if (toTop) toTop.classList.toggle('is-visible', y > 600);
    ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { window.requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
  });

  /* ---- Navegación móvil ---- */
  var navToggle = $('.nav-toggle');
  var desktop = window.matchMedia('(min-width:1080px)');
  function closeNav() {
    document.body.classList.remove('nav-open');
    if (navToggle) navToggle.setAttribute('aria-expanded', 'false');
  }
  if (navToggle) {
    navToggle.addEventListener('click', function () {
      var open = document.body.classList.toggle('nav-open');
      navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
  desktop.addEventListener && desktop.addEventListener('change', closeNav);

  /* ---- Submenús ---- */
  $$('.has-sub').forEach(function (li) {
    var btn = $('button', li);
    var timer;
    function set(open) {
      li.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    }
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      set(!li.classList.contains('is-open'));
    });
    li.addEventListener('mouseenter', function () { if (desktop.matches) { clearTimeout(timer); set(true); } });
    li.addEventListener('mouseleave', function () { if (desktop.matches) { timer = setTimeout(function () { set(false); }, 180); } });
    li.addEventListener('focusout', function (e) { if (desktop.matches && !li.contains(e.relatedTarget)) set(false); });
  });
  document.addEventListener('click', function (e) {
    $$('.has-sub.is-open').forEach(function (li) {
      if (desktop.matches && !li.contains(e.target)) { li.classList.remove('is-open'); $('button', li).setAttribute('aria-expanded', 'false'); }
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    $$('.has-sub.is-open').forEach(function (li) {
      li.classList.remove('is-open');
      var b = $('button', li); b.setAttribute('aria-expanded', 'false'); b.focus();
    });
    if (document.body.classList.contains('nav-open')) { closeNav(); navToggle.focus(); }
  });

  /* ---- Contadores y barras ---- */
  function animateCount(el) {
    var target = parseFloat(el.getAttribute('data-count'));
    var suffix = el.getAttribute('data-suffix') || '';
    var prefix = el.getAttribute('data-prefix') || '';
    if (isNaN(target)) return;
    if (reduceMotion) { el.textContent = prefix + fmt.format(target) + suffix; return; }
    var start = null, dur = 1600;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = prefix + fmt.format(Math.round(target * eased)) + suffix;
      if (p < 1) window.requestAnimationFrame(step);
    }
    window.requestAnimationFrame(step);
  }
  function fillBar(el) {
    var v = parseFloat(el.getAttribute('data-value'));
    var max = parseFloat(el.getAttribute('data-max')) || 100;
    if (!isNaN(v)) el.style.width = Math.max(2, Math.min(100, (v / max) * 100)) + '%';
  }

  /* ---- Aparición al hacer scroll ---- */
  function activate(el) {
    el.classList.add('is-in');
    if (el.hasAttribute('data-count')) animateCount(el);
    if (el.classList.contains('bar-fill')) fillBar(el);
    $$('[data-count]', el).forEach(animateCount);
    $$('.bar-fill', el).forEach(fillBar);
  }
  var observed = $$('.reveal, [data-count], .bar-fill');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { activate(en.target); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    observed.forEach(function (el) {
      // los elementos dentro de un .reveal se activan junto con su contenedor
      if (!el.classList.contains('reveal') && el.closest('.reveal')) return;
      io.observe(el);
    });
  } else {
    observed.forEach(activate);
  }

  /* ---- Pestañas (numeralia) ---- */
  $$('[role="tablist"]').forEach(function (list) {
    var tabs = $$('[role="tab"]', list);
    function select(tab, focus) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
        var panel = document.getElementById(t.getAttribute('aria-controls'));
        if (panel) {
          panel.hidden = !on;
          if (on) { $$('.bar-fill', panel).forEach(fillBar); $$('[data-count]', panel).forEach(animateCount); $$('.reveal', panel).forEach(function (r) { r.classList.add('is-in'); }); }
        }
      });
      if (focus) tab.focus();
      if (history.replaceState) history.replaceState(null, '', '#' + tab.getAttribute('aria-controls'));
    }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(t, false); });
      t.addEventListener('keydown', function (e) {
        var n = null;
        if (e.key === 'ArrowRight') n = tabs[(i + 1) % tabs.length];
        if (e.key === 'ArrowLeft') n = tabs[(i - 1 + tabs.length) % tabs.length];
        if (e.key === 'Home') n = tabs[0];
        if (e.key === 'End') n = tabs[tabs.length - 1];
        if (n) { e.preventDefault(); select(n, true); }
      });
    });
    var fromHash = location.hash && tabs.filter(function (t) { return '#' + t.getAttribute('aria-controls') === location.hash; })[0];
    if (fromHash) select(fromHash, false);
  });

  /* ---- Visor de imágenes ---- */
  var triggers = $$('[data-lightbox]');
  if (triggers.length && typeof HTMLDialogElement === 'function') {
    var dlg = document.createElement('dialog');
    dlg.className = 'lightbox';
    dlg.setAttribute('aria-label', 'Imagen ampliada');
    var closeBtn = document.createElement('button');
    closeBtn.className = 'lightbox-close';
    closeBtn.type = 'button';
    closeBtn.setAttribute('aria-label', 'Cerrar imagen');
    var svgNS = 'http://www.w3.org/2000/svg';
    var s = document.createElementNS(svgNS, 'svg'); var u = document.createElementNS(svgNS, 'use');
    u.setAttribute('href', (document.body.getAttribute('data-icons') || 'assets/img/icons.svg') + '#i-x');
    s.appendChild(u); s.setAttribute('aria-hidden', 'true'); closeBtn.appendChild(s);
    var img = document.createElement('img'); img.decoding = 'async';
    var cap = document.createElement('p');
    dlg.appendChild(closeBtn); dlg.appendChild(img); dlg.appendChild(cap);
    document.body.appendChild(dlg);
    closeBtn.addEventListener('click', function () { dlg.close(); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
    triggers.forEach(function (t) {
      t.addEventListener('click', function () {
        var inner = $('img', t);
        img.src = t.getAttribute('data-lightbox');
        img.alt = inner ? inner.alt : '';
        cap.textContent = t.getAttribute('data-caption') || (inner ? inner.alt : '');
        dlg.showModal();
      });
    });
  }

  /* ---- Consentimiento de cookies ---- */
  var banner = $('#cookie-banner');
  function readConsent() {
    try {
      var c = JSON.parse(window.localStorage.getItem(CONFIG.consentKey) || 'null');
      return c && c.v === CONFIG.consentVersion ? c : null;
    } catch (e) { return null; }
  }
  function saveConsent(analytics) {
    var c = { v: CONFIG.consentVersion, necessary: true, analytics: !!analytics, date: new Date().toISOString() };
    try { window.localStorage.setItem(CONFIG.consentKey, JSON.stringify(c)); } catch (e) { /* almacenamiento no disponible */ }
    applyConsent(c);
    return c;
  }
  // Punto único para cargar servicios opcionales SOLO si hay consentimiento.
  // Hoy el sitio no usa analítica ni cookies de terceros.
  function applyConsent(c) {
    document.documentElement.setAttribute('data-consent-analytics', c && c.analytics ? 'granted' : 'denied');
    document.dispatchEvent(new CustomEvent('consent:updated', { detail: c }));
  }
  function showBanner(withPrefs) {
    if (!banner) return;
    var prefs = $('#cookie-prefs', banner);
    var c = readConsent();
    $('#pref-analytics', banner).checked = !!(c && c.analytics);
    prefs.hidden = !withPrefs;
    $('[data-cookie="save"]', banner).hidden = !withPrefs;
    $('[data-cookie="config"]', banner).hidden = !!withPrefs;
    banner.hidden = false;
    window.requestAnimationFrame(function () { banner.classList.add('is-visible'); });
  }
  function hideBanner() {
    if (!banner) return;
    banner.classList.remove('is-visible');
    setTimeout(function () { banner.hidden = true; }, 500);
  }
  if (banner) {
    banner.addEventListener('click', function (e) {
      var b = e.target.closest('[data-cookie]');
      if (!b) return;
      var a = b.getAttribute('data-cookie');
      if (a === 'accept') { saveConsent(true); hideBanner(); }
      if (a === 'reject') { saveConsent(false); hideBanner(); }
      if (a === 'config') { showBanner(true); $('#pref-analytics', banner).focus(); }
      if (a === 'save') { saveConsent($('#pref-analytics', banner).checked); hideBanner(); }
    });
    var current = readConsent();
    if (current) applyConsent(current); else setTimeout(function () { showBanner(false); }, 800);
  }
  $$('[data-open-cookies]').forEach(function (b) {
    b.addEventListener('click', function () { showBanner(true); });
  });

  /* ---- Formulario de contacto (sin servidor: abre el cliente de correo) ---- */
  var form = $('#contact-form');
  if (form) {
    var status = $('#form-status');
    var rules = {
      nombre: function (v) { return v.length >= 3 && v.length <= 80 && /^[\p{L}\s.'-]+$/u.test(v) ? '' : 'Escribe tu nombre completo (solo letras).'; },
      correo: function (v) { return /^[^\s@<>()]+@[^\s@<>()]+\.[a-z]{2,}$/i.test(v) && v.length <= 120 ? '' : 'Escribe un correo electrónico válido.'; },
      telefono: function (v) { return v === '' || /^[0-9 +()-]{7,20}$/.test(v) ? '' : 'Escribe un teléfono válido (solo números).'; },
      escuela: function (v) { return v.length <= 120 ? '' : 'Máximo 120 caracteres.'; },
      asunto: function (v) { return v ? '' : 'Selecciona un asunto.'; },
      mensaje: function (v) { return v.length >= 10 && v.length <= 2000 ? '' : 'Escribe un mensaje de 10 a 2,000 caracteres.'; },
      privacidad: function (v, el) { return el.checked ? '' : 'Debes aceptar el aviso de privacidad.'; }
    };
    function clean(v) { return String(v || '').replace(/[\u0000-\u001F\u007F]/g, ' ').replace(/\s+/g, ' ').trim(); }
    function validateField(el) {
      var rule = rules[el.name]; if (!rule) return true;
      var msg = rule(el.type === 'checkbox' ? '' : clean(el.value), el);
      var field = el.closest('.field') || el.closest('.check');
      if (field) {
        field.classList.toggle('has-error', !!msg);
        var err = $('.field-error', field); if (err) err.textContent = msg;
      }
      el.setAttribute('aria-invalid', msg ? 'true' : 'false');
      return !msg;
    }
    $$('input, select, textarea', form).forEach(function (el) {
      el.addEventListener('blur', function () { if (el.value || el.type === 'checkbox') validateField(el); });
      el.addEventListener('input', function () { if (el.getAttribute('aria-invalid') === 'true') validateField(el); });
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      // Trampa anti-bots
      if ($('#website', form).value) return;
      var ok = true, first = null;
      $$('input, select, textarea', form).forEach(function (el) {
        if (!validateField(el)) { ok = false; first = first || el; }
      });
      if (!ok) {
        status.hidden = false; status.className = 'form-status err';
        status.textContent = 'Revisa los campos marcados en rojo.';
        first.focus();
        return;
      }
      var d = {};
      ['nombre', 'correo', 'telefono', 'escuela', 'asunto', 'mensaje'].forEach(function (k) { d[k] = clean(form.elements[k].value); });
      var prioridad = (form.querySelector('input[name="prioridad"]:checked') || {}).value || 'Media';
      var subject = '[Portal SIE] ' + d.asunto + ' — Prioridad ' + prioridad;
      var body = 'Nombre: ' + d.nombre + '\n' +
        'Correo: ' + d.correo + '\n' +
        'Teléfono: ' + (d.telefono || '—') + '\n' +
        'Escuela / Facultad / Dependencia: ' + (d.escuela || '—') + '\n' +
        'Asunto: ' + d.asunto + '\n' +
        'Prioridad: ' + prioridad + '\n\n' +
        'Mensaje:\n' + d.mensaje + '\n';
      var href = 'mailto:' + CONFIG.contactEmail + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      status.hidden = false; status.className = 'form-status ok';
      status.textContent = 'Abriendo tu aplicación de correo con el mensaje listo. Solo presiona “Enviar”. Si no se abre, escríbenos a ' + CONFIG.contactEmail + '.';
      window.location.href = href;
    });
  }

  /* ---- Copiar al portapapeles ---- */
  $$('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      var txt = b.getAttribute('data-copy');
      var done = function () { var o = b.getAttribute('aria-label'); b.setAttribute('aria-label', 'Copiado'); b.classList.add('is-copied'); setTimeout(function () { b.setAttribute('aria-label', o); b.classList.remove('is-copied'); }, 1600); };
      if (navigator.clipboard) navigator.clipboard.writeText(txt).then(done, function () {});
    });
  });
})();
