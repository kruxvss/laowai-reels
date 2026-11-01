// laowai 2.5D look test: Dafen alley at dusk, dimensional Zhao, pull-back reveal, new caption system.
import * as M from './lib/motion.js';
import * as G from './lib/gl.js';
const { THREE } = G;
const { W, H, E, prog, lerp, clamp, kf, font, text, layout, glyph, hash01, wobble } = M;

const BRAND = '#C41C1C', INK = '#1F1B16', GOLD = '#F5C76A';
const S = {};
const sec = (t) => t;   // timeline in seconds (beats.json period 0.5 -> u = 2t)

// ---------------------------------------------------------------- materials
const mat = (color, rough = 0.6, extra = {}) => new THREE.MeshStandardMaterial({ color, roughness: rough, ...extra });
const phys = (color, extra = {}) => new THREE.MeshPhysicalMaterial({ color, roughness: 0.45, clearcoat: 0.3, ...extra });

// ---------------------------------------------------------------- dimensional character
function makeChar({ skin = 0xe2b48a, shirt = 0x4a76b0, apron = 0xd8c49e, pants = 0x3c3836, hair = 0x18161a, scale = 1, painter = true } = {}) {
  const root = new THREE.Group(), r = {};
  const mSkin = phys(skin, { roughness: 0.55, clearcoat: 0.15, sheen: 0.4, sheenColor: new THREE.Color(0xffc6a8) });
  const mShirt = mat(shirt, 0.85), mApron = mat(apron, 0.9), mPants = mat(pants, 0.8), mHair = phys(hair, { roughness: 0.35, clearcoat: 0.6 });
  const mShoe = phys(0x222020, { roughness: 0.4 });
  // torso: lathe profile (hips -> waist -> chest -> shoulders)
  const prof = [[0, 0], [0.30, 0.02], [0.33, 0.18], [0.30, 0.42], [0.34, 0.66], [0.37, 0.80], [0.30, 0.90], [0.12, 0.96], [0, 0.97]].map(([x, y]) => new THREE.Vector2(x, y));
  const torso = new THREE.Mesh(new THREE.LatheGeometry(prof, 40), mShirt); torso.scale.set(1, 1, 0.72); torso.castShadow = true;
  const hips = new THREE.Group(); hips.position.y = 0.92; root.add(hips);
  const spine = new THREE.Group(); hips.add(spine); spine.add(torso);
  // apron: curved panel in front with folds (displaced cylinder segment)
  const ag = new THREE.CylinderGeometry(0.36, 0.42, 0.95, 32, 12, true, -0.85, 1.7);
  const pos = ag.attributes.position;
  for (let i = 0; i < pos.count; i++) { const x = pos.getX(i), y = pos.getY(i), z = pos.getZ(i); const a = Math.atan2(x, z); const f = 0.012 * Math.sin(a * 9) * (0.5 - y); pos.setXYZ(i, x * (1 + f), y, z * (1 + f)); }
  ag.computeVertexNormals();
  const ap = new THREE.Mesh(ag, new THREE.MeshStandardMaterial({ color: apron, roughness: 0.9, side: THREE.DoubleSide })); ap.position.set(0, 0.42, 0.0); ap.scale.set(1, 1, 0.78); ap.castShadow = true;
  if (painter) {
    spine.add(ap);
    // paint splotches on apron
    [[0.12, 0.6, 0x3060c0], [-0.1, 0.35, 0xf0b030], [0.05, 0.2, 0xc03828], [-0.16, 0.55, 0x3c9a5a]].forEach(([x, y, c]) => {
      const s = new THREE.Mesh(new THREE.SphereGeometry(0.035, 12, 8), mat(c, 0.3)); s.scale.set(1, 0.8, 0.25); s.position.set(x, y, 0.34); spine.add(s);
    });
  }
  // neck + head
  const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.1, 0.16, 16), mSkin); neck.position.y = 1.0; spine.add(neck);
  const head = new THREE.Group(); head.position.y = 1.3; spine.add(head); r.head = head;
  const skull = new THREE.Mesh(new THREE.SphereGeometry(0.36, 48, 36), mSkin); skull.scale.set(0.95, 1.0, 0.95); skull.castShadow = true; head.add(skull);
  const jaw = new THREE.Mesh(new THREE.SphereGeometry(0.29, 32, 24), mSkin); jaw.position.set(0, -0.11, 0.05); jaw.scale.set(1, 0.85, 0.95); head.add(jaw);
  const hairM = new THREE.Mesh(new THREE.SphereGeometry(0.37, 48, 24, 0, Math.PI * 2, 0, Math.PI * 0.42), mHair); hairM.scale.set(0.98, 1.0, 0.98); hairM.position.set(0, 0.06, -0.03); head.add(hairM);
  const trn = M.mulberry32(5);
  for (let i = 0; i < 14; i++) { const a = (i / 14) * Math.PI * 2, el = 0.55 + trn() * 0.3; const tuft = new THREE.Mesh(new THREE.SphereGeometry(0.1 + trn() * 0.04, 16, 12), mHair);
    tuft.position.set(Math.sin(a) * 0.3 * Math.cos(el - 0.5), 0.2 + trn() * 0.08, Math.cos(a) * 0.28 - 0.04); tuft.scale.set(1, 0.7, 1); if (Math.cos(a) > 0.6) tuft.position.y += 0.03; head.add(tuft); }
  for (const sx of [-1, 1]) {
    const ear = new THREE.Mesh(new THREE.SphereGeometry(0.075, 16, 12), mSkin); ear.scale.set(0.5, 1, 0.8); ear.position.set(sx * 0.34, -0.02, 0); head.add(ear);
  }
  const nose = new THREE.Mesh(new THREE.SphereGeometry(0.055, 20, 16), mSkin); nose.position.set(0, -0.04, 0.35); nose.scale.set(1, 0.9, 1.1); head.add(nose);
  // eyes: white sclera, dark iris, specular catchlight comes from clearcoat
  r.eyes = []; r.lids = []; r.brows = [];
  for (const sx of [-1, 1]) {
    const eg = new THREE.Group(); eg.position.set(sx * 0.135, 0.06, 0.29); head.add(eg);
    const scl = new THREE.Mesh(new THREE.SphereGeometry(0.085, 24, 16), phys(0xfbf8f2, { roughness: 0.1, clearcoat: 1 })); scl.scale.set(1, 1.2, 0.6); eg.add(scl);
    const iris = new THREE.Mesh(new THREE.SphereGeometry(0.05, 20, 16), phys(0x4a2a18, { roughness: 0.05, clearcoat: 1 })); iris.position.z = 0.04; iris.scale.set(1, 1.15, 0.45); const pup = new THREE.Mesh(new THREE.SphereGeometry(0.026, 16, 12), phys(0x080606, { roughness: 0.02, clearcoat: 1 })); pup.position.z = 0.02; iris.add(pup); const glint = new THREE.Mesh(new THREE.SphereGeometry(0.011, 8, 6), new THREE.MeshBasicMaterial({ color: 0xffffff })); glint.position.set(0.015, 0.02, 0.03); iris.add(glint); eg.add(iris);
    const lid = new THREE.Mesh(new THREE.SphereGeometry(0.09, 24, 12, 0, Math.PI * 2, 0, Math.PI * 0.5), mSkin); lid.scale.set(1, 1.2, 0.65); eg.add(lid);
    const brow = new THREE.Mesh(new THREE.CapsuleGeometry(0.02, 0.1, 4, 8), mHair); brow.rotation.z = Math.PI / 2; brow.position.set(sx * 0.135, 0.2, 0.32); head.add(brow);
    r.eyes.push(iris); r.lids.push(lid); r.brows.push(brow);
  }
  // mouth: a smile arc (torus segment) + an open-mouth ellipsoid
  const smile = new THREE.Mesh(new THREE.TorusGeometry(0.07, 0.012, 8, 24, Math.PI * 0.8), mat(0x6a2a22, 0.5)); smile.rotation.z = Math.PI * 1.1; smile.position.set(0, -0.15, 0.32); head.add(smile);
  const omouth = new THREE.Mesh(new THREE.SphereGeometry(0.04, 16, 12), mat(0x4a1a16, 0.6)); omouth.position.set(0, -0.17, 0.31); omouth.scale.set(1, 1.3, 0.4); head.add(omouth);
  r.smile = smile; r.omouth = omouth;
  // cheeks
  for (const sx of [-1, 1]) { const c = new THREE.Mesh(new THREE.SphereGeometry(0.05, 16, 12), mat(0xe89a84, 0.7, { transparent: true, opacity: 0.35 })); c.position.set(sx * 0.21, -0.07, 0.27); c.scale.set(1, 0.6, 0.3); head.add(c); }
  // arms: shoulder -> elbow groups, capsule sleeves, sphere hands
  const arm = (sx) => {
    const sh = new THREE.Group(); sh.position.set(sx * 0.38, 0.82, 0); spine.add(sh);
    const up = new THREE.Mesh(new THREE.CapsuleGeometry(0.085, 0.3, 6, 16), mShirt); up.position.y = -0.2; up.castShadow = true; sh.add(up);
    const el = new THREE.Group(); el.position.y = -0.4; sh.add(el);
    const fo = new THREE.Mesh(new THREE.CapsuleGeometry(0.075, 0.26, 6, 16), mShirt); fo.position.y = -0.17; fo.castShadow = true; el.add(fo);
    const hand = new THREE.Mesh(new THREE.SphereGeometry(0.075, 20, 16), mSkin); hand.position.y = -0.38; hand.scale.set(0.9, 1.1, 0.8); el.add(hand);
    return { sh, el, hand };
  };
  r.armL = arm(-1); r.armR = arm(1);
  // brush in right hand
  const brush = new THREE.Group(); brush.position.set(0, -0.4, 0.04); r.armR.el.add(brush);
  const handle = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.016, 0.42, 10), phys(0x8a5a2c)); handle.rotation.x = Math.PI / 2.4; handle.position.set(0, 0.04, 0.16); brush.add(handle);
  const tip = new THREE.Mesh(new THREE.ConeGeometry(0.025, 0.08, 12), mat(0xf2b33d, 0.4)); tip.rotation.x = Math.PI / 2.4 + Math.PI; tip.position.set(0, 0.12, 0.36); brush.add(tip);
  r.brush = brush;
  // legs
  const leg = (sx) => {
    const hp = new THREE.Group(); hp.position.set(sx * 0.15, 0, 0); hips.add(hp);
    const th = new THREE.Mesh(new THREE.CapsuleGeometry(0.11, 0.32, 6, 16), mPants); th.position.y = -0.22; th.castShadow = true; hp.add(th);
    const kn = new THREE.Group(); kn.position.y = -0.44; hp.add(kn);
    const sn = new THREE.Mesh(new THREE.CapsuleGeometry(0.095, 0.3, 6, 16), mPants); sn.position.y = -0.2; sn.castShadow = true; kn.add(sn);
    const shoe = new THREE.Mesh(new THREE.CapsuleGeometry(0.08, 0.14, 6, 12), mShoe); shoe.rotation.x = Math.PI / 2; shoe.position.set(0, -0.42, 0.06); shoe.castShadow = true; kn.add(shoe);
    return { hp, kn };
  };
  r.legL = leg(-1); r.legR = leg(1);
  root.scale.setScalar(scale);
  root.userData = r; r.hips = hips; r.spine = spine;
  return root;
}
// pose: every property set from scratch each call (pure)
function pose(ch, { walk = 0, amp = 0, yaw = 0, headYaw = 0, headPitch = 0, brow = 0, blink = 0, mouthOpen = 0, armR = [0.2, -0.3], armL = [0.1, -0.2], lean = 0, bob = 0, look = [0, 0] }) {
  const r = ch.userData;
  ch.rotation.y = yaw;
  const s = Math.sin(walk) * amp;
  r.hips.position.y = 0.92 + Math.abs(Math.cos(walk)) * 0.04 * amp + bob;
  r.spine.rotation.x = lean; r.spine.rotation.y = -s * 0.12;
  r.legL.hp.rotation.x = s * 0.55; r.legR.hp.rotation.x = -s * 0.55;
  r.legL.kn.rotation.x = Math.max(0, -Math.sin(walk + 0.8)) * 0.9 * amp; r.legR.kn.rotation.x = Math.max(0, Math.sin(walk + 0.8)) * 0.9 * amp;
  r.armL.sh.rotation.set(-s * 0.5 + armL[0], 0, 0.12 + armL[1] * 0.1); r.armL.el.rotation.x = -0.25 + armL[1];
  r.armR.sh.rotation.set(s * 0.5 + armR[0], 0, -0.12); r.armR.el.rotation.x = -0.25 + armR[1];
  r.head.rotation.set(headPitch, headYaw, 0);
  r.brows.forEach((b, i) => { b.position.y = 0.2 + brow * 0.04; b.rotation.y = 0; b.rotation.x = 0; b.rotation.set(0, 0, Math.PI / 2 + (i ? -1 : 1) * brow * 0.25); });
  r.lids.forEach((l) => { l.rotation.x = lerp(-1.25, 0.1, blink); });
  r.eyes.forEach((e) => { e.position.x = look[0] * 0.012; e.position.y = look[1] * 0.012; });
  r.smile.visible = mouthOpen < 0.3; r.omouth.visible = mouthOpen >= 0.3; r.omouth.scale.set(1, 0.8 + mouthOpen, 0.4);
}

