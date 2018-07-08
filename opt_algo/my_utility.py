# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 12:09:16 2017

@author: fangzhou
"""

import numpy as np
import collections
import ast
import itertools


# ======================= My Utilities ==========================
def setprod(*args):
    """cross product of multiple lists"""
    return itertools.product(*args)

def console(string):
    """For cplex result stream on console, in addition to file"""
    print(string, end='', flush=True)
    return string

def read_dat(file):
    """Return a list containing the data stored in the dat file."""
    with open(file, 'r') as f:
         ret = [ast.literal_eval(line) for line in iter(f.readline, '')]
    return ret

def flatten(x):
    """Flatten multi-level list."""
    if isinstance(x, collections.Iterable):
        return [a for i in x for a in flatten(i)]
    else:
        return [i for i in [x] if i is not None]

def create_dat(file='data.dat', sysnum=0, seed=None):
    """
    Create random data for MS1M.
    """
    # sysdata stores cfs_rate, cs_rate, hf_single, hs_single, K, op
    # info for each system
    sysdata = [
            [0.638, 0.100, 2.167, 3.900, 12, 0.373],
            [0.638, 0.100, 2.167, 0.228, 12, 1.073],
            [0.638, 0.100, 2.167, 0.260, 12, 0.373],
            [0.638, 0.070, 2.167, 0.228, 12, 1.405],
            [0.638, 0.080, 2.167, 3.120, 12, 0.511],
            [0.638, 0.080, 2.167, 0.189, 12, 1.211],
            [0.638, 0.080, 2.167, 0.212, 12, 0.511],
            [0.638, 0.056, 2.167, 0.189, 12, 1.542],
            [0.580, 0.100, 3.900, 3.900, 12, 0.373],
            [0.580, 0.100, 3.900, 0.228, 12, 1.073],
            [0.580, 0.100, 3.900, 0.260, 12, 0.373],
            [0.580, 0.070, 3.900, 0.228, 12, 1.405],
            [0.580, 0.080, 3.900, 3.120, 12, 0.511],
            [0.580, 0.080, 3.900, 0.189, 12, 1.211],
            [0.580, 0.080, 3.900, 0.212, 12, 0.511],
            [0.580, 0.056, 3.900, 0.189, 12, 1.542]]
    cskdata = [
            9930, 10380, 11280,
            19410, 19860, 20760,
            28890, 29340, 30240,
            38370, 38820, 39720,
            14495, 14945, 15845,
            23975, 24425, 25325,
            38020, 38470, 39370,
            47500, 47950, 48850,
            12730, 13180, 14080,
            22210, 22660, 23560,
            31690, 32140, 33040,
            41170, 41620, 42520,
            47459, 47909, 48809,
            94468, 94918, 95818,
            141477, 141927, 142827,
            188486, 188936, 189836,
            37320, 37770, 38670,
            74190, 74640, 75540,
            111060, 111510, 112410,
            147930, 148380, 149280,
            41885, 42335, 43235,
            78755, 79205, 80105,
            120190, 120640, 121540,
            157060, 157510, 158410,
            40120, 40570, 41470,
            76990, 77440, 78340,
            113860, 114310, 115210,
            150730, 151180, 152080,
            74849, 75299, 76199,
            149248, 149698, 150598,
            223647, 224097, 224997,
            298046, 298496, 299396,
            9930, 10380, 11280,
            19410, 19860, 20760,
            28890, 29340, 30240,
            38370, 38820, 39720,
            14495, 14945, 15845,
            23975, 24425, 25325,
            38020, 38470, 39370,
            47500, 47950, 48850,
            12730, 13180, 14080,
            22210, 22660, 23560,
            31690, 32140, 33040,
            41170, 41620, 42520,
            47459, 47909, 48809,
            94468, 94918, 95818,
            141477, 141927, 142827,
            188486, 188936, 189836,
            37320, 37770, 38670,
            74190, 74640, 75540,
            111060, 111510, 112410,
            147930, 148380, 149280,
            41885, 42335, 43235,
            78755, 79205, 80105,
            120190, 120640, 121540,
            157060, 157510, 158410,
            40120, 40570, 41470,
            76990, 77440, 78340,
            113860, 114310, 115210,
            150730, 151180, 152080,
            74849, 75299, 76199,
            149248, 149698, 150598,
            223647, 224097, 224997,
            298046, 298496, 299396]
    UEdata = [847, 1694, 2541, 3388, 847, 1694, 2541, 3388, 847, 1694, 2541,
              3388, 800, 1600, 2400, 3200, 847, 1694, 2541, 3388, 847, 1694,
              2541, 3388, 847, 1694, 2541, 3388, 800, 1600, 2400, 3200, 847,
              1694, 2541, 3388, 847, 1694, 2541, 3388, 847, 1694, 2541, 3388,
              800, 1600, 2400, 3200, 847, 1694, 2541, 3388, 847, 1694, 2541,
              3388, 847, 1694, 2541, 3388, 800, 1600, 2400, 3200]
    UCdata = [9240, 9240, 9240, 9240, 9240, 9240, 9240, 9240, 9240, 9240, 9240,
              9240, 9240, 9240, 9240, 9240, 9240, 9240, 9240, 9240, 9240, 9240,
              9240, 9240, 9240, 9240, 9240, 9240, 9240, 9240, 9240, 9240, 9999,
              9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999,
              9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999,
              9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999]

    np.random.seed(seed=seed)
    T, F, S = 26, 100, 50
    radius = 50
    total_biomass = 700000

    a_weight = np.array([5,5,6,7,10,11,12,11,9,8,6,5,5] + [0]*13)

#=================== generate coordinates, harvest, demand data ===============
    sites = np.random.uniform(-radius, radius, size=(2*(F+S),2))
    sits_in = sites[np.sum(sites*sites, axis=1) <= radius**2]
    coord_f = sits_in[:F]
    coord_s = sits_in[-S:]

#    from matplotlib import pyplot as plt
#    l1, = plt.plot(0, 'g^', markersize=7)
#    l2, = plt.plot(*coord_s.T, 'ro', markersize=5)
#    l3, = plt.plot(*coord_f.T, 'bx', markersize=5)
#    plt.legend([l1,l2,l3],['Bio-refinery','SSL','Farm'])
#    circles = [plt.Circle((0,0), i*10,color='k', fill=False,
#                          linestyle='dotted', linewidth=.5) for i in range(1,6)]
#    [plt.gcf().gca().add_artist(circles[i]) for i in range(5)]
#    plt.axis('equal')
#    plt.show()

    a_raw = np.random.uniform(1, 10, size=(T,F))

    a_raw = (a_raw.T*a_weight[:T]).T
    a_raw = a_raw/a_raw.sum()*total_biomass*1.001
    a = [[0]*F]+a_raw.round().astype(int).tolist()

    dt = int(total_biomass/T)
    d =  [0] + [dt]*T

#=================== generate system specific data ============================
    cfs_rate, cs_rate, hf_single, hs_single, K, c_op = sysdata[sysnum]

    cfs = [[np.linalg.norm(coord_f[f]-coord_s[s])*cfs_rate
           for s in range(S)] for f in range(F)]
    cs = [np.linalg.norm(coord_s[s])*cs_rate for s in range(S)]

    csk_index = [0] + np.cumsum(np.array(sysdata)[:,4]).astype(int).tolist()
    csk = [cskdata[csk_index[sysnum]:csk_index[sysnum+1]] for s in range(S)]

    hf = [hf_single]*F
    hs = [hs_single]*S

    U = [2500,5000,10000]*int(K/3)
    UE_index = [0] + np.cumsum(np.array(sysdata)[:,4]/3).astype(int).tolist()
    UE = flatten([[i]*3 for i in UEdata[UE_index[sysnum]:UE_index[sysnum+1]]])
    UC = flatten([[i]*3 for i in UCdata[UE_index[sysnum]:UE_index[sysnum+1]]])

    cfs_str = [['{:.2f}'.format(x) for x in y] for y in cfs]
    cs_str = ['{:.2f}'.format(x) for x in cs]
    with open(file,'w') as f:
        f.writelines(('{}\n'*11).format(cfs_str, cs_str, c_op, csk,
                     hf, hs, a, d, U, UE, UC).replace("'", ''))




