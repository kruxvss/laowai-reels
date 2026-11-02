// ---------- laowai Reel 10: "Two clocks" (Kashgar) ----------
const ME = { cols: PAL.red, hat: 'none', belt: false, blush: true };
const PAL2 = { teal: ['#2a9d8f', '#2a9d8f'], orange: ['#f08a2c', '#f6f1e8'] };
const FRIEND = { cols: PAL.green, hat: 'none', belt: false };
const AGENT = { cols: PAL.navy, hat: 'none', belt: false };
const C = (base, extra) => Object.assign({}, base, extra);
const walkLegs = (t, sp = 9, amp = .55) => ({ L: [Math.sin(t * sp) * amp + .05, -Math.max(0, Math.sin(t * sp + 1)) * .7], R: [-Math.sin(t * sp) * amp + .05, -Math.max(0, -Math.sin(t * sp + 1)) * .7] });
const walkArms = (t, sp = 9, amp = .6) => ({ L: [.3 - Math.sin(t * sp) * amp, -.3], R: [.3 + Math.sin(t * sp) * amp, -.3] });
const handheld = (t, a = 4) => shake(t * .35, a, 1, 2);
const cup = (c, k, h, a, side) => { if (k !== 'L') return; c.save(); c.translate(h[0], h[1]); rrect(c, -.04, -.085, .08, .09, .015); fillStroke(c, '#f6f2ea', .012); c.beginPath(); c.arc(.05, -.045, .022, -1.4, 1.4); c.lineWidth = .012; c.strokeStyle = INK; c.stroke(); c.restore(); };
const phoneProp = (c, k, h, a, side) => { if (k !== 'R') return; c.save(); c.translate(h[0], h[1]); c.rotate(-.2); rrect(c, -.035, -.11, .07, .12, .014); fillStroke(c, '#222', .01); rrect(c, -.026, -.1, .052, .095, .008); c.fillStyle = '#7fd0ff'; c.fill(); c.restore(); };

