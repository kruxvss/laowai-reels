// ---------- laowai: "This is not Paris" (Tianducheng) ----------
const ME = { cols: PAL.red, hat: 'none', belt: false, blush: true };
const FRIEND = { cols: PAL.green, hat: 'none', belt: false };
const BAG = { cols: PAL.navy, hat: 'none', belt: false };       // the baguette guy (running gag)
const MIME = { cols: ['#222', '#f6f1e8'], hat: 'none', belt: false };
const GROOM = { cols: ['#2b2230', '#2b2230'], hat: 'none', belt: false };
const BRIDE = { cols: ['#fffaf4', '#fffaf4'], hat: 'none', belt: false, blush: true };
const C = (base, extra) => Object.assign({}, base, extra);
const walkLegs = (t, sp = 9, amp = .55) => ({ L: [Math.sin(t * sp) * amp + .05, -Math.max(0, Math.sin(t * sp + 1)) * .7], R: [-Math.sin(t * sp) * amp + .05, -Math.max(0, -Math.sin(t * sp + 1)) * .7] });
const walkArms = (t, sp = 9, amp = .6) => ({ L: [.3 - Math.sin(t * sp) * amp, -.3], R: [.3 + Math.sin(t * sp) * amp, -.3] });
const handheld = (t, a = 4) => shake(t * .35, a, 1, 2);
const headPos = (x, y, s) => [x, y - .765 * s];
// the baguette guy strolls across, oblivious, in every shot
function bagGuy(ctx, lt, dur, y, s, dir = 1, t = 0, face) {
  const x = dir > 0 ? lerp(-200, 1280, lt / dur) : lerp(1280, -200, lt / dur);
  drawStick(ctx, C(BAG, { x, y, s, flip: dir, legs: walkLegs(t, 7, .45), arms: { L: [.3 - Math.sin(t * 7) * .4, -.3], R: [.9, -1.6] }, prop: bagProp, face: face || { eyes: 'happy', mouth: 'smile' } }));
  const [hx, hy] = headPos(x, y, s); beret(ctx, hx + dir * s * .02, hy - s * .17, s * .14);
}
// mime trapped in an invisible box, pressing the walls (second gag)
function mime(ctx, x, y, s, t, free = 0) {
  const p = Math.sin(t * 3);
  if (!free) mimeBox(ctx, x, y, s, t);
  drawStick(ctx, C(MIME, { x: x + (free ? free * 400 : 0), y, s, legs: free ? walkLegs(t, 14, .7) : POSE.idle.legs,
    arms: free ? POSE.handsUp.arms : { L: [1.6 + p * .2, -1.4], R: [1.6 - p * .2, -1.4] },
    face: free ? { eyes: 'happy', mouth: 'grin' } : { eyes: 'wide', mouth: 'frown', browAng: -.3 } }));
}
function parisStreet(ctx, t, cam, o = {}) {
  applyCam(ctx, cam, .06); parisSky(ctx, o.top || '#7cc6f2', o.bot || '#ffe6c4');
  applyCam(ctx, cam, .12); drawCloud(ctx, 200 + t * 6, 260, 110, 1); drawCloud(ctx, 860 + t * 4, 180, 80, 2);
  applyCam(ctx, cam, .3); if (o.paddies) paddies(ctx, 900, t); eiffel(ctx, 540, o.towerBase || 1000, o.towerH || 820);
  applyCam(ctx, cam, 1);
  const em = o.empty || 0;
  haussmann(ctx, -280, 1200, 440, 760, 1, em); haussmann(ctx, 880, 1200, 480, 720, 2, em);
  ctx.fillStyle = em > .5 ? '#a8a4a0' : '#d9cdb6'; ctx.fillRect(-600, 1200, 2400, 1400);
  for (let i = 0; i < 8; i++) line(ctx, -600, 1230 + i * i * 15, 1800, 1230 + i * i * 15, 3, 'rgba(80,60,40,.18)');
}

