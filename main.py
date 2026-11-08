import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird AI - Pygame & Neuroevolution")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("courier", 22, bold=True)

def sigmoid(x):
    return 1 / (1 + math.exp(-max(-50, min(50, x))))

class Matrix:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.data = [[0.0 for _ in range(cols)] for _ in range(rows)]

    @staticmethod
    def from_array(arr):
        m = Matrix(len(arr), 1)
        for i in range(len(arr)):
            m.data[i][0] = arr[i]
        return m

    def to_array(self):
        return [self.data[i][j] for i in range(self.rows) for j in range(self.cols)]

    def randomize(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.data[i][j] = random.uniform(-1, 1)

    @staticmethod
    def multiply(a, b):
        result = Matrix(a.rows, b.cols)
        for i in range(result.rows):
            for j in range(result.cols):
                sum_val = sum(a.data[i][k] * b.data[k][j] for k in range(a.cols))
                result.data[i][j] = sum_val
        return result

    def add(self, n):
        for i in range(self.rows):
            for j in range(self.cols):
                self.data[i][j] += n.data[i][j] if isinstance(n, Matrix) else n

    @staticmethod
    def map_func(m, fn):
        result = Matrix(m.rows, m.cols)
        for i in range(m.rows):
            for j in range(m.cols):
                result.data[i][j] = fn(m.data[i][j])
        return result

class NeuralNetwork:
    def __init__(self, input_nodes, hidden_nodes=None, output_nodes=None):
        if isinstance(input_nodes, NeuralNetwork):
            nn = input_nodes
            self.input_nodes, self.hidden_nodes, self.output_nodes = nn.input_nodes, nn.hidden_nodes, nn.output_nodes
            self.weights_ih = Matrix.map_func(nn.weights_ih, lambda x: x)
            self.weights_ho = Matrix.map_func(nn.weights_ho, lambda x: x)
            self.bias_h = Matrix.map_func(nn.bias_h, lambda x: x)
            self.bias_o = Matrix.map_func(nn.bias_o, lambda x: x)
        else:
            self.input_nodes, self.hidden_nodes, self.output_nodes = input_nodes, hidden_nodes, output_nodes
            self.weights_ih = Matrix(self.hidden_nodes, self.input_nodes)
            self.weights_ih.randomize()
            self.weights_ho = Matrix(self.output_nodes, self.hidden_nodes)
            self.weights_ho.randomize()
            self.bias_h = Matrix(self.hidden_nodes, 1)
            self.bias_h.randomize()
            self.bias_o = Matrix(self.output_nodes, 1)
            self.bias_o.randomize()

    def predict(self, input_array):
        inputs = Matrix.from_array(input_array)
        hidden = Matrix.multiply(self.weights_ih, inputs)
        hidden.add(self.bias_h)
        hidden = Matrix.map_func(hidden, sigmoid)

        output = Matrix.multiply(self.weights_ho, hidden)
        output.add(self.bias_o)
        output = Matrix.map_func(output, sigmoid)

        return output.to_array()

    def mutate(self, rate):
        def mutate_val(val):
            if random.random() < rate:
                return val + random.gauss(0, 0.2)
            return val

        self.weights_ih = Matrix.map_func(self.weights_ih, mutate_val)
        self.weights_ho = Matrix.map_func(self.weights_ho, mutate_val)
        self.bias_h = Matrix.map_func(self.bias_h, mutate_val)
        self.bias_o = Matrix.map_func(self.bias_o, mutate_val)

    def copy(self):
        return NeuralNetwork(self)

class Bird:
    def __init__(self, brain=None):
        self.x = 100
        self.y = HEIGHT // 2
        self.size = 20
        self.dy = 0
        self.gravity = 0.45
        self.score = 0
        self.fitness = 0
        self.alive = True

        if brain:
            self.brain = brain.copy()
        else:
            self.brain = NeuralNetwork(4, 4, 1)

    def think(self, closest_pipe):
        if not self.alive or not closest_pipe:
            return

        inputs = [
            self.y / HEIGHT,
            (closest_pipe.x - self.x) / WIDTH,
            closest_pipe.top_height / HEIGHT,
            closest_pipe.bottom_y / HEIGHT
        ]

        output = self.brain.predict(inputs)
        if output[0] > 0.5:
            self.dy = -8

    def update(self):
        if not self.alive:
            return
        self.score += 1
        self.dy += self.gravity
        self.y += self.dy

        if self.y < 0 or self.y + self.size > HEIGHT:
            self.alive = False

    def draw(self, surface):
        if self.alive:
            pygame.draw.rect(surface, (255, 235, 59), (self.x, self.y, self.size, self.size))

class Pipe:
    def __init__(self, start_x=WIDTH):
        self.x = start_x
        self.width = 60
        self.gap = 180
        self.top_height = random.randint(80, HEIGHT - self.gap - 80)
        self.bottom_y = self.top_height + self.gap
        self.speed = 4
        self.passed = False

    def update(self):
        self.x -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, (46, 125, 50), (self.x, 0, self.width, self.top_height))
        pygame.draw.rect(surface, (46, 125, 50), (self.x, self.bottom_y, self.width, HEIGHT - self.bottom_y))

    def collide(self, bird):
        if bird.x + bird.size > self.x and bird.x < self.x + self.width:
            if bird.y < self.top_height or bird.y + bird.size > self.bottom_y:
                return True
        return False

