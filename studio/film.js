// Reel 10 "Two clocks" (Kashgar). Three.js sets + 2-D editorial type. Pure function of time.
import * as M from './lib/motion.js';
import * as G from './lib/gl.js';
import { makeChar, pose, mat, phys } from './lib/chars.js';
const { THREE } = G;
const { W, H, E, prog, lerp, clamp, font, layout, wobble } = M;

const BRAND = '#C41C1C', GOLD = '#F5C76A';
const S = {};
let WN = [];
const n_ = (w) => w.toLowerCase().replace(/[^a-z0-9]/g, '');
const LS = (li) => Math.min(...WN.filter((w) => w[3] === li).map((w) => w[1]));
const LE = (li) => Math.max(...WN.filter((w) => w[3] === li).map((w) => w[2]));
const tw = (word, li, nth = 0) => { const c = WN.filter((w) => w[3] === li && n_(w[0]) === n_(word)); return c.length ? c[Math.min(nth, c.length - 1)][1] : LS(li); };

// ---------------------------------------------------------------- shared builders
function canvasTex(w, h, draw) {
  const c = document.createElement('canvas'); c.width = w; c.height = h; draw(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t;
}
function makeClock({ label = 'BEIJING', cjk = '北京时间', accent = 0xc41c1c, r = 0.9 } = {}) {
  const g = new THREE.Group();
  const face = canvasTex(512, 512, (c, w) => {
    const gr = c.createRadialGradient(256, 230, 40, 256, 256, 260); gr.addColorStop(0, '#fffaf0'); gr.addColorStop(1, '#efe4cf');
    c.fillStyle = gr; c.fillRect(0, 0, 512, 512);
    c.save(); c.translate(256, 256); c.rotate(-Math.PI / 2); c.translate(-256, -256);
    c.fillStyle = '#2a2420'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = '800 58px Display';
    for (let k = 1; k <= 12; k++) { const a = (k / 12) * Math.PI * 2; c.fillText(String(k), 256 + Math.sin(a) * 190, 256 - Math.cos(a) * 190); }
    for (let k = 0; k < 60; k++) { const a = (k / 60) * Math.PI * 2, r0 = k % 5 ? 228 : 218; c.lineWidth = k % 5 ? 3 : 6; c.strokeStyle = '#4a4038'; c.beginPath(); c.moveTo(256 + Math.sin(a) * r0, 256 - Math.cos(a) * r0); c.lineTo(256 + Math.sin(a) * 240, 256 - Math.cos(a) * 240); c.stroke(); }
    c.restore();
  });
  const disc = new THREE.Mesh(new THREE.CylinderGeometry(r, r, 0.08, 64), [mat(0xe8dcc6), new THREE.MeshStandardMaterial({ map: face, roughness: 0.45 }), mat(0xe8dcc6)]);
  disc.rotation.x = Math.PI / 2; disc.castShadow = true; g.add(disc);
  const rim = new THREE.Mesh(new THREE.TorusGeometry(r + 0.02, 0.07, 20, 80), phys(accent, { roughness: 0.3, clearcoat: 0.8, metalness: 0.2 })); rim.castShadow = true; g.add(rim);
  const glass = new THREE.Mesh(new THREE.SphereGeometry(r, 48, 16, 0, Math.PI * 2, 0, 0.35), new THREE.MeshPhysicalMaterial({ color: 0xffffff, transparent: true, opacity: 0.08, roughness: 0.05, clearcoat: 1 }));
  glass.rotation.x = Math.PI / 2; glass.position.z = -0.55 * r; glass.scale.set(1, 1, 1); g.add(glass);
  const handM = phys(0x1c1814, { roughness: 0.3 });
  const hh = new THREE.Mesh(new THREE.BoxGeometry(0.07, r * 0.5, 0.03), handM); hh.geometry.translate(0, r * 0.22, 0); hh.position.z = 0.07; g.add(hh);
  const mh = new THREE.Mesh(new THREE.BoxGeometry(0.045, r * 0.78, 0.03), handM); mh.geometry.translate(0, r * 0.36, 0); mh.position.z = 0.1; g.add(mh);
  const cap = new THREE.Mesh(new THREE.SphereGeometry(0.06, 16, 12), phys(accent)); cap.position.z = 0.12; g.add(cap);
  const plateT = canvasTex(512, 160, (c) => {
    c.fillStyle = '#' + accent.toString(16).padStart(6, '0'); c.beginPath(); c.roundRect(4, 4, 504, 152, 40); c.fill();
    c.fillStyle = '#fff'; c.textAlign = 'center'; c.font = '800 54px Display'; c.fillText(label, 256, 72);
    c.font = '700 44px "Noto Sans CJK SC"'; c.fillStyle = '#ffe7c0'; c.fillText(cjk, 256, 130);
  });
  const plate = new THREE.Mesh(new THREE.BoxGeometry(r * 1.6, r * 0.5, 0.06), [mat(0x333333), mat(0x333333), mat(0x333333), mat(0x333333), new THREE.MeshStandardMaterial({ map: plateT, roughness: 0.4 }), mat(0x333333)]);
  plate.position.y = -r - 0.42; plate.castShadow = true; g.add(plate);
  g.userData = { hh, mh, setTime(hours, minutes = 0) { const hm = hours + minutes / 60; hh.rotation.z = -(hm % 12) / 12 * Math.PI * 2; mh.rotation.z = -(minutes / 60) * Math.PI * 2; } };
  return g;
}

// ---------------------------------------------------------------- street set (Kashgar old-town style, neutral)
function streetSet() {
  const scene = new THREE.Scene(), cam = G.camera(36, 0.05, 200);
  scene.environment = G.ENV; scene.environmentIntensity = 0.2;
  scene.fog = new THREE.Fog(0x101830, 12, 55);
  const skyU = { top: { value: new THREE.Color() }, bot: { value: new THREE.Color() } };
  const sky = new THREE.Mesh(new THREE.SphereGeometry(90, 32, 16), new THREE.ShaderMaterial({ side: THREE.BackSide, fog: false, uniforms: skyU,
    vertexShader: 'varying vec3 vp; void main(){ vp = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
    fragmentShader: 'uniform vec3 top; uniform vec3 bot; varying vec3 vp; void main(){ float h = clamp(vp.y*1.6+0.25,0.0,1.0); gl_FragColor = vec4(mix(bot, top, h),1.0); }' }));
  scene.add(sky);
  // stars
  const sg = new THREE.BufferGeometry(); const sp = new Float32Array(900); const r = M.mulberry32(3);
  for (let i = 0; i < 300; i++) { const a = r() * Math.PI * 2, e = 0.15 + r() * 1.2; sp[i * 3] = Math.cos(a) * Math.cos(e) * 80; sp[i * 3 + 1] = Math.sin(e) * 80; sp[i * 3 + 2] = Math.sin(a) * Math.cos(e) * 80 - 20; }
  sg.setAttribute('position', new THREE.BufferAttribute(sp, 3));
  const starsM = new THREE.PointsMaterial({ color: 0xffffff, size: 0.35, transparent: true, fog: false });
  scene.add(new THREE.Points(sg, starsM));
  const hemi = new THREE.HemisphereLight(0x8aa0ff, 0x302020, 0.4); scene.add(hemi);
  const sun = new THREE.DirectionalLight(0xffb070, 0); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -10, right: 10, top: 10, bottom: -6, near: 1, far: 80 }); sun.shadow.bias = -0.0005; sun.shadow.normalBias = 0.03; sun.shadow.radius = 4;
  scene.add(sun); scene.add(sun.target); sun.target.position.set(0, 0, -4);
  const fill = new THREE.DirectionalLight(0xbcd0ff, 0.5); fill.position.set(3, 4, 10); scene.add(fill);
  const sunDisc = new THREE.Mesh(new THREE.SphereGeometry(3, 32, 16), new THREE.MeshBasicMaterial({ color: 0xffd090, fog: false })); scene.add(sunDisc);
  // ground: paved
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(16, 90), phys(0x8a7058, { roughness: 0.75, clearcoat: 0.1 })); ground.rotation.x = -Math.PI / 2; ground.position.z = -30; ground.receiveShadow = true; scene.add(ground);
  // buildings: mud-brick blocks with arched doorways, wooden doors, balconies
  const wallMs = [mat(0xc9a27a, 0.95), mat(0xb8916a, 0.95), mat(0xd6b48c, 0.95)];
  const doorM = phys(0x5a3420, { roughness: 0.6 }), trimM = mat(0x8a6a4a, 0.8), recessM = mat(0x2a1c14, 0.9);
  const lamps = [];
  const rr = M.mulberry32(17);
  for (const side of [-1, 1]) {
    let z = 4;
    while (z > -60) {
      const d = 3.5 + rr() * 3, h = 4 + rr() * 4;
      const b = new THREE.Mesh(new THREE.BoxGeometry(3, h, d), wallMs[Math.floor(rr() * 3)]); b.position.set(side * 4, h / 2, z - d / 2); b.castShadow = b.receiveShadow = true; scene.add(b);
      // arched door: recess + door + arch
      const dz = z - d / 2;
      const rec = new THREE.Mesh(new THREE.BoxGeometry(0.1, 2.2, 1.3), recessM); rec.position.set(side * 2.52, 1.1, dz); scene.add(rec);
      const door = new THREE.Mesh(new THREE.BoxGeometry(0.08, 2.0, 1.1), doorM); door.position.set(side * 2.56, 1.0, dz); door.castShadow = true; scene.add(door);
      const arch = new THREE.Mesh(new THREE.TorusGeometry(0.65, 0.09, 10, 24, Math.PI), trimM); arch.rotation.y = Math.PI / 2; arch.position.set(side * 2.5, 2.2, dz); scene.add(arch);
      // balcony
      if (rr() < 0.6) { const bal = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.12, d * 0.6), trimM); bal.position.set(side * 2.2, h * 0.7, dz); bal.castShadow = true; scene.add(bal);
        for (let k = 0; k < 5; k++) { const p = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.6, 0.05), trimM); p.position.set(side * 1.9, h * 0.7 + 0.3, dz - d * 0.3 + k * d * 0.15); scene.add(p); } }
      // windows (emissive when dark)
      const winM = new THREE.MeshStandardMaterial({ color: 0x3a2a20, emissive: 0xffb060, emissiveIntensity: 0 });
      for (let k = 0; k < 2; k++) { const wnd = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.7, 0.55), winM); wnd.position.set(side * 2.5, h * 0.62, dz - 0.9 + k * 1.8); scene.add(wnd); lamps.push(winM); }
      z -= d + 0.15;
    }
  }
  // street lamps
  const lampMs = [];
  for (let k = 0; k < 6; k++) {
    const x = (k % 2 ? 1 : -1) * 2.0, z = 1 - k * 7;
    const post = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.07, 3.6, 10), phys(0x2a2420)); post.position.set(x, 1.8, z); post.castShadow = true; scene.add(post);
    const lm = new THREE.MeshStandardMaterial({ color: 0xffe0b0, emissive: 0xffc070, emissiveIntensity: 2 }); lampMs.push(lm);
    const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.18, 16, 12), lm); bulb.position.set(x, 3.65, z); scene.add(bulb);
    if (k < 3) { const pl = new THREE.PointLight(0xffb060, 3, 8, 2); pl.position.set(x, 3.4, z); scene.add(pl); lampMs.push(pl); }
  }
  // two clocks on the shopfront (right side, near camera)
  const cB = makeClock({ label: 'BEIJING', cjk: '北京时间', accent: 0xc41c1c, r: 0.62 });
  const cX = makeClock({ label: 'XINJIANG', cjk: '新疆时间', accent: 0x2a6ab0, r: 0.62 });
  cB.position.set(-0.75, 3.4, -1.2); cX.position.set(0.85, 3.4, -1.2); scene.add(cB); scene.add(cX);
  const board = new THREE.Mesh(new THREE.BoxGeometry(3.6, 2.6, 0.2), phys(0x6a4428, { roughness: 0.7 })); board.position.set(0.05, 3.15, -1.45); board.castShadow = board.receiveShadow = true; scene.add(board);
  // characters
  const student = makeChar({ skin: 0xb07a58, shirt: 0xc41c1c, pants: 0x2c3040, hair: 0x2a1c16, painter: false });
  const friend = makeChar({ skin: 0xe0b48c, shirt: 0x3a6a5a, pants: 0x3c3836, hair: 0x1a1612, painter: false, apron: 0xd8c49e });
  scene.add(student); scene.add(friend);
  // phone in student's hand
  const phone = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.16, 0.012), phys(0x111114)); student.userData.armL.hand.add(phone); phone.position.set(0, -0.06, 0.06);
  const scr = canvasTex(128, 256, (c) => { c.fillStyle = '#0d1a3a'; c.fillRect(0, 0, 128, 256); c.fillStyle = '#fff'; c.font = '800 44px Display'; c.textAlign = 'center'; c.fillText('9:00', 64, 110); c.font = '600 18px UI'; c.fillText('AM', 64, 140); });
  const screen = new THREE.Mesh(new THREE.PlaneGeometry(0.07, 0.14), new THREE.MeshBasicMaterial({ map: scr })); screen.position.z = 0.007; phone.add(screen);
  const skyN = { top: new THREE.Color(0x060a1c), bot: new THREE.Color(0x14204a) }, skyD = { top: new THREE.Color(0x2a5aa8), bot: new THREE.Color(0xffb878) };

  return { scene, camera: cam, bloom: 0.4, bloomThreshold: 0.88, bloomRadius: 0.6, cB, cX, student, friend,
    update(t, u, o = {}) {
      const dawn = o.dawn ?? 0;   // 0 night -> 1 morning
      skyU.top.value.copy(skyN.top).lerp(skyD.top, dawn); skyU.bot.value.copy(skyN.bot).lerp(skyD.bot, dawn);
      scene.fog.color.copy(skyU.bot.value).multiplyScalar(0.6);
      starsM.opacity = clamp(1 - dawn * 1.6);
      const sy = lerp(-6, 14, dawn); sunDisc.position.set(-6, sy, -70); sunDisc.visible = dawn > 0.05;
      sun.position.set(-8, Math.max(1, sy * 0.6), -30); sun.intensity = 2.8 * clamp(dawn * 1.3 - 0.1); sun.color.setHSL(0.07, 0.9, lerp(0.55, 0.75, dawn));
      hemi.intensity = lerp(0.35, 1.0, dawn); hemi.color.setHSL(lerp(0.63, 0.08, dawn), 0.6, 0.65);
      lamps.forEach((m) => { m.emissiveIntensity = 1.4 * (1 - dawn); });
      lampMs.forEach((m) => { if (m.isMaterial) m.emissiveIntensity = 2.2 * (1 - dawn); else m.intensity = 3 * (1 - dawn); });
      cB.userData.setTime(o.bH ?? 9, o.bM ?? 0); cX.userData.setTime((o.bH ?? 9) - 2, o.bM ?? 0);
      cB.visible = cX.visible = board.visible = o.clocks ?? false;
      student.position.set(...(o.sPos ?? [0, 0, 2])); friend.position.set(...(o.fPos ?? [99, 0, 0]));
      pose(student, o.sPose ?? {}); pose(friend, o.fPose ?? {});
      G.lookFrom(cam, o.cam ?? [0, 1.8, 7], o.tgt ?? [0, 1.6, 0]); cam.fov = o.fov ?? 36; cam.updateProjectionMatrix();
    } };
}

