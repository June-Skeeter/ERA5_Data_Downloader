from download_ERA5_Data import getERA5_atPoint, getERA5_area, getERA5_IDW_at_points
import matplotlib.pyplot as plt

ps = getERA5_atPoint(
    longterm_Storage='tempData/SCL_time_series',
    latitude=69.229,
    longitude=-135.257,
    startDate='2026-06-01',
    stopDate='2026-09-30'
)

ass = getERA5_IDW_at_points(
    longterm_Storage='tempData/testing',
    latitude=[69.229,69.319],
    longitude=[-135.257,-135.478],
    pointID=['SCL','SEEP'],
    # area=[72,-139,67,-131],
    startDate='2026-06-01',
    stopDate='2026-09-30'
)

plt.figure()
plt.plot(
    ps.time_series.index,
    ps.time_series[('69.25,-135.25','t2m','K','float32','2 metre temperature')],
    label='SCL_nearest_grid'
)

plt.plot(
    ass.time_series.index,
    ass.time_series[('SCL','t2m','K','float32','2 metre temperature')],
    label='SCL_idw'
)

plt.legend()
plt.show()