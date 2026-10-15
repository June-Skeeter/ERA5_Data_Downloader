from dataclasses import dataclass, field
import xarray as xr
import pandas as pd
import cdsapi
import shutil
import yaml
import sys
import os

@dataclass(kw_only=True)
class getERA5_atPoint:
    outputFile: str = None
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
        "total_precipitation"
    ])
    data_format: str = 'netcdf'

    def __post_init__(self):
        if not os.path.isfile('cdsapi.rc'):
            sys.exit('Provide API key')
        with open('cdsapi.rc','r') as f:
            apikey = yaml.safe_load(f)
        client = cdsapi.Client(
            url=apikey['url'],
            key=apikey['key']
        )

        self.request = {
            'variable':self.variables,
            'location':{'longitude':self.longitude,'latitude':self.latitude},
            'date':[f"{self.startDate}/{self.stopDate}"],
            'data_format':self.data_format
        }

        tmpzip = os.path.join(os.path.split(__file__)[0],'tempData','download.zip')
        tmpout = tmpout = os.path.join(os.path.split(__file__)[0],'tempData','download')
        client.retrieve(self.dataset,self.request,tmpzip)
        shutil.unpack_archive(tmpzip,tmpout)
        self.ERA5_time_series = pd.concat([xr.open_dataset(os.path.join(tmpout,f)).to_dataframe().set_index(['latitude','longitude'],append=True) for f in os.listdir(tmpout)],axis=1)
        os.remove(tmpzip)
        shutil.rmtree(tmpout)
        self.ERA5_time_series = self.ERA5_time_series.sort_index(level=0)
        breakpoint()
        if self.outputFile is not None:
            self.ERA5_time_series.to_csv(self.outputFile)