TOTAL_BIRDS = 50
birds = [Bird() for _ in range(TOTAL_BIRDS)]
saved_birds = []
generation = 1
record_score = 0

def next_generation():
    global birds, saved_birds, generation, record_score
    
    saved_birds.sort(key=lambda b: b.score, reverse=True)
    best_bird = saved_birds[0]
    if best_bird.score > record_score:
        record_score = best_bird.score

    total_score = sum(b.score ** 2 for b in saved_birds)
    if total_score == 0:
        total_score = 1
    for b in saved_birds:
        b.fitness = (b.score ** 2) / total_score

    new_birds = []
    new_birds.append(Bird(best_bird.brain))

    for _ in range(TOTAL_BIRDS - 1):
        r = random.random()
        index = 0
        while r > 0 and index < len(saved_birds):
            r -= saved_birds[index].fitness
            index += 1
        index = max(0, index - 1)
        
        parent = saved_birds[index]
        child_brain = parent.brain.copy()
        child_brain.mutate(0.15)
        new_birds.append(Bird(child_brain))

    birds = new_birds
    saved_birds = []
    generation += 1

pipes = [Pipe(start_x=500)]
spawn_counter = 0
running = True

while running:
    clock.tick(60)
    win.fill((135, 206, 235))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    spawn_counter += 1
    if spawn_counter >= 90:
        pipes.append(Pipe())
        spawn_counter = 0

    for pipe in list(pipes):
        pipe.update()
        pipe.draw(win)
        if pipe.x + pipe.width < 0:
            pipes.remove(pipe)

    closest_pipe = None
    for pipe in pipes:
        if pipe.x + pipe.width > 100:
            closest_pipe = pipe
            break

    alive_count = 0
    for bird in birds:
        if bird.alive:
            bird.think(closest_pipe)
            bird.update()
            
            if closest_pipe and closest_pipe.collide(bird):
                bird.alive = False

            if not bird.alive:
                saved_birds.append(bird)
            else:
                bird.draw(win)
                alive_count += 1

    if alive_count == 0:
        pipes = [Pipe(start_x=500)]
        spawn_counter = 0
        next_generation()

    current_max = max([b.score for b in birds + saved_birds], default=0) // 10
    text = FONT.render(f"Gen: {generation} | Alive: {alive_count}/{TOTAL_BIRDS} | Score: {current_max} | Record: {record_score // 10}", True, (255, 255, 255))
    win.blit(text, (20, 20))

    pygame.display.flip()

pygame.quit()