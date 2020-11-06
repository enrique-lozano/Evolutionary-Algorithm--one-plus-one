import requests
from random import randint, uniform,random
import numpy as np

numMotores = 4
maxVariance = 90

'''No entiendo como implementar la distribución normal para la mutación de la parte funcional seria con numpy.random.normal (𝜎) para cada rotor?
'''

def inizialization(coefficients, variances):  

    for i in range(numMotores):
        coefficients.append(uniform(-180, 180))
        variances.append(maxVariance)

def mutation(coefficients, variances):
    new_coefficients = []
    new_variances = []
    for i in range(numMotores):
        normal = np.random.normal(0,variances[i])
        print(normal)
        new_coefficients.append(coefficients[i] + normal)
    return new_coefficients


coefficients = []
variances = []

inizialization(coefficients, variances)
print("Coef. ->" + str(coefficients))
print("Var. ->" + str(variances))
coefficients = mutation(coefficients,variances)
print(str(coefficients))


website = "http://163.117.164.219/age/robot4?"

aux = "c1=" + str(coefficients[0]) + "&c2=" + str(coefficients[1]) + "&c3=" + str(coefficients[2]) + "&c4=" + str(coefficients[3])
r = requests.get(website + aux)
print(r.text)

