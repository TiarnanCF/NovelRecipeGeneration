#Function to run through layer G of the graph for recipes of length L for a chosen gamma
def recipeLenDist(G,L,iterNo,gamma):
    lengthDist = []
    for j in range(iterNo):
        x = rdmWalkPort(G,np.random.choice(G.number_of_nodes()),L,gamma)
        #if len(set(x)) > 1:
        lengthDist.append(len(set(x)))
    return lengthDist

#Variables to change in order to match histogram to preferred region
gamma = 0.1
length = 30
region = 5
#Run function
lengthDist = recipeLenDist(Gnew[region],length,10000,gamma)
#Plot results
plt.hist(ingDist[newRegionList[region]],len(set(ingDist[newRegionList[region]])), density=True, facecolor='b', alpha=0.5,label='True Distribution')
plt.hist(lengthDist, len(set(lengthDist)), density=True, facecolor='r', alpha=0.5,label='Distribution')
plt.xlabel('Recipe Ingredient List Length', fontsize=16)
plt.ylabel('Probability', fontsize=16)
plt.title('Historgram showing the Distribution of Number of\nUnique Nodes Visited over 10,000 Random Walks\nof length ' + str(length) + ' with $\gamma$ =' + str(gamma), fontsize=20)
plt.legend(prop={"size":16})
plt.savefig('..\Plots\lenDist' + str(region) + '_' + str(gamma) + '_' + str(length) + '.png',bbox_inches='tight')
plt.show()