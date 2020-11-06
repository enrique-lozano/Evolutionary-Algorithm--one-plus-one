import requests
from random import randint, uniform,random
import numpy as np

# ----------PARAMETERS-------------

website = "http://163.117.164.219/age/robot4?"
numMotores = 4

# To initialize the variances vector
minVariance = 0
maxVariance = 90

# If the variances increase, solutions are being obtained every better times and at some point the optimal
cd = 0.82 
ci = 1.18 

# ----------FUNCTIONS-------------

def inizialization(coefficients, variances):  
    for i in range(numMotores):
        coefficients.append(uniform(-180, 180))
        variances.append(uniform(minVariance, maxVariance))

def coef_mutation(coefficients, variances):
    new_coefficients = []
    for i in range(numMotores):
        normal = np.random.normal(0,variances[i])
        new_coefficients.append(coefficients[i] + normal)
    return new_coefficients

def var_mutation(variances, lastIterations):
    new_variances = []


def evaluation(lastIterations):  
    aux = "c1=" + str(coefficients[0]) + "&c2=" + str(coefficients[1]) + "&c3=" + str(coefficients[2]) + "&c4=" + str(coefficients[3])
    r = requests.get(website + aux)
    print("Fitness value: " + str(r.text))

    # If improve
    if float(r.text) < lastIterations[0]:
        lastIterations[0] = float(r.text)
        if len(lastIterations[1]) < 10:
            lastIterations[1].append(1)
        else:
            lastIterations[1].append(1)
            lastIterations[1].pop(0) # Delete the oldest position
    
    # If not improve
    if float(r.text) > lastIterations[0]:
        if len(lastIterations[1]) < 10:
            lastIterations[1].append(0)
        else:
            lastIterations[1].append(0)
            lastIterations[1].pop(0) # Delete the oldest position
    return lastIterations

# -------------CODE----------------

coefficients = []
variances = []
lastIterations = [99999999, []] # [minFitness, [lastIterations]]. 0 not improve, 1 improve

inizialization(coefficients, variances)

for i in range(15):
    print("-----------------------------")
    print("-----------------------------")
    print("Coef. ->" + str(coefficients))
    print("Var. ->" + str(variances))

    coefficients = coef_mutation(coefficients,variances)
    lastIterations = evaluation(lastIterations)
    print(lastIterations)
    