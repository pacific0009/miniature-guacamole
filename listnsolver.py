from z3 import *
import re
wire = 0
def parse (s):
    mo = re.match ("\s*(net[\w]*\d*)\s*(\d*)\s*(\d*)\s*\n", s)
    if mo: return mo.groups ()

def createnetList(netfile):
	filne = netfile	
	netList = []
	count = 0
	#opening file 
	with open(filne, 'r+') as f:

	#iterating lines of file
	    for line in f:
	#Checking/parsing line for net information
	        a = parse(line)
		#if line is a net info line
		if a :
		#net is the list to store all points in a the perticular net
			net = []
			#print "next "+a[1]+" "+a[2]
		#To get each points of the net	
			for i in range(int(a[2])):
				#print f.next();
			#pin coordinates are converted into  is list of number 
				point = [int(n) for n in f.next().split()]
			#pins coordinate list is inserted in to net
				net.insert(i,point)
	#the net list is inserted in to nets list 
			netList.insert(count,net)
			count = count+1
	#print netList          
	#print count
	return netList



def createSolution(netList, num):
	print "Net ============================="+str(num)
	print netList
	maxx = netList[0][0]
	maxy = netList[0][1]
	minx = netList[0][0]
	miny = netList[0][1]

#Setting min and max points
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
	opt.add( uniq_c + cells_c +cost_c+conn_c)
	#minimizing cost/length
	h=opt.minimize(cost)

	if opt.check() == sat:
	   m = opt.model()
	   """r = [ [ m.evaluate(X[i][j]) for j in range(maxy) ]
	         for i in range(maxx) ]
	    print_matrix(r)"""
	   #wire = wire + m.evaluate(cost)
	   # print(m.evaluate(cost))
	   print "Net ========================= Completed" + str(num)
	   return m.evaluate(cost)
	else:
	    print "failed to solve"
	    return -1