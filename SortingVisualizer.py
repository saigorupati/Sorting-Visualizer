from Algoritms import *

import pygame as pg
import random
import colorsys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

DEFAULT_COLOR = (60, 174, 163)
POINTER_COLOR = (0, 0, 0)
HIGHLIGHT_COLOR = (32, 99, 155)
BACKGROUND_COLOR = (23, 63, 95)

# Whether the list is actually random values or shuffled list of all numbers in
# data range.
TRUE_RANDOM = False
DATA_MAX_VALUE = 400

# Decreasing bar width will increase the data set size
BAR_WIDTH = 6
# This value is scaled by the item value to get the actual height
BAR_HEIGHT = 1

FPS = 30

# Callbacks for event handler
_callbacks = {}


# Gets color of the bar, from its value
def get_bar_value(value):
    adjusted_hue = value / DATA_MAX_VALUE
    rgb_raw = colorsys.hsv_to_rgb(adjusted_hue, 0.6, 1)

    return tuple(round(i * 255) for i in rgb_raw)


# Renders text in
def render_text(text):
    font = pg.font.SysFont('Product Sans', 24)

    rendered_text = font.render(text, True, (255, 255, 255))

    return rendered_text


# Pygame button class
class Button:
    def __init__(self, rect, text, value):
        self.rect = rect
        self.color = DEFAULT_COLOR
        self.text = render_text(text)
        self.value = value

    # Checks to see if the button is hovering over the button
    # Assumes that mouse click event has already been checked in the mainloop
    def is_clicked(self):
        pos = pg.mouse.get_pos()
        if self.rect[0] < pos[0] and self.rect[0] + self.rect[2] > pos[0]:
            if self.rect[1] < pos[1] and self.rect[1] + self.rect[3] > pos[1]:
                return True

        return False

    # Renders the button and the centered text
    def render(self, screen):
        pg.draw.rect(screen, self.color, self.rect)

        text_x = self.rect[0] + ((self.rect[2] - self.text.get_width()) // 2)
        text_y = self.rect[1] + ((self.rect[3] - self.text.get_height()) // 2)

        screen.blit(self.text, (text_x, text_y))


# Event handler/emit class
class Event:
    # Creates an event handler
    @staticmethod
    def on(event_name, f):
        _callbacks[event_name] = _callbacks.get(event_name, []) + [f]
        return f

    # Trigger the event handler
    @staticmethod
    def emit(event_name, *data):
        [f(*data) for f in _callbacks.get(event_name, [])]

    # Destroys an event handler
    @staticmethod
    def off(event_name, f):
        _callbacks.get(event_name, []).remove(f)


# The pygame visualizer
class Visualizer:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        pg.display.set_caption("Sorting Visualizer")

        self.arr_size = int(SCREEN_WIDTH // (BAR_WIDTH + 1))
        self.generate_data()
        self.type = ''
        self.sort_speed = 1

        Event.on('output', self.refresh)

    # Generates new random datasets
    def generate_data(self):
        if TRUE_RANDOM:
            self.arr = [random.randint(1, DATA_MAX_VALUE) for x in [0] * self.arr_size]
        else:
            self.arr = [int(DATA_MAX_VALUE * (x / self.arr_size)) for x in range(1, self.arr_size + 1)]
            random.shuffle(self.arr)

    # Start the sorting algorithm of choice
    def start(self):
        if self.type == 'insertion':
            insertion_sort(Event, self.arr)
        elif self.type == 'bubble':
            bubble_sort(Event, self.arr)
        elif self.type == 'selection':
            selection_sort(Event, self.arr)
        elif self.type == 'merge':
            merge_sort_wrapper(Event, self.arr)
        elif self.type == 'quick':
            quick_sort_wrapper(Event, self.arr)

        self.type = ''

    # Called by the "output" event.
    # Refreshes the screen with the array being sorted
    def refresh(self, pointer):
        for event in pg.event.get():
            # Quits program on exit
            if event.type == pg.QUIT:
                pg.quit()
                exit(0)
            # Speed control
            elif event.type == pg.KEYUP:
                # Increase speed
                if event.key == pg.K_EQUALS:
                    self.sort_speed += 0.5
                # Decrease speed (floored at 0, 0 is instant speed)
                elif event.key == pg.K_MINUS:
                    self.sort_speed -= 0.5
                    if self.sort_speed < 0:
                        self.sort_speed = 0

        self.clock.tick(self.sort_speed * 15)
        self.screen.fill(BACKGROUND_COLOR)

        self.screen.blit(render_text(self.type.capitalize() + f' Sort '), (10, 10))

        for i, item in enumerate(self.arr):
            color = get_bar_value(item) if i is not pointer else POINTER_COLOR

            rect = (i * (BAR_WIDTH + 1), SCREEN_HEIGHT - (BAR_HEIGHT * item), BAR_WIDTH, BAR_HEIGHT * item)

            pg.draw.rect(self.screen, color, rect)

        pg.display.update()

    # The default loop shows the buttons and the array, passes to the start
    # function one all the options are chosen.
    def mainloop(self):

        buttons = []

        buttons.append(Button((10, 10, 100, 50), 'Insertion', 'insertion'))
        buttons.append(Button((120, 10, 100, 50), 'Bubble', 'bubble'))
        buttons.append(Button((230, 10, 100, 50), 'Selection', 'selection'))
        buttons.append(Button((340, 10, 100, 50), 'Merge', 'merge'))
        buttons.append(Button((450, 10, 100, 50), 'Quick', 'quick'))

        buttons.append(Button((SCREEN_WIDTH - 110, 10, 100, 50), 'Randomize', 'randomize'))
        buttons.append(Button((SCREEN_WIDTH - 110, 70, 100, 50), 'Start', 'start'))
        last_button = None

        while True:
            for event in pg.event.get():
                # Quits program on exit
                if event.type == pg.QUIT:
                    pg.quit()
                    exit(0)
                # Checks buttons when mouse is un-clicked
                elif event.type == pg.MOUSEBUTTONUP:
                    for button in buttons:
                        if button.is_clicked():
                            # Handles the buttons if they are clicked.
                            if button.value == 'randomize':
                                self.generate_data()
                            # Sorting can be started by button or space bar
                            elif button.value == 'start':
                                if self.type != '':
                                    return
                            # Selects the sorting algorithm and highlights the
                            # chosen button
                            else:
                                if last_button is None:
                                    button.color = HIGHLIGHT_COLOR
                                    last_button = button
                                else:
                                    last_button.color = DEFAULT_COLOR
                                    button.color = HIGHLIGHT_COLOR
                                    last_button = button

                                self.type = button.value
                # Handles keyboard presses
                elif event.type == pg.KEYUP:
                    # Space to start
                    if event.key == pg.K_SPACE:
                        if self.type != '':
                            return
                    # Increase speed
                    elif event.key == pg.K_EQUALS:
                        self.sort_speed += 0.5
                    # Decrease speed (floored at 0, 0 is instant speed)
                    elif event.key == pg.K_MINUS:
                        self.sort_speed -= 0.5
                        if self.sort_speed < 0:
                            self.sort_speed = 0

            self.clock.tick(FPS)
            self.screen.fill(BACKGROUND_COLOR)

            for button in buttons:
                button.render(self.screen)

            for i, item in enumerate(self.arr):
                rect = (i * (BAR_WIDTH + 1), SCREEN_HEIGHT - (BAR_HEIGHT * item), BAR_WIDTH, BAR_HEIGHT * item)

                pg.draw.rect(self.screen, get_bar_value(item), rect)

            pg.display.update()


if __name__ == "__main__":
    pg.init()
    visualizer = Visualizer()

    while True:
        visualizer.mainloop()
        visualizer.start()
