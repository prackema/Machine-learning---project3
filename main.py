import matplotlib.pyplot as plt
import random
import os
import csv
import statistics
import math

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
    

#---------------------------------------Task 2--------------------------------------------------

#Setup / Random seed

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
path = "data_1001.csv"
print(os.path.exists(path))

# Load data

def load_knapsack_data(csv_path):
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"File '{csv_path}' not found.")

    values, weights = [], []
    with open(csv_path, newline='') as f:
        reader = csv.reader(f)
        first_row = next(reader)

        def is_number(s):
            try:
                float(s)
                return True
            except:
                return False

        # Skip header if present
        if is_number(first_row[0]):
            values.append(float(first_row[0]))
            weights.append(float(first_row[1]))
        for row in reader:
            if len(row) < 2:
                continue
            values.append(float(row[0]))
            weights.append(float(row[1]))
    return values, weights


# Data exploration (EDA)

def analyze_items(values, weights, top_n=10):
    n = len(values)
    stats = {
        "n_items": n,
        "value_min": min(values),
        "value_max": max(values),
        "value_mean": statistics.mean(values),
        "value_median": statistics.median(values),
        "weight_min": min(weights),
        "weight_max": max(weights),
        "weight_mean": statistics.mean(weights),
        "weight_median": statistics.median(weights),
    }

    # Pearson correlation between value and weight
    try:
        mean_v, mean_w = stats["value_mean"], stats["weight_mean"]
        cov = sum((v - mean_v) * (w - mean_w) for v, w in zip(values, weights)) / (n - 1)
        std_v, std_w = statistics.pstdev(values), statistics.pstdev(weights)
        pearson = cov / (std_v * std_w) if std_v > 0 and std_w > 0 else float('nan')
    except Exception:
        pearson = float('nan')
    stats["value_weight_pearson"] = pearson

    # Top N items by value/weight ratio
    ratio = [(i, v / w if w != 0 else float('inf')) for i, (v, w) in enumerate(zip(values, weights))]
    ratio_sorted = sorted(ratio, key=lambda x: x[1], reverse=True)
    stats["top_ratio_indices"] = [i for i, _ in ratio_sorted[:top_n]]

    return stats


#  SGA components

def init_knapsack_population(pop_size, n_items):
   #Create an initial population of random binary vectors
    return [[random.randint(0, 1) for _ in range(n_items)] for _ in range(pop_size)]

def fitness_knapsack(individuals, item_values):
    #Compute total value for each individual
    fitness_values = []
    for ind in individuals:
        if len(ind) != len(item_values):
            raise ValueError("Individual length does not match number of items.")
        s = sum(v for bit, v in zip(ind, item_values) if bit == 1)
        fitness_values.append(s)
    return fitness_values

def parent_selection(individuals, fitness_values):
    #Roulette-wheel selection (fitness-proportional)
    total = sum(fitness_values)
    if total == 0:
        return [random.choice(individuals) for _ in range(len(individuals))]
    selected = random.choices(individuals, weights=fitness_values, k=len(individuals))
    return [p[:] for p in selected]

def one_point_crossover(parents, pc):
    #One-point crossover on pairs of parents
    offspring = []
    n = len(parents)
    if n % 2 == 1:
        parents.append(random.choice(parents))
        n += 1
    for i in range(0, n, 2):
        p1, p2 = parents[i][:], parents[i+1][:]
        if random.random() <= pc:
            point = random.randint(1, len(p1) - 1)
            c1 = p1[:point] + p2[point:]
            c2 = p2[:point] + p1[point:]
            offspring.extend([c1, c2])
        else:
            offspring.extend([p1, p2])
    return offspring[:len(parents)]

def mutation(individual, pm):
    #Bit-flip mutation with probability pm per bit.
    ind = individual[:]
    for i in range(len(ind)):
        if random.random() <= pm:
            ind[i] = 1 - ind[i]
    return ind

def survivor_selection(old_pop, offspring, fitness_old, fitness_off):
    #Deterministic survivor selection: keep the best individuals
    combined = old_pop + offspring
    combined_fit = fitness_old + fitness_off
    paired = list(zip(combined, combined_fit))
    paired.sort(key=lambda x: x[1], reverse=True)
    return [ind for ind, _ in paired[:len(old_pop)]]


#  Full SGA loop

def complete_sga_knapsack(item_values, pop_size=30, iterations=1000, pc=0.9, pm=0.1, verbose=True):
    n_items = len(item_values)
    population = init_knapsack_population(pop_size, n_items)

    avg_history, best_history = [], []

    for gen in range(iterations):
        fitness_pop = fitness_knapsack(population, item_values)
        avg_f, best_f = sum(fitness_pop)/len(fitness_pop), max(fitness_pop)
        avg_history.append(avg_f)
        best_history.append(best_f)

        if verbose and ((gen < 10) or ((gen+1) % 100 == 0) or (gen == iterations-1)):
            print(f"Gen {gen+1:4d} | Best: {best_f:.2f} | Avg: {avg_f:.2f}")

        parents = parent_selection(population, fitness_pop)
        offspring = one_point_crossover(parents, pc)
        offspring = [mutation(child, pm) for child in offspring]
        fitness_off = fitness_knapsack(offspring, item_values)
        population = survivor_selection(population, offspring, fitness_pop, fitness_off)

    final_fit = fitness_knapsack(population, item_values)
    best_idx = final_fit.index(max(final_fit))
    return {
        "final_population": population,
        "final_fitness": final_fit,
        "best_individual": population[best_idx],
        "best_value": final_fit[best_idx],
        "avg_history": avg_history,
        "best_history": best_history
    }


