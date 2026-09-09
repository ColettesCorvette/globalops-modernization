# Feuille de route

Quatre chantiers. Ils ne sont pas indépendants : le pipeline d'assets (4) conditionne le HUD (1),
et l'injection de code sert à la fois au raw input (2) et à la physique (3).

```
                    ┌─────────────────────────────┐
                    │ 4. Pipeline d'assets        │  ← prérequis
                    │    extraction REZ / DTX     │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │ 1. HUD & interface HD       │
                    └─────────────────────────────┘

                    ┌─────────────────────────────┐
                    │ Ultimate ASI Loader         │  ← socle commun
                    └──────┬───────────────┬──────┘
                           │               │
              ┌────────────▼───┐   ┌───────▼──────────────┐
              │ 2. Raw input   │   │ 3. Physique / FPS    │
              └────────────────┘   └──────────────────────┘
```

## Ordre recommandé

| # | Chantier | Effort | Gain | Dépend de |
|---|---|---|---|---|
| 4 | [Pipeline d'assets](06-assets-pipeline.md) | faible | débloque tout le reste | — |
| 1 | [HUD & interface HD](03-hud-upscale.md) | moyen | fort — c'est ce qui se voit | 4 |
| 3 | [Physique / FPS](05-fps-physics.md) | élevé | fort — supprime un plafond subi | ASI Loader |
| 2 | [Raw input souris](04-raw-input.md) | moyen | fort en FPS compétitif | ASI Loader |

Le chantier 4 vient en premier parce qu'il coûte peu et débloque le plus visible.
Les chantiers 2 et 3 partagent le même mécanisme d'injection : les traiter ensemble évite de
monter deux fois la même infrastructure.

## Jalons

- [x] Jeu fonctionnel en résolution native
- [x] Physique stable (plafond FPS)
- [ ] Seuil FPS optimal déterminé (monter par paliers : 100, 120, 144)
- [ ] Extraction des `.rez` opérationnelle
- [ ] Test décisif d'échelle du HUD
- [ ] Ultimate ASI Loader en place et plugin vide qui charge
- [ ] Clamp du delta time de la simulation
- [ ] Raw input souris
- [ ] Textures HD

## Hors périmètre

- **Portage 64 bits** — sans intérêt technique ici (aucun gain de perf ou de rendu) et hors de portée
  sans le code source. Voir `CLAUDE.md`.
- **Contournement de la protection 1.27** — non traité. Le projet reste en 1.16.
- **Multijoueur d'époque** — DirectPlay désactivé sur Windows 10/11, GameSpy éteint depuis 2014.
