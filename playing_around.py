# -*- coding: utf-8 -*-
"""
Australian frog dataset for pydatemm
====================================
Created on Tue Mar  5 13:10:23 2024

@author: theja
"""
from scipy import spatial
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

df = pd.read_csv('micxy.csv')
micxy = df.to_numpy()

mic_2_mic = spatial.distance_matrix(micxy, micxy)

plt.figure()
a0 = plt.subplot(111)
a0.set_aspect('equal')
a0.plot(micxy[:,0], micxy[:,1], 'k*')

# give them fak xyz coordinates 
micxyz_fake = np.column_stack((micxy.copy(), np.random.choice(np.linspace(0,0.03,10),
                                                              micxy.shape[0])))