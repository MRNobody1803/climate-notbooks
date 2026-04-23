import numpy as np
import os
import xarray as xr
import regionmask
from shapely.geometry import Polygon
from shapely.ops import unary_union
import geopandas as gpd
from .utils import c_path_c3s_atlas

class Mask:
    def __init__(self, ds: xr.Dataset):
        """
        Initialize the Mask object.

        Parameters:
            ds (xr.Dataset): Dataset containing the data.
        """
        self.ds=ds
    
    def polygon(self,region: np.array = np.array([])) -> np.ndarray:
        """
        Generates a mask for the user-defined region.

        Args:
            region (np.array, optional): User-defined region. Defaults to np.array([]).

        Returns:
            np.ndarray: Mask for the user-defined region.
        """
        # Define a polygon object (region_poly) based on the provided region definition
        region_poly = Polygon(region)
        
        # Extract longitude (lon) and latitude (lat) coordinates from the dataset (self.ds)
        lon = self.ds['lon'].values
        lat = self.ds['lat'].values
        
        # Create a list containing the user-defined polygon (user_regions_poly)
        user_regions_poly = [region_poly]
        
        # Create a mask for the user-defined region using regionmask.Regions
        mask_user = regionmask.Regions(user_regions_poly).mask(lon, lat)
        
        # Return the mask for the user-defined region (mask_user)
        mask_user = ~np.isnan(mask_user)
        return mask_user


    def regions_AR6(self, AR6_regions = ['']) -> np.ndarray:
        """
        Generates a mask for the AR6 region.

        Args:
            AR6_regions (arr, optional): AR6 regions. Defaults to [''].

        Returns:
            np.ndarray: Mask for the AR6 region.
        """
        # Extract longitude (lon) and latitude (lat) coordinates from the dataset (self.ds)
        lon = self.ds['lon'].values
        lat = self.ds['lat'].values
        
        # Define the target region (assuming AR6)
        regions_ar6_land = regionmask.defined_regions.ar6.all

        # Access the 'abbrevs' attribute correctly
        region_abbrevs = regions_ar6_land.abbrevs
        
        # Filter regions based on mask_data
        filtered_regions = regions_ar6_land[[region_abbrevs.index(abbrev) for abbrev in
                                             AR6_regions]]

        # Return the mask for AR6 regions (mask_AR6)
        mask_AR6 = filtered_regions.mask(lon, lat)

        # Convert the mask to a boolean array where True indicates the region and False
        # indicates NaN
        mask_AR6 = ~np.isnan(mask_AR6)

        return mask_AR6

        
    def regions_geojson(self,file_path:str = '', acronym = 'Acronym', 
                        geojson_regions = [''])->np.array:
        """
        This function generates a mask for a specified region based on a 
        GeoJSON file and abbreviation.
        
        Args:
          file_path (str, optional): Path to the GeoJSON file containing region data. Defaults to ''.
          acronym (str, optional): The name of the column containing region abbreviations in the GeoJSON file. Defaults to 'Acronym'.
          geojson_regions (list, optional): A list of region abbreviations to include in the mask. Defaults to [''].
        
        Returns:
          np.array: A boolean NumPy array representing the mask for the specified region.
        """
        # Read the GeoJSON file
        geojson_data = gpd.read_file(file_path)        
        # Filter the GeoDataFrame to get only rows with the abbreviations
        mask_data = geojson_data[geojson_data[acronym].isin(geojson_regions)]
        
        lon = self.ds['lon'].values
        lat = self.ds['lat'].values
        
        # Create the mask using latitude and longitude coordinates
        mask_geojson = regionmask.mask_geopandas(mask_data, lon, lat)
        mask_geojson = ~np.isnan(mask_geojson)
        return mask_geojson
        
    def European_contries(self,regions = [''])->np.array:
        """
          This function creates a mask for European countries based on provided abbreviations.
        
          Args:
              regions : A list of country abbreviations to include in the mask. Defaults to [''].
        
          Returns:
              np.array: A boolean NumPy array representing the mask for European countries.
          """
        # Read the GeoJSON file
        geojson_data = gpd.read_file(f"{c_path_c3s_atlas}/auxiliar/geojsons/european-countries_areas.geojson")
        
        # Filter the GeoDataFrame to get only rows with the abbreviations
        mask_data = geojson_data[geojson_data['Acronym'].isin(regions)]        
        # Get latitude and longitude coordinates from the data
        
        lon = self.ds['lon'].values
        lat = self.ds['lat'].values
        
        # Create the mask using latitude and longitude coordinates
        mask_geojson = regionmask.mask_geopandas(mask_data, lon, lat)
        mask_geojson = ~np.isnan(mask_geojson)
        return mask_geojson
        
    def EUCRA_contries(self,regions = [''])->np.array:
        """
        This function creates a mask for EUCRA countries based on provided abbreviations.

        Args:
          regions (list, optional): A list of country abbreviations to include in the mask.
          Defaults to [''] (empty list).

        Returns:
          np.array: A boolean NumPy array representing the mask for EUCRA countries.
        """
        # Read the GeoJSON file
        geojson_data = gpd.read_file(f"{c_path_c3s_atlas}/auxiliar/geojsons/EUCRA_areas.geojson")

        # Filter the GeoDataFrame to get only rows with the abbreviations
        mask_data = geojson_data[geojson_data['Acronym'].isin(regions)]
        # Get latitude and longitude coordinates from the data

        lon = self.ds['lon'].values
        lat = self.ds['lat'].values

        # Create the mask using latitude and longitude coordinates
        mask_geojson = regionmask.mask_geopandas(mask_data, lon, lat)
        mask_geojson = ~np.isnan(mask_geojson)

        return mask_geojson

    def African_countries(self, regions=['']) -> np.array:
        """
        This function creates a mask for African countries based on ISO 2-letter abbreviations.

        Args:
            regions (list, optional): A list of ISO 2-letter country codes to include in the mask.
                Examples: ['MA'] for Morocco, ['MA', 'DZ', 'TN'] for Maghreb.
                Defaults to [''].

        Returns:
            np.array: A boolean NumPy array representing the mask for the specified African countries.
        """
        geojson_data = gpd.read_file(f"{c_path_c3s_atlas}/auxiliar/geojsons/african-countries_areas.geojson")

        mask_data = geojson_data[geojson_data['Acronym'].isin(regions)]

        lon = self.ds['lon'].values
        lat = self.ds['lat'].values

        mask_geojson = regionmask.mask_geopandas(mask_data, lon, lat)
        mask_geojson = ~np.isnan(mask_geojson)

        return mask_geojson

    def Africa_continent(self, dissolve: bool = True) -> np.ndarray:
        """
        Create a mask for the African continent.

        The preferred source is Natural Earth through regionmask because the
        bundled GeoJSON is incomplete for some African countries and territories.
        If that lookup fails for any reason, the function falls back to the
        bundled GeoJSON.

        Parameters
        ----------
        dissolve : bool, optional
            If True, dissolve all African countries into a single geometry before masking.
            This is the most precise option for continent-wide masking. Defaults to True.

        Returns
        -------
        np.ndarray
            Boolean mask where True indicates grid cells inside Africa.
        """
        lon = self.ds["lon"].values
        lat = self.ds["lat"].values

        try:
            countries = regionmask.defined_regions.natural_earth_v5_0_0.countries_110
            african_ids = [
                "DZA", "AGO", "BEN", "BWA", "BFA", "BDI", "CMR", "CPV", "CAF", "TCD",
                "COM", "COD", "COG", "CIV", "DJI", "EGY", "GNQ", "ERI", "ETH", "GAB",
                "GMB", "GHA", "GIN", "GNB", "KEN", "LSO", "LBR", "LBY", "MDG", "MWI",
                "MLI", "MRT", "MUS", "MAR", "MOZ", "NAM", "NER", "NGA", "RWA", "STP",
                "SEN", "SLE", "SOM", "ZAF", "SSD", "SDN", "SWZ", "TZA", "TGO", "TUN",
                "UGA", "ZMB", "ZWE", "ESH",
            ]

            selected_polygons = [
                polygon
                for polygon, abbrev in zip(countries.polygons, countries.abbrevs)
                if abbrev in african_ids
            ]

            if not selected_polygons:
                raise ValueError("Natural Earth Africa selection returned no polygons.")

            if dissolve:
                africa_shape = unary_union(selected_polygons)
                africa_regions = regionmask.Regions(
                    [africa_shape],
                    names=["Africa"],
                    abbrevs=["AFR"],
                    name="Africa continent",
                )
                mask_africa = africa_regions.mask(lon, lat) == 0
            else:
                africa_regions = regionmask.Regions(
                    selected_polygons,
                    names=[f"Africa_{idx}" for idx in range(len(selected_polygons))],
                    abbrevs=[f"AF{idx}" for idx in range(len(selected_polygons))],
                    name="Africa countries",
                )
                mask_africa = africa_regions.mask(lon, lat)
                mask_africa = ~np.isnan(mask_africa)

        except Exception:
            geojson_data = gpd.read_file(
                f"{c_path_c3s_atlas}/auxiliar/geojsons/african-countries_areas.geojson"
            )

            if dissolve:
                africa_shape = unary_union(geojson_data.geometry)
                africa_regions = regionmask.Regions(
                    [africa_shape],
                    names=["Africa"],
                    abbrevs=["AFR"],
                    name="Africa continent",
                )
                mask_africa = africa_regions.mask(lon, lat) == 0
            else:
                mask_africa = regionmask.mask_geopandas(geojson_data, lon, lat)
                mask_africa = ~np.isnan(mask_africa)

        return mask_africa


