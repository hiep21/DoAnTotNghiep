class Button {
  float X, Y, W, H; // Tọa độ X, Y và kích thước W, H của nút
  String text; // Văn bản hiển thị trên nút

  Button(float x, float y, float w, float h, String t) {
    X = x;
    Y = y;
    W = w;
    H = h;
    text = t;
  }

  // Kiểm tra xem điểm (x, y) có nằm trong khu vực của nút hay không
  boolean collide(float x, float y) {
    if (x >= X - W / 2 && x <= X + W / 2 && y >= Y - H / 2 && y <= Y + H / 2) {
      return true;
    }
    return false;
  }

  // Hiển thị nút
  void show() {
    fill(255);
    stroke(0);
    rectMode(CENTER);
    rect(X, Y, W, H);
    textSize(22);
    textAlign(CENTER, CENTER);
    fill(0);
    noStroke();
    text(text, X, Y - 3);
  }
}
