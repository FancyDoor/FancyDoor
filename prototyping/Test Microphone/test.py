import sounddevice as sd
import numpy as np


def print_sound(indata, outdata, frames, time, status):
    global sound_val 
    sound_val = np.linalg.norm(indata)*10

def main():
    global sound_val
    delta = 0
    max_delta = 100
    prev_sound_val = 0

    try:
        while delta < max_delta:
            with sd.Stream(callback=print_sound): 
                sd.sleep(50)
            delta = abs(sound_val - prev_sound_val)
            print(delta)
            prev_sound_val = sound_val
        print(f'Done.') 
    except: 
        print('\nExiting.')


if __name__=='__main__':
    main()