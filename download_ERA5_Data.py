from dataclasses import dataclass, field
from urllib import request
import geopandas as gpd
import xarray as xr
import pandas as pd
import numpy as np
import rioxarray
import datetime
import cdsapi
import shutil
import uuid
import yaml
import time
import json
import sys
import os

Available_Variables = {
    'reanalysis-era5-single-levels-timeseries': [
        "100m_u_component_of_wind",
        "100m_v_component_of_wind",
        "10m_u_component_of_wind",
        "10m_v_component_of_wind",
        "10m_wind_gust_since_previous_post_processing",
        "2m_dewpoint_temperature",
        "2m_temperature",
        "boundary_layer_height",
        "cloud_base_height",
        "mean_sea_level_pressure",
        "mean_wave_direction",
        "mean_wave_period",
        "sea_surface_temperature",
        "significant_height_of_combined_wind_waves_and_swell",
        "skin_temperature",
        "surface_latent_heat_flux",
        "surface_pressure",
        "surface_sensible_heat_flux",
        "surface_solar_radiation_downwards",
        "surface_thermal_radiation_downwards",
        "total_cloud_cover",
        "total_precipitation",
        "total_sky_direct_solar_radiation_at_surface"],
    'reanalysis-era5-single-levels':[
        "10m_u_component_of_wind",
        "10m_v_component_of_wind",
        "2m_dewpoint_temperature",
        "2m_temperature",
        "mean_sea_level_pressure",
        "mean_wave_direction",
        "mean_wave_period",
        "sea_surface_temperature",
        "significant_height_of_combined_wind_waves_and_swell",
        "surface_pressure",
        "total_precipitation",
        "ice_temperature_layer_1",
        "ice_temperature_layer_2",
        "ice_temperature_layer_3",
        "ice_temperature_layer_4",
        "maximum_2m_temperature_since_previous_post_processing",
        "minimum_2m_temperature_since_previous_post_processing",
        "skin_temperature",
        "100m_u_component_of_wind",
        "100m_v_component_of_wind",
        "10m_u_component_of_neutral_wind",
        "10m_v_component_of_neutral_wind",
        "10m_wind_gust_since_previous_post_processing",
        "instantaneous_10m_wind_gust",
        "mean_boundary_layer_dissipation",
        "mean_convective_precipitation_rate",
        "mean_convective_snowfall_rate",
        "mean_eastward_gravity_wave_surface_stress",
        "mean_eastward_turbulent_surface_stress",
        "mean_evaporation_rate",
        "mean_gravity_wave_dissipation",
        "mean_large_scale_precipitation_fraction",
        "mean_large_scale_precipitation_rate",
        "mean_large_scale_snowfall_rate",
        "mean_northward_gravity_wave_surface_stress",
        "mean_northward_turbulent_surface_stress",
        "mean_potential_evaporation_rate",
        "mean_runoff_rate",
        "mean_snow_evaporation_rate",
        "mean_snowfall_rate",
        "mean_snowmelt_rate",
        "mean_sub_surface_runoff_rate",
        "mean_surface_direct_short_wave_radiation_flux",
        "mean_surface_direct_short_wave_radiation_flux_clear_sky",
        "mean_surface_downward_long_wave_radiation_flux",
        "mean_surface_downward_long_wave_radiation_flux_clear_sky",
        "mean_surface_downward_short_wave_radiation_flux",
        "mean_surface_downward_short_wave_radiation_flux_clear_sky",
        "mean_surface_downward_uv_radiation_flux",
        "mean_surface_latent_heat_flux",
        "mean_surface_net_long_wave_radiation_flux",
        "mean_surface_net_long_wave_radiation_flux_clear_sky",
        "mean_surface_net_short_wave_radiation_flux",
        "mean_surface_net_short_wave_radiation_flux_clear_sky",
        "mean_surface_runoff_rate",
        "mean_surface_sensible_heat_flux",
        "mean_top_downward_short_wave_radiation_flux",
        "mean_top_net_long_wave_radiation_flux",
        "mean_top_net_long_wave_radiation_flux_clear_sky",
        "mean_top_net_short_wave_radiation_flux",
        "mean_top_net_short_wave_radiation_flux_clear_sky",
        "mean_total_precipitation_rate",
        "mean_vertically_integrated_moisture_divergence",
        "clear_sky_direct_solar_radiation_at_surface",
        "downward_uv_radiation_at_the_surface",
        "forecast_logarithm_of_surface_roughness_for_heat",
        "instantaneous_surface_sensible_heat_flux",
        "near_ir_albedo_for_diffuse_radiation",
        "near_ir_albedo_for_direct_radiation",
        "surface_latent_heat_flux",
        "surface_net_solar_radiation",
        "surface_net_solar_radiation_clear_sky",
        "surface_net_thermal_radiation",
        "surface_net_thermal_radiation_clear_sky",
        "surface_sensible_heat_flux",
        "surface_solar_radiation_downward_clear_sky",
        "surface_solar_radiation_downwards",
        "surface_thermal_radiation_downward_clear_sky",
        "surface_thermal_radiation_downwards",
        "toa_incident_solar_radiation",
        "top_net_solar_radiation",
        "top_net_solar_radiation_clear_sky",
        "top_net_thermal_radiation",
        "top_net_thermal_radiation_clear_sky",
        "total_sky_direct_solar_radiation_at_surface",
        "uv_visible_albedo_for_diffuse_radiation",
        "uv_visible_albedo_for_direct_radiation",
        "cloud_base_height",
        "high_cloud_cover",
        "low_cloud_cover",
        "medium_cloud_cover",
        "total_cloud_cover",
        "total_column_cloud_ice_water",
        "total_column_cloud_liquid_water",
        "vertical_integral_of_divergence_of_cloud_frozen_water_flux",
        "vertical_integral_of_divergence_of_cloud_liquid_water_flux",
        "vertical_integral_of_eastward_cloud_frozen_water_flux",
        "vertical_integral_of_eastward_cloud_liquid_water_flux",
        "vertical_integral_of_northward_cloud_frozen_water_flux",
        "vertical_integral_of_northward_cloud_liquid_water_flux",
        "lake_bottom_temperature",
        "lake_cover",
        "lake_depth",
        "lake_ice_depth",
        "lake_ice_temperature",
        "lake_mix_layer_depth",
        "lake_mix_layer_temperature",
        "lake_shape_factor",
        "lake_total_layer_temperature",
        "evaporation",
        "potential_evaporation",
        "runoff",
        "sub_surface_runoff",
        "surface_runoff",
        "convective_precipitation",
        "convective_rain_rate",
        "instantaneous_large_scale_surface_precipitation_fraction",
        "large_scale_rain_rate",
        "large_scale_precipitation",
        "large_scale_precipitation_fraction",
        "maximum_total_precipitation_rate_since_previous_post_processing",
        "minimum_total_precipitation_rate_since_previous_post_processing",
        "precipitation_type",
        "total_column_rain_water",
        "convective_snowfall",
        "convective_snowfall_rate_water_equivalent",
        "large_scale_snowfall_rate_water_equivalent",
        "large_scale_snowfall",
        "snow_albedo",
        "snow_density",
        "snow_depth",
        "snow_evaporation",
        "snowfall",
        "snowmelt",
        "temperature_of_snow_layer",
        "total_column_snow_water",
        "soil_temperature_level_1",
        "soil_temperature_level_2",
        "soil_temperature_level_3",
        "soil_temperature_level_4",
        "soil_type",
        "volumetric_soil_water_layer_1",
        "volumetric_soil_water_layer_2",
        "volumetric_soil_water_layer_3",
        "volumetric_soil_water_layer_4",
        "vertical_integral_of_divergence_of_geopotential_flux",
        "vertical_integral_of_divergence_of_kinetic_energy_flux",
        "vertical_integral_of_divergence_of_mass_flux",
        "vertical_integral_of_divergence_of_moisture_flux",
        "vertical_integral_of_divergence_of_ozone_flux",
        "vertical_integral_of_divergence_of_thermal_energy_flux",
        "vertical_integral_of_divergence_of_total_energy_flux",
        "vertical_integral_of_eastward_geopotential_flux",
        "vertical_integral_of_eastward_heat_flux",
        "vertical_integral_of_eastward_kinetic_energy_flux",
        "vertical_integral_of_eastward_mass_flux",
        "vertical_integral_of_eastward_ozone_flux",
        "vertical_integral_of_eastward_total_energy_flux",
        "vertical_integral_of_eastward_water_vapour_flux",
        "vertical_integral_of_energy_conversion",
        "vertical_integral_of_kinetic_energy",
        "vertical_integral_of_mass_of_atmosphere",
        "vertical_integral_of_mass_tendency",
        "vertical_integral_of_northward_geopotential_flux",
        "vertical_integral_of_northward_heat_flux",
        "vertical_integral_of_northward_kinetic_energy_flux",
        "vertical_integral_of_northward_mass_flux",
        "vertical_integral_of_northward_ozone_flux",
        "vertical_integral_of_northward_total_energy_flux",
        "vertical_integral_of_northward_water_vapour_flux",
        "vertical_integral_of_potential_and_internal_energy",
        "vertical_integral_of_potential_internal_and_latent_energy",
        "vertical_integral_of_temperature",
        "vertical_integral_of_thermal_energy",
        "vertical_integral_of_total_energy",
        "vertically_integrated_moisture_divergence",
        "high_vegetation_cover",
        "leaf_area_index_high_vegetation",
        "leaf_area_index_low_vegetation",
        "low_vegetation_cover",
        "type_of_high_vegetation",
        "type_of_low_vegetation",
        "angle_of_sub_gridscale_orography",
        "anisotropy_of_sub_gridscale_orography",
        "benjamin_feir_index",
        "boundary_layer_dissipation",
        "boundary_layer_height",
        "charnock",
        "convective_available_potential_energy",
        "convective_inhibition",
        "duct_base_height",
        "eastward_gravity_wave_surface_stress",
        "eastward_turbulent_surface_stress",
        "forecast_albedo",
        "forecast_surface_roughness",
        "friction_velocity",
        "geopotential",
        "gravity_wave_dissipation",
        "instantaneous_eastward_turbulent_surface_stress",
        "instantaneous_moisture_flux",
        "instantaneous_northward_turbulent_surface_stress",
        "k_index",
        "land_sea_mask",
        "mean_vertical_gradient_of_refractivity_inside_trapping_layer",
        "minimum_vertical_gradient_of_refractivity_inside_trapping_layer",
        "northward_gravity_wave_surface_stress",
        "northward_turbulent_surface_stress",
        "sea_ice_cover",
        "skin_reservoir_content",
        "slope_of_sub_gridscale_orography",
        "standard_deviation_of_filtered_subgrid_orography",
        "standard_deviation_of_orography",
        "total_column_ozone",
        "total_column_supercooled_liquid_water",
        "total_column_water",
        "total_column_water_vapour",
        "total_totals_index",
        "trapping_layer_base_height",
        "trapping_layer_top_height",
        "u_component_stokes_drift",
        "v_component_stokes_drift",
        "zero_degree_level",
        "air_density_over_the_oceans",
        "coefficient_of_drag_with_waves",
        "free_convective_velocity_over_the_oceans",
        "maximum_individual_wave_height",
        "mean_direction_of_total_swell",
        "mean_direction_of_wind_waves",
        "mean_period_of_total_swell",
        "mean_period_of_wind_waves",
        "mean_square_slope_of_waves",
        "mean_wave_direction_of_first_swell_partition",
        "mean_wave_direction_of_second_swell_partition",
        "mean_wave_direction_of_third_swell_partition",
        "mean_wave_period_based_on_first_moment",
        "mean_wave_period_based_on_first_moment_for_swell",
        "mean_wave_period_based_on_first_moment_for_wind_waves",
        "mean_wave_period_based_on_second_moment_for_swell",
        "mean_wave_period_based_on_second_moment_for_wind_waves",
        "mean_wave_period_of_first_swell_partition",
        "mean_wave_period_of_second_swell_partition",
        "mean_wave_period_of_third_swell_partition",
        "mean_zero_crossing_wave_period",
        "model_bathymetry",
        "normalized_energy_flux_into_ocean",
        "normalized_energy_flux_into_waves",
        "normalized_stress_into_ocean",
        "ocean_surface_stress_equivalent_10m_neutral_wind_direction",
        "ocean_surface_stress_equivalent_10m_neutral_wind_speed",
        "peak_wave_period",
        "period_corresponding_to_maximum_individual_wave_height",
        "significant_height_of_total_swell",
        "significant_height_of_wind_waves",
        "significant_wave_height_of_first_swell_partition",
        "significant_wave_height_of_second_swell_partition",
        "significant_wave_height_of_third_swell_partition",
        "wave_spectral_directional_width",
        "wave_spectral_directional_width_for_swell",
        "wave_spectral_directional_width_for_wind_waves",
        "wave_spectral_kurtosis",
        "wave_spectral_peakedness",
        "wave_spectral_skewness"
    ],
}


