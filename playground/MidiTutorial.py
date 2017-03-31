from mido import MidiFile, MidiTrack, Message, MetaMessage
import os

givenFile = MidiFile(os.path.join(os.getcwd(), "ost_a_1.mid"))

ex2 = MidiFile()  # example2.mid / contents unchanged
ex2Track = MidiTrack()
ex2.tracks.append(ex2Track)

trans = MidiFile()  # example_transposed.mid / transpose up major 3rd
transTrack = MidiTrack()
trans.tracks.append(transTrack)

slow = MidiFile()  # example_slow.mid / every note twice as long
slowTrack = MidiTrack()
slow.tracks.append(slowTrack)

fun = MidiFile()  # example_fun.mid / anything
funTrack = MidiTrack()
fun.tracks.append(funTrack)

for i, track in enumerate(givenFile.tracks):
    # print('Track {}: {}'.format(i, track.name))
    linear_time = 0
    for message in track:
        linear_time += message.time
        # print(message.type + " " + str(message) + " tick_time: " + str(linear_time))  # prints message
        if not isinstance(message, MetaMessage):
            # print(str(message) + " " + str(linear_time))
            ex2Track.append(message.copy())
            transTrack.append(message.copy(note=message.note+4))
            slowTrack.append(message.copy(time=message.time*2))
            note = message.note
            if message.note % 2 != 0:
                note = message.note + 1
            funTrack.append(message.copy(note=note))
        else:
            ex2Track.append(message)
            transTrack.append(message)
            slowTrack.append(message)
            funTrack.append(message)

def write_midi(notes, times):
    midi = MidiFile()
    midi_track = MidiTrack()
    midi.tracks.append(midi_track)

    for i in range(len(notes)):
        message = Message("note_on", note=notes[i], velocity=100, time=times[i])
        midi_track.append(message)
    return midi

generated_midi = write_midi([56,63,66,74,69], [130, 235, 0, 600, 50])

for i, track in enumerate(generated_midi.tracks):
    # print('Track {}: {}'.format(i, track.name))
    linear_time = 0
    for message in track:
        linear_time += message.time
        print(message)

# ex2.save(os.path.join(os.getcwd(), "files", "example2.mid"))
# print("created example2.mid")
#
# trans.save(os.path.join(os.getcwd(), "files", "example_transposed.mid"))
# print("created example_transposed.mid")
#
# slow.save(os.path.join(os.getcwd(), "files", "example_slow.mid"))
# print("created example_slow.mid")
#
# fun.save(os.path.join(os.getcwd(), "files", "example_fun.mid"))
# print("created example_fun.mid")