// ---------------------------------------------------------------- globe set (no borders: grid, terminator, pins, time-zone bands)
function globeSet() {
  const scene = new THREE.Scene(), cam = G.camera(32, 0.05, 200);
  scene.background = new THREE.Color(0x05070f);
  const R = 3;
  const gridT = canvasTex(2048, 1024, (c, w, h) => {
    const g = c.createLinearGradient(0, 0, 0, h); g.addColorStop(0, '#16306a'); g.addColorStop(0.5, '#1e4a8a'); g.addColorStop(1, '#16306a'); c.fillStyle = g; c.fillRect(0, 0, w, h);
    c.strokeStyle = 'rgba(160,200,255,0.25)'; c.lineWidth = 2;
    for (let lon = 0; lon < 360; lon += 15) { const x = (lon / 360) * w; c.beginPath(); c.moveTo(x, 0); c.lineTo(x, h); c.stroke(); }
    for (let lat = -75; lat <= 75; lat += 15) { const y = ((90 - lat) / 180) * h; c.beginPath(); c.moveTo(0, y); c.lineTo(w, y); c.stroke(); }
    const r = M.mulberry32(5); c.fillStyle = 'rgba(200,225,255,0.35)';
    for (let i = 0; i < 2500; i++) c.fillRect(r() * w, r() * h, 2, 2);
  });
  const globe = new THREE.Mesh(new THREE.SphereGeometry(R, 96, 64), new THREE.MeshStandardMaterial({ map: gridT, roughness: 0.6, emissive: 0x0a1630, emissiveIntensity: 0.6 }));
  scene.add(globe);
  const atmo = new THREE.Mesh(new THREE.SphereGeometry(R * 1.04, 64, 32), new THREE.ShaderMaterial({ transparent: true, side: THREE.BackSide, blending: THREE.AdditiveBlending, depthWrite: false,
    vertexShader: 'varying vec3 n; void main(){ n = normalize(normalMatrix*normal); gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.0);}',
    fragmentShader: 'varying vec3 n; void main(){ float i = pow(0.75 - dot(n, vec3(0,0,1.0)), 3.0); gl_FragColor = vec4(0.4,0.65,1.0,1.0)*i; }' }));
  scene.add(atmo);
  const sun = new THREE.DirectionalLight(0xfff0e0, 2.6); scene.add(sun);
  scene.add(new THREE.AmbientLight(0x304070, 0.35));
  // geographic helpers: lon/lat -> point on sphere (texture u=0 at lon=-180)
  const ll = (lat, lon, rad = R) => { const phi = (90 - lat) * Math.PI / 180, th = (lon + 180) * Math.PI / 180; return new THREE.Vector3(-rad * Math.sin(phi) * Math.cos(th), rad * Math.cos(phi), rad * Math.sin(phi) * Math.sin(th)); };
  const pin = (color) => { const g = new THREE.Group(); const s = new THREE.Mesh(new THREE.SphereGeometry(0.07, 16, 12), new THREE.MeshStandardMaterial({ color, emissive: color, emissiveIntensity: 1.5 })); g.add(s); const ring = new THREE.Mesh(new THREE.RingGeometry(0.1, 0.13, 32), new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.8, side: THREE.DoubleSide })); g.add(ring); g.userData.ring = ring; return g; };
  const pK = pin(0xffc040), pB = pin(0xff3a2a);
  const pk = ll(39.47, 75.99, R * 1.01), pb = ll(39.9, 116.4, R * 1.01);
  pK.position.copy(pk); pB.position.copy(pb); pK.lookAt(0, 0, 0); pB.lookAt(0, 0, 0); globe.add(pK); globe.add(pB);
  // five longitude bands 67.5E..142.5E (UTC+5..+9), drawn as sphere slices
  const bands = [];
  for (let k = 0; k < 5; k++) {
    const lon0 = 67.5 + k * 15;
    const geo = new THREE.SphereGeometry(R * 1.012, 24, 24, (lon0 + 180) * Math.PI / 180, (15 * Math.PI) / 180, (38 * Math.PI) / 180, (40 * Math.PI) / 180);
    const m = new THREE.MeshBasicMaterial({ color: [0x4aa0ff, 0x44d0b0, 0xf2c040, 0xff8a40, 0xff4a6a][k], transparent: true, opacity: 0, side: THREE.DoubleSide, depthWrite: false });
    const b = new THREE.Mesh(geo, m); globe.add(b); bands.push(m);
  }
  const one = new THREE.Mesh(new THREE.SphereGeometry(R * 1.016, 48, 24, (67.5 + 180) * Math.PI / 180, (75 * Math.PI) / 180, (38 * Math.PI) / 180, (40 * Math.PI) / 180), new THREE.MeshBasicMaterial({ color: 0xc41c1c, transparent: true, opacity: 0, side: THREE.DoubleSide, depthWrite: false }));
  globe.add(one);
  const v = new THREE.Vector3();
  return { scene, camera: cam, bloom: 0.5, bloomThreshold: 0.8, bloomRadius: 0.5,
    focus(lon) { const p = ll(30, lon); return Math.atan2(-p.x, p.z); },
    project(name) { (name === 'k' ? pK : pB).getWorldPosition(v); v.project(cam); return [(v.x + 1) / 2 * W, (1 - v.y) / 2 * H, v.z]; },
    update(t, u, o = {}) {
      globe.rotation.y = o.rot ?? 0; globe.rotation.x = 0.35;
      sun.position.set(o.sunX ?? 6, 2, 4);
      const pulse = 1 + 0.25 * Math.sin(t * 6);
      pK.userData.ring.scale.setScalar(pulse); pB.userData.ring.scale.setScalar(pulse);
      pB.visible = (o.showB ?? 0) > 0;
      bands.forEach((m, k) => { m.opacity = 0.55 * clamp((o.bands ?? 0) * 5 - k) * (1 - (o.merge ?? 0)); });
      one.material.opacity = 0.6 * (o.merge ?? 0);
      G.lookFrom(cam, o.cam ?? [0, 0, 11], [0, 0, 0]); cam.fov = o.fov ?? 32; cam.updateProjectionMatrix();
    } };
}

