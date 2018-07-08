# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 10:10:09 2017

@author: fangzhou
"""

from my_utility import create_dat, read_dat, setprod
import logging
import sys
import os
import numpy as np
from collections import Counter
from gurobipy import *

def keyboard_terminate(model, where):
    try:
        pass
    except KeyboardInterrupt:
        model.terminate()

# logging.basicConfig(
#         level=logging.INFO,
#         format='%(asctime)s %(filename)s:%(levelname)s - %(message)s',
#         handlers=[logging.FileHandler('RunLog.log'),logging.StreamHandler()])

#sysnum = 7
#t_limit = 50
sysnum = int(sys.argv[1])
t_limit = float(sys.argv[2])
#("[Sys{}] begin, time limit = {:.0f}s".format(sysnum, t_limit))

create_dat('data.dat', sysnum, seed=1)
cfs, cs, c_op, csk, hf, hs, a, d, U, UE, UC = read_dat('data.dat')

T = list(range(1,len(d)))
F, S, K = list(range(len(hf))), list(range(len(hs))), list(range(len(U)))
a = np.array(a)
M = a.sum(axis=0)

m = Model('ms1m_base')

# =========================== Create vars and objectives ======================
w = m.addVars(S,K, obj=csk, vtype='B', name='w')
y = m.addVars(F, S, vtype='B', name='y')
z1 = m.addVars(T,F,S, obj=cfs*len(T), name='z1')
z2 = m.addVars(T,S, obj=cs*len(T), name='z2')
Is = m.addVars([0]+T,S, obj=[0]*len(S)+hs*len(T), name='Is')
If = m.addVars([0]+T,F, obj=[0]*len(F)+hf*len(T), name='If')

m.setAttr('UB', Is.select(0,'*'), [0]*len(S))
m.setAttr('UB', If.select(0,'*'), [0]*len(F))

m.ModelSense = GRB.MINIMIZE

# ============================ Create constraints =============================
m.addConstrs((w.sum(s,'*') <= 1 for s in S), name='c1')
m.addConstrs((y[f,s] <= w.sum(s,'*') for f in F for s in S), name='c2')
m.addConstrs((y.sum(f,'*') == 1 for f in F), name='c3')
m.addConstrs((Is[t,s] == Is[t-1,s]-z2[t,s]+z1.sum(t,'*',s) for
              t in T for s in S), name='c4')
m.addConstrs((If[t,f] == If[t-1,f]+a[t,f]-z1.sum(t,f,'*') for
              t in T for f in F), name='c5')
m.addConstrs((z2.sum(t,'*') == d[t] for t in T), name='c6')
m.addConstrs((Is[t,s] <= quicksum([U[k]*w[s,k] for k in K]) for
              t in T for s in S), name='c7')
m.addConstrs((z1.sum('*',f,s) <= M[f]*y[f,s] for f in F for s in S), name='c8')
m.addConstrs((z1.sum(t,'*',s) <= quicksum([min(UC[k],UE[k])*w[s,k] for k in K])
                for t in T for s in S), name='c9')

#================================== Solve =====================================
#m.update()
#m.write('ms1m_grb.lp')
m.setParam('MIPGap', 0.01)
m.setParam('TimeLimit', t_limit)
m.setParam('Threads',6)
m.update()
#m.read('start.mst')
# if os.path.isfile('warm starts/BASE {} 26wk.mst'.format(sysnum)):
#     m.read('warm starts/BASE {} 26wk.mst'.format(sysnum))
# elif os.path.isfile('warm starts/JIT {} 26wk.mst'.format(sysnum)):
#     m.read('warm starts/JIT {} 26wk.mst'.format(sysnum))
m.optimize(keyboard_terminate)

#================================== Result ====================================
status = {1:'LOADED',2:'OPTIMAL',3:'INFEASIBLE',7:'ITERATION_LIMIT',
    8:'NODE_LIMIT',9:'TIME_LIMIT',10:'SOLUTION_LIMIT',11:'INTERRUPTED'}

if m.SolCount:
    m.write('start.mst')
    #m.write('warm starts/BASE {} 26wk.mst'.format(sysnum))
    op_cost = a.sum()*c_op
    total_lb = m.objBound + op_cost
    total_obj = m.objVal + op_cost
    gap = (total_obj-total_lb)/total_obj
    loc_cost = w.prod({(s,k): csk[s][k] for s in S for k in K}).getValue()
    trans1_cost = z1.prod({(t,f,s):cfs[f][s] for
                           t,f,s in setprod(T,F,S)}).getValue()
    trans2_cost = z2.prod({(t,s):cs[s] for t in T for s in S}).getValue()
    invS_cost = Is.prod({(t,s):hs[s] for t in T for s in S}).getValue()
    invF_cost = If.prod({(t,f):hf[f] for t in T for f in F}).getValue()
    numSSL = w.sum().getValue()
    K_cnt = dict(Counter(k for s in S for k in K if w[s,k].x > 0.9))

    print("[Sys{}] {} in {:.1f}sec\n"
                 "    LB     = {:.0f}\n"
                 "    UB     = {:.0f}\n"
                 "    op.    = {:.0f}\n"
                 "    loc    = {:.0f}\n"
                 "    trans1 = {:.0f}\n"
                 "    trans2 = {:.0f}\n"
                 "    invS   = {:.0f}\n"
                 "    invF   = {:.0f}\n"
                 "    Gap    = {:.2f}%\n"
                 "    NumSSL = {:.0f}\n"
                 "    K_cnt  = {}\n".format(
                 sysnum, status[m.status], m.runtime,
                 total_lb, total_obj, op_cost, loc_cost, trans1_cost,
                 trans2_cost, invS_cost, invF_cost, gap*100, numSSL,K_cnt))

#else:
    #logging.info("[Sys{}] {}\n".format(sysnum, status[m.status]))
    #print("[Sys{}] {}\n".format(sysnum, status[m.status]))