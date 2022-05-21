import board
import os
from audiocore import WaveFile, RawSample
from audiobusio import I2SOut as AudioOut
# some boards require this instead?
# from audiopwmio import PWMAudioOut as AudioOut
import audiomixer
import random
from digitalio import DigitalInOut, Direction

clips_dir = "/clips"
tones_dir = "/tones"
dial_tone_path = "dial_tone.wav"
error_tone_path = "error_tone.wav"
ringer_path = "ringer.wav"

clips = []
for s in os.listdir(clips_dir):
    clips.append(clips_dir + "/" + s)

# shuffle the clips at boot
clips.sort(key=lambda f: random.random())
clip_count = len(clips)

# button touch tones
tones = []
for s in os.listdir(tones_dir):
    tones.append(tones_dir + "/" + s)


VOICE_COUNT = 3
CLIP_STATUS_VOICE = 0
TONES_VOICE = 1
RINGER_VOICE = 2
clip_status_decoder = WaveFile(open(dial_tone_path, 'rb'))
tones_decoder = WaveFile(open(dial_tone_path, 'rb'))
ringer_decoder = WaveFile(open(ringer_path, 'rb'))

class Sounds():
    def __init__(self, ring_volume=0.75, earpiece_volume=0.12):
        self._clip_playing = True
        self._button_tone = None
        self._playing_status = False
        self._playing_error = False
        self.clip_index = 0
        # This pin should be connected to the "enable" pin of the ringer amplifier
        # We use the same I2S stream of audio for all sounds, but we programmatically enable
        # the ringer amplifier when the ringing sound is playing.
        self.amp_switch = DigitalInOut(board.SCL)  
        self.amp_switch.direction = Direction.OUTPUT
        self.mixer = audiomixer.Mixer(voice_count=VOICE_COUNT, sample_rate=16000, channel_count=1, bits_per_sample=16)
        for i in range(VOICE_COUNT):
            self.mixer.voice[i].level = earpiece_volume 
        self.mixer.voice[RINGER_VOICE].level = ring_volume
        self.audio = AudioOut(board.D27, board.D28, board.D29)
        self.audio.play(self.mixer) 
        

    def play_button_tone(self, button):
        # only restart if the button changes
        if button != self._button_tone:
            if button is not None:
                tones_decoder = WaveFile(open(tones[button], 'rb'))
                self.mixer.voice[TONES_VOICE].play(tones_decoder, loop=True)
                pass
            else:
                self.mixer.voice[TONES_VOICE].stop()
                pass
            self._button_tone = button
            self._playing_status = False

    def play_ringer(self):
        print("play ringer")
        self.amp_switch.value = True
        self.mixer.voice[RINGER_VOICE].play(ringer_decoder, loop=True)

    def stop_ringer(self):
        print("stop ringer")
        self.amp_switch.value = False
        self.mixer.voice[RINGER_VOICE].stop()

    def play_error_tone(self):
        if (self._playing_error):
            return
        self._playing_error = True
        self._playing_status = False
        self._clip_playing = None
        print("play error")
        clip_status_decoder = WaveFile(open(error_tone_path, 'rb'))
        self.mixer.voice[CLIP_STATUS_VOICE].play(clip_status_decoder, loop=True)

    def play_dial_tone(self):
        global clip_status_decoder
        if (self._playing_status):
            return 
        self._playing_error = False
        self._playing_status = True
        self._clip_playing = None
        print("play dial")
        clip_status_decoder = WaveFile(open(dial_tone_path, 'rb'))
        self.mixer.voice[CLIP_STATUS_VOICE].play(clip_status_decoder, loop=True)

    def stop_status_tone(self):
        self._playing_error = False
        self._playing_status = False
        print("stop status")
        self.mixer.voice[CLIP_STATUS_VOICE].stop()

    def play_random_clip(self):
        # self._clip_playing = random.choice(clips)
        self._clip_playing = clips[self.clip_index % clip_count]
        self.clip_index = (self.clip_index + 1) % clip_count
        print("play clip", self._clip_playing)
        clip_status_decoder = WaveFile(open(self._clip_playing, 'rb'))
        self.mixer.voice[CLIP_STATUS_VOICE].play(clip_status_decoder)

    def stop_clip(self):
        print("stop clip")
        self._clip_playing = None
        self.mixer.voice[CLIP_STATUS_VOICE].stop()

    @property
    def clip_playing(self):
        return self._clip_playing is not None and self.mixer.voice[CLIP_STATUS_VOICE].playing

    @property
    def playing(self):
        return self.mixer.playing