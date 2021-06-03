import pygame
import os
pygame.font.init()

WIDTH, HEIGHT = 1100, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

LETTERS_FONT = pygame.font.SysFont('georgia', 40)
alphabet = ['A', 'B', 'C', 'D', 'E', 'F',
            'G', 'H', 'I', 'J', 'K', 'L',
            'M', 'N', 'O', 'P', 'Q', 'R',
            'S', 'T', 'U', 'V', 'W', 'X',
            'Y', 'Z']

FPS = 60
HANGING_SPOT_WIDTH, HANGING_SPOT_HEIGHT = 200, 200

HANGING_SPOT_IMAGE = pygame.image.load(
    os.path.join('Hangman Assets', 'Hanging Spot.png'))
HANGING_SPOT = pygame.transform.rotate(pygame.transform.scale(
    HANGING_SPOT_IMAGE, (HANGING_SPOT_WIDTH, HANGING_SPOT_HEIGHT)), 0)


def draw_letters():
    position_x, position_y = 15, 10
    half_of_alphabet = int(len(alphabet)/2)
    for s in range(0, half_of_alphabet):
        top_letter = LETTERS_FONT.render(alphabet[s], True, BLACK)
        WIN.blit(top_letter, (position_x, position_y))
        position_x += 85

    position_x, position_y = 15, 65
    for e in range(half_of_alphabet, int(len(alphabet))):
        bottom_letter = LETTERS_FONT.render(alphabet[e], True, BLACK)
        WIN.blit(bottom_letter, (position_x, position_y))
        position_x += 85


def draw_window():
    WIN.fill(WHITE)
    draw_letters()
    WIN.blit(HANGING_SPOT, (550, 375))
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
