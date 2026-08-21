# Computational Economics & Data Science — Multi-Stack Design System & Frontend Architecture

> **A rigorous, anti-slop design system uniting Academic Presentation Engineering, Modern Web UI Standards, Three.js 3D Geometric Manifolds, Cobe.js Optimization Networks, and Vanta.js Atmospheric WebGL Shaders.**

---

## 1. Multi-Stack Architectural Matrix

| Stack Layer | Skill Integration | Core Purpose & Technical Mandate |
|:---|:---|:---|
| **Academic Slides & Deck Engine** | `/academic-slides`<br>`/frontend-slides` | Zero-dependency, browser-native presentation engine. Strict **100dvh viewport fitting** (no internal scrolling), Beamer-inspired theorem environments (`.theorem-box`, `.proof-box` with Q.E.D. `\25A1`), KaTeX mathematical typography, progressive disclosure (`data-overlay`, `.reveal`), and `@media print` PDF handout compilation. |
| **Anti-Slop UI & Design System** | `/frontend-design`<br>`/frontend-design-deslop`<br>`/ui-ux-pro-max`<br>`/frontend-ui-engineering` | Strategy-driven design. Strict OKLCH mathematical color system (60-30-10 distribution), 8-state component interaction matrix, elimination of generic AI slop (no default purple gradients, no blob radii, no missing hover/focus states), WCAG 2.2 AA accessibility, and tabular numeric alignment. |
| **Interactive 3D Manifolds** | `/skills-threejs` | WebGL 3D parametric visualization of convex epigraphs, Lorentz second-order cones, PSD cones, and supporting hyperplanes. PBR lighting (Key + Rim + Ambient), strict WebGL memory lifecycle (`.dispose()`), and clamped DPR ($\le 2.0$). |
| **Network & Global Viz** | `/skills-cobejs` | Lightweight WebGL interactive globe for distributed optimization, ADMM consensus networks, and decentralized node topologies with custom coordinate markers and dynamic rotation. |
| **Atmospheric Shaders** | `/skills-vantajs` | Subtle, performant WebGL background shaders (geometric waves, net topologies) for hero sections and lecture openers, with container bounding, resize observers, and unmount destruction. |

---

## 2. Academic Presentation & Slide Engineering (`/academic-slides`, `/frontend-slides`)

### Viewport Fitting Mandate (Zero-Scroll Policy)
Every presentation slide and lecture frame MUST fit within exactly one viewport (`100vh` / `100dvh`).
```css
/* Mandatory Viewport Lock */
html, body {
  height: 100%;
  overflow-x: hidden;
}
html {
  scroll-snap-type: y mandatory;
  scroll-behavior: smooth;
}
.frame, .slide {
  width: 100vw;
  height: 100vh;
  height: 100dvh;
  overflow: hidden;
  scroll-snap-align: start;
  display: flex;
  flex-direction: column;
  position: relative;
  box-sizing: border-box;
}
.frame-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  max-height: 100%;
  overflow: hidden;
  padding: var(--frame-padding, clamp(1rem, 4vw, 4rem));
}
```

### Academic Typography & Beamer Environments
- **Typeface Pairing**: Computer Modern / Latin Modern Roman display serif paired with Charter / Inter for body, and Fira Code for algorithms.
- **Theorem & Proof Styling**:
```css
.theorem-box, .lemma-box, .definition-box {
  border-left: 4px solid var(--convex-primary);
  background: var(--surface-secondary);
  padding: clamp(0.5rem, 1.5vw, 1rem) clamp(0.75rem, 2vw, 1.5rem);
  margin: clamp(0.25rem, 0.5vw, 0.5rem) 0;
  max-height: min(40vh, 350px);
}
.proof-box {
  border-left: 2px solid var(--text-muted);
  background: var(--surface-elevated);
  padding: clamp(0.4rem, 1vw, 0.75rem) clamp(0.75rem, 2vw, 1.5rem);
  font-style: italic;
}
.proof-box::after {
  content: '\25A1'; /* Q.E.D. Halmos square */
  float: right;
  font-style: normal;
  color: var(--text-secondary);
}
```

### Progressive Disclosure & Overlay Engine
- **Linear Reveals**: Elements with class `.reveal` sequentially gain `.visible` on user advance.
- **Non-Linear Overlays**: `data-overlay="spec"` syntax (e.g. `"2-"` visible from step 2 onward, `"-3"` visible steps 1 to 3).
- **Print / Handout Mode (`@media print`)**: Unrolls all overlays, strips navigation UI, forces `break-after: page`, and converts into clean black-and-white PDF handouts.