def crop_to_bbox(
    data: xr.Dataset | xr.DataArray,
    lon_bounds: tuple[float, float] = (-18.0, 52.0),
    lat_bounds: tuple[float, float] = (-35.0, 37.5),
) -> xr.Dataset | xr.DataArray:
    """
    Crop a Dataset or DataArray to a lon/lat bounding box while preserving latitude order.

    Parameters
    ----------
    data : xr.Dataset or xr.DataArray
        Input data with ``lon`` and ``lat`` coordinates.
    lon_bounds : tuple[float, float], optional
        Longitude bounds as (west, east). Defaults to (-18.0, 52.0).
    lat_bounds : tuple[float, float], optional
        Latitude bounds as (south, north). Defaults to (-35.0, 37.5).

    Returns
    -------
    xr.Dataset or xr.DataArray
        Cropped data.
    """
    west, east = lon_bounds
    south, north = lat_bounds

    lat_values = data["lat"].values
    if lat_values[0] < lat_values[-1]:
        lat_slice = slice(south, north)
    else:
        lat_slice = slice(north, south)

    return data.sel(lon=slice(west, east), lat=lat_slice)


def mask_africa(
    data: xr.Dataset | xr.DataArray,
    crop: bool = True,
    lon_bounds: tuple[float, float] = (-18.0, 52.0),
    lat_bounds: tuple[float, float] = (-35.0, 37.5),
    dissolve: bool = True,
) -> xr.Dataset | xr.DataArray:
    """
    Precisely mask a Dataset or DataArray to the African continent.

    This uses the repository's bundled African countries GeoJSON and can optionally
    crop the result to an African bounding box after masking.

    Parameters
    ----------
    data : xr.Dataset or xr.DataArray
        Input data with ``lon`` and ``lat`` coordinates.
    crop : bool, optional
        If True, crop to the African bounding box after masking. Defaults to True.
    lon_bounds : tuple[float, float], optional
        Longitude bounds used for cropping. Defaults to (-18.0, 52.0).
    lat_bounds : tuple[float, float], optional
        Latitude bounds used for cropping. Defaults to (-35.0, 37.5).
    dissolve : bool, optional
        If True, dissolve country polygons into a continent geometry before masking.
        Defaults to True.

    Returns
    -------
    xr.Dataset or xr.DataArray
        Masked data containing only African grid cells.
    """
    mask = Mask(data).Africa_continent(dissolve=dissolve)
    masked = data.where(mask)

    if crop:
        masked = crop_to_bbox(
            masked,
            lon_bounds=lon_bounds,
            lat_bounds=lat_bounds,
        )

    masked.attrs = dict(masked.attrs)
    masked.attrs["mask_region"] = "Africa"
    masked.attrs["mask_source"] = "auxiliar/geojsons/african-countries_areas.geojson"

    return masked