// ---------------------------------------------------------------- painting textures (original swirl motifs)
function paintingCanvas(seed, w = 256, h = 200) {
  const c = document.createElement('canvas'); c.width = w; c.height = h; const g = c.getContext('2d');
  const pal = [['#13265a', '#2a52a8', '#9ec0f0', '#f2b33d'], ['#2c5a2a', '#e6b83a', '#f2d070', '#8a4a20'], ['#7a1e1e', '#e0603a', '#f2c060', '#2a2a40'], ['#203a5a', '#6aa0c0', '#f0e6c8', '#c03a2a']][seed % 4];
  g.fillStyle = pal[0]; g.fillRect(0, 0, w, h);
  const rnd = M.mulberry32(seed * 977 + 3);
  for (let i = 0; i < 420; i++) {
    let x = rnd() * w, y = rnd() * h; g.strokeStyle = pal[1 + Math.floor(rnd() * 3)]; g.lineWidth = 3 + rnd() * 3; g.beginPath(); g.moveTo(x, y);
    for (let k = 0; k < 4; k++) { const a = Math.atan2(y - h * 0.4, x - w * 0.5) + Math.PI / 2 + rnd() * 0.4; x += Math.cos(a) * 7; y += Math.sin(a) * 7; g.lineTo(x, y); }
    g.stroke();
  }
  return c;
}

