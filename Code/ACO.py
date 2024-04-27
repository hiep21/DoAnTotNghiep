import numpy as np
import matplotlib.pyplot as plt
import time
class AntColony:
    def __init__(self, distances, city_names, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
        self.distances = distances
        self.city_names = city_names
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = range(len(distances))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        for i in range(self.n_iterations):
            all_paths = self.gen_all_paths()
            self.spread_pheromone(all_paths, self.n_best, shortest_path=shortest_path)
            shortest_path = min(all_paths, key=lambda x: x[1])
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path
            self.pheromone *= (1 - self.decay)
        return all_time_shortest_path

    def spread_pheromone(self, all_paths, n_best, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                self.pheromone[move] += 1.0 / self.distances[move]

    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.gen_path(0)
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths

    def gen_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        while len(path) < len(self.distances) - 1:
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start))
        return path

    def gen_path_dist(self, path):
        total_dist = 0
        for (start, end) in path:
            total_dist += self.distances[start][end]
        return total_dist

    def pick_move(self, pheromone, distances, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0
        heuristic = 1.0 / np.where(distances == 0, np.inf, distances)
        row = pheromone ** self.alpha * (heuristic ** self.beta)

        if np.sum(row) == 0:
            available = [i for i in self.all_inds if i not in visited and distances[i] > 0]
            if not available:
                return start
            return np.random.choice(available)
        else:
            norm_row = row / np.sum(row)
            move = np.random.choice(self.all_inds, 1, p=norm_row)[0]
            return move

# Hàm để tạo ngẫu nhiên ma trận khoảng cách và tên các thành phố
def generate_random_cities(n_cities):
    np.random.seed(0)
    cities = np.random.rand(n_cities, 2) * 100
    distances = np.zeros((n_cities, n_cities))
    city_names = [f"City {i}" for i in range(n_cities)]

    for i in range(n_cities):
        for j in range(n_cities):
            distance = np.linalg.norm(cities[i] - cities[j])
            distances[i][j] = np.round(distance)

    return distances, city_names, cities

# Tạo ma trận khoảng cách, tên thành phố và tọa độ ngẫu nhiên cho các thành phố
distances, city_names, cities = generate_random_cities(100)

# Khởi tạo và chạy thuật toán kiến
start_time = time.time()
ant_colony = AntColony(distances, city_names, n_ants=30, n_best=1, n_iterations=20, decay=0.1, alpha=1, beta=5)
shortest_path = ant_colony.run()
end_time = time.time()

print("Shortest path: ", shortest_path)

execution_time = end_time - start_time
print(f"Execution time: {execution_time:.2f} seconds")
# Hiển thị đường đi ngắn nhất
plt.figure(figsize=(8, 6))
plt.scatter(cities[:,0], cities[:,1], c='blue', edgecolors='black', s=100)
for i, city in enumerate(city_names):
    plt.text(cities[i,0], cities[i,1], city, fontsize=12, ha='center', va='bottom')

# Vẽ đường đi ngắn nhất
path_indices = [move[0] for move in shortest_path[0]]
path_indices.append(shortest_path[0][-1][1])
for i in range(len(path_indices) - 1):
    start_city = path_indices[i]
    end_city = path_indices[i + 1]
    start_coords = cities[start_city]
    end_coords = cities[end_city]
    plt.plot([start_coords[0], end_coords[0]], [start_coords[1], end_coords[1]], color='red', linewidth=2)

plt.title('Shortest Path')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.grid(True)
plt.show()
