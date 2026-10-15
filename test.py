from download_ERA5_Data import getERA5_atPoint


ps = getERA5_atPoint(
    outputFile='tempData/SCL_time_series.csv',
    latitude=69.229,
    longitude=-135.257,
    startDate='2000-09-01',
    stopDate='2026-09-30'
)