@dataclass(kw_only=True)
class session():
    dataset: str
    variables: list
    data_format: str = 'netcdf'
    dataPath: str = None
    logPath: str = field(default=None,init=False)

    def __post_init__(self):
        root = os.path.join(os.path.split(__file__)[0],'tempData')
        if not os.path.isdir(root):
            os.makedirs(root)
        self.tempzip = os.path.join(os.path.split(__file__)[0],'tempData','download.zip')
        if self.dataPath is None:
            self.ncOut = os.path.join(os.path.split(__file__)[0],'tempData','request')
        else:
            self.ncOut = os.path.join(self.dataPath,'request')

        if self.dataPath is None:
            input('Proceed without storing request?')
        elif not os.path.isdir(self.dataPath):
            sys.exit(f'Path does not exist: {self.dataPath}')
        else:
            self.logPath = os.path.join(self.dataPath,'request.log')
            if os.path.isfile(self.logPath):
                with open(self.logPath) as f:
                    self.log = json.load(f)
            else:
                self.log = {}

        badVar = [v for v in self.variables if v not in Available_Variables[self.dataset]]
        if len(badVar):
            sys.exit(f"Invalid variable selections for {self.dataset}: {badVar}")
        if not os.path.isfile(os.path.join(os.path.split(__file__)[0],'cdsapi.rc')):
            sys.exit(f'Save API key here: {os.path.join(os.path.split(__file__)[0],'cdsapi.rc')}')
        with open(os.path.join(os.path.split(__file__)[0],'cdsapi.rc'),'r') as f:
            apikey = yaml.safe_load(f)
        self.client = cdsapi.Client(
            url=apikey['url'],
            key=apikey['key']
        )

    def submitRequest(self,request):
        request_id = str(uuid.uuid5(uuid.NAMESPACE_DNS,str(request)))
        if request_id in self.log:
            print('Request already complete, skipping download')
        else:
            self.log[request_id] = request
            self.downloadSave(request_id,request)
            if self.logPath is not None:
                with open(self.logPath, 'w+') as f:
                    json.dump(self.log,f)
        return(str(request_id))

    def downloadSave(self,name,request):
        # for d,request in self.request.items():
        print(f'Downloading {name}')
        self.client.retrieve(self.dataset, request, self.tempzip)
        shutil.unpack_archive(self.tempzip,self.ncOut.replace('request',name))
        os.remove(self.tempzip)


