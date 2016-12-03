#!/usr/bin/python

# ------------------------------------------------------------------------------
# Author: 
#   ANAND RATNA, NIT Durgapur(charianand.maurya@gmail.com)
# Description: 
#	The function createSolution will take input list of points and find optimal rectilinear steineree.
#	Place this file inside buil directry where you maked the z3 
# Usage: 
#   python steiner-tree.py
# ------------------------------------------------------------------------------

from z3 import *
def createSolution(netList):
	#netList is the list of vertex, co-ordinates of tree 
	print netList
	maxx = netList[0][0]
	maxy = netList[0][1]
	minx = netList[0][0]
	miny = netList[0][1]

#Setting min and max co-ordiates for solutin space
	for p in netList:
	    if maxx < p[0]:
	        maxx=p[0]
	    if maxy < p[1]:
	        maxy=p[1]
	    if minx > p[0]:
	        minx=p[0]
	    if miny > p[1]:
	    	miny=p[1]

	maxx = maxx - minx+1
	maxy = maxy - miny+1
	#creating integer variables x_i_j size maxx X maxy
	X = [ [ Int("x_%s_%s" % (i, j)) for j in range(maxy+1) ]
	     for i in range(maxx+1) ]


	#length/cost variable
	cost = Int('cost')


	# each cell contains a value in {1, ..., n}
	cells_c  = [ And(0 <= X[i][j],X[i][j] <= 1)
	            for i in range(maxx+1) for j in range(maxy+1) ]

	# Ternimnal/Sink node co-ordinates k,l
	k = netList[0][0]-minx
	l = netList[0][1]-miny

	#conectivity Constraint
	conn_c = [If(And(k==i,l>j),
	             -X[k][l]-X[i][j]+X[i][j+1] >= -1,
	             If(And(k>i,l==j),
	             -X[k][l]-X[i][j]+X[i+1][j]>= -1,
	             If(And(k==i,l<j),
	             -X[k][l]-X[i][j]+X[i][j-1]>= -1,
	             If(And(k<i,l==j),
	             -X[k][l]-X[i][j]+X[i-1][j]>= -1,
	             If(And(k<i,l<j),
	             -X[k][l]-X[i][j]+X[i][j-1]+X[i-1][j] >= -1,
	             If(And(k>i,l>j),
	             -X[k][l]-X[i][j]+X[i+1][j]+X[i][j+1]>=-1,
	             If(And(k<i,l>j),
	             -X[k][l]-X[i][j]+X[i][j+1]+X[i-1][j]>=-1,
	             If(And(k>i,l<j),
	             -X[k][l]-X[i][j]+X[i][j-1]+X[i+1][j]>=-1,True))))))))
	           for i in range(maxx) for j in range(maxy)]

	#uniqness constraint for nodes in net mapping origin r[0]-minx,r[1]-miny
	uniq_c = [X[r[0]-minx][r[1]-miny] == 1
	                for r in netList]

	#Length constraint for minimizing
	cost_c = [cost== sum(IntSort().cast(X[i][j]) for i in range(maxx) for j in range(maxy) )]

	#s = Solver()
	opt = Optimize()

	#Adding constraint to  solver
	opt.add( uniq_c + cells_c + cost_c + conn_c)
	#minimizing cost/length
	h=opt.minimize(cost)

	if opt.check() == sat:
	   m = opt.model()
	   r = [ [ m.evaluate(X[i][j]) for j in range(maxy) ]
	         for i in range(maxx) ]
	    print_matrix(r)
	   
	   # print(m.evaluate(cost))
	   print "Net ========================= Completed" 
	   return m.evaluate(cost)
	else:
	    print "failed to solve"
	    return -1
def main():
	#net is the list of points of the tree
	net = [[2,3], [5,8], [9,8]]
	m = createSolution(net)
	print m

if __name__ == '__main__':
   main()
