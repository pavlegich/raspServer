import numpy as np
from scipy.interpolate import splrep, splev
from pymavlink import mavutil
import time
import random

# vehicle = mavutil.mavlink_connection("/dev/ttyACM0", baud=115200)

UAV2 = []


while len(UAV2)<6:
	x = random.uniform(59.973982, 59.973478)
	y = random.uniform(30.298140, 30.300297)
	UAV2.append([x,y])

UAV2e = np.array(UAV2)
lat = np.array(UAV2e[:,0])
lon = np.array(UAV2e[:,1])

j = 5

step = np.diff(lon[(j-5):(j+2)]).mean()
x_extra = np.array([lon[j]+step,lon[j]+step*2,lon[j]+step*3])
lon_sort = np.sort(lon)
spl = splrep(lon_sort[(j-5):(j+2):2], lat[(j-5):(j+2):2], k=1)
y_extra = splev(x_extra, spl)

# data = np.array([[60.03158, 30.36], [60.03151, 30.36011], [60.03148, 30.3603], [60.03147, 30.3605], [60.03154, 30.36071], [60.03148, 30.36081]])
# x = np.array(data[:,1])
# y = np.array(data[:,0])


# In[170]:


# plt.plot(x, y, '.'+'-')
# j = len(x)-1
# step = np.diff(x[:(j+2)]).mean()
# x_extra = np.array([x[j]+step,x[j]+step*2,x[j]+step*3])
# spl = splrep(x[:(j+2):2], y[:(j+2):2], k=1)
# y_extra = splev(x_extra, spl)
# plt.plot (x_extra, y_extra, '.'+'--')