---

## 3. Anti-Slop Design Tokens & UI/UX Standards (`/frontend-design-deslop`, `/ui-ux-pro-max`)

### OKLCH Palette (60-30-10 Distribution)
```css
:root {
  /* 60% Base / Surface Neutrals */
  --bg-canvas: oklch(0.985 0.005 240);
  --bg-surface: oklch(0.96 0.01 240);
  --bg-elevated: oklch(1.0 0 0);
  --text-primary: oklch(0.18 0.02 240);
  --text-secondary: oklch(0.42 0.03 240);
  --text-muted: oklch(0.60 0.02 240);
  --border-subtle: oklch(0.88 0.015 240);
  --border-strong: oklch(0.70 0.03 240);

  /* 30% Mathematical Domain Colors */
  --convex-primary: oklch(0.45 0.16 245);       /* Primal Blue */
  --convex-dual: oklch(0.52 0.20 335);          /* Dual Magenta */
  --convex-cone: oklch(0.50 0.18 285);          /* Conic Violet */

  /* 10% Optimization & State Accents */
  --convex-optima: oklch(0.60 0.19 145);        /* Optimal Emerald */
  --convex-infeasible: oklch(0.58 0.22 25);     /* Infeasible Coral */
  --convex-warning: oklch(0.72 0.16 75);        /* Warning Amber */
}
```

### 8-State Interactive Component Matrix
Every interactive control (buttons, sliders, toggles, formula inspectors) MUST define all 8 states:
1. `default`: Clean border, high-contrast text, subtle shadow.
2. `hover`: Subtle tint shift, crisp border highlight, zero layout shift.
3. `focus-visible`: 2px offset solid outline in `--convex-primary`.
4. `active`: 1px inward transform, darkened background.
5. `disabled`: Opacity $0.45$, `cursor: not-allowed`, no hover response.
6. `loading`: Animated SVG spinner or skeleton pulse.
7. `error`: Red outline with aria-invalid="true" and inline message.
8. `success`: Green check confirmation badge.

---

## 4. Interactive 3D WebGL Manifolds (`/skills-threejs`)

### Three.js Engineering Standards
1. **PBR Lighting Pipeline**:
   - `MeshPhysicalMaterial` / `MeshStandardMaterial` for convex sets and epigraphs (roughness $0.35$, metalness $0.10$).
   - Three-point lighting setup: Key directional light ($I=2.0$), cool rim light ($I=0.85$), and warm ambient fill ($I=0.45$).
2. **GPU Lifecycle & Memory Management**:
   ```javascript
   function cleanupScene(scene, renderer) {
     scene.traverse((object) => {
       if (object.geometry) object.geometry.dispose();
       if (object.material) {
         if (Array.isArray(object.material)) {
           object.material.forEach(m => m.dispose());
         } else {
           object.material.dispose();
         }
       }
     });
     renderer.dispose();
   }
   ```
3. **Clamped DPR**: Always enforce `renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))` to prevent mobile GPU thermal throttling.
4. **Reduced Motion**: If `window.matchMedia('(prefers-reduced-motion: reduce)').matches`, halt auto-rotation and render static view with orbit controls.

---

## 5. Distributed Network Optimization Globe (`/skills-cobejs`)

### Cobe.js Integration Architecture
- Used in Lecture 15 & 21 for distributed ADMM, federated optimization, and multi-agent consensus networks.
- Clamped DPR, responsive canvas resizing, dynamic location markers representing consensus nodes, and smooth inertial drag.

---

## 6. Atmospheric WebGL Shaders (`/skills-vantajs`)

### Vanta.js Presentation Standards
- Used for hero slide headers and module transition cards.
- Background shader effects (e.g. `VANTA.WAVES`, `VANTA.NET`) running at low vertex density to preserve 60 FPS UI interaction.
- Container bounding, explicit resize event listeners, and unmount destruction (`effect.destroy()`).

---

## 7. Anti-Slop Quality Gate Checklist

- [x] **Zero Viewport Overflow**: All slides fit 100dvh across desktop, tablet, and mobile.
- [x] **Mathematical Integrity**: KaTeX rendered everywhere; no raw unicode equations.
- [x] **No AI Clichés**: Zero default purple gradients, zero unstyled buttons, zero blob radiuses.
- [x] **Tabular Numeric Precision**: `font-variant-numeric: tabular-nums` for all matrices and coordinates.
- [x] **Resource Safety**: All WebGL shaders and Three.js scenes implement strict teardown listeners.
- [x] **Print Ready**: Full `@media print` support for instant PDF slide deck generation.