@dataclass(kw_only=True)
class getERA5_atPoint(session):
    dataPath: str = None
    name: str = None
    latitude: float
    longitude: float
    startDate: str
    stopDate: str
    dataset: str = 'reanalysis-era5-single-levels-timeseries' # 'reanalysis-era5-single-levels' for area downloads
    variables: list = field(default_factory=lambda:[
        "10m_u_component_of_wind",
        "10m_v_component_of_wind",
        "2m_dewpoint_temperature",
        "2m_temperature",
        "boundary_layer_height",
        "surface_latent_heat_flux",
        "surface_pressure",
        "surface_sensible_heat_flux",
        "surface_solar_radiation_downwards",
        "surface_thermal_radiation_downwards",
        "total_cloud_cover",
        "total_precipitation"])

    def __post_init__(self):
        super().__post_init__()
        request = {
            'variable':self.variables,
            'location':{'longitude':self.longitude,'latitude':self.latitude},
            'date':[f"{self.startDate}/{self.stopDate}"],
            'data_format':self.data_format
        }
        request_id = self.submitRequest(request)
        tmp = self.ncOut.replace('request',request_id)
        self.time_series = []
        for f in os.listdir(tmp):
            ds = xr.open_dataset(os.path.join(tmp,f))
            ts = ds.to_dataframe()
            # Only runs for one point at a time, so this is fine
            if self.name is None:
                xy = ts.groupby(['latitude','longitude']).count().index.values[0]
                self.name = f"{xy[0]},{xy[1]}"
            ts = ts[[v for v in ds.data_vars]].copy()
            ts.columns = pd.MultiIndex.from_tuples([
                (self.name,varName,ds[varName].units,str(ds['t2m'].dtype),ds[varName].long_name)
                for varName in ds.data_vars
            ])
            self.time_series.append(ts)
        self.time_series = pd.concat(self.time_series).sort_index()
        self.time_series.index = self.time_series.index.tz_localize('UTC')


