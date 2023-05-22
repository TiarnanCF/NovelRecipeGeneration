#Modified Random Walk Proposed
def modRdmWalkPort(G,region,x0,maxIng,gamma,delta):
    #x is an ingredient list
    x = [x0]
    
    #storing info on nerby ingredients as well as weights of edges for each ingredient in list x
    ing = [[] for _ in range(len(G))]
    weight = [[] for _ in range(len(G))]
    total = [[] for _ in range(len(G))]
    invWeight = [[] for _ in range(len(G))]
    
    #Adding ingredients to our list
    for i in range(maxIng-1):
        
        #Deciding whether to choose randomly, change region or just pick an ingredient
        choice = np.random.choice([0,1,2],p=[gamma,delta, 1-gamma-delta])
        
        #For the new ingredient added we have to store the information found
        for j in range(len(G)):
            #Getting adjacent ingredient and edge weight info for region j
            nextIng = []
            nextWeight = []
            for u,v,w in G[j].edges(x[i],data=True):
                nextWeight.append(w['weight'])
                nextIng.append(v)
           
            #Storing all information 
            total[j].append(sum(nextWeight))
            ing[j].append(nextIng)
            weight[j].append(nextWeight)
            
            #Storing inverted total weight (making sure to account for when the weight sums to zero)
            if (total[j][i] < pow(10,-6)):
                invWeight[j].append(0)
            else:
                invWeight[j].append(1/total[j][i])
        
        #Updating region (if applicable)
        if choice == 1:
            newRegion = np.random.choice(range(len(G)-1))
            if newRegion < region:
                region = newRegion
            else:
                region = newRegion +1
        
        if choice == 0:
            #Choosing random ingredient if applicable
            x.append(np.random.choice(G[region].nodes()))
        else:
            #Summing all inverted weights
            totInvWeight = sum(invWeight[region])
            if totInvWeight == 0:
                x.append(np.random.choice(G[region].nodes()))
            else:
                #Picking an ingredient from list x with probability proportional to inverse of
                #sum of weights on edges leaving it
                prob = [w/totInvWeight for w in invWeight[region]]
                j = np.random.choice(range(len(x)),p=prob)

                #Picking ingredient neighbouring our chosen ingredient from list x
                newIng = np.random.choice(ing[region][j],p=[w/total[region][j] for w in weight[region][j]])
                x.append(newIng)
            
    return x

#Random Walk for a single layer
def rdmWalkPort(G,x0,maxIng,gamma):
    return modRdmWalkPort([G],0,x0,maxIng,gamma,0)