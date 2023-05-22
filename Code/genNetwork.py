#Loading in required modules
import pandas as pd
import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
import math

#Load in CulinaryDB database
recipeDetails = pd.read_csv(filepath_or_buffer='./Data/01_Recipe_Details.csv', sep=',', encoding='latin')
ing = pd.read_csv(filepath_or_buffer='./Data/02_Ingredients.csv', sep=',', encoding='latin')
compIng = pd.read_csv(filepath_or_buffer='./Data/03_Compound_Ingredients.csv', sep=',', encoding='latin')
recipeIng = pd.read_csv(filepath_or_buffer='./Data/04_Recipe-Ingredients_Aliases.csv', sep=',', encoding='latin')

#Record number of ingredients (compound and simple)
ingShape = ing.shape
compIngShape = compIng.shape
totIng = ingShape[0] + compIngShape[0]

#Record Number of Regions
regionList = np.unique(recipeDetails['Cuisine'].values.tolist())
regions = regionList.shape[0]

#Quick map from region name to layer of matrix
areaCode = {}
for i in range(regions):
    areaCode[regionList[i]] = i
    
#Quick map from ingredient code to node number
ingCode = {}
ingredients = ing['Entity ID']
for i in range(ingShape[0]):
    ingCode[ingredients[i]] = i
ingredientsComp = compIng['entity_id']
for i in range(compIngShape[0]):
    ingCode[ingredientsComp[i]] = ingShape[0] + i
    
#Quick map from node number to ingredient name
labels = {}
for j in range(totIng):
    if (j < 930):
        labels[j] = ing['Aliased Ingredient Name'][j]
    else:
        labels[j] = compIng['Compound Ingredient Name'][j-930]

#Create adjacency matrix for each region
adjMx = []
for i in range(regions):
    adjMx.append(np.zeros([totIng,totIng]))

#Store dist of ingredient list length
ingDist = []
for i in range(regions):
    ingDist.append([])
    
#Record number of recipes and length of ingredient file
fileLength = recipeIng.shape[0]
recipeCount = recipeDetails.shape[0]
startPoint = 0;

#Iterate through each recipe
for i in range(recipeCount):
    #Find which ingredients are in the recipe
    ingredientList = []
    ingLength = 0;
    while (recipeIng.iloc[startPoint,0] == i+1):
        #Add ingredient to ingredient list and update number of ingredients
        ingredientList.append(ingCode[recipeIng.iloc[startPoint,3]])
        startPoint = startPoint + 1
        ingLength = ingLength + 1
        #Stop once we are at a new recipe
        if (startPoint == fileLength):
            break
    #Check region
    region = areaCode[recipeDetails.iloc[i,3]]
    
    #Add recipe ingredient list length to distribution
    ingDist[region].append(ingLength)
    
    #For each ingredient add one to frequency of occurrence together in adj mx
    count = len(ingredientList)
    for j in range(count):
        for k in range(count):
            adjMx[region][ingredientList[j]][ingredientList[k]] += 1

G = [] #List of graphs

#Create Weights
for i in range(regions):
    #Remove all self-loops
    for j in range(totIng):
        adjMx[i][j][j] = 0
    
    #Create Weighted graph
    G.append(nx.from_numpy_matrix(adjMx[i]))
        
#Save Properly for MATLAB WSBM code
for i in range(len(G)):
    A = nx.adjacency_matrix(G[i])
    np.savetxt(".\\adjMx\\adjMx" + str(i) + ".txt", A.todense(),delimiter= " ")