# Evolutionary strategies ♻️📈

This project develops 3 simple evolutionary algorithms, from the branch of evolutionary strategies (https://en.wikipedia.org/wiki/Evolution_strategy). These algorithms are:

-   1+1
-   (µ,λ)
-   (µ+λ)

Don't worry! we'll explain how the algorithms work in later sections. The final objective of the problem is to find the correct degree of inclination of a number X of motors, to carry out a certain task. This degree of inclination is a continuous number between -180 and 180 degrees

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

The script.py should be replaced for one of this:

-   1+1.py
-   Mu+Lamda.py
-   MuLamda.py

Once the command is entered, the execution of the script will begin, which will perform the specified algorithm 5 times. The results of these five iterations will appear in the **results.txt files**.

**Warning:** _This project has been fully developed in python 3.7, so its operation for previous versions is not guaranteed_

## What are these algorithms? 🧠

As a general rule, these algorithms have one or more individuals, made up of two main components. The first is a **vector of coefficients**, which will represent the values ​​that we want to optimize, the solution to seek (in this case, the orientation of the motors). The second is a **vector of variances** with the same size as the first one, which will help us to mutate the individual, so that each iteration is usually better than the previous one.

_To measure the performance of the vector of coefficients we call an external server, which will return a value, known as **fitness**. The lower this value, the better the performance of the vector of coefficients, being 0 when it's optimal_

## Issues 🤕

This project depends on the operation of an external server, which may be unavailable at the time of execution.

## Want to collaborate? 🙋🏻

Feel free to improve and optimize the existing code. To contribute to the project, read the previous points carefully and do the next steps with the project:

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## Need help ❓

Feel free to contact the developer if you have any questions or suggestions about the project or how you can help with it.
