# Climate Notebooks

Ce dépôt contient des notebooks climat et un package Python local pour reproduire des analyses/visualisations inspirées du workflow C3S Atlas.

## Contenu du projet

- `c3s_atlas/`: package Python (agrégation, interpolation, indices, unités, analyses, temporalité).
- `book/notebooks/`: notebooks principaux (cartes, séries temporelles, stripes, cycles annuels, etc.).
- `book/customizing/`: workflows personnalisés (Afrique/Maroc, scripts de génération de previews).
- `auxilier/`: fichiers auxiliaires (`settings.json`, `regions.json`).
- `data/`: données locales (non versionnées pour les gros formats).
- `environment.yml`: environnement Conda recommandé.
- `setup.py`: installation editable du package local.

## Installation

```bash
conda env create -f environment.yml
conda activate atlas-zarr
pip install -e .
```

## Lancer les notebooks

```bash
jupyter lab
```

Ouvrir ensuite les notebooks dans `book/notebooks/` ou `book/customizing/`.

## Notebook NetCDF -> Zarr

Le notebook `book/notebooks/netcdf_to_zarr.ipynb`:
- détecte automatiquement la racine du projet ;
- permet de cibler un sous-dossier de `data/` ;
- applique un chunking configurable (`time/lat/lon`) ;
- écrit un store Zarr `.zarr`.

Si le backend `zarr` n'est pas détecté dans le kernel, vérifier l'environnement (`xarray`, `zarr`, `numcodecs`, `dask`) puis redémarrer le kernel.

## Construire le Jupyter Book

```bash
pip install -r book/requirements.txt
jupyter-book build book
```

Sortie HTML: `book/_build/html/`

## Données et Git

Les gros fichiers de données sont exclus du versioning via `.gitignore` (ex: `.nc`, `.h5`, `.parquet`, `.geojson`).
Placer les datasets localement dans `data/` selon les besoins des notebooks.
