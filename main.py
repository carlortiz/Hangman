import pygame
import random
import os

# make window
pygame.init()
WIDTH, HEIGHT = 1100, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")

# make images
images = []
for i in range(7):
    image_name = 'hangman' + str(i) + '.png'
    image = pygame.image.load(os.path.join(
        'images', image_name))
    images.append(image)

# game constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (64, 224, 208)

FPS = 60
HALF_OF_ALPHABET = 13

DIRECTIONS_FONT = pygame.font.SysFont('comicsans', 45)
PHRASE_FONT = pygame.font.SysFont('georgia', 65)
LETTERS_FONT = pygame.font.SysFont('impact', 50)

DIRECTIONS_X = 275
HANGMAN_X, HANGMAN_Y = 100, 225
PHRASE_X, PHRASE_Y = 140, 65
BUTTONS_GAP_X = 80
BUTTONS_GAP_Y = 65

# game variables
directions_y = 100
button_x = 35
button_y = 550
second_row_y = button_y + BUTTONS_GAP_Y

phrases = ["MILKING A COW", "EATING PIZZA",
           "AIRPLANE", "LEBRON JAMES",
           "WHITE HOUSE", "DANCE AND SING"]
current_phrase = random.choice(phrases)
directions = ["Welcome to HANGMAN! Instructions below",
              "There will be twenty-six letters. One",
              "will be light blue, and the rest will",
              "be black. Use the arrow keys to change",
              "which letter is light blue. Once the",
              "letter you have in mind is light blue,",
              "press 'enter' to check if it's correct.",
              "Press space to continue"]
checked_letters = []

letters = []
A = 65
for x in range(26):
    letter = chr(A + x)
    letters.append([letter, False, False])
letters_length = len(letters)


def set_initial_selected_letter():
    first_letter = letters[0]
    return first_letter


def get_mystery_phrase(phrase):
    phrase_letters = []
    for character in phrase:
        phrase_letters.append([character, False])
    phrase = ""
    for letter in phrase_letters:
        if letter[0].isspace():
            phrase += "  "
            continue
        if letter[1]:
            phrase += letter[0] + " "
        else:
            phrase += "_" + " "
    return phrase


def get_button_color(chosen_letter):
    if chosen_letter:
        return LIGHT_BLUE
    return BLACK


def set_chosen_letter(letter):
    letter[1] = True


def get_new_letter(change, chosen_letter):
    next_letter = letters.index(chosen_letter) + change
    if 0 <= next_letter < letters_length:
        next_letter = letters[next_letter]
        return next_letter
    else:
        return chosen_letter


def find_nearest_letter(chosen_letter):
    distance = 1
    while True:
        next_letter = get_new_letter(distance, chosen_letter)
        if next_letter[2]:
            distance = distance * -1
            if distance > 0:
                distance += 1
        else:
            return next_letter


def check_if_spacebar_pressed(event):
    if event.key == pygame.K_SPACE:
            return True
    return False


def check_if_enter_pressed(event, chosen_letter):
    if event.type == pygame.K_RETURN:
        chosen_letter[2] = True


def check_for_movement(event, chosen_letter):
    if event.key == pygame.K_RIGHT:
        chosen_letter[1] = False
        chosen_letter = get_new_letter(1, chosen_letter)
    elif event.key == pygame.K_LEFT:
        chosen_letter[1] = False
        chosen_letter = get_new_letter(-1, chosen_letter)
    elif event.key == pygame.K_UP:
        chosen_letter[1] = False
        chosen_letter = get_new_letter(-HALF_OF_ALPHABET, chosen_letter)
    elif event.key == pygame.K_DOWN:
        chosen_letter[1] = False
        chosen_letter = get_new_letter(HALF_OF_ALPHABET, chosen_letter)
    return chosen_letter


def get_letter_checked_status(letter):
    if letter[2]:
        return True
    return False


def draw_directions(directions_y):
    for line in directions:
        message = DIRECTIONS_FONT.render(line, True, BLACK)
        WIN.blit(message, (DIRECTIONS_X, directions_y))
        directions_y += 50


def draw_button_row(button_x, button_y, start, finish):
    for letter in range(start, finish):
        letter = letters[letter]
        color = get_button_color(letter[1])
        checked_letter = letter[2]
        if not checked_letter:
            button = LETTERS_FONT.render(letter[0], True, color)
            WIN.blit(button, (button_x, button_y))
        button_x += BUTTONS_GAP_X


def draw_start_window():
    WIN.fill(WHITE)
    draw_directions(directions_y)
    pygame.display.update()


def draw_game_window(hangman_image, chosen_letter):
    WIN.fill(WHITE)
    phrase = get_mystery_phrase(current_phrase)
    phrase = PHRASE_FONT.render(phrase, True, BLACK)
    set_chosen_letter(chosen_letter)
    draw_button_row(button_x, button_y, 0, HALF_OF_ALPHABET)
    draw_button_row(button_x, second_row_y,
                    HALF_OF_ALPHABET, letters_length)
    WIN.blit(phrase, (PHRASE_X, PHRASE_Y))
    WIN.blit(hangman_image, (HANGMAN_X, HANGMAN_Y))
    pygame.display.update()


def draw_ending_window():
    pass


def main():
    clock = pygame.time.Clock()
    run = True
    start_menu_status = True
    chosen_letter = set_initial_selected_letter()

    hangman_status = 0

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if check_if_spacebar_pressed(event):
                start_menu_status = False
            if event.type == pygame.KEYDOWN:
                chosen_letter = check_for_movement(event, chosen_letter)
                check_if_enter_pressed(event, chosen_letter)


        checked_letter = get_letter_checked_status(chosen_letter)
        if checked_letter:
            chosen_letter = find_nearest_letter(chosen_letter)
        if start_menu_status:
            draw_start_window()
            continue
        # for letter in checked_letters:
            # hangman_status += 1
        hangman_image = images[hangman_status]
        hangman_image = pygame.transform.scale(hangman_image, (300, 265))
        draw_game_window(hangman_image, chosen_letter)
    pygame.quit()


if __name__ == "__main__":
    main()