const SHOTS = [];
// A - hook: Paris... stamped NOT PARIS
SHOTS.push({ start: 0, end: 1.2, tr: 'whip', draw(ctx, lt, t) {
  const hh = handheld(t, 3);
  const cam = { x: 540 + hh[0], y: 860 + hh[1], z: 1.15 - lt * .05, r: 0 };
  parisStreet(ctx, t, cam);
  applyCam(ctx, cam, 1);
  mime(ctx, 860, 1480, 380, t);
  drawStick(ctx, C(ME, { x: 300, y: 1580, s: 520, arms: { L: [.3, -.2], R: [2.3, .3] }, face: { eyes: 'happy', mouth: 'grin' } }));
  const [hx, hy] = headPos(300, 1580, 520); beret(ctx, hx, hy - 88, 72);
  const st = clamp((lt - .32) / .18);
  if (st > 0) { const sc = lerp(2.4, 1, easeOut(st)); ctx.save(); ctx.translate(540, 560); ctx.rotate(-.18); ctx.scale(sc, sc); ctx.globalAlpha = Math.min(1, st * 2);
    rrect(ctx, -400, -110, 800, 220, 26); ctx.lineWidth = 20; ctx.strokeStyle = '#e0392f'; ctx.stroke(); text(ctx, 'NOT PARIS', 0, 6, 150, '#e0392f', '#fff', 0, 'Poppins', 700); ctx.restore(); }
  if (st > 0 && st < 1) { ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.fillStyle = `rgba(255,255,255,${.5 * (1 - st)})`; ctx.fillRect(0, 0, W, H); ctx.restore(); }
} });
// B - pull back: rice paddies around it, pin on Hangzhou; tower, fountain, apartments; selfie guy falls in
SHOTS.push({ start: 1.2, end: 7.12, tr: 'whip', draw(ctx, lt, t) {
  const hh = handheld(t, 3);
  const pull = ease(clamp(lt / 1.4));
  const cam = { x: 540 + hh[0], y: 900 + hh[1], z: lerp(1.15, .82, pull) + lt * .01, r: 0 };
  applyCam(ctx, cam, .06); parisSky(ctx);
  applyCam(ctx, cam, .3); paddies(ctx, 1060, t); eiffel(ctx, 540, 1080, 820);
  applyCam(ctx, cam, 1);
  haussmann(ctx, -220, 1200, 420, 700, 1); haussmann(ctx, 880, 1200, 440, 680, 2);
  ctx.fillStyle = '#d9cdb6'; ctx.fillRect(-500, 1200, 2100, 520); for (let i = 0; i < 6; i++) { ctx.fillStyle = i % 2 ? '#7bc65a' : '#9ad86c'; ctx.fillRect(-2000, 1720 + i * 90, 5000, 90); } ctx.fillStyle = '#9ad86c'; ctx.fillRect(-2000, 1200, 1500, 600); ctx.fillRect(1600, 1200, 1500, 600);
  const fp = backOut(clamp((lt - (4.88 - 1.2)) / .35));
  if (fp > 0) { ctx.save(); ctx.translate(560, 1500); ctx.scale(fp, fp); fountain(ctx, 0, 0, 1, t, 0); ctx.restore(); }
  // selfie guy backs into the fountain
  const back = clamp((lt - 4.1) / .7), fall = clamp((lt - 4.8) / .4);
  if (fp > 0) {
    if (fall < 1) drawStick(ctx, C(ME, { x: lerp(860, 760, back), y: 1540 + fall * 60, s: 300, lean: -fall * 1.2, flip: -1, arms: { L: [.3, -.2], R: [2.0, -.4] }, prop: phoneUp, face: fall > 0 ? { eyes: 'wide', mouth: 'o' } : { eyes: 'happy', mouth: 'grin' } }));
    if (fall >= 1) { fountain(ctx, 560, 1500, 1, t, clamp((lt - 5.2) / .5)); const legsUp = { L: [2.9, .2], R: [3.2, .1] }; ctx.save(); ctx.translate(720, 1460); ctx.rotate(Math.PI); drawStick(ctx, C(ME, { x: 0, y: 0, s: 220, legs: legsUp, shadow: false, face: { eyes: 'x', mouth: 'o' } })); ctx.restore(); }
  }
  bagGuy(ctx, lt, 5.9, 1680, 260, 1, t);
  // labels
  if (lt > .8) { const a = backOut(clamp((lt - .8) / .3)); ctx.save(); ctx.translate(540, 380); ctx.scale(a, a); rrect(ctx, -300, -80, 600, 160, 50); fillStroke(ctx, '#e0392f', 8); text(ctx, 'HANGZHOU', 0, -20, 74, '#fff', INK, 0, 'Poppins', 700); cjkText(ctx, '杭州 · 天都城', 0, 44, 42, '#ffe08a'); ctx.restore(); }
  const lab = (word, tt, x, y) => { if (t < tt) return; const a = backOut(clamp((t - tt) / .25)); ctx.save(); ctx.translate(x, y); ctx.scale(a, a); rrect(ctx, -150, -42, 300, 84, 40); fillStroke(ctx, '#fff', 6); text(ctx, word, 0, 2, 40, INK, INK, 0, 'Poppins', 700); ctx.restore(); };
  lab('EIFFEL TOWER', 3.76, 540, 620); lab('FOUNTAINS', 4.88, 300, 1080); lab('APARTMENTS', 5.6, 860, 820);
} });
// C - opened 2007 for 10,000 people: ribbon cutting + people icons filling
SHOTS.push({ start: 7.12, end: 11.04, tr: 'whip', draw(ctx, lt, t) {
  const hh = handheld(t, 3);
  const cam = { x: 540 + hh[0], y: 940 + hh[1], z: 1.0 + lt * .02, r: 0 };
  parisStreet(ctx, t, cam);
  applyCam(ctx, cam, 1);
  const cut = clamp((lt - .55) / .2);
  // ribbon
  if (cut < 1) { line(ctx, 120, 1300, 960, 1300, 22, '#e0392f'); } else { line(ctx, 120, 1300, 520, 1300 + (lt - .75) * 200, 22, '#e0392f'); line(ctx, 560, 1300 + (lt - .75) * 200, 960, 1300, 22, '#e0392f'); }
  drawStick(ctx, C(FRIEND, { x: 540, y: 1600, s: 480, arms: { L: [.3, -.2], R: [1.6, -.4] }, face: { eyes: cut >= 1 ? 'happy' : 'normal', mouth: 'grin' } }));
  // giant scissors
  ctx.save(); ctx.translate(640, 1300); ctx.rotate(-.3 + (cut >= 1 ? 0 : Math.sin(t * 20) * .1)); line(ctx, -120, -20, 120, 20, 18, '#c0c8d4'); line(ctx, -120, 20, 120, -20, 18, '#c0c8d4'); circle(ctx, -140, -26, 26); fillStroke(ctx, null, 10); circle(ctx, -140, 26, 26); fillStroke(ctx, null, 10); ctx.restore();
  if (cut >= 1) { for (let i = 0; i < 18; i++) { const R = rng(i + 3); const p = clamp((lt - .75) / 1.5); circle(ctx, 540 + (R() - .5) * 900 * p, 700 + R() * 600 * p + p * p * 200, 9); ctx.fillStyle = ['#e0392f', '#f2b52a', '#2f63c9', '#3fa35b'][i % 4]; ctx.fill(); } }
  const a = backOut(clamp((lt - .6) / .3)); ctx.save(); ctx.translate(540, 360); ctx.scale(a, a); text(ctx, 'OPENED 2007', 0, 0, 104, '#fff', INK, 16, 'Poppins', 700); ctx.restore();
  // capacity counter
  const cp = clamp((lt - (9.6 - 7.12)) / .9);
  if (cp > 0) { const n = Math.round(10000 * easeOut(cp)); ctx.save(); ctx.translate(540, 560); const b = backOut(clamp(cp * 3)); ctx.scale(b, b); rrect(ctx, -330, -90, 660, 180, 60); fillStroke(ctx, '#ffd23a', 8); text(ctx, `FOR ${n.toLocaleString('en-US')}`, 0, -10, 84, INK, INK, 0, 'Poppins', 700); text(ctx, 'people', 0, 56, 40, INK, INK, 0, 'Poppins', 700); ctx.restore(); }
  bagGuy(ctx, lt, 3.9, 1760, 300, -1, t);
} });
// D - only 2,000 moved in: empty windows, one hopeful guy waving from a balcony
SHOTS.push({ start: 11.04, end: 14.08, tr: 'whip', draw(ctx, lt, t) {
  const hh = handheld(t, 3);
  const cam = { x: 540 + hh[0], y: 960 + hh[1], z: 1.0 + lt * .03, r: 0 };
  applyCam(ctx, cam, .06); parisSky(ctx, '#9cc8e0', '#efe2cc');
  applyCam(ctx, cam, 1);
  haussmann(ctx, 90, 1500, 900, 1200, 7, 1);
  // the one lit window with a guy waving
  rrect(ctx, 600, 560, 120, 160, [50, 50, 6, 6]); fillStroke(ctx, '#ffe28a', 6);
  drawStick(ctx, C(FRIEND, { x: 660, y: 760, s: 200, shadow: false, arms: { L: [.3, -.2], R: [2.6 + Math.sin(t * 12) * .4, .3] }, face: { eyes: 'happy', mouth: 'grin' } }));
  const cnt = clamp((lt - (12.4 - 11.04)) / .7); const n = Math.round(lerp(10000, 2000, easeOut(cnt)));
  ctx.save(); ctx.translate(540, 300); rrect(ctx, -320, -80, 640, 160, 50); fillStroke(ctx, cnt > .9 ? '#e0392f' : '#fff', 8); text(ctx, n.toLocaleString('en-US'), 0, 4, 100, cnt > .9 ? '#fff' : INK, INK, 0, 'Poppins', 700); ctx.restore();
  if (cnt > .9) { text(ctx, 'moved in', 540, 430, 52, '#fff', INK, 10, 'Poppins', 700); }
  bagGuy(ctx, lt, 3.0, 1800, 300, 1, t);
} });
// E - ghost town: tumbleweed, lonely bench guy, the mime is STILL in the box
SHOTS.push({ start: 14.08, end: 17.12, tr: 'whip', draw(ctx, lt, t) {
  const hh = handheld(t, 2);
  const cam = { x: 540 + hh[0], y: 900 + hh[1], z: 1.05 + lt * .03, r: 0 };
  parisStreet(ctx, t, cam, { empty: 1, top: '#a8b4c4', bot: '#e0dcd4' });
  applyCam(ctx, cam, 1);
  ctx.save(); ctx.globalCompositeOperation = 'multiply'; ctx.fillStyle = 'rgba(150,150,170,.35)'; ctx.fillRect(-500, -500, 2200, 3000); ctx.restore();
  tumbleweed(ctx, lerp(-150, 1250, lt / 3.0), 1520 - Math.abs(Math.sin(t * 5)) * 60, 70, t);
  bench(ctx, 280, 1600, 1.1);
  drawStick(ctx, C(ME, { x: 280, y: 1560, s: 360, legs: { L: [1.3, -1.4], R: [1.3, -1.4] }, arms: { L: [.3, -.2], R: [2.5 + Math.sin(t * 6) * .4, .3] }, face: { eyes: 'normal', mouth: 'smile', look: [.5, 0], browAng: -.25 } }));
  if (lt > 1.2) bubble(ctx, 360, 880, 300, 120, -40, 110, c => text(c, 'hello?', 0, 2, 54, INK, INK, 0, 'Poppins', 700), clamp((lt - 1.2) * 4));
  mime(ctx, 820, 1560, 360, t);
  const g = backOut(clamp((t - 16.32) / .3)); if (g > 0) { ctx.save(); ctx.translate(540, 400); ctx.scale(g, g); text(ctx, 'GHOST TOWN', 0, 0, 120, '#e8ecf4', INK, 18, 'Poppins', 700); ctx.restore(); }
} });
// F - "then something nobody planned happened": everyone freezes and turns
SHOTS.push({ start: 17.12, end: 19.04, tr: 'whip', draw(ctx, lt, t) {
  const z = kf(lt, [[0, 1.0], [1.4, 1.35, easeIn]]);
  const cam = { x: 540, y: 1000, z, r: 0 };
  parisStreet(ctx, t, cam, { empty: 1, top: '#a8b4c4', bot: '#e0dcd4' });
  applyCam(ctx, cam, 1);
  const turn = lt > .5;
  drawStick(ctx, C(ME, { x: 280, y: 1560, s: 380, arms: POSE.idle.arms, face: turn ? { eyes: 'wide', mouth: 'o', look: [1, 0], browUp: 1 } : { eyes: 'half', mouth: 'flat' } }));
  mime(ctx, 820, 1560, 380, 0);
  if (turn) { ctx.save(); ctx.globalAlpha = .9; text(ctx, '!', 300, 1020, 140, '#ffd23a', INK, 14, 'Poppins', 700); text(ctx, '!', 840, 1020, 140, '#ffd23a', INK, 14, 'Poppins', 700); ctx.restore(); }
  bagGuy(ctx, lt, 1.9, 1760, 300, -1, t, { eyes: 'wide', mouth: 'o' });
} });
// G - couples in wedding dresses arrive; photographer flat on the ground; one groom faints
SHOTS.push({ start: 19.04, end: 21.36, tr: 'whip', draw(ctx, lt, t) {
  const hh = handheld(t, 3);
  const cam = { x: 540 + hh[0], y: 900 + hh[1], z: 1.0 + lt * .03, r: 0 };
  parisStreet(ctx, t, cam);
  applyCam(ctx, cam, 1);
  const couple = (x, y, s, i, faint = 0) => {
    const d = clamp((lt - i * .25) / .5); const xx = lerp(x + (i % 2 ? 600 : -600), x, easeOut(d));
    dress(ctx, xx - s * .12, y, s); drawStick(ctx, C(BRIDE, { x: xx - s * .12, y, s, legs: { L: [.05, 0], R: [.05, 0] }, arms: { L: [.4, -.3], R: [1.2, -1.2] }, face: { eyes: 'happy', mouth: 'grin' }, shadow: false }));
    const [hx, hy] = headPos(xx - s * .12, y, s); veil(ctx, hx, hy + s * .2, s);
    ctx.save(); if (faint) { ctx.translate(xx + s * .2, y); ctx.rotate(-1.4 * faint); ctx.translate(-(xx + s * .2), -y); }
    drawStick(ctx, C(GROOM, { x: xx + s * .2, y, s, arms: { L: [1.0, -1.0], R: [.3, -.2] }, face: faint ? { eyes: 'spiral', mouth: 'o' } : { eyes: 'happy', mouth: 'smile' } })); ctx.restore();
    heartsPop(ctx, xx, y - s * 1.1, t + i, d);
  };
  couple(300, 1440, 360, 0); couple(800, 1480, 380, 1, clamp((lt - 1.3) / .3));
  // photographer lying on the ground for the low angle
  ctx.save(); ctx.translate(560, 1820); ctx.rotate(-Math.PI / 2); drawStick(ctx, C(ME, { x: 0, y: 0, s: 260, shadow: false, arms: { L: [.3, -.2], R: [1.6, -.4] }, prop: camProp, face: { eyes: 'squint', mouth: 'teeth' } })); ctx.restore();
  bagGuy(ctx, lt, 2.3, 1760, 260, 1, t);
} });
// H - why fly to Paris? plane crossed out; Paris is right here
SHOTS.push({ start: 21.36, end: 24.8, tr: 'whip', draw(ctx, lt, t) {
  const hh = handheld(t, 3);
  const cam = { x: 540 + hh[0], y: 940 + hh[1], z: 1.0 + lt * .02, r: 0 };
  parisStreet(ctx, t, cam);
  applyCam(ctx, cam, 1);
  // plane flying across, then a big red X
  const px = lerp(-200, 1300, clamp(lt / 1.8));
  ctx.save(); ctx.translate(px, 420); rrect(ctx, -140, -24, 280, 48, 24); fillStroke(ctx, '#fff', 6); ctx.beginPath(); ctx.moveTo(-20, -10); ctx.lineTo(40, -110); ctx.lineTo(70, -110); ctx.lineTo(50, -10); ctx.closePath(); fillStroke(ctx, '#e9eef4', 5); ctx.beginPath(); ctx.moveTo(-130, -10); ctx.lineTo(-150, -70); ctx.lineTo(-110, -70); ctx.lineTo(-90, -10); ctx.closePath(); fillStroke(ctx, '#e0392f', 5); ctx.restore();
  if (lt > 1.0) { const a = backOut(clamp((lt - 1.0) / .25)); ctx.save(); ctx.translate(540, 420); ctx.scale(a, a); line(ctx, -160, -120, 160, 120, 30, '#e0392f'); line(ctx, 160, -120, -160, 120, 30, '#e0392f'); ctx.restore(); }
  const here = clamp((lt - (24.08 - 21.36)) / .25);
  if (here > 0) { pin(ctx, 540, 900, 1.3, '#e0392f', elastic(here)); const a = backOut(here); ctx.save(); ctx.translate(540, 1040); ctx.scale(a, a); text(ctx, 'RIGHT HERE', 0, 0, 110, '#fff', INK, 16, 'Poppins', 700); ctx.restore(); }
  dress(ctx, 260, 1600, 400); drawStick(ctx, C(BRIDE, { x: 260, y: 1600, s: 400, legs: { L: [.05, 0], R: [.05, 0] }, arms: { L: [.3, -.2], R: here > 0 ? [2.4, .3] : [.9, -1.8] }, face: { eyes: here > 0 ? 'happy' : 'smug', mouth: 'smirk' }, shadow: false }));
  const [hx, hy] = headPos(260, 1600, 400); veil(ctx, hx, hy + 80, 400);
  mime(ctx, 860, 1600, 360, t);
} });
// I - social media did the rest: crowds with phones, hearts flying, a pigeon chase
SHOTS.push({ start: 24.8, end: 27.76, tr: 'whip', draw(ctx, lt, t) {
  const hh = handheld(t, 4);
  const cam = { x: 540 + hh[0], y: 900 + hh[1], z: kf(lt, [[0, 1.1], [2.9, .95]]), r: 0 };
  parisStreet(ctx, t, cam);
  applyCam(ctx, cam, 1);
  const crowd = clamp((lt - (26.6 - 24.8)) / .8);
  const n = 4 + Math.floor(crowd * 8);
  for (let i = 0; i < n; i++) { const R = rng(i + 30); const x = 80 + R() * 920, y = 1440 + R() * 300, s = 220 + R() * 80;
    drawStick(ctx, C(i % 3 === 0 ? FRIEND : (i % 3 === 1 ? ME : C(ME, { cols: PAL.yellow })), { x, y, s, arms: { L: [.3, -.2], R: [2.0, -.3] }, prop: phoneUp, face: { eyes: 'happy', mouth: 'grin', look: [0, -1] } }));
    heartsPop(ctx, x, y - s * 1.2, t + i * .3, .8); }
  // likes counter
  const likes = Math.round(lerp(12, 98000, easeIn(clamp(lt / 2.8))));
  ctx.save(); ctx.translate(540, 360); rrect(ctx, -280, -70, 560, 140, 70); fillStroke(ctx, '#fff', 8); ctx.beginPath(); ctx.moveTo(-190, 18); ctx.bezierCurveTo(-240, -20, -210, -60, -190, -36); ctx.bezierCurveTo(-170, -60, -140, -20, -190, 18); fillStroke(ctx, '#ff4a6a', 5); text(ctx, likes.toLocaleString('en-US'), 50, 4, 84, INK, INK, 0, 'Poppins', 700); ctx.restore();
  // baguette guy now chased by pigeons
  const bx = lerp(1250, -200, lt / 2.9); bagGuy(ctx, lt, 2.9, 1820, 300, -1, t, { eyes: 'wide', mouth: 'teeth' });
  for (let i = 0; i < 3; i++) pigeon(ctx, bx + 160 + i * 70, 1700 - i * 20, 1.4, t + i, .3 + .2 * Math.sin(t * 9 + i));
} });
// J - closer than you think: guy with a telescope, tower right behind him
SHOTS.push({ start: 27.76, end: 30.72, tr: 'whip', draw(ctx, lt, t) {
  const hh = handheld(t, 3);
  const cam = { x: 540 + hh[0], y: 960 + hh[1], z: 1.0 + lt * .03, r: 0 };
  applyCam(ctx, cam, .06); parisSky(ctx);
  applyCam(ctx, cam, .3); paddies(ctx, 1100, t);
  applyCam(ctx, cam, 1);
  eiffel(ctx, 300, 1560, 1100);
  // telescope pointed away to the right
  ctx.save(); ctx.translate(660, 1260); ctx.rotate(-.25); rrect(ctx, 0, -30, 300, 60, 18); fillStroke(ctx, '#c9874a', 6); rrect(ctx, 260, -40, 80, 80, 12); fillStroke(ctx, '#a06a3a', 6); ctx.restore();
  line(ctx, 760, 1300, 700, 1580, 10); line(ctx, 760, 1300, 820, 1580, 10);
  drawStick(ctx, C(ME, { x: 640, y: 1600, s: 480, lean: .15, arms: { L: { ik: [.2, -.7] }, R: { ik: [.3, -.68] } }, face: { eyes: 'squint', mouth: 'flat', look: [1, 0] } }));
  const tap = lt > 1.5;
  drawStick(ctx, C(FRIEND, { x: 380, y: 1640, s: 420, arms: { L: [.3, -.2], R: tap ? { ik: [.5, -.62] } : [.3, -.2] }, face: { eyes: 'half', mouth: 'smirk', browOne: 1 } }));
  if (tap) { const a = clamp((lt - 1.5) * 4); ctx.save(); ctx.globalAlpha = a; text(ctx, 'tap tap', 560, 960, 46, '#fff', INK, 10, 'Poppins', 700); ctx.restore(); }
} });
// K - like your next job: his phone pings with a casting right here
SHOTS.push({ start: 30.72, end: 32.4, tr: 'whip', draw(ctx, lt, t) {
  const cam = { x: 540, y: 960, z: kf(lt, [[0, 1.0], [1.6, 1.15]]), r: 0 };
  parisStreet(ctx, t, cam);
  applyCam(ctx, cam, 1);
  drawStick(ctx, C(ME, { x: 540, y: 1580, s: 580, arms: { L: [.3, -.2], R: [1.4, -1.6] }, prop: phoneUp, face: { eyes: 'wide', mouth: 'grin', browUp: 1, look: [0, -.5] } }));
  const pop = backOut(clamp((lt - .2) / .3));
  ctx.save(); ctx.translate(540, 520); ctx.scale(pop, pop); rrect(ctx, -320, -110, 640, 220, 50); fillStroke(ctx, '#fff', 8); circle(ctx, -230, 0, 50); fillStroke(ctx, '#e0392f', 6); text(ctx, 'CASTING', 50, -30, 64, INK, INK, 0, 'Poppins', 700); text(ctx, 'HANGZHOU', 50, 40, 46, '#e0392f', INK, 0, 'Poppins', 700); ctx.restore();
  bagGuy(ctx, lt, 1.7, 1900, 300, 1, t);
} });
// L - end card: booth, laowai.ma; the mime finally escapes
SHOTS.push({ start: 32.4, end: 36.4, tr: 'cut', draw(ctx, lt, t) {
  const cam = { x: 540, y: 960, z: kf(lt, [[0, 1.08], [2.0, 1.0]]), r: 0 };
  applyCam(ctx, cam, 1);
  const g = ctx.createLinearGradient(0, -200, 0, H + 200); g.addColorStop(0, '#d8342b'); g.addColorStop(1, '#9a1414'); ctx.fillStyle = g; ctx.fillRect(-300, -300, W + 600, H + 600);
  ctx.save(); ctx.globalAlpha = .25; eiffel(ctx, 540, 1300, 900, '#5a0a0a'); ctx.restore();
  ctx.fillStyle = '#7a0e10'; ctx.fillRect(-300, 1300, W + 600, 900);
  const a = backOut(clamp(lt / .35)); ctx.save(); ctx.translate(540, 480); ctx.scale(a, a);
  ctx.font = '700 180px Poppins'; const lw = ctx.measureText('laowai').width;
  text(ctx, 'laowai', -95, 0, 180, '#fff', INK, 20, 'Poppins', 700);
  rrect(ctx, lw / 2 - 60, -100, 190, 190, 40); fillStroke(ctx, '#fff', 12); cjkText(ctx, '吗', lw / 2 + 35, -2, 150, '#d8342b');
  ctx.restore();
  const b = backOut(clamp((lt - .3) / .3)); ctx.save(); ctx.translate(540, 720); ctx.scale(b, b); rrect(ctx, -250, -62, 500, 124, 62); fillStroke(ctx, '#fff', 10); text(ctx, 'laowai.ma', 0, 2, 76, '#d8342b', INK, 0, 'Poppins', 700); ctx.restore();
  if (lt > .5) { ctx.save(); ctx.globalAlpha = clamp((lt - .5) * 3); text(ctx, 'every job. every agent. one place.', 540, 865, 48, '#fff', INK, 0, 'Poppins', 700); cjkText(ctx, '外国人才的工作与经纪人，一站汇集', 540, 935, 40, '#ffd9b0'); ctx.restore(); }
  drawStick(ctx, C(ME, { x: 300, y: 1620 - Math.abs(Math.sin(t * 8)) * 30, s: 400, arms: { L: [.3, -.2], R: [2.6 + Math.sin(t * 12) * .35, .3] }, face: { eyes: 'happy', mouth: 'grin', browUp: 1 } }));
  // baguette guy waves with the baguette
  drawStick(ctx, C(BAG, { x: 560, y: 1620, s: 380, arms: { L: [.3, -.2], R: [2.6 + Math.sin(t * 10) * .4, .2] }, prop: bagProp, face: { eyes: 'happy', mouth: 'grin' } }));
  { const [hx, hy] = headPos(560, 1620, 380); beret(ctx, hx, hy - 64, 54); }
  // mime finally breaks out and runs off
  const free = clamp((lt - 1.6) / 1.2);
  mime(ctx, 820, 1620, 380, t, free > 0 ? free : 0);
  if (free > 0 && free < .3) { burst(ctx, 820, 1300, 160 * free / .3, 12, '#bfe9ff', 4, .5); }
} });
