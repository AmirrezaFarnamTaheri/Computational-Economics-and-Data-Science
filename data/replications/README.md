# Empirical Replication Data

## Card & Krueger (1994) fast-food panel

- File: `card_krueger_1994_njmin3.csv`
- Observations: 820 restaurant-wave rows (410 restaurants across two survey waves before missing-data adjustments).
- Variables used in the curriculum replication: New Jersey indicator `nj`, post-wave indicator `d`, interaction `d_nj`, full-time-equivalent employment `fte`, and restaurant/region controls.
- Provenance: public replication mirror of the Card & Krueger fast-food survey; the mirror documents that its source is David Card's public data archive.
- Retrieved for this project: 2026-08-21.
- SHA-256: `5dd549a40790d58cd1705474297ba9cf069e3dbc7fd561e4f6e14a1cde98a4d2`.

The notebook `Appendix/T4_Replication_Card_Krueger_1994.ipynb` reproduces the two-by-two DiD and regression representation. It does not claim that a two-wave panel can test pre-treatment parallel trends.

Other course datasets retain their provenance notes in `data/README.md` and `docs/resources/datasets.md`.