// ---------------------------------------------------------------- final set: clocks merge -> job cards orbit -> laowai card
function finaleSet() {
  const scene = new THREE.Scene(), cam = G.camera(34, 0.05, 100);
  scene.environment = G.ENV; scene.environmentIntensity = 0.15;
  const bgU = { a: { value: new THREE.Color(0x3a1418) }, b: { value: new THREE.Color(0xd8783c) } };
  const bg = new THREE.Mesh(new THREE.SphereGeometry(60, 32, 16), new THREE.ShaderMaterial({ side: THREE.BackSide, fog: false, uniforms: bgU,
    vertexShader: 'varying vec3 vp; void main(){ vp = normalize(position); gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.0); }',
    fragmentShader: 'uniform vec3 a; uniform vec3 b; varying vec3 vp; void main(){ float h = clamp(vp.y*1.4+0.45,0.0,1.0); gl_FragColor = vec4(mix(b, a, h),1.0); }' }));
  scene.add(bg);
  const key = new THREE.DirectionalLight(0xfff0e0, 2.0); key.position.set(-3, 6, 6); key.castShadow = true; key.shadow.mapSize.set(2048, 2048);
  Object.assign(key.shadow.camera, { left: -5, right: 5, top: 6, bottom: -3, near: 1, far: 30 }); key.shadow.normalBias = 0.03; scene.add(key);
  const rim = new THREE.DirectionalLight(0xff8a5a, 2.2); rim.position.set(3, 3, -5); scene.add(rim);
  scene.add(new THREE.HemisphereLight(0xffd8c0, 0x401818, 0.6));
  const floor = new THREE.Mesh(new THREE.CircleGeometry(30, 64), phys(0x5a2a22, { roughness: 0.3, clearcoat: 0.7 })); floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; scene.add(floor);
  // sun for the callback (rises behind at the end)
  const sunM = new THREE.MeshBasicMaterial({ color: 0xffd28a, fog: false }); const sun = new THREE.Mesh(new THREE.SphereGeometry(2.2, 48, 24), sunM); scene.add(sun);
  // clocks
  const cB = makeClock({ label: 'BEIJING', cjk: '北京时间', accent: 0xc41c1c, r: 1.25 }), cX = makeClock({ label: 'XINJIANG', cjk: '新疆时间', accent: 0x2a6ab0, r: 1.25 });
  scene.add(cB); scene.add(cX); cB.traverse((o) => { if (o.isMesh) o.castShadow = true; }); cX.traverse((o) => { if (o.isMesh) o.castShadow = true; });
  // job dial overlay that replaces the numbers
  const JOBS = ['CASTING', 'TV HOST', 'MODEL', 'VOICE-OVER', 'AGENT', 'LIVESTREAM', 'SHOOT', 'AGENT'];
  const dialT = canvasTex(1024, 1024, (c) => {
    c.fillStyle = '#fbf6ec'; c.beginPath(); c.arc(512, 512, 505, 0, Math.PI * 2); c.fill();
    JOBS.forEach((j, i) => {
      const a = (i / JOBS.length) * Math.PI * 2, x = 512 + Math.sin(a) * 330, y = 512 - Math.cos(a) * 330;
      c.font = '800 54px Display'; const w = c.measureText(j).width + 64;
      c.fillStyle = j === 'AGENT' ? '#1f1b16' : '#c41c1c'; c.beginPath(); c.roundRect(x - w / 2, y - 40, w, 80, 40); c.fill();
      c.fillStyle = '#fff'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(j, x, y + 3);
    });
  });
  const dialM = new THREE.MeshStandardMaterial({ map: dialT, transparent: true, opacity: 0, roughness: 0.5 });
  const dial = new THREE.Mesh(new THREE.CircleGeometry(1.24, 64), dialM); dial.position.z = 0.045; cB.add(dial);
  // centre cap that becomes the iris
  const coreM = new THREE.MeshStandardMaterial({ color: 0xc41c1c, emissive: 0xc41c1c, emissiveIntensity: 0.4 });
  const core = new THREE.Mesh(new THREE.CircleGeometry(0.12, 48), coreM); core.position.z = 0.135; cB.add(core);
  // characters
  const student = makeChar({ skin: 0xb07a58, shirt: 0xc41c1c, pants: 0x2c3040, hair: 0x2a1c16, painter: false });
  const friend = makeChar({ skin: 0xe0b48c, shirt: 0x3a6a5a, pants: 0x3c3836, hair: 0x1a1612, painter: false });
  scene.add(student); scene.add(friend);
  const v = new THREE.Vector3();
  return { scene, camera: cam, bloom: 0.15, bloomThreshold: 0.95, bloomRadius: 0.5,
    coreScreen() { core.getWorldPosition(v); v.project(cam); return [(v.x + 1) / 2 * W, (1 - v.y) / 2 * H]; },
    update(t, u, o = {}) {
      const m = o.merge ?? 0, dialK = o.dial ?? 0, spin = o.spin ?? 0, endK = o.end ?? 0;
      const endMode = endK > 0;
      // backdrop warms to brand red on the end card
      bgU.a.value.set(endMode ? 0x8a0e12 : 0x3a1418); bgU.b.value.set(endMode ? 0xe0402c : 0xd8783c);
      cB.visible = cX.visible = !endMode;
      cB.position.set(lerp(-1.45, 0, m), 2.25, 0); cX.position.set(lerp(1.45, 0, m), 2.25, -0.02);
      cB.rotation.y = lerp(0.3, 0, m); cX.rotation.y = lerp(-0.3, 0, m); cX.visible = !endMode && m < 0.97;
      cB.userData.setTime(12, 0); cX.userData.setTime(lerp(10, 12, E.inOutCubic(m)), 0);
      dialM.opacity = dialK;
      // hand: spins through the jobs, lands on AGENT
      cB.userData.mh.rotation.z = -spin * Math.PI * 2; cB.userData.hh.visible = dialK < 0.5;
      cB.scale.setScalar(1 + 0.06 * wobble(t - (o.mergeT ?? 0), 2.5, 5));
      // sun callback
      sun.visible = endMode; sun.position.set(0, lerp(-2.5, 1.2, E.outCubic(endK)), -20); sunM.color.setHSL(0.08, 1, 0.62);
      // characters
      const cheer = endMode ? 1 : 0, hop = endMode ? Math.abs(Math.sin(t * 7)) * 0.12 : 0;
      student.position.set(endMode ? 0.75 : 1.55, hop, endMode ? 0.4 : 1.1); friend.position.set(endMode ? -0.75 : -1.55, endMode ? Math.abs(Math.sin(t * 7 + 1.4)) * 0.12 : 0, endMode ? 0.4 : 1.1);
      const lookUp = !endMode;
      pose(student, { yaw: endMode ? -0.15 : -0.5, headPitch: lookUp ? -0.45 : 0, headYaw: lookUp ? -0.5 : 0, brow: (o.wow ?? 0) * 0.9 + 0.5 * cheer, mouthOpen: !endMode && (o.wow ?? 0) > 0.5 ? 0.7 : 0, blink: 1,
        armR: cheer ? [-2.7 + 0.25 * Math.sin(t * 9), 0.35] : [0.1, -0.3], armL: [0.1, -0.3], look: [lookUp ? -0.6 : 0, lookUp ? 0.8 : 0] });
      pose(friend, { yaw: endMode ? 0.15 : 0.5, headPitch: lookUp ? -0.45 : 0, headYaw: lookUp ? 0.5 : 0, brow: (o.wow ?? 0) * 0.9 + 0.2 * cheer, mouthOpen: 0, blink: (t > 30.2 && t < 30.32) ? 0 : 1,
        armR: cheer ? [-2.7 + 0.25 * Math.sin(t * 9 + 1), 0.35] : [-0.2 - 0.4 * (o.wow ?? 0), -0.9 * (o.wow ?? 0)], armL: [0.1, -0.3], look: [lookUp ? 0.6 : 0, lookUp ? 0.8 : 0] });
      G.lookFrom(cam, o.cam ?? [0, 2.2, 8.5], o.tgt ?? [0, 2.0, 0]); cam.fov = o.fov ?? 36; cam.updateProjectionMatrix();
    } };
}

