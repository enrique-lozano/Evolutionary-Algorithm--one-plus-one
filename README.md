# Evolutionary strategies ♻️📈

This project develops 3 simple evolutionary algorithms, from the branch of evolutionary strategies (https://en.wikipedia.org/wiki/Evolution_strategy). These algorithms are:

-   1+1
-   (µ,λ)
-   (µ+λ)

Don't worry! we'll explain how the algorithms work in later sections. The final objective of the problem is to find the correct degree of inclination of a number X of motors, to carry out a certain task. This degree of inclination is a continuous number between -180 and 180 degrees.

## Run it 🚀

### Pre-requistes ⛔

First of all, make sure you have python installed, in version 3. For more information on this, visit the docs at https://www.python.org/

You will need to install some dependencies via pip, entering the following commands in the root folder of the project:

```sh
pip install requests
```

```sh
pip install numpy
```

### Usage example 💡

Just run in the terminal:

```sh
python script.py
```

In Linux or MacOS, you might have to type instead:

```sh
python3 script.py
```

The "script.py" should be replaced for one of this:

-   1+1.py
-   Mu+Lamda.py
-   MuLamda.py

Once the command is entered, the execution of the script will begin, which will perform the specified algorithm 5 times. The results of these five iterations will appear in the **results.txt files**.

**Warning:** _This project has been fully developed in python 3.7, so its operation for previous versions is not guaranteed._

## What are these algorithms? 🧠

As a general rule, these algorithms have one or more individuals, made up of two main components. The first is a **vector of coefficients** (known as X), which will represent the values ​​that we want to optimize, the solution to seek (in this case, the orientation of the motors). The second is a **vector of variances** (known as σ) with the same size as the first one, which will help us to mutate the individual, so that each iteration is usually better than the previous one.

> To measure the performance of the vector of coefficients we call an external server, which will return a value, known as **fitness**. The lower this value, the better the performance of the vector of coefficients, being 0 when it's optimal.

### 1+1 Algorithm

Here the population of each iteration is made up of **a single individual**. The vector of coefficients mutates following the following formula:

<img src="/screenshots/sc1.PNG" alt="Screenshot 1" width="20%" height="20%" />

_Where N(σ) is the gaussian distribution with a SD of σ (See http://onlinestatbook.com/2/calculators/normal_dist.html)._

The variances vector mutates according to the 1/5 rule. For this rule, we define a constant ψ that denotes the percentage of times that the individual has improved in the last X iterations and a constant c<1. So if ψ<1/5 the new variances are the old variances multiplied by the constant c. If ψ>1/5 the new variances are the old variances divided by the constant c.

Only the individual with the best fitness will access the next iteration, between the new X2 and the old x1.

### Algorithms (µ,λ) and (µ+λ)

In these algorithms we have multiple individuals in each iteration. The 1/5 rule is not used for the variances, instead we use:

<img src="/screenshots/sc2.PNG" alt="Screenshot 2" width="20%" height="20%" />

_Where T is equal to b/√(2N), being b a constant near 1.00 and N the size of the vectors_

So, we generate new individuals in this way:

-   **First step:** We select parents with a probability proportional to their performance (fitness).
-   **Second step:** We calculate the mean of all the coefficients of the parents and select one random variance of the vectors of the parents.
-   **Third step:** We apply the mutation of the coefficients with the same formula as in 1+1 and the mutation of the variances with the previous formula.

Example:

> In the **first step** we get the parents I1=[X=(20,30,50,120) σ=(120,130,63,14.6)] and I2=[X=(40,30,60,10) σ=(43.65,32,62,100)]

> **Second step:** The new individual will be: I3=[X=(30,30,55,65) σ=(43.65,130,63,100)]

> **Third step:** We mutate the new individual, so X1 will be X1+N(σ1) and σ1 will be σ1*(e^N(b/√(2*8)). The same with X2, X3 and X4 and their variances.

**We do that process λ times, generating λ new individuals starting from µ individuals** (population size).

### So, what's the difference between the two algorithms?

-   In (µ,λ) a replacement per **insertion** is performed in each iteration, that is, the new λ individuals always pass to the new population, replacing the worst µ individuals.
-   In (µ+λ) a replacement per **inclusion** is performed in each iteration, that is, the new λ individuals compete with the old µ individuals for being in the new population.

## Issues 🤕

This project depends on the operation of an external server, which may be unavailable at the time of execution.

## Want to collaborate? 🙋🏻

Feel free to improve and optimize the existing code. To contribute to the project, read the previous points carefully and do the next steps with the project:

1. Fork it.
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## Need help ❓

Feel free to contact the developer if you have any questions or suggestions about the project or how you can help with it.
