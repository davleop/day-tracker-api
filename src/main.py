# file: main.py

import json
from signal import pause
from random import randint
from itertools import cycle
from typing import Generator
from collections import deque
from gpiozero import LED, Button, LEDMultiCharDisplay

# ~~~ constant values ~~~ #
# Noting the used pins here:
# 4, 6, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27
# G, G, GS, GP, GP, GU, GU, GC, GC, GP, GM, GS,  G,  G,  G,  G,  G,  G

# these pin numbers might need to be changed for them to work,
# just gotta play with it
button1 = Button(27)
button2 = Button(14)
button3 = Button(15)
button4 = Button(17)

start_finish_button = Button(11)

enabled_led = LED(4)

# Go see this diagram to see pin layout for display
# https://gpiozero.readthedocs.io/en/stable/_images/7seg_multi_bb.svg
display = LEDMultiCharDisplay(
    LEDMultiCharDisplay(22, 23, 24, 25, 21, 20, 16, dp=12), 26, 19, 13, 6)
display.source_delay = 0.2

LED_ON = False


def scroller(message: str, chars=4) -> Generator[str, None, None]:
    d = deque(maxlen=chars)
    for c in cycle(message):
        d.append(c)
        if len(d) == chars:
            yield ''.join(d)


def toggle_led() -> None:
    if not LED_ON:
        enabled_led.on()
        display.source = scroller(f'000{randint(1, 5)}')
    else:
        enabled_led.off()


def main():
    # This will display the message
    # It scrolls across the screen:
    #   display.source = scroller('GPIO 2ER0    ')
    start_finish_button.when_pressed = toggle_led


if __name__ == '__main__':
    # So you can Ctrl+c out of the loop without error
    # This will show other erros though
    try:
        main()
    except KeyboardInterrupt:
        pass
