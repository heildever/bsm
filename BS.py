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

import sys

import matplotlib.pyplot as plt
import numpy as np
import scipy.io as scio


def main(arg):
    # strategy(com)
    strategy(com_end)
    # strategy(res)
    # strategy(res_end)
    return 0


def randomator(traffic):
    for i in range(len(traffic)):
        margin = np.random.uniform(0.0, (traffic[i] / 4))
        if np.random.random_integers(0, 1) == 1:  # random decision of (+/-)
            traffic[i] = min(1, traffic[i] + margin)
        else:
            traffic[i] = max(0.01, traffic[i] - margin)
    return traffic


def strategy(traffic):
    # defining constants
    no_macro = 1
    ntrx_macro = 6
    ntrx_micro = 2
    pmax_macro = 20
    pmax_micro = 6.3
    p0_macro = 84
    p0_micro = 56
    deltaP_macro = 2.8  # different in paper&excel sheet
    deltaP_micro = 2.6
    energy = np.empty(np.shape(traffic))
    energy2 = np.empty(np.shape(traffic))
    saving = np.empty(np.shape(traffic))
    power = np.empty(np.shape(traffic))
    cart = np.arange(0, 48)
    plt.plot(traffic, '--', color="blue", linewidth=2, label='fixed')
    randomator(traffic)
    plt.plot(traffic, color="red", label="randomized")
    plt.title('randomized load profile')
    plt.legend(loc='upper left')
    plt.grid(which="major", axis="both")
    plt.show()
    traffic = traffic * 5
    for i in range(len(traffic)):
        if 4.0 < traffic[i] < 5:
            no_micro = 4
        elif 3.0 < traffic[i] < 4:
            no_micro = 3
        elif 2.0 < traffic[i] < 3:
            no_micro = 2
        elif 1.0 < traffic[i] < 2:
            no_micro = 1
        elif traffic[i] < 1.0:
            no_micro = 0
        load = traffic[i] / (no_micro + no_macro)
        macro = no_macro * (ntrx_macro * (p0_macro + pmax_macro * deltaP_macro * load) / 2)
        energy[i] = macro + (no_micro * (ntrx_micro * (p0_micro + pmax_micro * deltaP_micro * load) / 2))
        energy2[i] = macro + (4 * ntrx_micro * (p0_micro + pmax_micro * deltaP_micro * traffic[i] / 5) / 2)
        power[i] = energy[i] * 2
        saving[i] = energy2[i] - energy[i]
    print "daily energy consumption without strategy applied (in Wh) :", sum(energy2)
    print "daily energy consumption when strategy applied (in Wh) :", sum(energy)
    print "daily energy saving(in Wh) is :", sum(saving)
    # visualization of results	
    plt.bar(cart, energy, label="energy-saving", width=1, color='green', edgecolor='green')
    # plt.plot(energy,label="energy-saving",color='green',drawstyle='steps')
    plt.plot((cart + 1), energy2, label="always ON", linewidth=5, drawstyle='steps')
    plt.xlabel("30mins")
    plt.ylabel("energy consumption in Wh")
    plt.title('strategy effect')
    plt.grid(which="major", axis="both")
    plt.legend(loc='upper left')
    plt.show()
    plt.plot(saving/ energy2, linewidth=2, drawstyle='steps')
    plt.grid(which="major", axis="both")
    plt.xlabel("30mins")
    plt.ylabel("energy savings in percentage")
    plt.show()
    plt.plot(saving, linewidth=2, drawstyle='steps')
    plt.xlabel("30mins")
    plt.ylabel("energy savings in Wh")
    plt.grid(which="major", axis="both")
    plt.show()
    return power


if __name__ == '__main__':
    # importing traffic profiles
    mat_file = scio.loadmat('normalizedtraffic.mat')
    data = mat_file.get('normalizedtraffic')
    com = data[:, 0]  # 24h weekday traffic for commercial area BS
    com_end = data[:, 1]  # 24h weekend traffic for commercial area BS
    res = data[:, 2]  # 24h weekday traffic for residential area BS
    res_end = data[:, 3]  # 24h weekend traffic for residential area BS
    sys.exit(main(sys.argv))
