import os
import numpy
import math
import sys
import glob
from music21 import *

from keras import optimizers
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Flatten
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
import matplotlib.pyplot as plt

# load ascii text
filename_train = "training_off.txt"
raw_text = open(filename_train).read()

filename_val = "val_off.txt"
val_text = open(filename_val).read()

# create mapping of unique chars to integers
chars = sorted(list(set(raw_text)))
chars_val = sorted(list(set(val_text)))

char_to_int = dict((c, i) for i, c in enumerate(chars))
int_to_char = dict((i,c) for i,c in enumerate(chars))

n_chars = len(raw_text)
n_chars_val = len(val_text)
n_vocab = len(chars)

# prepare the dataset of input to output pairs encoded as integers
seq_length = 50
dataX = []
dataY = []
for i in range(0, n_chars - seq_length, 1):
	seq_in = raw_text[i:i + seq_length]
	seq_out = raw_text[i + seq_length]
	dataX.append([char_to_int[char] for char in seq_in])
	dataY.append(char_to_int[seq_out])
n_seq = len(dataX)
print ("Total Sequences: ", n_seq)

dataX_val = []
dataY_val = []
for i in range(0, n_chars_val - seq_length, 1):
	seq_in = val_text[i:i + seq_length]
	seq_out = val_text[i + seq_length]
	dataX_val.append([char_to_int[char] for char in seq_in])
	dataY_val.append(char_to_int[seq_out])
n_seq_val = len(dataX_val)
print ("Total Sequences val: ", n_seq_val)


#reshape the data for input to LSTM
X = numpy.reshape(dataX, (n_seq, seq_length,1))
X = X/n_vocab
y = np_utils.to_categorical(dataY)

X_val = numpy.reshape(dataX_val, (n_seq_val, seq_length,1))
X_val = X_val/n_vocab
y_val = np_utils.to_categorical(dataY_val)

#define model 1
model_1_Off = Sequential()
model_1_Off.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
model_1_Off.add(Dropout(0.5, noise_shape=None, seed=None))
model_1_Off.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
model_1_Off.add(Dropout(0.5, noise_shape=None, seed=None))
model_1_Off.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
model_1_Off.add(Dropout(0.5, noise_shape=None, seed=None))
model_1_Off.add(Flatten())
model_1_Off.add(Dense(n_vocab, activation='softmax'))
adam = optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
model_1_Off.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])


# define the checkpoint
filepath="weights-{epoch:02d}-{loss:.4f}-{acc:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

history_1_Off = model_1_Off.fit(X, y, epochs=50, batch_size=128, callbacks=callbacks_list, validation_data = (X_val, y_val))


######################################################
#receive MIDI input and encode
MIDI_input = [72, -2, -2, -2, -1, 81, -2, -2, -2, 80, -2, -2, -2, -1, 81, -2, -2, -2, 74, -2, -2, -2, -2, -2, -2, -2, -2, -1, 71, -2, -2, -2, 72, -2, -2, -2, -2, -2, -2, -2, -2, -2, 69, -2, -2, -2, -2, 67, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, 74, -2, -2, -2]

#convert MIDI notation
length_semiquavers = len(MIDI_input)
input = numpy.zeros(length_semiquavers)
for i in range (0, length_semiquavers):
    note = MIDI_input[i]
    
    if i == 0:
        if note == -1:
            print('Cannot begin on a note off event')
            break
        else:
            if note == -2:
                print('Cannot begin on a no event')
                break
            else:
                if (note < 21) or (note > 108):
                    print('MIDI pitch is out of range')
                    break
    
    #note is a MIDI pitch
    if (note > 20) and (note < 109):
        input[i] = note
    
    #no event, ie held
    else :
        if note == -2: 
            input[i] = input[i-1]
    
        else:
        #note off   
            input[i] = 0

input = input.astype(int)   #changes to int from double
#create empty lists to store variables
nmat_dur = []
nmat_off = []
nmat_dur_char = []
nmat_dur.append('S')
nmat_dur.append('\n')
nmat_off.append('S')
nmat_off.append('\n')

nmat_MIDI = []
nmat_on = []
nmat_dur_dur = []
nmat_off_off = []

