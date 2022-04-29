import pygame
import os
import random
import sys

pygame.init()

screen_height = 600
screen_width = 1100
screen = pygame.display.set_mode((screen_width, screen_height))

home_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

dino = {
    "run": [
        pygame.image.load(os.path.join(home_folder, "rsrc/Dino/DinoRun1.png")),
        pygame.image.load(os.path.join(home_folder, "rsrc/Dino/DinoRun2.png")),
    ],
    "jump": [
        pygame.image.load(os.path.join(home_folder, "rsrc/Dino/DinoJump.png")),
    ],
}

cactus = [
    pygame.image.load(os.path.join(home_folder, "rsrc/Cactus/LargeCactus1.png")),
    pygame.image.load(os.path.join(home_folder, "rsrc/Cactus/LargeCactus2.png")),
    pygame.image.load(os.path.join(home_folder, "rsrc/Cactus/LargeCactus3.png")),
    pygame.image.load(os.path.join(home_folder, "rsrc/Cactus/SmallCactus1.png")),
    pygame.image.load(os.path.join(home_folder, "rsrc/Cactus/SmallCactus2.png")),
    pygame.image.load(os.path.join(home_folder, "rsrc/Cactus/SmallCactus3.png")),
]

track = [pygame.image.load(os.path.join(home_folder, "rsrc/Other/Track.png"))]

font = pygame.font.Font(os.path.join(home_folder, "rsrc/Other/HeyHaters.ttf"), 20)


class Dinosaur(object):
    def __init__(self, x_pos=80, y_pos=310, jump_vel=8.5, image=dino["run"][0]):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.jump_vel = jump_vel
        self.image = image
        self.dino_run = True
        self.duno_jump = False
        self.rect = pygame.Rect(
            self.x_pos, self.y_pos, self.image.get_width(), self.image.get_height()
        )
        self.step_index = 0

    def update(self):
        pass

    def jump(self):
        pass

    def run(self):
        pass

    def draw(self, screen):
        pass


def main():
    clock = pygame.time.Clock()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((255, 255, 255, 255))
        clock.tick(30)
        pygame.display.update()


if __name__ == "__main__":
    main()
