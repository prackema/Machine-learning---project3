import matplotlib.pyplot as plt
import random

def geno_to_pheno(individuals):
    return [int("".join(map(str, individual)), 2) for individual in individuals]
def pheno_to_geno(x_values):
    return [[int(bit) for bit in format(x_value, '06b')] for x_value in x_values]

def initialization_population(pop_size):
    """Create initial population of 6-bit individuals (list of lists)."""
    population = [[random.randint(0, 1) for _ in range(6)] for _ in range(pop_size)]
    return population

population = initialization_population(4)
print(population)
print("Type of output:", type(population))
print("Type of one individual:", type(population[0]))

def fitness(individuals):
    """Calculate fitness values for given individuals."""
    phenotypes = geno_to_pheno(individuals)
    for x in phenotypes:
        if x >= 32:
            x -= 64
        else:
            x = x
        fitness_values = -0.00008333 * x ** 6 - 0.001 * x ** 5 + 0.09375 * x ** 4 + 1.16667 * x ** 3 - 19.53125 * x ** 2 - 234.375 * x + 8350
    return fitness_values
# 12620.97
value = fitness([[0, 1, 0, 1, 0, 1]])
print("Fitness value for individual [0, 1, 0, 1, 0, 1]:", value)

# Plotting the fitness landscape
x_values = list(range(64))
y_values = [fitness([[int(bit) for bit in format(x, '06b')]]) for x in x_values]

plt.plot(x_values, y_values)
plt.xlabel("Phenotype (Integer Value)")
plt.ylabel("Fitness")
plt.title("Fitness Landscape")
plt.grid()
plt.show()

# Finding min and max fitness values
min_fitness = min(y_values)
max_fitness = max(y_values)
min_x = x_values[y_values.index(min_fitness)]
max_x = x_values[y_values.index(max_fitness)]

print(f"Minimum fitness value: {min_fitness} (at x = {min_x})")
print(f"Maximum fitness value: {max_fitness} (at x = {max_x})")

