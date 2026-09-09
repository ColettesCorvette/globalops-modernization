# Chantier 4 — Pipeline d'assets

**Objectif :** extraire, modifier et réintégrer les ressources du jeu.
**Dépend de :** rien. **Débloque :** le [chantier 1](03-hud-upscale.md).

C'est le premier chantier à traiter : coût faible, et sans lui rien de visuel n'est possible.

## Réponse à une question fréquente

**On ne charge pas un `.rez` dans `goedit`.** L'éditeur travaille sur un projet en fichiers libres —
`Textures/`, `Prefabs/`, `Worlds/` — identifiés par des fichiers-marqueurs vides `DirTypeProject`,
`DIRTYPEWORLDS`, `DIRTYPEPREFABS`. Les `.rez` sont des archives : il faut les extraire d'abord.

## Les archives

```
F:\Games\GO116\
  globalops.rez    ~490 Mo   contenu principal
  interface.rez    ~3 Mo     menus, HUD, polices    ← cible du chantier 1
  models.rez       ~1,3 Mo
  worlds.rez       ~16 Mo    mondes compilés (.dat)
  Engine.REZ       33 Ko
```

`resource.txt` liste les archives chargées :

```
interface.rez
models.rez
worlds.rez
```

## Outillage

| Outil | Usage | Source |
|---|---|---|
| **RezExtract** | extraction `.rez`, plusieurs générations LithTech, conversion DTX optionnelle | [github.com/no-lith/RezExtract](https://github.com/no-lith/RezExtract) |
| **DTX-Meta-Transfer** | report des métadonnées DTX d'un fichier vers un autre — **écrit pour l'upscale** | [github.com/AkvenJan/DTX-Meta-Transfer](https://github.com/AkvenJan/DTX-Meta-Transfer) |
| WinRez LT Studio | alternative d'extraction | outil communautaire historique |

Un tutoriel ModDB « Upscaling LithTech 2.X Engine games » couvre exactement cette génération de moteur —
Talon **est** du LithTech 2.x. À consulter avant de commencer (le site refuse les requêtes automatisées ;
y accéder depuis un navigateur).

## Question à trancher en priorité

**Les fichiers libres priment-ils sur les archives ?**

LithTech charge généralement un fichier présent sur disque avant son homologue dans un `.rez`.
Si c'est vrai ici, **aucun repackaging n'est jamais nécessaire** : on dépose les fichiers modifiés
dans l'arborescence et le moteur les prend. Gain de temps considérable sur tout le projet.

**Protocole :** extraire une texture identifiable, la modifier de façon flagrante (teinte vive),
la reposer dans l'arborescence sans toucher au `.rez`, lancer le jeu.

- **Modification visible** → travailler en fichiers libres, définitivement.
- **Pas de changement** → tester `-rez <dossier>` en ligne de commande, puis le repackaging.

## Formats

| Extension | Contenu | Notes |
|---|---|---|
| `.dtx` | texture | DXT compressé, mipmaps + métadonnées — **fragile à l'upscale** |
| `.abc` | modèle / animation | |
| `.dat` | monde compilé | produit par `goprocess` depuis un `.ed` |
| `.ed` | monde source | éditable dans `goedit` |
| `.rez` | archive | « LithTech Resource File » |

## Méthode

1. installer RezExtract et DTX-Meta-Transfer ;
2. extraire `interface.rez` dans un dossier de travail hors dépôt ;
3. inventorier : textures HUD, éléments de menu, polices, atlas éventuels ;
4. trancher la question des fichiers libres (ci-dessus) ;
5. exécuter le test d'échelle du [chantier 1](03-hud-upscale.md) ;
6. seulement ensuite, upscaler en volume.

## Critères de succès

- [ ] `interface.rez` extrait et inventorié
- [ ] Polices bitmap localisées
- [ ] Question des fichiers libres tranchée
- [ ] Aller-retour complet validé sur une texture (extraction → modification → visible en jeu)
- [ ] Métadonnées DTX préservées sur cet aller-retour

## Risques

- **Version de DTX** : DTX v1, v1.5 et v2 coexistent selon les jeux LithTech ; les outils n'ont pas le
  même support (DTX-Meta-Transfer lit v1.5 mais n'écrit qu'en v1 et v2). Identifier la version employée
  par Global Operations avant tout traitement de masse.
- **Atlas partagés** : plusieurs éléments dans une même image ; modifier les dimensions décale les autres.
- **Volume** : `globalops.rez` fait 490 Mo. Extraire hors du dépôt — le `.gitignore` exclut déjà ces formats.
- **Sauvegarde** : conserver les `.rez` d'origine intacts avant toute manipulation.