const SHOTS = [];
// A - hook: 9:00 on the clock, pitch-dark street, he looks up at the stars
SHOTS.push({ start: 0, end: 3.6, tr: 'whip', draw(ctx, lt, t) {
  const hh = handheld(t, 3);
  const cam = { x: 540 + hh[0], y: 930 + hh[1] - lt * 12, z: 1.0 + lt * .045, r: Math.sin(t * .5) * .006 };
  street(ctx, t, cam, 1);
  applyCam(ctx, cam, 1);
  const pop = backOut(clamp(lt / .35));
  drawClock(ctx, 540, 520, 200 * pop, 9, 0, { rim: '#e0392f', sq: .05 * Math.sin(lt * 18) * Math.exp(-lt * 3) });
  if (lt > .3) { const a = clamp((lt - .3) * 4); text(ctx, '9:00 AM', 540, 830, 92, '#ffe08a', INK, 16, 'Poppins', 700); }
  const look = kf(lt, [[0, 0], [1.4, 0], [1.7, 1]]);
  const yawn = lt > 2.1 && lt < 2.9;
  drawStick(ctx, C(ME, { x: 540, y: 1640, s: 640, bob: Math.sin(t * 3) * .004, headTilt: -.12 * look,
    arms: { L: { ik: [-.12, -.62], bend: -1 }, R: yawn ? [2.5, .4] : [.3, -.15] }, prop: cup,
    face: yawn ? { eyes: 'squint', mouth: 'o', browAng: -.2 } : { eyes: look > .5 ? 'wide' : 'normal', look: [0, -1 * look], mouth: look > .5 ? 'o' : 'flat', browUp: look } }));
  if (lt > 1.8) { const a = clamp((lt - 1.8) * 3); ctx.save(); ctx.globalAlpha = a; text(ctx, '?', 760, 1000 - (lt - 1.8) * 30, 120, '#fff', INK, 14, 'Poppins', 700); ctx.restore(); }
} });
// B - the clock spins on, sky warms, sun finally pops up after ten
SHOTS.push({ start: 3.6, end: 7.04, tr: 'whip', draw(ctx, lt, t) {
  const hh = handheld(t, 3);
  const dawn = kf(lt, [[0, 0], [2.9, 1]]);
  const sunY = kf(lt, [[0, 1250], [2.4, 1150], [2.9, 760, backOut]]);
  const cam = { x: 540 + hh[0], y: 900 + hh[1], z: kf(lt, [[0, 1.08], [3.4, 1.0]]), r: 0 };
  street(ctx, t, cam, 1 - dawn, { sun: sunY });
  applyCam(ctx, cam, 1);
  const hrs = kf(lt, [[0, 9], [2.85, 10.25]]);
  drawClock(ctx, 540, 470, 190, Math.floor(hrs), (hrs % 1) * 60, { rim: '#e0392f' });
  const big = backOut(clamp((lt - 2.85) / .3));
  if (big > 0) { ctx.save(); ctx.translate(540, 760); ctx.scale(big, big); text(ctx, 'AFTER 10:00', 0, 0, 96, '#fff', INK, 16, 'Poppins', 700); ctx.restore(); }
  if (lt > 2.85) burst(ctx, 540, 760 + 80, 70 * clamp((lt - 2.85) * 4), 12, '#ffd23a', 5, .5);
  const cheer = lt > 2.9;
  drawStick(ctx, C(ME, { x: 300, y: 1560, s: 640, squash: cheer ? kf(lt, [[2.9, .85], [3.2, 1, backOut]]) : 1, bob: cheer ? -Math.abs(Math.sin(t * 9)) * .03 : 0,
    arms: cheer ? POSE.handsUp.arms : { L: { ik: [-.12, -.62], bend: -1 }, R: [.4, -.2] }, prop: cheer ? null : cup,
    face: cheer ? { eyes: 'happy', mouth: 'grin', browUp: 1 } : { eyes: 'half', mouth: 'flat', look: [.6, -.6] } }));
} });
// C - zoom out to the globe: pin drops on Kashgar, far west
SHOTS.push({ start: 7.04, end: 9.84, tr: 'whip', draw(ctx, lt, t) {
  const hh = handheld(t, 2);
  const cam = { x: 540 + hh[0], y: 900 + hh[1], z: kf(lt, [[0, 1.35], [1.0, 1.0]]), r: 0 };
  applyCam(ctx, cam, .1); drawSky(ctx, '#2b2a6a', '#7a5cc8');
  stars(ctx, .8, t);
  applyCam(ctx, cam, 1);
  globe(ctx, 540, 820, 380, t, t * .2);
  const drop = elastic(clamp((lt - .3) / .7));
  pin(ctx, 330, 700, 1.2, '#ffd23a', drop);
  if (lt > .9) { const a = backOut(clamp((lt - .9) / .3)); ctx.save(); ctx.translate(330, 470); ctx.scale(a, a); rrect(ctx, -170, -70, 340, 140, 40); fillStroke(ctx, '#e0392f', 7); text(ctx, 'KASHGAR', 0, -18, 56, '#fff', INK, 0, 'Poppins', 700); cjkText(ctx, '喀什', 0, 34, 40, '#ffe08a'); ctx.restore(); }
  // little traveller on top of the globe pointing west
  drawStick(ctx, C(ME, { x: 640, y: 450, s: 260, shadowScale: .6, arms: { L: [1.6, .1], R: [.3, -.2] }, face: { eyes: 'wide', mouth: 'grin', look: [-1, 0], turn: -.5 } }));
} });
// D - five clocks on a long wall, then they all snap to one: Beijing time
SHOTS.push({ start: 9.84, end: 16.0, tr: 'whip', draw(ctx, lt, t) {
  const hh = handheld(t, 3);
  const snap = clamp((lt - (13.9 - 9.84)) / .35);
  const camX = kf(lt, [[0, 240], [3.0, 840], [4.2, 540]]);
  const cam = { x: camX + hh[0], y: 930 + hh[1], z: kf(lt, [[0, 1.25], [3.0, 1.25], [4.2, .78]]), r: 0 };
  applyCam(ctx, cam, .2); drawSky(ctx, '#5bb8f0', '#ffe8c4');
  applyCam(ctx, cam, 1);
  rrect(ctx, -700, 300, 2500, 900, 20); fillStroke(ctx, '#e3b07a', 7);
  ctx.save(); rrect(ctx, -700, 300, 2500, 900, 20); ctx.clip(); for (let i = 0; i < 40; i++) { ctx.fillStyle = 'rgba(120,70,40,.15)'; rrect(ctx, -700 + (i * 157) % 2500, 340 + (i * 89) % 800, 60, 10, 4); ctx.fill(); } ctx.restore();
  ctx.fillStyle = '#c79a6e'; ctx.fillRect(-1000, 1200, 3000, 1200);
  const cols = ['#4aa0ff', '#44d0b0', '#f2c040', '#ff8a40', '#ff4a6a'];
  for (let i = 0; i < 5; i++) {
    const x = -340 + i * 360; const appear = backOut(clamp((lt - (11.6 - 9.84) + .15 - i * .12) / .3));
    if (appear <= 0) continue;
    const hOwn = 8 + i, h = lerp(hOwn, 12, snap);
    const shakeX = snap > 0 && snap < 1 ? Math.sin(lt * 80 + i) * 8 : 0;
    ctx.save(); ctx.translate(x + shakeX, 660); ctx.scale(appear, appear); drawClock(ctx, 0, 0, 140, h, 0, { rim: snap >= 1 ? '#e0392f' : cols[i] }); ctx.restore();
    text(ctx, `UTC+${5 + i}`, x, 880, 44, snap >= 1 ? '#bbb' : '#fff', INK, 10, 'Poppins', 700);
  }
  if (snap >= 1) { const a = backOut(clamp((lt - (14.6 - 9.84)) / .3)); ctx.save(); ctx.translate(360, 1020); ctx.scale(a, a); rrect(ctx, -420, -80, 840, 160, 50); fillStroke(ctx, '#e0392f', 8); text(ctx, 'BEIJING TIME', 0, -18, 70, '#fff', INK, 0, 'Poppins', 700); cjkText(ctx, '北京时间', 0, 42, 40, '#ffe08a'); ctx.restore(); }
  if (snap > 0 && snap < 1) burst(ctx, 360, 660, 300 * snap, 14, '#fff3a0', 9, .6);
  // he walks along the wall, dazed by the count
  const wx = kf(lt, [[0, -100], [3.0, 1000], [4.2, 760]]);
  drawStick(ctx, C(ME, { x: wx, y: 1560, s: 560, legs: lt < 4.2 ? walkLegs(t) : POSE.idle.legs, arms: lt < 4.2 ? walkArms(t) : POSE.hips.arms,
    face: snap > 0 ? { eyes: 'wide', mouth: 'o', browUp: 1, look: [-1, -.5] } : { eyes: 'normal', mouth: 'smile', look: [0, -1] } }));
} });
// E - shop wall with two clocks, friend points to the second one
SHOTS.push({ start: 16.0, end: 20.8, tr: 'whip', draw(ctx, lt, t) {
  const hh = handheld(t, 3);
  const cam = { x: 540 + hh[0], y: 900 + hh[1], z: kf(lt, [[0, 1.0], [4.6, 1.1]]), r: 0 };
  street(ctx, t, cam, 0, { lamps: [] });
  applyCam(ctx, cam, 1);
  rrect(ctx, 80, 300, 920, 640, 26); fillStroke(ctx, '#8a5530', 8);
  drawClock(ctx, 320, 560, 170, 12, 0, { rim: '#e0392f', tag: 'BEIJING', tagZh: '北京时间' });
  const second = backOut(clamp((lt - (18.2 - 16.0)) / .35));
  const back = kf(lt, [[3.4, 0], [4.0, 1]]);
  if (second > 0) { ctx.save(); ctx.translate(760, 560); ctx.scale(second, second); drawClock(ctx, 0, 0, 170, lerp(12, 10, back), 0, { rim: '#2f63c9', tag: 'XINJIANG', tagZh: '新疆时间' }); ctx.restore(); }
  if (back > .9) { const a = backOut(clamp((lt - 4.0) / .25)); ctx.save(); ctx.translate(760, 300); ctx.scale(a, a); rrect(ctx, -110, -50, 220, 100, 40); fillStroke(ctx, '#ffd23a', 6); text(ctx, '-2 HRS', 0, 2, 50, INK, INK, 0, 'Poppins', 700); ctx.restore(); }
  const point = second > 0;
  drawStick(ctx, C(FRIEND, { x: 820, y: 1560, s: 600, flip: -1, arms: point ? { L: [.3, -.2], R: [2.4, .6] } : POSE.idle.arms, face: { eyes: 'normal', mouth: 'grin', look: [.4, -.6], browUp: .5 } }));
  drawStick(ctx, C(ME, { x: 270, y: 1580, s: 620, headTilt: point ? .1 : 0, arms: POSE.idle.arms, face: point ? { eyes: 'wide', mouth: 'o', look: [1, -.8], browUp: 1 } : { eyes: 'normal', mouth: 'smile', look: [.8, -.6] } }));
} });
// F - SAME CITY. TWO CLOCKS. (pattern interrupt, big type)
SHOTS.push({ start: 20.8, end: 22.88, tr: 'whip', draw(ctx, lt, t) {
  const cam = { x: 540, y: 960, z: kf(lt, [[0, 1.05], [2.0, 1.0]]), r: 0 };
  applyCam(ctx, cam, 1);
  const g = ctx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, '#ffd27a'); g.addColorStop(1, '#ff8a5a'); ctx.fillStyle = g; ctx.fillRect(-200, -200, W + 400, H + 400);
  const a1 = backOut(clamp(lt / .3)); ctx.save(); ctx.translate(540, 380); ctx.scale(a1, a1); text(ctx, 'SAME CITY', 0, 0, 130, '#fff', INK, 18, 'Poppins', 700); ctx.restore();
  const two = clamp((lt - (21.6 - 20.8)) / .3);
  const sh = two > 0 && two < 1 ? shake(t, 20) : [0, 0];
  ctx.save(); ctx.translate(sh[0], sh[1]);
  drawClock(ctx, lerp(540, 290, backOut(two)), 840, 220 * (two > 0 ? 1 : .001), 12, 0, { rim: '#e0392f', rot: -.12 * (1 - two) });
  drawClock(ctx, lerp(540, 790, backOut(two)), 840, 220 * (two > 0 ? 1 : .001), 10, 0, { rim: '#2f63c9', rot: .12 * (1 - two) });
  ctx.restore();
  if (two > 0) { const a2 = backOut(two); ctx.save(); ctx.translate(540, 1150); ctx.scale(a2, a2); text(ctx, 'TWO CLOCKS', 0, 0, 120, '#ffe08a', INK, 18, 'Poppins', 700); ctx.restore(); }
} });
// G - "see you at noon!" ... "which noon?"
SHOTS.push({ start: 22.88, end: 26.4, tr: 'whip', draw(ctx, lt, t) {
  const hh = handheld(t, 3);
  const cam = { x: 540 + hh[0], y: 960 + hh[1], z: kf(lt, [[0, 1.0], [3.4, 1.12]]), r: 0 };
  street(ctx, t, cam, 0, { lamps: [980] });
  applyCam(ctx, cam, 1);
  const say = clamp((lt - .1) / .3), which = clamp((lt - (25.4 - 22.88)) / .3);
  bubble(ctx, 300, 520, 520, 190, 60, 160, c => { text(c, 'see you at', 0, -34, 52, INK, INK, 0, 'Poppins', 700); text(c, 'NOON!', 0, 36, 70, '#e0392f', INK, 0, 'Poppins', 700); }, say * (1 - which * .6));
  if (which > 0) bubble(ctx, 780, 560, 420, 320, -60, 260, c => { drawClock(c, -95, -10, 85, 12, 0, { rim: '#e0392f' }); drawClock(c, 95, -10, 85, 10, 0, { rim: '#2f63c9' }); text(c, '?', 0, -10, 90, INK, INK, 0, 'Poppins', 700); }, which, true);
  drawStick(ctx, C(FRIEND, { x: 260, y: 1580, s: 600, arms: { L: [.3, -.2], R: [2.6 + Math.sin(t * 10) * .3, .3] }, face: { eyes: 'happy', mouth: 'grin' } }));
  const conf = which > 0;
  drawStick(ctx, C(ME, { x: 800, y: 1580, s: 620, flip: -1, headTilt: conf ? Math.sin(t * 6) * .1 : 0,
    arms: conf ? { L: [.3, -.2], R: { ik: [.05, -.8], bend: -1 } } : POSE.idle.arms,
    face: conf ? { eyes: 'spiral', mouth: 'flat', browAng: .3 } : { eyes: 'normal', mouth: 'smile', look: [1, 0] } }));
  if (conf) { sweat(ctx, 930, 900, 40, clamp((lt - 2.7) * 3)); }
} });
// H - One country, one clock: the two clocks smash into one
SHOTS.push({ start: 26.4, end: 28.64, tr: 'cut', draw(ctx, lt, t) {
  const hit = (27.5 - 26.4);
  const p = clamp(lt / hit);
  const sh = lt > hit && lt < hit + .35 ? shake(t, 26 * (1 - (lt - hit) / .35)) : [0, 0];
  const cam = { x: 540 + sh[0], y: 900 + sh[1], z: kf(lt, [[0, 1.0], [hit, 1.05], [hit + .1, 1.15], [2.2, 1.08]]), r: 0 };
  applyCam(ctx, cam, .2); const g = ctx.createRadialGradient(540, 800, 100, 540, 900, 1400); g.addColorStop(0, '#ffe2a0'); g.addColorStop(1, '#ff7a4a'); ctx.fillStyle = g; ctx.fillRect(-600, -600, 2400, 3200);
  applyCam(ctx, cam, 1);
  if (lt < hit) {
    drawClock(ctx, lerp(200, 470, easeIn(p)), 760, 220, 12, 0, { rim: '#e0392f', rot: -.3 * (1 - p) });
    drawClock(ctx, lerp(880, 610, easeIn(p)), 760, 220, lerp(10, 12, p), 0, { rim: '#2f63c9', rot: .3 * (1 - p) });
  } else {
    burst(ctx, 540, 760, 420 * clamp((lt - hit) / .2), 14, '#fff3a0', 3, .55);
    const sq = Math.exp(-(lt - hit) * 6) * Math.sin((lt - hit) * 30) * .15;
    drawClock(ctx, 540, 760, 290, 12, 0, { rim: '#e0392f', sq });
    const a = backOut(clamp((lt - hit - .05) / .3)); ctx.save(); ctx.translate(540, 1150); ctx.scale(a, a); text(ctx, 'ONE CLOCK', 0, 0, 120, '#fff', INK, 18, 'Poppins', 700); ctx.restore();
  }
  if (lt < hit) { const a = backOut(clamp(lt / .3)); ctx.save(); ctx.translate(540, 300); ctx.scale(a, a); text(ctx, 'ONE COUNTRY', 0, 0, 110, '#fff', INK, 16, 'Poppins', 700); ctx.restore(); }
  if (lt > hit && lt < hit + .08) { ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.fillStyle = 'rgba(255,255,255,.7)'; ctx.fillRect(0, 0, W, H); ctx.restore(); }
} });
// I - one place: job cards and people fly in to the laowai booth
SHOTS.push({ start: 28.64, end: 32.08, tr: 'whip', draw(ctx, lt, t) {
  const hh = handheld(t, 3);
  const cam = { x: 540 + hh[0], y: 980 + hh[1], z: kf(lt, [[0, 1.2], [1.2, 1.0], [3.4, .95]]), r: 0 };
  street(ctx, t, cam, 0, { lamps: [] });
  applyCam(ctx, cam, 1);
  booth(ctx, 540, 1180, 1.0, t, clamp(lt / .8));
  const jobs = [['CASTING', '#e0392f'], ['TV HOST', '#2f63c9'], ['MODEL', '#f2b52a'], ['VOICE-OVER', '#3fa35b'], ['LIVESTREAM', '#7a4bc4'], ['SHOOT', '#f08a2c']];
  const tJob = 30.56 - 28.64, tAg = 31.44 - 28.64;
  jobs.forEach(([lab, col], i) => {
    const t0 = tJob - .5 + i * .12; const p = clamp((lt - t0) / .5); if (p <= 0) return;
    const sx = i % 2 ? 1300 : -220, sy = 220 + i * 120;
    const tx = 540 + ((i % 3) - 1) * 270, ty = 300 + Math.floor(i / 3) * 120;
    jobCard(ctx, lerp(sx, tx, backOut(p)), lerp(sy, ty, backOut(p)), .95, lab, col, (1 - p) * (i % 2 ? .6 : -.6));
  });
  // people arrive: talent from the left, agents from the right
  const run = (x0, x1, t0, ch, i) => { const p = clamp((lt - t0) / .7); const x = lerp(x0, x1, easeOut(p)); const moving = p < 1;
    drawStick(ctx, C(ch, { x, y: 1600 - (i % 2) * 40, s: 360, flip: x1 < x0 ? -1 : 1, legs: moving ? walkLegs(t + i, 14, .7) : POSE.idle.legs, arms: moving ? walkArms(t + i, 14) : (lt > tAg + .4 ? POSE.handsUp.arms : POSE.idle.arms),
      face: { eyes: lt > tAg + .4 ? 'happy' : 'normal', mouth: 'grin', look: [x1 > x0 ? 1 : -1, 0] } })); };
  run(-200, 170, tJob - .4, ME, 0); run(-300, 330, tJob - .2, C(ME, { cols: PAL.yellow }), 1);
  run(1300, 760, tAg - .5, AGENT, 2); run(1400, 920, tAg - .3, C(AGENT, { cols: PAL.purple }), 3);
} });
// J - end card
SHOTS.push({ start: 32.08, end: 34.2, tr: 'cut', draw(ctx, lt, t) {
  const cam = { x: 540, y: 960, z: kf(lt, [[0, 1.08], [2.0, 1.0]]), r: 0 };
  applyCam(ctx, cam, 1);
  const g = ctx.createLinearGradient(0, -200, 0, H + 200); g.addColorStop(0, '#d8342b'); g.addColorStop(1, '#9a1414'); ctx.fillStyle = g; ctx.fillRect(-300, -300, W + 600, H + 600);
  drawSun(ctx, 540, kf(lt, [[0, 1500], [.8, 1180, backOut]]), 120, t, .9);
  ctx.fillStyle = '#7a0e10'; ctx.fillRect(-300, 1260, W + 600, 900);
  const a = backOut(clamp(lt / .35)); ctx.save(); ctx.translate(540, 520); ctx.scale(a, a);
  ctx.font = '700 180px Poppins'; const lw = ctx.measureText('laowai').width;
  text(ctx, 'laowai', -95, 0, 180, '#fff', INK, 20, 'Poppins', 700);
  rrect(ctx, lw / 2 - 60, -100, 190, 190, 40); fillStroke(ctx, '#fff', 12); cjkText(ctx, '吗', lw / 2 + 35, -2, 150, '#d8342b');
  ctx.restore();
  const b = backOut(clamp((lt - .3) / .3)); ctx.save(); ctx.translate(540, 760); ctx.scale(b, b); rrect(ctx, -250, -62, 500, 124, 62); fillStroke(ctx, '#fff', 10); text(ctx, 'laowai.ma', 0, 2, 76, '#d8342b', INK, 0, 'Poppins', 700); ctx.restore();
  if (lt > .6) { ctx.save(); ctx.globalAlpha = clamp((lt - .6) * 3); text(ctx, 'every job. every agent. one place.', 540, 905, 48, '#fff', INK, 0, 'Poppins', 700); cjkText(ctx, '外国人才的工作与经纪人，一站汇集', 540, 975, 40, '#ffd9b0'); ctx.restore(); }
  drawStick(ctx, C(ME, { x: 360, y: 1560 - Math.abs(Math.sin(t * 8)) * 30, s: 420, arms: { L: [.3, -.2], R: [2.6 + Math.sin(t * 12) * .35, .3] }, face: { eyes: 'happy', mouth: 'grin', browUp: 1 } }));
  drawStick(ctx, C(FRIEND, { x: 720, y: 1560 - Math.abs(Math.sin(t * 8 + 1.5)) * 30, s: 420, flip: -1, arms: { L: [.3, -.2], R: [2.6 + Math.sin(t * 12 + 1) * .35, .3] }, face: { eyes: 'happy', mouth: 'grin', browUp: 1 } }));
} });
