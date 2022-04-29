import pygame
import os
import random
import sys

pygame.init()

# Window Variables
screen_height = 600
screen_width = 1100
screen = pygame.display.set_mode((screen_width, screen_height))

# Location Variables
home_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

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
    global obstacles

    if len(obstacles) == 0:
        rand_int = random.randint(0, 1)
        if rand_int == 0:
            obstacles.append(SmallCactus(random.randint(1, 3)))
        elif rand_int == 1:
            obstacles.append(LargeCactus(random.randint(1, 3)))


def manage_obstacles():
    global obstacles, screen, dinosaurs

    for obstacle in obstacles:
        obstacle.draw(screen)
        obstacle.update()
        for dinosaur in dinosaurs:
            if dinosaur.rect.colliderect(obstacle.rect):
                dinosaurs.remove(dinosaur)


def main():
    global screen, game_speed, background_x_pos, background_y_pos, score, dinosaurs

    clock = pygame.time.Clock()
    dinosaurs = [Dinosaur()]

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

        manage_background()
        increase_score()
        render_score()
        clock.tick(30)
        pygame.display.update()


if __name__ == "__main__":
    main()
