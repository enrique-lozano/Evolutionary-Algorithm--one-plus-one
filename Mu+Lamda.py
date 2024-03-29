import requests
from random import randint, uniform,random
import numpy as np
import random
import math


# ----------PARAMETERS-------------

website = "http://163.117.164.219/age/robot4?"
numMotors = 4

# To initialize the variances vector
minVariance = 100
maxVariance = 180

sizePopulation = 100  # Size of the population
lambdaValue = 30     # Number of individuals that will change in the next population
sizeFamily = 2       # Number of parents to generate new individuals
b = 1               # To do the mutation in the variances
percTournament = 0.3 # Only applies if tournament selected (see reproduction function)


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
    for i in range(numMotors):
        coefficients.append(uniform(-180, 180))
        variances.append(uniform(minVariance, maxVariance))

def population_evaluation(population):
    population_fitness = []
    for x in range(sizePopulation):
        population_fitness.append(individual_evaluation(population[x]))
    return population_fitness

def individual_evaluation(coefficients):  
    aux = "c1=" + str(coefficients[0]) + "&c2=" + str(coefficients[1]) + "&c3=" + str(coefficients[2]) + "&c4=" + str(coefficients[3])
    done = False
    while (not done):
        try:
            r = requests.get(website + aux)
            done = True
        except:
            print("Waiting for the server.................")
    return float(r.text)

def tournament(all_data):
    tournamentSize = math.floor(sizePopulation * percTournament)
    
    new_population = []
    for i in range(sizeFamily):
        participants = random.choices(all_data, k=tournamentSize)
        min = participants[0]

        for participant in participants:
            if int(participant[2]) < int(min[2]):
                min = participant
        new_population.append(min)
    
    return new_population

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

    
def reproduction(all_data):
    
    new_population = []
    new_population_variances = []

    for i in range(lambdaValue):
        # Comment on one of the two lines below: 1-Tournaments. 2-Roulette
        parents = tournament(all_data)
        #parents = random.choices(all_data, probabilities, k=sizeFamily) # k parents: parents[0], parents[1]...
     
        # The best individual could be selected

        son_coefficients = []
        son_variances = []

        for i in range(numMotors): #REPRODUCTION
            sum_coef = 0
            choices = []
            for parent in range(sizeFamily):
                # Mean of parental coefficients
                sum_coef = sum_coef + parents[parent][0][i]

                # Random choice between the variances of the parents
                choices.append(parents[parent][1][i])
                   
            son_coefficients.append(sum_coef/sizeFamily) #Mean
            son_variances.append(random.choice(choices)) #Random choice

        # MUTATION
        son_coefficients = coef_mutation(son_coefficients, son_variances)
        son_variances = var_mutation(son_variances)

        new_population.append(son_coefficients)  
        new_population_variances.append(son_variances)   
    
    return new_population, new_population_variances

def coef_mutation(coefficients, variances):
    new_coefficients = []
    for i in range(numMotors):
        normal = np.random.normal(0,variances[i])
        new_coefficients.append(coefficients[i] + normal)
    return new_coefficients

def var_mutation(variances):
    new_variances = []
    for i in range(numMotors):
        t = b/math.sqrt(2*math.sqrt(numMotors))
        normal = np.random.normal(0,t)
        new_variances.append(variances[i] * math.exp(normal))

    return new_variances

def sortKey(e):
  return e[2]


# -------------CODE----------------

for i in range(5):

    population = []             # Coefficents of the population
    population_variances = []   # Variances of the population
    fitness = []                # Fitness of the population
    probabilities = []          # Probability of be a parent

    population_inizialization(population, population_variances)

    doc_results = open("Mu+LamdaResults.txt","a")
    min_fitness = 9999999
    rounds_without_improve = 0
    fitness = population_evaluation(population)


    for round in range(500):
        print("--------------------------------------------------------------")
        print("---------------------STARTING ROUND " + str(round) + "--------------------------")
        print("--------------------------------------------------------------")
        
        try:
            probabilities = genera_ruleta(population,fitness)
        except:
            print("The best evaluation is: 0")
            break

        all_data = []                        # [[[coef],[var],fitness,prob],[[coef],[var],fitness,prob],...]
        for i in range(sizePopulation):
            all_data.append([])               
            all_data[i].append(population[i])
            all_data[i].append(population_variances[i])
            all_data[i].append(fitness[i])
            all_data[i].append(probabilities[i])

        all_data.sort(key=sortKey)
        probabilities.sort(reverse=True)
        print("The best evaluation is: " + str(all_data[0][2]))
        print("Rounds without improve: " + str(rounds_without_improve))
        print("--------------------------------------------------------------")

        if all_data[0][2] < min_fitness:
            rounds_without_improve = 0
            min_fitness = all_data[0][2]
        else:
            rounds_without_improve += 1
        
        if (rounds_without_improve>50 and round>100) or (all_data[0][2]==0.0):
            break
        
        doc_results.write(str(round) + "   " + str(all_data[0][2]) + "\n")

        #print_population(all_data)

        intermedia, intermedia_varianzas = reproduction(all_data)

        for i in range(lambdaValue):
            all_data.append([])               
            all_data[sizePopulation+i].append(intermedia[i])
            all_data[sizePopulation+i].append(intermedia_varianzas[i])
            all_data[sizePopulation+i].append(individual_evaluation(intermedia[i]))
        all_data.sort(key=sortKey)

        # In inclusion replacement, both parents and children descendants compete to be included in the new population.
        fitness = []
        for i in range(sizePopulation):
            population[i] = all_data[i][0]
            population_variances[i] = all_data[i][1]
            fitness.append(all_data[i][2])

    doc_results.write("\n")
    doc_results.close()