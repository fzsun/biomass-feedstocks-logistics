from gurobipy import *
import random

#sysnum = int(sys.argv[1])
t_limit = int(sys.argv[1])


def subtourelim(model, where):
  '''Callback - use lazy constraints to eliminate sub-tours'''
  try:
    if where==GRB.Callback.MIPSOL:
      # make a list of edges selected in the solution
      vals=model.cbGetSolution(model._vars)
      selected=tuplelist((i, j) for i, j in model._vars.keys() if vals[i, j]>0.5)
      # find the shortest cycle in the selected edge list
      tour=subtour(selected)
      if len(tour)<t_limit:
        # add subtour elimination constraint for every pair of cities in tour
        model.cbLazy(quicksum(model._vars[i, j]
                              for i, j in itertools.combinations(tour, 2))
                     <=len(tour)-1)
  except KeyboardInterrupt:
    model.terminate()

def subtour(edges):
  '''Given a tuplelist of edges, find the shortest subtour'''
  unvisited=list(range(t_limit))
  cycle=range(t_limit+1)  # initial length has 1 more city
  while unvisited:  # true if list is non-empty
    thiscycle=[]
    neighbors=unvisited
    while neighbors:
      current=neighbors[0]
      thiscycle.append(current)
      unvisited.remove(current)
      neighbors=[j for i, j in edges.select(current, '*') if j in unvisited]
    if len(cycle)>len(thiscycle):
      cycle=thiscycle
  return cycle

#def tsp():
random.seed(1)
points=[(random.randint(0, 100), random.randint(0, 100)) for i in range(t_limit)]
dist={(i, j):
   math.sqrt(sum((points[i][k]-points[j][k])**2 for k in range(2)))
   for i in range(t_limit) for j in range(i)}
m=Model()

vars=m.addVars(dist.keys(), obj=dist, vtype=GRB.BINARY, name='e')
for i, j in vars.keys():
  vars[j, i]=vars[i, j]  # edge in opposite direction
m.addConstrs(vars.sum(i, '*')==2 for i in range(t_limit))

m._vars=vars
m.Params.lazyConstraints=1
m.setParam('Threads', 6)

m.optimize(subtourelim)

vals=m.getAttr('x', vars)
selected=tuplelist((i, j) for i, j in vals.keys() if vals[i, j]>0.5)

tour=subtour(selected)
print(tour)