// ---------------------------------------------------------------- the alley set
function alleySet() {
  const scene = new THREE.Scene(), cam = G.camera(38, 0.05, 200);
  scene.background = new THREE.Color(0x3a2238);
  scene.fog = new THREE.Fog(0x5a3040, 10, 48);
  scene.environment = G.ENV; scene.environmentIntensity = 0.25;
  const hemi = new THREE.HemisphereLight(0xffc89a, 0x2a2440, 0.9); scene.add(hemi);
  const sun = new THREE.DirectionalLight(0xffb070, 2.6); sun.position.set(-6, 9, -14); sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048); Object.assign(sun.shadow.camera, { left: -8, right: 8, top: 10, bottom: -10, near: 1, far: 60 }); sun.shadow.bias = -0.0005; sun.shadow.normalBias = 0.03; sun.shadow.radius = 4;
  scene.add(sun); scene.add(sun.target); sun.target.position.set(0, 0, -6);
  const keyF = new THREE.DirectionalLight(0xdfe8ff, 0.7); keyF.position.set(4, 3, 8); scene.add(keyF);   // cool front fill
  // sky plane (sunset gradient) at the end of the alley
  const skyC = document.createElement('canvas'); skyC.width = 4; skyC.height = 256; const sg = skyC.getContext('2d');
  const gr = sg.createLinearGradient(0, 0, 0, 256); gr.addColorStop(0, '#3a2a5e'); gr.addColorStop(0.55, '#e86a4a'); gr.addColorStop(1, '#ffd08a'); sg.fillStyle = gr; sg.fillRect(0, 0, 4, 256);
  const skyT = new THREE.CanvasTexture(skyC); skyT.colorSpace = THREE.SRGBColorSpace;
  const sky = new THREE.Mesh(new THREE.PlaneGeometry(80, 50), new THREE.MeshBasicMaterial({ map: skyT, fog: false })); sky.position.set(0, 14, -60); scene.add(sky);
  // ground: wet stone
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(14, 120), phys(0x4a3a3e, { roughness: 0.28, clearcoat: 0.6, clearcoatRoughness: 0.2 }));
  ground.rotation.x = -Math.PI / 2; ground.position.z = -40; ground.receiveShadow = true; scene.add(ground);
  // buildings both sides + canvases on walls
  const wallM = [mat(0xd8b898, 0.92), mat(0xc8a488, 0.92), mat(0xe2c8a6, 0.92)];
  const tex = [0, 1, 2, 3, 4, 5].map((s) => { const t = new THREE.CanvasTexture(paintingCanvas(s)); t.colorSpace = THREE.SRGBColorSpace; return t; });
  const frameM = phys(0x6a4426, { roughness: 0.5 });
  const pmats = tex.map((t) => new THREE.MeshStandardMaterial({ map: t, roughness: 0.55 }));
  const rnd = M.mulberry32(41);
  for (const side of [-1, 1]) {
    let z = 4;
    while (z > -50) {
      const d = 4 + rnd() * 3, h = 5 + rnd() * 5;
      const b = new THREE.Mesh(new THREE.BoxGeometry(3, h, d), wallM[Math.floor(rnd() * 3)]); b.position.set(side * 4.2, h / 2, z - d / 2); b.castShadow = b.receiveShadow = true; scene.add(b);
      // roof eave
      const eave = new THREE.Mesh(new THREE.BoxGeometry(3.6, 0.18, d + 0.3), mat(0x4a3430, 0.7)); eave.position.set(side * 4.0, h + 0.05, z - d / 2); eave.castShadow = true; scene.add(eave);
      // canvases on the inner face in a grid
      for (let row = 0; row < 3; row++) for (let col = 0; col < Math.floor(d / 1.1); col++) {
        if (rnd() < 0.15) continue;
        const cw = 0.7 + rnd() * 0.3, chh = 0.55 + rnd() * 0.25;
        const fr = new THREE.Mesh(new THREE.BoxGeometry(0.06, chh + 0.08, cw + 0.08), frameM);
        const px = side * 2.66, py = 0.9 + row * 0.95 + rnd() * 0.1, pz = z - 0.6 - col * 1.1;
        fr.position.set(px, py, pz); fr.castShadow = true; scene.add(fr);
        const pm = new THREE.Mesh(new THREE.PlaneGeometry(cw, chh), pmats[Math.floor(rnd() * pmats.length)]);
        pm.position.set(px - side * 0.035, py, pz); pm.rotation.y = -side * Math.PI / 2; scene.add(pm);
      }
      z -= d + 0.2;
    }
  }
  // lantern strings with emissive lanterns
  const lanM = new THREE.MeshStandardMaterial({ color: 0xc41c1c, emissive: 0xff3a22, emissiveIntensity: 1.6, roughness: 0.5 });
  const lanterns = [];
  for (let k = 0; k < 9; k++) {
    const z = -2 - k * 5;
    for (let j = -2; j <= 2; j++) {
      const l = new THREE.Mesh(new THREE.SphereGeometry(0.16, 20, 14), lanM); l.scale.set(1, 0.85, 1);
      l.position.set(j * 0.95, 5.2 - (1 - (j / 2) ** 2) * 0.5, z); scene.add(l); lanterns.push(l);
    }
    if (k < 4) { const pl = new THREE.PointLight(0xff5a3a, 3.0, 7, 2); pl.position.set(0, 4.6, z); scene.add(pl); }
  }
  // a hero easel + canvas in the foreground (Zhao paints it)
  const easel = new THREE.Group(); scene.add(easel); easel.position.set(0.9, 0, 1.4); easel.rotation.y = -0.5;
  const wood = phys(0x8a5a30, { roughness: 0.6 });
  for (const [x, rz] of [[-0.35, 0.12], [0.35, -0.12]]) { const lg = new THREE.Mesh(new THREE.BoxGeometry(0.06, 2.0, 0.06), wood); lg.position.set(x, 1.0, 0); lg.rotation.z = rz; lg.castShadow = true; easel.add(lg); }
  const back = new THREE.Mesh(new THREE.BoxGeometry(0.06, 1.9, 0.06), wood); back.position.set(0, 0.95, -0.35); back.rotation.x = -0.2; easel.add(back);
  const heroC = paintingCanvas(0, 512, 400); const heroT = new THREE.CanvasTexture(heroC); heroT.colorSpace = THREE.SRGBColorSpace;
  const heroCanvas = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.86, 0.04), [mat(0xf2ead8), mat(0xf2ead8), mat(0xf2ead8), mat(0xf2ead8), new THREE.MeshStandardMaterial({ map: heroT, roughness: 0.5 }), mat(0xf2ead8)]);
  heroCanvas.position.set(0, 1.45, 0.06); heroCanvas.castShadow = true; easel.add(heroCanvas);
  // Zhao
  const zhao = makeChar({}); zhao.position.set(-0.35, 0, 1.6); scene.add(zhao);
  // background painters (smaller copies)
  const painters = [];
  for (let k = 0; k < 6; k++) {
    const p = makeChar({ shirt: [0xb05a3a, 0x3a7a5a, 0x7a5aa0, 0xc89a30, 0x3a5a8a, 0x8a3a3a][k], apron: 0xcfc8bc, hair: 0x241c18 });
    const side = k % 2 ? 1 : -1; p.position.set(side * 1.9, 0, -4 - k * 4.2); p.rotation.y = side * Math.PI / 2; scene.add(p); painters.push(p);
  }
  // 3-D sign: 大芬村 on a hanging board (canvas texture with CJK) + DAFEN in display face
  const signC = document.createElement('canvas'); signC.width = 512; signC.height = 1024; const sx = signC.getContext('2d');
  sx.fillStyle = '#a81818'; sx.fillRect(0, 0, 512, 1024); sx.strokeStyle = '#f5c76a'; sx.lineWidth = 16; sx.strokeRect(24, 24, 464, 976);
  sx.fillStyle = '#f5c76a'; sx.font = '900 260px "Noto Sans CJK SC"'; sx.textAlign = 'center';
  ['大', '芬', '村'].forEach((ch, i) => sx.fillText(ch, 256, 290 + i * 300));
  const signT = new THREE.CanvasTexture(signC); signT.colorSpace = THREE.SRGBColorSpace;
  const sign = new THREE.Mesh(new THREE.BoxGeometry(0.08, 2.2, 1.1), [new THREE.MeshStandardMaterial({ map: signT, roughness: 0.4, emissive: 0x401010, emissiveIntensity: 0.4 }), mat(0x7a1010), mat(0x7a1010), mat(0x7a1010), mat(0x7a1010), mat(0x7a1010)]);
  sign.position.set(2.45, 4.6, -7.5); sign.castShadow = true; scene.add(sign);
  const signGlow = new THREE.PointLight(0xffb060, 2.0, 4, 2); signGlow.position.set(1.8, 4.6, -7.5); scene.add(signGlow);
  // light shafts: additive cones from the sun side
  const shaftM = new THREE.MeshBasicMaterial({ color: 0xffb080, transparent: true, opacity: 0.06, blending: THREE.AdditiveBlending, depthWrite: false, fog: false });
  for (let k = 0; k < 4; k++) { const s = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 1.6, 16, 24, 1, true), shaftM); s.position.set(-1.5 + k * 0.9, 5, -10 - k * 6); s.rotation.set(0.5, 0, 0.55); scene.add(s); }
  // dust motes
  const dg = new THREE.BufferGeometry(); const dn = 500, dp = new Float32Array(dn * 3); const drn = M.mulberry32(9);
  for (let i = 0; i < dn; i++) { dp[i * 3] = (drn() - 0.5) * 5; dp[i * 3 + 1] = drn() * 5; dp[i * 3 + 2] = 3 - drn() * 30; }
  dg.setAttribute('position', new THREE.BufferAttribute(dp, 3));
  const dust = new THREE.Points(dg, new THREE.PointsMaterial({ color: 0xffd8a8, size: 0.03, transparent: true, opacity: 0.7, depthWrite: false }));
  scene.add(dust);

  return { scene, camera: cam, bloom: 0.35, bloomThreshold: 0.9, bloomRadius: 0.6,
    update(t) {
      // Zhao performance: painting, then notices camera (anticipation -> brow lift -> grin), then turns to present the alley
      const paint = Math.sin(t * 7);
      const notice = E.outBack(prog(t, 1.2, 1.6), 2.0);
      const present = E.inOutCubic(prog(t, 3.0, 3.7));
      pose(zhao, {
        yaw: lerp(0.35, -0.15, notice) + present * 0.5,
        headYaw: lerp(0.5, -0.1, notice) + present * 0.7, headPitch: lerp(0.12, -0.05, notice),
        brow: notice * 0.9 - present * 0.3 + 0.15 * wobble(t - 1.4, 3, 6),
        blink: (t > 2.4 && t < 2.52) ? 0 : 1,
        mouthOpen: t > 1.35 && t < 1.9 ? 0.7 : 0,
        armR: present > 0 ? [lerp(-0.6 + 0.15 * paint * (1 - notice), -1.6, present), lerp(-0.6, -0.1, present)] : [-0.6 + 0.15 * paint * (1 - notice), -0.6],
        armL: [0.1, -0.25], lean: -0.04 * notice + 0.03 * wobble(t - 1.3, 2.5, 5), look: [lerp(0.8, 0, notice), 0],
      });
      painters.forEach((p, k) => { pose(p, { armR: [-0.7 + 0.2 * Math.sin(t * 6 + k), -0.6], headYaw: 0.1 * Math.sin(t + k), yaw: p.rotation.y, blink: 1 }); });
      dust.position.y = Math.sin(t * 0.3) * 0.1; dust.rotation.y = t * 0.02;
      // camera: close on Zhao + canvas -> pull back and crane up to reveal the alley -> settle
      const k1 = E.inOutCubic(prog(t, 2.2, 5.6));
      const cx = lerp(0.35, 0.0, k1), cy = lerp(2.05, 3.3, k1), cz = lerp(4.7, 9.0, k1);
      const tx = lerp(-0.1, 0.2, k1), ty = lerp(1.85, 2.2, k1), tz = lerp(1.6, -8, k1);
      G.lookFrom(cam, [cx + 0.05 * Math.sin(t * 0.7), cy, cz], [tx, ty, tz]);
      cam.fov = lerp(30, 42, k1); cam.updateProjectionMatrix();
    } };
}

