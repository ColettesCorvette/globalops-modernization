# Installation reproductible

Procédure complète pour reconstruire une installation fonctionnelle depuis zéro.

## Sources requises

| Élément | Emplacement |
|---|---|
| Contenu du CD | `Global Operations/` (dossier `Setup/` = installeur InstallShield) |
| Exécutable sans SafeDisc | `Global Operations/Crack/globalops.exe` — build **1.16** |
| SDK officiel | `Global-Operations_Misc_Win_EN_Tools/gotools/` |
| Clé produit | `Global-Operations_Misc_Win_EN_CD-Key.txt` (non versionné) |

## Étapes

### 1. Installer le jeu — sans aucun patch

```
Global Operations/Setup/Setup.exe  →  cible : C:\Games\GlobalOps
```

**Ne pas appliquer les patchs 1.2 ou 2.0.** Ils font passer l'installation en build 1.27, incompatible
avec le seul exécutable non protégé disponible (1.16). C'est tout l'intérêt de la manœuvre.

Résultat attendu : `globalops.exe`, `Globalops/cshell.dll`, `Globalops/object.lto`, `server.dll` et les
`.rez` tous en build **1.16**.

### 2. Remplacer l'exécutable

```
Global Operations/Crack/globalops.exe  →  C:\Games\GlobalOps\globalops.exe
```

Build 1.16, donc ABI cohérente avec les DLL installées. Vérifier l'absence de SafeDisc :

```bash
python tools/pe.py "C:/Games/GlobalOps/globalops.exe"
```

Les sections doivent être `.text .rdata .data .exc .rsrc` — **sans** `stxt774` ni `stxt371`.

### 3. Installer DXVK

DXVK 3.1 ou supérieur, archive officielle, répertoire **`x32`** (le jeu est 32 bits) :

```
dxvk-<ver>/x32/d3d8.dll  →  C:\Games\GlobalOps\d3d8.dll
dxvk-<ver>/x32/d3d9.dll  →  C:\Games\GlobalOps\d3d9.dll
```

`d3d9.dll` est **obligatoire** : DXVK implémente D3D8 par-dessus son D3D9. Pour désactiver DXVK,
renommer ou supprimer les deux fichiers.

### 4. Déposer les configurations

Copier `config/dxvk.conf` et `config/autoexec.cfg` dans `C:\Games\GlobalOps\`.

### 5. Régler le profil

Jeu fermé, dans `C:\Games\GlobalOps\Globalops\profile\<nom>.cfg` :

```
"windowed" "0"
"ScreenWidth" "2560"
"ScreenHeight" "1440"
"bitdepth" "32"
"zbitdepth" "24"
"backbuffercount" "2"
```

Adapter la résolution à l'écran. **`bitdepth 32` n'est pas négociable.**

S'assurer que `autoexec.cfg` désigne bien ce profil : `"profilename" "<nom>"`.

## Vérification

```bash
cd "C:/Games/GlobalOps" && ./globalops.exe
```

Attendu : menu complet avec onglets Single Player / Multiplayer, dialogues fonctionnels, compteur FPS
DXVK en surimpression stabilisé à 60.

En cas d'échec, contrôler dans l'ordre :

1. `bitdepth` vaut bien 32 dans le profil **réellement chargé** (celui désigné par `autoexec.cfg`) ;
2. `C:\Games\GlobalOps\<exe>_d3d9.log` — cherche `Buffer size:` pour la résolution effective et les lignes `err:` ;
3. `C:\Games\GlobalOps\error.log` — vide signifie « aucune erreur moteur », pas « tout va bien » ;
4. versions de fichier homogènes (toutes en 1.16).

## Arguments de ligne de commande utiles

| Argument | Effet |
|---|---|
| `-skipmovies` | saute `bdogintro.bik`, `crave.bik`, `go.bik` |
| `-nosplash` | supprime l'écran de démarrage |
| `+runworld <chemin>` | charge un monde directement (chemin relatif aux ressources) |
| `-rez <dossier>` | ajoute un répertoire de ressources |
