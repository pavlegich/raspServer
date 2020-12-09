#!/usr/bin/env python
# coding: utf-8

# In[119]:


import numpy as np
from scipy.interpolate import splrep, splev
from pymavlink import mavutil
import time

# vehicle = mavutil.mavlink_connection("/dev/ttyACM0", baud=115200)

UAV = []

# while True:
# vehicle.wait_heartbeat()
lat = 60.03151
lon = 30.36011

lat1 = 60.03148
lon1 = 30.3603

while True:
	if len(UAV)<6:
		UAV.append([lat, lon])
	else:
		UAV.pop(0)
		UAV.append([lat1, lon1])
	time.sleep(2)




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

# plt.show()


# In[ ]:




