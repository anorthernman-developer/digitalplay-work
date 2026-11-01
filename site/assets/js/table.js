/* The home-page loose parts table: decorative, so it is hidden from assistive tech. Drag a shape to move it; nothing is saved. */
(function () {
  'use strict';
  var svg = document.querySelector('.table svg');
  if (!svg || !window.PointerEvent) return;
  var drag = null;
  function pt(e) { var p = svg.createSVGPoint(); p.x = e.clientX; p.y = e.clientY; return p.matrixTransform(svg.getScreenCTM().inverse()); }
  svg.addEventListener('pointerdown', function (e) {
    var g = e.target.closest('.part'); if (!g) return;
    var m = /translate\(([-\d.]+)[ ,]+([-\d.]+)\)(.*)/.exec(g.getAttribute('transform') || '');
    if (!m) return;
    var p = pt(e);
    drag = { g: g, ox: p.x - +m[1], oy: p.y - +m[2], rest: m[3] };
    g.parentNode.appendChild(g);
    svg.setPointerCapture(e.pointerId);
    e.preventDefault();
  });
  svg.addEventListener('pointermove', function (e) {
    if (!drag) return;
    var p = pt(e);
    var x = Math.max(20, Math.min(480, p.x - drag.ox)), y = Math.max(20, Math.min(380, p.y - drag.oy));
    drag.g.setAttribute('transform', 'translate(' + x.toFixed(1) + ' ' + y.toFixed(1) + ')' + drag.rest);
  });
  function end() { drag = null; }
  svg.addEventListener('pointerup', end);
  svg.addEventListener('pointercancel', end);
})();
