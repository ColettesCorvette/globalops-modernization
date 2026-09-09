Quatre bonnes questions. Je vérifie ce qui existe localement avant de répondre.

Découverte importante pour ton point 1 : le jeu a généré `bite_2560x1440.hud`, avec des coordonnées **normalisées** (0.0–1.0). Les positions s'adaptent donc déjà. Ce qui ne s'adapte pas, c'est la **taille** des textures et polices, rendues à leur dimension d'origine prévue pour 640×480. Je cherche s'il existe un facteur d'échelle :

Résultat net : **aucune cvar d'échelle du HUD**. Seulement `HudAlpha` et `HudLayout`. Je vérifie le dernier point, l'injection de code :

Réponses dans l'ordre, avec ce que j'ai vérifié.

## 1. HUD — bonne et mauvaise nouvelle

Le fichier `bite_2560x1440.hud` utilise des coordonnées **normalisées** :

```
hud_health      0.392188   0.956250
hud_ammo        0.004688   0.875000
```

Le **placement** suit donc déjà la résolution. C'est la **taille** qui ne suit pas : les éléments sont dessinés à leur dimension d'origine en pixels, pensée pour 640×480. En 1440p, ils occupent quatre fois moins de surface relative.

Et il n'existe **aucune cvar d'échelle** — `cshell.dll` n'expose que `HudAlpha` et `HudLayout`.

Deux voies, et un test simple les départage. En LithTech, les quads du HUD dérivent souvent leur taille de celle de la texture source — c'est précisément le principe des tutoriels d'upscale. Si c'est le cas ici, remplacer une texture 32×32 par une 128×128 agrandit l'élément, sans toucher au code. Sinon, il faudra hooker le rendu.

**Test décisif** : extraire une texture HUD, l'agrandir ×4, la remettre, regarder. Une demi-heure, et ça détermine toute la stratégie. À faire avant d'upscaler quoi que ce soit.

## 2. DirectInput 8 — pas de fix tout prêt

Global Operations est trop confidentiel pour avoir son correctif dédié. Mais le socle d'injection existe et est mature : **[Ultimate ASI Loader](https://github.com/ThirteenAG/Ultimate-ASI-Loader)** (ThirteenAG, v9.7.x). C'est une DLL proxy qu'on pose sous le nom d'une DLL système et qui charge des plugins `.asi`.

Point d'attention : DXVK occupe déjà `d3d8.dll` et `d3d9.dll`. On utilisera donc `dinput8.dll` ou `winmm.dll` — aucun conflit, les deux sont importés par le jeu.

Le plugin raw input, en revanche, il faudra l'écrire : intercepter `IDirectInputDevice8::GetDeviceData` et le réalimenter depuis `WM_INPUT`. C'est du code sur mesure, pas un téléchargement.

## 3. Ton analogie Fallout 4 est juste, avec une nuance

Le High FPS Physics Fix borne le pas de temps de la physique tout en laissant le rendu libre. Même principe ici. La nuance : chez Bethesda la physique est un module séparé (Havok), facile à isoler. Dans LithTech Talon, simulation et boucle principale sont plus intriquées — un découplage complet sera plus délicat.

Mais on a un point d'entrée solide : **`MaxFPS` existe déjà** comme cvar, donc le code de timing est identifiable. `WINMM.dll` est importé, ce qui pointe vers `timeGetTime`. Dans Ghidra, on remonte de là au calcul du delta et on le clampe. Un clamp bien placé, c'est déjà l'essentiel du gain — tu joueras à 144 FPS avec une physique cadencée à 60.

Avantage décisif : `globalops.exe` en 1.16 n'est **pas protégé**, donc entièrement analysable.

## 4. Non, on ne charge pas un `.rez` dans goedit

`goedit` veut un projet en fichiers libres (`Textures/`, `Prefabs/`, `Worlds/` avec leurs marqueurs `DirType*`). Il faut extraire d'abord :

- **[RezExtract](https://github.com/no-lith/RezExtract)** — gère plusieurs générations LithTech et convertit les DTX à l'extraction ;
- **[DTX-Meta-Transfer](https://github.com/AkvenJan/DTX-Meta-Transfer)** — reporte les métadonnées DTX d'un fichier à l'autre, écrit **spécifiquement pour du travail d'upscale**. C'est lui qui évitera ton problème de flou : une texture upscalée sans ses métadonnées et ses mipmaps rend mal.

Et il existe un tutoriel ModDB « Upscaling LithTech 2.X Engine games » — Talon **est** du LithTech 2.x, donc directement applicable (le site m'a renvoyé un 403, mais il est accessible depuis un navigateur).

Une question à trancher tôt, qui peut t'épargner beaucoup de travail : LithTech charge généralement les fichiers libres **avant** ceux des archives. Si c'est vrai ici, tu poses tes textures modifiées dans l'arborescence et tu ne repackes jamais. `resource.txt` liste les `.rez` chargés — c'est testable en dix minutes.

## Par où commencer

Le point 4 conditionne le point 1 : sans extraction, pas de test HUD. Je propose donc l'ordre : outillage d'extraction → test d'échelle du HUD → puis l'injection (points 2 et 3 ensemble, même mécanisme).

Je récupère **RezExtract** et **Ultimate ASI Loader** depuis leurs dépôts GitHub ? Ce sont deux petits téléchargements, et ils débloquent les quatre chantiers.