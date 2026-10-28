/* FNS shared navigation behaviour: hamburger, "More" dropdown, current page, TR/EN labels. */
(function () {
  'use strict';
  var nav = document.querySelector('.site-nav');
  if (!nav) return;
  var toggle = nav.querySelector('.site-nav__toggle');
  var menu = nav.querySelector('.site-nav__menu');
  var ddBtn = nav.querySelector('.site-nav__dd-btn');
  var panel = nav.querySelector('.site-nav__panel');
  var mq = window.matchMedia('(max-width: 960px)');

  function setMenu(open) {
    nav.setAttribute('data-open', open ? 'true' : 'false');
    if (toggle) {
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', toggle.getAttribute(open ? 'data-label-close-' + lang() : 'data-label-open-' + lang()) || 'Menu');
    }
  }
  function setPanel(open) {
    if (!ddBtn || !panel) return;
    ddBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (open) panel.removeAttribute('hidden'); else panel.setAttribute('hidden', '');
  }
  function lang() {
    var l = document.getElementById('langLabel');
    var t = l ? (l.textContent || '').trim().toLowerCase() : '';
    if (t === 'english' || t === 'en') return 'tr';
    if (t === 'türkçe' || t === 'tr') return 'en';
    return document.documentElement.lang === 'tr' ? 'tr' : 'en';
  }
  function applyLang() {
    var L = lang();
    document.documentElement.lang = L;
    nav.querySelectorAll('[data-tr]').forEach(function (el) {
      var v = el.getAttribute('data-' + L);
      if (v != null && el.textContent !== v) el.textContent = v;
    });
    nav.querySelectorAll('[data-title-tr]').forEach(function (el) {
      el.setAttribute('data-title', el.getAttribute('data-title-' + L));
    });
    if (toggle) setMenu(nav.getAttribute('data-open') === 'true');
  }

  if (toggle) toggle.addEventListener('click', function () {
    setMenu(nav.getAttribute('data-open') !== 'true');
  });
  if (ddBtn) {
    ddBtn.addEventListener('click', function (e) { e.stopPropagation(); setPanel(ddBtn.getAttribute('aria-expanded') !== 'true'); });
    ddBtn.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') { e.preventDefault(); setPanel(true); var f = panel.querySelector('a'); if (f) f.focus(); }
    });
  }
  if (panel) panel.addEventListener('keydown', function (e) {
    var items = Array.prototype.slice.call(panel.querySelectorAll('a'));
    var i = items.indexOf(document.activeElement);
    if (e.key === 'ArrowDown') { e.preventDefault(); items[(i + 1) % items.length].focus(); }
    if (e.key === 'ArrowUp') { e.preventDefault(); items[(i - 1 + items.length) % items.length].focus(); }
  });
  document.addEventListener('click', function (e) {
    if (!nav.contains(e.target)) { setPanel(false); setMenu(false); }
  });
  nav.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a');
    if (a) { setPanel(false); setMenu(false); }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var wasPanel = ddBtn && ddBtn.getAttribute('aria-expanded') === 'true';
    var wasMenu = nav.getAttribute('data-open') === 'true';
    setPanel(false); setMenu(false);
    if (wasPanel && ddBtn && !mq.matches) ddBtn.focus();
    else if (wasMenu && toggle) toggle.focus();
  });
  function onMq() { setMenu(false); setPanel(mq.matches); }
  if (mq.addEventListener) mq.addEventListener('change', onMq); else if (mq.addListener) mq.addListener(onMq);

  /* current page */
  var file = (location.pathname.split('/').pop() || 'index.html');
  nav.querySelectorAll('a[data-page]').forEach(function (a) {
    if (a.getAttribute('data-page') === file) a.setAttribute('aria-current', 'page');
  });

  /* follow the page's own language switch */
  var l = document.getElementById('langLabel');
  if (l && window.MutationObserver) new MutationObserver(applyLang).observe(l, { childList: true, characterData: true, subtree: true });
  applyLang();
  setPanel(mq.matches);
  setMenu(false);
})();
