# Chantier 3 — Découpler physique et rendu

**Objectif :** jouer à 144 FPS avec une simulation cadencée à 60, sans traverser les murs.
**Dépend de :** Ultimate ASI Loader (socle partagé avec le [chantier 2](04-raw-input.md)).
**État actuel :** contourné par un plafond global à 60 FPS — un pansement, pas un correctif.

## Le problème

La physique de LithTech est cadencée sur le framerate. Sans plafond, la détection de collision travaille
sur des pas de temps trop petits : le joueur traverse la géométrie puis s'y encastre définitivement.

Confirmé empiriquement : plafond à 60 → problème disparu.

**Indice historique :** le patch officiel 2.0 ajoute une « prévention des speed hacks côté serveur ».
Si accélérer artificiellement était possible, c'est bien que la simulation suivait les FPS.

**Ce que coûte le contournement actuel :** 60 FPS sur un écran capable de bien plus, sur un jeu qui
tournerait à plusieurs centaines d'images par seconde.

## Précédent : Fallout 4

Le *High FPS Physics Fix* borne le pas de temps de la physique tout en laissant le rendu libre.
Même principe visé ici, avec une différence importante :

| | Fallout 4 | LithTech Talon |
|---|---|---|
| Physique | module séparé (Havok) | intriquée dans la boucle principale |
| Point d'accroche | net et documenté | à localiser |
| Difficulté | moyenne | plus élevée |

Le découplage complet sera donc plus délicat. Mais **borner le delta time est déjà l'essentiel du gain**.

## Points d'entrée identifiés

Cvars présentes dans les binaires :

```
globalops.exe : MaxFPS, MaxFrameRate, UpdateRate, ModelLODOffset
server.dll    : MaxFPS, UpdateRate
cshell.dll    : FrameRate
object.lto    : FrameRate
```

Deux atouts :

- **`MaxFPS` existe déjà** — il y a donc un limiteur interne, et son code manipule forcément le timing.
  C'est le meilleur point de départ dans Ghidra.
- **`WINMM.dll` est importé** → `timeGetTime` est très probablement la source d'horloge.
  Chercher aussi `QueryPerformanceCounter` dans `KERNEL32`.

DXVK confirme l'existence du limiteur interne :

```
warn: Built-in frame rate limiter enabled.
```

## Méthode

1. **Localiser l'horloge.** Dans Ghidra sur `globalops.exe`, référencer les appels à `timeGetTime` /
   `QueryPerformanceCounter`, identifier la soustraction produisant le delta d'une image à l'autre.
2. **Confirmer par `MaxFPS`.** Retrouver le code du limiteur et vérifier qu'il agit sur la même variable.
   Deux chemins convergents = bonne cible.
3. **Distinguer les deux consommateurs.** Le delta sert à la fois au rendu (interpolation, animations)
   et à la simulation (collision, mouvement). Le but est de borner **le second seulement**.
4. **Clamper.** Forcer le delta de simulation à un maximum (1/60 s), en accumulant le reste. Si la boucle
   ne permet pas la séparation, un clamp global reste préférable au plafond FPS actuel.
5. **Valider par paliers.** 100, 120, 144 — en cherchant activement à se coincer dans les murs.

## Étape intermédiaire, sans code

Avant tout travail de rétro-ingénierie, **déterminer le seuil réel** : monter `MaxFPS` et
`dxvk.maxFrameRate` par paliers (100, 120, 144) et noter où le bug réapparaît. Le résultat oriente
le chantier — si la physique tient à 120, l'urgence est moindre et l'effort peut aller ailleurs.

**Modifier les deux valeurs ensemble** : `autoexec.cfg` bride la boucle du moteur, `dxvk.conf` la présentation.

## Critères de succès

- [ ] Seuil de rupture connu (jalon préalable)
- [ ] Rendu à 144 FPS, simulation stable
- [ ] Aucun blocage dans les murs, y compris en se collant volontairement aux angles
- [ ] Vitesse de déplacement identique quel que soit le framerate (pas de speed hack involontaire)
- [ ] Animations et son non altérés

## Risques

- **Boucle non séparable** : si simulation et rendu sont indissociables, le gain se limitera à un clamp
  global. Résultat honorable malgré tout.
- **Vitesse de déplacement dépendante du delta** : un clamp mal placé rend le joueur plus lent ou plus
  rapide. À tester chronomètre en main sur une distance fixe.
- **Réseau** : `UpdateRate` (30) touche la synchronisation. Ne pas y toucher sans tester le multijoueur.
- **Effet de bord sur les animations** : elles peuvent partager la même horloge.
