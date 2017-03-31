from mido import MidiFile, MidiTrack, Message, MetaMessage
from random import randint
import os

'''
make a 128 X 128 matrix
where row represents previous note
and col represents the number of counts
for the next note based on the previous note

'''

limit = 16

count = 0
files = os.listdir(os.path.join(os.getcwd(), "motif_midi_files"))
n = 128
t = 1000
next_note_list = [[0 for x in range(n)] for y in range(n + 1)]
next_time_list = [[0 for x in range(t)] for y in range(t)]
print(len(next_note_list[0]))
for file in files:
    midi = MidiFile(os.path.join(os.getcwd(), "motif_midi_files", file))
    for i, track in enumerate(midi.tracks):
        print('Track {}: {}'.format(i, track.name))
        linear_time = 0
        prev_note = 0
        prev_time = 0
        for message in track:
            linear_time += message.time
            print(str(message) + " linear_time: " + str(linear_time))
            if message.type == "note_on":
                print(message.note)
                next_note_list[prev_note][message.note] += 1
                prev_note = message.note
    count += 1
print(len(next_note_list), len(next_note_list[0]))
for x in range(len(next_note_list)):
    total = 0
    for y in range(len(next_note_list[x])):
        if next_note_list[x][y] != 0:
            next_note_list[x][y] += total
            total = next_note_list[x][y]
        if y == len(next_note_list[x]) - 1:
            next_note_list[x][y] = total

for x in range(len(next_note_list)):
    print(next_note_list[x])

gen_list = []
ind = 0
for x in range(limit):
    rand = randint(0, next_note_list[ind][127])
    note = 0
    for y in range(len(next_note_list[ind])):
        if next_note_list[ind][y] != 0:
            if next_note_list[ind][y] > rand:
                break
            note = y
    note = randint(50, 80) if note == 0 else note
    gen_list.append(note)

# use index next_note_list[52] as default as it contains the most amount of notes
print(gen_list)
print("Number of files read: ", count)

# write to MIDI file
output_file = MidiFile()
output_track = MidiTrack()
output_file.tracks.append(output_track)

# for note in gen_list:
#     output_track.append()
"""
implement N-gram

Markov Chain:
iterate through all motifs
extract transition property
note value to the next note value
   also rhythm value

Things to think about:
   maybe want to play sumnote when it

probability distribution and generate notes
"""
