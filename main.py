import pygame
import os

# make window
pygame.init()
WIDTH, HEIGHT = 1100, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")

# make images
images = []
for i in range(7):
    image = pygame.image.load(os.path.join(
        'images', 'hangman' + str(i) + ".png"))
    images.append(image)

# game constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FPS = 60

# game variables
hangman_status = 0
phrases = ["MILKING A COW", "EATING PIZZA",
           "AIRPLANE", "LEBRON JAMES",
           "WHITE HOUSE", "DANCING AND SINGING"]

def draw_window():
    WIN.fill(WHITE)
    WIN.blit(images[hangman_status], (100, 225))
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window()
    pygame.quit()


if __name__ == "__main__":
    main()
