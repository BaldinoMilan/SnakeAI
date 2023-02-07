import pygame, sys
from pygame.locals import *

from snake import *
from neural_network import *

def exit_program():
    pygame.quit()
    sys.exit()

def argmax(outputs):
    result = -1
    past_max = -1
    for i in range(len(outputs)):
        if outputs[i]**2 >= past_max:
            result = i
            past_max = outputs[i]**2
    return result
            

def main():
    hiddens = list()
    connexions = [
        Connexion(Node("input", 0), Node("output", 0), random.uniform(-1, 1)),
        Connexion(Node("input", 0), Node("output", 1), random.uniform(-1, 1)),
        Connexion(Node("input", 0), Node("output", 2), random.uniform(-1, 1)),
        Connexion(Node("input", 0), Node("output", 3), random.uniform(-1, 1)),
        Connexion(Node("input", 0), Node("output", 4), random.uniform(-1, 1)),

        Connexion(Node("input", 1), Node("output", 0), random.uniform(-1, 1)),
        Connexion(Node("input", 1), Node("output", 1), random.uniform(-1, 1)),
        Connexion(Node("input", 1), Node("output", 2), random.uniform(-1, 1)),
        Connexion(Node("input", 1), Node("output", 3), random.uniform(-1, 1)),
        Connexion(Node("input", 1), Node("output", 4), random.uniform(-1, 1)),

        Connexion(Node("input", 2), Node("output", 0), random.uniform(-1, 1)),
        Connexion(Node("input", 2), Node("output", 1), random.uniform(-1, 1)),
        Connexion(Node("input", 2), Node("output", 2), random.uniform(-1, 1)),
        Connexion(Node("input", 2), Node("output", 3), random.uniform(-1, 1)),
        Connexion(Node("input", 2), Node("output", 4), random.uniform(-1, 1)),

        Connexion(Node("input", 3), Node("output", 0), random.uniform(-1, 1)),
        Connexion(Node("input", 3), Node("output", 1), random.uniform(-1, 1)),
        Connexion(Node("input", 3), Node("output", 2), random.uniform(-1, 1)),
        Connexion(Node("input", 3), Node("output", 3), random.uniform(-1, 1)),
        Connexion(Node("input", 3), Node("output", 4), random.uniform(-1, 1)),

        Connexion(Node("input", 4), Node("output", 0), random.uniform(-1, 1)),
        Connexion(Node("input", 4), Node("output", 1), random.uniform(-1, 1)),
        Connexion(Node("input", 4), Node("output", 2), random.uniform(-1, 1)),
        Connexion(Node("input", 4), Node("output", 3), random.uniform(-1, 1)),
        Connexion(Node("input", 4), Node("output", 4), random.uniform(-1, 1)),

        Connexion(Node("input", 5), Node("output", 0), random.uniform(-1, 1)),
        Connexion(Node("input", 5), Node("output", 1), random.uniform(-1, 1)),
        Connexion(Node("input", 5), Node("output", 2), random.uniform(-1, 1)),
        Connexion(Node("input", 5), Node("output", 3), random.uniform(-1, 1)),
        Connexion(Node("input", 5), Node("output", 4), random.uniform(-1, 1)),
    ]
    base_network = Network(6, 7, connexions, hiddens)
    
    population = Population(base_network, -1, 100, 0.3, 0.5, 0.2)
    current_network = population.get_network()
    
    pygame.init()

    pygame.display.set_caption("Snake AI")

    width, height = 1000, 500
    padding = 25
    window = pygame.display.set_mode((width, height), 0, 32)
    clock = pygame.time.Clock()
    
    rows = 15
    snake_surface = pygame.Surface((height-padding*2, height-padding*2), 0, 32)
    snake = Snake((rows//2 + 1, rows//2), (-1, 0), rows)

    framerate = 1000//6
    pygame.time.set_timer(pygame.event.Event(USEREVENT), 10)

    fitness = 0
    distance = 0
    count = 0
    
    _iter = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit_program()

            if event.type == USEREVENT:
                current_network.reset()
                current_network.inputs[0].out = (snake.body[0].pos[0] - rows/2)/(rows/2)
                current_network.inputs[1].out = (snake.body[0].pos[1] - rows/2)/(rows/2)
                current_network.inputs[2].out = snake.body[0].dir[0]
                current_network.inputs[3].out = snake.body[0].dir[1]
                current_network.inputs[4].out = (snake.snack.pos[0] - rows/2)/(rows/2)
                current_network.inputs[5].out = (snake.snack.pos[1] - rows/2)/(rows/2)
    
                up      = current_network.process(Node("output", 0))
                down    = current_network.process(Node("output", 1))
                right   = current_network.process(Node("output", 2))
                left    = current_network.process(Node("output", 3))
                nothing = current_network.process(Node("output", 4))
                result = argmax([up, down, right, left, nothing])
                if result == 0:
                    snake.changeDir((0, -1))
                elif result == 1:
                    snake.changeDir((0, 1))
                elif result == 2:
                    snake.changeDir((1, 0))
                elif result == 3:
                    snake.changeDir((-1, 0))
                
                if snake.collideSnack():
                    fitness += 1
                    _iter = 0

                _iter += 1
                distance += 1

                snake.update()

                if snake.checkLoss() or _iter == 60:
                    fitness *= distance
                    population.current_fitness += fitness
                    fitness = 0
                    count += 1

                    snake = Snake((rows//2 + 1, rows//2), (-1, 0), rows)
                    if count == 10:
                        count = 0
                        population.current_fitness = population.current_fitness / 10
                        if not population.next_network():
                            population = Population(population.best_network, population.best_fitness, 100, 0.3, 0.5, 0.2)

                        current_network = population.get_network()

                    
                    _iter = 0
                
                snake_surface.fill((0, 255, 0))
                snake.draw(snake_surface)

                pygame.time.set_timer(pygame.event.Event(USEREVENT), framerate)

            if event.type == KEYDOWN:
                if event.key == K_UP:
                    framerate = int(framerate * 0.9)
                    if framerate < 14:
                        framerate = 14
                    
                elif event.key == K_DOWN:
                    framerate = int(framerate * 1.1)
                    if framerate > 200:
                        framerate = 200
                

        window.fill((0, 0, 0))
        window.blit(snake_surface, (padding, padding))
        pygame.display.update()
        clock.tick(120)

                


if __name__ == "__main__":
    main()
