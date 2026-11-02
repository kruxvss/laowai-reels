// ---------- Kashgar street, clocks, globe, laowai booth ----------
const CJK = '"Noto Sans CJK SC", "Noto Sans CJK", sans-serif';
function cjkText(ctx, str, x, y, size, fill = '#fff', stroke = INK, sw = 0, weight = 900) {
  ctx.font = `${weight} ${size}px ${CJK}`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  if (sw) { ctx.lineWidth = sw; ctx.strokeStyle = stroke; ctx.lineJoin = 'round'; ctx.strokeText(str, x, y); }
  ctx.fillStyle = fill; ctx.fillText(str, x, y);
}
// sky that goes from night (0) to morning (1)
function dawnSky(ctx, k) {
  const top = mix('#0b1238', '#4aaeea', k), mid = mix('#1d2a66', '#ffc07a', k), bot = mix('#2a3270', '#ffe2b0', k);
  const g = ctx.createLinearGradient(0, -400, 0, 1300); g.addColorStop(0, top); g.addColorStop(.6, mid); g.addColorStop(1, bot);
  ctx.fillStyle = g; ctx.fillRect(-2000, -2400, 5080, 5000);
}
function stars(ctx, a, t) {
  if (a <= 0) return; const R = rng(21); ctx.save(); ctx.globalAlpha = a;
  for (let i = 0; i < 60; i++) { const x = R() * 1300 - 110, y = R() * 900 - 200, r = 3 + R() * 5; const tw = .6 + .4 * Math.sin(t * 3 + i); ctx.globalAlpha = a * tw; star5(ctx, x, y, r * 2.2, R() * 3, '#fff7c8'); }
  ctx.restore();
}
function moon(ctx, x, y, r, a = 1) {
  if (a <= 0) return; ctx.save(); ctx.globalAlpha = a;
  const g = ctx.createRadialGradient(x, y, r * .5, x, y, r * 3); g.addColorStop(0, 'rgba(255,245,200,.35)'); g.addColorStop(1, 'rgba(255,245,200,0)'); ctx.fillStyle = g; ctx.fillRect(x - r * 3, y - r * 3, r * 6, r * 6);
  circle(ctx, x, y, r); fillStroke(ctx, '#fff3c4', r * .08);
  circle(ctx, x - r * .3, y - r * .2, r * .18); ctx.fillStyle = 'rgba(200,180,120,.5)'; ctx.fill(); circle(ctx, x + r * .25, y + r * .3, r * .12); ctx.fill();
  ctx.restore();
}
// adobe-style building block with arched door, carved wooden door, balcony, windows that glow at night
function building(ctx, x, base, w, h, col, night = 0, seed = 1, o = {}) {
  const R = rng(seed);
  rrect(ctx, x, base - h, w, h, 10); fillStroke(ctx, col, 6);
  ctx.save(); rrect(ctx, x, base - h, w, h, 10); ctx.clip(); ctx.fillStyle = 'rgba(60,20,10,.14)'; ctx.fillRect(x + w * .72, base - h, w, h);
  for (let i = 0; i < 9; i++) { ctx.fillStyle = 'rgba(120,70,40,.18)'; rrect(ctx, x + R() * w, base - h + R() * h, 18 + R() * 30, 6, 3); ctx.fill(); }
  ctx.restore();
  // parapet
  rrect(ctx, x - 8, base - h - 16, w + 16, 22, 6); fillStroke(ctx, mix(col, '#7a4a2a', .35), 5);
  // windows
  const wc = mix('#3a2a26', '#ffc35a', night);
  for (let k = 0; k < (o.wins || 2); k++) {
    const wx = x + w * (k + .5) / (o.wins || 2) - 34, wy = base - h + h * .2;
    ctx.beginPath(); ctx.moveTo(wx, wy + 90); ctx.lineTo(wx, wy + 30); ctx.arc(wx + 34, wy + 30, 34, Math.PI, 0); ctx.lineTo(wx + 68, wy + 90); ctx.closePath(); fillStroke(ctx, wc, 5);
    if (night > .1) { ctx.save(); ctx.globalCompositeOperation = 'lighter'; const g = ctx.createRadialGradient(wx + 34, wy + 55, 5, wx + 34, wy + 55, 120); g.addColorStop(0, `rgba(255,190,90,${.35 * night})`); g.addColorStop(1, 'rgba(255,190,90,0)'); ctx.fillStyle = g; ctx.fillRect(wx - 90, wy - 70, 250, 250); ctx.restore(); }
    line(ctx, wx + 34, wy, wx + 34, wy + 90, 4);
  }
  // arched doorway with carved door
  if (o.door !== false) {
    const dw = Math.min(150, w * .45), dx = x + w * (o.doorAt ?? .5) - dw / 2, dh = Math.min(260, h * .55);
    ctx.beginPath(); ctx.moveTo(dx, base); ctx.lineTo(dx, base - dh + dw / 2); ctx.arc(dx + dw / 2, base - dh + dw / 2, dw / 2, Math.PI, 0); ctx.lineTo(dx + dw, base); ctx.closePath(); fillStroke(ctx, '#7a3f1e', 6);
    ctx.save(); ctx.clip(); for (let i = 0; i < 4; i++) { rrect(ctx, dx + 14 + (i % 2) * (dw / 2 - 8), base - dh + dw / 2 + 20 + Math.floor(i / 2) * 70, dw / 2 - 26, 56, 6); fillStroke(ctx, '#934d26', 4); } ctx.restore();
    circle(ctx, dx + dw * .62, base - dh * .45, 7); fillStroke(ctx, '#e8c04a', 3);
  }
  if (o.balcony) { rrect(ctx, x + w * .15, base - h * .55, w * .7, 18, 6); fillStroke(ctx, '#8a5530', 5); for (let i = 0; i < 6; i++) line(ctx, x + w * .18 + i * w * .12, base - h * .55, x + w * .18 + i * w * .12, base - h * .55 - 50, 5, '#8a5530'); line(ctx, x + w * .15, base - h * .55 - 50, x + w * .85, base - h * .55 - 50, 6, '#8a5530'); }
}
function street(ctx, t, cam, night, o = {}) {
  applyCam(ctx, cam, .06); dawnSky(ctx, 1 - night); stars(ctx, night, t);
  applyCam(ctx, cam, .1); moon(ctx, 820, 240, 70, night);
  if (o.sun != null) { applyCam(ctx, cam, .12); drawSun(ctx, 540, o.sun, 90, t, 1.2 * (1 - night)); }
  applyCam(ctx, cam, .3);
  // far rooftops with a dome silhouette
  ctx.fillStyle = mix('#1a1a40', '#d89a70', 1 - night);
  ctx.beginPath(); ctx.moveTo(-600, 1000); [[-500, 760], [-300, 760], [-300, 700], [-100, 700], [-100, 780], [120, 780], [120, 640], [300, 640], [300, 740], [520, 740], [520, 690], [560, 690], [600, 600], [640, 690], [680, 690], [680, 760], [900, 760], [900, 660], [1100, 660], [1100, 740], [1700, 740], [1700, 1000]].forEach(p => ctx.lineTo(p[0], p[1])); ctx.closePath(); ctx.fill();
  applyCam(ctx, cam, 1);
  const cols = ['#d9a066', '#c98c58', '#e3b07a', '#cf9a68'];
  building(ctx, -260, 1180, 420, 640, cols[0], night, 1, { balcony: true });
  building(ctx, 170, 1180, 360, 560, cols[1], night, 2, { wins: 2 });
  building(ctx, 540, 1180, 380, 700, cols[2], night, 3, { balcony: true, doorAt: .4 });
  building(ctx, 930, 1180, 420, 600, cols[3], night, 4);
  // ground: brick street in perspective
  ctx.fillStyle = mix('#3a2c34', '#c79a6e', 1 - night); ctx.fillRect(-600, 1180, 2400, 1400);
  ctx.strokeStyle = 'rgba(40,20,20,.25)'; ctx.lineWidth = 4;
  for (let i = 0; i < 9; i++) { ctx.beginPath(); ctx.moveTo(-600, 1210 + i * i * 14); ctx.lineTo(1700, 1210 + i * i * 14); ctx.stroke(); }
  // street lamps
  for (const lx of o.lamps || [120, 980]) {
    line(ctx, lx, 1240, lx, 820, 12, '#2b2230'); line(ctx, lx, 830, lx + (lx < 540 ? 60 : -60), 830, 10, '#2b2230');
    const bx = lx + (lx < 540 ? 60 : -60); circle(ctx, bx, 860, 26); fillStroke(ctx, night > .2 ? '#ffe7a0' : '#f4f0e0', 5);
    if (night > .1) { ctx.save(); ctx.globalCompositeOperation = 'lighter'; const g = ctx.createRadialGradient(bx, 860, 10, bx, 860, 260); g.addColorStop(0, `rgba(255,210,120,${.5 * night})`); g.addColorStop(1, 'rgba(255,210,120,0)'); ctx.fillStyle = g; ctx.fillRect(bx - 260, 600, 520, 520); ctx.restore(); }
  }
}
// cartoon wall clock. h = hours (float), m = minutes. accent = rim colour.
function drawClock(ctx, x, y, r, h, m, o = {}) {
  const acc = o.rim || '#e0392f';
  ctx.save(); ctx.translate(x, y); if (o.rot) ctx.rotate(o.rot); if (o.sq) ctx.scale(1 + o.sq, 1 - o.sq);
  circle(ctx, 6, 10, r * 1.08); ctx.fillStyle = 'rgba(30,10,20,.25)'; ctx.fill();
  circle(ctx, 0, 0, r * 1.08); fillStroke(ctx, acc, r * .06);
  circle(ctx, 0, 0, r * .9); fillStroke(ctx, o.face || '#fffaf0', r * .03);
  ctx.save(); circle(ctx, 0, 0, r * .9); ctx.clip(); ctx.fillStyle = 'rgba(30,10,40,.07)'; ctx.fillRect(r * .2, -r, r, r * 2); ctx.restore();
  if (o.labels) {
    o.labels.forEach((L, i) => { const a = i / o.labels.length * TAU; text(ctx, L, Math.sin(a) * r * .62, -Math.cos(a) * r * .62, r * .13, i % 2 ? INK : acc, INK, 0, 'Poppins', 700); });
  } else for (let i = 1; i <= 12; i++) { const a = i / 12 * TAU; if (i % 3 === 0) text(ctx, String(i), Math.sin(a) * r * .7, -Math.cos(a) * r * .7, r * .22, INK, INK, 0, 'Poppins', 700); else { circle(ctx, Math.sin(a) * r * .74, -Math.cos(a) * r * .74, r * .035); ctx.fillStyle = INK; ctx.fill(); } }
  const ha = ((h % 12) + m / 60) / 12 * TAU, ma = m / 60 * TAU;
  line(ctx, 0, 0, Math.sin(ha) * r * .45, -Math.cos(ha) * r * .45, r * .085, INK);
  line(ctx, 0, 0, Math.sin(ma) * r * .7, -Math.cos(ma) * r * .7, r * .055, o.hand || INK);
  circle(ctx, 0, 0, r * .08); fillStroke(ctx, acc, r * .03);
  if (o.tag) {
    rrect(ctx, -r * .85, r * 1.18, r * 1.7, r * .5, r * .14); fillStroke(ctx, acc, r * .04);
    text(ctx, o.tag, 0, r * 1.36, r * .2, '#fff', INK, 0, 'Poppins', 700);
    if (o.tagZh) cjkText(ctx, o.tagZh, 0, r * 1.56, r * .15, '#ffe9c0');
  }
  ctx.restore();
}
// stylised globe: grid only, no borders
function globe(ctx, x, y, r, t, rot = 0) {
  circle(ctx, x + 10, y + 16, r); ctx.fillStyle = 'rgba(20,10,40,.25)'; ctx.fill();
  circle(ctx, x, y, r); fillStroke(ctx, '#3a86d8', r * .03);
  ctx.save(); circle(ctx, x, y, r); ctx.clip();
  ctx.strokeStyle = 'rgba(255,255,255,.35)'; ctx.lineWidth = 4;
  for (let i = -3; i <= 3; i++) { const yy = y + i * r * .28; const hw = Math.sqrt(Math.max(0, r * r - (yy - y) ** 2)); ctx.beginPath(); ctx.moveTo(x - hw, yy); ctx.lineTo(x + hw, yy); ctx.stroke(); }
  for (let i = 0; i < 12; i++) { const a = (i / 12 * TAU + rot) % TAU; const sx = Math.cos(a); if (Math.sin(a) < 0) continue; ctx.beginPath(); ctx.ellipse(x, y, Math.abs(sx) * r, r, 0, 0, TAU); ctx.stroke(); }
  ctx.fillStyle = 'rgba(30,20,60,.18)'; ctx.fillRect(x + r * .25, y - r, r, r * 2);
  ctx.restore();
  circle(ctx, x - r * .38, y - r * .42, r * .16); ctx.fillStyle = 'rgba(255,255,255,.3)'; ctx.fill();
  circle(ctx, x, y, r); fillStroke(ctx, null, r * .03);
}
function pin(ctx, x, y, s, col = '#e0392f', drop = 1) {
  const yy = y - (1 - drop) * 600;
  ctx.save(); ctx.translate(x, yy); ctx.scale(s, s);
  ellipse(ctx, 0, 6 + (1 - drop) * 0, 26 * drop, 8 * drop); ctx.fillStyle = 'rgba(20,10,30,.3)'; ctx.fill();
  ctx.beginPath(); ctx.moveTo(0, 0); ctx.bezierCurveTo(-46, -60, -40, -120, 0, -120); ctx.bezierCurveTo(40, -120, 46, -60, 0, 0); fillStroke(ctx, col, 7);
  circle(ctx, 0, -78, 18); fillStroke(ctx, '#fff', 5);
  ctx.restore();
}
function bubble(ctx, x, y, w, h, tailX, tailY, draw, a = 1, think = false) {
  if (a <= 0) return; ctx.save(); ctx.globalAlpha = Math.min(1, a); ctx.translate(x, y); const s = .6 + .4 * backOut(Math.min(1, a)); ctx.scale(s, s);
  if (think) { [[tailX * .35, tailY * .35, 16], [tailX * .65, tailY * .65, 11], [tailX * .9, tailY * .9, 7]].forEach(([bx, by, br]) => { circle(ctx, bx, by, br); fillStroke(ctx, '#fff', 5); }); }
  rrect(ctx, -w / 2, -h / 2, w, h, h * .45); fillStroke(ctx, '#fff', 7);
  if (!think) { ctx.beginPath(); ctx.moveTo(-26, h / 2 - 4); ctx.lineTo(tailX, tailY); ctx.lineTo(26, h / 2 - 4); ctx.closePath(); ctx.fillStyle = '#fff'; ctx.fill(); ctx.beginPath(); ctx.moveTo(-26, h / 2 - 2); ctx.lineTo(tailX, tailY); ctx.lineTo(26, h / 2 - 2); ctx.lineWidth = 7; ctx.strokeStyle = INK; ctx.stroke(); }
  draw(ctx); ctx.restore();
}
function jobCard(ctx, x, y, s, label, col, rot = 0, a = 1) {
  if (a <= 0) return; ctx.save(); ctx.globalAlpha = a; ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s);
  rrect(ctx, -130, -46, 260, 92, 26); fillStroke(ctx, '#fff', 6);
  circle(ctx, -90, 0, 22); fillStroke(ctx, col, 5);
  text(ctx, label, 22, 2, label.length > 8 ? 30 : 36, INK, INK, 0, 'Poppins', 700);
  ctx.restore();
}
function booth(ctx, x, base, s, t, glow = 0) {
  ctx.save(); ctx.translate(x, base); ctx.scale(s, s);
  if (glow > 0) { ctx.save(); ctx.globalCompositeOperation = 'lighter'; const g = ctx.createRadialGradient(0, -300, 40, 0, -300, 700); g.addColorStop(0, `rgba(255,200,120,${.45 * glow})`); g.addColorStop(1, 'rgba(255,200,120,0)'); ctx.fillStyle = g; ctx.fillRect(-700, -1000, 1400, 1400); ctx.restore(); }
  rrect(ctx, -330, -420, 660, 420, 18); fillStroke(ctx, '#f6efe2', 7);
  // awning stripes
  ctx.beginPath(); ctx.moveTo(-380, -420); ctx.lineTo(380, -420); ctx.lineTo(360, -330); ctx.lineTo(-360, -330); ctx.closePath(); ctx.save(); ctx.clip();
  for (let i = 0; i < 12; i++) { ctx.fillStyle = i % 2 ? '#fff' : '#e0392f'; ctx.fillRect(-380 + i * 64, -430, 64, 120); } ctx.restore();
  ctx.beginPath(); ctx.moveTo(-380, -420); ctx.lineTo(380, -420); ctx.lineTo(360, -330); ctx.lineTo(-360, -330); ctx.closePath(); fillStroke(ctx, null, 7);
  for (let i = 0; i < 12; i++) { ctx.beginPath(); ctx.arc(-330 + i * 60, -330, 30, 0, Math.PI); fillStroke(ctx, i % 2 ? '#fff' : '#e0392f', 5); }
  // sign
  rrect(ctx, -250, -640, 500, 170, 40); fillStroke(ctx, '#e0392f', 8);
  ctx.font = `700 96px Poppins`; const lw = ctx.measureText('laowai').width; ctx.font = `900 96px ${CJK}`; const zw = ctx.measureText('吗').width;
  const x0 = -(lw + zw) / 2;
  text(ctx, 'laowai', x0 + lw / 2, -556, 96, '#fff', INK, 0, 'Poppins', 700); cjkText(ctx, '吗', x0 + lw + zw / 2, -556, 92, '#ffe08a');
  line(ctx, -200, -470, -200, -420, 8); line(ctx, 200, -470, 200, -420, 8);
  // counter
  rrect(ctx, -330, -150, 660, 150, 10); fillStroke(ctx, '#c9874a', 7);
  ctx.restore();
}
