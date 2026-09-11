/* AppliCab Avocats — JS progressif (~4 Ko, chargé en defer, non bloquant).
   Tout le contenu reste lisible sans JavaScript ; ce fichier n'ajoute que du confort. */
(function () {
  'use strict';
  var d = document, w = window;
  var reduced = w.matchMedia && w.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* --- Menu mobile ------------------------------------------------------- */
  var toggle = d.querySelector('.nav-toggle'), nav = d.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
      toggle.querySelector('span').textContent = open ? 'Fermer' : 'Menu';
    });
  }

  /* --- Méga-menus (clic / clavier, fermeture à l'extérieur et Échap) ------ */
  var megaBtns = d.querySelectorAll('.nav button[aria-controls]');
  function closeMegas(except) {
    megaBtns.forEach(function (b) {
      if (b === except) return;
      b.setAttribute('aria-expanded', 'false');
      d.getElementById(b.getAttribute('aria-controls')).dataset.open = 'false';
    });
  }
  megaBtns.forEach(function (b) {
    b.addEventListener('click', function () {
      var panel = d.getElementById(b.getAttribute('aria-controls'));
      var open = b.getAttribute('aria-expanded') === 'true';
      closeMegas(b);
      b.setAttribute('aria-expanded', String(!open));
      panel.dataset.open = String(!open);
    });
  });
  d.addEventListener('click', function (e) { if (!e.target.closest('.nav')) closeMegas(); });
  d.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    closeMegas();
    if (nav && nav.classList.contains('is-open')) { toggle.click(); toggle.focus(); }
  });

  /* --- Ombre de l'en-tête + barre de lecture ------------------------------ */
  var header = d.querySelector('.site-header'), bar = d.querySelector('.reading-bar');
  function onScroll() {
    if (header) header.classList.toggle('is-stuck', w.scrollY > 8);
    if (bar) {
      var h = d.documentElement.scrollHeight - w.innerHeight;
      bar.style.width = (h > 0 ? Math.min(100, w.scrollY / h * 100) : 0) + '%';
    }
  }
  onScroll();
  w.addEventListener('scroll', onScroll, { passive: true });

  /* --- Onglets produit, rotation automatique (pause au survol/focus) ------- */
  var tablist = d.querySelector('.tabs');
  if (tablist) {
    var tabs = Array.prototype.slice.call(tablist.querySelectorAll('button[role="tab"]'));
    var panels = tabs.map(function (t) { return d.getElementById(t.getAttribute('aria-controls')); });
    var i = 0, timer = null, paused = false;
    function select(n, byUser) {
      i = (n + tabs.length) % tabs.length;
      tabs.forEach(function (t, k) {
        t.setAttribute('aria-selected', String(k === i));
        t.tabIndex = k === i ? 0 : -1;
        panels[k].dataset.active = String(k === i);
      });
      if (byUser) { paused = true; tablist.classList.add('is-paused'); clearInterval(timer); }
    }
    tabs.forEach(function (t, k) {
      t.addEventListener('click', function () { select(k, true); });
      t.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowRight') { select(k + 1, true); tabs[i].focus(); }
        if (e.key === 'ArrowLeft') { select(k - 1, true); tabs[i].focus(); }
      });
    });
    select(0);
    if (!reduced) {
      timer = setInterval(function () { if (!paused) select(i + 1); }, 7000);
      var wrap = tablist.parentElement;
      wrap.addEventListener('mouseenter', function () { tablist.classList.add('is-paused'); paused = true; });
      wrap.addEventListener('mouseleave', function () { if (!tablist.dataset.locked) { tablist.classList.remove('is-paused'); paused = false; } });
      tablist.addEventListener('click', function () { tablist.dataset.locked = '1'; });
    }
  }

  /* --- Révélations : seuls les blocs hors écran au chargement sont animés --- */
  var reveals = d.querySelectorAll('.reveal');
  if (!reduced && 'IntersectionObserver' in w && reveals.length) {
    var vh = w.innerHeight;
    reveals.forEach(function (el) {
      if (el.getBoundingClientRect().top > vh) el.classList.add('reveal--pending');
      else el.classList.add('is-in');
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -10% 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* --- Compteurs animés ---------------------------------------------------- */
  var counters = d.querySelectorAll('[data-count]');
  if (counters.length && 'IntersectionObserver' in w && !reduced) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, target = parseFloat(el.dataset.count), start = null, dur = 1400;
        function step(ts) {
          if (!start) start = ts;
          var p = Math.min(1, (ts - start) / dur), e = 1 - Math.pow(1 - p, 3);
          el.textContent = Math.round(target * e);
          if (p < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
        cio.unobserve(el);
      });
    }, { threshold: .6 });
    counters.forEach(function (c) { cio.observe(c); });
  }

  /* --- Sommaire / sous-navigation : section active ------------------------- */
  function spy(linksSel) {
    var links = d.querySelectorAll(linksSel);
    if (!links.length || !('IntersectionObserver' in w)) return;
    var map = {};
    links.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var targets = Object.keys(map).map(function (id) { return d.getElementById(id); }).filter(Boolean);
    var sio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          links.forEach(function (a) { a.classList.remove('is-active'); });
          map[en.target.id].classList.add('is-active');
        }
      });
    }, { rootMargin: '-25% 0px -65% 0px' });
    targets.forEach(function (t) { sio.observe(t); });
  }
  spy('.toc a[href^="#"]');
  spy('.subnav a[href^="#"]');

  /* --- Façade vidéo : l'iframe n'est injectée qu'au clic ------------------- */
  d.querySelectorAll('.video-facade[data-video]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var f = d.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + btn.dataset.video + '?autoplay=1&rel=0';
      f.title = btn.dataset.title || 'Vidéo'; f.allow = 'autoplay; encrypted-media; picture-in-picture'; f.setAttribute('allowfullscreen', '');
      btn.replaceChildren(f);
    });
  });

  /* --- Newsletter (maquette : aucun envoi) --------------------------------- */
  var form = d.querySelector('.newsletter form');
  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    var m = form.querySelector('.form-msg'); if (m) m.textContent = 'Merci, vous êtes inscrit·e à la lettre mensuelle.';
  });
})();