@dataclass(kw_only=True)
class getERA5_area(session):
    area: list = None
    startDate: str
    stopDate: str
    dataset: str = 'reanalysis-era5-single-levels'
    variables: list = field(default_factory=lambda:[
        # "10m_u_component_of_wind",
        # "10m_v_component_of_wind",
        # "2m_dewpoint_temperature",
        "2m_temperature",
        # "surface_pressure",
        # "total_precipitation",
        # "surface_net_solar_radiation",
        # "surface_net_thermal_radiation",
        # "surface_sensible_heat_flux",
        # "surface_latent_heat_flux",
        # "surface_solar_radiation_downwards",
        # "surface_thermal_radiation_downwards",
        # "snow_depth",
        # "snowfall",
        # "soil_temperature_level_1",
        # "volumetric_soil_water_layer_1",
        # "boundary_layer_height"
    ])
    WGS: str = field(default="EPSG:4326",init=False)
    UTM: str = field(default=None,init=False)
    Points: gpd.GeoDataFrame = field(default=None,init=False)

    def __post_init__(self):
        self.requests = []
        
        super().__post_init__()
        # self.request = {}
        for d in pd.date_range(self.startDate,self.stopDate,freq='MS'):
            if d > datetime.datetime.now(): continue
            request = {
                "product_type": ["reanalysis"],
                'variable':self.variables,
                'year':[str(d.year)],
                'month':[str(d.month).zfill(2)],
                "day": [
                    "01", "02", "03",
                    "04", "05", "06",
                    "07", "08", "09",
                    "10", "11", "12",
                    "13", "14", "15",
                    "16", "17", "18",
                    "19", "20", "21",
                    "22", "23", "24",
                    "25", "26", "27",
                    "28", "29", "30",
                    "31"
                ],
                "time": [
                    "00:00", "01:00", "02:00",
                    "03:00", "04:00", "05:00",
                    "06:00", "07:00", "08:00",
                    "09:00", "10:00", "11:00",
                    "12:00", "13:00", "14:00",
                    "15:00", "16:00", "17:00",
                    "18:00", "19:00", "20:00",
                    "21:00", "22:00", "23:00"
                ],
                'data_format':self.data_format,
                'download_format':'zip'
            }
            if self.area is not None:
                request = request | {'area':self.area}
            request_id = self.submitRequest(request)
            self.requests.append(request_id)



