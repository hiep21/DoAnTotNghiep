import numpy as np
import random
import matplotlib.pyplot as plt
import time
class GeneticAlgorithm:
    def __init__(self, distances, n_population=10, n_generations=100, mutation_rate=0.01):
        self.distances = distances
        self.n_population = n_population
        self.n_generations = n_generations
        self.mutation_rate = mutation_rate
        self.population = [np.random.permutation(len(distances)) for _ in range(n_population)]

    def fitness(self, chromosome):
        return sum(self.distances[chromosome[i], chromosome[(i + 1) % len(chromosome)]] for i in range(len(chromosome)))

    def select(self, population, tournament_size=3):
        tournament = random.sample(population, tournament_size)
        best_individual = min(tournament, key=self.fitness)
        return best_individual

    def select(self, population, tournament_size=2):
        population2 = sorted(population, key=self.fitness)
        tournament = population2[:tournament_size]
        # print(tournament)
        best_individual = min(tournament, key=self.fitness)
        return best_individual

    def crossover(self, parent1, parent2):
        size = len(parent1)
        idx1, idx2 = sorted(random.sample(range(size), 2))
        new_child = parent1[idx1:idx2]
        new_child = np.concatenate((new_child, [city for city in parent2 if city not in new_child]))
        return new_child

    def mutate(self, chromosome):
        idx1, idx2 = random.sample(range(len(chromosome)), 2)
        chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]
        return chromosome

    def run(self):
        for _ in range(self.n_generations):
            new_population = []
            for _ in range(len(self.population)):
                parent1, parent2 = self.select(self.population), self.select(self.population)
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                new_population.append(child)
            self.population = sorted(new_population, key=self.fitness)
        return min(self.population, key=self.fitness)

def generate_random_cities(n_cities):
    np.random.seed(0)  # Để kết quả có thể lặp lại
    cities = np.random.rand(n_cities, 2) * 100  # Tạo ngẫu nhiên tọa độ cho các thành phố trong một phạm vi 0-100
    distances = np.zeros((n_cities, n_cities))  # Khởi tạo ma trận khoảng cách
    city_names = [f"City {i}" for i in range(n_cities)]  # Tạo tên các thành phố

    # Tính toán và làm tròn khoảng cách giữa các thành phố
    for i in range(n_cities):
        for j in range(n_cities):
            distance = np.linalg.norm(cities[i] - cities[j])
            distances[i][j] = np.round(distance)

    return distances, city_names, cities
distances, city_names, cities = generate_random_cities(100)

genetic_algorithm = GeneticAlgorithm(distances, n_population=100, n_generations = 50, mutation_rate = 0.1)
best_route = genetic_algorithm.run()
print("Best route: ", best_route)
print("Best distance: ", genetic_algorithm.fitness(best_route))