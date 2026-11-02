// ---------- fake Paris: tower, facades, fountain, paddies, gags ----------
function parisSky(ctx, top = '#7cc6f2', bot = '#ffe6c4') { drawSky(ctx, top, bot, -600, 1200); }
function eiffel(ctx, x, base, h, col = '#7a5a46') {
  const w = h * .42;
  ctx.save(); ctx.translate(x, base);
  const leg = (s) => { ctx.beginPath(); ctx.moveTo(s * w / 2, 0); ctx.quadraticCurveTo(s * w * .18, -h * .35, s * w * .06, -h * .72); ctx.lineTo(s * w * .03, -h * .72); ctx.quadraticCurveTo(s * w * .1, -h * .35, s * w * .3, 0); ctx.closePath(); fillStroke(ctx, col, h * .008); };
  leg(-1); leg(1);
  // arch between legs
  ctx.beginPath(); ctx.moveTo(-w * .34, 0); ctx.quadraticCurveTo(0, -h * .2, w * .34, 0); ctx.lineWidth = h * .012; ctx.strokeStyle = col; ctx.stroke();
  // platforms
  rrect(ctx, -w * .3, -h * .26, w * .6, h * .03, 4); fillStroke(ctx, col, h * .006);
  rrect(ctx, -w * .14, -h * .52, w * .28, h * .025, 4); fillStroke(ctx, col, h * .006);
  // spire
  ctx.beginPath(); ctx.moveTo(-w * .06, -h * .72); ctx.lineTo(-w * .02, -h * .97); ctx.lineTo(w * .02, -h * .97); ctx.lineTo(w * .06, -h * .72); ctx.closePath(); fillStroke(ctx, col, h * .006);
  line(ctx, 0, -h * .97, 0, -h * 1.03, h * .006, col);
  // lattice cross-hatch
  ctx.save(); ctx.globalAlpha = .45; ctx.strokeStyle = '#3a2a22'; ctx.lineWidth = Math.max(1.5, h * .003);
  for (let i = 1; i < 14; i++) { const yy = -h * .72 * i / 14; const ww = w * .5 * (1 - i / 14) * .9 + w * .06; ctx.beginPath(); ctx.moveTo(-ww, yy); ctx.lineTo(ww, yy - h * .03); ctx.moveTo(ww, yy); ctx.lineTo(-ww, yy - h * .03); ctx.stroke(); }
  ctx.restore(); ctx.restore();
}
function haussmann(ctx, x, base, w, h, seed = 1, empty = 0) {
  const R = rng(seed);
  rrect(ctx, x, base - h, w, h, 6); fillStroke(ctx, '#f1e2c4', 6);
  ctx.save(); rrect(ctx, x, base - h, w, h, 6); ctx.clip(); ctx.fillStyle = 'rgba(80,50,30,.12)'; ctx.fillRect(x + w * .7, base - h, w, h); ctx.restore();
  // mansard roof
  ctx.beginPath(); ctx.moveTo(x - 10, base - h); ctx.lineTo(x + 30, base - h - 90); ctx.lineTo(x + w - 30, base - h - 90); ctx.lineTo(x + w + 10, base - h); ctx.closePath(); fillStroke(ctx, '#6a7488', 6);
  for (let i = 0; i < 3; i++) { const dx = x + w * (i + .5) / 3 - 22; rrect(ctx, dx, base - h - 70, 44, 50, [20, 20, 4, 4]); fillStroke(ctx, '#f1e2c4', 4); }
  // windows rows with balconies
  const rows = Math.floor((h - 160) / 150), cols = Math.max(2, Math.floor(w / 120));
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
    const wx = x + w * (c + .5) / cols - 30, wy = base - h + 40 + r * 150;
    rrect(ctx, wx, wy, 60, 100, [26, 26, 4, 4]); fillStroke(ctx, empty > .5 && R() < .6 ? '#4a4a58' : '#8fc6e8', 4);
    if (empty > .5 && R() < .5) { ctx.fillStyle = '#9a9aa6'; rrect(ctx, wx + 4, wy + 4, 52, 92, [22, 22, 2, 2]); ctx.fill(); for (let k = 0; k < 6; k++) line(ctx, wx + 6, wy + 14 + k * 14, wx + 54, wy + 14 + k * 14, 2, '#6a6a76'); }
    line(ctx, wx - 10, wy + 100, wx + 70, wy + 100, 6, '#2b2230');
    for (let k = 0; k < 5; k++) line(ctx, wx - 6 + k * 18, wy + 100, wx - 6 + k * 18, wy + 82, 3, '#2b2230');
  }
  // shop front at street level
  rrect(ctx, x + 20, base - 130, w - 40, 130, 4); fillStroke(ctx, empty > .5 ? '#7a7a86' : '#2f6a5a', 5);
  if (empty > .5) { for (let k = 0; k < 8; k++) line(ctx, x + 24, base - 124 + k * 16, x + w - 24, base - 124 + k * 16, 3, '#5a5a66'); }
}
function fountain(ctx, x, y, s, t, splash = 0) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  ellipse(ctx, 0, 0, 260, 60); fillStroke(ctx, '#d8d0c4', 6); ellipse(ctx, 0, -8, 230, 46); fillStroke(ctx, '#7fd0ea', 4);
  rrect(ctx, -26, -200, 52, 200, 10); fillStroke(ctx, '#e6ddd0', 5);
  ellipse(ctx, 0, -200, 110, 26); fillStroke(ctx, '#d8d0c4', 5);
  for (let i = 0; i < 7; i++) { const a = -Math.PI / 2 + (i - 3) * .35; const ph = (t * 1.5 + i * .3) % 1;
    ctx.beginPath(); ctx.moveTo(0, -220); ctx.quadraticCurveTo(Math.cos(a) * 120, -330, Math.cos(a) * 200, -40); ctx.lineWidth = 7; ctx.strokeStyle = 'rgba(160,220,255,.85)'; ctx.stroke();
    circle(ctx, Math.cos(a) * 200 * ph, -220 + (ph * ph * 180 - ph * 110), 6); ctx.fillStyle = '#c8ecff'; ctx.fill(); }
  if (splash > 0) for (let i = 0; i < 10; i++) { const a = -Math.PI * (i / 9); circle(ctx, 150 + Math.cos(a) * 140 * splash, -20 + Math.sin(a) * 160 * splash, 14 * (1 - splash * .6)); fillStroke(ctx, '#bfe9ff', 3); }
  ctx.restore();
}
function paddies(ctx, horizon, t) {
  for (let i = 0; i < 9; i++) { const y = horizon + i * i * 16 + 10; ctx.fillStyle = i % 2 ? '#7bc65a' : '#9ad86c'; ctx.fillRect(-800, y, 2700, (i + 1) * 30 + 30); line(ctx, -800, y, 1900, y, 3, 'rgba(60,110,40,.5)'); }
  // hills
  ctx.fillStyle = '#8ab8a0'; ctx.beginPath(); ctx.moveTo(-800, horizon + 10); for (let x = -800; x <= 1900; x += 60) ctx.lineTo(x, horizon - 60 - 70 * Math.sin(x / 210) - 40 * Math.sin(x / 90 + 1)); ctx.lineTo(1900, horizon + 10); ctx.closePath(); ctx.fill();
}
function baguette(ctx, x, y, s, rot = 0) { ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s); rrect(ctx, -10, -150, 20, 300, 10); fillStroke(ctx, '#e0a85a', 3); for (let i = 0; i < 4; i++) line(ctx, -6, -110 + i * 70, 6, -90 + i * 70, 3, '#9a6a2a'); ctx.restore(); }
const bagProp = (c, k, h, a, side) => { if (k !== 'R') return; c.save(); c.translate(h[0], h[1]); c.rotate(-side * .5); rrect(c, -.018, -.26, .036, .36, .018); fillStroke(c, '#e0a85a', .008); for (let i = 0; i < 4; i++) line(c, -.01, -.2 + i * .08, .01, -.18 + i * .08, .006, '#9a6a2a'); c.restore(); };
const camProp = (c, k, h, a, side) => { if (k !== 'R') return; c.save(); c.translate(h[0], h[1]); rrect(c, -.06, -.05, .12, .08, .012); fillStroke(c, '#2b2230', .01); circle(c, 0, -.01, .025); fillStroke(c, '#7fb0e0', .008); c.restore(); };
const phoneUp = (c, k, h, a, side) => { if (k !== 'R') return; c.save(); c.translate(h[0], h[1]); rrect(c, -.03, -.1, .06, .11, .01); fillStroke(c, '#222', .009); c.restore(); };
function beret(ctx, x, y, s) { ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ellipse(ctx, 0, 0, 1.1, .38, -.15); fillStroke(ctx, '#2b2230', .06); line(ctx, .1, -.38, .14, -.55, .08); ctx.restore(); }
function veil(ctx, x, y, s) { ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.beginPath(); ctx.moveTo(-.12, -.9); ctx.quadraticCurveTo(-.32, -.6, -.28, -.3); ctx.lineTo(.0, -.38); ctx.quadraticCurveTo(.1, -.7, .1, -.92); ctx.closePath(); ctx.globalAlpha = .85; fillStroke(ctx, '#ffffff', .012); ctx.restore(); }
function dress(ctx, x, y, s) { ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.beginPath(); ctx.moveTo(-.1, -.55); ctx.lineTo(.1, -.55); ctx.lineTo(.3, 0); ctx.quadraticCurveTo(0, .05, -.3, 0); ctx.closePath(); fillStroke(ctx, '#fffaf4', .014); ctx.restore(); }
function mimeBox(ctx, x, y, s, t) { ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.globalAlpha = .35; rrect(ctx, -.32, -1.05, .64, 1.08, .02); ctx.lineWidth = .01; ctx.setLineDash([.03, .03]); ctx.strokeStyle = '#8fd8ff'; ctx.stroke(); ctx.restore(); }
function tumbleweed(ctx, x, y, r, t) { ctx.save(); ctx.translate(x, y); ctx.rotate(t * 6); ctx.strokeStyle = '#a07a3a'; ctx.lineWidth = 4; for (let i = 0; i < 9; i++) { ctx.beginPath(); ctx.arc(Math.sin(i * 2.1) * r * .2, Math.cos(i * 1.7) * r * .2, r * (.5 + (i % 3) * .2), i, i + 4); ctx.stroke(); } ctx.restore(); }
function bench(ctx, x, y, s) { ctx.save(); ctx.translate(x, y); ctx.scale(s, s); rrect(ctx, -160, -70, 320, 22, 6); fillStroke(ctx, '#8a5530', 5); rrect(ctx, -160, -140, 320, 20, 6); fillStroke(ctx, '#8a5530', 5); line(ctx, -130, -48, -130, 0, 10); line(ctx, 130, -48, 130, 0, 10); ctx.restore(); }
function pigeon(ctx, x, y, s, t, fly = 0) { ctx.save(); ctx.translate(x, y - fly * 200); ctx.scale(s, s); ellipse(ctx, 0, 0, 30, 20); fillStroke(ctx, '#9aa0b0', 3); circle(ctx, 24, -16, 12); fillStroke(ctx, '#8a90a0', 3); ctx.beginPath(); ctx.moveTo(34, -16); ctx.lineTo(44, -12); ctx.lineTo(34, -10); ctx.fillStyle = '#e8b04a'; ctx.fill(); circle(ctx, 27, -19, 2.5); ctx.fillStyle = INK; ctx.fill();
  if (fly > 0) { const w = Math.sin(t * 40) * 20; ctx.beginPath(); ctx.moveTo(-6, -6); ctx.lineTo(-36, -30 - w); ctx.lineTo(4, -10); ctx.closePath(); fillStroke(ctx, '#b0b6c4', 3); } ctx.restore(); }
function heartsPop(ctx, x, y, t, a = 1) { if (a <= 0) return; for (let i = 0; i < 4; i++) { const p = (t * .8 + i * .25) % 1; ctx.save(); ctx.globalAlpha = a * (1 - p); ctx.translate(x + Math.sin(i * 2 + t) * 50, y - p * 200); ctx.scale(.6 + p * .4, .6 + p * .4); ctx.beginPath(); ctx.moveTo(0, 12); ctx.bezierCurveTo(-30, -10, -16, -34, 0, -18); ctx.bezierCurveTo(16, -34, 30, -10, 0, 12); fillStroke(ctx, '#ff5a7a', 3); ctx.restore(); } }
