/* Taxonomy browser: filters server-rendered cards. State lives in the URL hash so a filtered view can be shared. No storage, no requests. */
(function () {
  'use strict';
  var root = document.getElementById('browser');
  if (!root) return;
  var cards = Array.prototype.slice.call(root.querySelectorAll('.card'));
  var q = document.getElementById('q');
  var status = document.getElementById('status');
  var empty = document.getElementById('empty');
  var tabs = Array.prototype.slice.call(root.querySelectorAll('.sec-tabs button[data-sec]'));
  var boxes = Array.prototype.slice.call(root.querySelectorAll('.filters input[type=checkbox]'));
  var FACETS = ['skillLevel', 'input', 'output', 'era', 'sessionLength', 'ai'];
  var state = { q: '', sec: 'all', f: {} };

  function norm(s) { return (s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, ''); }
  cards.forEach(function (c) { c._text = norm(c.textContent + ' ' + (c.dataset.terms || '')); });

  function cardMatches(c, skip) {
    if (state.sec !== 'all' && c.dataset.section !== state.sec) return false;
    if (state.q) {
      var words = norm(state.q).split(/\s+/).filter(Boolean);
      for (var i = 0; i < words.length; i++) if (c._text.indexOf(words[i]) < 0) return false;
    }
    for (var k = 0; k < FACETS.length; k++) {
      var f = FACETS[k];
      if (f === skip) continue;
      var want = state.f[f];
      if (!want || !want.length) continue;
      var have = (c.dataset[f] || '').split(' ');
      if (!want.some(function (w) { return have.indexOf(w) >= 0; })) return false;
    }
    return true;
  }

  function render() {
    var shown = 0;
    cards.forEach(function (c) { var ok = cardMatches(c); c.hidden = !ok; if (ok) shown++; });
    boxes.forEach(function (b) {
      var f = b.name, v = b.value, n = 0;
      cards.forEach(function (c) { if (cardMatches(c, f) && (c.dataset[f] || '').split(' ').indexOf(v) >= 0) n++; });
      b.parentNode.querySelector('.count').textContent = n;
    });
    tabs.forEach(function (t) { t.setAttribute('aria-pressed', String(t.dataset.sec === state.sec)); });
    status.textContent = shown === cards.length ? 'Showing all ' + shown + ' tools' : 'Showing ' + shown + ' of ' + cards.length + ' tools';
    empty.hidden = shown > 0;
  }

  function writeHash() {
    var parts = [];
    if (state.q) parts.push('q=' + encodeURIComponent(state.q));
    if (state.sec !== 'all') parts.push('section=' + encodeURIComponent(state.sec));
    FACETS.forEach(function (f) { if (state.f[f] && state.f[f].length) parts.push(f + '=' + state.f[f].map(encodeURIComponent).join(',')); });
    var h = parts.join('&');
    history.replaceState(null, '', h ? '#' + h : location.pathname + location.search);
  }

  function readHash() {
    state = { q: '', sec: 'all', f: {} };
    location.hash.replace(/^#/, '').split('&').forEach(function (p) {
      if (!p) return;
      var i = p.indexOf('='), k = p.slice(0, i), v = decodeURIComponent(p.slice(i + 1));
      if (k === 'q') state.q = v;
      else if (k === 'section') state.sec = v;
      else if (FACETS.indexOf(k) >= 0) state.f[k] = v.split(',').map(decodeURIComponent);
    });
    if (!tabs.some(function (t) { return t.dataset.sec === state.sec && !t.disabled; })) state.sec = 'all';
    q.value = state.q;
    boxes.forEach(function (b) { b.checked = !!(state.f[b.name] && state.f[b.name].indexOf(b.value) >= 0); });
  }

  function update() { writeHash(); render(); }
  var t;
  q.addEventListener('input', function () { clearTimeout(t); t = setTimeout(function () { state.q = q.value.trim(); update(); }, 120); });
  root.querySelector('form').addEventListener('submit', function (e) { e.preventDefault(); state.q = q.value.trim(); update(); });
  tabs.forEach(function (b) { b.addEventListener('click', function () { state.sec = b.dataset.sec; update(); }); });
  boxes.forEach(function (b) {
    b.addEventListener('change', function () {
      var list = state.f[b.name] || (state.f[b.name] = []);
      var i = list.indexOf(b.value);
      if (b.checked && i < 0) list.push(b.value);
      if (!b.checked && i >= 0) list.splice(i, 1);
      update();
    });
  });
  Array.prototype.forEach.call(document.querySelectorAll('[data-clear]'), function (b) {
    b.addEventListener('click', function () { state = { q: '', sec: 'all', f: {} }; q.value = ''; boxes.forEach(function (x) { x.checked = false; }); update(); q.focus(); });
  });
  window.addEventListener('hashchange', function () { readHash(); render(); });
  readHash(); render();
})();
