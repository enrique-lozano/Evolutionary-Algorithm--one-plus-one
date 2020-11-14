import requests
from random import randint, uniform,random
import numpy as np
import random
import math


# ----------PARAMETERS-------------

website = "http://163.117.164.219/age/robot4?"
numMotores = 4

# To initialize the variances vector
minVariance = 60
maxVariance = 180

sizePopulation = 4  # Size of the population
lambdaValue = 3     # Number of individuals that will change in the next population
b = 1               # To do the mutation in the variances

# ----------FUNCTIONS-------------

def print_population(all_data):
    for i in range(sizePopulation):
        prob = float("{:.3f}".format(all_data[i][3]))
        print("")
        print("Ind. " + str(i) + ": Coefficents:" + str(all_data[i][0]) + ". Variances:" + str(all_data[i][1]) + "---> FITNESS: " + str(all_data[i][2]) + " (prob=" + str(prob) + ")")

def population_inizialization(population, population_variances):
    for i in range(sizePopulation):
        aux_population = []
        aux_variances = []
        individual_initialization(aux_population, aux_variances)
        population.append(aux_population)
        population_variances.append(aux_variances)
    
def individual_initialization(coefficients, variances):  
    for i in range(numMotores):
        coefficients.append(uniform(-180, 180))
        variances.append(uniform(minVariance, maxVariance))

def population_evaluation(population):
    population_fitness = []
    for x in range(sizePopulation):
        population_fitness.append(individual_evaluation(population[x]))
    return population_fitness

def individual_evaluation(coefficients):  
    aux = "c1=" + str(coefficients[0]) + "&c2=" + str(coefficients[1]) + "&c3=" + str(coefficients[2]) + "&c4=" + str(coefficients[3])
    r = requests.get(website + aux)
    return float(r.text)

def genera_ruleta(population, fitness):
    # lower values generate higher probabilities. That's why we do 1/fitness
    total_fitness = 0
    for i in range(sizePopulation):
        total_fitness = total_fitness + 1/fitness[i]    
    
    probabilities = []
    for i in range(sizePopulation):
        prob = (1/fitness[i])/total_fitness
        probabilities.append( prob )        
    return probabilities

    
def reproduccion(all_data):
    
    new_population = []
    new_population_variances = []

    for i in range(lambdaValue):

        parents = random.choices(all_data, probabilities, k=2) # Two parents: parents[0] & parents[1]
        # Puede que el mejor individuo sea seleccionado

        son_coefficients = []
        son_variances = []

        for i in range(numMotores): #CRUCE
            # Mean of parental coefficients
            son_coefficients.append((parents[0][0][i]+parents[1][0][i])/2)

            # Random choice between the variances of the parents
            son_variances.append(random.choice([parents[0][1][i],parents[1][1][i]]))

        # MUTACION
        son_coefficients = coef_mutation(son_coefficients, son_variances)
        son_variances = var_mutation(son_variances)

        new_population.append(son_coefficients)  
        new_population_variances.append(son_variances)   
    
    return new_population, new_population_variances

def coef_mutation(coefficients, variances):
    new_coefficients = []
    for i in range(numMotores):
        normal = np.random.normal(0,variances[i])
        new_coefficients.append(coefficients[i] + normal)
    return new_coefficients

def var_mutation(variances):
    new_variances = []
    for i in range(numMotores):
        t = b/math.sqrt(2*math.sqrt(numMotores))
        normal = np.random.normal(0,t)
        new_variances.append(variances[i] * math.exp(normal))

    return new_variances

def sortKey(e):
  return e[2]


# -------------CODE----------------

population = []             # Coefficents of the population
population_variances = []   # Variances of the population
fitness = []                # Fitness of the population
probabilities = []          # Probability of be a parent

population_inizialization(population, population_variances)

doc_results = open("MuLamdaResults.txt","a")
min_fitness = 9999999
rounds_without_improve = 0

for round in range(200000):
    print("--------------------------------------------------------------")
    print("---------------------STARTING ROUND " + str(round) + "--------------------------")
    print("--------------------------------------------------------------")
    fitness = population_evaluation(population)
    probabilities = genera_ruleta(population,fitness)

    all_data = []                        # [[[coef],[var],fitness,prob],[[coef],[var],fitness,prob],...]
    for i in range(sizePopulation):
        all_data.append([])               
        all_data[i].append(population[i])
        all_data[i].append(population_variances[i])
        all_data[i].append(fitness[i])
        all_data[i].append(probabilities[i])

    all_data.sort(key=sortKey)
    probabilities.sort(reverse=True)
    print("La mejor evaluación es: " + str(all_data[0][2]))
    print("Rounds without improve: " + str(rounds_without_improve))
    print("--------------------------------------------------------------")

    if all_data[0][2] < min_fitness:
        rounds_without_improve = 0
        min_fitness = all_data[0][2]
    else:
        rounds_without_improve += 1
    
    if rounds_without_improve>50 and round>100:
        break
    
    doc_results.write(str(round) + " " + str(all_data[0][2]) + "\n")

    print_population(all_data)

    intermedia, intermedia_varianzas = reproduccion(all_data)
    
    for i in range(lambdaValue):
        all_data[len(all_data) - 1 - i][0] = intermedia[i]
        all_data[len(all_data) - 1 - i][1] = intermedia_varianzas[i]
    
    for i in range(sizePopulation):
        population[i] = all_data[i][0]
        population_variances[i] = all_data[i][1]

doc_results.close()