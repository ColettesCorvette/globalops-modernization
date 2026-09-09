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

## Piste communautaire — à explorer en priorité

Une communauté active existe autour du jeu : Discord, correctifs de compatibilité pour systèmes modernes,
**serveurs multijoueur toujours en ligne**, et un *Global Operations Remake Mod* (GORM) en cours.

**Déduction importante :** le multijoueur exige que client et serveur partagent la même build. Si des serveurs
tournent et que des gens y jouent, c'est qu'il existe une façon de lancer la **1.27** sur un système actuel.
Le problème considéré comme bloquant dans ce projet est donc déjà résolu quelque part.

Avant d'engager les quatre chantiers, prendre contact :

- [ ] Rejoindre le Discord communautaire
- [ ] Déterminer comment la communauté lance la 1.27
- [ ] Vérifier ce qui existe déjà en matière de correctifs HD / HUD / input
- [ ] Se signaler : les chantiers 1 à 4 les intéressent probablement
- [ ] Évaluer GORM — recoupement ou complémentarité avec ce projet

Ne pas refaire ce qui existe. Cette étape peut rendre plusieurs chantiers caducs, ou au contraire
fournir des interlocuteurs compétents.

## Multijoueur — reclassé

Initialement écarté (DirectPlay désactivé sur Windows 10/11, GameSpy éteint depuis 2014), le multijoueur
redevient envisageable puisque **des serveurs communautaires fonctionnent**. Prérequis : pouvoir exécuter
la build 1.27, sujet à éclaircir avec la communauté.

## Hors périmètre

- **Portage 64 bits** — sans intérêt technique ici (aucun gain de perf ou de rendu) et hors de portée
  sans le code source. Voir `CLAUDE.md`.
- **Développement d'un contournement de la protection SafeDisc** — non traité dans ce projet.
  Le jeu tourne en 1.16 ; pour la 1.27, voir la piste communautaire ci-dessus.
