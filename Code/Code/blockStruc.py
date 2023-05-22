#Pick layer or "region"
region = 0

#collect nodes by their group
group = [[],[],[],[],[],[],[],[],[],[]]
for i in range(1033):
    group[z[i+1033*region]-1].append(i)
blockStructure = []

#Construct order for nodes based on block structure
for g in group:
    blockStructure = blockStructure + g

#List of all unused nodes
remove = [node for node,degree in dict(G[newRegionList[region]].degree()).items() if degree == 0]

#Default order
defaultStructure = list(range(1033))

#Remove unused nodes from both orders
for i in remove:
    blockStructure.remove(i)
    defaultStructure.remove(i)

#Load both adjacency matrices
adjNew = nx.adjacency_matrix(G[newRegionList[region]], nodelist=blockStructure,weight='weight')
adjOld = nx.adjacency_matrix(G[newRegionList[region]],nodelist=defaultStructure,weight='weight')

#Plot results
fig = plt.figure(figsize=(20,40))

ax1 = fig.add_subplot(121)
ax1.imshow(adjOld.todense(), cmap="copper_r")

ax2 = fig.add_subplot(122)
ax2.imshow(adjNew.todense(), cmap="copper_r")

plt.savefig('block' + str(region) + '10.png',bbox_inches='tight')
plt.show()