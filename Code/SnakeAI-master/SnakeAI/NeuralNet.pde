class NeuralNet {
  
  int iNodes, hNodes, oNodes, hLayers; // Số lượng nút đầu vào, ẩn, đầu ra và số lớp ẩn
  Matrix[] weights; // Mảng các ma trận trọng số cho các lớp
  
  // Constructor khởi tạo mạng nơ-ron với số lượng nút và lớp nhất định
  NeuralNet(int input, int hidden, int output, int hiddenLayers) {
    iNodes = input;
    hNodes = hidden;
    oNodes = output;
    hLayers = hiddenLayers;
    
    weights = new Matrix[hLayers+1];
    weights[0] = new Matrix(hNodes, iNodes+1); // Trọng số từ đầu vào đến lớp ẩn đầu tiên
    for(int i=1; i<hLayers; i++) {
       weights[i] = new Matrix(hNodes, hNodes+1); // Trọng số giữa các lớp ẩn
    }
    weights[weights.length-1] = new Matrix(oNodes, hNodes+1); // Trọng số từ lớp ẩn cuối cùng đến đầu ra
    
    // Khởi tạo trọng số ngẫu nhiên cho mạng
    for(Matrix w : weights) {
       w.randomize(); 
    }
  }
  
  // Đột biến trọng số của mạng với tỷ lệ đột biến mr
  void mutate(float mr) {
     for(Matrix w : weights) {
        w.mutate(mr); 
     }
  }
  
  // Tính toán đầu ra của mạng dựa trên đầu vào cho trước
  float[] output(float[] inputsArr) {
     Matrix inputs = weights[0].singleColumnMatrixFromArray(inputsArr);
     
     Matrix curr_bias = inputs.addBias(); // Thêm bias vào đầu vào
     
     // Tính toán qua các lớp ẩn
     for(int i=0; i<hLayers; i++) {
        Matrix hidden_ip = weights[i].dot(curr_bias); 
        Matrix hidden_op = hidden_ip.activate(); // Áp dụng hàm kích hoạt
        curr_bias = hidden_op.addBias(); // Thêm bias cho lớp tiếp theo
     }
     
     Matrix output_ip = weights[weights.length-1].dot(curr_bias);
     Matrix output = output_ip.activate(); // Đầu ra cuối cùng sau khi áp dụng hàm kích hoạt
     
     return output.toArray();
  }
  
  // Lai tạo hai mạng nơ-ron để tạo ra một mạng con
  NeuralNet crossover(NeuralNet partner) {
     NeuralNet child = new NeuralNet(iNodes, hNodes, oNodes, hLayers);
     for(int i=0; i<weights.length; i++) {
        child.weights[i] = weights[i].crossover(partner.weights[i]); // Lai tạo từng lớp trọng số
     }
     return child;
  }
  
  // Tạo bản sao của mạng nơ-ron này
  NeuralNet clone() {
     NeuralNet clone = new NeuralNet(iNodes, hNodes, oNodes, hLayers);
     for(int i=0; i<weights.length; i++) {
        clone.weights[i] = weights[i].clone(); // Sao chép từng lớp trọng số
     }
     
     return clone;
  }
  
  // Tải trọng số từ một mảng ma trận vào mạng
  void load(Matrix[] weight) {
      for(int i=0; i<weights.length; i++) {
         weights[i] = weight[i]; 
      }
  }
  
  // Trích xuất trọng số của mạng thành một mảng ma trận
  Matrix[] pull() {
     Matrix[] model = weights.clone();
     return model;
  }
  
  // Hiển thị mạng nơ-ron dưới dạng đồ họa, với vị trí, kích thước và thông tin trực quan hóa được chỉ định
  void show(float x, float y, float w, float h, float[] vision, float[] decision) {
     float space = 5;
     float nSize = (h - (space*(iNodes-2))) / iNodes; // Kích thước của từng nút
     float nSpace = (w - (weights.length*nSize)) / weights.length; // Khoảng cách giữa các nút
     float hBuff = (h - (space*(hNodes-1)) - (nSize*hNodes))/2; // Đệm dọc cho lớp ẩn
     float oBuff = (h - (space*(oNodes-1)) - (nSize*oNodes))/2; // Đệm dọc cho lớp đầu ra
     
     int maxIndex = 0; // Tìm chỉ số của nút đầu ra có giá trị cao nhất
     for(int i = 1; i < decision.length; i++) {
        if(decision[i] > decision[maxIndex]) {
           maxIndex = i; 
        }
     }
     
     int lc = 0;  // Biến đếm lớp
     
     // Vẽ các nút đầu vào
     for(int i = 0; i < iNodes; i++) {
         if(vision[i] != 0) {
           fill(0,255,0); // Nút hoạt động hiển thị màu xanh lá
         } else {
           fill(255); // Nút không hoạt động hiển thị màu trắng
         }
         stroke(0);
         ellipseMode(CORNER);
         ellipse(x, y+(i*(nSize+space)), nSize, nSize);
         textSize(nSize/2);
         textAlign(CENTER, CENTER);
         fill(0);
         text(i, x+(nSize/2), y+(nSize/2)+(i*(nSize+space)));
     }
     
     lc++; // Tăng biến đếm lớp
     
     // Vẽ các lớp ẩn
     for(int a = 0; a < hLayers; a++) {
       for(int i = 0; i < hNodes; i++) {
           fill(255);
           stroke(0);
           ellipseMode(CORNER);
           ellipse(x+(lc*nSize)+(lc*nSpace), y+hBuff+(i*(nSize+space)), nSize, nSize);
       }
       lc++;
     }
     
     // Vẽ các nút đầu ra
     for(int i = 0; i < oNodes; i++) {
         if(i == maxIndex) {
           fill(0,255,0); // Nút đầu ra có giá trị cao nhất hiển thị màu xanh lá
         } else {
           fill(255); // Các nút khác hiển thị màu trắng
         }
         stroke(0);
         ellipseMode(CORNER);
         ellipse(x+(lc*nSpace)+(lc*nSize), y+oBuff+(i*(nSize+space)), nSize, nSize);
     }
     
     lc = 1; // Đặt lại biến đếm lớp cho việc vẽ trọng số
     
     // Vẽ các trọng số từ đầu vào đến lớp ẩn đầu tiên
     for(int i = 0; i < weights[0].rows; i++) {
        for(int j = 0; j < weights[0].cols-1; j++) {
            if(weights[0].matrix[i][j] < 0) {
               stroke(255,0,0); // Trọng số âm hiển thị màu đỏ
            } else {
               stroke(0,0,255); // Trọng số dương hiển thị màu xanh dương
            }
            line(x+nSize, y+(nSize/2)+(j*(space+nSize)), x+nSize+nSpace, y+hBuff+(nSize/2)+(i*(space+nSize)));
        }
     }
     
     lc++;
     
     // Vẽ các trọng số giữa các lớp ẩn
     for(int a = 1; a < hLayers; a++) {
       for(int i = 0; i < weights[a].rows; i++) {
          for(int j = 0; j < weights[a].cols-1; j++) {
              if(weights[a].matrix[i][j] < 0) {
                 stroke(255,0,0);
              } else {
                 stroke(0,0,255);
              }
              line(x+(lc*nSize)+((lc-1)*nSpace), y+hBuff+(nSize/2)+(j*(space+nSize)), x+(lc*nSize)+(lc*nSpace), y+hBuff+(nSize/2)+(i*(space+nSize)));
          }
       }
       lc++;
     }
     
     // Vẽ các trọng số từ lớp ẩn cuối cùng đến lớp đầu ra
     for(int i = 0; i < weights[weights.length-1].rows; i++) {
        for(int j = 0; j < weights[weights.length-1].cols-1; j++) {
            if(weights[weights.length-1].matrix[i][j] < 0) {
               stroke(255,0,0);
            } else {
               stroke(0,0,255);
            }
            line(x+(lc*nSize)+((lc-1)*nSpace), y+hBuff+(nSize/2)+(j*(space+nSize)), x+(lc*nSize)+(lc*nSpace), y+oBuff+(nSize/2)+(i*(space+nSize)));
        }
     }
     
     // Vẽ các chữ cái biểu thị hành động trên nút đầu ra
     fill(0);
     textSize(15);
     textAlign(CENTER, CENTER);
     text("U", x+(lc*nSize)+(lc*nSpace)+nSize/2, y+oBuff+(nSize/2));
     text("D", x+(lc*nSize)+(lc*nSpace)+nSize/2, y+oBuff+space+nSize+(nSize/2));
     text("L", x+(lc*nSize)+(lc*nSpace)+nSize/2, y+oBuff+(2*space)+(2*nSize)+(nSize/2));
     text("R", x+(lc*nSize)+(lc*nSpace)+nSize/2, y+oBuff+(3*space)+(3*nSize)+(nSize/2));
  }
}
