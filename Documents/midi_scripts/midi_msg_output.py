import mido

# Open Mido file
midi_file_path = '/home/instrumentgroup/Downloads/Carol.mid'
midi_file = mido.MidiFile(midi_file_path)

# Print all messages
for msg in midi_file:
	print(msg)
