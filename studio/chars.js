import * as M from './motion.js';
import * as G from './gl.js';
const { THREE } = G;
const { lerp } = M;
// ---------------------------------------------------------------- materials
export const mat = (color, rough = 0.6, extra = {}) => new THREE.MeshStandardMaterial({ color, roughness: rough, ...extra });
export const phys = (color, extra = {}) => new THREE.MeshPhysicalMaterial({ color, roughness: 0.45, clearcoat: 0.3, ...extra });

// ---------------------------------------------------------------- dimensional character
export function makeChar({ skin = 0xe2b48a, shirt = 0x4a76b0, apron = 0xd8c49e, pants = 0x3c3836, hair = 0x18161a, scale = 1, painter = true } = {}) {
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
  const jaw = new THREE.Mesh(new THREE.SphereGeometry(0.29, 32, 24), mSkin); jaw.position.set(0, -0.11, 0.05); jaw.castShadow = false; jaw.receiveShadow = false; jaw.scale.set(1, 0.85, 0.95); head.add(jaw);
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
export function pose(ch, { walk = 0, amp = 0, yaw = 0, headYaw = 0, headPitch = 0, brow = 0, blink = 0, mouthOpen = 0, armR = [0.2, -0.3], armL = [0.1, -0.2], lean = 0, bob = 0, look = [0, 0] }) {
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

