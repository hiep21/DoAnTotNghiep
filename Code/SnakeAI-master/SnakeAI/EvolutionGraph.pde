// Lớp EvolutionGraph mở rộng từ PApplet, cho phép tạo và quản lý một cửa sổ đồ họa riêng biệt
class EvolutionGraph extends PApplet {
  
   // Constructor khởi tạo đồ họa mới
   EvolutionGraph() {
       super();  // Gọi constructor của lớp cha PApplet
       // Khởi chạy sketch với tên của lớp hiện tại làm tham số
       PApplet.runSketch(new String[] {this.getClass().getSimpleName()}, this);
   }
   
   // Cài đặt ban đầu cho kích thước cửa sổ
   void settings() {
      size(900,600);  // Đặt kích thước của cửa sổ đồ họa
   }
   
   // Cài đặt ban đầu cho đồ họa
   void setup() {
       background(150);  // Đặt màu nền
       frameRate(30);    // Đặt tốc độ khung hình cho đồ họa
   }
   
   // Phương thức vẽ lặp lại để tạo đồ họa
   void draw() {
      background(150);
      fill(0);
      strokeWeight(1);
      textSize(15);
      textAlign(CENTER,CENTER);
      text("Generation", width/2,height-10);
      translate(10,height/2);
      rotate(PI/2);
      text("Score", 0,0);
      rotate(-PI/2);
      translate(-10,-height/2);
      textSize(10);
      float x = 50;
      float y = height-35;
      float xbuff = (width-50) / 51.0;
      float ybuff = (height-50) / 200.0;  // Tính toán khoảng cách y dựa trên chiều cao có thể và giá trị tối đa là 200
      for(int i=0; i<=50; i++) {
          text(i,x,y); 
          x += xbuff;
      }
      x = 35;
      y = height-50;
      float ydif = ybuff * 10.0;
      for(int i=0; i<200; i += 10) {
          text(i,x,y); 
          line(50,y,width,y);
          y -= ydif;
      }
      strokeWeight(2);
      stroke(255,0,0);
      int score = 0;
      for(int i=0; i<evolution.size(); i++) {
          int newscore = evolution.get(i);
          line(50+(i*xbuff), height-50-(score*ybuff), 50+((i+1)*xbuff), height-50-(newscore*ybuff));
          score = newscore;
      }
      stroke(0);
      strokeWeight(5);
      line(50,0,50,height-50);
      line(50,height-50,width,height-50);
  }

   // Xử lý khi cửa sổ đồ họa được đóng
   void exit() {
      dispose();  // Giải phóng tài nguyên
      graph = null;  // Đặt biến graph về null
   }
}