for i in range (0, length_semiquavers):
    dur = 1
    MIDI = input[i]
    
    if MIDI == 0:
	    continue # don't add in the silence
    
    on = i + 1
    
    if i == length_semiquavers-1:
       #the last element as while loop will be out of #range
	    off = on
	    nmat_on.append(on)
	    nmat_dur_dur.append(dur)
	    nmat_off_off.append(off)
	    nmat_MIDI.append(MIDI)
	    break
    
    if (input[i+1] != MIDI):
	    off = i + 1
	
    while input[i+1] == MIDI:
	    dur = dur + 1
	    off = i + 2
	    if i == length_semiquavers-2: #last element
		    break
	    i = i+1
		
	nmat_on.append(on)
    nmat_dur_dur.append(dur)
    nmat_off_off.append(off)
    nmat_MIDI.append(MIDI)
	
length_note = len(nmat_on)
for i in range (0, length_note):
    
    if i == 0:
        nmat_dur += list(str(nmat_on[i]))
        nmat_dur.append(' ')
        nmat_dur += list(str(nmat_dur_dur[i]))
        nmat_dur.append(' ')
        nmat_dur += list(str(nmat_MIDI[i]))
        nmat_dur.append('\n')

        nmat_off += list(str(nmat_on[i]))
        nmat_off.append(' ')
        nmat_off += list(str(nmat_off_off[i]))
        nmat_off.append(' ')
        nmat_off += list(str(nmat_MIDI[i]))
        nmat_off.append('\n')
	
    if i > 0:
        if (nmat_MIDI[i] != nmat_MIDI[i-1]) and (nmat_dur_dur[i] != nmat_dur_dur[i-1] - 1):
                    
            nmat_dur += list(str(nmat_on[i]))
            nmat_dur.append(' ')
            nmat_dur += list(str(nmat_dur_dur[i]))
            nmat_dur.append(' ')
            nmat_dur += list(str(nmat_MIDI[i]))
            nmat_dur.append('\n')

            nmat_off += list(str(nmat_on[i]))
            nmat_off.append(' ')
            nmat_off += list(str(nmat_off_off[i]))
            nmat_off.append(' ')
            nmat_off += list(str(nmat_MIDI[i]))
            nmat_off.append('\n')

for i in range (0, len(nmat_dur)):
   nmat_dur[i] = str(nmat_dur[i])
   nmat_off[i] = str(nmat_off[i])
   
nmat_dur = [char_to_int[i] for i in nmat_dur]
nmat_off = [char_to_int[i] for i in nmat_off]

#put into size 50 for input
len_nmat_dur = len(nmat_dur)
len_nmat_off = len(nmat_off)

if len_nmat_dur < 50:
	seed_dur = []
	seed_off = []
	zeros_dur = numpy.zeros(50 - len_nmat_dur)
	zeros_dur = zeros_dur.astype(int)
	for i in range (0, len(zeros_dur)):
		zeros_dur[i] = str(zeros_dur[i])

	seed_dur.extend(zeros_dur)
	seed_dur.extend(nmat_dur)
	print(seed_dur)
	
else:
	seed_dur = nmat_dur[0:50]
	print(seed_dur)
	seed_off = nmat_off[0:50]
	print(seed_off)

print(''.join([int_to_char[i] for i in seed_dur]))


################################################################
#Prediction
filename = 'filename.hdf5'
model_1_Off.load_weights(filename)
model_1_Off.compile(loss='categorical_crossentropy', optimizer=adam)
pattern = seed_off
print ("Seed: ")
print(''.join([int_to_char[i] for i in pattern]))

x = numpy.reshape(pattern, (1, len(pattern),1))
x = x/float(n_vocab)
prediction = model_1_Off.predict(x, verbose=0)
index = numpy.argmax(prediction)
result = int_to_char[index]
#write to new text file
f = open("Model1_Off_piece1_S.txt", "w+")
while index != 12:
    result = int_to_char[index]
    f.write(result)
    seq_in = [int_to_char[value] for value in pattern]
    sys.stdout.write(result)
	pattern.append(index)
    pattern = pattern[1:len(pattern)]
	
	x = numpy.reshape(pattern, (1, len(pattern),1))
    x = x/float(n_vocab)
    prediction = model_1_Off.predict(x, verbose=0)
    index = numpy.argmax(prediction)
