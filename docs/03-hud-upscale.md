# Chantier 1 — HUD et interface haute résolution

**Objectif :** un HUD et des menus lisibles en 2560×1440, sans flou.
**Dépend de :** [chantier 4 — pipeline d'assets](06-assets-pipeline.md).

## Ce qui est déjà établi

### Le placement suit déjà la résolution

Le jeu génère un fichier de layout **par résolution** dans `Globalops/profile/` :

```
bite_640x480.hud
bite_2560x1440.hud
```

Son contenu utilise des coordonnées **normalisées** entre 0.0 et 1.0 :

```
hud_health       0.392188   0.956250
hud_wallet       0.898438   0.900000
hud_ammo         0.004688   0.875000
hud_ammobar      0.006250   0.368750
hud_fireselect   0.843750   0.962500
hud_compass      0.814062   0.006250
```

Les éléments sont donc **correctement positionnés** quelle que soit la résolution. Ce n'est pas le problème.

`Globalops/hud.txt` définit le jeu d'éléments par défaut (`NUM_HUD_ELEMENTS 9`), également en coordonnées
normalisées. Ces deux fichiers sont éditables sans outil.

### Le problème est la taille, et il n'existe aucun réglage

Les éléments sont dessinés à leur dimension d'origine **en pixels**, pensée pour 640×480. En 1440p ils
occupent environ quatre fois moins de surface relative.

Recherche exhaustive des cvars dans `cshell.dll` : seules `HudAlpha` et `HudLayout` existent.
**Aucun facteur d'échelle.** Les symboles `Scale`, `ScaleX`, `ScaleY` trouvés dans le binaire sont
génériques (rendu d'objets) et ne s'appliquent pas au HUD.

## Le test décisif — à faire en premier

En LithTech, les quads du HUD dérivent fréquemment leur taille de celle de la **texture source**.
Si c'est le cas ici, tout le chantier se règle sans toucher au code.

**Protocole :**

1. extraire une texture HUD identifiable et isolée (l'icône de santé par exemple) ;
2. l'agrandir ×4 par simple mise à l'échelle — la qualité importe peu à ce stade ;
3. la replacer et lancer le jeu.

**Interprétation :**

| Observation | Conclusion | Suite |
|---|---|---|
| L'élément est 4× plus grand | la taille dérive de la texture | **voie A** — travail de contenu uniquement |
| L'élément garde sa taille, plus net | dimensions codées en dur | **voie B** — hook de rendu nécessaire |

Ne pas upscaler quoi que ce soit avant d'avoir tranché : la voie B changerait entièrement l'approche.

## Voie A — remplacement des textures

Le chemin souhaitable : aucun code, uniquement des assets.

1. extraire `interface.rez` (voir chantier 4) ;
2. upscaler les textures — un modèle IA convient bien pour de l'art 2002 basse résolution ;
3. **reporter les métadonnées DTX** avec `DTX-Meta-Transfer` : une texture upscalée qui perd ses
   métadonnées et ses mipmaps rend floue ou ne s'affiche pas. C'est la cause la plus fréquente d'échec ;
4. réintégrer.

### Polices

Point encore non élucidé : `cshell.dll` ne référence que `cursor.pcx`. Les polices bitmap n'ont pas
été localisées — elles sont probablement dans `interface.rez`, à identifier après extraction.
Une police bitmap upscalée demande en général d'ajuster aussi ses métriques (largeurs de glyphes).

## Voie B — hook de rendu

Si les dimensions sont codées en dur, il faut intercepter les appels de dessin du HUD et appliquer un
facteur d'échelle fonction de la résolution. Infrastructure commune avec les
[chantiers 2](04-raw-input.md) et [3](05-fps-physics.md) : Ultimate ASI Loader + plugin.

Plus lourd, mais avec un avantage réel : un facteur d'échelle continu, réglable par l'utilisateur,
plutôt qu'un jeu de textures figé.

## Critères de succès

- [ ] Test d'échelle effectué et voie tranchée
- [ ] HUD lisible à distance normale en 1440p
- [ ] Aucun élément flou, pixelisé ou mal découpé
- [ ] Texte des menus net
- [ ] Aucune régression en 1080p et en 4:3

## Risques

- **Métadonnées DTX perdues** → flou ou textures manquantes. Prévenu par `DTX-Meta-Transfer`.
- **Mipmaps** : DXT compressé avec chaîne de mipmaps ; les régénérer est indispensable.
- **Atlas de textures** : si plusieurs éléments partagent une même image, agrandir l'un décale les autres.
  À vérifier dès l'extraction.
- **Cohérence visuelle** : un HUD upscalé sur des textures de monde d'origine peut jurer. Prévoir
  l'ordre inverse (monde d'abord) si le résultat détonne.