#  Summarize final solution

def summarize_solution(individual, item_values, item_weights):
    selected = [i for i, bit in enumerate(individual) if bit == 1]
    not_selected = [i for i, bit in enumerate(individual) if bit == 0]

    def stats_for(indices):
        if not indices:
            return {"count": 0}
        vals = [item_values[i] for i in indices]
        wts  = [item_weights[i] for i in indices]
        ratios = [(v / w if w != 0 else float('inf')) for v, w in zip(vals, wts)]
        return {
            "count": len(indices),
            "value_sum": sum(vals),
            "value_min": min(vals), "value_mean": statistics.mean(vals), "value_max": max(vals),
            "weight_min": min(wts), "weight_mean": statistics.mean(wts), "weight_max": max(wts),
            "ratio_min": min(ratios), "ratio_mean": statistics.mean(ratios), "ratio_max": max(ratios)
        }

    return {
        "total_value": sum(item_values[i] for i in selected),
        "n_selected": len(selected),
        "selected_stats": stats_for(selected),
        "not_selected_stats": stats_for(not_selected),
        "selected_indices": selected
    }


# task 2 execution

def task2():
    csv_path = "data_1001.csv" 
    try:
        item_values, item_weights = load_knapsack_data(csv_path)
    except FileNotFoundError as e:
        print(e)
        return

    stats = analyze_items(item_values, item_weights)
    print("\n    DATA SUMMARY   ")
    print(f"Items: {stats['n_items']}")
    print(f"Value  - min: {stats['value_min']:.2f}, mean: {stats['value_mean']:.2f}, max: {stats['value_max']:.2f}")
    print(f"Weight - min: {stats['weight_min']:.2f}, mean: {stats['weight_mean']:.2f}, max: {stats['weight_max']:.2f}")
    print(f"Pearson corr (value vs weight): {stats['value_weight_pearson']:.4f}")
    print(f"Top indices by value/weight ratio: {stats['top_ratio_indices'][:10]}")

    POP_SIZE, ITER, PC, PM = 30, 1000, 0.9, 0.1
    print(f"\nRunning SGA: pop={POP_SIZE}, iter={ITER}, pc={PC}, pm={PM}")
    result = complete_sga_knapsack(item_values, pop_size=POP_SIZE, iterations=ITER, pc=PC, pm=PM)

    # Plot progress
    plt.figure(figsize=(10,5))
    plt.plot(result["best_history"], label="Best Fitness")
    plt.plot(result["avg_history"], label="Average Fitness")
    plt.xlabel("Generation")
    plt.ylabel("Fitness (Total Value)")
    plt.title("SGA Progress — Knapsack Task 2")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Summarize final best solution
    summary = summarize_solution(result["best_individual"], item_values, item_weights)
    print("\n    BEST SOLUTION SUMMARY   ")
    print(f"Total value (fitness): {summary['total_value']:.2f}")
    print(f"Number of selected items: {summary['n_selected']}")

    sel, not_sel = summary["selected_stats"], summary["not_selected_stats"]
    print("\nSelected items:")
    print(f"Values  — count={sel['count']}, sum={sel['value_sum']:.2f}, min={sel['value_min']:.2f}, mean={sel['value_mean']:.2f}, max={sel['value_max']:.2f}")
    print(f"Weights — min={sel['weight_min']:.2f}, mean={sel['weight_mean']:.2f}, max={sel['weight_max']:.2f}")
    print(f"Ratio   — min={sel['ratio_min']:.4f}, mean={sel['ratio_mean']:.4f}, max={sel['ratio_max']:.4f}")

    print("\nNot selected items:")
    print(f"Values  — count={not_sel['count']}, sum={not_sel['value_sum']:.2f}, min={not_sel['value_min']:.2f}, mean={not_sel['value_mean']:.2f}, max={not_sel['value_max']:.2f}")
    print(f"Weights — min={not_sel['weight_min']:.2f}, mean={not_sel['weight_mean']:.2f}, max={not_sel['weight_max']:.2f}")
    print(f"Ratio   — min={not_sel['ratio_min']:.4f}, mean={not_sel['ratio_mean']:.4f}, max={not_sel['ratio_max']:.4f}")

    print("\nIndices of selected items (first 50 shown):", summary["selected_indices"][:50])
    print("\nTask 2 completed.")

