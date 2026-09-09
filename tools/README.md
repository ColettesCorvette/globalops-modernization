# Outils d'analyse binaire

## `pe.py`
En-têtes PE : architecture, drapeaux, **table des sections**.

```bash
python tools/pe.py "F:/Games/GO116/globalops.exe"
```

Sert principalement à détecter SafeDisc : la présence des sections `stxt774` et `stxt371` signale un
exécutable protégé, inutilisable sur Windows 10+.

## `imp.py`
Table d'imports réelle (et non les chaînes du binaire, trompeuses).

```bash
python tools/imp.py "F:/Games/GO116/globalops.exe"
```

A servi à établir que `dev.exe` et `globalops.exe` sont le même moteur, et que `cshell.dll` / `cres.dll` /
`sres.dll` sont chargés dynamiquement — donc absents de cette table.

## Extraction de chaînes

`strings` n'est pas installé. Équivalent :

```bash
tr -c '[:print:]' '\n' < fichier.exe | grep -aiE 'motif' | sort -u
```

Inopérant sur un binaire protégé (code chiffré) : utiliser les binaires non protégés.
