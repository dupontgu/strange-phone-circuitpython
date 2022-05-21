from sounds import Sounds
from buttons import Buttons
import time

# TWEAKABLE PARAMETERS

RING_INTERVAL = 150
RING_DURATION = 28
RING_VOLUME = 0.625
EARPIECE_VOLUME = 0.12

# END OF TWEAKABLE PARAMETERS

PICK_UP_PAUSE_DURATION = 2.5
SLEEP_POLL_INTERVAL = 0.02

buttons = Buttons()
sounds = Sounds(ring_volume=RING_VOLUME, earpiece_volume=EARPIECE_VOLUME)
ring_start_time = -RING_INTERVAL

# return the most recent (really any) button that is currently pressed
# can only play one tone at a time, so no point in tracking multiple
def poll_buttons():
    b = buttons.pressed_key
    if b is not None and buttons.phone_off_hook:
        sounds.play_button_tone(b)
    else: 
        sounds.play_button_tone(None)
    return b

# delay for `duration`, but keep periodically checking for button input
def sleep_poll(duration):
    finish = time.monotonic() + duration
    while time.monotonic() < finish:
        poll_buttons()
        time.sleep(SLEEP_POLL_INTERVAL)

def check_off_hook():
    if not buttons.phone_off_hook:
        return
    sounds.play_dial_tone()
    while sounds.playing and buttons.phone_off_hook:
        if (poll_buttons() is not None):
            sounds.play_error_tone()
    poll_buttons()
    sounds.stop_status_tone()


def ring():
    global ring_start_time
    print("ringing...", time.monotonic())
    ring_start_time = time.monotonic()
    sounds.play_ringer()
    while sounds.playing and not buttons.phone_off_hook and (time.monotonic() - ring_start_time < RING_DURATION):
        time.sleep(0.1)
    print("stopped ringing.", time.monotonic())
    sounds.stop_ringer()
    if buttons.phone_off_hook:
        print("picked up phone!")
        sleep_poll(PICK_UP_PAUSE_DURATION)
        sounds.play_random_clip()
        while(sounds.clip_playing and buttons.phone_off_hook):
            sleep_poll(0.5)
        sounds.stop_clip()
        print("call ended!")
        check_off_hook()
    ring_start_time = time.monotonic()


while True:
    if time.monotonic() - ring_start_time > RING_INTERVAL:
        ring()
    sleep_poll(0.5)
    check_off_hook()
    sounds.play_button_tone(None)