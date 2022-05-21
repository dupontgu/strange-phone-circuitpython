# A Strange Phone

These repo contains the CircuitPython firmware for a prop phone that was originally built for the Stranger Things Season 4 permiere in New York.
Hear the story and learn more about the phone in this video:

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/cjzxD0_v9hM/0.jpg)](https://www.youtube.com/watch?v=cjzxD0_v9hM)

## Important Notes

* This firmware should run on any RP2040 based board with enough pins to connect the DAC, Keypad, and phone receiver switch. For my final build, I used the [SparkFun Thing Plus - RP2040](https://www.sparkfun.com/products/17745). *The pin numbers used in the Python code correspond to this dev board specifically.*
* For more details about the hardware, including a schematic, checkout the [hackaday.io project page](https://hackaday.io/project/185413-a-strange-phone).
* I did not include the sound files in this repository. 
  * All audio files should be 16 bit, 16khz WAV files. (You can experiment with different quality, but I had trouble getting any files other than these to work consistently)
  * The "clips" (call recordings) should be placed in a "clips" directory at the root of the CIRCUITPY drive.
  * The button touch tones should be placed in a "tones" directory at the root of the CIRCUITPY drive. You can generate authentic DTMF touch tones [here](https://www.audiocheck.net/audiocheck_dtmf.php)
  * The dial tone sound should be named "dial_tone.wav" and placed at the root of the CIRCUITPY drive.
  * The busy/disconnected tone sound should be named "error_tone.wav" and placed at the root of the CIRCUITPY drive.
  * See [sounds.py](sounds.py) to change any of the configuration above.
