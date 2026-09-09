# Diagnostic — historique et fausses pistes

Ce document existe pour qu'aucune session future ne refasse le chemin. Les fausses pistes y figurent
autant que les conclusions : elles étaient plausibles, et c'est justement pour ça qu'elles ont coûté du temps.

## Chronologie

### 1. SafeDisc — le jeu ne démarre pas du tout

`globalops.exe` (build 1.27) porte les sections PE `stxt774` et `stxt371`, signature de **SafeDisc**.
Cette protection dépend du pilote noyau `secdrv.sys`, **retiré de Windows** depuis la version 10 v1607.

```
sc query secdrv
  STATE           : 1  STOPPED
  WIN32_EXIT_CODE : 1275  (0x4FB)   → ERROR_DRIVER_BLOCKED
```

`C:\Windows\System32\drivers\secdrv.sys` est absent. Le jeu ne démarrera jamais dans cette configuration.

**Fausse piste écartée :** appliquer le patch officiel 2.0 dans l'espoir qu'il retire la protection.
Il la conserve. Vérifié — l'installation patchée est en build 1.27 homogène et reste protégée.

**Piège méthodologique :** InstallShield **préserve les horodatages d'origine**. La date d'un fichier ne dit
rien du patch dont il provient. Toujours se fier aux versions de fichier :

```powershell
(Get-Item x).VersionInfo.FileVersion
```

### 2. `bitdepth 16` — la cause n°1, sous deux déguisements

Le profil par défaut demande **640×480 en 16 bits**. Les pilotes modernes n'exposent plus de mode 16 bits.

| Contexte | Symptôme observé | Interprétation trompeuse |
|---|---|---|
| Sans wrapper | sortie **propre** : `ExitCode 0`, `error.log` vide | « Échap ferme le jeu » |
| Avec DXVK | crash `0xC0000005` | « DXVK est incompatible » |

Dans le premier cas, l'absence totale de message est ce qui égare : le moteur échoue à créer son device
Direct3D 8 et se termine normalement, en sauvegardant même son profil.

**Le faux lien de causalité :** la vidéo d'intro passe par DirectDraw/Smacker, **sans aucun rapport avec D3D8**.
Elle s'affiche donc toujours. Quand on l'interrompt, le jeu enchaîne sur le menu et tente enfin de créer son
device — d'où l'illusion que la touche Échap ferme le jeu.

**Correctif :** `bitdepth 32`, `zbitdepth 24`.

### 3. Lignes verticales grises — le shell de développement

`dev.exe` du SDK est le même moteur que `globalops.exe` **sans SafeDisc** (table d'imports identique,
`.text` de taille comparable, pas de sections SafeDisc). Il démarre et affiche un menu.

Mais il ne peut charger que `dev.dll` / `dev.lto`, c'est-à-dire le **shell de développement** :
pas de dialogues (« New Profile » n'ouvre rien), pas de rendu de la scène du jeu. Le fond noir strié de
fines lignes verticales régulières est simplement **un backbuffer sur lequel rien n'est dessiné**.

**Fausse piste écartée :** supposer un écart de format des mondes entre builds. Infirmé — un monde 1.26
compilé par le SDK, chargé par le moteur 1.26, donne exactement le même résultat.

### 4. Rupture d'ABI 1.26 / 1.27

Monter `cshell.dll` / `object.lto` (1.27) sous les noms `dev.dll` / `dev.lto` sur `dev.exe` (1.26) :

```
Invalid shell DLL version for dev.dll.  DLL version is 2, current version is 1.
```

L'interface du client shell est passée de la version 1 à la version 2. Et quand le moteur ne vérifie pas
(exécutable 1.16 avec DLL 1.27), il crashe en `0xC0000005`.

**Conclusion :** les builds ne se mélangent pas. Un ensemble homogène est obligatoire.

### 5. Physique cadencée sur le framerate

**Symptôme :** le joueur reste coincé dans les murs sans pouvoir se dégager.

Sur un GPU moderne, la boucle tourne à un débit tel que la détection de collision travaille sur des pas de
temps trop petits : le joueur traverse la géométrie puis s'y encastre.

**Indice historique corroborant :** le patch 2.0 officiel ajoute une « prévention des speed hacks côté
serveur ». Si accélérer était possible, c'est bien que la simulation suivait les FPS.

**Contre-indice pour l'hypothèse « bug corrigé par un patch » :** aucune note de patch (1.1 / 1.2 / 2.0)
ne mentionne de correctif de collision.

**Correctif confirmé :** plafond à 60 FPS. Problème disparu.

## Pièges méthodologiques rencontrés

- **Deux profils, deux vérités.** `autoexec.cfg` désigne le profil actif (`"profilename" "<nom>"`).
  Vide ou absent → le jeu utilise `Player` et recrée `Player.cfg` avec les défauts 640×480×16.
  Éditer le mauvais `.cfg` produit des tests ininterprétables : le log DXVK affichait 640×480 alors que
  le fichier modifié disait 1920×1080.
- **Le jeu réécrit ses `.cfg` à chaque sortie propre.** Ne les éditer que jeu fermé.
- **Les logs ne sont vidés qu'à la sortie propre.** Un `Stop-Process -Force` laisse un fichier de 0 octet.
- **Ne pas empiler les correctifs avant d'avoir isolé la cause.** DXVK a été installé alors que la cause
  réelle (`bitdepth 16`) n'était pas identifiée, ce qui a brouillé plusieurs essais.
- **Changer une variable à la fois.** Résolution et profondeur de couleur modifiées ensemble ont rendu
  un test non concluant.