// ---------------------------------------------------------------- typography system (no pills)
// 1 editorial subtitle: clean, bottom-third, soft shadow, emphasis by face change (serif italic gold)
function subtitle(ctx, parts, t, t0, t1, y = H * 0.80) {
  const a = Math.min(E.outCubic(prog(t, t0, t0 + 0.25)), 1 - prog(t, t1 - 0.2, t1));
  if (a <= 0) return;
  const segs = parts.map(([s, em]) => ({ s, f: em ? font(66, 400, 'Serif') : font(54, 700, 'UI'), em }));
  let wsum = 0; segs.forEach((g) => { ctx.font = g.f; g.w = ctx.measureText(g.s).width; wsum += g.w; });
  let x = (W - wsum) / 2;
  ctx.save(); ctx.globalAlpha = a; ctx.shadowColor = 'rgba(0,0,0,0.55)'; ctx.shadowBlur = 18; ctx.shadowOffsetY = 4;
  segs.forEach((g) => { ctx.font = g.f; ctx.fillStyle = g.em ? GOLD : '#FFFFFF'; ctx.fillText(g.s, x, y + (1 - a) * 16); x += g.w; });
  ctx.restore();
}
// 2 location label: map pin + name + leader line (integrated, anchored to a point in the frame)
function locationLabel(ctx, t, t0, x, y, t1 = 99) {
  const p = E.outCubic(prog(t, t0, t0 + 0.5)); if (p <= 0) return;
  const out = 1 - prog(t, t1, t1 + 0.3); if (out <= 0) return;
  ctx.save(); ctx.globalAlpha = out;
  ctx.strokeStyle = 'rgba(255,255,255,0.85)'; ctx.lineWidth = 3;
  ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x, y - 150 * p); ctx.lineTo(x + 70 * p, y - 150 * p); ctx.stroke();
  // pin
  ctx.fillStyle = BRAND; ctx.beginPath(); ctx.arc(x, y, 12 * p, 0, Math.PI * 2); ctx.fill(); ctx.strokeStyle = '#fff'; ctx.lineWidth = 4; ctx.stroke();
  const q = E.outCubic(prog(t, t0 + 0.2, t0 + 0.7));
  ctx.globalAlpha = q * out;
  ctx.font = font(64, 800, 'Display'); ctx.fillStyle = '#fff'; ctx.shadowColor = 'rgba(0,0,0,0.5)'; ctx.shadowBlur = 14;
  ctx.fillText('DAFEN', x + 86, y - 132 + (1 - q) * 20);
  ctx.font = '700 34px "Noto Sans CJK SC"'; ctx.fillStyle = GOLD; ctx.fillText('大芬村  ·  SHENZHEN', x + 88, y - 84 + (1 - q) * 20);
  ctx.restore();
}
// 3 dimensional number reveal: per-glyph 3D-ish rise with extrusion + light sweep, towards camera
function bigNumber(ctx, str, t, t0, cy) {
  const p = prog(t, t0, t0 + 0.6); if (p <= 0) return;
  const size = 230, f = font(size, 800, 'Display'); const L = layout(ctx, str, f, -0.03 * size);
  const x0 = (W - L.width) / 2;
  L.glyphs.forEach((g, j) => {
    const k = M.springU(t * 2, (t0 + j * 0.04) * 2, M.SPRING.bouncy); if (k <= 0) return;
    const sc = lerp(2.2, 1, Math.min(1, k)); const y = cy + (1 - Math.min(1, k)) * -60;
    ctx.save(); ctx.translate(x0 + g.cx, y); ctx.scale(sc, sc);
    for (let d = 14; d > 0; d--) { ctx.font = f; ctx.textAlign = 'center'; ctx.fillStyle = `rgb(${120 - d * 3},${40 - d},${10})`; ctx.fillText(g.ch, d * 0.6, d * 1.0); }
    const gr = ctx.createLinearGradient(0, -size * 0.8, 0, 0); gr.addColorStop(0, '#FFF3C8'); gr.addColorStop(1, '#F0A040');
    ctx.font = f; ctx.textAlign = 'center'; ctx.fillStyle = gr; ctx.fillText(g.ch, 0, 0);
    ctx.restore();
  });
  // light sweep
  const s = prog(t, t0 + 0.5, t0 + 1.2);
  if (s > 0 && s < 1) { ctx.save(); ctx.globalCompositeOperation = 'lighter'; const sx = lerp(x0 - 200, x0 + L.width + 200, s); const gr = ctx.createLinearGradient(sx - 80, 0, sx + 80, 0); gr.addColorStop(0, 'rgba(255,255,255,0)'); gr.addColorStop(0.5, 'rgba(255,255,255,0.35)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); ctx.fillStyle = gr; ctx.fillRect(x0 - 40, cy - size, L.width + 80, size + 40); ctx.restore(); }
  const q = E.outCubic(prog(t, t0 + 0.35, t0 + 0.8));
  if (q > 0) { ctx.save(); ctx.globalAlpha = q; ctx.font = font(44, 700, 'UI'); ctx.fillStyle = '#fff'; ctx.textAlign = 'center'; ctx.shadowColor = 'rgba(0,0,0,0.6)'; ctx.shadowBlur = 12; ctx.fillText('Van Gogh copies from one studio.', W / 2, cy + 80); ctx.restore(); }
}

M.film({
  fonts: [font(100, 800, 'Display'), font(40, 700, 'UI'), font(60, 400, 'Serif'), '700 40px "Noto Sans CJK SC"'],
  samples: 1,
  async init() { await G.initGL({ exposure: 1.05 }); S.alley = alleySet(); },
  draw(ctx, u, t) {
    G.renderSet(ctx, S.alley, t, u);
    // depth grade: warm top, cool bottom, subtle vignette
    const v = ctx.createRadialGradient(W / 2, H * 0.45, H * 0.2, W / 2, H * 0.5, H * 0.75);
    v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(10,4,12,0.55)'); ctx.fillStyle = v; ctx.fillRect(0, 0, W, H);
    subtitle(ctx, [['He started out as a ', 0], ['farmer.', 1]], t, 0.2, 2.2);
    subtitle(ctx, [['Now thousands paint here. ', 0], ['By hand.', 1]], t, 2.6, 5.4);
    locationLabel(ctx, t, 3.6, W * 0.30, H * 0.42, 5.6);
    bigNumber(ctx, '100,000+', t, 5.9, H * 0.30);
  },
  post(ctx, u, t) {
    // film grain
    const r = M.mulberry32(Math.floor(t * 60) + 7);
    ctx.save(); ctx.globalAlpha = 0.05; for (let i = 0; i < 1400; i++) { ctx.fillStyle = r() > 0.5 ? '#fff' : '#000'; ctx.fillRect(r() * W, r() * H, 2, 2); } ctx.restore();
  },
});
