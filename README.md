# Circular Product Redesign

Un skill pour Claude qui guide la reconception circulaire d'un produit physique, étape par étape.

Il s'appuie sur trois couches liées :

- **une feuille de route en 7 étapes (0 à 6)** qui ordonne le travail : du diagnostic du produit existant jusqu'à l'évaluation de la reconception ;
- **six axes de stratégie** qui orientent ce qu'il faut concevoir : *Narrow, Slow (long life), Slow (life extension), Close, Regenerate, Inform* ;
- **une hiérarchie de rétention de valeur** appliquée à chaque composant : *Maintain → Repair → Reuse → Refurbish → Remanufacture → Recycle*.

Le skill produit un diagnostic de départ, plusieurs concepts distincts, une comparaison chiffrée, des illustrations, et, si vous le demandez, un brief CAO et un fichier STEP conceptuel vérifié.

## Installation

### Avec Claude Code

Clonez le dépôt dans votre dossier de skills personnels :

```bash
git clone https://github.com/ielhassani/circular-product-redesign.git ~/.claude/skills/circular-product-redesign
```

Sous Windows (PowerShell) :

```powershell
git clone https://github.com/ielhassani/circular-product-redesign.git "$HOME\.claude\skills\circular-product-redesign"
```

Pour l'utiliser dans un seul projet, clonez-le plutôt dans `.claude/skills/circular-product-redesign` à la racine de ce projet.

Redémarrez ensuite Claude Code.

### Avec Claude (application web ou bureau)

1. Cliquez sur **Code → Download ZIP** en haut de cette page.
2. Dans Claude, ouvrez les paramètres, puis la section des **Skills**, et importez le fichier ZIP.
3. Activez le skill.

Le dossier contenu dans le ZIP doit contenir directement le fichier `SKILL.md`.

## Utilisation

Décrivez simplement le produit à reconcevoir. Par exemple :

> Utilise le skill circular-product-redesign pour reconcevoir cette bouilloire électrique. Voici une photo et ce que je sais de ses matériaux.

Dans Claude Code, vous pouvez aussi taper `/circular-product-redesign`.

Conseils :

- Donnez le plus d'informations possible : photos, matériaux, dimensions, usage, fin de vie actuelle. Le skill distingue toujours ce qui est observé, calculé, supposé ou inconnu.
- Précisez jusqu'où aller. Sans précision, le skill fait une reconception complète (concepts, comparaison, illustrations, CAO). Vous pouvez demander seulement le diagnostic ou seulement les concepts.
- Pour un produit nouveau, indiquez le service de référence auquel le comparer.

## Contenu du dépôt

| Fichier ou dossier | Rôle |
|---|---|
| `SKILL.md` | Instructions principales du skill |
| `references/` | Méthode détaillée : feuille de route, évaluation, données de comparaison, CAO, livrables, sources |
| `scripts/calculate_scores.py` | Score de conception complémentaire pour comparer deux options |
| `scripts/compare_concepts.py` | Le même score pour plusieurs concepts |
| `scripts/verify_step.py` | Vérification d'un fichier STEP par aller-retour |
| `agents/openai.yaml` | Configuration pour une utilisation avec Codex d'OpenAI |

## Prérequis

- **Python 3** pour les scripts de score. Ils n'utilisent que la bibliothèque standard.
- **CadQuery** (`pip install cadquery`), seulement pour vérifier des fichiers STEP avec `verify_step.py`.

## Limites à garder en tête

- Les scores calculés par les scripts sont des indicateurs de conception complémentaires. Ce ne sont ni un pourcentage de circularité, ni un indicateur MCI, ni un résultat ISO.
- Les illustrations et les modèles CAO sont **conceptuels**. Ils ne prouvent ni la sécurité, ni la conformité, ni la faisabilité industrielle.
- Vérifiez toujours les normes, réglementations et filières de recyclage actuelles auprès de sources primaires.