// ---------------------------------------------------------------- typography system
function subtitle(ctx, parts, t, t0, t1, y = H * 0.83) {
  const a = Math.min(E.outCubic(prog(t, t0 - 0.05, t0 + 0.2)), 1 - prog(t, t1 - 0.05, t1 + 0.15));
  if (a <= 0) return;
  const segs = parts.map(([s, em]) => ({ s, f: em ? font(64, 400, 'Serif') : font(52, 700, 'UI'), em }));
  let wsum = 0; segs.forEach((g) => { ctx.font = g.f; g.w = ctx.measureText(g.s).width; wsum += g.w; });
  const sc = Math.min(1, (W - 120) / wsum);
  let x = (W - wsum * sc) / 2;
  ctx.save(); ctx.globalAlpha = a; ctx.shadowColor = 'rgba(0,0,0,0.6)'; ctx.shadowBlur = 18; ctx.shadowOffsetY = 4;
  segs.forEach((g) => { ctx.save(); ctx.translate(x, y + (1 - a) * 14); ctx.scale(sc, sc); ctx.font = g.f; ctx.fillStyle = g.em ? GOLD : '#FFFFFF'; ctx.fillText(g.s, 0, 0); ctx.restore(); x += g.w * sc; });
  ctx.restore();
}
function dimType(ctx, str, t, t0, cx, cy, size, { top = '#FFF3C8', bot = '#F0A040', side = [120, 40, 10], out = 99, rot = 0 } = {}) {
  const p = prog(t, t0, t0 + 0.5); if (p <= 0) return;
  const fade = 1 - prog(t, out, out + 0.25); if (fade <= 0) return;
  const f = font(size, 800, 'Display'); const L = layout(ctx, str, f, -0.03 * size); const x0 = cx - L.width / 2;
  ctx.save(); ctx.globalAlpha = fade;
  L.glyphs.forEach((g, j) => {
    const k = M.spring(Math.max(0, t - t0 - j * 0.035), M.SPRING.bouncy); if (t - t0 - j * 0.035 <= 0) return;
    const sc = lerp(1.9, 1, Math.min(1.2, k)); const y = cy - (1 - Math.min(1, k)) * 50;
    ctx.save(); ctx.translate(x0 + g.cx, y); ctx.rotate(rot * (1 - Math.min(1, k))); ctx.scale(sc, sc); ctx.textAlign = 'center'; ctx.font = f;
    const dpt = Math.max(6, size * 0.06);
    for (let d = dpt; d > 0; d--) { ctx.fillStyle = `rgb(${side[0] - d * 2},${side[1] - d},${side[2]})`; ctx.fillText(g.ch, d * 0.5, d); }
    const gr = ctx.createLinearGradient(0, -size * 0.8, 0, 0); gr.addColorStop(0, top); gr.addColorStop(1, bot); ctx.fillStyle = gr; ctx.fillText(g.ch, 0, 0);
    ctx.restore();
  });
  const s = prog(t, t0 + 0.45, t0 + 1.1);
  if (s > 0 && s < 1) { ctx.globalCompositeOperation = 'source-atop'; }
  ctx.restore();
}
function mapLabel(ctx, x, y, t, t0, title, sub, t1 = 99, dir = 1) {
  const p = E.outCubic(prog(t, t0, t0 + 0.45)); if (p <= 0) return; const o = 1 - prog(t, t1, t1 + 0.25); if (o <= 0) return;
  ctx.save(); ctx.globalAlpha = o; ctx.strokeStyle = 'rgba(255,255,255,0.9)'; ctx.lineWidth = 3;
  ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + dir * 60 * p, y - 120 * p); ctx.lineTo(x + dir * 140 * p, y - 120 * p); ctx.stroke();
  const q = E.outCubic(prog(t, t0 + 0.2, t0 + 0.6)); ctx.globalAlpha = q * o; ctx.textAlign = dir > 0 ? 'left' : 'right';
  ctx.shadowColor = 'rgba(0,0,0,0.6)'; ctx.shadowBlur = 12;
  ctx.font = font(60, 800, 'Display'); ctx.fillStyle = '#fff'; ctx.fillText(title, x + dir * 156, y - 108 + (1 - q) * 16);
  ctx.font = '700 32px "Noto Sans CJK SC"'; ctx.fillStyle = GOLD; ctx.fillText(sub, x + dir * 158, y - 64 + (1 - q) * 16);
  ctx.restore();
}
function bubble(ctx, x, y, str, t, t0, t1, tail = 1) {
  const p = E.outBack(prog(t, t0, t0 + 0.3), 2.0); if (p <= 0) return; const o = 1 - prog(t, t1, t1 + 0.2); if (o <= 0) return;
  ctx.save(); ctx.globalAlpha = o; ctx.translate(x, y); ctx.scale(p, p);
  ctx.font = font(50, 800, 'Display'); const w = ctx.measureText(str).width + 70, h = 96;
  ctx.shadowColor = 'rgba(0,0,0,0.35)'; ctx.shadowBlur = 20; ctx.shadowOffsetY = 8;
  ctx.fillStyle = '#fffaf2'; M.rrect(ctx, -w / 2, -h, w, h, 48); ctx.fill();
  ctx.beginPath(); ctx.moveTo(-14 * tail, -4); ctx.lineTo(10 * tail, 30); ctx.lineTo(24 * tail, -4); ctx.fill();
  ctx.shadowColor = 'transparent'; ctx.fillStyle = '#1f1b16'; ctx.textAlign = 'center'; ctx.fillText(str, 0, -30);
  ctx.restore();
}