f.close()

#############################################################
#Decode

#MIDI note numbers to note names
note_numbers = {
	21: 'A0',
	22: 'A#0',
	23: 'B0',
	24: 'C1',
	25: 'C#1',
	26: 'D1',
	27: 'D#1',
	28: 'E1',
	29: 'F1',
	30: 'F#1',
	31: 'G1',
	32: 'G#1',
	33: 'A1',
	34: 'A#1',
	35: 'B1',
	36: 'C2',
	37: 'C#2',
	38: 'D2',
	39: 'D#2',
	40: 'E2',
	41: 'F2',
	42: 'F#2',
	43: 'G2',
	44: 'G#2',
	45: 'A2',
	46: 'A#2',
	47: 'B2',
	48: 'C3',
	49: 'C#3',
	50: 'D3',
	51: 'D#3',
	52: 'E3',
	53: 'F3',
	54: 'F#3',
	55: 'G3',
	56: 'G#3',
	57: 'A3',
	58: 'A#3',
	59: 'B3',
	60: 'C4',
	61: 'C#4',
	62: 'D4',
	63: 'D#4',
	64: 'E4',
	65: 'F4',
	66: 'F#4',
	67: 'G4',
	68: 'G#4',
	69: 'A4',
	70: 'A#4',
	71: 'B4',
	72: 'C5',
	73: 'C#5',
	74: 'D5',
	75: 'D#5',
	76: 'E5',
	77: 'F5',
	78: 'F#5',
	79: 'G5',
	80: 'G#5',
	81: 'A5',
	82: 'A#5',
	83: 'B5',
	84: 'C6',
	85: 'C#6',
	86: 'D6',
	87: 'D#6',
	88: 'E6',
	89: 'F6',
	90: 'F#6',
	91: 'G6',
	92: 'G#6',
	93: 'A6',
	94: 'A#6',
	95: 'B6',
	96: 'C7',
	97: 'C#7',
	98: 'D7',
	99: 'D#7',
	100: 'E7',
	101: 'F7',
	102: 'F#7',
	103: 'G7',
	104: 'G#7',
	105: 'A7',
	106: 'A#7',
	107: 'B7',
	108: 'C8',
}

#DURATION ENCODING
#column 1 is on beat, column 2 is duration, column 3 is MIDI note number
#148 5 60
#148 5 71
#153 5 60

#OFF ENCODING
#column 1 is on beat, column 2 is off beat, column 3 is MIDI note number
#148 153 60
#148 153 71
#153 158 60

#change directory if needed
os.chdir("path")
for filename in glob.glob("*.txt"):
	print(filename)
	f = open(filename, "r")
	data = f.read().split('\n')
	f.close()

	in_notes = []
	for i in range (0, len(data)):
		data2 = data[i].split(' ')
		#skip S and E flags
		for j in range(0, len(data2)):
			if data2[j] == 'S':
				continue
			if data2[j] =='E':
				continue
			if data2[j] == '':
				continue
			in_notes.append(data2[j])

	#convert from chars to ints
	in_notes = numpy.array(in_notes).astype(int)
	print(in_notes)
	print(len(in_notes))

	output_notes = stream.Stream()

	for i in range (0, len(in_notes), 3):
		
		if i == len(in_notes)-2:
		#the last note in array will cause out of range
			break
			
		#all notes
		new_note = note.Note(note_numbers[in_notes[i+ 2]]) #note name
		#if using duraion encoding
		new_note.duration.quarterLength = in_notes[i+1]/4 #
		
		#if using off encoding
		new_note.duration.quarterLength = (in_notes[i+1]-in_notes[i])/4
		
		output_notes.insert(in_notes[i]/4, new_note)
		
	file = filename.split('.')
	filepath = file[0] + '.mid'
	output_notes.write('midi', fp = filepath)
	#output_notes.write('midi', fp='model1_Off_piece1_S.mid')
	#output_notes.show('text')		
	


