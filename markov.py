from mido import MidiFile, MidiTrack, Message, MetaMessage
from random import randint
import os

TRACKS = 100
LENGTH = 40
QUANTIZE_BASE = 5


# TODO: find more midi data / markov smoothing weights / incorporate notes and times together / put everything in same key
def get_random(given):
    result_list = []
    for i in given:
        result_list.append(i)
    return result_list[randint(0, len(given) - 1)][0]


def quantize(given_list):
    for i in range(len(given_list)):
        given_list[i] = int(QUANTIZE_BASE * round(float(given_list[i]) / QUANTIZE_BASE))


def insert_all(to_insert, model):
    for length in range(1, len(to_insert)):
        if length not in model:
            model[length] = dict()
        d1 = model[length]
        for i in range(0, len(to_insert) - length):
            prev = tuple(to_insert[i: i + length])
            next = to_insert[i + length]
            if prev in d1:
                if next in d1[prev]:
                    d1[prev][next] += 1
                else:
                    d1[prev][next] = 1
                d1[prev]["count"] += 1
            else:
                d1[prev] = {"count": 1}
                d1[prev][next] = 1


markov = dict()
notes_markov = dict()
times_markov = dict()

midi_files = os.listdir(os.path.join(os.getcwd(), "motif_midi_files"))
for file in midi_files:
    midi = MidiFile(os.path.join(os.getcwd(), "motif_midi_files", file))
    notes = []
    times = []
    for i, track in enumerate(midi.tracks):
        # print('Track {}: {}'.format(i, track.name))
        linear_time = 0
        for message in track:
            linear_time += message.time
            # print(str(message) + " linear_time: " + str(linear_time))
            if message.type == "note_on":
                notes.append(message.note)
                times.append(message.time)
    insert_all(notes, notes_markov)
    quantize(times)
    insert_all(times, times_markov)


def get_next(prev, model):
    ind = randint(0, model["count"])  # [0, model["count"]] inclusive
    running_count = 0
    print("GET NEXT", prev, model)
    for i in model:
        if i == "count":
            continue
        running_count += model[i]
        if ind <= running_count:
            return i
    print("Returned random")
    return get_random(notes_markov[1])


"""
Smooth the current markov chain:
weigh all the different possibilities
"""

def generate(dict, given_length):
    result_list = []
    result_list.append(get_random(dict[1]))
    while len(result_list) < given_length:
        added = False
        for j in range(0, len(result_list)):
            length = len(result_list) - j
            current_tuple = tuple(result_list[j: len(result_list)])
            print(len(result_list), "current list", result_list)
            # print(length, current_tuple, "NOTES", dict[length])
            # for k in dict[length]:
            #     print(type(k), k, dict[length][k])
            # print(current_tuple in dict[length])
            if len(dict) < len(result_list):
                continue
            if current_tuple in dict[length]:
                result_list.append(get_next(current_tuple, dict[length][current_tuple]))
                added = True
                print("Added using: ", current_tuple)
                break
        if not added:
            print("NOT ADDED!")
            result_list.append(get_random(dict[1]))
    print("NOTES: ", result_list)
    return result_list


def write_midi(notes, times):
    midi = MidiFile()
    midi_track = MidiTrack()
    midi.tracks.append(midi_track)

    for i in range(len(notes)):
        midi_track.append(Message("note_on", note=notes[i], velocity=100, time=times[i]))
        midi_track.append(Message("note_off", note=notes[i], velocity=0, time=times[i] + 200))
    return midi


for i in range(TRACKS):
    notes = generate(notes_markov, LENGTH)
    times = generate(times_markov, LENGTH)
    print("notes", notes)
    print("times", times)
    midi = write_midi(notes, times)
    midi.save(os.path.join(os.getcwd(), "out", "midi" + str(i + 1) + ".mid"))
    print("Saved " % midi)
