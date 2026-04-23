from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import xarray as xr


@dataclass(frozen=True)
class PreviewConfig:
    dataset_path: Path
    variable: str
    cmap: str
    output_name: str
    qmin: float = 0.02
    qmax: float = 0.98


REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = REPO_ROOT / "book" / "customizing" / "data" / "africa_visualization" / "maps"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


CONFIGS = [
    PreviewConfig(
        dataset_path=REPO_ROOT / "book" / "customizing" / "data" / "africa_era5" / "era5_africa_masked.nc",
        variable="t",
        cmap="coolwarm",
        output_name="era5_africa_temperature_preview.png",
    ),
    PreviewConfig(
        dataset_path=REPO_ROOT / "book" / "customizing" / "data" / "africa_era5_precip" / "era5_africa_precip_masked.nc",
        variable="r",
        cmap="YlGnBu",
        output_name="era5_africa_precipitation_preview.png",
    ),
    PreviewConfig(
        dataset_path=REPO_ROOT / "book" / "customizing" / "data" / "africa_era5_evap" / "era5_africa_evap_masked.nc",
        variable="evspsbl",
        cmap="viridis",
        output_name="era5_africa_evaporation_preview.png",
    ),
    PreviewConfig(
        dataset_path=REPO_ROOT / "book" / "customizing" / "data" / "africa_era5_drought" / "era5_africa_drought_masked.nc",
        variable="spei6",
        cmap="RdYlBu",
        output_name="era5_africa_drought_preview.png",
    ),
]


def get_plot_data(ds: xr.Dataset, variable: str) -> xr.DataArray:
    da = ds[variable]
    time_dim = next((dim for dim in ("time", "valid_time") if dim in da.dims), None)
    if time_dim:
        da = da.mean(time_dim, skipna=True)
    return da


def compute_limits(da: xr.DataArray, qmin: float, qmax: float) -> tuple[float, float]:
    values = da.where(da.notnull(), drop=True)
    vmin = float(values.quantile(qmin))
    vmax = float(values.quantile(qmax))
    if vmin == vmax:
        vmin = float(values.min())
        vmax = float(values.max())
    return vmin, vmax


def save_catalog_preview(config: PreviewConfig) -> Path:
    ds = xr.open_dataset(config.dataset_path)
    try:
        da = get_plot_data(ds, config.variable)
        vmin, vmax = compute_limits(da, config.qmin, config.qmax)

        fig, ax = plt.subplots(figsize=(5.2, 5.2), dpi=160)
        da.plot.imshow(
            ax=ax,
            cmap=config.cmap,
            vmin=vmin,
            vmax=vmax,
            add_colorbar=False,
            interpolation="nearest",
        )
        ax.set_axis_off()
        ax.set_aspect("equal")
        fig.patch.set_alpha(0)
        ax.set_facecolor((1, 1, 1, 0))
        fig.tight_layout(pad=0)

        output_path = OUTPUT_DIR / config.output_name
        fig.savefig(output_path, transparent=True, bbox_inches="tight", pad_inches=0)
        plt.close(fig)
        return output_path
    finally:
        ds.close()


def main() -> None:
    print("Generating Africa dataset previews...")
    for config in CONFIGS:
        output_path = save_catalog_preview(config)
        print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
