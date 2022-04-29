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


def main():
    global screen

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

        clock.tick(30)
        pygame.display.update()


if __name__ == "__main__":
    main()
