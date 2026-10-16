from download_ERA5_Data import getERA5_atPoint, getERA5_area, getERA5_IDW_at_points


# ps = getERA5_atPoint(
#     outputFile='tempData/SCL_time_series.csv',
#     latitude=69.229,
#     longitude=-135.257,
#     startDate='2000-09-01',
#     stopDate='2026-09-30'
# )

# 763s to do full month in one batch
# 4343s to do full month day-by-day
ass = getERA5_IDW_at_points(
    outputFolder='tempData/SCL_time_series',
    latitude=[69.229,69.319],
    longitude=[-135.257,-135.478],
    pointID=['SCL','SEEP'],
    # area=[72,-139,67,-131],
    startDate='2026-08-01',
    stopDate='2026-08-31'
)