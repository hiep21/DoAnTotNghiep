import numpy as np
import random
import matplotlib.pyplot as plt
import time
class GeneticAlgorithm:
    def __init__(self, distances, n_population=10, n_generations=100, mutation_rate=0.01):
        # Khởi tạo các thuộc tính của thuật toán di truyền
        self.distances = distances  # Ma trận khoảng cách giữa các thành phố
        self.n_population = n_population  # Số lượng cá thể trong quần thể
        self.n_generations = n_generations  # Số thế hệ tiến hóa
        self.mutation_rate = mutation_rate  # Tỷ lệ đột biến
        # Tạo ngẫu nhiên các cá thể trong quần thể ban đầu
        self.population = [np.random.permutation(len(distances)) for _ in range(n_population)]
        print( self.population)
        
    def fitness(self, chromosome):
        # Hàm tính độ thích nghi của một cá thể (độ dài của đường đi)
        return sum([self.distances[chromosome[i], chromosome[i + 1]] for i in range(-1, len(chromosome) - 1)])
    
    def select(self, population):
        # Tính toán fitness cho mỗi cá thể trong quần thể. Fitness càng thấp (tổng khoảng cách càng ngắn) càng tốt.
        fitnesses = np.array([self.fitness(chromosome) for chromosome in population])
       
        # Chuyển đổi fitness thành một giá trị mà ở đó cá thể có tổng khoảng cách ngắn nhất có giá trị fitness cao nhất
        fitnesses = np.max(fitnesses) - fitnesses
    
        # Kiểm tra nếu tất cả các cá thể có cùng fitness (tức là tất cả các khoảng cách tổng là như nhau)
        if np.sum(fitnesses) == 0:
            # Nếu tất cả các fitness là bằng nhau (không có sự khác biệt), chọn một cá thể ngẫu nhiên
            return population[np.random.randint(len(population))]
    
        # Chuẩn hóa các giá trị fitness để chúng cộng lại thành 1, tạo thành một phân phối xác suất
        fitnesses = fitnesses / np.sum(fitnesses)
    
        # Chọn một cá thể từ quần thể dựa trên phân phối xác suất đã tính, cá thể càng có fitness cao càng có xác suất cao được chọn
        idx = np.random.choice(np.arange(len(population)), p=fitnesses)
    
        # Trả về cá thể đã chọn
        return population[idx]

    
    def crossover(self, parent1, parent2):
        # Xác định kích thước của cá thể, giả sử độ dài của chuỗi gen của parent1 và parent2 là như nhau
        size = len(parent1)
        
        # Khởi tạo hai cá thể con với giá trị ban đầu là 0
        c1, c2 = np.zeros(size, dtype=int), np.zeros(size, dtype=int)
        
        # Chọn ngẫu nhiên hai điểm cắt trong chuỗi gen
        cut1, cut2 = sorted(random.sample(range(size), 2))
        
        # Trích xuất và sao chép phân đoạn giữa hai điểm cắt từ mỗi bậc cha mẹ sang con
        c1_in, c2_in = parent1[cut1:cut2], parent2[cut1:cut2]
        c1[cut1:cut2], c2[cut1:cut2] = c1_in, c2_in
        print(parent1)
        # Danh sách vị trí cần điền vào các phần còn lại của cá thể con
        fill_pos = list(range(cut1)) + list(range(cut2, size))
    
        # Điền vào các vị trí còn lại trong c1 bằng các gen từ parent2 chưa xuất hiện trong c1
        for i in fill_pos:
            for j in range(size):
                if parent2[j] not in c1:
                    c1[i] = parent2[j]
                    break
    
        # Điền vào các vị trí còn lại trong c2 bằng các gen từ parent1 chưa xuất hiện trong c2
        for i in fill_pos:
            for j in range(size):
                if parent1[j] not in c2:
                    c2[i] = parent1[j]
                    break
    
        # Trả về danh sách gồm hai cá thể con đã lai tạo
        return [c1, c2]

    
    def mutate(self, chromosome):
        # Duyệt qua từng gen trong nhiễm sắc thể
        for i in range(len(chromosome)):
            # Xác suất thực hiện đột biến cho từng gen dựa trên mutation_rate
            if random.random() < self.mutation_rate:
                # Chọn ngẫu nhiên một vị trí j trong nhiễm sắc thể để hoán đổi vị trí gen
                j = random.randint(0, len(chromosome) - 1)
                # Hoán đổi gen tại vị trí i với gen tại vị trí j
                chromosome[i], chromosome[j] = chromosome[j], chromosome[i]
        # Trả về nhiễm sắc thể sau khi đã có thể xảy ra đột biến
        return chromosome

    
    def run(self):
        # Hàm chạy thuật toán di truyền qua các thế hệ
        for _ in range(self.n_generations):
            new_population = []
            for _ in range(self.n_population // 2):
                # Chọn lọc và lai ghép để tạo ra thế hệ mới
                parent1, parent2 = self.select(self.population), self.select(self.population)
                child1, child2 = self.crossover(parent1, parent2)
                new_population.extend([self.mutate(child1), self.mutate(child2)])
            self.population = new_population
        # Trả về cá thể có đường đi ngắn nhất trong quần thể cuối cùng
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

# Sử dụng hàm để tạo ma trận khoảng cách và tên các thành phố
distances, city_names, cities = generate_random_cities(10)

# Sử dụng ma trận khoảng cách để chạy thuật toán di truyền
start_time = time.time()

genetic_algorithm = GeneticAlgorithm(distances, n_population=2, n_generations=1, mutation_rate=0.1)
best_route = genetic_algorithm.run()
end_time = time.time()
print("Best route: ", best_route)
print("Best distance: ", genetic_algorithm.fitness(best_route))
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.2f} seconds")

# Vẽ các thành phố
plt.figure(figsize=(8, 6))
plt.scatter(cities[:,0], cities[:,1], c='blue', edgecolors='black', s=100)
for i, city in enumerate(city_names):
    plt.text(cities[i,0], cities[i,1], city, fontsize=12, ha='center', va='bottom')
plt.title('Randomly Generated Cities')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')

# Vẽ đường đi tốt nhất
route_coords = cities[best_route]
route_coords = np.append(route_coords, [route_coords[0]], axis=0)
plt.plot(route_coords[:,0], route_coords[:,1], linestyle='-', marker='o', markersize=5, color='red')

plt.grid(True)
plt.show()
