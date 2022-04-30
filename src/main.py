import pygame
import os
import random
import sys
import neat
import math
import pickle
import argparse

pygame.init()

# Window Variables
screen_height = 600
screen_width = 1100
screen = pygame.display.set_mode((screen_width, screen_height))

# Location Variables
home_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
config_path = os.path.join(home_folder, "rsrc/config.txt")
winner_path = os.path.join(home_folder, "rsrc/winner.nn")
input_path = os.path.join(home_folder, "rsrc/winner.nn")

# Static Game Variables
dino = {
    "run": [
        pygame.image.load(os.path.join(home_folder, "rsrc/Dino/DinoRun1.png")),
        pygame.image.load(os.path.join(home_folder, "rsrc/Dino/DinoRun2.png")),
    ],
    "jump": [
        pygame.image.load(os.path.join(home_folder, "rsrc/Dino/DinoJump.png")),
    ],
}
large_cactus = [
    pygame.image.load(os.path.join(home_folder, "rsrc/Cactus/LargeCactus1.png")),
    pygame.image.load(os.path.join(home_folder, "rsrc/Cactus/LargeCactus2.png")),
    pygame.image.load(os.path.join(home_folder, "rsrc/Cactus/LargeCactus3.png")),
]
small_cactus = [
    pygame.image.load(os.path.join(home_folder, "rsrc/Cactus/SmallCactus1.png")),
    pygame.image.load(os.path.join(home_folder, "rsrc/Cactus/SmallCactus2.png")),
    pygame.image.load(os.path.join(home_folder, "rsrc/Cactus/SmallCactus3.png")),
]
track = pygame.image.load(os.path.join(home_folder, "rsrc/Other/Track.png"))
font = pygame.font.Font(os.path.join(home_folder, "rsrc/Other/HeyHaters.ttf"), 20)

# Game Variables
game_speed = 15
background_x_pos = 0
background_y_pos = 380
score = 0
score_text = "Score: " + str(score)
obstacles = []
dinosaurs = []
obstacle_spawned = False

# Network Variables
genomes_list = []
nueral_nets = []
pop = None
use_previous_winner = True

# Program Variables
mode = "train"
generations = 10


class Dinosaur(object):
    def __init__(self, x_pos=80, y_pos=310, jump_vel=8.5, image=dino["run"][0]):
        self.default_x_pos = x_pos
        self.default_y_pos = y_pos
        self.default_jump_vel = jump_vel
        self.jump_vel = jump_vel
        self.image = image
        self.dino_run = True
        self.dino_jump = False
        self.rect = pygame.Rect(
            self.default_x_pos,
            self.default_y_pos,
            self.image.get_width(),
            self.image.get_height(),
        )
        self.step_index = 0

    def update(self):
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.step_index >= 10:
            self.step_index = 0

    def jump(self):
        global dino

        self.image = dino["jump"][0]

        if self.dino_jump:
            self.rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel <= -self.default_jump_vel:
            self.set_jump(False)
            self.jump_vel = self.default_jump_vel

    def run(self):
        global dino

        self.image = dino["run"][self.step_index // 5]
        self.rect.x = self.default_x_pos
        self.rect.y = self.default_y_pos
        self.step_index += 1

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def set_jump(self, jump: bool):
        self.dino_jump = jump
        self.dino_run = not jump


class Obstacle:
    def __init__(self, images, number_of_obstacles=1):
        global screen_width
        self.images = images
        self.type = number_of_obstacles - 1
        self.rect = self.images[self.type].get_rect()
        self.rect.x = screen_width

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.remove(self)

    def draw(self, screen):
        screen.blit(self.images[self.type], self.rect)


class EmptyPop(object):
    generation = 0


class SmallCactus(Obstacle):
    def __init__(self, number_of_obstacles=1):
        global small_cactus
        super().__init__(small_cactus, number_of_obstacles)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, number_of_obstacles=1):
        global large_cactus
        super().__init__(large_cactus, number_of_obstacles)
        self.rect.y = 300


def increase_score():
    global score, game_speed, score_text

    score += 1

    if score % 100 == 0:
        game_speed += 1

    score_text = "Score: " + str(score)


def render_score():
    global score_text, screen, font

    text = font.render(score_text, True, (0, 0, 0, 0))
    screen.blit(text, (950, 50))


def manage_background():
    global background_x_pos, background_y_pos, screen, track, game_speed

    image_width = track.get_width()
    screen.blit(track, (background_x_pos, background_y_pos))
    screen.blit(track, (image_width + background_x_pos, background_y_pos))

    if background_x_pos <= -image_width:
        background_x_pos = 0

    background_x_pos -= game_speed


def spawn_obstacles():
    global obstacles, obstacle_spawned

    if len(obstacles) == 0:
        rand_int = random.randint(0, 1)
        if rand_int == 0:
            obstacles.append(SmallCactus(random.randint(1, 3)))
        elif rand_int == 1:
            obstacles.append(LargeCactus(random.randint(1, 3)))
        obstacle_spawned = True


def remove_dino(index):
    global dinosaurs, genomes_list, nueral_nets

    dinosaurs.pop(index)
    genomes_list.pop(index)
    nueral_nets.pop(index)


def manage_obstacles():
    global obstacles, screen, dinosaurs, genomes_list, score

    for obstacle in obstacles:
        obstacle.draw(screen)
        obstacle.update()
        for i, dinosaur in enumerate(dinosaurs):
            if dinosaur.rect.colliderect(obstacle.rect):
                genomes_list[i].fitness = score
                remove_dino(i)


