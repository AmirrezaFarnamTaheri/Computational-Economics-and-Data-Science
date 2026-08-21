# DESIGN.md — Computational Economics & Data Science Visual Design System

> **Aesthetic Essence:** *Austere Academic Precision* (Editorial Quantitative Journal)  
> **Brand Adjectives:** Rigorous · Authoritative · Architectural · Tactile · Uncluttered  
> **Stack Adapter:** Plain CSS Custom Properties (OKLCH) + MkDocs Material Theme Extensions  
> **Hallmark Version:** 2026 Anti-Slop Compliant

---

## 1. Aesthetic Direction & Positioning

- **Artifact Type:** Interactive Academic Textbook, Quantitative Research Portal & WebGL Simulation Laboratory.
- **Audience:** Graduate students, quantitative researchers, macroeconomists, and computational data scientists.
- **Single Core Outcome:** Seamless understanding of complex economic theory through mathematically rigorous derivations, reproducible code, and tactile, high-performance interactive simulations.
- **Signature Move:** Asymmetric split-screen laboratory view — formal LaTeX theorem derivations on the left with a live, interactive WebGL/Matter.js parameter manifold on the right, sharing real-time synchronized numerical state.

---

## 2. Typography System

| Role | Font Family | Weights | Usage & Rules |
| :--- | :--- | :--- | :--- |
| **Display / Headings** | `Newsreader`, Georgia, serif | 600, 700 | Primary chapter titles, module headers, theorem labels. **Always roman (`font-style: normal`) — zero italic headings.** |
| **Section Heads / UI** | `Cabinet Grotesk`, `Satoshi`, sans-serif | 500, 600, 700 | Interactive lab controls, badges, table headers, navigation links. |
| **Body Text** | `Satoshi`, -apple-system, sans-serif | 400, 500 | Explanatory narrative, economic intuition, problem sets. |
| **Code & Tabular Numbers** | `JetBrains Mono`, monospace | 400, 500 | Python code, matrix outputs, `font-variant-numeric: tabular-nums`. |

### Modular Scale (Ratio: 1.250 — Major Third)
- `--font-size-xs`: `0.75rem` (12px)
- `--font-size-sm`: `0.875rem` (14px)
- `--font-size-base`: `1.000rem` (16px)
- `--font-size-md`: `1.250rem` (20px)
- `--font-size-lg`: `1.563rem` (25px)
- `--font-size-xl`: `1.953rem` (31px)
- `--font-size-xxl`: `2.441rem` (39px)

---

## 3. OKLCH Color Palette & Semantic Roles (60-30-10 Distribution)

