class Matrix {
  
  int rows, cols; // Số hàng và số cột của ma trận
  float[][] matrix; // Mảng hai chiều để lưu trữ các giá trị của ma trận
  
   // Constructor khởi tạo ma trận với kích thước r x c, tất cả các giá trị ban đầu là 0
   Matrix(int r, int c) {
     rows = r;
     cols = c;
     matrix = new float[rows][cols];
   }
   
   // Constructor khởi tạo ma trận từ một mảng hai chiều đã có
   Matrix(float[][] m) {
      matrix = m;
      rows = matrix.length;
      cols = matrix[0].length;
   }
   
   // In tất cả các giá trị của ma trận ra console
   void output() {
      for(int i = 0; i < rows; i++) {
         for(int j = 0; j < cols; j++) {
            print(matrix[i][j] + " "); 
         }
         println();
      }
      println();
   }
   
   // Phương thức nhân hai ma trận, trả về ma trận kết quả
   Matrix dot(Matrix n) {
     Matrix result = new Matrix(rows, n.cols);
     
     if(cols == n.rows) { // Kiểm tra điều kiện hợp lệ để nhân ma trận
        for(int i = 0; i < rows; i++) {
           for(int j = 0; j < n.cols; j++) {
              float sum = 0;
              for(int k = 0; k < cols; k++) {
                 sum += matrix[i][k] * n.matrix[k][j];
              }
              result.matrix[i][j] = sum;
           }
        }
     }
     return result;
   }
   
   // Điền giá trị ngẫu nhiên từ -1 đến 1 vào ma trận
   void randomize() {
      for(int i = 0; i < rows; i++) {
         for(int j = 0; j < cols; j++) {
            matrix[i][j] = random(-1,1); 
         }
      }
   }
   
   // Tạo ma trận một cột từ một mảng
   Matrix singleColumnMatrixFromArray(float[] arr) {
      Matrix n = new Matrix(arr.length, 1);
      for(int i = 0; i < arr.length; i++) {
         n.matrix[i][0] = arr[i]; 
      }
      return n;
   }
   
   // Chuyển ma trận thành một mảng một chiều
   float[] toArray() {
      float[] arr = new float[rows * cols];
      for(int i = 0; i < rows; i++) {
         for(int j = 0; j < cols; j++) {
            arr[j + i * cols] = matrix[i][j]; 
         }
      }
      return arr;
   }
   
   // Thêm một hàng có giá trị 1 vào cuối ma trận, thường dùng cho bias trong mạng neural
   Matrix addBias() {
      Matrix n = new Matrix(rows + 1, 1);
      for(int i = 0; i < rows; i++) {
         n.matrix[i][0] = matrix[i][0]; 
      }
      n.matrix[rows][0] = 1; // Thêm giá trị bias
      return n;
   }
   
   // Áp dụng hàm kích hoạt ReLU lên từng phần tử của ma trận
   Matrix activate() {
      Matrix n = new Matrix(rows, cols);
      for(int i = 0; i < rows; i++) {
         for(int j = 0; j < cols; j++) {
            n.matrix[i][j] = relu(matrix[i][j]); 
         }
      }
      return n;
   }
   
   // Hàm ReLU, trả về max(0, x)
   float relu(float x) {
       return max(0, x);
   }
   
   // Đột biến ma trận với tỷ lệ đột biến cho trước, điều chỉnh giá trị ngẫu nhiên
   void mutate(float mutationRate) {
      for(int i = 0; i < rows; i++) {
         for(int j = 0; j < cols; j++) {
            float rand = random(1);
            if(rand < mutationRate) { // Nếu xảy ra đột biến
               matrix[i][j] += randomGaussian() / 5; // Điều chỉnh giá trị theo phân phối Gaussian
               
               // Giới hạn giá trị của ma trận trong khoảng [-1, 1]
               if(matrix[i][j] > 1) {
                  matrix[i][j] = 1;
               }
               if(matrix[i][j] < -1) {
                 matrix[i][j] = -1;
               }
            }
         }
      }
   }
   
   // Lai tạo giữa hai ma trận, tạo ra ma trận con
   Matrix crossover(Matrix partner) {
      Matrix child = new Matrix(rows, cols);
      
      int randC = floor(random(cols)); // Chọn cột ngẫu nhiên
      int randR = floor(random(rows)); // Chọn hàng ngẫu nhiên
      
      for(int i = 0; i < rows; i++) {
         for(int j = 0; j < cols; j++) {
            if((i < randR) || (i == randR && j <= randC)) { // Chọn gen từ ma trận này
               child.matrix[i][j] = matrix[i][j];
            } else { // Chọn gen từ ma trận đối tác
              child.matrix[i][j] = partner.matrix[i][j];
            }
         }
      }
      return child;
   }
   
   // Tạo bản sao của ma trận này
   Matrix clone() {
      Matrix clone = new Matrix(rows, cols);
      for(int i = 0; i < rows; i++) {
         for(int j = 0; j < cols; j++) {
            clone.matrix[i][j] = matrix[i][j];
         }
      }
      return clone;
   }
}
