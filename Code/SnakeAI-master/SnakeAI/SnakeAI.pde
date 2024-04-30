final int SIZE = 20;
final int hidden_nodes = 16;
final int hidden_layers = 2;
final int fps = 100;  //15 is ideal for self play, increasing for AI does not directly increase speed, speed is dependant on processing power

int highscore = 0;

float mutationRate = 0.05;
float defaultmutation = mutationRate;

boolean humanPlaying = false;  //false for AI, true to play yourself
boolean replayBest = true;  //shows only the best of each generation
boolean seeVision = false;  //see the snakes vision
boolean modelLoaded = false;
boolean showGraph = false; // Flag to control the graph display

ArrayList<Integer> evolution = new ArrayList<Integer>();

Button graphButton = new Button(349, 15, 100, 30, "Graph");
Button loadButton = new Button(249, 15, 100, 30, "Load");
Button saveButton = new Button(149, 15, 100, 30, "Save");
Button increaseMut = new Button(340, 85, 20, 20, "+");
Button decreaseMut = new Button(365, 85, 20, 20, "-");

EvolutionGraph graph;

Snake snake;
Snake model;

Population pop;

public void settings() {
    size(1200, 800);
}

void setup() {
    frameRate(fps);
    if (humanPlaying) {
        snake = new Snake();
    } else {
        pop = new Population(2000); // Adjust size of population
    }
}

void draw() {
    background(0);
    noFill();
    stroke(255);
    line(400, 0, 400, height);
    rectMode(CORNER);
    rect(400 + SIZE, SIZE, width - 400 - 40, height - 40);

    if (showGraph) {
        drawGraph();
    }

    if (humanPlaying) {
        snake.move();
        snake.show();
        fill(150);
        textSize(20);
        text("SCORE : " + snake.score, 500, 50);
        if (snake.dead) {
            snake = new Snake();
        }
    } else {
        if (!modelLoaded) {
            if (pop.done()) {
                highscore = pop.bestSnake.score;
                pop.calculateFitness();
                pop.naturalSelection();
            } else {
                pop.update();
                pop.show();
            }
            fill(150);
            textSize(25);
            textAlign(LEFT);
            text("GEN : " + pop.gen, 120, 60);
            text("MUTATION RATE : " + mutationRate * 100 + "%", 120, 90);
            text("SCORE : " + pop.bestSnake.score, 120, height - 45);
            text("HIGHSCORE : " + highscore, 120, height - 15);
            increaseMut.show();
            decreaseMut.show();
        } else {
            model.look();
            model.think();
            model.move();
            model.show();
            model.brain.show(0, 0, 360, 790, model.vision, model.decision);
            if (model.dead) {
                Snake newmodel = new Snake();
                newmodel.brain = model.brain.clone();
                model = newmodel;
            }
            textSize(25);
            fill(150);
            textAlign(LEFT);
            text("SCORE : " + model.score, 120, height - 45);
        }
        textAlign(LEFT);
        textSize(18);
        fill(255, 0, 0);
        text("RED < 0", 120, height - 75);
        fill(0, 0, 255);
        text("BLUE > 0", 200, height - 75);
        graphButton.show();
        loadButton.show();
        saveButton.show();
    }
}

void drawGraph() {
    if (evolution.isEmpty()) return;

    int maxValue = evolution.get(0);
    for (int score : evolution) {
        if (score > maxValue) {
            maxValue = score;
        }
    }

    stroke(255, 0, 0);
    noFill();
    beginShape();
    for (int i = 0; i < evolution.size(); i++) {
        float x = map(i, 0, evolution.size() - 1, 50, width - 50);
        float y = map(evolution.get(i), 0, maxValue, height - 50, 50);
        vertex(x, y);
    }
    endShape();
}

void mousePressed() {
    if (graphButton.collide(mouseX, mouseY)) {
        showGraph = !showGraph; // Toggle the graph display
        println("Graph button clicked");
    }
    if (loadButton.collide(mouseX, mouseY)) {
        selectInput("Load Snake Model", "fileSelectedIn");
        println("Load button clicked");
    }
    if (saveButton.collide(mouseX, mouseY)) {
        selectOutput("Save Snake Model", "fileSelectedOut");
        println("Save button clicked");
    }
    if (increaseMut.collide(mouseX, mouseY)) {
        mutationRate *= 2;
        defaultmutation = mutationRate;
        println("Increase Mutation Rate to " + mutationRate * 100 + "%");
    }
    if (decreaseMut.collide(mouseX, mouseY)) {
        mutationRate /= 2;
        defaultmutation = mutationRate;
        println("Decrease Mutation Rate to " + mutationRate * 100 + "%");
    }
}

void fileSelectedIn(File selection) {
    if (selection == null) {
        println("Window was closed or the user hit cancel.");
    } else {
        println("Loaded model from " + selection.getAbsolutePath());
        // Load the model data
    }
}

void fileSelectedOut(File selection) {
    if (selection == null) {
        println("Window was closed or the user hit cancel.");
    } else {
        println("Saved model to " + selection.getAbsolutePath());
        // Save the model data
    }
}
