#Construct new graph from MATLAB data
totIng = 1033
Gnew = []

#Load in blockstructure data
thetaE = np.loadtxt(".\params\\thetaE10.txt",delimiter = ",")
thetaW = np.loadtxt(".\params\\thetaW10.txt", delimiter = ",")
z = np.loadtxt(".\params\\z10.txt",dtype =int, delimiter = ",")
newRegionList = np.loadtxt(".\params\\regions10.txt",dtype =int, delimiter = ",")

#Generate each layer
for k in range(int(len(z) / totIng)): 
    Gnew.append(nx.Graph())
    Gnew[k].add_nodes_from(range(totIng))
    for i in range(totIng):
        for j in range(i+1,totIng):
            edge = np.random.random_sample()
            if (edge < thetaE[z[i]-1][z[j]-1]):
                Gnew[k].add_edge(i,j,weight = np.random.poisson(thetaW[z[i]-1][z[j]-1]) + 1)