if __name__ == "__main__":
   task2()

#------------------------------------task 3------------------------------------------------

#  Data loading (same as Task 2)
#  enforce exact number of ones
def enforce_exact_k(individual, k):
    #Repair individual so that it has exactly k ones
    ones = [i for i, bit in enumerate(individual) if bit == 1]
    zeros = [i for i, bit in enumerate(individual) if bit == 0]

    if len(ones) > k:
        for i in random.sample(ones, len(ones) - k):
            individual[i] = 0
    elif len(ones) < k:
        for i in random.sample(zeros, k - len(ones)):
            individual[i] = 1
    return individual


# Initialization with constraint
def init_knapsack_population_fixed(pop_size, n_items, k):
   
    population = []
    for _ in range(pop_size):
        ind = [0] * n_items
        ones_idx = random.sample(range(n_items), k)
        for i in ones_idx:
            ind[i] = 1
        population.append(ind)
    return population


# Fitness (same as Task 2)
# Parent selection (same as Task 2)

#  Crossover with repair
def one_point_crossover_fixed(parents, pc, k):
    #Same as one-point crossover but ensures each child has exactly k ones
    offspring = []
    n = len(parents)
    if n % 2 == 1:
        parents.append(random.choice(parents))
        n += 1
    for i in range(0, n, 2):
        p1, p2 = parents[i][:], parents[i+1][:]
        if random.random() <= pc:
            point = random.randint(1, len(p1) - 1)
            c1 = p1[:point] + p2[point:]
            c2 = p2[:point] + p1[point:]
        else:
            c1, c2 = p1[:], p2[:]
        offspring.append(enforce_exact_k(c1, k))
        offspring.append(enforce_exact_k(c2, k))
    return offspring[:len(parents)]


# Mutation with repair

def mutation_fixed(individual, pm, k):
    #Bit-flip mutation followed by enforcing exactly k ones
    ind = individual[:]
    for i in range(len(ind)):
        if random.random() <= pm:
            ind[i] = 1 - ind[i]
    return enforce_exact_k(ind, k)

#  Survivor selection (same as Task 2)

#  Full SGA with exact-number constraint

def complete_sga_knapsack_fixed(item_values, pop_size, iterations, pc, pm, k, verbose=True):
    n_items = len(item_values)
    pop = init_knapsack_population_fixed(pop_size, n_items, k)
    avg_hist, best_hist = [], []

    for gen in range(iterations):
        fit_pop = fitness_knapsack(pop, item_values)
        avg_f, best_f = sum(fit_pop) / len(fit_pop), max(fit_pop)
        avg_hist.append(avg_f)
        best_hist.append(best_f)

        if verbose and ((gen < 10) or ((gen + 1) % 100 == 0) or (gen == iterations - 1)):
            print(f"Gen {gen+1:4d} | Best={best_f:.2f} | Avg={avg_f:.2f}")

        parents = parent_selection(pop, fit_pop)
        off = one_point_crossover_fixed(parents, pc, k)
        off = [mutation_fixed(child, pm, k) for child in off]
        fit_off = fitness_knapsack(off, item_values)
        pop = survivor_selection(pop, off, fit_pop, fit_off)

    final_fit = fitness_knapsack(pop, item_values)
    best_idx = final_fit.index(max(final_fit))
    best_ind = pop[best_idx]
    return {
        "best_individual": best_ind,
        "best_value": final_fit[best_idx],
        "avg_history": avg_hist,
        "best_history": best_hist
    }


# Run for multiple K values

def run_task3(csv_path="data_1001.csv"):
    item_values, item_weights = load_knapsack_data(csv_path)
    n_items = len(item_values)

    POP, ITER, PC, PM = 30, 1000, 0.9, 0.1
    K_values = [1001, 802, 400, 100, 10]

    results = []
    for k in K_values:
        print(f"\n Running SGA with exactly {k} items selected")
        res = complete_sga_knapsack_fixed(item_values, pop_size=POP, iterations=ITER,
                                          pc=PC, pm=PM, k=k, verbose=False)
        avg_value_per_item = res["best_value"] / k
        print(f"Best total value: {res['best_value']:.2f} | "
              f"Avg per item: {avg_value_per_item:.2f}")
        results.append((k, res["best_value"], avg_value_per_item))

        # Plot evolution for this K
        plt.figure()
        plt.plot(res["best_history"], label="Best Fitness")
        plt.plot(res["avg_history"], label="Average Fitness")
        plt.xlabel("Generation")
        plt.ylabel("Fitness (Total Value)")
        plt.title(f"SGA Progress (K = {k})")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    # Summary table
    print("\n  SUMMARY ACROSS K VALUES   ")
    print(f"{'K':>8} | {'Best Value':>12} | {'Avg Value per Item':>18}")
    print("-" * 45)
    for k, best_val, avg_val in results:
        print(f"{k:8d} | {best_val:12.2f} | {avg_val:18.2f}")

if __name__ == "__main__":
    run_task3()