```css
:root {
  /* 60% Dominant Backgrounds & Surfaces (Warm Academic Slate / Alabaster) */
  --color-bg: oklch(0.985 0.005 85);            /* #fcfbf9 Warm Ivory White */
  --color-surface: oklch(0.965 0.008 85);       /* #f5f4ef Surface Card */
  --color-surface-hover: oklch(0.945 0.012 85); /* #eee9e0 Card Hover */
  --color-border: oklch(0.880 0.015 85);        /* #dfdcce Hairline Border */
  --color-border-focus: oklch(0.450 0.180 250); /* #2a6fdb Focus Ring */

  /* 30% Typographic Content & Neutrals */
  --color-text-primary: oklch(0.180 0.020 260);   /* #1a1e24 Deep Charcoal */
  --color-text-secondary: oklch(0.420 0.025 260); /* #525a66 Muted Text */
  --color-text-tertiary: oklch(0.600 0.020 260);  /* #8892a0 Meta / Footnotes */

  /* 10% Sharp Accents & Semantic Signals */
  --color-accent: oklch(0.580 0.220 38);          /* #d9480f Oxford Crimson / Terracotta */
  --color-accent-hover: oklch(0.520 0.230 38);    /* #b83808 Pressed Accent */
  --color-accent-subtle: oklch(0.940 0.050 38);   /* #fdece5 Accent Tint Fill */

  --color-success: oklch(0.620 0.160 145);        /* #2b8a3e Academic Green */
  --color-warning: oklch(0.720 0.160 75);         /* #e67700 Warning Amber */
  --color-error: oklch(0.580 0.220 25);           /* #c92a2a Diagnostic Red */
  --color-info: oklch(0.550 0.180 240);           /* #1971c2 Theory Callout Blue */

  /* Spacing Scale (4-pt base) */
  --space-1: 0.25rem;  /* 4px */
  --space-2: 0.50rem;  /* 8px */
  --space-3: 0.75rem;  /* 12px */
  --space-4: 1.00rem;  /* 16px */
  --space-6: 1.50rem;  /* 24px */
  --space-8: 2.00rem;  /* 32px */
  --space-12: 3.00rem; /* 48px */
  --space-16: 4.00rem; /* 64px */

  /* Radii (Strict discipline: max 2 values) */
  --radius-sm: 4px;   /* Buttons, chips, inputs */
  --radius-md: 8px;   /* Panels, cards, interactive visualizer frames */

  /* Elevation (Defined hairline edge over diffuse blur) */
  --shadow-card: 0 1px 3px rgba(0, 0, 0, 0.05), 0 0 0 1px var(--color-border);
  --shadow-dropdown: 0 4px 12px rgba(0, 0, 0, 0.08), 0 0 0 1px var(--color-border);
}

/* Dark Mode (Designed elevation via lightness, not inverted black) */
[data-theme="dark"] {
  --color-bg: oklch(0.140 0.015 260);            /* #0f1318 Slate Charcoal */
  --color-surface: oklch(0.180 0.018 260);       /* #171c24 Elevated Surface */
  --color-surface-hover: oklch(0.220 0.022 260); /* #202732 Card Hover */
  --color-border: oklch(0.260 0.020 260);        /* #293240 Hairline Border */

  --color-text-primary: oklch(0.920 0.010 85);   /* #e6e8eb Off-White */
  --color-text-secondary: oklch(0.700 0.015 85); /* #9da5b1 Muted Text */
  --color-text-tertiary: oklch(0.500 0.015 260); /* #636e7d Metadata */

  --color-accent: oklch(0.680 0.200 42);          /* #f76707 Vibrant Amber-Orange */
  --color-accent-hover: oklch(0.740 0.180 42);
  --color-accent-subtle: oklch(0.220 0.050 42);

  --shadow-card: 0 1px 3px rgba(0, 0, 0, 0.3), 0 0 0 1px var(--color-border);
}
```

---

## 4. The 8-State Interactive Component Discipline

Every interactive UI component in the web lab and documentation (buttons, sliders, tabs, parameter inputs) must implement all **8 interactive states**:

1. **Default (`:default`)**: Clean resting elevation with `--shadow-card` and subtle border.
2. **Hover (`:hover`, `.is-hover`)**: Subtle surface lightening + accent border shift.
3. **Focus-Visible (`:focus-visible`, `.is-focus`)**: Visible 2px outline `var(--color-border-focus)` with 2px offset.
4. **Active (`:active`, `.is-active`)**: Subtle 1px translation `translateY(1px)` simulating physical compression.
5. **Disabled (`[disabled]`, `.is-disabled`)**: Opacity 0.45, `cursor: not-allowed`, muted neutral background.
6. **Loading (`[data-state="loading"]`)**: Animated subtle spinner or pulse, retaining fixed width to prevent layout shift.
7. **Error (`[data-state="error"]`)**: Border color `var(--color-error)`, contextual tooltip, high contrast warning text.
8. **Success (`[data-state="success"]`)**: Border color `var(--color-success)`, checkmark icon, transient positive feedback.

---

## 5. Anti-Patterns & De-Slop Prohibitions (NEVER LIST)

- ❌ **No Generic SaaS Blue/Purple Gradients on White**: Replaced by dedicated OKLCH warm slate + terracotta accent.
- ❌ **No Italic Headings or Theorem Titles**: Headings are always upright roman (`font-style: normal`).
- ❌ **No Centered Numeric Table Columns**: Numbers are always right-aligned with `font-variant-numeric: tabular-nums`.
- ❌ **No Fake Numbers or Fabricated Metrics**: Real benchmarks from `cProfile` and empirical tests only.
- ❌ **No Hand-Drawn Fake Browser Chrome**: No simulated window pills or fake traffic lights. Clean `<figure>` frames only.
- ❌ **No Layout-Shifting Animations**: Motion strictly limited to `transform` and `opacity` with durations <= 250ms.
- ❌ **No Horizontal Mobile Overflow**: Non-negotiable `overflow-x: clip` with test coverage at 320px, 375px, 414px, and 768px.

---

## 6. Hallmark Pre-Emit Quality Gate Stamp

Before delivering any visual or interactive update, verify against the 6 Hallmark Axes:
`/* Hallmark · pre-emit critique: Philosophy:5 Hierarchy:5 Execution:5 Specificity:5 Restraint:5 Variety:5 */`
