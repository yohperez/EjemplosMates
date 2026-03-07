import random
import numpy as np
from midiutil import MIDIFile

# Function to generate random MIDI notes

def generate_random_midi_notes(num_notes):
    return [random.randint(60, 72) for _ in range(num_notes)]  # MIDI notes between C4 (60) and B4 (72)

# Function to create a MIDI file

def create_midi_file(file_name, num_notes):
    midi_file = MIDIFile(1)
    midi_file.addTrackName(0, 0, "MainTrack")
    midi_file.addTempo(0, 0, 120)
    notes = generate_random_midi_notes(num_notes)

    for i, note in enumerate(notes):
        midi_file.addNote(0, 0, note, i, 1, 100)  # channel=0, pitch, time, duration, volume

    with open(file_name, "wb") as output_file:
        midi_file.writeFile(output_file)

# Main function to run the music generator

def main():
    num_notes = 16  # Number of notes to generate
    create_midi_file("algorithmic_music.mid", num_notes)

if __name__ == "__main__":
    main()