// ---------------------------------------------------------------- timeline
let SC = [];
function scene(t) { for (let k = SC.length - 2; k >= 0; k--) if (t >= SC[k]) return k; return 0; }

M.film({
  fonts: [font(100, 800, 'Display'), font(40, 700, 'UI'), font(60, 400, 'Serif'), '700 40px "Noto Sans CJK SC"', '900 40px "Noto Sans CJK SC"'],
  samples: 1,
  async init() {
    WN = await fetch('assets/words.json').then((r) => r.json());
    SC = [0, LS(1), LS(2), LS(3), LS(4), LS(5), LS(6), LS(7), LS(8), LS(9) - 0.1, 99];
    await G.initGL({ exposure: 1.0 }); S.street = streetSet(); S.globe = globeSet(); S.fin = finaleSet();
  },
  draw(ctx, u, t) {
    const s = scene(t), rt = t - SC[s];
    if (s <= 1) {
      // night street at 9am -> sunrise after ten
      const dawn = s === 0 ? 0 : E.inOutCubic(prog(t, SC[1], SC[2] - 0.2));
      const look = s === 0 ? E.outBack(prog(t, 0.9, 1.4), 1.8) : 1;
      const bH = s === 0 ? 9 : lerp(9, 10.25, E.inOutCubic(prog(t, SC[1], SC[2] - 0.3)));
      G.renderSet(ctx, S.street, t, u, {
        dawn, clocks: false, bH,
        sPos: [0.1, 0, 1.6],
        sPose: { yaw: lerp(0.2, -0.1, look), headPitch: lerp(0.35, -0.35, look) - (s === 1 ? 0.15 : 0), headYaw: lerp(0.1, -0.2, look), brow: look * 0.8, blink: (t > 2.6 && t < 2.72) ? 0 : 1,
          mouthOpen: s === 0 && t > 1.4 && t < 2.0 ? 0.8 : 0, armL: [lerp(-1.1, -0.3, look), lerp(-1.3, -0.4, look)], armR: s === 1 ? [-2.6 * E.outBack(prog(t, SC[1] + 1.0, SC[1] + 1.5)), -0.3] : [0.1, -0.2], look: [0, lerp(0.8, -0.8, look)] },
        cam: s === 0 ? [lerp(1.2, 0.9, rt / 4), lerp(2.0, 1.9, rt / 4), lerp(6.4, 5.4, rt / 4)] : [lerp(0.9, 0.2, E.inOutCubic(rt / 3.2)), lerp(1.9, 2.6, E.inOutCubic(rt / 3.2)), lerp(5.4, 9.5, E.inOutCubic(rt / 3.2))],
        tgt: s === 0 ? [0.0, 2.0, 1.2] : [0, lerp(1.85, 3.6, E.inOutCubic(rt / 3.2)), lerp(1.6, -6, E.inOutCubic(rt / 3.2))], fov: s === 0 ? 34 : 40,
      });
      if (s === 0) {
        dimType(ctx, '9:00 AM', t, tw('nine', 0) - 0.15, W / 2, H * 0.2, 190);
        subtitle(ctx, [['Nine a.m. Still ', 0], ['dark.', 1]], t, tw('nine', 0), LE(0) + 0.3);
      } else {
        dimType(ctx, 'SUNRISE', t, tw('sun', 1) - 0.1, W / 2, H * 0.17, 120, { top: '#FFFFFF', bot: '#FFC890', side: [130, 60, 20] });
        dimType(ctx, 'AFTER 10:00', t, tw('ten', 1) - 0.2, W / 2, H * 0.27, 130);
        subtitle(ctx, [['In winter, the sun comes up ', 0], ['after ten.', 1]], t, LS(1), LE(1) + 0.3);
      }
    } else if (s === 2) {
      // globe: Kashgar pin, far west
      const k = E.inOutCubic(prog(t, SC[2], SC[2] + 1.6));
      G.renderSet(ctx, S.globe, t, u, { rot: S.globe.focus(lerp(20, 82, k)), cam: [0, lerp(4, 3, k), lerp(34, 18, k)], sunX: 5 });
      const [x, y] = S.globe.project('k');
      mapLabel(ctx, x, y, t, tw('kashgar', 2) - 0.1, 'KASHGAR', '喀什 · FAR WEST', 99, -1);
      subtitle(ctx, [['This is ', 0], ['Kashgar,', 1], [' in China\'s far west.', 0]], t, LS(2), LE(2) + 0.2);
    } else if (s === 3) {
      // five zones -> one clock
      const bands = prog(t, tw('five', 3) - 0.3, tw('five', 3) + 0.7), merge = E.inOutCubic(prog(t, tw('one', 3) - 0.1, tw('one', 3) + 0.6));
      G.renderSet(ctx, S.globe, t, u, { rot: S.globe.focus(lerp(82, 100, E.inOutCubic(prog(t, SC[3], SC[3] + 1.5)))), cam: [0, 3, lerp(18, 16, prog(t, SC[3], SC[4]))], bands, merge, showB: 1 });
      const [bx, by] = S.globe.project('b'), [kx, ky] = S.globe.project('k');
      mapLabel(ctx, bx, by, t, tw('beijing', 3) - 0.1, 'BEIJING', '北京', 99, 1);
      mapLabel(ctx, kx, ky, t, SC[3], 'KASHGAR', '喀什', tw('wide', 3), -1);
      if (merge < 0.5) dimType(ctx, '5 ZONES', t, tw('five', 3) - 0.1, W / 2, H * 0.16, 150, { top: '#E0F0FF', bot: '#6AB0FF', side: [20, 50, 110], out: tw('one', 3) - 0.1 });
      else dimType(ctx, '1 CLOCK', t, tw('one', 3) - 0.05, W / 2, H * 0.16, 150, { top: '#FFE0D8', bot: '#E8402C', side: [110, 10, 10] });
      subtitle(ctx, [['About five time zones. ', 0], ['One clock.', 1]], t, LS(3), tw('clock', 3) + 0.2);
      subtitle(ctx, [['Beijing ', 1], ['time.', 0]], t, tw('beijing', 3) - 0.05, LE(3) + 0.3);
    } else if (s <= 6) {
      // street morning: two clocks; "see you at noon" -> "which noon?"
      const k = E.inOutCubic(prog(t, SC[4], SC[4] + 1.2));
      const noon = s === 6;
      const bH = s === 4 ? lerp(11, 12, prog(t, SC[4], SC[5])) : 12;
      const confused = noon ? E.outBack(prog(t, tw('which', 6) - 0.2, tw('which', 6) + 0.2), 2) : 0;
      G.renderSet(ctx, S.street, t, u, {
        dawn: 1, clocks: true, bH, bM: 0,
        sPos: [0.9, 0, 1.0], fPos: [-0.9, 0, 1.0],
        sPose: { yaw: -0.5 + confused * 0.3, headYaw: noon ? -0.4 + 0.2 * Math.sin(t * 4) * (confused > 0) : 0.3, headPitch: noon ? 0 : -0.35, brow: noon ? confused : 0.4, blink: 1, mouthOpen: confused > 0.3 ? 0.6 : 0,
          armR: [-0.4 * confused, -1.6 * confused], armL: [0.1, -0.3], lean: 0.05 * confused, look: [-0.5, noon ? 0 : -0.8] },
        fPose: { yaw: 0.5, headYaw: 0.2, brow: 0.3, blink: (t > 22.3 && t < 22.42) ? 0 : 1, mouthOpen: noon && t < tw('which', 6) - 0.3 && t > LS(6) ? 0.5 + 0.3 * Math.sin(t * 20) : 0,
          armR: noon ? [-2.8 + 0.25 * Math.sin(t * 9), -0.2] : [0.1, -0.2], armL: [0.1, -0.2], look: [0.6, 0] },
        cam: s === 4 ? [lerp(0, 0.1, k), lerp(3.6, 2.7, k), lerp(5.0, 7.6, k)] : s === 5 ? [0.0, 3.3, lerp(6.4, 5.4, E.inOutCubic(rt / 1.6))] : [0.2, 2.3, 7.4],
        tgt: s === 4 ? [0, lerp(3.3, 2.3, k), -1.0] : s === 5 ? [0, 3.35, -1.2] : [0, 2.1, 0.0], fov: s === 5 ? 34 : 40,
      });
      if (s === 4) subtitle(ctx, [['So many keep a second clock: ', 0], ['Xinjiang time.', 1]], t, LS(4), LE(4) + 0.2);
      if (s === 5) { dimType(ctx, 'SAME CITY.', t, LS(5) - 0.05, W / 2, H * 0.16, 130, { top: '#FFFFFF', bot: '#D8E4FF', side: [40, 50, 90] }); dimType(ctx, 'TWO CLOCKS.', t, tw('two', 5) - 0.1, W / 2, H * 0.26, 130, { top: '#FFE0D8', bot: '#E8402C', side: [110, 10, 10] }); }
      if (noon) {
        bubble(ctx, W * 0.30, H * 0.30, 'See you at noon!', t, LS(6) - 0.05, LE(6) + 0.3, 1);
        bubble(ctx, W * 0.72, H * 0.36, 'Which noon? 🤔'.replace(' 🤔', '?'), t, tw('which', 6) - 0.15, LE(6) + 0.4, -1);
        subtitle(ctx, [['Say "see you at noon"… ', 0], ['which noon?', 1]], t, LS(6), LE(6) + 0.3);
      }
    } else {
      // finale: two clocks merge into one -> the numbers become jobs -> push into the centre -> red iris -> end card
      const merge = E.inOutCubic(prog(t, SC[7] + 0.1, SC[7] + 1.0));
      const dial = E.outCubic(prog(t, LS(8) + 0.1, LS(8) + 0.5));
      const tA = tw('agent', 8);
      const spin = dial > 0 ? (t < tA ? 1.6 * E.inCubic(prog(t, LS(8) + 0.3, tA)) : 1.6 + (4 / 8 - 0.6 + 1.0) * E.outBack(prog(t, tA, tA + 0.45), 2.2)) : 0;
      const push = E.inCubic(prog(t, tA + 0.5, LS(9) + 0.05));
      const endT = LS(9) + 0.05, endK = prog(t, endT, endT + 0.9);
      const camEnd = [0, 2.3, 12.5];
      const cam = endK > 0 ? camEnd : [lerp(0.3, 0, push), lerp(2.0, 2.25, push), lerp(8.2, 1.05, push) - 0.3 * prog(t, SC[7], tA)];
      const tgt = endK > 0 ? [0, 3.6, 0] : [0, lerp(1.9, 2.25, push), 0];
      G.renderSet(ctx, S.fin, t, u, { merge, mergeT: SC[7] + 1.0, dial, spin, end: endK, wow: prog(t, LS(8), LS(8) + 0.4), cam, tgt, fov: endK > 0 ? 34 : 36 });
      // iris: the red centre swells to fill the frame, then opens on the end card
      if (push > 0 && endK <= 0) {
        const [cx, cy] = S.fin.coreScreen(); const r = 30 + 2400 * E.inExpo(prog(t, tA + 0.9, endT));
        ctx.save(); ctx.fillStyle = BRAND; ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.fill(); ctx.restore();
      }
      if (endK > 0 && endK < 1) { const r = 2400 * (1 - E.outCubic(prog(t, endT, endT + 0.35))); if (r > 1) { ctx.save(); ctx.fillStyle = BRAND; ctx.globalAlpha = 1; ctx.beginPath(); ctx.arc(W / 2, H / 2, r, 0, Math.PI * 2); ctx.fill(); ctx.restore(); } }
      if (s === 7) { dimType(ctx, 'ONE COUNTRY.', t, LS(7) - 0.05, W / 2, H * 0.15, 120, { top: '#FFFFFF', bot: '#FFD0C8', side: [110, 20, 20] }); dimType(ctx, 'ONE CLOCK.', t, tw('one', 7, 1) - 0.1, W / 2, H * 0.25, 140, { top: '#FFE0D8', bot: '#E8402C', side: [110, 10, 10] }); }
      if (s === 8 && push < 0.4) {
        dimType(ctx, 'EVERY JOB.', t, tw('job', 8) - 0.15, W / 2, H * 0.13, 120, { top: '#FFFFFF', bot: '#FFE6C8', side: [110, 30, 20], out: tA + 0.6 });
        dimType(ctx, 'EVERY AGENT.', t, tA - 0.15, W / 2, H * 0.22, 120, { top: '#FFFFFF', bot: '#FFE6C8', side: [110, 30, 20], out: tA + 0.6 });
        subtitle(ctx, [['Now imagine ', 0], ['one place', 1], [' for every job and every agent.', 0]], t, LS(8), LE(8) + 0.2);
      }
      if (endK > 0) {
        // wordmark: per-glyph dimensional "laowai" + 吗 seal, URL pill, tagline
        dimType(ctx, 'laowai', t, endT + 0.15, W / 2 - 70, H * 0.24, 200, { top: '#FFFFFF', bot: '#FFE2DA', side: [120, 10, 14] });
        const q = E.outBack(prog(t, endT + 0.45, endT + 0.8), 2.2);
        if (q > 0) {
          ctx.save(); ctx.font = font(200, 800, 'Display'); const lw = ctx.measureText('laowai').width; ctx.translate(W / 2 - 70 + lw / 2 + 110, H * 0.24 - 70); ctx.rotate(-0.08 * (1 - q)); ctx.scale(q, q);
          ctx.fillStyle = '#FFFFFF'; M.rrect(ctx, -82, -88, 164, 164, 34); ctx.shadowColor = 'rgba(80,0,0,0.5)'; ctx.shadowBlur = 24; ctx.shadowOffsetY = 10; ctx.fill();
          ctx.shadowColor = 'transparent'; ctx.fillStyle = BRAND; ctx.font = '900 128px "Noto Sans CJK SC"'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('吗', 0, -2); ctx.restore();
        }
        const p2 = E.outCubic(prog(t, endT + 0.7, endT + 1.1));
        if (p2 > 0) {
          ctx.save(); ctx.globalAlpha = p2; ctx.font = font(58, 800, 'Display'); const w = ctx.measureText('laowai.ma').width + 90;
          ctx.fillStyle = '#FFFFFF'; M.rrect(ctx, W / 2 - w / 2, H * 0.31 + (1 - p2) * 30, w, 100, 50); ctx.fill();
          ctx.fillStyle = BRAND; ctx.textAlign = 'center'; ctx.fillText('laowai.ma', W / 2, H * 0.31 + 70 + (1 - p2) * 30);
          ctx.font = font(46, 700, 'UI'); ctx.fillStyle = '#FFF2EC'; ctx.shadowColor = 'rgba(60,0,0,0.5)'; ctx.shadowBlur = 12; ctx.fillText('Every job. Every agent. One place.', W / 2, H * 0.43);
          ctx.font = '700 38px "Noto Sans CJK SC"'; ctx.fillStyle = '#FFE0B0'; ctx.fillText('外国人才的工作与经纪人，一站汇集', W / 2, H * 0.475);
          ctx.restore();
        }
      }
    }
    // grade + vignette
    const v = ctx.createRadialGradient(W / 2, H * 0.45, H * 0.25, W / 2, H * 0.5, H * 0.8);
    v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(6,4,10,0.5)'); ctx.fillStyle = v; ctx.fillRect(0, 0, W, H);
    // whip between scenes: short directional smear using a translated copy
    const cut = SC.slice(0, 9).find((c) => c > 0 && Math.abs(t - c) < 0.08);
    if (cut !== undefined) { const k = 1 - Math.abs(t - cut) / 0.08; ctx.save(); ctx.globalAlpha = 0.35 * k; for (let i = 1; i <= 3; i++) ctx.drawImage(ctx.canvas, i * 26 * k, 0); ctx.restore(); }
  },
  post(ctx, u, t) {
    const r = M.mulberry32(Math.floor(t * 30) + 7);
    ctx.save(); ctx.globalAlpha = 0.05; for (let i = 0; i < 1400; i++) { ctx.fillStyle = r() > 0.5 ? '#fff' : '#000'; ctx.fillRect(r() * W, r() * H, 2, 2); } ctx.restore();
  },
});
function DUR() { return LE(9) + 2.4; }
