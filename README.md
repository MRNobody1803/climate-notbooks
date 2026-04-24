# Climate Notebooks

This repository contains Jupyter notebooks and reusable Python utilities to reproduce climate indicators and visual products inspired by the Copernicus C3S Atlas workflow.

It combines:
- A Python package (`c3s_atlas/`) with processing helpers (aggregation, interpolation, indices, temporal handling, units, analysis).
- A Jupyter Book project (`book/`) with notebooks for climate indices and visual products (maps, time series, stripes, annual cycles, customized regions).
- Auxiliary metadata (`auxilier/`) used by notebooks and regional analyses.

## Repository structure

- `c3s_atlas/`: Core Python functions and wrappers used by notebooks.
- `book/notebooks/`: Main reproducible notebooks.
- `book/customizing/`: Custom workflows/scripts for regional products.
- `auxilier/`: Settings and region metadata.
- `environment.yml`: Conda environment definition.
- `setup.py`: Editable installation of the local package.

## Setup

```bash
conda env create -f environment.yml
conda activate c3s-atlas
pip install -e .
```

## Run notebooks

```bash
jupyter lab
```

Then open notebooks from `book/notebooks/` or `book/customizing/`.

## Build the Jupyter Book

```bash
pip install -r book/requirements.txt
jupyter-book build book
```

Generated pages are written to `book/_build/html/`.

## Data files and Git policy

Large data files are intentionally excluded from version control through `.gitignore` (for example files under `**/data/` and large binary climate formats such as `.nc`, `.h5`, `.parquet`, `.geojson`).

If you run notebooks that require local datasets, place those files in the expected data folders (for example under `book/customizing/data/`) on your machine.

## Notes

- This project is designed for reproducible analysis workflows in Python/Jupyter.
- Some notebooks depend on external climate datasets that are not stored in the repository.
