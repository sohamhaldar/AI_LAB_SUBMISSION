import random
import math
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple, Dict

# Define the tourist locations in Rajasthan with coordinates
rajasthan_locations: Dict[str, Tuple[float, float]] = {
    "Jaipur": (26.9124, 75.7873),
    "Udaipur": (24.5854, 73.7125),
    "Jodhpur": (26.2389, 73.0243),
    "Pushkar": (26.4897, 74.5511),
    "Jaisalmer": (26.9157, 70.9083),
    "Ajmer": (26.4499, 74.6399),
    "Mount Abu": (24.5925, 72.7156),
    "Bikaner": (28.0229, 73.3119),
    "Ranthambore": (25.8667, 76.3),
    "Chittorgarh": (24.8887, 74.6269),
    "Bundi": (25.4415, 75.6454),
    "Alwar": (27.5530, 76.6346),
    "Bharatpur": (27.1767, 77.6844),
    "Kota": (25.2138, 75.8648),
    "Sawai Madhopur": (25.9928, 76.3526),
    "Shekhawati": (27.7366, 75.9730),
    "Dungarpur": (23.8363, 73.7143),
    "Nathdwara": (24.9339, 73.8226),
    "Mandawa": (28.0556, 75.1419),
    "Osian": (26.9112, 72.3917)
}

# Calculate distance between two locations using the Haversine formula
def haversine_distance(location1: Tuple[float, float], location2: Tuple[float, float]) -> float:
    lat1, lon1 = location1
    lat2, lon2 = location2
    radius = 6371  # Radius of Earth in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius * c

# Calculate total distance of a tour
def total_tour_distance(tour: List[str]) -> float:
    return sum(haversine_distance(rajasthan_locations[tour[i]], rajasthan_locations[tour[(i + 1) % len(tour)]]) for i in range(len(tour)))

# Simulated Annealing algorithm with distance tracking
def simulated_annealing_with_distances(locations: Dict[str, Tuple[float, float]], initial_temperature: float = 1000, cooling_rate: float = 0.99, num_iterations: int = 100000) -> Tuple[List[str], float, List[float]]:
    current_solution = list(locations.keys())
    random.shuffle(current_solution)
    current_cost = total_tour_distance(current_solution)
    best_solution = current_solution[:]
    best_cost = current_cost

    temperature = initial_temperature
    distances = []

    for _ in range(num_iterations):
        # Generate a new solution by swapping two random locations
        new_solution = current_solution[:]
        i, j = random.sample(range(len(new_solution)), 2)
        new_solution[i], new_solution[j] = new_solution[j], new_solution[i]

        # Calculate the cost of the new solution
        new_cost = total_tour_distance(new_solution)

        # Accept the new solution if it's better or by probability
        if new_cost < current_cost or random.random() < math.exp((current_cost - new_cost) / temperature):
            current_solution = new_solution[:]
            current_cost = new_cost

            # Update the best solution if the new solution is better
            if new_cost < best_cost:
                best_solution = new_solution[:]
                best_cost = new_cost

        # Track the cost at each step
        distances.append(current_cost)

        # Cooling schedule
        temperature *= cooling_rate

    # Ensure the tour forms a cycle
    best_solution.append(best_solution[0])

    return best_solution, best_cost, distances

# Run simulated annealing to find an optimized tour with distances
best_tour, best_cost, distances = simulated_annealing_with_distances(rajasthan_locations)

# Extract intermediary distances for the final route
intermediary_distances = [haversine_distance(rajasthan_locations[best_tour[i]], rajasthan_locations[best_tour[i + 1]]) for i in range(len(best_tour) - 1)]

# Print the results
print("Best tour:", best_tour)
print("Best cost:", best_cost, "km")
print("Intermediary distances:", intermediary_distances)

# Visualization function
def plot_tour(locations: Dict[str, Tuple[float, float]], tour: List[str]) -> None:
    plt.figure(figsize=(10, 8))
    for city, (lat, lon) in locations.items():
        plt.plot(lon, lat, 'o', markersize=8, label=city)
    plt.plot([locations[tour[i]][1] for i in range(len(tour))],
             [locations[tour[i]][0] for i in range(len(tour))],
             'r-')
    plt.title('Best Tour of Rajasthan')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    plt.grid(True)
    plt.show()

# Call the plot function
plot_tour(rajasthan_locations, best_tour)
