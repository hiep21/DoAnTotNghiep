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
        # Sắp xếp tất cả các đường đi dựa trên độ dài (khoảng cách) của chúng
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        
        # Lặp qua n_best đường đi ngắn nhất để tăng cường pheromone
        for path, dist in sorted_paths[:n_best]:
            # Tăng cường pheromone trên mỗi bước di chuyển trong đường đi
            for move in path:
                # Cập nhật lượng pheromone trên từng đoạn đường dựa vào độ dài đoạn đường đó
                # Bằng cách lấy nghịch đảo của khoảng cách: pheromone càng cao khi khoảng cách càng ngắn
                self.pheromone[move] += 1.0 / self.distances[move]


    def gen_all_paths(self):
        # Khởi tạo một danh sách rỗng để lưu trữ tất cả các đường đi được sinh ra
        all_paths = []
        
        # Lặp qua số lượng kiến đã được định trước (n_ants)
        for i in range(self.n_ants):
            # Sinh ra một đường đi cho mỗi con kiến từ điểm bắt đầu (ví dụ: điểm 0)
            path = self.gen_path(0)
            
            # Tính toán khoảng cách tổng của đường đi vừa sinh ra
            path_distance = self.gen_path_dist(path)
            
            # Thêm cặp (đường đi, khoảng cách) vào danh sách các đường đi
            all_paths.append((path, path_distance))
            
        # Trả về danh sách chứa tất cả các đường đi và khoảng cách tương ứng của chúng
        return all_paths


    def gen_path(self, start):
        # Khởi tạo danh sách path để lưu trữ đường đi
        path = []
        # Tạo một tập hợp visited để theo dõi các đỉnh đã thăm
        visited = set()
        # Đánh dấu đỉnh bắt đầu là đã thăm
        visited.add(start)
        # Đặt đỉnh hiện tại là đỉnh bắt đầu
        prev = start
        
        # Lặp cho đến khi đường đi chưa đạt đủ số đỉnh (trừ điểm bắt đầu)
        while len(path) < len(self.distances) - 1:
            # Chọn nước đi tiếp theo dựa trên pheromone và khoảng cách, tránh các đỉnh đã thăm
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            # Thêm nước đi vào đường đi
            path.append((prev, move))
            # Cập nhật đỉnh hiện tại là đỉnh vừa di chuyển tới
            prev = move
            # Đánh dấu đỉnh mới là đã thăm
            visited.add(move)
        
        # Kết thúc đường đi bằng cách quay trở lại điểm bắt đầu
        path.append((prev, start))
        # Trả về đường đi hoàn chỉnh
        return path

    def gen_path_dist(self, path):
        total_dist = 0
        for (start, end) in path:
            total_dist += self.distances[start][end]
        return total_dist

    def pick_move(self, pheromone, distances, visited):
        # Sao chép mảng pheromone để không làm thay đổi mảng ban đầu
        pheromone = np.copy(pheromone)
        # Đặt giá trị pheromone của các điểm đã thăm bằng 0 để tránh lặp lại
        pheromone[list(visited)] = 0
        
        # Tạo một heuristic dựa trên nghịch đảo khoảng cách (vô cùng nếu khoảng cách là 0)
        heuristic = 1.0 / np.where(distances == 0, np.inf, distances)
        
        # Tính toán giá trị cho mỗi lựa chọn di chuyển dựa trên pheromone và heuristic
        row = pheromone ** self.alpha * (heuristic ** self.beta)
    
        # Nếu tổng giá trị của các lựa chọn di chuyển là 0, tức là không còn lựa chọn hợp lệ
        if np.sum(row) == 0:
            # Tạo danh sách các chỉ số có thể di chuyển, loại trừ các điểm đã thăm và khoảng cách là 0
            available = [i for i in self.all_inds if i not in visited and distances[i] > 0]
            
            # Nếu không còn điểm nào có thể di chuyển, trả về điểm bắt đầu (cần định nghĩa biến start)
            if not available:
                return start
            # Ngược lại, chọn ngẫu nhiên một điểm có thể di chuyển từ danh sách available
            return np.random.choice(available)
        else:
            # Chuẩn hóa các giá trị di chuyển để tổng là 1, tạo thành xác suất
            norm_row = row / np.sum(row)
            # Chọn một điểm di chuyển dựa trên xác suất đã tính
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
distances, city_names, cities = generate_random_cities(10)

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
