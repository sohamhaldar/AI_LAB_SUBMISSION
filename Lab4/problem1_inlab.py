import random
import math
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple

# Function to calculate the total distance of a tour
def total_distance(tour: List[int], distances: np.ndarray) -> float:
    return sum(distances[tour[i - 1], tour[i]] for i in range(len(tour)))

# Function to generate a random initial tour
def initial_tour(num_cities: int) -> List[int]:
    tour = list(range(num_cities))
    random.shuffle(tour)
    return tour

# Function to generate a neighboring solution by swapping two cities
def perturb_tour(tour: List[int]) -> List[int]:
    new_tour = tour[:]
    i, j = sorted(random.sample(range(len(new_tour)), 2))
    new_tour[i:j + 1] = reversed(new_tour[i:j + 1])
    return new_tour

# Simulated annealing algorithm
def simulated_annealing(distances: np.ndarray, max_iterations: int, initial_temperature: float, cooling_rate: float) -> Tuple[List[int], float]:
    num_cities = len(distances)
    current_tour = initial_tour(num_cities)
    current_distance = total_distance(current_tour, distances)
    best_tour = current_tour[:]
    best_distance = current_distance

    temperature = initial_temperature

    for iteration in range(max_iterations):
        new_tour = perturb_tour(current_tour)
        new_distance = total_distance(new_tour, distances)

        # Calculate acceptance probability
        if new_distance < current_distance or random.random() < math.exp((current_distance - new_distance) / temperature):
            current_tour, current_distance = new_tour, new_distance

            # Update the best tour if needed
            if current_distance < best_distance:
                best_tour, best_distance = current_tour[:], current_distance

        # Cool down the temperature
        temperature *= cooling_rate

    return best_tour, best_distance

# Example distance matrix
distances = np.array([
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
])

max_iterations = 10000
initial_temperature = 100.0
cooling_rate = 0.90

# Perform simulated annealing
best_tour, best_distance = simulated_annealing(
    distances, max_iterations, initial_temperature, cooling_rate
)

# Visualization
cities = len(distances)
x = np.random.rand(cities) * 100
y = np.random.rand(cities) * 100

plt.figure(figsize=(8, 6))
plt.scatter(x, y, c='blue', s=100)
for i in range(cities):
    plt.annotate(i, (x[i], y[i]), fontsize=12)

# Plotting the best tour
for i in range(cities):
    plt.plot([x[best_tour[i]], x[best_tour[(i + 1) % cities]]],
             [y[best_tour[i]], y[best_tour[(i + 1) % cities]]], c='red')

plt.title("Traveling Salesman Problem - Best Tour")
plt.xlabel("X-coordinate")
plt.ylabel("Y-coordinate")
plt.grid(True)
plt.show()

print("Best Tour:", best_tour)
print("Best Distance:", best_distance)
