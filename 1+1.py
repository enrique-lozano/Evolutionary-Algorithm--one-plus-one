import requests
from random import randint, uniform,random
import numpy as np

# ----------PARAMETERS-------------

website = "http://163.117.164.219/age/robot4?"
numMotors = 4

# To initialize the variances vector
minVariance = 60
maxVariance = 180

# If the variances increase, solutions are being obtained every better times and at some point the optimal
c = 0.82 

# Iterations to compute the improve ratio
ItImproveRatio = 10

# ----------FUNCTIONS-------------

def inizialization(coefficients, variances):  
    for i in range(numMotors):
        coefficients.append(uniform(-180, 180))
        variances.append(uniform(minVariance, maxVariance))

def coef_mutation(coefficients, variances):
    new_coefficients = []
    for i in range(numMotors):
        normal = np.random.normal(0,variances[i])
        #print(normal)
        new_coefficients.append(coefficients[i] + normal)
    return new_coefficients

def var_mutation(variances, lastIterations):
    new_variances = variances
    improveRatio = 0
    for i in lastIterations:
        improveRatio = improveRatio + i
    improveRatio = improveRatio / len(lastIterations)
    print("Improve ratio of the last "  + str(ItImproveRatio) + " rounds: " + str(improveRatio))

    for i in range(numMotors):
        if improveRatio<0.2:
            new_variances[i] = variances[i] * c
        if improveRatio>0.2:
            new_variances[i] = variances[i] / c
    
    return new_variances

def evaluation(coefficients):  
    aux = "c1=" + str(coefficients[0]) + "&c2=" + str(coefficients[1]) + "&c3=" + str(coefficients[2]) + "&c4=" + str(coefficients[3])
    done = False
    while (not done):
        try:
            r = requests.get(website + aux)
            done = True
        except:
            print("Waiting for the server.................")
    return float(r.text)

def addIteration(fitness1, fitness2):
    # If improve
    if fitness2 < fitness1:
        if len(lastIterations) < ItImproveRatio:
            lastIterations.append(1)
        else:
            lastIterations.append(1)
            lastIterations.pop(0) # Delete the oldest position
    
    # If not improve
    if fitness2 > fitness1:
        if len(lastIterations) < ItImproveRatio:
            lastIterations.append(0)
        else:
            lastIterations.append(0)
            lastIterations.pop(0) # Delete the oldest position
    return lastIterations

# -------------CODE----------------

for i in range(5):
    coefficients = []
    variances = []
    lastIterations = [] # 0 not improve, 1 improve

    inizialization(coefficients, variances)
    fitness1 = evaluation(coefficients) # Minimum value of fitness always in fitness1

    doc_results = open("1+1results.txt","a")

    for i in range(1000):
        print("-----------------------------")
        print("-----------------------------")
        print("Coef. ->" + str(coefficients))
        print("Var. ->" + str(variances))

        totalVariances = 0
        for var in variances:
            totalVariances = totalVariances + var
        if totalVariances<0.005:
            break

        new_coefficients = coef_mutation(coefficients,variances)
        fitness2 = evaluation(new_coefficients)
        lastIterations = addIteration(fitness1, fitness2)
        #print("Fitness1 value: " + str(fitness1))
        #print("Fitness2 value: " + str(fitness2))
        if fitness2 < fitness1:
            coefficients = new_coefficients
            #print("New coefficients vector....")
            fitness1 = fitness2
        variances = var_mutation(variances, lastIterations)
        print(lastIterations)

        doc_results.write(str(i) + "   " + str(fitness1) + "\n")
    
    doc_results.write("\n")    
    doc_results.close()
    print("-----------------------------")
    print("-----------FINISH------------")
    print("--Final value: " + str(fitness1) + "--")
    print("-----------------------------")