def distance_matrix(x0, y0, x1, y1):
    obs = np.vstack((x0, y0)).T
    interp = np.vstack((x1, y1)).T

    # Make a distance matrix between pairwise observations
    # Note: from <http://stackoverflow.com/questions/1871536>
    # (Yay for ufuncs!)
    d0 = np.subtract.outer(obs[:,0], interp[:,0])
    d1 = np.subtract.outer(obs[:,1], interp[:,1])

    return np.hypot(d0, d1)

def simple_idw(x, y, z, xi, yi):
    mask = ~np.isnan(z)
    x = x[mask]
    y = y[mask]
    z = z[mask]
    dist = distance_matrix(x,y, xi,yi)
    # In IDW, weights are 1 / distance
    weights = 1.0 / dist

    # Make weights sum to one
    weights /= weights.sum(axis=0)

    # Multiply the weights for each interpolated point by all observed Z-values
    zi = np.dot(weights.T, z)
    return zi

@dataclass(kw_only=True)
class getERA5_IDW_at_points(getERA5_area):
    latitude: list
    longitude: list
    pointID: list
    area: list = None #[ymax,xmin,ymin,xmax] < copernicus request format
    radius: float = 1e5

    def __post_init__(self):
        # Project points in UTM, buffer, get bounds in Lat/Lon for "area" query,
        self.Points = gpd.GeoDataFrame(index = [id for id in self.pointID], geometry=gpd.points_from_xy(x=self.longitude,y=self.latitude),crs='WGS1984')
        self.UTM = f"EPSG:{self.Points.estimate_utm_crs().to_epsg()}"
        self.Points = self.Points.to_crs(self.UTM)
        pointBox = self.Points.dissolve().buffer(self.radius).to_crs(self.WGS).total_bounds
        # Reformat area expectation by api
        pointBox = [round(float(pointBox[-1]),3)]+[round(float(a),3) for a in pointBox[0:3]]
        if self.area is None:
            self.area = pointBox
        else:
            pointBox = [max(self.area[0],pointBox[0]),min(self.area[1],pointBox[1]),min(self.area[2],pointBox[2]),max(self.area[3],pointBox[3])]
            if pointBox != self.area:
                print('Point buffer has larger bbox that area provided, overwriting area to point buffer')
                self.area = pointBox
        super().__post_init__()
        point_var = []
        T0 = time.time()
        for request_id in self.requests:
            point_var.append([])
            T1 = time.time()
            # self.downloadSave(d,request)
            print('Completed in :',time.time()-T1)
            tmp = self.ncOut.replace('request',request_id)
            for dsname in os.listdir(tmp):
                dsname = os.path.join(tmp,dsname)
                ds = xr.open_dataset(dsname)
                ds.rio.write_crs(self.WGS,inplace=True)
                ds = ds.rio.reproject(self.UTM)
                x,y=np.meshgrid(ds.x.values,ds.y.values)
                x,y=x.flatten(),y.flatten()
                timestamp = ds.valid_time.values
                point_var[-1].append(
                    pd.concat([pd.DataFrame(
                    index=timestamp,
                    columns=pd.MultiIndex.from_tuples([(id,varName,ds[varName].units,str(ds['t2m'].dtype),ds[varName].long_name) for id in self.Points.index]),
                    # For each variable, do IDW on all timesteps (masking for nan values)
                    data=np.array([
                        simple_idw(x,y,ds[varName].values[i].flatten(),self.Points.geometry.x,self.Points.geometry.y)
                        for i in range(ds[varName].values.shape[0])]), 
                    ) for varName in ds.data_vars],axis=1)
                    )
            point_var[-1] = pd.concat(point_var[-1],axis=1)
        print('Full time: ',time.time()-T0)
        self.time_series = pd.concat(point_var)
        self.time_series.index = self.time_series.index.tz_localize('UTC')