def training_setup(genomes, config):
    global dinosaurs, genomes_list, nueral_nets, game_speed, background_x_pos, background_y_pos, score, obstacle_spawned, obstacles, use_previous_winner, winner_path

    dinosaurs = []
    genomes_list = []
    nueral_nets = []
    obstacles = []
    game_speed = 15
    background_x_pos = 0
    background_y_pos = 380
    score = 0
    obstacle_spawned = False

    if use_previous_winner and os.path.exists(winner_path):
        with open(winner_path, "rb") as f:
            genome_winner = pickle.load(f)
        genomes_list.append(genome_winner)
        net = neat.nn.FeedForwardNetwork.create(genome_winner, config)
        nueral_nets.append(net)
        genome_winner.fitness = 0

    for genome_id, genome in genomes:
        dinosaurs.append(Dinosaur())
        genomes_list.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nueral_nets.append(net)
        genome.fitness = 0


def distance(pos_a, pos_b):
    dx = pos_a[0] - pos_b[0]
    dy = pos_a[1] - pos_b[1]
    return math.sqrt(dx**2 + dy**2)


def feed_forward():
    global dinosaurs, genomes_list, nueral_nets, obstacle_spawned, obstacles

    for i, dinosaur in enumerate(dinosaurs):
        output = nueral_nets[i].activate(
            (
                dinosaur.rect.y,
                distance((dinosaur.rect.x, dinosaur.rect.y), obstacles[0].rect.midtop)
                if len(obstacles) >= 1
                else 500,
            )
        )
        if output[0] > 0.5 and dinosaur.rect.y == dinosaur.default_y_pos:
            dinosaur.dino_jump = True
            dinosaur.dino_run = False
        obstacle_spawned = False


def statistics():
    global dinosaurs, genomes_list, game_speed, pop, font, screen, generations

    num_of_dinos_alive = font.render(
        "Dinosaurs Alive: " + str(len(dinosaurs)), True, (0, 0, 0)
    )
    generation_number = font.render(
        "Generation: " + str(pop.generation) + " / " + str(generations), True, (0, 0, 0)
    )
    game_speed_surface = font.render("Game Speed: " + str(game_speed), True, (0, 0, 0))

    screen.blit(num_of_dinos_alive, (50, 450))
    screen.blit(generation_number, (50, 480))
    screen.blit(game_speed_surface, (50, 510))


def eval(genomes, config):
    global screen, game_speed, background_x_pos, background_y_pos, score, dinosaurs, genomes_list, nueral_nets

    clock = pygame.time.Clock()

    training_setup(genomes, config)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((255, 255, 255, 255))

        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_SPACE]:
            dinosaurs[0].set_jump(True)

        for dino in dinosaurs:
            dino.update()
            dino.draw(screen)

        if len(dinosaurs) == 0:
            break

        spawn_obstacles()
        manage_obstacles()
        feed_forward()

        manage_background()
        increase_score()
        render_score()
        statistics()
        clock.tick(30)
        pygame.display.update()


def train():
    global pop, winner_path, config_path, generations

    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )
    pop = neat.Population(config)
    winner = pop.run(eval, generations)
    with open(winner_path, "wb") as f:
        pickle.dump(winner, f)


def str_to_bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    raise argparse.ArgumentTypeError("Boolean value expected.")


def train_or_run(v):
    if v == "train" or v == "run":
        return v
    raise argparse.ArgumentTypeError("'train' or 'run' expected.")


def valid_path(v):
    if v != "":
        if os.path.exists(v) and os.path.isfile(v):
            return v
        elif os.path.exists(v) and not os.path.isfile(v):
            raise argparse.ArgumentTypeError("Path must be an existing file.")
    return v


def existing_path(v):
    if v != "":
        if os.path.exists(v) and os.path.isfile(v):
            return v
        raise argparse.ArgumentTypeError("Path must be an existing file.")
    return v


def positive_int(v):
    v = int(v)
    if v > 0:
        return v
    raise argparse.ArgumentTypeError("Value must be greater than 0.")


def parse_args():
    global winner_path, use_previous_winner, mode, input_path, generations

    parser = argparse.ArgumentParser(
        description="Run a Neat Algorithm to Play / Train on the Chrome Dinosaur Game"
    )
    parser.add_argument(
        "-wp",
        "--winner_path",
        type=valid_path,
        default="",
        help="Path to save the winner file to.",
    )
    parser.add_argument(
        "-ip", "--input_path", type=existing_path, default="", help="Path to"
    )
    parser.add_argument(
        "-up",
        "--use_previous",
        type=str_to_bool,
        default="False",
        help="Use previous winner in the first generation of training.",
    )
    parser.add_argument(
        "-m",
        "--mode",
        type=train_or_run,
        default="train",
        help="Whether the program is set to 'train' or 'run' mode.",
    )
    parser.add_argument(
        "-g",
        "--generations",
        type=positive_int,
        default=10,
        help="Number of generations the networks will train for. Must be greater than 0.",
    )

    args = parser.parse_args()
    if args.winner_path != "":
        winner_path = args.winner_path
    if args.input_path != "":
        input_path = args.input_path
    use_previous_winner = args.use_previous
    mode = args.mode
    generations = args.generations


def run():
    global config_path, input_path, pop, generations

    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )

    with open(input_path, "rb") as f:
        genome_winner = pickle.load(f)

    gnomes = [(1, genome_winner)]
    pop = EmptyPop()
    generations = 0
    eval(gnomes, config)


if __name__ == "__main__":
    parse_args()
    if mode == "train":
        train()
    elif mode == "run":
        run()
