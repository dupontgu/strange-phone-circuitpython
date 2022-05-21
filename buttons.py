import keypad
import board
from digitalio import DigitalInOut, Direction, Pull

km = keypad.KeyMatrix(
    # NOTE!!! Double check your pinout. These are for SparkFun Thing Plus RP2040
    row_pins=(board.D18, board.D17, board.D16),
    column_pins=(board.D19, board.D20, board.D21, board.D22),
)

switch = DigitalInOut(board.SDA)  
switch.direction = Direction.INPUT
switch.pull = Pull.UP

# too lazy to figure out which row/column is which, so I just re-mapped all the numbers
key_map = [5, 2, 11, 8, 3, 0, 9, 6, 4, 1, 10, 7]

class Buttons():
    def __init__(self):
        self._pressed_keys = []

    def poll_keys(self):
        event = km.events.get()
        if event:
            if event.pressed:
                self._pressed_keys.insert(0, key_map[event.key_number])
            else:
                self._pressed_keys.remove(key_map[event.key_number])

    @property
    def pressed_key(self):
        self.poll_keys()
        return self._pressed_keys[0] if self._pressed_keys else None

    @property
    def phone_off_hook(self):
        return not switch.value

    
    