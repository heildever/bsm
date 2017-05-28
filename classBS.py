#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Bs.py  
#  Copyright 2017 heildever <https://github.com/heildever> 
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY.
import scipy.io as scio
import numpy as np

# importing traffic profiles
mat_file = scio.loadmat('normalizedtraffic.mat')
data = mat_file.get('normalizedtraffic')

class BaseStation(object):
	def __init__(self):
		self.com = data[:,0] # 24h weekday traffic for commercial area BS
		#self.com_end = data[:,1] # 24h weekend traffic for commercial area BS
		self.res = data[:,2] # 24h weekday traffic for residential area BS
		#self.res_end = data[:,3] # 24h weekend traffic for residential area BS
		self.energy = self.strategy(self.com)
		#self.power = power 
	
	def randomator(self, traffic):
		for i in range(len(traffic)):
			margin = np.random.uniform(0.0,(traffic[i]/4))
			if np.random.random_integers(0,1)==1: # random decision of (+/-)
				traffic[i] = min(1,traffic[i]+margin)
			else:
				traffic[i] = max(0.01,traffic[i]-margin)	
		return(traffic)	
		
	def strategy(self, traffic):
		self.energy = np.empty(np.shape(traffic))
		self.power = np.empty(np.shape(traffic))
		self.randomator(traffic)
		traffic = traffic*5
		for i in range(len(traffic)) :
			if 4.0<traffic[i]<5.0 :
				no_Micro = 4 
			elif 3.0<traffic[i]<4.0 :
				no_Micro = 3
			elif 2.0<traffic[i]<3.0:
				no_Micro = 2
			elif 1.0<traffic[i]<2.0:
				no_Micro = 1
			elif traffic[i]<1.0:
				no_Micro = 0
			load = traffic[i]/(no_Micro+1)			
			Macro = 6*(84+20*2.8*load)/2
			self.energy[i] = Macro+(no_Micro*(2*(56+6.3*2.6*load)/2))
			power = self.energy*2
		return self.energy
