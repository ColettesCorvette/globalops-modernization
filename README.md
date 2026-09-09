# Global Operations — Modernisation

Rétro-ingénierie et modernisation de **Global Operations** (Barking Dog Studios / Crave, 2002),
FPS bâti sur le moteur **LithTech Talon** (génération 2.x).

**État : le jeu tourne.** 2560×1440 natif, 32 bits, plein écran, Direct3D 8 traduit en Vulkan, physique stable.
---

## Démarrage rapide

> Les chemins de cette documentation utilisent `C:\Games\GlobalOps` comme dossier d'installation
> et `player` comme nom de profil. Adapter aux siens.

```bash
cd "C:/Games/GlobalOps" && ./globalops.exe
```

| Élément | Valeur |
|---|---|
| Installation | `C:\Games\GlobalOps` — build **1.16** homogène |
| Exécutable | sans SafeDisc, ABI cohérente avec les DLL |
| Rendu | DXVK 3.1 — D3D8 → Vulkan |
| Affichage | 2560×1440 · **32 bits** · plein écran |
| Framerate | plafonné à **60** (obligatoire, voir plus bas) |
| Profil actif | `player` (défini dans `autoexec.cfg`) |

### Trois règles à ne jamais enfreindre

1. **`bitdepth` doit valoir 32.** En 16 bits le jeu ne démarre pas — et selon le contexte, il sort proprement
   (`ExitCode 0`, aucun message) ou crashe en `0xC0000005`. C'est la cause n°1 des faux diagnostics de ce projet.
2. **Le framerate doit rester plafonné.** Sans plafond, la détection de collision laisse traverser les murs
   et le joueur s'y encastre définitivement.
3. **Ne jamais mélanger les builds.** 1.16 et 1.27 ont des ABI incompatibles ; le moteur le vérifie et,
   quand il ne le vérifie pas, il crashe.

---

## Structure du dépôt

```
README.md                    ce fichier
docs/
  ROADMAP.md                 les 4 chantiers, priorités et dépendances
  01-diagnostic.md           historique du diagnostic et fausses pistes
  02-installation.md         recette d'installation reproductible
  03-hud-upscale.md          chantier 1 — HUD et interface haute résolution
  04-raw-input.md            chantier 2 — souris en raw input
  05-fps-physics.md          chantier 3 — découpler physique et rendu
  06-assets-pipeline.md      chantier 4 — extraction et remplacement des assets
config/                      fichiers de configuration validés
tools/                       scripts d'analyse binaire
```

Aucun binaire ni asset du jeu n'est versionné (voir `.gitignore`) : le dépôt ne contient que de la
documentation, des configurations et des outils.

---

## Ce qui a été résolu

| Obstacle | Cause réelle |
|---|---|
| Le jeu ne démarrait pas | SafeDisc — `secdrv.sys` retiré de Windows 10+ |
| « Échap ferme le jeu » | `bitdepth 16` → device Direct3D 8 impossible |
| Lignes verticales grises | shell de **développement** du SDK, pas celui du jeu |
| Crash `0xC0000005` | encore `bitdepth 16`, cette fois via DXVK |
| Coincé dans les murs | physique cadencée sur un framerate sans plafond |

Détail complet et fausses pistes : [`docs/01-diagnostic.md`](docs/01-diagnostic.md).

---

## Limite connue

Le jeu tourne en **1.16** (version CD d'origine), sans les correctifs de gameplay et d'équilibrage des
patchs officiels 1.2 et 2.0 — ces patchs conservent SafeDisc, et aucun exécutable 1.27 exploitable n'est
disponible. Sans conséquence en solo ; bloquant pour le multijoueur d'époque.

---

## Licence

Ce dépôt est publié sous licence **MIT** — voir [`LICENSE`](LICENSE).

Elle couvre **uniquement** ce que contient ce dépôt : documentation, fichiers de configuration et
outils d'analyse. Elle ne s'étend à aucun élément du jeu.

Les dépendances externes (DXVK, Ultimate ASI Loader, RezExtract, DTX-Meta-Transfer…) restent soumises
à leurs licences respectives, à vérifier individuellement avant toute intégration ou redistribution.

## Avertissement

Ce projet **n'est affilié à aucun ayant droit et n'est approuvé par aucun d'eux**.

- Il ne contient **aucun asset, aucune ressource et aucun binaire du jeu**.
- Il ne distribue ni ne facilite le contournement d'aucune mesure de protection.
- **Une copie légitime du jeu est nécessaire** pour utiliser ces outils et cette documentation.
- « Global Operations » et les marques associées appartiennent à leurs détenteurs respectifs.
  Barking Dog Studios, Crave Entertainment et Electronic Arts sont cités à titre documentaire.

Le contenu de ce dépôt relève de l'analyse technique et de la préservation logicielle, à des fins
d'interopérabilité et d'usage personnel.
