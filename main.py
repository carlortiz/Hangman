import pygame
import random
import os

pygame.init()
WIDTH, HEIGHT = 1100, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")

images = []
for i in range(7):
    image_name = 'hangman' + str(i) + '.png'
    image = pygame.image.load(os.path.join(
        'images', image_name))
    images.append(image)
losing_image = images[6]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (64, 224, 208)

FPS = 60
HALF_OF_ALPHABET = 13

DIRECTIONS_FONT = pygame.font.SysFont('comicsans', 45)
PHRASE_FONT = pygame.font.SysFont('georgia', 65)
LETTERS_FONT = pygame.font.SysFont('impact', 50)
END_MESSAGE_FONT = pygame.font.SysFont('verdana', 95)

DIRECTIONS_X = 250
HANGMAN_X, HANGMAN_Y = 100, 225
PHRASE_X, PHRASE_Y = 140, 65
BUTTONS_GAP_X = 80
BUTTONS_GAP_Y = 65
END_MESSAGE_X = 300
END_MESSAGE_Y = 300

directions_y = 70
button_x = 35
button_y = 550
second_row_y = button_y + BUTTONS_GAP_Y

phrases = ["MILKING A COW", "EATING PIZZA",
           "AIRPLANE", "LEBRON JAMES",
           "WHITE HOUSE", "DANCE AND SING"]
directions = ["Welcome to HANGMAN! Instructions below",
              " ",
              "There will be twenty-six letters. One",
              "will be light blue, and the rest will",
              "be black. Use the arrow keys to change",
              "which letter is light blue. Once the",
              "letter you have in mind is light blue,",
              "press 'enter' to check if it's correct.",
              "Press space to continue"]

letters = []
A = 65
for x in range(26):
    letter = chr(A + x)
    letters.append([letter, False, False, False])
letters_length = len(letters)

current_phrase = random.choice(phrases)
phrase_letters = []
for letter in current_phrase:
    phrase_letters.append([letter, False])


def update_letters(letters, phrase):
    for letter in letters:
        no_match = False
        if letter[2]:
            if letter[0] not in phrase:
                no_match = True
            if no_match:
                letter[3] = True


def update_phrase(phrase_letters, letters):
    for letter in letters:
        for character in phrase_letters:
            if letter[2]:
                if character[0] == letter[0]:
                    character[1] = True
    return phrase_letters


def get_hangman_image():
    global hangman_index
    hangman_index = 0
    hangman_status = 0
    for letter in letters:
        if letter[3]:
            hangman_status += 1
            hangman_index += 1
    hangman_image = images[hangman_status]
    hangman_image = pygame.transform.scale(hangman_image, (300, 265))
    return hangman_image


def get_phrase_display(phrase_letters):
    phrase = ""
    for letter in phrase_letters:
        if letter[0].isspace():
            phrase += "  "
            letter[1] = True
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
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
                return True
    return False


def check_if_enter_pressed(event, chosen_letter):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            chosen_letter[2] = True
            chosen_letter = find_nearest_letter(chosen_letter)
    return chosen_letter


def check_letter_range(change, letter_index):
    if letter_index == 0:
        change = change * -1
    elif letter_index == letters_length - 1:
        change = change * -1
    return change


def move_letter(old_letter, change, chosen_letter):
    while True:
        chosen_letter = get_new_letter(change, chosen_letter)
        letter_index = letters.index(chosen_letter)
        if chosen_letter[2]:
            if abs(change) > 1:
                chosen_letter = old_letter
                break
            change = check_letter_range(change, letter_index)
            continue
        else:
            break
    return chosen_letter


def check_for_movement(event, chosen_letter):
    change = 0
    if event.key == pygame.K_RIGHT:
        change = 1
    elif event.key == pygame.K_LEFT:
        change = -1
    elif event.key == pygame.K_UP:
        change = -HALF_OF_ALPHABET
    elif event.key == pygame.K_DOWN:
        change = HALF_OF_ALPHABET
    if change != 0:
        chosen_letter[1] = False
    old_letter = chosen_letter
    chosen_letter = move_letter(old_letter, change, chosen_letter)
    return chosen_letter


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


def draw_game_window(hangman_image, phrase_letters):
    WIN.fill(WHITE)
    phrase = get_phrase_display(phrase_letters)
    phrase = PHRASE_FONT.render(phrase, True, BLACK)
    draw_button_row(button_x, button_y, 0, HALF_OF_ALPHABET)
    draw_button_row(button_x, second_row_y,
                    HALF_OF_ALPHABET, letters_length)
    WIN.blit(phrase, (PHRASE_X, PHRASE_Y))
    WIN.blit(hangman_image, (HANGMAN_X, HANGMAN_Y))
    pygame.display.update()


def draw_ending_window(won):
    WIN.fill(WHITE)
    if won:
        end_message = "You WON!"
    else:
        end_message = "You LOST"
    end_message = END_MESSAGE_FONT.render(end_message, True, BLACK)
    WIN.blit(end_message, (END_MESSAGE_X, END_MESSAGE_Y))
    pygame.display.update()
    pygame.time.delay(7000)
    pygame.quit()

def main():
    clock = pygame.time.Clock()
    won = False
    run = True
    start_menu_status = True
    end_window_status = False
    chosen_letter = letters[0]

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if check_if_spacebar_pressed(event):
                start_menu_status = False
            if event.type == pygame.KEYDOWN:
                chosen_letter = check_for_movement(event, chosen_letter)
                chosen_letter = check_if_enter_pressed(event, chosen_letter)

        hangman_image = get_hangman_image()
        chosen_letter[1] = True
        update_letters(letters, current_phrase)
        phrase = update_phrase(phrase_letters, letters)
        if start_menu_status:
            draw_start_window()
            continue
        draw_game_window(hangman_image, phrase)
        if hangman_index == images.index(losing_image):
            end_window_status = True
        letter_missing = False
        for letter in phrase_letters:
            if not letter[1]:
                letter_missing = True
        if not letter_missing:
            won = True
            end_window_status = True
        if end_window_status:
            draw_ending_window(won)
    pygame.quit()


if __name__ == "__main__":
    main()
