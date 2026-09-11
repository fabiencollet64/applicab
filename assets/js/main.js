/* AppliCab Avocats — JS progressif (≈2 Ko, non bloquant : chargé en defer)
   Tout le contenu est lisible sans JavaScript. */
(function () {
  'use strict';
  document.documentElement.classList.add('js');

  /* Menu mobile */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.querySelector('.nav-toggle__label').textContent = open ? 'Fermer' : 'Menu';
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) { toggle.click(); toggle.focus(); }
    });
  }

  /* Ombre de l'en-tête au défilement */
  var header = document.querySelector('.site-header');
  if (header) {
    var onScroll = function () { header.classList.toggle('is-stuck', window.scrollY > 8); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* Façade vidéo : l'iframe YouTube n'est injectée qu'au clic (Core Web Vitals) */
  document.querySelectorAll('.video-facade[data-video]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var id = btn.getAttribute('data-video');
      var iframe = document.createElement('iframe');
      iframe.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0';
      iframe.title = btn.getAttribute('data-title') || 'Vidéo de présentation';
      iframe.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture';
      iframe.setAttribute('allowfullscreen', '');
      btn.replaceChildren(iframe);
    });
  });

  /* Apparition douce des blocs (position seulement, jamais d'opacité 0) */
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* Sommaire d'article : surligne la section en cours */
  var tocLinks = document.querySelectorAll('.toc a[href^="#"]');
  if ('IntersectionObserver' in window && tocLinks.length) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var headings = Object.keys(map).map(function (id) { return document.getElementById(id); }).filter(Boolean);
    var hio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          tocLinks.forEach(function (a) { a.classList.remove('is-active'); });
          map[en.target.id].classList.add('is-active');
        }
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    headings.forEach(function (h) { hio.observe(h); });
  }

  /* Newsletter (maquette) : pas d'envoi réel */
  var form = document.querySelector('.newsletter form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = form.querySelector('.form-msg');
      if (msg) { msg.textContent = 'Merci ! Vous êtes inscrit·e à la lettre mensuelle.'; }
    });
  }
})();
