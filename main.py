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

# Parent Selection Function
def parent_selection(individuals, fitness_values):
    """Select parents based on fitness-proportional selection."""
    total_fitness = sum(fitness_values)
    probabilities = [f / total_fitness for f in fitness_values]
    selected_parents = random.choices(individuals, weights=probabilities, k=len(individuals))
    return selected_parents

# Testing the Parent Selection Function
test_individuals = [
    [0, 0, 0, 0, 0, 0],  # Minimum fitness
    [1, 1, 1, 1, 1, 1],  # Maximum fitness
    [0, 1, 0, 1, 0, 1],  # Moderate fitness
    [1, 0, 1, 0, 1, 0]   # Moderate fitness
]
test_fitness_values = [min_fitness, max_fitness, 5000, 6000]  # Example fitness values

selected_parents = parent_selection(test_individuals, test_fitness_values)
print("Selected Parents:")
for parent in selected_parents:
    print(parent)

# Recombination (Crossover) Function
def one_point_crossover(parents, pc):
    """Perform one-point crossover on pairs of parents."""
    offspring = []
    for i in range(0, len(parents), 2):
        parent1 = parents[i]
        parent2 = parents[i + 1]
        if random.random() <= pc:
            crossover_point = random.randint(1, len(parent1) - 1)
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]
            offspring.extend([child1, child2])
        else:
            offspring.extend([parent1, parent2])
    return offspring

# Testing the One-Point Crossover Function
parent_a = [1, 1, 1, 1, 1, 1]
parent_b = [0, 0, 0, 0, 0, 0]
parents_for_crossover = [parent_a, parent_b]
crossover_probability = 1.0  # Ensure crossover occurs
offspring = one_point_crossover(parents_for_crossover, crossover_probability)
print("Parents:")
print("Parent A:", parent_a)
print("Parent B:", parent_b)
print("Offspring:")
for child in offspring:
    print(child)

# Mutation Function
def mutation(individual, pm):
    """Perform bitflip mutation on a single individual."""
    mutated_individual = individual[:]
    for i in range(len(mutated_individual)):
        if random.random() <= pm:
            mutated_individual[i] = 1 - mutated_individual[i]  # Flip the bit
    return mutated_individual

# Testing the Mutation Function
original_individual = [0, 1, 1, 0, 1, 0]
mutation_probability_1 = 0.2
mutation_probability_2 = 0.9

mutated_individual_1 = mutation(original_individual, mutation_probability_1)
mutated_individual_2 = mutation(original_individual, mutation_probability_2)

print("Original Individual:", original_individual)
print("Mutated Individual (PM=0.2):", mutated_individual_1)
print("Mutated Individual (PM=0.9):", mutated_individual_2)

def survivor_selection(individuals, offspring, fitness_individuals, fitness_offspring):
    paired = list(zip(individuals + offspring, fitness_individuals + fitness_offspring))
    # Sort by fitness in descending order (highest fitness first)
    paired.sort(key=lambda x: x[1], reverse=True)

    # Select the best 'len(individuals)' survivors (keep population size constant)
    new_population = [ind for ind, fit in paired[:len(individuals)]]

    return new_population

# Example individuals (genotypes)
individuals = ["A1", "A2"]
offspring = ["B1", "B2"]

# Example fitness values
fitness_individuals = [5.0, 3.0]   # A1 = 5.0, A2 = 3.0
fitness_offspring = [4.5, 6.0]     # B1 = 4.5, B2 = 6.0

# Perform survivor selection
new_population = survivor_selection(individuals, offspring, fitness_individuals, fitness_offspring)

print("New population:", new_population)

def complete_sga(pop_size, iterations, pc=0.8, pm=0.1):
    # Initialize population
    individuals = initialization_population(pop_size)

    avg_fitness_history = []
    best_fitness_history = []

    # Repeat for a number of iterations
    for gen in range(iterations):
        # Evaluate current fitness
        fitness_individuals = fitness(individuals)

        avg_fit = sum(fitness_individuals) / len(fitness_individuals)
        best_fit = max(fitness_individuals)

        avg_fitness_history.append(avg_fit)
        best_fitness_history.append(best_fit)

        print(f"Generation {gen+1}: Best = {best_fit:.2f}, Avg = {avg_fit:.2f}")

        # Parent selection
        parents = parent_selection(individuals, fitness_individuals)

        # Crossover
        offspring = one_point_crossover(parents, pc)

        # Mutation
        offspring = [mutation(child, pm) for child in offspring]

        # Evaluate offspring fitness
        fitness_offspring = fitness(offspring)

        # Survivor selection (keep population size constant)
        individuals = survivor_selection(individuals, offspring, fitness_individuals, fitness_offspring)

    # After all generations
    final_fitness = fitness(individuals)
    best_index = final_fitness.index(max(final_fitness))
    best_individual = individuals[best_index]

    print("\nFinal best individual:", best_individual)
    print("Final best fitness:", final_fitness[best_index])

    # Plot fitness trends
    plt.plot(best_fitness_history, label="Best Fitness")
    plt.plot(avg_fitness_history, label="Average Fitness")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.title("SGA Progress")
    plt.legend()
    plt.grid()
    plt.show()
    



